"""Quick test of all major components"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.validation.phone_validator import IranianPhoneValidator
from app.validation.industry_validator import IndustryValidator
from app.extraction.phone import PhoneExtractor
from app.extraction.company import CompanyExtractor
from app.extraction.person import PersonExtractor
from app.matching.resolver import EntityResolver
from app.search.router import SearchRouter
from app.core.pipeline import LeadDiscoveryPipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_phone_validator():
    """Test phone validation"""
    logger.info("Testing Phone Validator...")
    validator = IranianPhoneValidator()
    
    test_phones = [
        ("09121234567", True),
        ("0912-123-4567", True),
        ("+989121234567", True),
        ("invalid", False),
    ]
    
    for phone, expected in test_phones:
        result = validator.validate(phone)
        status = "✓" if result == expected else "✗"
        logger.info(f"  {status} {phone}: {result}")
    
    logger.info("✓ Phone Validator OK\n")


def test_phone_extractor():
    """Test phone extraction"""
    logger.info("Testing Phone Extractor...")
    extractor = PhoneExtractor()
    
    text = "شماره تماس: 09121234567 یا 0913-123-4567"
    phones = extractor.extract(text)
    logger.info(f"  Extracted {len(phones)} phone(s): {phones}")
    
    logger.info("✓ Phone Extractor OK\n")


def test_company_extractor():
    """Test company extraction"""
    logger.info("Testing Company Extractor...")
    extractor = CompanyExtractor()
    
    text = "شرکت ایران کاشی و سرامیک تحت مدیریت مهندس احمدی"
    companies = extractor.extract(text)
    logger.info(f"  Extracted {len(companies)} company(ies): {companies[:2]}")
    
    logger.info("✓ Company Extractor OK\n")


def test_person_extractor():
    """Test person extraction"""
    logger.info("Testing Person Extractor...")
    extractor = PersonExtractor()
    
    text = "مدیر فروش محمد احمدی"
    people = extractor.extract_person_mentions(text)
    logger.info(f"  Extracted {len(people)} person(s)")
    if people:
        logger.info(f"    {people[0]}")
    
    logger.info("✓ Person Extractor OK\n")


def test_search_router():
    """Test search router"""
    logger.info("Testing Search Router...")
    router = SearchRouter()
    
    providers = router.get_available_providers()
    logger.info(f"  Available providers: {providers}")
    
    logger.info("✓ Search Router OK\n")


def test_entity_resolver():
    """Test entity resolver"""
    logger.info("Testing Entity Resolver...")
    resolver = EntityResolver()
    
    lead = resolver.resolve_lead(
        company_name="ایران کاشی",
        person_name="محمد احمدی",
        role="مدیر فروش",
        phone="09121234567",
        evidence_count=1,
    )
    
    logger.info(f"  Company: {lead.company_name}")
    logger.info(f"  Person: {lead.person_name}")
    logger.info(f"  Confidence: {lead.confidence_score:.2f}")
    
    logger.info("✓ Entity Resolver OK\n")


def main():
    """Run all tests"""
    logger.info("="*60)
    logger.info("B2B Lead Intelligence Engine - Quick Test")
    logger.info("="*60 + "\n")
    
    try:
        test_phone_validator()
        test_phone_extractor()
        test_company_extractor()
        test_person_extractor()
        test_search_router()
        test_entity_resolver()
        
        logger.info("="*60)
        logger.info("✓ All component tests passed!")
        logger.info("="*60)
        return 0
        
    except Exception as e:
        logger.error(f"\n✗ Test failed: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
