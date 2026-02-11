from typing import List, Dict
from rank_bm25 import BM25Okapi


class BM25SearchEngine:
    """
    Keyword-based lexical search using BM25.
    """

    def __init__(self, records: List[Dict]):
        self.records = records
        self.corpus = [r["text"].lower().split() for r in records]
        self.bm25 = BM25Okapi(self.corpus)

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict]:
        query_tokens = query.lower().split()
        scores = self.bm25.get_scores(query_tokens)

        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "text": self.records[idx]["text"],
                "metadata": self.records[idx]["metadata"],
                "score": float(scores[idx]),
                "source": "bm25"
            })

        return results
