"""Google search provider (using public results)"""

import logging
from typing import List, Optional
from app.search.provider import SearchProvider, SearchResult
from app.network.client import HTTPClient
import logging

logger = logging.getLogger(__name__)


class GoogleProvider(SearchProvider):
    """Google Search via public results (no API key required)"""
    
    def __init__(self):
        super().__init__(
            name="Google",
            api_key=None,
            timeout=30,
        )
        self.enabled = True
        self.http_client = HTTPClient(timeout=self.timeout)
    
    def search(self, query: str, limit: int = 10, **kwargs) -> List[SearchResult]:
        """Search using Google via fallback method"""
        # Note: Public Google search scraping is limited
        # In production, you'd use SerpAPI, GoogleSearch API, or similar
        logger.info(f"Google provider: query '{query}' - returning empty (use Tavily/Exa for actual results)")
        return []
    
    def get_priority(self) -> int:
        return 4
