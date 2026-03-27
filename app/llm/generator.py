# app/llm/generator.py

import boto3
import json
from app.llm.prompts import SYSTEM_PROMPT, build_user_prompt


class LLMGenerator:
    """
    Handles interaction with LLM (Amazon Bedrock).
    """

    def __init__(
        self,
        model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
        region: str = "us-east-1"
    ):
        self.model_id = model_id
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region
        )

    def generate(self, query: str, context_chunks: list[str]) -> dict:
        prompt = build_user_prompt(query, context_chunks)

        payload = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.2
        }

        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(payload),
            accept="application/json",
            contentType="application/json",
        )

        body = json.loads(response["body"].read())

        # Claude-style parsing
        text = body.get("content", [{}])[0].get("text", "")

        try:
            return json.loads(text)
        except Exception:
            return {
                "answer": text,
                "citations": [],
                "confidence": 0.5
            }