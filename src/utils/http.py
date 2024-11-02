# HTTP utilities 
import random
from typing import List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def get_user_agent() -> str:
    """
    Returns a randomly selected user agent string from a list of common browsers.
    This helps prevent blocking by making requests appear more like regular browser traffic.
    """
    user_agents = [
        # Chrome on Windows 10
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        # Firefox on Windows 10
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        # Edge on Windows 10
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        # Safari on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        # Chrome on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    return random.choice(user_agents)

class RequestError(Exception):
    """Base exception for HTTP request errors"""
    pass

class HTTPClient:
    """
    HTTP client utility class with built-in retry logic and error handling
    """
    def __init__(self, max_retries: int = 3, timeout: int = 30):
        self.max_retries = max_retries
        self.timeout = timeout
        self._session = None
        self._last_request_time: Optional[datetime] = None

    def get_headers(self, additional_headers: Optional[dict] = None) -> dict:
        """
        Get default headers with optional additional headers
        
        Args:
            additional_headers: Optional dictionary of additional headers to include
        
        Returns:
            Dictionary of HTTP headers
        """
        headers = {
            "User-Agent": get_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }
        
        if additional_headers:
            headers.update(additional_headers)
            
        return headers

    @staticmethod
    def parse_cookies(cookie_string: str) -> dict:
        """
        Parse cookie string into dictionary
        
        Args:
            cookie_string: String containing cookies
            
        Returns:
            Dictionary of cookie name-value pairs
        """
        cookies = {}
        if not cookie_string:
            return cookies
            
        for cookie in cookie_string.split(';'):
            if '=' in cookie:
                name, value = cookie.split('=', 1)
                cookies[name.strip()] = value.strip()
        return cookies

    @staticmethod
    def build_url(base_url: str, path: str = "", params: Optional[dict] = None) -> str:
        """
        Build complete URL from components
        
        Args:
            base_url: Base URL
            path: Optional path to append
            params: Optional query parameters
            
        Returns:
            Complete URL string
        """
        url = base_url.rstrip('/')
        
        if path:
            url += '/' + path.lstrip('/')
            
        if params:
            param_strings = []
            for key, value in params.items():
                if isinstance(value, (list, tuple)):
                    for v in value:
                        param_strings.append(f"{key}={v}")
                else:
                    param_strings.append(f"{key}={value}")
            if param_strings:
                url += '?' + '&'.join(param_strings)
                
        return url

    @staticmethod
    def is_success_status(status_code: int) -> bool:
        """Check if HTTP status code indicates success"""
        return 200 <= status_code < 300

    @staticmethod
    def should_retry(status_code: int) -> bool:
        """
        Determine if request should be retried based on status code
        
        Args:
            status_code: HTTP status code
            
        Returns:
            Boolean indicating if retry is appropriate
        """
        # Retry on server errors (5xx) and specific client errors
        return (
            status_code >= 500 or  # Server errors
            status_code == 429 or  # Too Many Requests
            status_code == 408 or  # Request Timeout
            status_code == 404     # Not Found (temporary)
        )