"""Search router with fallback mechanism"""

import logging
from typing import List, Optional, Dict
from app.search.provider import SearchResult, SearchProvider
from app.search.providers.tavily import TavilyProvider
from app.search.providers.exa import ExaProvider
from app.search.providers.google import GoogleProvider
from app.search.providers.duckduckgo import DuckDuckGoProvider

logger = logging.getLogger(__name__)


class SearchRouter:
    """Route search queries through multiple providers with fallback"""
    
    def __init__(self):
        self.providers: List[SearchProvider] = []
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize and sort providers by priority"""
        import os
        
        # Try to add providers in priority order
        providers = [
            TavilyProvider(api_key=os.getenv("TAVILY_API_KEY")),
            ExaProvider(api_key=os.getenv("EXA_API_KEY")),
            GoogleProvider(),
            DuckDuckGoProvider(),
        ]
        
        # Filter to only available providers
        self.providers = [p for p in providers if p.is_available()]
        
        # Sort by priority
        self.providers.sort(key=lambda p: p.get_priority(), reverse=True)
        
        logger.info(f"Initialized {len(self.providers)} search providers: {[p.name for p in self.providers]}")
    
    def search(
        self,
        query: str,
        limit: int = 10,
        providers: Optional[List[str]] = None,
    ) -> List[SearchResult]:
        """Search through providers with fallback"""
        if not query:
            return []
        
        results: Dict[str, SearchResult] = {}  # Use dict to deduplicate by URL
        
        # Filter providers if specified
        search_providers = self.providers
        if providers:
            search_providers = [p for p in self.providers if p.name in providers]
        
        if not search_providers:
            logger.warning(f"No search providers available. Query: {query}")
            return []
        
        # Try each provider with fallback
        for provider in search_providers:
            try:
                logger.debug(f"Searching with {provider.name}: {query}")
                provider_results = provider.search(query, limit=limit)
                
                # Add results, avoiding duplicates
                for result in provider_results:
                    if result.url not in results:
                        results[result.url] = result
                
                # Return early if we have enough results
                if len(results) >= limit:
                    logger.debug(f"Got enough results ({len(results)}) from {provider.name}")
                    break
                    
            except Exception as e:
                logger.warning(f"Search failed with {provider.name}: {str(e)}. Trying next provider...")
                continue
        
        final_results = list(results.values())[:limit]
        logger.info(f"Total results: {len(final_results)} from {len(self.providers)} providers")
        return final_results
    
    def add_provider(self, provider: SearchProvider):
        """Add a custom search provider"""
        self.providers.append(provider)
        self.providers.sort(key=lambda p: p.get_priority(), reverse=True)
        logger.info(f"Added provider: {provider.name}")
    
    def get_available_providers(self) -> List[str]:
        """Get list of available provider names"""
        return [p.name for p in self.providers]
