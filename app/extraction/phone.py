"""Phone number extraction from text"""

import re
from typing import List, Set
from app.validation.phone_validator import IranianPhoneValidator
import logging

logger = logging.getLogger(__name__)


class PhoneExtractor:
    """Extract phone numbers from text"""
    
    def __init__(self):
        self.validator = IranianPhoneValidator()
        self.patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> List[re.Pattern]:
        """Compile regex patterns for phone extraction"""
        patterns = [
            # Format: 0912-123-4567 or 0912 123 4567
            r'0\d{2,3}[\s\-]?\d{3}[\s\-]?\d{4}',
            # Format: +98 912 123 4567
            r'\+98\s?\d{9,10}',
            # Format: 0098912 1234567
            r'0098\d{9,10}',
            # Format: 98912 1234567
            r'(?<!0)98\d{9,10}',
            # Format: 09121234567 (continuous)
            r'0\d{10,11}',
        ]
        return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    
    def extract(self, text: str) -> List[str]:
        """Extract phone numbers from text"""
        if not text:
            return []
        
        phones: Set[str] = set()
        
        # Apply all patterns
        for pattern in self.patterns:
            matches = pattern.findall(text)
            for match in matches:
                normalized = self.validator.normalize(match)
                if normalized and self.validator.validate(normalized):
                    phones.add(normalized)
        
        return list(phones)
    
    def extract_with_context(self, text: str, context_size: int = 100) -> List[dict]:
        """Extract phone numbers with surrounding context"""
        if not text:
            return []
        
        results = []
        
        for pattern in self.patterns:
            for match in pattern.finditer(text):
                phone = match.group(0)
                normalized = self.validator.normalize(phone)
                
                if normalized and self.validator.validate(normalized):
                    # Get context
                    start = max(0, match.start() - context_size)
                    end = min(len(text), match.end() + context_size)
                    context = text[start:end]
                    
                    results.append({
                        'phone': normalized,
                        'phone_type': self.validator.get_type(normalized).value,
                        'context': context.strip(),
                        'position': match.start(),
                    })
        
        # Remove duplicates based on phone number
        seen = set()
        unique_results = []
        for result in results:
            phone = result['phone']
            if phone not in seen:
                seen.add(phone)
                unique_results.append(result)
        
        return unique_results
