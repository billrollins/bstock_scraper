from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # Database settings
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DATABASE_URL: Optional[str] = None

    # B-Stock credentials
    BSTOCK_EMAIL: str
    BSTOCK_PASSWORD: str

    # Scraping settings
    REQUESTS_PER_MINUTE: int = 60
    CONCURRENT_REQUESTS: int = 5

    # Base URLs
    AMAZON_BASE_URL: str = "https://bstock.com/amazon"
    TARGET_BASE_URL: str = "https://bstock.com/target"

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.DATABASE_URL:
            self.DATABASE_URL = f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

@lru_cache()
def get_settings() -> Settings:
    return Settings()