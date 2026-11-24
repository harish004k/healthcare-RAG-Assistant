import streamlit as st
from dotenv import load_dotenv

from healthcare_rag.config import Settings
from healthcare_rag.ingestion import MAX_UPLOAD_BYTES, ingest_file
from healthcare_rag.pipeline import answer_question, get_vector_store

load_dotenv()

st.set_page_config(page_title="Healthcare Document Assistant", page_icon="🩺")
st.title("Healthcare & Insurance Document Assistant")
st.caption("Ask questions about your organization's approved healthcare and insurance documents.")

st.warning(
    "This assistant is for document lookup, not medical advice, diagnosis, or emergency care. "
    "Do not upload protected health information (PHI) unless your Azure environment, agreements, "
    "access controls, and retention policies are approved for it."
)

settings = Settings.from_environment()
missing = settings.missing_for_search()
if missing:
    st.info(
        "Connect your Azure services to get started. Add the required values from "
        "`.env.example` to a local `.env` file; never commit secrets."
    )
    st.code("\n".join(missing), language="text")
    st.stop()

with st.sidebar:
    st.header("Add a document")
    uploaded_file = st.file_uploader(
        "PDF, TXT, or Markdown (max 20 MB)",
        type=["pdf", "txt", "md"],
    )
    if st.button("Upload and index", disabled=uploaded_file is None):
        blob_missing = settings.missing_for_blob()
        if blob_missing:
            st.error("Blob Storage is not configured: " + ", ".join(blob_missing))
        elif uploaded_file is not None:
            if uploaded_file.size > MAX_UPLOAD_BYTES:
                st.error("File exceeds the 20 MB upload limit.")
            else:
                with st.spinner("Uploading and indexing document..."):
                    indexed_count = ingest_file(uploaded_file, settings)
                st.success(f"Indexed {indexed_count} text chunks.")

st.subheader("Ask a question")
question = st.text_input(
    "Question",
    placeholder="For example: What documents are required to submit a claim?",
)
if st.button("Get answer", type="primary", disabled=not question.strip()):
    with st.spinner("Searching your indexed documents..."):
        result = answer_question(question.strip(), settings)
    st.markdown(result["answer"])
    if result["sources"]:
        with st.expander("Sources"):
            for source in result["sources"]:
                st.markdown(f"- {source}")

st.caption(
    "Answers may be incomplete or out of date. Verify important coverage and care decisions "
    "with the relevant clinician or insurer."
)
