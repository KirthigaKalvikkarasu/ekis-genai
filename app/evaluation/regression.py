# app/evaluation/regression.py

from typing import List, Dict
from app.evaluation.metrics import groundedness


def run_regression_tests(test_cases: List[Dict]):
    """
    Runs evaluation on predefined test cases.
    """

    results = []

    for case in test_cases:
        score = groundedness(
            case["answer"],
            case["context"]
        )

        results.append({
            "query": case["query"],
            "score": score
        })

    avg_score = sum(r["score"] for r in results) / len(results)

    return {
        "average_score": avg_score,
        "details": results
    }