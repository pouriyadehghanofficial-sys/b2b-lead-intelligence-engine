# Contributing to B2B Lead Intelligence Engine

Thank you for your interest in contributing! This document provides guidelines and instructions.

## Code of Conduct

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Report issues privately if needed

## How to Contribute

### Reporting Bugs

1. Check existing [issues](https://github.com/pouriyadehghanofficial-sys/b2b-lead-intelligence-engine/issues)
2. Create detailed bug report with:
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Error messages/traceback
   - Screenshots if applicable

### Suggesting Features

1. Check [issues](https://github.com/pouriyadehghanofficial-sys/b2b-lead-intelligence-engine/issues) and [discussions](https://github.com/pouriyadehghanofficial-sys/b2b-lead-intelligence-engine/discussions)
2. Provide clear use case
3. Explain expected behavior
4. Link related features if any

### Pull Requests

#### Setup

```bash
git clone https://github.com/yourusername/b2b-lead-intelligence-engine.git
cd b2b-lead-intelligence-engine
git checkout -b feature/your-feature
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Make Changes

1. Write your code
2. Add/update tests
3. Update documentation
4. Run tests: `python run_tests.py`
5. Check formatting: `python -m black app/`

#### Submit PR

1. Commit with clear messages
2. Push to your fork
3. Create pull request with:
   - Clear title and description
   - Reference to related issues
   - List of changes
   - Screenshots if UI changes

## Development Guidelines

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings
- Max line length: 100 chars

```python
def extract_phones(text: str) -> List[str]:
    """
    Extract phone numbers from text.
    
    Args:
        text: Input text to search
        
    Returns:
        List of extracted phone numbers
    """
    pass
```

### Testing

- Write tests for new features
- Maintain 80%+ coverage
- Use pytest
- Test edge cases

```python
def test_extract_phones():
    extractor = PhoneExtractor()
    
    # Test valid phone
    assert "09121234567" in extractor.extract("Call: 09121234567")
    
    # Test formatted phone
    assert "09121234567" in extractor.extract("0912-123-4567")
    
    # Test empty input
    assert extractor.extract("") == []
```

### Documentation

- Update README.md for user-facing changes
- Update API.md for API changes
- Add docstrings to functions
- Update CHANGELOG.md

## Areas for Contribution

### High Priority

- [ ] Additional search providers
- [ ] Email extraction
- [ ] Social media extraction
- [ ] Duplicate detection UI
- [ ] Performance optimization

### Medium Priority

- [ ] Multi-language support
- [ ] Web scraping module
- [ ] CRM integrations
- [ ] More export formats
- [ ] Advanced filtering

### Low Priority

- [ ] UI/UX improvements
- [ ] Documentation updates
- [ ] Example notebooks
- [ ] Docker support

## Questions?

- 💬 Ask in [Discussions](https://github.com/pouriyadehghanofficial-sys/b2b-lead-intelligence-engine/discussions)
- 📧 Email: pouriyadehghan.official@gmail.com
- 🔗 GitHub: https://github.com/pouriyadehghanofficial-sys

Thank you for contributing! 🚀
