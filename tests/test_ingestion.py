import pytest
from io import BytesIO
from pypdf import PdfWriter

from healthcare_rag.ingestion import parse_document


def test_parse_text_file_preserves_source_metadata():
    documents = parse_document("benefits.txt", b"Claims are reviewed within 30 days.")

    assert len(documents) == 1
    assert documents[0].page_content == "Claims are reviewed within 30 days."
    assert documents[0].metadata == {"source": "benefits.txt", "page": 1}


def test_parse_pdf_with_no_extractable_text_is_rejected():
    output = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.write(output)

    with pytest.raises(ValueError, match="No readable text"):
        parse_document("empty.pdf", output.getvalue())


def test_parse_unsupported_file_type_is_rejected():
    with pytest.raises(ValueError, match="Only PDF, TXT, and Markdown"):
        parse_document("scan.png", b"image bytes")
