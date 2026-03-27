# app/optimization/cache.py

from functools import lru_cache


class QueryCache:
    """
    Simple in-memory cache.
    Replace with Redis in production.
    """

    def __init__(self, maxsize: int = 1000):
        self._cache = lru_cache(maxsize=maxsize)(self._get)

    def _get(self, query: str):
        return None

    def get(self, query: str):
        return self._cache(query)

    def set(self, query: str, value):
        self._cache.cache_clear()
        self._cache = lru_cache(maxsize=1000)(lambda q: value if q == query else None)