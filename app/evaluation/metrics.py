# app/evaluation/metrics.py

from typing import List


def groundedness(answer: str, context_chunks: List[str]) -> float:
    """
    Simple groundedness check:
    measures overlap between answer and context.
    """
    answer_words = set(answer.lower().split())

    context_text = " ".join(context_chunks).lower()
    context_words = set(context_text.split())

    overlap = answer_words.intersection(context_words)

    if not answer_words:
        return 0.0

    return len(overlap) / len(answer_words)


def answer_length(answer: str) -> int:
    return len(answer.split())


def cost_estimate(tokens: int, price_per_1k: float = 0.003) -> float:
    """
    Rough cost estimator (adjust based on model).
    """
    return (tokens / 1000) * price_per_1k