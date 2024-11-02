# B-Stock Scraper

A Python-based web scraper for collecting auction data from B-Stock marketplaces (Amazon and Target). The scraper monitors auctions, tracks pricing, and stores historical data for analysis.

## Project Structure

```
bstock_scraper/
├── alembic/              # Database migrations
├── config/              
│   ├── settings.py       # Application configuration
│   └── marketplaces/     # Marketplace-specific settings
├── notebooks/            # Jupyter notebooks for data analysis
├── scripts/
│   ├── export_data.py    # Data export utilities
│   └── run_scraper.py    # Main execution script
├── src/
│   ├── core/             # Core functionality
│   │   ├── auth.py       # Authentication handling
│   │   ├── rate_limiter.py  # Request rate limiting
│   │   └── scraper.py    # Main scraping logic
│   ├── models/           # Data models
│   │   ├── auction.py    # Auction data structure
│   │   └── marketplace.py # Marketplace configuration
│   ├── parsers/          # HTML parsing
│   │   ├── amazon_parser.py
│   │   ├── base_parser.py
│   │   └── target_parser.py
│   ├── storage/          # Data persistence
│   │   ├── database.py   # Database operations
│   │   └── exporters.py  # Export functionality
│   └── utils/            # Utility functions
│       ├── http.py       # HTTP helpers
│       └── logging.py    # Logging configuration
└── tests/                # Test suite
```

## Features

- Scrapes auction data from multiple B-Stock marketplaces:
  - Amazon Returns
  - Target Liquidation
- Implements rate limiting to respect website policies
- Stores data in PostgreSQL database
- Tracks key auction metrics:
  - Current bid
  - Total units
  - Retail value
  - Location
  - Shipping costs
  - Cost per unit
  - Auction end time

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Unix
.\venv\Scripts\activate   # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and update with your credentials:
```bash
cp .env.example .env
```

4. Initialize the database:
```bash
alembic upgrade head
```

## TODOs

### High Priority
- [ ] Implement authentication in `src/core/auth.py`
- [ ] Complete Amazon parser implementation in `src/parsers/amazon_parser.py`
- [ ] Implement Target parser in `src/parsers/target_parser.py`
- [ ] Add error handling and retry logic in `src/core/scraper.py`
- [ ] Implement main scraping loop in `scripts/run_scraper.py`

### Medium Priority
- [ ] Add database models for historical price tracking
- [ ] Implement shipping cost calculator
- [ ] Add logging throughout the application
- [ ] Create data export functionality in `scripts/export_data.py`
- [ ] Add unit tests for parsers and data models

### Low Priority
- [ ] Add documentation for all modules
- [ ] Create dashboard for visualizing auction data
- [ ] Implement email notifications for interesting auctions
- [ ] Add support for additional B-Stock marketplaces
- [ ] Create Dockerfile for containerization

### Infrastructure
- [ ] Set up CI/CD pipeline
- [ ] Add monitoring and alerting
- [ ] Implement backup strategy for database
- [ ] Add rate limiting configuration per marketplace
- [ ] Create deployment documentation

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is private and confidential.

## Notes

- Remember to respect B-Stock's terms of service and rate limiting
- Keep credentials secure and never commit them to the repository
- Regular backups of the database are recommended