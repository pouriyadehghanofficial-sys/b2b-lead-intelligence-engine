"""Proxy configuration and management"""

import os
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class ProxyManager:
    """Manage proxy configuration"""
    
    @staticmethod
    def get_proxy_config() -> Optional[Dict[str, str]]:
        """Get proxy configuration from environment"""
        http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
        https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
        
        if http_proxy or https_proxy:
            proxy = {}
            if http_proxy:
                proxy["http"] = http_proxy
                logger.debug(f"HTTP proxy configured")
            if https_proxy:
                proxy["https"] = https_proxy
                logger.debug(f"HTTPS proxy configured")
            return proxy
        return None
    
    @staticmethod
    def validate_proxy(proxy_url: str) -> bool:
        """Validate proxy URL format"""
        try:
            from urllib.parse import urlparse
            result = urlparse(proxy_url)
            return all([result.scheme in ['http', 'https', 'socks5'], result.netloc])
        except Exception as e:
            logger.error(f"Invalid proxy URL: {str(e)}")
            return False
