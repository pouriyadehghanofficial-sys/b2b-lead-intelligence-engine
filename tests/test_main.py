"""Unit tests for B2B Lead Intelligence Engine"""

import pytest
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.validation.phone_validator import IranianPhoneValidator, PhoneType
from app.validation.industry_validator import IndustryValidator
from app.extraction.phone import PhoneExtractor
from app.extraction.company import CompanyExtractor
from app.extraction.person import PersonExtractor
from app.matching.phone_matcher import PhoneMatcher
from app.matching.person_matcher import PersonMatcher
from app.matching.company_matcher import CompanyMatcher
from app.matching.resolver import EntityResolver


class TestPhoneValidator:
    """Test phone validation"""
    
    def setup_method(self):
        self.validator = IranianPhoneValidator()
    
    def test_validate_mobile(self):
        """Test mobile number validation"""
        assert self.validator.validate("09121234567") == True
        assert self.validator.validate("0912-123-4567") == True
        assert self.validator.validate("+989121234567") == True
    
    def test_validate_invalid(self):
        """Test invalid number validation"""
        assert self.validator.validate("1234567") == False
        assert self.validator.validate("") == False
        assert self.validator.validate("invalid") == False
    
    def test_normalize(self):
        """Test phone normalization"""
        assert self.validator.normalize("09121234567") == "09121234567"
        assert self.validator.normalize("0912-123-4567") == "09121234567"
        assert self.validator.normalize("+989121234567") == "09121234567"
    
    def test_get_type(self):
        """Test phone type detection"""
        assert self.validator.get_type("09121234567") == PhoneType.MOBILE
        assert self.validator.get_type("021xxxxxxx") == PhoneType.LANDLINE


class TestIndustryValidator:
    """Test industry validation"""
    
    def setup_method(self):
        self.validator = IndustryValidator()
    
    def test_validate_known_industry(self):
        """Test validation of known industries"""
        assert self.validator.validate("کاشی و سرامیک") == True
        assert self.validator.validate("tile") == True
    
    def test_normalize(self):
        """Test industry normalization"""
        result = self.validator.normalize("tile")
        assert result is not None


class TestPhoneExtractor:
    """Test phone extraction"""
    
    def setup_method(self):
        self.extractor = PhoneExtractor()
    
    def test_extract_single_phone(self):
        """Test extracting a single phone"""
        text = "شماره تماس: 09121234567"
        phones = self.extractor.extract(text)
        assert len(phones) > 0
        assert "09121234567" in phones
    
    def test_extract_multiple_phones(self):
        """Test extracting multiple phones"""
        text = "تماس: 09121234567 یا 09131234567"
        phones = self.extractor.extract(text)
        assert len(phones) >= 1
    
    def test_extract_formatted_phone(self):
        """Test extracting formatted phones"""
        text = "Phone: 0912-123-4567"
        phones = self.extractor.extract(text)
        assert len(phones) > 0


class TestCompanyExtractor:
    """Test company extraction"""
    
    def setup_method(self):
        self.extractor = CompanyExtractor()
    
    def test_extract_company_with_suffix(self):
        """Test extracting companies with Persian suffixes"""
        text = "شرکت ایران کاشی"
        companies = self.extractor.extract(text)
        assert len(companies) > 0
    
    def test_extract_english_company(self):
        """Test extracting English company names"""
        text = "Company: Iran Tile Company"
        companies = self.extractor.extract(text)
        assert len(companies) > 0


class TestPersonExtractor:
    """Test person extraction"""
    
    def setup_method(self):
        self.extractor = PersonExtractor()
    
    def test_extract_role(self):
        """Test role extraction"""
        text = "مدیر فروش محمد احمدی"
        roles = self.extractor.extract_roles(text)
        assert len(roles) > 0
    
    def test_normalize_role(self):
        """Test role normalization"""
        result = self.extractor.normalize_role("مدیر فروش")
        assert result is not None


class TestPhoneMatcher:
    """Test phone matching"""
    
    def setup_method(self):
        self.matcher = PhoneMatcher()
    
    def test_exact_match(self):
        """Test exact phone match"""
        score = self.matcher.match("09121234567", "09121234567")
        assert score == 1.0
    
    def test_formatted_match(self):
        """Test formatted phone match"""
        score = self.matcher.match("09121234567", "0912-123-4567")
        assert score > 0.9
    
    def test_no_match(self):
        """Test non-matching phones"""
        score = self.matcher.match("09121234567", "09131234567")
        assert score == 0.0


class TestPersonMatcher:
    """Test person matching"""
    
    def setup_method(self):
        self.matcher = PersonMatcher()
    
    def test_exact_name_match(self):
        """Test exact name match"""
        score = self.matcher.match_names("محمد احمدی", "محمد احمدی")
        assert score == 1.0
    
    def test_similar_name_match(self):
        """Test similar name matching"""
        score = self.matcher.match_names("محمد احمدی", "محمد احمد")
        assert score > 0.7


class TestCompanyMatcher:
    """Test company matching"""
    
    def setup_method(self):
        self.matcher = CompanyMatcher()
    
    def test_exact_company_match(self):
        """Test exact company match"""
        score = self.matcher.match("ایران کاشی", "ایران کاشی")
        assert score == 1.0
    
    def test_similar_company_match(self):
        """Test similar company matching"""
        score = self.matcher.match("ایران کاشی", "شرکت ایران کاشی")
        assert score > 0.7


class TestEntityResolver:
    """Test entity resolution"""
    
    def setup_method(self):
        self.resolver = EntityResolver()
    
    def test_resolve_lead(self):
        """Test lead resolution"""
        lead = self.resolver.resolve_lead(
            company_name="ایران کاشی",
            person_name="محمد احمدی",
            role="مدیر فروش",
            phone="09121234567",
            evidence_count=1,
        )
        assert lead is not None
        assert lead.company_name == "ایران کاشی"
        assert lead.confidence_score > 0
    
    def test_can_merge(self):
        """Test lead merge capability"""
        from app.entities.lead import Lead
        
        lead1 = Lead(
            company_name="ایران کاشی",
            person_name="محمد احمدی",
            phone="09121234567",
        )
        
        lead2 = Lead(
            company_name="شرکت ایران کاشی",
            person_name="محمد احمدی",
            phone="09121234567",
        )
        
        can_merge = self.resolver.can_merge(lead1, lead2)
        assert can_merge == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
