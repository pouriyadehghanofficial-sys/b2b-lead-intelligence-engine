"""Tavily search provider"""

import logging
from typing import List, Optional
from app.search.provider import SearchProvider, SearchResult
from app.network.client import HTTPClient
import json

logger = logging.getLogger(__name__)


class TavilyProvider(SearchProvider):
    """Tavily Search API provider"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            name="Tavily",
            api_key=api_key,
            timeout=30,
        )
        self.base_url = "https://api.tavily.com/search"
        self.http_client = HTTPClient(timeout=self.timeout)
    
    def search(self, query: str, limit: int = 10, **kwargs) -> List[SearchResult]:
        """Search using Tavily API"""
        if not self.enabled or not self.api_key:
            raise Exception("Tavily provider not configured")
        
        try:
            payload = {
                "api_key": self.api_key,
                "query": query,
                "max_results": limit,
                "include_answer": False,
            }
            
            response = self.http_client.post(self.base_url, json=payload)
            data = response.json()
            
            results = []
            for result in data.get("results", []):
                results.append(SearchResult(
                    url=result.get("url", ""),
                    title=result.get("title", ""),
                    snippet=result.get("content", ""),
                    source="Tavily",
                ))
            
            logger.debug(f"Tavily: Got {len(results)} results for '{query}'")
            return results
            
        except Exception as e:
            logger.error(f"Tavily search error: {str(e)}")
            raise
    
    def get_priority(self) -> int:
        return 10
