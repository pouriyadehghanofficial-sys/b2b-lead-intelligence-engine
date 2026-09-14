"""Phone number matching"""

import logging
from typing import List, Tuple
from app.validation.phone_validator import IranianPhoneValidator

logger = logging.getLogger(__name__)


class PhoneMatcher:
    """Match and deduplicate phone numbers"""
    
    def __init__(self):
        self.validator = IranianPhoneValidator()
    
    def match(self, phone1: str, phone2: str) -> float:
        """Return matching score (0-1) between two phone numbers"""
        norm1 = self.validator.normalize(phone1)
        norm2 = self.validator.normalize(phone2)
        
        if not norm1 or not norm2:
            return 0.0
        
        if norm1 == norm2:
            return 1.0
        
        # Check if one is substring of other (allowing for formatting differences)
        digits1 = ''.join(c for c in norm1 if c.isdigit())
        digits2 = ''.join(c for c in norm2 if c.isdigit())
        
        if digits1 == digits2:
            return 0.95
        
        return 0.0
    
    def deduplicate(self, phones: List[str]) -> List[str]:
        """Remove duplicate phone numbers"""
        normalized = {}
        
        for phone in phones:
            norm = self.validator.normalize(phone)
            if norm and self.validator.validate(norm):
                if norm not in normalized:
                    normalized[norm] = phone
        
        return list(normalized.keys())
