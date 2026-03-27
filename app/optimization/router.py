# app/optimization/router.py

def route_model(query: str) -> str:
    """
    Route query to appropriate model.
    """

    # Simple heuristic (can be upgraded later)
    if len(query.split()) < 10:
        return "cheap-model"
    return "expensive-model"