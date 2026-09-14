"""Phone validation and normalization"""

import re
from typing import Optional, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class PhoneType(Enum):
    """Type of phone number"""
    MOBILE = "mobile"
    LANDLINE = "landline"
    UNKNOWN = "unknown"


class PhoneValidator:
    """Base phone validator"""
    
    def validate(self, phone: str) -> bool:
        """Validate phone number format"""
        raise NotImplementedError
    
    def normalize(self, phone: str) -> Optional[str]:
        """Normalize phone to standard format"""
        raise NotImplementedError
    
    def get_type(self, phone: str) -> PhoneType:
        """Get type of phone number"""
        return PhoneType.UNKNOWN


class IranianPhoneValidator(PhoneValidator):
    """Iranian phone number validator"""
    
    # Mobile prefixes (Iran)
    MOBILE_PREFIXES = {
        '0901', '0902', '0903', '0905', '0930', '0933', '0934', '0935',
        '0936', '0937', '0938', '0939', '0910', '0911', '0912', '0913',
        '0914', '0915', '0916', '0917', '0918', '0919', '0920', '0921',
        '0922', '0932', '0931',
    }
    
    # Landline prefixes (sample)
    LANDLINE_PREFIXES = {
        '021',  # Tehran
        '031',  # Isfahan
        '041',  # Tabriz
        '051',  # Mashhad
        '061',  # Shiraz
        '071',  # Ahvaz
    }
    
    def validate(self, phone: str) -> bool:
        """Validate Iranian phone number"""
        if not phone:
            return False
        
        # Clean phone
        cleaned = self.normalize(phone)
        if not cleaned:
            return False
        
        # Check length (10 digits for mobile, 10-11 for landline)
        if len(cleaned) not in [10, 11]:
            return False
        
        # Check if starts with 0
        if not cleaned.startswith('0'):
            return False
        
        return True
    
    def normalize(self, phone: str) -> Optional[str]:
        """Normalize Iranian phone number"""
        if not phone:
            return None
        
        # Convert to string
        phone = str(phone).strip()
        
        # Remove common separators
        phone = re.sub(r'[\s\-().]', '', phone)
        
        # Handle country codes
        if phone.startswith('+98'):
            phone = '0' + phone[3:]
        elif phone.startswith('0098'):
            phone = '0' + phone[4:]
        elif phone.startswith('98'):
            phone = '0' + phone[2:]
        
        # Remove non-digit characters
        phone = re.sub(r'\D', '', phone)
        
        # Validate basic format
        if not phone.startswith('0'):
            return None
        
        if len(phone) < 10 or len(phone) > 11:
            return None
        
        # Pad to 11 digits if needed
        if len(phone) == 10:
            phone = '0' + phone
        
        return phone
    
    def get_type(self, phone: str) -> PhoneType:
        """Get type of Iranian phone number"""
        normalized = self.normalize(phone)
        if not normalized:
            return PhoneType.UNKNOWN
        
        # Check mobile prefixes
        prefix = normalized[:4]
        if prefix in self.MOBILE_PREFIXES:
            return PhoneType.MOBILE
        
        # Check landline prefixes (first 3 digits after 0)
        prefix3 = normalized[:3]
        if prefix3 in self.LANDLINE_PREFIXES:
            return PhoneType.LANDLINE
        
        # If starts with 0 and has 11 digits, likely landline
        if len(normalized) == 11:
            return PhoneType.LANDLINE
        
        return PhoneType.UNKNOWN
    
    def format_display(self, phone: str) -> str:
        """Format phone for display"""
        normalized = self.normalize(phone)
        if not normalized:
            return phone
        
        # Format: 0912-xxx-xxxx
        if len(normalized) == 11:
            return f"{normalized[:4]}-{normalized[4:7]}-{normalized[7:]}"
        else:
            return f"{normalized[:3]}-{normalized[3:6]}-{normalized[6:]}"
