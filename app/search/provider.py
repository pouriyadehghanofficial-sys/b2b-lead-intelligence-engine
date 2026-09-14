"""Search provider base class"""

from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Result from a search query"""
    url: str
    title: str
    snippet: str
    source: str
    published_date: Optional[datetime] = None
    
    def __hash__(self):
        return hash(self.url)
    
    def __eq__(self, other):
        if not isinstance(other, SearchResult):
            return False
        return self.url == other.url


class SearchProvider(ABC):
    """Base class for search providers"""
    
    def __init__(
        self,
        name: str,
        api_key: Optional[str] = None,
        timeout: int = 30,
        retries: int = 3,
    ):
        self.name = name
        self.api_key = api_key
        self.timeout = timeout
        self.retries = retries
        self.enabled = api_key is not None if api_key else True
    
    @abstractmethod
    def search(self, query: str, limit: int = 10, **kwargs) -> List[SearchResult]:
        """Execute search query"""
        pass
    
    def is_available(self) -> bool:
        """Check if provider is available"""
        return self.enabled
    
    def get_priority(self) -> int:
        """Get provider priority (higher = better)"""
        return 0
