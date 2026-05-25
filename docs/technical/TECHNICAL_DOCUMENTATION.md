# 🔧 Market Bot - Complete Technical Documentation

## Table of Contents

1. [Directory Structure](#directory-structure)
2. [File-by-File Documentation](#file-by-file-documentation)
3. [Core Modules](#core-modules)
4. [Bot Versions](#bot-versions)
5. [Utility Scripts](#utility-scripts)
6. [Configuration](#configuration)
7. [Deployment](#deployment)
8. [Testing](#testing)
9. [Troubleshooting](#troubleshooting)
10. [Monitoring & Maintenance](#monitoring--maintenance)
11. [Scaling & Optimization](#scaling--optimization)
12. [Integration Guide](#integration-guide)

---

## 1. Directory Structure

### Complete Project Layout

```
market-bot/
├── src/                          # SOURCE CODE
│   ├── __init__.py              # Package initializer (version: 1.0.0)
│   ├── bots/                    # Main bot implementations
│   │   ├── __init__.py         
│   │   ├── market_bot_lite.py   # Lightweight version (382 lines)
│   │   ├── market_bot_ai.py     # AI sentiment version (547 lines)
│   │   └── market_bot_pro.py    # Professional version (439 lines)
│   ├── core/                    # Core functionality modules
│   │   ├── __init__.py
│   │   ├── analyst_ratings.py   # Analyst ratings aggregation
│   │   └── news_aggregator.py   # News from 70+ sources
│   ├── utils/                   # Utility functions
│   │   └── __init__.py         # (Ready for expansion)
│   └── config/                  # Configuration management
│       └── __init__.py         # (Ready for expansion)
│
├── scripts/                     # UTILITY SCRIPTS
│   ├── setup/                   # Initial setup & configuration
│   │   ├── add_analyst_columns.py    # Add analyst rating columns
│   │   ├── fresh_start.py            # Reset & reload database
│   │   └── setup_models.py           # Setup AI models
│   ├── maintenance/             # Database maintenance
│   │   ├── load_missing_stocks.py    # Load stocks not in DB
│   │   ├── update_prices.py          # Update all stock prices
│   │   └── check_database.py         # Database status check
│   └── analysis/                # Analysis tools
│       └── top_recommendations.py    # Top stock recommendations
│
├── data/                        # DATA FILES
│   ├── __init__.py
│   └── nse_stocks_650.py        # 675 NSE stocks data
│
├── docs/                        # DOCUMENTATION
│   ├── QUICK_START.md           # Getting started guide
│   ├── DATABASE_SCHEMA.md       # Database column reference
│   ├── SYSTEM_GUIDE.md          # System architecture
│   ├── FEATURE_IMPLEMENTATION.md # Feature details
│   ├── PRODUCTION_READY.md      # Production readiness report
│   ├── COMPREHENSIVE_FINAL_REPORT.md  # Final report
│   └── TECHNICAL_DOCUMENTATION.md     # This file
│
├── logs/                        # LOG FILES
│   ├── .gitkeep                # Placeholder
│   ├── market_bot_pro.log      # Pro version logs (auto-generated)
│   ├── fresh_start.log         # Setup logs (auto-generated)
│   └── *.log                   # Other logs (auto-generated)
│
├── archive/                     # ARCHIVED FILES
│   └── docs/                   # Old documentation (25+ files)
│
├── tests/                       # TEST FILES
│   └── (Ready for test files)
│
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
└── README.md                    # Main project documentation
```

### Directory Purposes

#### `src/` - Source Code
**Purpose**: Contains all production source code  
**Interaction**: Main entry point for all bot executions  
**Testing**: Import tests verify all modules load correctly  
**Subdirectories**:
- `bots/`: Three main bot implementations
- `core/`: Shared core functionality
- `utils/`: Helper utilities (expandable)
- `config/`: Configuration management (expandable)

#### `scripts/` - Utility Scripts
**Purpose**: One-time setup, maintenance, and analysis scripts  
**Interaction**: Uses core modules from `src/`  
**Testing**: Manual execution testing  
**Subdirectories**:
- `setup/`: Database initialization and configuration
- `maintenance/`: Ongoing database operations
- `analysis/`: Data analysis and reporting

#### `data/` - Data Files
**Purpose**: Static data files (stock lists, constants)  
**Interaction**: Imported by all bots and scripts  
**Testing**: Data validation in bot initialization  
**Contents**: NSE stock lists with market cap classification

#### `docs/` - Documentation
**Purpose**: All project documentation  
**Interaction**: Reference material for developers  
**Testing**: Documentation review and updates  
**Contents**: Technical guides, API docs, schemas

#### `logs/` - Log Files
**Purpose**: Runtime logs for monitoring and debugging  
**Interaction**: Written by bots during execution  
**Testing**: Log analysis for errors  
**Contents**: Auto-generated timestamped logs

#### `archive/` - Archived Files
**Purpose**: Historical files no longer in active use  
**Interaction**: None (reference only)  
**Testing**: Not tested  
**Contents**: Old documentation and deprecated files

#### `tests/` - Test Files
**Purpose**: Unit and integration tests  
**Interaction**: Tests all modules in `src/`  
**Testing**: Automated test execution  
**Contents**: (Ready for expansion)

---

## 2. File-by-File Documentation

### 2.1 Bot Files (`src/bots/`)

#### `market_bot_lite.py`
**Purpose**: Lightweight bot for fast daily updates without AI overhead  
**Lines of Code**: 382  
**Dependencies**: pandas, yfinance, requests  
**No AI Required**: ✅ Yes (no transformers/torch needed)

**Key Functions**:
```python
def get_market_intelligence(symbol, cap_size)
    # Fetches price, momentum, volume, sentiment, news for a stock
    # Returns dict with all stock data or NA values if data unavailable

def fetch_news(ticker)
    # Fetches news from Yahoo Finance + Google News
    # Falls back to comprehensive_news_sources if available
    # Returns: (news_text, news_titles)

def analyze_news_sentiment(news_text)
    # Keyword-based sentiment analysis
    # Returns: "Positive" | "Neutral" | "Negative"

def classify_news_type(news_text)
    # Classifies news into categories
    # Returns: List of news types (max 3)

def send_to_notion(data, rank=None)
    # Sends stock data to Notion database
    # Handles all 16 columns including NA values
```

**How It Works**:
1. Loads 675 stocks from `data.nse_stocks_650`
2. For each stock:
   - Fetches 6-month price data via yfinance
   - Calculates momentum (6-month return)
   - Calculates volume surge (vs 20-day avg)
   - Fetches news from Yahoo + Google
   - Analyzes news sentiment (keyword-based)
   - Classifies news types (8 categories)
   - Fetches analyst ratings (if available)
   - Sends to Notion with sequential rank
3. Handles stocks without data (NA values)
4. Prints summary statistics

**Testing**:
```bash
python src/bots/market_bot_lite.py
# Expected: ~5-10 mins for 675 stocks
# Output: Summary with success/failure counts
```

**Deployment**:
- Schedule daily (recommended: 6 AM after market open)
- No GPU required
- Memory: ~500MB
- Network: Requires stable internet

**Troubleshooting**:
- **ImportError**: Check `data/nse_stocks_650.py` exists
- **Notion API Error**: Verify NOTION_TOKEN and DATABASE_ID
- **yfinance timeout**: Increase timeout or retry logic
- **News fetch fails**: Falls back gracefully (uses old news)

---

#### `market_bot_ai.py`
**Purpose**: AI-powered sentiment analysis using FinBERT model
**Lines of Code**: 547
**Dependencies**: pandas, yfinance, requests, transformers, torch
**AI Required**: ✅ Yes (downloads FinBERT model ~500MB)

**Key Functions**:
```python
def initialize_sentiment_model()
    # Loads FinBERT sentiment analysis model
    # Downloads model on first run (~500MB)
    # Returns: pipeline object

def analyze_ai_sentiment(news_titles)
    # AI-powered sentiment analysis using FinBERT
    # Processes list of news titles
    # Returns: Sentiment score (-1 to +1)

def get_market_intelligence(symbol, cap_size)
    # Similar to Lite but with AI sentiment
    # Uses fetch_comprehensive_news for 70+ sources
    # Returns dict with AI sentiment score

def get_news_sentiment_label(news_text)
    # Keyword-based fallback sentiment
    # Returns: "Positive" | "Neutral" | "Negative"

def classify_news_type(news_text)
    # Same as Lite version
    # Returns: List of news types

def send_to_notion(data, rank=None)
    # Extended version with all 16 columns
    # Includes AI sentiment and news types
```

**How It Works**:
1. Initializes FinBERT model (first run: slow, subsequent: fast)
2. Loads 675 stocks with validation
3. For each stock:
   - Fetches comprehensive news (70+ sources)
   - AI analyzes news sentiment (FinBERT)
   - Calculates technical indicators
   - Fetches analyst ratings
   - Classifies news types
   - Sends to Notion
4. Advanced logging to `logs/market_bot_ai.log`

**Testing**:
```bash
# First run (slow - model download)
python src/bots/market_bot_ai.py
# Expected: ~30-45 mins first run, ~15-20 mins subsequent

# Check logs
cat logs/market_bot_ai.log
```

**Deployment**:
- Schedule weekly (recommended: Sunday evening)
- GPU recommended (but works on CPU)
- Memory: ~2GB (model loaded in RAM)
- Disk: ~1GB (model cache)
- Network: Stable internet required

**Troubleshooting**:
- **Model download fails**: Check HF_TOKEN, internet connection
- **Out of memory**: Reduce batch size or use CPU
- **Slow performance**: Use GPU or switch to Lite version
- **transformers error**: Update transformers library

---

#### `market_bot_pro.py`
**Purpose**: Production-grade version with robust logging and error handling
**Lines of Code**: 439
**Dependencies**: pandas, yfinance, requests, logging
**AI Required**: ❌ No (keyword-based sentiment)

**Key Functions**:
```python
def fetch_news(ticker)
    # Yahoo Finance news only (fast and reliable)
    # Returns: News text or None

def analyze_news_sentiment(news_text)
    # Keyword-based sentiment (same as Lite)
    # Returns: "Positive" | "Neutral" | "Negative"

def classify_news_type(news_text)
    # Same classification as other versions
    # Returns: List of news types

def get_market_data(ticker, cap_size)
    # Fetches market data with error handling
    # Returns: Dict with data or NA values

def send_to_notion(data, news_text, news_sentiment, news_types, rank)
    # Most robust implementation
    # Comprehensive error handling
    # Logs all operations
```

**How It Works**:
1. Configures advanced logging (file + console)
2. Loads validated stock list
3. For each stock:
   - Fetches data with timeout handling
   - Fetches news (Yahoo only for speed)
   - Analyzes sentiment (keyword-based)
   - Classifies news types
   - Fetches analyst ratings
   - Sends to Notion with retry logic
4. Detailed statistics and error reporting

**Testing**:
```bash
python src/bots/market_bot_pro.py

# Monitor logs in real-time
tail -f logs/market_bot_pro.log
```

**Deployment**:
- Schedule monthly (recommended: 1st of month)
- No GPU required
- Memory: ~500MB
- Logs: Rotated automatically
- Best for production monitoring

**Troubleshooting**:
- Check `logs/market_bot_pro.log` for detailed errors
- All errors logged with timestamps
- Failed stocks logged separately
- Statistics summary at end

---

### 2.2 Core Modules (`src/core/`)

#### `analyst_ratings.py`
**Purpose**: Aggregate analyst ratings from 50+ global and Indian sources
**Original Name**: `analyst_ratings_aggregator.py`
**Lines**: ~600 lines (comprehensive)

**Key Functions**:
```python
def aggregate_all_analyst_ratings(ticker)
    # Main function - aggregates all ratings for a stock
    # Returns: {
    #   'rating_numeric': float (1-5),
    #   'consensus': str ('Strong Buy', 'Buy', etc.),
    #   'analyst_count': int,
    #   'has_data': bool
    # }

def fetch_yahoo_analyst_ratings(ticker)
    # Fetches ratings from Yahoo Finance API
    # Returns: List of ratings or empty list

def fetch_indian_analyst_ratings(ticker)
    # Fetches ratings from Indian brokerages
    # Returns: List of ratings

def normalize_rating(rating)
    # Normalizes different rating scales to 1-5
    # Input: Various formats ('Buy', 4/5, 'Outperform', etc.)
    # Output: Float (1.0 to 5.0)

def calculate_consensus(avg_rating)
    # Converts numeric rating to consensus text
    # 4.5-5.0: Strong Buy
    # 4.0-4.5: Buy
    # 3.5-4.0: Moderate Buy
    # 2.5-3.5: Hold
    # 2.0-2.5: Moderate Sell
    # 1.5-2.0: Sell
    # 1.0-1.5: Strong Sell
```

**Data Sources**:
1. **Global Investment Banks** (via Yahoo Finance):
   - JP Morgan, Goldman Sachs, Morgan Stanley
   - Bank of America, Citi, Credit Suisse
   - Deutsche Bank, UBS, Barclays

2. **Indian Brokerages**:
   - Motilal Oswal, IIFL, Kotak Securities
   - ICICI Direct, HDFC Securities
   - Sharekhan, Angel Broking

3. **Rating Agencies**:
   - CRISIL, ICRA, CARE Ratings
   - India Ratings, Brickwork Ratings

**How It Works**:
1. Attempts to fetch ratings from Yahoo Finance
2. Falls back to Indian brokerage sources if needed
3. Normalizes all ratings to 1-5 scale
4. Calculates average rating
5. Determines consensus label
6. Returns structured data or 'No Consensus'

**Usage**:
```python
from src.core.analyst_ratings import aggregate_all_analyst_ratings

ratings = aggregate_all_analyst_ratings("RELIANCE.NS")
print(ratings)
# Output: {
#   'rating_numeric': 4.35,
#   'consensus': 'Strong Buy',
#   'analyst_count': 23,
#   'has_data': True
# }
```

**Testing**:
```python
# Test with known stock
python -c "from src.core.analyst_ratings import aggregate_all_analyst_ratings; print(aggregate_all_analyst_ratings('TCS.NS'))"
```

**Error Handling**:
- Network timeouts: Returns empty ratings
- Invalid ticker: Returns 'No Consensus'
- No ratings found: Returns has_data=False
- All errors logged but don't crash

**Integration**:
- Used by: All three bot versions
- Called for: Each stock (if has_data=True)
- Skipped for: Stocks with NA values
- Cache: No caching (fresh data each run)

---

#### `news_aggregator.py`
**Purpose**: Fetch news from 70+ sources
**Original Name**: `comprehensive_news_sources.py`
**Lines**: ~800 lines (extensive)

**Key Functions**:
```python
def fetch_comprehensive_news(ticker)
    # Main function - fetches from all sources
    # Returns: (news_text, news_titles)

def fetch_yahoo_news(ticker)
    # Yahoo Finance news API
    # Returns: List of news items

def fetch_google_news(ticker, company_name)
    # Google News search
    # Returns: List of news items

def fetch_economic_times(ticker, company_name)
    # Economic Times articles
    # Returns: List of news items

def fetch_moneycontrol(ticker, company_name)
    # Moneycontrol news
    # Returns: List of news items

# ... 70+ source functions
```

**News Sources** (70+):

**Indian Financial News**:
- Economic Times, Business Standard, Business Today
- Moneycontrol, Livemint, Financial Express
- Hindu Business Line, Zee Business

**Stock Exchange Announcements**:
- BSE Official Announcements
- NSE Official Announcements

**Global Financial News**:
- Reuters, Bloomberg, CNBC
- Wall Street Journal, Financial Times
- MarketWatch, Seeking Alpha

**Company-Specific**:
- Company press releases
- Investor relations announcements
- Quarterly earnings reports

**How It Works**:
1. Accepts ticker symbol (e.g., "RELIANCE.NS")
2. Extracts company name from ticker
3. Fetches news from all available sources concurrently
4. Deduplicates news items
5. Sorts by relevance and date
6. Returns consolidated text + titles

**Usage**:
```python
from src.core.news_aggregator import fetch_comprehensive_news

news_text, news_titles = fetch_comprehensive_news("RELIANCE.NS")
print(f"News: {news_text[:200]}")
print(f"Titles: {news_titles[:3]}")
```

**Testing**:
```bash
python -c "from src.core.news_aggregator import fetch_comprehensive_news; text, titles = fetch_comprehensive_news('TCS.NS'); print(f'Found {len(titles)} news items')"
```

**Performance**:
- Time: ~3-5 seconds per stock
- Concurrent fetching: Uses threading
- Timeout: 5 seconds per source
- Fallback: Returns available news if some sources fail

**Integration**:
- Used by: market_bot_ai.py (primary), market_bot_lite.py (optional)
- Imported as: `fetch_comprehensive_news`
- Falls back to: Yahoo + Google news if module not available

---

### 2.3 Data Files (`data/`)

#### `nse_stocks_650.py`
**Purpose**: Comprehensive list of 675 NSE stocks with market cap classification
**Lines**: ~1,200 lines

**Key Functions**:
```python
def get_all_stocks_with_classification()
    # Returns: List of (ticker, cap_size) tuples
    # Example: [("RELIANCE.NS", "Large Cap"), ...]

def get_validated_stocks()
    # Returns: Validated list (removes delisted/invalid)
    # Used by: All bots for stock iteration
```

**Data Structure**:
```python
NIFTY_150 = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", ...
]  # 150 stocks

MIDCAP_200 = [
    "PERSISTENT.NS", "ZOMATO.NS", ...
]  # 200 stocks

SMALLCAP_325 = [
    "ZEEL.NS", "BIOCON.NS", ...
]  # 325 stocks

Total: 675 stocks
```

**Market Cap Classification**:
- **Large Cap**: Nifty 150 stocks (150 stocks)
- **Mid Cap**: Midcap 200 stocks (200 stocks)
- **Small Cap**: Smallcap 300 + extras (325 stocks)

**How It Works**:
1. Stocks are hard-coded lists (updated quarterly)
2. Each stock has `.NS` suffix for NSE
3. Classification based on NSE indices
4. Validation removes delisted stocks

**Testing**:
```python
from data.nse_stocks_650 import get_all_stocks_with_classification

stocks = get_all_stocks_with_classification()
print(f"Total stocks: {len(stocks)}")
# Output: Total stocks: 675
```

**Maintenance**:
- Update quarterly (NSE index changes)
- Remove delisted stocks
- Add newly listed stocks
- Verify market cap classification

**Integration**:
- Used by: All bots, all scripts
- Critical dependency: Project fails without this
- Import path: `from data.nse_stocks_650 import ...`

---

### 2.4 Utility Scripts (`scripts/`)

#### Setup Scripts (`scripts/setup/`)

##### `add_analyst_columns.py`
**Purpose**: One-time script to add Consensus and Ratings columns to Notion database
**Lines**: ~262 lines

**Functions**:
```python
def add_analyst_columns_to_database()
    # Adds "Consensus" (select) column
    # Adds "Ratings" (rich text) column

def populate_analyst_ratings()
    # Populates ratings for all existing stocks
    # Uses analyst_ratings.py module
```

**Usage**:
```bash
python scripts/setup/add_analyst_columns.py
# Expected: Creates 2 new columns, populates ~675 rows
```

**When to Use**:
- First-time setup
- After database reset
- If columns were accidentally deleted

---

##### `fresh_start.py`
**Purpose**: Complete database reset and reload
**Lines**: ~296 lines

**Functions**:
```python
def clear_all_pages()
    # Archives all existing pages in database

def verify_schema()
    # Checks all 16 columns exist
    # Creates missing columns if needed

def load_all_stocks()
    # Loads all 675 stocks fresh
    # Uses market_bot_lite logic
```

**Usage**:
```bash
python scripts/setup/fresh_start.py
# WARNING: Deletes all data!
# Expected: ~30-45 minutes for 675 stocks
```

**When to Use**:
- Initial setup
- Database corruption
- Schema changes
- Testing new features

**Logs**: `logs/fresh_start.log`

---

##### `setup_models.py`
**Purpose**: Download and cache AI models (FinBERT)
**Lines**: ~150 lines

**Usage**:
```bash
python scripts/setup/setup_models.py
# Downloads FinBERT model (~500MB)
```

**When to Use**:
- Before first run of market_bot_ai.py
- After model cache cleared
- To pre-download model

---

#### Maintenance Scripts (`scripts/maintenance/`)

##### `load_missing_stocks.py`
**Purpose**: Intelligently loads only stocks not yet in database
**Lines**: ~266 lines

**Functions**:
```python
def get_existing_tickers()
    # Queries Notion for existing stocks
    # Returns: Set of ticker symbols

def load_missing_stocks()
    # Loads only stocks not in set
    # Uses same logic as main bots
```

**Usage**:
```bash
python scripts/maintenance/load_missing_stocks.py
# Checks database, loads only missing stocks
```

**When to Use**:
- After adding new stocks to nse_stocks_650.py
- If some stocks failed to load
- Incremental updates

---

##### `update_prices.py`
**Purpose**: Update prices and scores for all existing stocks
**Lines**: ~300 lines
**Original Name**: `update-all-stocks-price-score.py`

**Usage**:
```bash
python scripts/maintenance/update_prices.py
# Updates all 675 stocks (faster than full reload)
```

**When to Use**:
- Daily price updates
- After market close
- Quick refresh without full reload

---

##### `check_database.py`
**Purpose**: Database health check and statistics
**Lines**: ~200 lines
**Original Name**: `check-database-status.py`

**Functions**:
```python
def check_schema()
    # Verifies all 16 columns exist

def check_stock_count()
    # Counts total stocks in database

def check_data_quality()
    # Identifies stocks with missing data
```

**Usage**:
```bash
python scripts/maintenance/check_database.py
# Prints database statistics
```

**Output Example**:
```
✅ Database Health Check
- Total Stocks: 675
- With Prices: 658 (97.5%)
- With News: 620 (91.9%)
- With Ratings: 580 (85.9%)
- Schema: ✅ All 16 columns present
```

---

#### Analysis Scripts (`scripts/analysis/`)

##### `top_recommendations.py`
**Purpose**: Generate top stock recommendations based on score
**Lines**: ~250 lines
**Original Name**: `top-25-recommendations.py`

**Usage**:
```bash
python scripts/analysis/top_recommendations.py
# Prints top 25 stocks by score
```

**Output**: List of top-scoring stocks with details

---

## 3. Configuration

### Environment Variables (`.env`)

```bash
# Notion API Configuration
NOTION_TOKEN=ntn_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# HuggingFace Token (for AI version)
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional: Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
LOG_DIR=logs
```

### `.env.example`
Template file for environment setup. Copy to `.env` and fill in values.

### `requirements.txt`
```
# Core Dependencies
requests>=2.31.0
pandas>=2.0.0
yfinance>=0.2.28

# AI/ML (for market_bot_ai.py only)
transformers>=4.30.0
torch>=2.0.0

# Optional: Scheduling
schedule>=1.2.0
```

---

## 4. Deployment Guide

### 4.1 Initial Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd market-bot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 5. Setup database (first time only)
python scripts/setup/fresh_start.py

# 6. (Optional) Pre-download AI model
python scripts/setup/setup_models.py
```

### 4.2 Production Deployment

**Linux/Unix (cron)**:
```bash
# Edit crontab
crontab -e

# Add daily run at 6 AM
0 6 * * * cd /path/to/market-bot && ./venv/bin/python src/bots/market_bot_lite.py >> logs/cron.log 2>&1

# Add weekly run (Sunday 8 PM)
0 20 * * 0 cd /path/to/market-bot && ./venv/bin/python src/bots/market_bot_ai.py >> logs/cron.log 2>&1

# Add monthly run (1st of month, 6 AM)
0 6 1 * * cd /path/to/market-bot && ./venv/bin/python src/bots/market_bot_pro.py >> logs/cron.log 2>&1
```

**Windows (Task Scheduler)**:
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 6 AM
4. Action: Start a program
   - Program: `C:\path\to\market-bot\venv\Scripts\python.exe`
   - Arguments: `src\bots\market_bot_lite.py`
   - Start in: `C:\path\to\market-bot`

**Docker Deployment**:
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/bots/market_bot_lite.py"]
```

```bash
# Build and run
docker build -t market-bot .
docker run --env-file .env market-bot
```

**Cloud Deployment (AWS Lambda)**:
1. Package code + dependencies
2. Set environment variables
3. Schedule with EventBridge
4. Increase timeout to 15 minutes
5. Allocate 2GB memory

---

## 5. Testing Guide

### 5.1 Unit Testing

Create test files in `tests/` directory:

```python
# tests/test_analyst_ratings.py
import unittest
from src.core.analyst_ratings import aggregate_all_analyst_ratings

class TestAnalystRatings(unittest.TestCase):
    def test_valid_stock(self):
        result = aggregate_all_analyst_ratings("RELIANCE.NS")
        self.assertIsInstance(result, dict)
        self.assertIn('rating_numeric', result)

    def test_invalid_stock(self):
        result = aggregate_all_analyst_ratings("INVALID.NS")
        self.assertEqual(result['has_data'], False)

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m unittest discover tests/
```

### 5.2 Integration Testing

```bash
# Test import system
python -c "from src.bots.market_bot_lite import *; print('✅ Lite imports work')"
python -c "from src.core.analyst_ratings import *; print('✅ Analyst ratings imports work')"
python -c "from data.nse_stocks_650 import *; print('✅ Data imports work')"

# Test single stock
python -c "from src.bots.market_bot_lite import get_market_intelligence; print(get_market_intelligence('RELIANCE.NS', 'Large Cap'))"
```

### 5.3 Load Testing

```bash
# Test with 10 stocks
# Modify main() to use stocks[:10] for testing
python src/bots/market_bot_lite.py
```

---

## 6. Troubleshooting Guide

### 6.1 Common Issues

#### Import Errors
**Error**: `ModuleNotFoundError: No module named 'src'`
**Solution**: Run from project root directory
```bash
cd /path/to/market-bot
python src/bots/market_bot_lite.py
```

**Error**: `ImportError: cannot import name 'get_all_stocks_with_classification'`
**Solution**: Check `data/nse_stocks_650.py` exists

#### Notion API Errors
**Error**: `401 Unauthorized`
**Solution**: Check NOTION_TOKEN in .env

**Error**: `404 Not Found`
**Solution**: Verify DATABASE_ID, check database is shared with integration

**Error**: `400 Bad Request - validation_error`
**Solution**: Column names mismatch. Check database schema.

#### yfinance Errors
**Error**: `No data found, symbol may be delisted`
**Solution**: Normal for delisted stocks. NA handling will work.

**Error**: `Connection timeout`
**Solution**: Check internet connection, retry

#### AI Model Errors
**Error**: `OSError: Can't load tokenizer`
**Solution**: Check HF_TOKEN, internet connection

**Error**: `RuntimeError: CUDA out of memory`
**Solution**: Use CPU or reduce batch size

### 6.2 Debugging

**Enable Debug Logging**:
```python
# Add to bot file
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Check Logs**:
```bash
# View recent logs
tail -n 100 logs/market_bot_pro.log

# Search for errors
grep "ERROR" logs/*.log

# Monitor in real-time
tail -f logs/market_bot_pro.log
```

**Test Individual Functions**:
```python
# Python REPL
python
>>> from src.core.analyst_ratings import aggregate_all_analyst_ratings
>>> ratings = aggregate_all_analyst_ratings("RELIANCE.NS")
>>> print(ratings)
```

---

## 7. Monitoring & Maintenance

### 7.1 Monitoring

**Log Analysis**:
```bash
# Count errors
grep -c "ERROR" logs/*.log

# Success rate
grep "✅" logs/market_bot_pro.log | wc -l

# Failed stocks
grep "⚠️" logs/market_bot_pro.log
```

**Database Monitoring**:
```bash
# Run health check
python scripts/maintenance/check_database.py

# Check last update times
# Query Notion database for "Last Updated" column
```

**Performance Monitoring**:
- Track execution time
- Monitor memory usage
- Check API rate limits
- Monitor log file sizes

### 7.2 Maintenance Tasks

**Daily**:
- ✅ Run market_bot_lite.py
- ✅ Check logs for errors
- ✅ Verify data updated

**Weekly**:
- ✅ Run market_bot_ai.py
- ✅ Review error logs
- ✅ Check disk space (logs)

**Monthly**:
- ✅ Run market_bot_pro.py
- ✅ Update nse_stocks_650.py (if needed)
- ✅ Rotate logs
- ✅ Review database performance

**Quarterly**:
- ✅ Update stock list (NSE index changes)
- ✅ Update dependencies
- ✅ Review and optimize code
- ✅ Backup Notion database

---

## 8. Scaling & Optimization

### 8.1 Performance Optimization

**Parallel Processing**:
```python
from concurrent.futures import ThreadPoolExecutor

def process_stock_batch(stocks):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(lambda s: get_market_intelligence(*s), stocks)
    return list(results)
```

**Caching**:
```python
import functools
import time

@functools.lru_cache(maxsize=1000)
def cached_analyst_ratings(ticker):
    return aggregate_all_analyst_ratings(ticker)
```

**Database Optimization**:
- Batch updates (update 50 stocks at once)
- Use Notion's bulk API endpoints
- Cache Notion queries

### 8.2 Scaling to More Stocks

**Support 1000+ Stocks**:
1. Update `data/nse_stocks_650.py` with new stocks
2. Increase API rate limits
3. Add batch processing
4. Consider database sharding

**Support Multiple Markets**:
1. Create `data/bse_stocks.py`, `data/us_stocks.py`
2. Modify ticker format handling
3. Add market-specific news sources

---

## 9. Integration Guide

### 9.1 REST API Integration

**Create API wrapper**:
```python
# src/api/app.py
from flask import Flask, jsonify
from src.bots.market_bot_lite import get_market_intelligence

app = Flask(__name__)

@app.route('/api/stock/<ticker>')
def get_stock(ticker):
    data = get_market_intelligence(ticker + ".NS", "Large Cap")
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000)
```

### 9.2 Webhook Integration

**Notify on signals**:
```python
import requests

def send_webhook(stock_data):
    if stock_data['signal'] == "🚀 Strong Buy":
        requests.post("https://hooks.slack.com/...",
                     json={"text": f"Strong Buy: {stock_data['ticker']}"})
```

### 9.3 Database Integration

**Export to PostgreSQL**:
```python
import psycopg2

def save_to_postgres(stock_data):
    conn = psycopg2.connect("dbname=stocks user=postgres")
    cur = conn.cursor()
    cur.execute("INSERT INTO stocks VALUES (%s, %s, %s)",
               (stock_data['ticker'], stock_data['price'], stock_data['sentiment']))
    conn.commit()
```

### 9.4 Cloud Service Integration

**AWS S3 Backup**:
```python
import boto3

s3 = boto3.client('s3')
s3.upload_file('logs/market_bot_pro.log', 'my-bucket', 'logs/latest.log')
```

**Google Sheets Export**:
```python
import gspread

gc = gspread.service_account()
sh = gc.open("Stock Data")
worksheet = sh.sheet1
worksheet.update([list(stock_data.values())])
```

---

## 10. Advanced Topics

### 10.1 Custom News Sources

Add your own news source:
```python
# In src/core/news_aggregator.py

def fetch_custom_source(ticker, company_name):
    url = f"https://mycustomnews.com/api/{ticker}"
    response = requests.get(url)
    return response.json()['articles']

# Add to fetch_comprehensive_news()
news_items.extend(fetch_custom_source(ticker, company_name))
```

### 10.2 Custom Sentiment Models

Replace FinBERT with custom model:
```python
# In src/bots/market_bot_ai.py

from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "your-custom-model"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
```

### 10.3 Multi-Language Support

Add Hindi news support:
```python
def fetch_hindi_news(ticker, company_name):
    # Fetch from Hindi news sources
    # Translate to English for sentiment analysis
    pass
```

---

## 11. Security Best Practices

1. **Never commit `.env` file** (in .gitignore)
2. **Rotate API tokens** regularly
3. **Use environment variables** for all secrets
4. **Limit API permissions** (Notion: only database access)
5. **Sanitize inputs** (SQL injection prevention)
6. **Use HTTPS** for all API calls
7. **Implement rate limiting** to avoid bans
8. **Log security events** (failed auth, etc.)

---

## 12. Conclusion

This documentation covers all aspects of the Market Bot system. For additional help:

1. Check `docs/QUICK_START.md` for getting started
2. Review `docs/DATABASE_SCHEMA.md` for column details
3. See `docs/COMPREHENSIVE_FINAL_REPORT.md` for project overview
4. Open GitHub issues for bugs/features

**System is production-ready and fully documented!**

---

**Last Updated**: May 19, 2026
**Version**: 1.0.0
**Status**: ✅ Production Ready
