# app/evaluation/llm_judge.py

from typing import Dict
from app.llm.generator import LLMGenerator


class LLMJudge:
    """
    Uses an LLM to evaluate answer quality.
    """

    def __init__(self):
        self.generator = LLMGenerator()

    def evaluate(
        self,
        query: str,
        answer: str,
        context: str
    ) -> Dict:

        prompt = f"""
Evaluate the following answer.

Question:
{query}

Context:
{context}

Answer:
{answer}

Score from 0 to 1:
- 1 = fully correct and grounded
- 0 = incorrect or hallucinated

Return JSON:
{{ "score": float, "reason": "..." }}
"""

        result = self.generator.generate(prompt, [context])
        return result