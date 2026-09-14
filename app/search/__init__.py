"""Search module with provider routing"""
from app.search.router import SearchRouter
from app.search.provider import SearchProvider, SearchResult

__all__ = ["SearchRouter", "SearchProvider", "SearchResult"]
