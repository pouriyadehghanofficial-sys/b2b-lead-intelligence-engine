"""Lead entity model - final output"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from app.entities.evidence import Evidence


class LeadStatus(Enum):
    """Status of a lead"""
    VERIFIED = "VERIFIED"
    LIKELY = "LIKELY"
    POSSIBLE = "POSSIBLE"
    UNVERIFIED = "UNVERIFIED"
    NOT_FOUND = "NOT_FOUND"
    REJECTED = "REJECTED"


@dataclass
class Lead:
    """Final lead output"""
    
    company_name: str
    person_name: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    
    # Company details
    industry: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    website: Optional[str] = None
    
    # Scoring
    confidence_score: float = 0.0
    lead_score: float = 0.0
    phone_validity: float = 0.0
    person_confidence: float = 0.0
    company_confidence: float = 0.0
    role_confidence: float = 0.0
    industry_confidence: float = 0.0
    freshness_score: float = 0.0
    
    # Evidence
    evidence: List[Evidence] = field(default_factory=list)
    status: LeadStatus = LeadStatus.UNVERIFIED
    
    # Metadata
    discovered_at: Optional[datetime] = field(default_factory=datetime.now)
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    duplicate_of: Optional[str] = None  # ID of original if duplicate
    
    def add_evidence(self, evidence: Evidence):
        """Add evidence for this lead"""
        self.evidence.append(evidence)
    
    def update_score(self):
        """Update lead score based on components"""
        # Simple weighted average - can be customized
        weights = {
            'phone_validity': 0.20,
            'person_confidence': 0.20,
            'company_confidence': 0.20,
            'role_confidence': 0.15,
            'industry_confidence': 0.15,
            'freshness_score': 0.10,
        }
        
        self.lead_score = (
            self.phone_validity * weights['phone_validity'] +
            self.person_confidence * weights['person_confidence'] +
            self.company_confidence * weights['company_confidence'] +
            self.role_confidence * weights['role_confidence'] +
            self.industry_confidence * weights['industry_confidence'] +
            self.freshness_score * weights['freshness_score']
        )
        
        # Determine status
        if self.lead_score >= 0.85:
            self.status = LeadStatus.VERIFIED
        elif self.lead_score >= 0.65:
            self.status = LeadStatus.LIKELY
        elif self.lead_score >= 0.45:
            self.status = LeadStatus.POSSIBLE
        else:
            self.status = LeadStatus.UNVERIFIED
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "company_name": self.company_name,
            "person_name": self.person_name,
            "role": self.role,
            "phone": self.phone,
            "email": self.email,
            "industry": self.industry,
            "city": self.city,
            "province": self.province,
            "website": self.website,
            "confidence_score": round(self.confidence_score, 3),
            "lead_score": round(self.lead_score, 3),
            "phone_validity": round(self.phone_validity, 3),
            "person_confidence": round(self.person_confidence, 3),
            "company_confidence": round(self.company_confidence, 3),
            "role_confidence": round(self.role_confidence, 3),
            "industry_confidence": round(self.industry_confidence, 3),
            "freshness_score": round(self.freshness_score, 3),
            "status": self.status.value,
            "evidence_count": len(self.evidence),
            "discovered_at": self.discovered_at.isoformat() if self.discovered_at else None,
        }
