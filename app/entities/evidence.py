"""Evidence entity model"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class EvidenceType(Enum):
    """Type of evidence source"""
    WEBSITE = "website"
    DIRECTORY = "directory"
    PDF = "pdf"
    SOCIAL_MEDIA = "social_media"
    SEARCH_RESULT = "search_result"
    NEWS = "news"
    EXHIBITION = "exhibition"
    CATALOG = "catalog"
    ASSOCIATION = "association"
    OTHER = "other"


@dataclass
class Evidence:
    """Evidence for a claim"""
    
    url: str
    source_type: EvidenceType
    extracted_text: str
    entity_type: str  # 'company', 'person', 'phone', 'role', etc.
    entity_value: str
    confidence: float = 0.8
    
    # Metadata
    discovered_at: Optional[datetime] = field(default_factory=datetime.now)
    published_date: Optional[datetime] = None
    last_checked: Optional[datetime] = None
    is_valid: bool = True
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "url": self.url,
            "source_type": self.source_type.value,
            "extracted_text": self.extracted_text[:200],  # First 200 chars
            "entity_type": self.entity_type,
            "entity_value": self.entity_value,
            "confidence": self.confidence,
            "discovered_at": self.discovered_at.isoformat() if self.discovered_at else None,
            "published_date": self.published_date.isoformat() if self.published_date else None,
            "last_checked": self.last_checked.isoformat() if self.last_checked else None,
            "is_valid": self.is_valid,
        }
