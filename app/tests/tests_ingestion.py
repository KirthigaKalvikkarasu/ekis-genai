# tests/test_ingestion.py

from app.ingestion.loader import DocumentLoader

file_location = "/Users/kirthiga.kalvikkarasu/Projects/ekis-genai/app/tests/sample_document.pdf"

def test_loader():
    loader = DocumentLoader()
    text = loader.load(file_location)
    assert isinstance(text, str)