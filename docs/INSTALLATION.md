# Installation and Setup Guide

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

## Local Installation

### 1. Clone Repository

```bash
git clone https://github.com/pouriyadehghanofficial-sys/b2b-lead-intelligence-engine.git
cd b2b-lead-intelligence-engine
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys (Optional)

Create `.env` file in project root:

```bash
TAVILY_API_KEY=your_tavily_key
EXA_API_KEY=your_exa_key
OPENROUTER_API_KEY=your_openrouter_key
```

## Running the Application

### Option 1: Web UI (Recommended)

```bash
python run_ui.py
```

Then open http://localhost:8501

### Option 2: Command Line

```bash
python run_cli.py \
  --industry "کاشی و سرامیک" \
  --location "یزد" \
  --roles "مدیر فروش" "مسئول خرید" \
  --quantity 100
```

### Option 3: Google Colab

See `B2B_Lead_Intelligence_Colab.ipynb`

## Running Tests

```bash
# Quick component tests
python test_components.py

# Full test suite
python run_tests.py
```

## Project Structure

```
app/
├── config/           # Configuration management
├── network/          # HTTP client and retry logic
├── entities/         # Data models
├── validation/       # Phone and industry validation
├── extraction/       # Text extraction (phones, companies, people)
├── search/           # Search provider routing
├── sources/          # Data source adapters
├── matching/         # Entity resolution and matching
├── scoring/          # Confidence and lead scoring
├── storage/          # Database layer
├── export/           # Export formatters (Excel, JSON, CSV)
├── llm/              # LLM routing and integration
├── core/             # Pipeline orchestration
└── ui/               # Streamlit web interface

tests/                # Unit tests
docs/                 # Documentation
```

## API Keys Setup

### Tavily (Search API)

1. Visit https://tavily.com
2. Sign up for free account
3. Get API key from dashboard
4. Add to `.env` or Colab secrets

### Exa (Semantic Search)

1. Visit https://exa.ai
2. Sign up for developer account
3. Get API key
4. Add to environment

### OpenRouter (LLM)

1. Visit https://openrouter.ai
2. Create account
3. Get API key
4. Add to environment

## Troubleshooting

### "No search providers available"

This is expected without API keys. The system will fallback gracefully.

### "LLM features disabled"

Add OpenRouter or Ollama API key for AI query generation.

### "Database locked" error

Close other instances accessing the database.

### Colab session timeout

Use checkpoint/resume feature to continue from last step.

## Performance Tips

1. **Start with small quantity**: Test with 50-100 leads first
2. **Use specific industry**: Narrow queries return better results
3. **Enable API keys**: Provides better coverage and speed
4. **Batch processing**: Process multiple locations sequentially
5. **Caching**: Results are cached to avoid redundant searches

## Cost Estimation

- **Free tier**: ~100 searches using public providers
- **Tavily**: $0.10 per 100 searches
- **Exa**: $0.05 per semantic search
- **OpenRouter**: $0.01-0.10 per 1K tokens

**Total for 1000 leads**: $5-25 (varies by API selection)

## Support

- 📖 Check README.md for overview
- 📝 See docs/ for detailed documentation
- 🐛 Report issues on GitHub
- 💬 For questions, open a discussion

## Legal Notice

This tool only processes publicly available information. Always:

- ✅ Respect robots.txt
- ✅ Follow terms of service
- ✅ Comply with local data privacy laws
- ✅ Use data responsibly
- ❌ Don't bypass authentication
- ❌ Don't violate paywalls
- ❌ Don't access private data
