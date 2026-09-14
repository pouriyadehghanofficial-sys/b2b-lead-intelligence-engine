"""Entity resolution - linking companies, people, and phones"""

import logging
from typing import List, Optional, Tuple, Dict
from app.matching.phone_matcher import PhoneMatcher
from app.matching.person_matcher import PersonMatcher
from app.matching.company_matcher import CompanyMatcher
from app.entities.lead import Lead

logger = logging.getLogger(__name__)


class EntityResolver:
    """Resolve relationships between entities"""
    
    def __init__(self):
        self.phone_matcher = PhoneMatcher()
        self.person_matcher = PersonMatcher()
        self.company_matcher = CompanyMatcher()
    
    def resolve_lead(
        self,
        company_name: str,
        person_name: Optional[str] = None,
        role: Optional[str] = None,
        phone: Optional[str] = None,
        evidence_count: int = 1,
    ) -> Lead:
        """Create a lead with resolution confidence"""
        lead = Lead(
            company_name=company_name,
            person_name=person_name,
            role=role,
            phone=phone,
        )
        
        # Confidence factors
        company_confidence = 0.7  # Company name from search result
        person_confidence = 0.0
        role_confidence = 0.0
        phone_confidence = 0.0
        
        # Person confidence
        if person_name:
            person_confidence = 0.6  # Person mentioned on website
            if evidence_count > 1:
                person_confidence = min(0.9, person_confidence + 0.2)
        
        # Role confidence
        if role:
            role_confidence = 0.6  # Role mentioned with person
            if person_name:
                role_confidence = min(0.9, role_confidence + 0.2)
        
        # Phone confidence
        if phone:
            phone_confidence = 0.7  # Phone from company website
            if person_name and role:  # Associated with specific person/role
                phone_confidence = min(0.95, phone_confidence + 0.2)
        
        # Update lead
        lead.company_confidence = company_confidence
        lead.person_confidence = person_confidence
        lead.role_confidence = role_confidence
        lead.phone_validity = phone_confidence
        lead.confidence_score = (company_confidence + person_confidence + role_confidence + phone_confidence) / 4
        
        return lead
    
    def can_merge(
        self,
        lead1: Lead,
        lead2: Lead,
        company_threshold: float = 0.85,
        person_threshold: float = 0.85,
        phone_threshold: float = 0.95,
    ) -> bool:
        """Check if two leads refer to the same entity"""
        # Must have matching company
        company_match = self.company_matcher.match(lead1.company_name, lead2.company_name)
        if company_match < company_threshold:
            return False
        
        # Check phones if both have them
        if lead1.phone and lead2.phone:
            phone_match = self.phone_matcher.match(lead1.phone, lead2.phone)
            if phone_match < phone_threshold:
                return False
        
        # Check persons if both have them
        if lead1.person_name and lead2.person_name:
            person_match = self.person_matcher.match_names(lead1.person_name, lead2.person_name)
            if person_match < person_threshold:
                return False
        
        return True
    
    def merge_leads(self, lead1: Lead, lead2: Lead) -> Lead:
        """Merge two related leads"""
        # Keep the one with higher score
        primary = lead1 if lead1.confidence_score >= lead2.confidence_score else lead2
        secondary = lead2 if primary == lead1 else lead1
        
        # Merge details
        if not primary.person_name and secondary.person_name:
            primary.person_name = secondary.person_name
            primary.person_confidence = max(primary.person_confidence, secondary.person_confidence)
        
        if not primary.role and secondary.role:
            primary.role = secondary.role
            primary.role_confidence = max(primary.role_confidence, secondary.role_confidence)
        
        if not primary.phone and secondary.phone:
            primary.phone = secondary.phone
            primary.phone_validity = max(primary.phone_validity, secondary.phone_validity)
        
        # Merge evidence
        for evidence in secondary.evidence:
            if evidence not in primary.evidence:
                primary.add_evidence(evidence)
        
        # Update scores
        primary.update_score()
        
        return primary
