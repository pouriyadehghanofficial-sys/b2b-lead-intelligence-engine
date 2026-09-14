"""Company entity model"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class Company:
    """Company entity"""
    
    name: str
    industry: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None
    
    # Metadata
    source_urls: List[str] = field(default_factory=list)
    confidence: float = 0.0
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    verified: bool = False
    
    def add_source(self, url: str):
        """Add a source URL"""
        if url and url not in self.source_urls:
            self.source_urls.append(url)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "industry": self.industry,
            "city": self.city,
            "province": self.province,
            "website": self.website,
            "phone": self.phone,
            "email": self.email,
            "description": self.description,
            "source_urls": self.source_urls,
            "confidence": self.confidence,
            "first_seen": self.first_seen.isoformat() if self.first_seen else None,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "verified": self.verified,
        }
