"""Person name and role extraction from text"""

import re
from typing import List, Optional, Tuple
from fuzzywuzzy import fuzz
import logging

logger = logging.getLogger(__name__)


class PersonExtractor:
    """Extract person names and roles from text"""
    
    # Common job titles (Persian)
    JOB_TITLES = {
        'مدیرعامل': 'ceo',
        'مدیر': 'manager',
        'مدیر فروش': 'sales_manager',
        'مدیر بازرگانی': 'commercial_manager',
        'مدیر خرید': 'purchasing_manager',
        'مسئول خرید': 'purchase_officer',
        'مدیر تولید': 'production_manager',
        'مدیر کیفیت': 'quality_manager',
        'مدیر IT': 'it_manager',
        'مدیر فنی': 'technical_manager',
        'مدیر مالی': 'financial_manager',
        'مدیر منابع انسانی': 'hr_manager',
        'دستیار': 'assistant',
        'کارمند': 'employee',
        'متخصص': 'specialist',
        'مهندس': 'engineer',
        'کارشناس': 'expert',
        'رئیس': 'chief',
    }
    
    # English equivalents
    JOB_TITLES_EN = {
        'ceo': 'CEO',
        'manager': 'Manager',
        'sales manager': 'Sales Manager',
        'commercial manager': 'Commercial Manager',
        'purchasing manager': 'Purchasing Manager',
        'purchase officer': 'Purchase Officer',
        'director': 'Director',
        'officer': 'Officer',
        'head': 'Head',
        'lead': 'Lead',
        'consultant': 'Consultant',
    }
    
    def __init__(self):
        self.role_patterns = self._compile_role_patterns()
    
    def _compile_role_patterns(self) -> List[re.Pattern]:
        """Compile patterns for role extraction"""
        # Build regex from job titles
        titles_fa = '|'.join(re.escape(title) for title in self.JOB_TITLES.keys())
        titles_en = '|'.join(re.escape(title) for title in self.JOB_TITLES_EN.keys())
        
        patterns = [
            re.compile(f'({titles_fa})', re.IGNORECASE),
            re.compile(f'({titles_en})', re.IGNORECASE),
            # Generic pattern for role-like text
            re.compile(r'\b(مدیر|رئیس|مسئول|کارشناس)\s+\w+', re.IGNORECASE),
        ]
        return patterns
    
    def extract_roles(self, text: str) -> List[str]:
        """Extract job roles/titles from text"""
        if not text:
            return []
        
        roles = set()
        
        for pattern in self.role_patterns:
            matches = pattern.finditer(text)
            for match in matches:
                role = match.group(0).strip()
                if role:
                    roles.add(role)
        
        return list(roles)
    
    def extract_person_mentions(self, text: str) -> List[dict]:
        """Extract mentions of people with potential roles"""
        if not text:
            return []
        
        results = []
        
        # Pattern: Role + Name
        pattern = r'(\bمدیر|رئیس|مسئول|متخصص|کارشناس|مهندس)?\s+([\u0600-\u06FF]+(?:\s+[\u0600-\u06FF]+)?)'
        matches = re.finditer(pattern, text)
        
        for match in matches:
            role = match.group(1) or "Unknown"
            name = match.group(2)
            
            if name and len(name.split()) <= 3:  # Max 3 word names
                results.append({
                    'name': name.strip(),
                    'role': role.strip(),
                    'confidence': self._score_person_mention(match.group(0), text),
                })
        
        return results
    
    def extract_person_with_role(self, text: str, target_role: Optional[str] = None) -> List[dict]:
        """Extract persons matching specific role"""
        mentions = self.extract_person_mentions(text)
        
        if target_role:
            # Filter by role similarity
            mentions = [
                m for m in mentions
                if fuzz.token_set_ratio(m['role'].lower(), target_role.lower()) > 60
            ]
        
        return mentions
    
    def _score_person_mention(self, mention: str, context: str) -> float:
        """Score how likely a mention is a real person"""
        score = 0.5
        
        # Boost if appears multiple times
        if context.lower().count(mention.lower()) > 1:
            score += 0.2
        
        # Boost if in structured context (like contact info)
        if any(indicator in context for indicator in ['تماس', 'رابط', 'نماینده', 'مسئول']):
            score += 0.2
        
        return min(score, 1.0)
    
    def normalize_role(self, role: str) -> Optional[str]:
        """Normalize role to standard form"""
        role = role.strip().lower()
        
        # Check Persian
        for fa_role, en_role in self.JOB_TITLES.items():
            if fa_role.lower() == role:
                return fa_role
        
        # Check English
        for en_role_key, en_role_val in self.JOB_TITLES_EN.items():
            if en_role_key.lower() == role:
                return en_role_val
        
        # Fuzzy match
        for fa_role in self.JOB_TITLES.keys():
            if fuzz.token_set_ratio(role, fa_role.lower()) > 80:
                return fa_role
        
        return None
