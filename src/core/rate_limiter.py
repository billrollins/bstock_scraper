# Rate limiting implementation 
import time
from datetime import datetime, timedelta
from collections import deque
from typing import Deque, Optional
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """Rate limiter implementation using token bucket algorithm"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.window_size = 60  # 1 minute in seconds
        self.requests: Deque[datetime] = deque()
    
    async def acquire(self) -> bool:
        """Acquire permission to make a request"""
        now = datetime.now()
        
        # Remove requests older than window_size
        while self.requests and (now - self.requests[0]).total_seconds() > self.window_size:
            self.requests.popleft()
        
        # Check if we can make a new request
        if len(self.requests) < self.requests_per_minute:
            self.requests.append(now)
            return True
        
        # Calculate wait time
        wait_time = (self.requests[0] + timedelta(seconds=self.window_size) - now).total_seconds()
        if wait_time > 0:
            logger.info(f"Rate limit reached, waiting {wait_time:.2f} seconds")
            time.sleep(wait_time)
            self.requests.popleft()
            self.requests.append(datetime.now())
            return True
        
        return False