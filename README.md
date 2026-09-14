# B2B Lead Intelligence Engine

A production-grade, AI-powered B2B Lead Intelligence Engine for discovering and validating Iranian business leads from public sources. Optimized for Google Colab execution.

## Features

✅ **Modular Architecture**: Pluggable search providers, LLM routers, and source adapters
✅ **Smart Query Generation**: Automatic generation of Persian/English variations and industry-specific queries
✅ **Multi-Provider Support**: Fallback mechanisms across Tavily, Exa, SearXNG, and public search
✅ **Entity Resolution**: Advanced matching between companies, people, roles, and phone numbers
✅ **Evidence Engine**: Comprehensive tracking of all data sources with URLs and timestamps
✅ **Confidence Scoring**: Multi-dimensional scoring system with explainability
✅ **Phone Normalization**: Iranian phone number handling with validity checks
✅ **Deduplication**: Intelligent duplicate detection across multiple sources
✅ **Checkpoint/Resume**: Pipeline can survive Colab interruptions
✅ **Excel Export**: Professional output with statistics and evidence sheets
✅ **Zero Hard Coding**: All API keys from environment variables or Colab secrets
✅ **Colab Optimized**: No Docker, Kubernetes, or persistent infrastructure needed

## Quick Start

### Option 1: Google Colab (Recommended)

1. Open the [Colab Notebook](./B2B_Lead_Intelligence_Colab.ipynb)
2. Click "Run all cells"
3. Enter your search parameters and optional API keys
4. Download results as Excel/JSON

### Option 2: Local Python

```bash
# Clone repository
git clone https://github.com/pouriyadehghanofficial-sys/b2b-lead-intelligence-engine.git
cd b2b-lead-intelligence-engine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API keys (optional)
export TAVILY_API_KEY="your_key"
export EXA_API_KEY="your_key"
export OPENROUTER_API_KEY="your_key"

# Run UI
streamlit run app/ui/main.py
```

## Architecture

```
app/
├── ui/                    # Streamlit UI
│   ├── main.py
│   └── components.py
├── core/                  # Core pipeline engine
│   ├── pipeline.py
│   └── checkpoint.py
├── search/                # Search routing
│   ├── router.py
│   ├── provider.py
│   └── providers/
│       ├── base.py
│       ├── tavily.py
│       ├── exa.py
│       ├── searxng.py
│       └── google.py
├── sources/               # Data source adapters
│   ├── base.py
│   ├── website.py
│   ├── directory.py
│   ├── pdf.py
│   └── factory.py
├── extraction/            # Data extraction
│   ├── company.py
│   ├── person.py
│   ├── phone.py
│   └── llm_extractor.py
├── entities/              # Data models
│   ├── company.py
│   ├── person.py
│   ├── evidence.py
│   └── lead.py
├── validation/            # Validation logic
│   ├── phone_validator.py
│   ├── industry_validator.py
│   └── entity_validator.py
├── matching/              # Entity matching & resolution
│   ├── phone_matcher.py
│   ├── person_matcher.py
│   ├── company_matcher.py
│   └── resolver.py
├── scoring/               # Confidence & Lead scoring
│   ├── confidence.py
│   ├── lead_score.py
│   └── freshness.py
├── storage/               # Database layer
│   ├── db.py
│   ├── models.py
│   └── repository.py
├── export/                # Export formats
│   ├── excel.py
│   ├── json.py
│   └── csv.py
├── llm/                   # LLM routing & integration
│   ├── router.py
│   ├── providers.py
│   └── prompts.py
├── network/               # HTTP layer with retry logic
│   ├── client.py
│   ├── retry.py
│   └── proxy.py
└── config/                # Configuration
    ├── settings.py
    ├── providers.py
    └── defaults.yaml
```

## Pipeline Flow

```
User Input (Industry, Location, Product, Quantity)
    ↓
Query Generation (Persian/English variations)
    ↓
Search Router (Tavily → Exa → SearXNG → Fallback)
    ↓
Company Discovery (Extract companies from results)
    ↓
Company Verification (Validate industry, location)
    ↓
Person Discovery (Find contacts for each company)
    ↓
Role Verification (Match against target roles)
    ↓
Phone Discovery (Extract from public sources)
    ↓
Phone Normalization (Standardize formats)
    ↓
Entity Resolution (Match Person ↔ Phone ↔ Company)
    ↓
Evidence Collection (Track all sources)
    ↓
Confidence Scoring (Multi-dimensional scoring)
    ↓
Freshness Analysis (Evaluate source recency)
    ↓
Lead Scoring (Overall lead quality)
    ↓
Deduplication (Remove duplicates)
    ↓
Status Assignment (VERIFIED/LIKELY/POSSIBLE/UNVERIFIED)
    ↓
Excel Export (Professional output with stats)
```

## Configuration

### Environment Variables

```bash
# Search Providers
TAVILY_API_KEY=...
EXA_API_KEY=...
SEARXNG_INSTANCE_URL=...

# LLM Providers
OPENROUTER_API_KEY=...
AGNES_API_KEY=...
OLLAMA_BASE_URL=...
GEMINI_API_KEY=...

# Network
HTTP_PROXY=...
HTTPS_PROXY=...
SEND_HTTP_PROXY_ERRORS=1

# App
DEBUG=false
LOG_LEVEL=INFO
```

### Colab Secrets

In Colab, click the 🔑 icon in left panel to add secrets. They'll be available as environment variables.

## Usage Examples

### Example 1: Tile & Ceramic Manufacturers in Yazd

```
Industry: کاشی و سرامیک
Location: یزد
Target Roles: مدیرعامل، مدیر فروش، مسئول خرید
Quantity: 1000
```

### Example 2: Tech Startups in Tehran

```
Industry: فناوری اطلاعات
Location: تهران
Target Roles: مدیر محصول، مدیر فروش
Quantity: 500
```

## Output

Generated Excel file contains:

- **Leads Sheet**: Company, Person, Role, Phone, Industry, Evidence, Confidence Score, Lead Score, Status
- **Statistics Sheet**: Companies found, people found, verified leads, errors
- **Evidence Sheet**: Detailed source tracking
- **Rejected Sheet**: Leads that didn't meet confidence thresholds

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test
pytest tests/test_phone_validator.py -v
```

## Performance Notes

- First run takes 10-30 minutes for 1000 leads depending on API availability
- Subsequent runs are faster due to caching
- Pipeline resumes from checkpoints if interrupted
- Use 100-200 leads for testing
- System handles concurrent requests with rate limiting

## Known Limitations

1. **Phone Numbers**: Only includes publicly available phone numbers from indexed sources
2. **Age of Data**: Information freshness depends on search engine indexes (typically 1-3 weeks old)
3. **Geographic Coverage**: Best results for major cities; smaller cities may have limited data
4. **API Rate Limits**: Free tiers have daily/monthly limits
5. **Language**: Optimized for Persian, but handles English queries too

## Providers Supported

### Search
- Tavily Search API
- Exa Search API
- SearXNG (Open source metasearch)
- Google Search (via public results)
- DuckDuckGo (via public results)

### LLM
- OpenRouter (50+ models)
- Agnes (via OpenAI API)
- Ollama (local)
- Google Gemini
- Any OpenAI-compatible API

## Cost Estimation

- **Tavily**: $0.10 per 100 searches
- **Exa**: $0.05 per search (custom model)
- **OpenRouter**: Varies by model, typically $0.01-0.10 per 1K tokens
- **Free options**: SearXNG, Google, DuckDuckGo (no cost, limited rate)

Total cost per 1000 leads: $5-25 depending on provider selection

## Contributing

Contributions welcome! Please:

1. Fork repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## Legal & Ethical

This system only processes publicly available information. It does not:
- Bypass authentication or paywalls
- Violate robots.txt or terms of service
- Access private data
- Perform unauthorized scraping

Use responsibly and respect data privacy regulations (GDPR, Iranian laws, etc.).

## License

MIT License - See LICENSE file

## Support

- 📧 Email: support@example.com
- 💬 Issues: GitHub Issues
- 📚 Docs: Full documentation in `/docs`
