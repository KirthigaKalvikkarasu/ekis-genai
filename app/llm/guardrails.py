# app/llm/guardrails.py

from typing import Dict


def validate_response(response: Dict, min_confidence: float = 0.6):
    """
    Basic guardrails for LLM output.
    """

    if not isinstance(response, dict):
        raise ValueError("Invalid response format")

    if "answer" not in response:
        raise ValueError("Missing answer")

    if "confidence" in response and response["confidence"] < min_confidence:
        raise ValueError("Low confidence response")

    if not response.get("citations"):
        raise ValueError("Missing citations")

    return True