# app/ingestion/metadata.py

from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import uuid


def build_document_metadata(file_path: str) -> Dict[str, Any]:
    """
    Metadata that applies to the entire document.
    """
    path = Path(file_path)

    return {
        "doc_id": str(uuid.uuid4()),
        "source": path.name,
        "file_type": path.suffix.lower(),
        "ingested_at": datetime.utcnow().isoformat()
    }


def build_chunk_metadata(
    document_metadata: Dict[str, Any],
    chunk_index: int
) -> Dict[str, Any]:
    """
    Metadata for an individual chunk.
    """
    return {
        **document_metadata,
        "chunk_index": chunk_index
    }
