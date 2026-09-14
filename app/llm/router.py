"""LLM router with fallback mechanism"""

import logging
from typing import List, Optional
from app.llm.providers import LLMProvider

logger = logging.getLogger(__name__)


class LLMRouter:
    """Route LLM requests through multiple providers with fallback"""
    
    def __init__(self):
        self.providers: List[LLMProvider] = []
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize LLM providers"""
        import os
        from app.llm.implementations import (
            OpenRouterProvider,
            OllamaProvider,
        )
        
        providers = []
        
        # OpenRouter
        if os.getenv("OPENROUTER_API_KEY"):
            providers.append(
                OpenRouterProvider(
                    api_key=os.getenv("OPENROUTER_API_KEY"),
                    model="openrouter/auto",
                )
            )
        
        # Ollama (local fallback)
        try:
            providers.append(
                OllamaProvider(
                    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                    model="mistral",
                )
            )
        except:
            pass
        
        self.providers = [p for p in providers if p.is_available()]
        self.providers.sort(key=lambda p: p.get_priority(), reverse=True)
        
        if self.providers:
            logger.info(f"Initialized {len(self.providers)} LLM providers: {[p.name for p in self.providers]}")
        else:
            logger.warning("No LLM providers available - LLM features will be limited")
    
    def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 2000,
    ) -> Optional[str]:
        """Generate text with fallback"""
        if not prompt:
            return None
        
        for provider in self.providers:
            try:
                logger.debug(f"Generating with {provider.name}")
                result = provider.generate(
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                logger.debug(f"Generated successfully with {provider.name}")
                return result
            except Exception as e:
                logger.warning(f"Generation failed with {provider.name}: {str(e)}. Trying next...")
                continue
        
        logger.error("All LLM providers failed")
        return None
    
    def is_available(self) -> bool:
        """Check if any LLM provider is available"""
        return len(self.providers) > 0
