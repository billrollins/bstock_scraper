# Abstract base parser 

from abc import ABC, abstractmethod
from typing import List, Optional
from bs4 import BeautifulSoup
from ..models.auction import Auction

class BaseParser(ABC):
    """Abstract base class for marketplace-specific parsers"""
    
    @abstractmethod
    def parse_auction_list(self, html: str) -> List[Auction]:
        """Parse auction listing page and return list of auctions"""
        pass
    
    @abstractmethod
    def parse_auction_detail(self, html: str) -> Optional[Auction]:
        """Parse individual auction detail page"""
        pass
    
    def _parse_price(self, price_str: str) -> float:
        """Helper method to parse price strings"""
        try:
            return float(price_str.replace('$', '').replace(',', '').strip())
        except (ValueError, AttributeError):
            return 0.0

    def _parse_datetime(self, date_str: str) -> Optional[datetime]:
        """Helper method to parse datetime strings"""
        try:
            return datetime.strptime(date_str.strip(), '%a %b %d, %Y %I:%M:%S %p')
        except (ValueError, AttributeError):
            return None