# app/embeddings/versioning.py

import hashlib
from typing import Dict


def embedding_version(
    model_id: str,
    chunk_size: int,
    chunk_overlap: int
) -> str:
    """
    Create a deterministic version hash for embeddings.
    Any change in model or chunking strategy produces
    a new version.
    """
    raw = f"{model_id}:{chunk_size}:{chunk_overlap}"
    return hashlib.sha256(raw.encode()).hexdigest()


def attach_embedding_version(
    metadata: Dict,
    version: str
) -> Dict:
    """
    Attach embedding version to chunk metadata.
    """
    enriched = metadata.copy()
    enriched["embedding_version"] = version
    return enriched
