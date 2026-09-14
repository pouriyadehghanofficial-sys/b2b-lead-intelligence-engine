"""DuckDuckGo search provider"""

import logging
from typing import List, Optional
from app.search.provider import SearchProvider, SearchResult
from app.network.client import HTTPClient

logger = logging.getLogger(__name__)


class DuckDuckGoProvider(SearchProvider):
    """DuckDuckGo Search provider (public, no API key required)"""
    
    def __init__(self):
        super().__init__(
            name="DuckDuckGo",
            api_key=None,
            timeout=30,
        )
        self.enabled = True
        self.http_client = HTTPClient(timeout=self.timeout)
    
    def search(self, query: str, limit: int = 10, **kwargs) -> List[SearchResult]:
        """Search using DuckDuckGo"""
        # Note: DuckDuckGo doesn't have a free public API
        # This is a placeholder for future implementation
        logger.info(f"DuckDuckGo provider: query '{query}' - returning empty (use Tavily/Exa)")
        return []
    
    def get_priority(self) -> int:
        return 3
