# Configuration Guide

## Environment Variables

### Search Providers

```bash
# Tavily Search
TAVILY_API_KEY=your_tavily_api_key

# Exa Search
EXA_API_KEY=your_exa_api_key

# SearXNG Instance (optional)
SEARXNG_INSTANCE_URL=https://searx.example.com
```

### LLM Providers

```bash
# OpenRouter
OPENROUTER_API_KEY=your_openrouter_key

# Agnes
AGNES_API_KEY=your_agnes_key

# Ollama (Local)
OLLAMA_BASE_URL=http://localhost:11434

# Google Gemini
GEMINI_API_KEY=your_gemini_key
```

### Network

```bash
# HTTP Proxy (optional)
HTTP_PROXY=http://proxy.example.com:8080
HTTPS_PROXY=https://proxy.example.com:8080

# SSL Verification
VERIFY_SSL=true
```

### Application

```bash
# Debug mode
DEBUG=false

# Log level
LOG_LEVEL=INFO

# Colab mode
COLAB_MODE=false
```

## Configuration File (YAML)

Create `config.yaml` in project root:

```yaml
# Application Settings
debug: false
log_level: INFO
cache_enabled: true
checkpoint_dir: ./checkpoints
data_dir: ./data
db_path: ./data/leads.db

# Search Configuration
search_timeout: 30
search_retries: 3

# LLM Configuration
enable_llm: true
llm_timeout: 60

# Pipeline Configuration
batch_size: 10
max_concurrent_requests: 5
enable_deduplication: true
confidence_threshold: 0.3
lead_score_threshold: 0.5

# Phone Configuration
country_code: '+98'
phone_validation_strict: false

# Industry Configuration
industry_cache_enabled: true
```

## Colab Configuration

In Colab, click the 🔑 icon in the left sidebar to add secrets:

1. `TAVILY_API_KEY` - Tavily Search API key
2. `EXA_API_KEY` - Exa Search API key
3. `OPENROUTER_API_KEY` - OpenRouter LLM API key

They'll be automatically loaded as environment variables.

## Provider Configuration

### Tavily

Optimal for:
- General B2B searches
- News and web results
- Persian and English queries

Free tier: 1000 calls/month

### Exa

Optimal for:
- Semantic/intent-based search
- Finding relevant companies
- Deep web indexing

Free tier: Limited requests

### OpenRouter

Optimal for:
- Query generation
- Entity extraction
- Role classification

Models:
- `openrouter/auto` - Auto-select best available
- `meta-llama/llama-2-70b` - Large model
- `mistralai/mistral-7b` - Fast model

### Ollama (Local)

Optimal for:
- Privacy (no API calls)
- Offline operation
- Cost-free operation

Models: mistral, llama2, neural-chat

## Performance Tuning

### For Speed

```python
from app.config.settings import Settings

settings = Settings(
    batch_size=20,  # Increase from default 10
    max_concurrent_requests=10,  # Increase from 5
    search_timeout=15,  # Decrease from 30
)
```

### For Quality

```python
settings = Settings(
    batch_size=5,  # Decrease
    search_timeout=60,  # Increase
    confidence_threshold=0.7,  # Increase filtering
    enable_deduplication=True,  # Enable
)
```

### For Cost

```python
settings = Settings(
    max_queries=10,  # Fewer searches
    batch_size=10,  # Balance
    enable_llm=False,  # Disable LLM for cost
)
```

## Provider Fallback Priority

Default order:

1. **Tavily** (Priority: 10)
2. **Exa** (Priority: 9)
3. **Google** (Priority: 4)
4. **DuckDuckGo** (Priority: 3)

Custom order:

```python
from app.search.router import SearchRouter
from app.search.providers.custom import CustomProvider

router = SearchRouter()

# Add custom provider
custom = CustomProvider()
router.add_provider(custom)
```

## Logging Configuration

```python
from app.logging_config import setup_logging
import logging

logger = setup_logging(
    log_level=logging.DEBUG,
    log_file="./logs/app.log"
)
```

## Database Configuration

### SQLite (Default)

```python
from app.storage.db import Database

db = Database(db_path="./data/leads.db")
```

### Custom Path

```bash
export DB_PATH=/path/to/database.db
```

## Cache Configuration

```python
from app.config.settings import Settings

settings = Settings(
    cache_enabled=True,  # Enable caching
)
```

Cache is stored in-memory during session.
