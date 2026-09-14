"""Exa search provider"""

import logging
from typing import List, Optional
from app.search.provider import SearchProvider, SearchResult
from app.network.client import HTTPClient
import json

logger = logging.getLogger(__name__)


class ExaProvider(SearchProvider):
    """Exa Search API provider"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            name="Exa",
            api_key=api_key,
            timeout=30,
        )
        self.base_url = "https://api.exa.ai/search"
        self.http_client = HTTPClient(timeout=self.timeout)
    
    def search(self, query: str, limit: int = 10, **kwargs) -> List[SearchResult]:
        """Search using Exa API"""
        if not self.enabled or not self.api_key:
            raise Exception("Exa provider not configured")
        
        try:
            headers = {
                "x-api-key": self.api_key,
            }
            
            payload = {
                "query": query,
                "numResults": limit,
                "contents": {"text": True},
            }
            
            response = self.http_client.post(
                self.base_url,
                json=payload,
                headers=headers,
            )
            data = response.json()
            
            results = []
            for result in data.get("results", []):
                results.append(SearchResult(
                    url=result.get("url", ""),
                    title=result.get("title", ""),
                    snippet=result.get("text", "")[:300],
                    source="Exa",
                ))
            
            logger.debug(f"Exa: Got {len(results)} results for '{query}'")
            return results
            
        except Exception as e:
            logger.error(f"Exa search error: {str(e)}")
            raise
    
    def get_priority(self) -> int:
        return 9
