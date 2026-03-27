# tests/test_ingestion.py

from app.ingestion.loader import DocumentLoader

file_location = "User/kirthiga.kalvikkarasu/Downloads/ekis-ai/app/tests/sample_document.txt"

def test_loader():
    loader = DocumentLoader()
    text = loader.load(file_location)
    assert isinstance(text, str)