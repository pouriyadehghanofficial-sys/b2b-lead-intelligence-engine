"""Application settings and configuration management"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
import yaml
import logging

logger = logging.getLogger(__name__)


@dataclass
class SearchProviderConfig:
    """Configuration for search providers"""
    enabled: bool = True
    api_key: Optional[str] = None
    timeout: int = 30
    retries: int = 3
    backoff_factor: float = 1.5
    rate_limit: Optional[int] = None  # requests per minute
    priority: int = 0  # higher = better


@dataclass
class LLMProviderConfig:
    """Configuration for LLM providers"""
    enabled: bool = True
    api_key: Optional[str] = None
    model: str = "default"
    temperature: float = 0.3
    max_tokens: int = 2000
    timeout: int = 60
    retries: int = 2
    base_url: Optional[str] = None
    priority: int = 0


@dataclass
class Settings:
    """Main application settings"""
    
    # App
    debug: bool = False
    log_level: str = "INFO"
    cache_enabled: bool = True
    checkpoint_dir: str = "./checkpoints"
    data_dir: str = "./data"
    db_path: str = "./data/leads.db"
    
    # Search
    search_providers: Dict[str, SearchProviderConfig] = field(default_factory=dict)
    search_timeout: int = 30
    search_retries: int = 3
    
    # LLM
    llm_providers: Dict[str, LLMProviderConfig] = field(default_factory=dict)
    enable_llm: bool = True
    llm_timeout: int = 60
    
    # Network
    http_proxy: Optional[str] = None
    https_proxy: Optional[str] = None
    verify_ssl: bool = True
    user_agent: str = "B2B-Lead-Intelligence-Engine/1.0"
    
    # Pipeline
    batch_size: int = 10
    max_concurrent_requests: int = 5
    enable_deduplication: bool = True
    confidence_threshold: float = 0.3
    lead_score_threshold: float = 0.5
    
    # Phone
    country_code: str = "+98"  # Iran
    phone_validation_strict: bool = False
    
    # Industry
    industry_cache_enabled: bool = True
    
    def __post_init__(self):
        """Post-initialization processing"""
        # Create directories
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize default providers if not set
        if not self.search_providers:
            self._init_default_search_providers()
        
        if not self.llm_providers:
            self._init_default_llm_providers()
    
    def _init_default_search_providers(self):
        """Initialize default search provider configurations"""
        self.search_providers = {
            "tavily": SearchProviderConfig(
                enabled=bool(os.getenv("TAVILY_API_KEY")),
                api_key=os.getenv("TAVILY_API_KEY"),
                priority=10
            ),
            "exa": SearchProviderConfig(
                enabled=bool(os.getenv("EXA_API_KEY")),
                api_key=os.getenv("EXA_API_KEY"),
                priority=9
            ),
            "searxng": SearchProviderConfig(
                enabled=True,
                api_key=os.getenv("SEARXNG_INSTANCE_URL", "https://searx.be/"),
                priority=5
            ),
            "google": SearchProviderConfig(
                enabled=True,
                priority=4
            ),
            "duckduckgo": SearchProviderConfig(
                enabled=True,
                priority=3
            ),
        }
    
    def _init_default_llm_providers(self):
        """Initialize default LLM provider configurations"""
        self.llm_providers = {
            "openrouter": LLMProviderConfig(
                enabled=bool(os.getenv("OPENROUTER_API_KEY")),
                api_key=os.getenv("OPENROUTER_API_KEY"),
                model="openrouter/auto",
                base_url="https://openrouter.ai/api/v1",
                priority=10
            ),
            "agnes": LLMProviderConfig(
                enabled=bool(os.getenv("AGNES_API_KEY")),
                api_key=os.getenv("AGNES_API_KEY"),
                model="agnes",
                priority=9
            ),
            "gemini": LLMProviderConfig(
                enabled=bool(os.getenv("GEMINI_API_KEY")),
                api_key=os.getenv("GEMINI_API_KEY"),
                model="gemini-pro",
                priority=8
            ),
            "ollama": LLMProviderConfig(
                enabled=True,
                model="mistral",
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                priority=5
            ),
        }
    
    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment variables"""
        settings = cls(
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            http_proxy=os.getenv("HTTP_PROXY"),
            https_proxy=os.getenv("HTTPS_PROXY"),
            verify_ssl=os.getenv("VERIFY_SSL", "true").lower() == "true",
        )
        return settings
    
    @classmethod
    def from_yaml(cls, path: str) -> "Settings":
        """Load settings from YAML file"""
        if not os.path.exists(path):
            logger.warning(f"Config file not found: {path}. Using defaults.")
            return cls.from_env()
        
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        
        return cls(**data)


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or initialize global settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    return _settings


def set_settings(settings: Settings) -> None:
    """Override global settings instance"""
    global _settings
    _settings = settings
