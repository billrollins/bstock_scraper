# Database operations 

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL construction
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy setup
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# src/models/database_models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..storage.database import Base
from datetime import datetime

class AuctionDB(Base):
    __tablename__ = "auctions"

    id = Column(Integer, primary_key=True, index=True)
    auction_id = Column(String, unique=True, index=True)
    marketplace = Column(String, index=True)
    title = Column(String)
    current_bid = Column(Float)
    total_units = Column(Integer)
    condition = Column(String)
    retail_value = Column(Float)
    location = Column(String)
    end_time = Column(DateTime)
    shipping_cost = Column(Float, nullable=True)
    total_bids = Column(Integer, nullable=True)
    cost_per_unit = Column(Float, nullable=True)
    source_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)