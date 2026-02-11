from typing import List, Dict
from sentence_transformers import CrossEncoder


class Reranker:
    """
    Cross-encoder reranker to improve precision.
    """

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        candidates: List[Dict],
        top_k: int = 3
    ) -> List[Dict]:

        pairs = [(query, c["text"]) for c in candidates]
        scores = self.model.predict(pairs)

        for c, s in zip(candidates, scores):
            c["rerank_score"] = float(s)

        ranked = sorted(
            candidates,
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return ranked[:top_k]
