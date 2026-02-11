from typing import List, Dict
from collections import defaultdict


class HybridRetriever:
    """
    Combines vector and BM25 search using weighted scoring.
    """

    def __init__(
        self,
        vector_weight: float = 0.6,
        bm25_weight: float = 0.4
    ):
        self.vector_weight = vector_weight
        self.bm25_weight = bm25_weight

    def combine(
        self,
        vector_results: List[Dict],
        bm25_results: List[Dict],
        top_k: int = 5
    ) -> List[Dict]:

        combined_scores = defaultdict(float)
        combined_records = {}

        for r in vector_results:
            key = r["metadata"]["doc_id"], r["metadata"]["chunk_index"]
            combined_scores[key] += r["score"] * self.vector_weight
            combined_records[key] = r

        for r in bm25_results:
            key = r["metadata"]["doc_id"], r["metadata"]["chunk_index"]
            combined_scores[key] += r["score"] * self.bm25_weight
            combined_records[key] = r

        ranked = sorted(
            combined_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        results = []
        for key, score in ranked:
            record = combined_records[key]
            record["hybrid_score"] = score
            results.append(record)

        return results
