"""Company name matching"""

import logging
from typing import Optional
from fuzzywuzzy import fuzz
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class CompanyMatcher:
    """Match company names"""
    
    def __init__(self, threshold: float = 0.80):
        self.threshold = threshold
    
    def match(self, company1: str, company2: str) -> float:
        """Match two company names (0-1)"""
        if not company1 or not company2:
            return 0.0
        
        company1 = company1.strip().lower()
        company2 = company2.strip().lower()
        
        # Exact match
        if company1 == company2:
            return 1.0
        
        # Substring match (one is contained in other)
        if company1 in company2 or company2 in company1:
            return 0.95
        
        # Token-based matching (order-independent)
        token_score = fuzz.token_set_ratio(company1, company2) / 100.0
        
        # Sequence matching
        sequence_score = SequenceMatcher(None, company1, company2).ratio()
        
        # Average the scores
        final_score = (token_score * 0.6) + (sequence_score * 0.4)
        
        return final_score
    
    def match_with_variants(self, company: str, candidates: list) -> dict:
        """Match a company against multiple candidates"""
        results = {}
        
        for candidate in candidates:
            score = self.match(company, candidate)
            if score >= self.threshold:
                results[candidate] = score
        
        return results
