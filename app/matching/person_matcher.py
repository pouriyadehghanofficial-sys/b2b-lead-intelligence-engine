"""Person name and role matching"""

import logging
from typing import Optional, Tuple
from fuzzywuzzy import fuzz

logger = logging.getLogger(__name__)


class PersonMatcher:
    """Match persons by name and role"""
    
    def __init__(self, name_threshold: float = 0.85):
        self.name_threshold = name_threshold
    
    def match_names(self, name1: str, name2: str) -> float:
        """Match two person names (0-1)"""
        if not name1 or not name2:
            return 0.0
        
        # Exact match
        if name1.strip().lower() == name2.strip().lower():
            return 1.0
        
        # Token set ratio (order-independent)
        score = fuzz.token_set_ratio(name1.lower(), name2.lower()) / 100.0
        
        return score
    
    def match_roles(self, role1: str, role2: str) -> float:
        """Match two roles (0-1)"""
        if not role1 or not role2:
            return 0.0
        
        if role1.strip().lower() == role2.strip().lower():
            return 1.0
        
        score = fuzz.token_set_ratio(role1.lower(), role2.lower()) / 100.0
        return score
    
    def match_person(
        self,
        name1: str,
        role1: Optional[str],
        name2: str,
        role2: Optional[str],
    ) -> float:
        """Match complete person profiles"""
        name_score = self.match_names(name1, name2)
        
        if name_score < 0.5:  # Names don't match enough
            return 0.0
        
        # If we have roles, they should also match reasonably
        if role1 and role2:
            role_score = self.match_roles(role1, role2)
            return (name_score * 0.7) + (role_score * 0.3)
        
        return name_score
