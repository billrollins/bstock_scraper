import logging
import aiohttp
from typing import Optional
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from ..utils.http import get_user_agent

logger = logging.getLogger(__name__)

class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass

class BStockAuthenticator:
    """Handles authentication with B-Stock marketplaces"""
    
    MARKETPLACE_URLS = {
        "amazon": "https://bstock.com/amazon",
        "target": "https://bstock.com/target"
    }

    def __init__(self, email: str, password: str, marketplace: str = "amazon"):
        if marketplace.lower() not in self.MARKETPLACE_URLS:
            raise ValueError(f"Unsupported marketplace: {marketplace}")
            
        self.email = email
        self.password = password
        self.marketplace = marketplace.lower()
        self.base_url = self.MARKETPLACE_URLS[marketplace]
        self.session: Optional[aiohttp.ClientSession] = None
        self.last_auth: Optional[datetime] = None
        self.auth_token: Optional[str] = None

    async def create_session(self) -> None:
        """Create a new aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
        
        headers = {
            "User-Agent": get_user_agent(),
            "Accept": "text/html,application/xhtml+xml,*/*",
        }
        self.session = aiohttp.ClientSession(headers=headers)

    async def close(self) -> None:
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None
            self.last_auth = None
            self.auth_token = None

    def is_authenticated(self) -> bool:
        """Check if current session is authenticated and not expired"""
        if not all([self.last_auth, self.session, not self.session.closed]):
            return False
        return (datetime.now() - self.last_auth) < timedelta(hours=1)

    async def login(self) -> None:
        """Authenticate with B-Stock"""
        if self.is_authenticated():
            return

        if not self.session or self.session.closed:
            await self.create_session()

        try:
            # Get form key
            login_response = await self.session.get(f"{self.base_url}/customer/account/login/")
            await login_response.raise_for_status()
            html = await login_response.text()
            
            # Parse form key
            soup = BeautifulSoup(html, 'html.parser')
            form_key = soup.select_one('input[name="form_key"]')
            if not form_key or not form_key.get('value'):
                raise AuthenticationError("Could not find form key")
            
            # Login request
            login_data = {
                'form_key': form_key['value'],
                'login[username]': self.email,
                'login[password]': self.password
            }
            
            response = await self.session.post(
                f"{self.base_url}/customer/account/loginPost/",
                data=login_data
            )
            await response.raise_for_status()
            
            if "login" in str(response.url):
                raise AuthenticationError("Invalid credentials")

            self.last_auth = datetime.now()
            self.auth_token = response.cookies.get('frontend')

        except Exception as e:
            raise AuthenticationError(f"Login failed: {str(e)}")

    async def make_authenticated_request(self, url: str, method: str = "GET", **kwargs) -> aiohttp.ClientResponse:
        """Make an authenticated request"""
        if not self.is_authenticated():
            await self.login()

        response = await self.session.request(method, url, **kwargs)
        await response.raise_for_status()
        
        return response

    async def __aenter__(self):
        if not self.session:
            await self.create_session()
        await self.login()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()