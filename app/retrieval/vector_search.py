from typing import List, Dict
import numpy as np


class VectorSearchEngine:
    """
    Simple in-memory vector search engine.
    Replace this with OpenSearch / Pinecone in production.
    """

    def __init__(self, embeddings: List[List[float]], records: List[Dict]):
        self.embeddings = np.array(embeddings)
        self.records = records

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5
    ) -> List[Dict]:
        query_vec = np.array(query_embedding)

        # Cosine similarity
        norms = np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_vec)
        scores = np.dot(self.embeddings, query_vec) / norms

        top_indices = scores.argsort()[-top_k:][::-1]

        results = []
        for idx in top_indices:
            results.append({
                "text": self.records[idx]["text"],
                "metadata": self.records[idx]["metadata"],
                "score": float(scores[idx]),
                "source": "vector"
            })

        return results
