"""Industry validation and classification"""

import logging
from typing import Optional, List, Set
from fuzzywuzzy import fuzz
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class IndustryValidator:
    """Validate and classify industries"""
    
    # Common Iranian industries (in Persian and English)
    INDUSTRIES = {
        # Manufacturing
        'کاشی و سرامیک': ['tile', 'ceramic', 'porcelain'],
        'فولاد': ['steel', 'iron'],
        'نساجی': ['textile', 'fabric', 'garment'],
        'پلاستیک': ['plastic', 'polymers'],
        'شیمیایی': ['chemical', 'petrochemical'],
        'غذایی': ['food', 'beverage', 'agriculture'],
        'خودروسازی': ['automotive', 'car', 'vehicle'],
        
        # Services
        'فناوری اطلاعات': ['it', 'software', 'technology'],
        'مشاوره': ['consulting', 'advisory'],
        'حسابداری': ['accounting', 'audit', 'finance'],
        'حقوقی': ['legal', 'law'],
        'بیمه': ['insurance'],
        'بانکداری': ['banking', 'financial'],
        
        # Trade
        'واردات صادرات': ['import', 'export', 'trading'],
        'عمده فروشی': ['wholesale'],
        'خرده فروشی': ['retail'],
        'توزیع': ['distribution', 'logistics'],
    }
    
    def __init__(self, similarity_threshold: float = 0.7):
        self.similarity_threshold = similarity_threshold
        self._build_lookup_table()
    
    def _build_lookup_table(self):
        """Build lookup table for fast matching"""
        self.lookup = {}
        for farsi, keywords in self.INDUSTRIES.items():
            self.lookup[farsi.lower()] = farsi
            for keyword in keywords:
                self.lookup[keyword.lower()] = farsi
    
    def validate(self, industry: str) -> bool:
        """Validate if industry is recognized"""
        if not industry:
            return False
        
        normalized = self.normalize(industry)
        return normalized is not None
    
    def normalize(self, industry: str) -> Optional[str]:
        """Normalize industry to standard form"""
        if not industry:
            return None
        
        industry = industry.strip().lower()
        
        # Direct lookup
        if industry in self.lookup:
            return self.lookup[industry]
        
        # Fuzzy match
        for standard_industry in self.INDUSTRIES.keys():
            similarity = fuzz.token_set_ratio(industry, standard_industry.lower())
            if similarity >= self.similarity_threshold * 100:
                return standard_industry
        
        return None
    
    def get_keywords(self, industry: str) -> Set[str]:
        """Get keywords for an industry"""
        normalized = self.normalize(industry)
        if not normalized:
            return set()
        
        keywords = set(self.INDUSTRIES.get(normalized, []))
        keywords.add(normalized)
        return keywords
    
    def suggest_queries(self, industry: str) -> List[str]:
        """Suggest search queries for an industry"""
        normalized = self.normalize(industry)
        if not normalized:
            return []
        
        keywords = self.get_keywords(industry)
        queries = list(keywords)[:5]  # Top 5 keywords
        return queries
