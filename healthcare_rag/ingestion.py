from io import BytesIO
from pathlib import PurePath
from uuid import uuid4

from azure.storage.blob import BlobServiceClient
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from healthcare_rag.config import Settings
from healthcare_rag.pipeline import get_vector_store

MAX_UPLOAD_BYTES = 20 * 1024 * 1024


def parse_document(filename: str, content: bytes) -> list[Document]:
    extension = PurePath(filename).suffix.lower()
    if extension == ".pdf":
        pages = PdfReader(BytesIO(content)).pages
        documents = [
            Document(
                page_content=page.extract_text() or "",
                metadata={"source": filename, "page": page_number},
            )
            for page_number, page in enumerate(pages, start=1)
        ]
    elif extension in {".txt", ".md"}:
        documents = [
            Document(
                page_content=content.decode("utf-8"),
                metadata={"source": filename, "page": 1},
            )
        ]
    else:
        raise ValueError("Only PDF, TXT, and Markdown files are supported.")

    documents = [document for document in documents if document.page_content.strip()]
    if not documents:
        raise ValueError("No readable text was found in the uploaded document.")
    return documents


def ingest_file(uploaded_file, settings: Settings) -> int:
    content = uploaded_file.getvalue()
    if len(content) > MAX_UPLOAD_BYTES:
        raise ValueError("File exceeds the 20 MB upload limit.")

    filename = PurePath(uploaded_file.name.replace("\\", "/")).name
    documents = parse_document(filename, content)
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=True,
    ).split_documents(documents)

    blob_name = f"{uuid4().hex}/{filename}"
    blob_service = BlobServiceClient.from_connection_string(
        settings.azure_storage_connection_string
    )
    container = blob_service.get_container_client(settings.azure_storage_container)
    if not container.exists():
        container.create_container()
    container.upload_blob(name=blob_name, data=content, overwrite=False)

    for chunk in chunks:
        chunk.metadata["blob_name"] = blob_name
    get_vector_store(settings).add_documents(chunks)
    return len(chunks)
