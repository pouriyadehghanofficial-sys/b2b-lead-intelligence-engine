"""LLM provider implementations"""

import logging
from typing import Optional
from app.llm.providers import LLMProvider
import requests

logger = logging.getLogger(__name__)


class OpenRouterProvider(LLMProvider):
    """OpenRouter LLM provider"""
    
    def __init__(
        self,
        api_key: str,
        model: str = "openrouter/auto",
    ):
        super().__init__(
            name="OpenRouter",
            api_key=api_key,
            model=model,
        )
        self.base_url = "https://openrouter.ai/api/v1"
    
    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate using OpenRouter"""
        if not self.api_key:
            raise Exception("OpenRouter API key not configured")
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature or self.temperature,
                "max_tokens": max_tokens or self.max_tokens,
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            
            data = response.json()
            return data['choices'][0]['message']['content']
            
        except Exception as e:
            logger.error(f"OpenRouter error: {str(e)}")
            raise
    
    def get_priority(self) -> int:
        return 10


class OllamaProvider(LLMProvider):
    """Ollama local LLM provider"""
    
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "mistral",
    ):
        super().__init__(
            name="Ollama",
            api_key=None,
            model=model,
        )
        self.base_url = base_url
    
    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate using Ollama"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature or self.temperature,
                "num_predict": max_tokens or self.max_tokens,
                "stream": False,
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120,
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('response', '')
            
        except Exception as e:
            logger.error(f"Ollama error: {str(e)}")
            raise
    
    def get_priority(self) -> int:
        return 5
