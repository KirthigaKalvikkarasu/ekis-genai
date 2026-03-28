# app/pipeline/ingestion_pipeline.py

from typing import List, Dict

from app.ingestion.loader import DocumentLoader
from app.ingestion.chunking import SemanticChunker
from app.ingestion.metadata import (
    build_document_metadata,
    build_chunk_metadata
)

from app.embeddings.embedder import BedrockEmbedder
from app.embeddings.versioning import (
    embedding_version,
    attach_embedding_version
)


class IngestionPipeline:
    """
    End-to-end ingestion pipeline:
    load → chunk → metadata → embed → version

    Produces records ready for indexing / retrieval.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
        embedding_model: str = "amazon.titan-embed-text-v1"
    ):
        # Core components
        self.loader = DocumentLoader()
        self.chunker = SemanticChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.embedder = BedrockEmbedder(model_id=embedding_model)

        # Versioning (CRITICAL)
        self.embedding_version = embedding_version(
            model_id=embedding_model,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def run(self, file_path: str) -> List[Dict]:
        """
        Process a document and return index-ready records.
        """

        # Load document
        text = self.loader.load(file_path)

        # Build document-level metadata
        doc_metadata = build_document_metadata(file_path)

        # Chunk document
        chunks = self.chunker.chunk(text)

        if not chunks:
            raise ValueError("No valid chunks generated")

        # Generate embeddings
        embeddings = self.embedder.embed(chunks)

        if len(embeddings) != len(chunks):
            raise RuntimeError("Mismatch between chunks and embeddings")

        records = []

        # Combine everything
        for idx, (chunk, vector) in enumerate(zip(chunks, embeddings)):

            # Chunk metadata
            chunk_metadata = build_chunk_metadata(doc_metadata, idx)

            # Attach embedding version
            chunk_metadata = attach_embedding_version(
                chunk_metadata,
                self.embedding_version
            )

            record = {
                "text": chunk,
                "embedding": vector,
                "metadata": chunk_metadata
            }

            records.append(record)

        return records