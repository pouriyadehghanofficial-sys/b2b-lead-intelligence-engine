"""Company name extraction from text"""

import re
from typing import List, Set, Optional
from fuzzywuzzy import fuzz
import logging

logger = logging.getLogger(__name__)


class CompanyExtractor:
    """Extract company names from text"""
    
    # Company type suffixes (Persian)
    COMPANY_TYPES = {
        'شرکت',
        'کارخانه',
        'کارگاه',
        'مؤسسه',
        'موسسه',
        'دفتر',
        'اداره',
        'تجارت',
        'صنعت',
        'گروه',
        'نمایندگی',
        'تعاونی',
        'سازمان',
        'نهاد',
    }
    
    # English equivalents
    COMPANY_TYPES_EN = {
        'company',
        'factory',
        'workshop',
        'institute',
        'corporation',
        'group',
        'organization',
        'association',
        'ltc',
        'pvt',
        'ltd',
        'inc',
    }
    
    def __init__(self, min_length: int = 3):
        self.min_length = min_length
    
    def extract(self, text: str) -> List[str]:
        """Extract potential company names"""
        if not text:
            return []
        
        companies: Set[str] = set()
        
        # Pattern 1: Explicit company indicators
        pattern1 = r'(\w+\s+)*?(\w+)\s+(شرکت|کارخانه|مؤسسه|موسسه|گروه|کارگاه)'
        matches = re.finditer(pattern1, text)
        for match in matches:
            company = match.group(0).strip()
            if len(company) >= self.min_length:
                companies.add(company)
        
        # Pattern 2: English company types
        pattern2 = r'(\w+\s+)+?(company|corporation|ltc|ltd|inc|group|factory)\b'
        matches = re.finditer(pattern2, text, re.IGNORECASE)
        for match in matches:
            company = match.group(0).strip()
            if len(company) >= self.min_length:
                companies.add(company)
        
        # Pattern 3: Capitalized phrases (potential company names)
        pattern3 = r'[A-Z][a-z]+(\s+[A-Z][a-z]+)*'
        matches = re.finditer(pattern3, text)
        for match in matches:
            company = match.group(0).strip()
            if 3 <= len(company) <= 100 and len(company.split()) <= 4:
                companies.add(company)
        
        # Pattern 4: Persian capitalized names
        pattern4 = r'[\u0600-\u06FF][\u0600-\u06FF\s]*'
        matches = re.finditer(pattern4, text)
        for match in matches:
            company = match.group(0).strip()
            if len(company) >= self.min_length and len(company.split()) <= 4:
                companies.add(company)
        
        return list(companies)
    
    def extract_with_confidence(self, text: str) -> List[dict]:
        """Extract companies with confidence scores"""
        companies = self.extract(text)
        results = []
        
        for company in companies:
            confidence = self._score_company(company, text)
            results.append({
                'name': company,
                'confidence': confidence,
            })
        
        # Sort by confidence
        return sorted(results, key=lambda x: x['confidence'], reverse=True)
    
    def _score_company(self, company: str, text: str) -> float:
        """Score how likely a string is a real company name"""
        score = 0.5
        
        # Boost if has company type suffix
        for company_type in self.COMPANY_TYPES:
            if company.endswith(company_type):
                score += 0.3
                break
        
        for company_type in self.COMPANY_TYPES_EN:
            if company.lower().endswith(company_type):
                score += 0.3
                break
        
        # Boost if appears multiple times
        if text.lower().count(company.lower()) > 1:
            score += 0.1
        
        # Check length (not too short, not too long)
        if 4 <= len(company) <= 50:
            score += 0.1
        
        return min(score, 1.0)
