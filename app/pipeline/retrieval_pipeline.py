# app/pipeline/retrieval_pipeline.py

from typing import List, Dict

from app.embeddings.embedder import BedrockEmbedder
from app.retrieval.vector_search import VectorSearchEngine
from app.retrieval.bm25_search import BM25SearchEngine
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.reranker import Reranker


class RetrievalPipeline:
    """
    Query → embedding → retrieval → reranking → final context
    """

    def __init__(self, records: List[Dict]):
        self.records = records

        # Extract embeddings
        self.embeddings = [r["embedding"] for r in records]

        # Components
        self.embedder = BedrockEmbedder()
        self.vector_engine = VectorSearchEngine(self.embeddings, records)
        self.bm25_engine = BM25SearchEngine(records)
        self.hybrid = HybridRetriever()
        self.reranker = Reranker()

    def run(self, query: str, top_k: int = 3) -> List[Dict]:

        # Embed query
        query_embedding = self.embedder.embed([query])[0]

        # Retrieve candidates
        vector_results = self.vector_engine.search(query_embedding, top_k=10)
        bm25_results = self.bm25_engine.search(query, top_k=10)

        # Hybrid combine
        combined = self.hybrid.combine(vector_results, bm25_results, top_k=10)

        # Rerank (precision)
        final_results = self.reranker.rerank(query, combined, top_k=top_k)

        return final_results