"""LLM provider base class and implementations"""

from abc import ABC, abstractmethod
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Base class for LLM providers"""
    
    def __init__(
        self,
        name: str,
        api_key: Optional[str] = None,
        model: str = "default",
        temperature: float = 0.3,
        max_tokens: int = 2000,
    ):
        self.name = name
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.enabled = api_key is not None if api_key else True
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate text using LLM"""
        pass
    
    def is_available(self) -> bool:
        """Check if provider is available"""
        return self.enabled
    
    def get_priority(self) -> int:
        """Get provider priority (higher = better)"""
        return 0
