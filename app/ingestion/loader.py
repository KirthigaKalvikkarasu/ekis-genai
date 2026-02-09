# app/ingestion/loader.py

from pathlib import Path
from typing import Union
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
from docx import Document


class DocumentLoader:
    """
    Loads documents of various formats and returns clean text.
    Supported formats: PDF, DOCX, HTML
    """

    def load(self, file_path: Union[str, Path]) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist")

        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return self._load_pdf(path)
        elif suffix == ".docx":
            return self._load_docx(path)
        elif suffix in [".html", ".htm"]:
            return self._load_html(path)
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

    def _load_pdf(self, path: Path) -> str:
        doc = fitz.open(path)
        text = []

        for page in doc:
            page_text = page.get_text("text")
            if page_text:
                text.append(page_text)

        return self._normalize("\n".join(text))

    def _load_docx(self, path: Path) -> str:
        doc = Document(path)
        text = [p.text for p in doc.paragraphs if p.text.strip()]
        return self._normalize("\n".join(text))

    def _load_html(self, path: Path) -> str:
        with open(path, encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        # Remove scripts & styles
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        return self._normalize(soup.get_text(separator="\n"))

    def _normalize(self, text: str) -> str:
        # Basic normalization 
        text = text.replace("\u00a0", " ")
        text = "\n".join(
            line.strip() for line in text.splitlines() if line.strip()
        )
        return text


# Testing Lines
# if __name__ == "__main__":
#     loader = DocumentLoader()
#     print(loader.load("Rev_Recon_User_Guide.pdf")[:500])
