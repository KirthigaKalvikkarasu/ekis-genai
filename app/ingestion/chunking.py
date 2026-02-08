# app/ingestion/chunking.py

from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter


class SemanticChunker:
    """
    Splits clean document text into semantically meaningful chunks
    with controlled overlap to preserve context across boundaries.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
        min_chunk_length: int = 100
    ):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.min_chunk_length = min_chunk_length

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ],
        )

    def chunk(self, text: str) -> List[str]:
        """
        Return a list of semantically coherent text chunks.
        """
        chunks = self.splitter.split_text(text)

        # Filter out very small or noisy chunks
        return [
            chunk.strip()
            for chunk in chunks
            if len(chunk.strip()) >= self.min_chunk_length
        ]
