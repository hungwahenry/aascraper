# AA Flight Scraper

Automated web scraper for American Airlines that compares cash prices vs award (points) prices and calculates Cents Per Point (CPP) value.

## Features

- Scrapes both cash and award pricing for the same flights
- Calculates CPP (Cents Per Point) using formula: `(cash_price - taxes_fees) / points_required × 100`
- Bypasses Akamai bot detection using undetected-chromedriver
- Outputs structured JSON with flight data
- Docker support for containerized deployment

## Installation

### Local Setup

```bash
# Clone the repository
git clone https://github.com/hungwahenry/aascraper.git
cd aascraper

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the scraper
python main.py
```

### Docker

```bash
# Pull from Docker Hub
docker pull henryhenter/aa-scraper:latest

# Run the container
docker run --rm henryhenter/aa-scraper:latest
```

Or build locally:

```bash
docker build --platform linux/amd64 -t aa-scraper .
docker run --rm aa-scraper
```

## Configuration

Edit `src/config.py` to customize all parameters present.

## Output

Results are saved to `output/results_TIMESTAMP.json`:

```json
{
  "search_metadata": {
    "origin": "LAX",
    "destination": "JFK",
    "date": "2025-12-15",
    "passengers": 1,
    "cabin_class": "economy"
  },
  "flights": [
    {
      "flight_number": "AA1",
      "departure_time": "6:05 AM",
      "arrival_time": "2:10 PM",
      "points_required": 15000,
      "cash_price_usd": 159.0,
      "taxes_fees_usd": 5.6,
      "cpp": 1.02
    }
  ],
  "total_results": 40
}
```

## Architecture

```
AAScraper/
├── src/
│   ├── browser.py      # Browser automation setup
│   ├── scraper.py      # Flight data extraction
│   ├── calculator.py   # CPP calculation logic
│   └── config.py       # Configuration settings
├── main.py             # Entry point
├── Dockerfile          # Docker configuration
└── requirements.txt    # Python dependencies
```

## Tech Stack

- **Python 3.13**
- **Selenium** - Browser automation
- **undetected-chromedriver** - Bot detection bypass
- **Chrome** - Headless browser

## Known Limitations

- Headless mode may be blocked by Akamai in some environments
- Chrome version must match ChromeDriver version
- Requires stable internet connection

## License

MIT

## Author

Henry Henter
