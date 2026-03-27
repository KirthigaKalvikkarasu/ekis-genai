# app/retrieval/vector_search.py

import faiss
import numpy as np
from typing import List, Dict


class VectorSearchEngine:
    def __init__(self, embeddings: List[List[float]], records: List[Dict]):
        self.records = records

        self.embeddings = np.array(embeddings).astype("float32")
        dim = self.embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)

    def search(self, query_embedding: List[float], top_k: int = 5):

        query_vec = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            results.append({
                "text": self.records[idx]["text"],
                "metadata": self.records[idx]["metadata"],
                "score": float(distances[0][i]),
                "source": "vector"
            })

        return results