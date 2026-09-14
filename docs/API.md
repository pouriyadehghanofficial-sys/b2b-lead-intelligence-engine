# API Documentation

## Core Pipeline

### LeadDiscoveryPipeline

```python
from app.core.pipeline import LeadDiscoveryPipeline

# Initialize
pipeline = LeadDiscoveryPipeline(db_path="./data/leads.db")

# Run discovery
leads = pipeline.discover(
    industry="کاشی و سرامیک",
    location="یزد",
    product="سیستم کنترل کیفیت",
    target_roles=["مدیر فروش", "مسئول خرید"],
    quantity=100,
    max_queries=20,
)

# Access statistics
stats = pipeline.stats
print(f"Found {stats['companies_found']} companies")
print(f"Found {stats['phones_found']} phone numbers")
```

## Phone Validation

```python
from app.validation.phone_validator import IranianPhoneValidator

validator = IranianPhoneValidator()

# Validate
if validator.validate("09121234567"):
    print("Valid phone")

# Normalize
normalized = validator.normalize("0912-123-4567")
print(normalized)  # 09121234567

# Get type
phone_type = validator.get_type("09121234567")
print(phone_type)  # PhoneType.MOBILE
```

## Text Extraction

### Extract Phones

```python
from app.extraction.phone import PhoneExtractor

extractor = PhoneExtractor()
text = "تماس: 09121234567 یا 021-1234567"
phones = extractor.extract(text)
# ['09121234567', '02112345670']
```

### Extract Companies

```python
from app.extraction.company import CompanyExtractor

extractor = CompanyExtractor()
text = "شرکت ایران کاشی تحت مدیریت..."
companies = extractor.extract(text)
# ['شرکت ایران کاشی']
```

### Extract People

```python
from app.extraction.person import PersonExtractor

extractor = PersonExtractor()
text = "مدیر فروش محمد احمدی"
people = extractor.extract_person_mentions(text)
# [{'name': 'محمد احمدی', 'role': 'مدیر فروش', 'confidence': 0.8}]
```

## Search

```python
from app.search.router import SearchRouter

router = SearchRouter()
results = router.search(
    query="کاشی یزد",
    limit=10,
)

for result in results:
    print(f"{result.title}")
    print(f"URL: {result.url}")
    print(f"Source: {result.source}")
```

## Entity Matching

```python
from app.matching.resolver import EntityResolver
from app.entities.lead import Lead

resolver = EntityResolver()

# Create lead
lead = resolver.resolve_lead(
    company_name="شرکت X",
    person_name="محمد احمدی",
    role="مدیر فروش",
    phone="09121234567",
    evidence_count=2,
)

# Check if leads can merge
lead1 = Lead(company_name="شرکت X")
lead2 = Lead(company_name="شرکت X", phone="09121234567")

if resolver.can_merge(lead1, lead2):
    merged = resolver.merge_leads(lead1, lead2)
```

## Scoring

```python
from app.scoring.confidence import ConfidenceEngine
from app.scoring.lead_score import LeadScorer
from app.scoring.freshness import FreshnessAnalyzer

# Confidence scoring
conf_engine = ConfidenceEngine()
company_conf = conf_engine.score_company(
    "شرکت X",
    industry="کاشی",
    city="یزد",
)

# Lead scoring
scorer = LeadScorer()
leads = scorer.batch_score(leads)

# Freshness analysis
freshness = FreshnessAnalyzer()
fresh_score = freshness.score_date(datetime.now())
```

## Export

```python
from app.export.excel_export import ExcelExporter
from app.export.json_export import JSONExporter
from app.export.csv_export import CSVExporter

# Excel
excel_exporter = ExcelExporter()
excel_exporter.export(leads, "leads.xlsx")

# JSON
json_exporter = JSONExporter()
json_exporter.export(leads, "leads.json")

# CSV
csv_exporter = CSVExporter()
csv_exporter.export(leads, "leads.csv")
```

## LLM Integration

```python
from app.llm.router import LLMRouter
from app.query_generator import QueryGenerator

# LLM router
llm = LLMRouter()
if llm.is_available():
    response = llm.generate(
        "Generate 5 search queries for tile companies in Tehran",
        temperature=0.5,
        max_tokens=500,
    )

# Query generation
gen = QueryGenerator(llm)
queries = gen.generate(
    industry="کاشی",
    location="تهران",
    count=15,
)
```

## Database

```python
from app.storage.db import Database

db = Database("./data/leads.db")

# Add lead
lead_id = db.add_lead(lead)

# Get leads
leads = db.get_leads(
    status=LeadStatus.VERIFIED,
    min_score=0.7,
    limit=100,
)

# Statistics
stats = db.get_statistics()
print(f"Total leads: {stats['total_leads']}")
print(f"Verified: {stats['verified_leads']}")
```

## Checkpoints

```python
from app.core.checkpoint import CheckpointManager

checkpoint = CheckpointManager()

# Save
checkpoint.save_checkpoint(
    name="lead_discovery",
    data={"leads": leads},
    step="extraction_complete",
)

# Load
data = checkpoint.load_checkpoint("lead_discovery")
last_step = checkpoint.get_last_checkpoint_step("lead_discovery")
```
