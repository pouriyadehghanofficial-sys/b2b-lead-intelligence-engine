"""HTTP client with retry logic and proxy support"""

import os
from typing import Optional, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin
import logging
from app.network.retry import RetryStrategy, BackoffStrategy

logger = logging.getLogger(__name__)


class HTTPClient:
    """Robust HTTP client with automatic retry and fallback"""
    
    def __init__(
        self,
        user_agent: str = "B2B-Lead-Intelligence/1.0",
        timeout: int = 30,
        retries: int = 3,
        verify_ssl: bool = True,
    ):
        self.user_agent = user_agent
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.retry_strategy = RetryStrategy(
            max_retries=retries,
            backoff_factor=1.5,
            strategy=BackoffStrategy.EXPONENTIAL,
        )
        
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry adapter"""
        session = requests.Session()
        
        # Set headers
        session.headers.update({
            "User-Agent": self.user_agent,
            "Accept": "application/json, text/html",
            "Accept-Language": "fa,en;q=0.9",
        })
        
        # Set proxy if available
        proxy = self._get_proxy()
        if proxy:
            session.proxies.update(proxy)
            logger.info(f"Using proxy: {proxy}")
        
        # Set SSL verification
        session.verify = self.verify_ssl
        
        return session
    
    def _get_proxy(self) -> Optional[Dict[str, str]]:
        """Get proxy configuration from environment"""
        http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
        https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
        
        if http_proxy or https_proxy:
            proxy = {}
            if http_proxy:
                proxy["http"] = http_proxy
            if https_proxy:
                proxy["https"] = https_proxy
            return proxy
        return None
    
    def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """GET request with retries"""
        merged_headers = {**self.session.headers}
        if headers:
            merged_headers.update(headers)
        
        def request_func():
            return self.session.get(
                url,
                headers=merged_headers,
                params=params,
                timeout=self.timeout,
                **kwargs
            )
        
        try:
            response = self.retry_strategy.execute(request_func)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"GET request failed: {url} - {str(e)}")
            raise
    
    def post(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """POST request with retries"""
        merged_headers = {**self.session.headers}
        if headers:
            merged_headers.update(headers)
        
        def request_func():
            return self.session.post(
                url,
                json=json,
                data=data,
                headers=merged_headers,
                timeout=self.timeout,
                **kwargs
            )
        
        try:
            response = self.retry_strategy.execute(request_func)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"POST request failed: {url} - {str(e)}")
            raise
    
    def close(self):
        """Close session"""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
