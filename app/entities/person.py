"""Person entity model"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class Person:
    """Person entity"""
    
    name: str
    role: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    
    # Metadata
    source_urls: List[str] = field(default_factory=list)
    confidence: float = 0.0
    role_confidence: float = 0.0
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
            "role": self.role,
            "company_name": self.company_name,
            "email": self.email,
            "phone": self.phone,
            "source_urls": self.source_urls,
            "confidence": self.confidence,
            "role_confidence": self.role_confidence,
            "first_seen": self.first_seen.isoformat() if self.first_seen else None,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "verified": self.verified,
        }
