# Auction data model 

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Auction:
    """Base auction model representing common fields across marketplaces"""
    auction_id: str
    title: str
    current_bid: float
    total_units: int
    condition: str
    retail_value: float
    location: str
    end_time: datetime
    shipping_cost: Optional[float] = None
    total_bids: Optional[int] = None
    cost_per_unit: Optional[float] = None
    marketplace: str
    source_url: str
    
    @property
    def is_ending_soon(self) -> bool:
        """Check if auction is ending within 1 hour"""
        if not self.end_time:
            return False
        return (self.end_time - datetime.now()).total_seconds() < 3600