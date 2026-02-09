# app/embeddings/embedder.py

from typing import List
import boto3
import json
import logging

logger = logging.getLogger(__name__)


class BedrockEmbedder:
    """
    Generates vector embeddings for text using Amazon Bedrock.
    This layer is intentionally isolated to allow model swaps
    without impacting ingestion or retrieval.
    """

    def __init__(
        self,
        model_id: str = "amazon.titan-embed-text-v1",
        region: str = "us-east-1"
    ):
        self.model_id = model_id
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region
        )

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of text chunks.
        """
        if not texts:
            return []

        embeddings: List[List[float]] = []

        for text in texts:
            payload = {"inputText": text}

            try:
                response = self.client.invoke_model(
                    modelId=self.model_id,
                    body=json.dumps(payload),
                    accept="application/json",
                    contentType="application/json",
                )

                body = json.loads(response["body"].read())
                embeddings.append(body["embedding"])

            except Exception as exc:
                logger.exception("Failed to generate embedding")
                raise RuntimeError(f"Embedding failed: {exc}")

        return embeddings
