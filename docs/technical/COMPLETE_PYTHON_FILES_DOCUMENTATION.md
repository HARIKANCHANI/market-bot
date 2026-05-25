# 📚 Complete Python Files Documentation
# Market Bot - Indian Stock Market Intelligence Suite

**Last Updated**: 2026-05-24
**Total Python Files**: 25+
**Status**: ✅ Production Ready
**Total Lines**: 1,579

---

## 🎯 Quick Start Guide

**New User?** Start here:
1. Read Section 1.3 (`market_bot_lite.py`) - Fastest bot to get started
2. Read Section 3.1 (`env_config.py`) - Setup your credentials
3. Follow "Workflow 1: Fresh Installation" in Appendix A
4. Run your first bot!

**Looking for specific functionality?**
- Update prices only → Section 6.2 (`update_prices.py`)
- Generate reports → Section 7 (Analysis Scripts)
- Troubleshooting → Appendix B
- Performance metrics → Appendix C

---

## 📖 Table of Contents

### Core Files
1. [Core Bot Files](#1-core-bot-files) - Main market analysis bots
   - 1.1 market_bot_ai.py - AI-powered analysis (4-5 hours)
   - 1.2 market_bot_pro.py - Professional analysis (30-35 min)
   - 1.3 market_bot_lite.py - Quick updates (18-20 min)

2. [Core Module Files](#2-core-module-files) - Shared functionality
   - 2.1 analyst_ratings.py - Analyst data aggregation
   - 2.2 news_aggregator.py - 70+ news sources
   - 2.3 ranking_engine.py - Intelligent ranking (9 metrics)

3. [Configuration Files](#3-configuration-files) - Environment setup
   - 3.1 env_config.py - Credential management

4. [Data Files](#4-data-files) - Stock universe
   - 4.1 nse_stocks_650.py - 675 NSE stocks

### Scripts
5. [Setup Scripts](#5-setup-scripts) - Initial configuration
   - 5.1 fresh_start.py - Database reset
   - 5.2 add_analyst_columns.py - Add analyst data
   - 5.3 setup_models.py - Download AI models

6. [Maintenance Scripts](#6-maintenance-scripts) - Daily operations
   - 6.1 check_database.py - Health checks
   - 6.2 update_prices.py - Price updates only
   - 6.3 load_missing_stocks.py - Add new stocks

7. [Analysis Scripts](#7-analysis-scripts) - Generate insights
   - 7.1 top_recommendations.py - Top 25 picks
   - 7.2 analyze_institutional_top.py - FII/DII analysis
   - 7.3 inspect_ranking_samples.py - Debug rankings

8. [Utility Scripts](#8-utility-scripts) - Helper tools
   - 8.1 delete_notion_entries.py - Clean database
   - 8.2 check_total_stocks.py - Count stocks
   - 8.3 create_stock_excel.py - Export to Excel
   - 8.4 create_ranking_flowcharts.py - Generate charts
   - 8.5 convert_to_word.py - Markdown to Word
   - 8.6 check_dependencies.py - Verify dependencies
   - 8.7 check_links.py - Validate documentation

9. [Test Files](#9-test-files) - Quality assurance
   - 9.1 test_ranking_engine.py - Unit tests
   - 9.2 test_excel_bot.py - Excel export tests

10. [Helper Scripts](#10-helper-scripts) - Development aids
    - 10.1 run_large_caps_lite.py - Test subset
    - 10.2 debug_holdings.py - Debug holdings

### Appendices
- [Appendix A](#appendix-a-common-workflows) - Common Workflows
- [Appendix B](#appendix-b-troubleshooting-guide) - Troubleshooting
- [Appendix C](#appendix-c-performance-benchmarks) - Performance
- [Appendix D](#appendix-d-scaling-recommendations) - Scaling
- [Appendix E](#appendix-e-monitoring--alerting) - Monitoring
- [Appendix F](#appendix-f-security-best-practices) - Security

---

## 📊 File Statistics

| Category | Files | Total Lines | Primary Use |
|----------|-------|-------------|-------------|
| Core Bots | 3 | ~2,650 | Market analysis |
| Core Modules | 3 | ~1,340 | Shared functionality |
| Setup Scripts | 3 | ~450 | Initial setup |
| Maintenance | 3 | ~480 | Daily operations |
| Analysis | 3 | ~350 | Insights & reports |
| Utilities | 7 | ~980 | Helper tools |
| Tests | 2 | ~200 | Quality assurance |
| **Total** | **25+** | **~6,500** | Complete suite |

---

# 1. CORE BOT FILES

## 1.1. market_bot_ai.py

**Location**: `src/bots/market_bot_ai.py`  
**Lines**: 778  
**Purpose**: AI-powered sentiment analysis bot with comprehensive news aggregation

### Functionality
- Analyzes 675 NSE stocks (Nifty 150, Midcap 200, Smallcap 300)
- AI sentiment analysis using FinBERT model
- Fetches news from 70+ sources
- Aggregates analyst ratings from 50+ analysts
- Intelligent multi-factor ranking
- Updates Notion database with 16 columns

### Key Functions
```python
analyze_ai_sentiment(news_titles)
  # AI-powered sentiment analysis using FinBERT
  # Input: List of news titles
  # Output: Sentiment score (-1 to +1)

get_market_intelligence(symbol, cap_size)
  # Fetch comprehensive market data with AI sentiment
  # Input: Stock symbol (e.g., "RELIANCE.NS"), cap size
  # Output: Dict with price, momentum, volume, sentiment, news

send_to_notion(data, rank=None)
  # Upload stock data to Notion database
  # Input: Stock data dict, optional rank
  # Output: Boolean (success/failure)
```

### How to Use
```bash
# Set environment variables in .env
NOTION_TOKEN=your_token
DATABASE_ID=your_database_id
HF_TOKEN=your_huggingface_token

# Run the bot
python src/bots/market_bot_ai.py
```

### Expected Runtime
- **First Run**: 4-5 hours (downloads FinBERT model ~500MB)
- **Subsequent Runs**: 3-4 hours (675 stocks × ~15-20 seconds each)

### Output
- Updates all 675 stocks in Notion database
- Columns populated: All 16 columns including AI sentiment
- Log file: `logs/market_bot_ai.log`
- Console: Real-time progress with ✅/❌ indicators

### Testing
```bash
# Test imports
python -c "from src.bots.market_bot_ai import *; print('✅ Imports OK')"

# Test single stock
python -c "from src.bots.market_bot_ai import get_market_intelligence; \
  data = get_market_intelligence('RELIANCE.NS', 'Large Cap'); print(data)"

# Dry run (test without uploading)
# Comment out the send_to_notion() call in main()
```

### Troubleshooting
**Issue**: HuggingFace token error  
**Solution**: Set `HF_TOKEN` in `.env` file

**Issue**: Out of memory during model load  
**Solution**: Close other applications, minimum 8GB RAM required

**Issue**: News fetching fails  
**Solution**: Check internet connection, some sources may be temporarily down

### Monitoring
- Monitor log file: `tail -f logs/market_bot_ai.log`
- Check success rate: Count ✅ vs ❌ in logs
- Track memory usage: Should stay under 4GB

### Scaling
- **Parallel Processing**: Not recommended (rate limits, memory)
- **Batch Processing**: Process in chunks of 100 stocks
- **Cloud Deployment**: Use AWS Lambda with 3GB+ memory

### Dependencies
- transformers>=4.30.0
- torch>=2.0.0
- yfinance>=0.2.28
- requests>=2.31.0

---

## 1.2. market_bot_pro.py

**Location**: `src/bots/market_bot_pro.py`  
**Lines**: 980  
**Purpose**: Production-grade bot with configurable news sources and keyword-based sentiment

### Functionality
- Professional-grade market analysis
- Configurable news coverage (2 sources or 70+ sources)
- Keyword-based sentiment analysis (fast, no AI model needed)
- Analyst ratings aggregation
- Intelligent multi-factor ranking
- Robust error handling and logging

### Key Functions
```python
get_market_data(symbol, cap_size)
  # Fetch market data with yfinance + NSE fallback
  # Input: Stock symbol, cap size
  # Output: Dict with price, momentum, volume data

get_news_and_sentiment(symbol)
  # Fetch news with configurable sources
  # Input: Stock symbol
  # Output: Tuple (news_text, news_sentiment, news_types)

calculate_score(momentum, volume_surge, signal)
  # Calculate composite investment score
  # Input: Technical indicators
  # Output: Numeric score (0-1500+)
```

### Configuration
```python
# In the file, line ~40
USE_COMPREHENSIVE_NEWS = True   # 70+ sources (30-35 min)
USE_COMPREHENSIVE_NEWS = False  # 2 sources (18-20 min)
```

### How to Use
```bash
# Configure news sources (edit file or use default)
# Run the bot
python src/bots/market_bot_pro.py
```

### Expected Runtime
- **Comprehensive News (True)**: 30-35 minutes
- **Basic News (False)**: 18-20 minutes

### Output
- Updates all 675 stocks in Notion
- Columns: All 16 columns with keyword sentiment
- Log: `logs/market_bot_pro.log`
- Summary statistics at end

### Testing
```bash
# Test market data fetching
python -c "from src.bots.market_bot_pro import get_market_data; \
  data = get_market_data('TCS.NS', 'Large Cap'); print(data)"

# Test with small subset (edit main() to use [:5])
```

### Troubleshooting
**Issue**: yfinance returns None  
**Solution**: Automatic NSE fallback activates

**Issue**: News fetching timeout  
**Solution**: Increase timeout or use basic news mode

### Monitoring
- Success rate: Should be >98%
- Average time per stock: 2-3 seconds
- Memory usage: ~500MB

### Scaling
- Suitable for production use
- Can run hourly/daily via cron
- Handles API rate limits automatically

---

## 1.3. market_bot_lite.py

**Location**: `src/bots/market_bot_lite.py`  
**Lines**: 901  
**Purpose**: Fast, lightweight bot for quick daily updates (technical analysis only)

### Functionality
- Quick technical analysis (no AI model required)
- Optional news fetching (configurable)
- Automatic yfinance/NSE fallback
- Intelligent ranking
- Fast execution (18-20 minutes)

### Key Functions
```python
get_market_intelligence(symbol, cap_size)
  # Fast market data with optional news
  # Input: Stock symbol, cap size
  # Output: Complete stock data dict

simple_sentiment_analysis(news_text)
  # Keyword-based sentiment (fast)
  # Input: News text
  # Output: Sentiment score (0-1)

send_to_notion(data, rank=None)
  # Upload to Notion database
  # Input: Stock data, rank
  # Output: Boolean success
```

### How to Use
```bash
# Daily quick update
python src/bots/market_bot_lite.py
```

### Expected Runtime
- **18-20 minutes** for 675 stocks
- ~1.5-2 seconds per stock

### Output
- Updates: 14 of 16 columns (excludes AI sentiment)
- Fast updates for price, momentum, volume
- Log: `logs/market_bot_lite.log`

### Testing
```bash
# Quick test
python -c "from src.bots.market_bot_lite import get_market_intelligence; \
  print(get_market_intelligence('INFY.NS', 'Large Cap'))"
```

### Use Cases
- Daily morning updates before market opens
- Hourly price updates
- Quick portfolio refreshes
- Development/testing

### Monitoring
- Should complete in <25 minutes
- Success rate: >99%
- Memory: <300MB

---

# 2. CORE MODULE FILES

## 2.1. analyst_ratings.py

**Location**: `src/core/analyst_ratings.py`
**Lines**: 429
**Purpose**: Aggregate analyst ratings from 50+ global and Indian analysts

### Functionality
- Fetches ratings from yfinance
- Aggregates global analyst consensus
- Converts ratings to 1-5 scale
- Returns consensus (Strong Buy, Buy, Hold, Sell, Strong Sell)
- Calculates average rating

### Key Functions
```python
aggregate_all_analyst_ratings(ticker)
  # Get complete analyst ratings for a stock
  # Input: Stock symbol (e.g., "RELIANCE.NS")
  # Output: Dict with consensus and average rating
  #   {
  #     "consensus": "Strong Buy",
  #     "avg_rating": 4.75,
  #     "num_ratings": 25
  #   }

convert_rating_to_numeric(rating_text)
  # Convert text rating to 1-5 scale
  # Input: "Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"
  # Output: Float (1.0 to 5.0)
```

### How to Use
```python
from src.core.analyst_ratings import aggregate_all_analyst_ratings

# Get ratings for a stock
ratings = aggregate_all_analyst_ratings("TCS.NS")
print(f"Consensus: {ratings['consensus']}")
print(f"Average Rating: {ratings['avg_rating']}/5.0")
print(f"Number of Analysts: {ratings['num_ratings']}")
```

### Testing
```bash
# Test function directly
python -c "from src.core.analyst_ratings import aggregate_all_analyst_ratings; \
  print(aggregate_all_analyst_ratings('RELIANCE.NS'))"
```

### Output
Returns dictionary:
- `consensus`: "Strong Buy" | "Buy" | "Hold" | "Sell" | "Strong Sell" | "N/A"
- `avg_rating`: Float (1.0-5.0)
- `num_ratings`: Integer (number of analysts)

### Troubleshooting
**Issue**: Returns "N/A" for all stocks
**Solution**: Check internet connection, yfinance may be down

**Issue**: Inconsistent ratings
**Solution**: Normal - analyst opinions vary, use consensus

### Performance
- Average time per stock: 0.5-1 second
- Caches data within session
- Respects API rate limits

---

## 2.2. news_aggregator.py

**Location**: `src/core/news_aggregator.py`
**Lines**: 679
**Purpose**: Comprehensive news aggregation from 70+ financial sources

### Functionality
- Fetches news from 70+ sources including:
  - NSE/BSE official announcements
  - Company websites
  - Major financial publications (ET, MC, BS, FE, Mint, etc.)
  - News aggregators (Google News, Bing, Yahoo)
  - Financial platforms (TradeB rains, Simply Wall St, etc.)
  - Rating agencies (CRISIL, ICRA, CARE, Moody's, S&P)
  - Brokerages (Motilal, IIFL, Kotak, HDFC, ICICI, etc.)
- Deduplicates news items
- Returns consolidated text and titles
- Concurrent fetching for speed

### Key Functions
```python
fetch_comprehensive_news(ticker)
  # Fetch news from all 70+ sources
  # Input: Stock symbol (e.g., "RELIANCE.NS")
  # Output: Tuple (news_text, news_titles_list)
  #   news_text: Consolidated news text (up to 3000 chars)
  #   news_titles: List of news headlines

fetch_from_company_website(ticker, company_url)
  # Fetch news from official company website
  # Input: Ticker, company URL
  # Output: List of news items

fetch_nse_bse_announcements(ticker)
  # Get official NSE/BSE announcements
  # Input: Ticker
  # Output: List of announcements
```

### How to Use
```python
from src.core.news_aggregator import fetch_comprehensive_news

# Get news for a stock
news_text, news_titles = fetch_comprehensive_news("TCS.NS")
print(f"Found {len(news_titles)} news items")
print(f"News preview: {news_text[:200]}")
```

### Testing
```bash
# Test news fetching
python -c "from src.core.news_aggregator import fetch_comprehensive_news; \
  text, titles = fetch_comprehensive_news('INFY.NS'); \
  print(f'Found {len(titles)} news items')"
```

### Expected Output
- news_text: String of consolidated news (max 3000 chars)
- news_titles: List of 10-50 headlines (deduplicated)
- Typical runtime: 3-5 seconds per stock

### Troubleshooting
**Issue**: Few or no news items
**Solution**: Normal for small-cap stocks, focus on large caps

**Issue**: Timeout errors
**Solution**: Some sources may be slow, built-in fallback

**Issue**: Duplicate news
**Solution**: Deduplication logic included, slight variations normal

### Performance Optimization
- Uses concurrent fetching (all sources in parallel)
- Timeout: 5 seconds per source
- Total time: ~5 seconds (not 70×5 seconds)
- Efficient regex-based parsing

### Monitoring
- Track success rate by source
- Monitor fetch times
- Log failed sources

---

## 2.3. ranking_engine.py

**Location**: `src/core/ranking_engine.py`
**Lines**: 230
**Purpose**: Intelligent multi-factor ranking system (9 metrics)

### Functionality
- Ranks stocks from 1 (best) to 650+ (worst)
- Uses 9 weighted metrics:
  - Momentum (20%)
  - Volume Surge (15%)
  - Sentiment (15%)
  - Investment Score (15%)
  - Market Cap (10%)
  - Signal (10%)
  - News Sentiment (8%)
  - Analyst Consensus (5%)
  - Analyst Ratings (2%)
- Handles missing data gracefully
- Optimized for performance

### Key Functions
```python
rank_stocks(stocks_data)
  # Rank all stocks by composite score
  # Input: List of stock data dicts
  # Output: Same list with 'rank' field added (1=best)

normalize_metric(value, min_val, max_val)
  # Normalize metric to 0-1 scale
  # Input: Value and range
  # Output: Normalized float (0-1)

calculate_composite_score(stock_data)
  # Calculate weighted composite score
  # Input: Stock data dict
  # Output: Float score (0-100)
```

### How to Use
```python
from src.core.ranking_engine import rank_stocks

# Prepare stock data
stocks = [
    {"ticker": "TCS.NS", "momentum": 0.15, "volume_surge": 1.5, ...},
    {"ticker": "INFY.NS", "momentum": 0.08, "volume_surge": 1.2, ...},
]

# Rank stocks
ranked_stocks = rank_stocks(stocks)

# Access ranks
for stock in ranked_stocks:
    print(f"{stock['ticker']}: Rank {stock['rank']}")
```

### Testing
```bash
# Run unit tests
python tests/test_ranking_engine.py

# Expected output: All tests passing
```

### Output
- Adds 'rank' field to each stock (1 = best opportunity)
- Maintains original order if requested
- Returns sorted list by rank

### Performance
- **Optimized**: Ranks 675 stocks in ~0.1 seconds (650x improvement)
- Memory efficient: O(n) complexity
- Handles edge cases (missing data, NaN values)

### Customization
```python
# Edit weights in ranking_engine.py
WEIGHTS = {
    'momentum': 0.20,      # Adjust these
    'volume_surge': 0.15,  # to your
    'sentiment': 0.15,     # preference
    ...
}
```

---

# 3. CONFIGURATION FILES

## 3.1. env_config.py

**Location**: `src/config/env_config.py`
**Lines**: 91
**Purpose**: Centralized environment configuration management

### Functionality
- Loads environment variables from .env file
- Validates required credentials
- Provides helper functions for Notion API
- Automatic .env file detection

### Key Functions
```python
validate_notion_config()
  # Validate NOTION_TOKEN and DATABASE_ID are set
  # Output: True or raises ValueError

validate_hf_config()
  # Validate HF_TOKEN is set (for AI bot)
  # Output: True or raises ValueError

get_notion_headers()
  # Get authenticated Notion API headers
  # Output: Dict with Authorization header
```

### Environment Variables
```bash
# Required for all bots
NOTION_TOKEN=your_token_here
DATABASE_ID=your_database_id_here

# Required for AI bot only
HF_TOKEN=your_huggingface_token_here

# Optional
NOTION_API_VERSION=2022-06-28
LOG_LEVEL=INFO
LOG_DIR=logs
```

### How to Use
```python
from src.config.env_config import (
    NOTION_TOKEN,
    DATABASE_ID,
    validate_notion_config,
    get_notion_headers
)

# Validate before use
validate_notion_config()

# Get headers
headers = get_notion_headers()
```

### Testing
```bash
# Test configuration loading
python -c "from src.config.env_config import NOTION_TOKEN, DATABASE_ID; \
  print('✅ Config loaded' if NOTION_TOKEN and DATABASE_ID else '❌ Missing')"
```

---

# 4. DATA FILES

## 4.1. nse_stocks_650.py

**Location**: `data/nse_stocks_650.py`
**Purpose**: Comprehensive NSE stock universe (675 stocks)

### Functionality
- Contains 675 NSE stocks across:
  - Nifty 150 (Large Cap)
  - Nifty Midcap 200 (Mid Cap)
  - Nifty Smallcap 300 (Small Cap)
- Includes sector classification
- Provides helper functions

### Key Functions
```python
get_all_stocks_with_classification()
  # Get all 675 stocks with cap size
  # Output: List of tuples (symbol, cap_size)
  #   [("RELIANCE.NS", "Large Cap"), ...]

get_validated_stocks()
  # Get stocks with validation
  # Output: Validated list of stocks

get_stocks_by_cap(cap_size)
  # Filter stocks by market cap
  # Input: "Large Cap" | "Mid Cap" | "Small Cap"
  # Output: List of stocks in that category
```

### Data Structure
```python
stocks = [
    ("RELIANCE.NS", "Large Cap", "Energy"),
    ("TCS.NS", "Large Cap", "IT"),
    ("INFY.NS", "Large Cap", "IT"),
    ...
]
```

### How to Use
```python
from data.nse_stocks_650 import get_all_stocks_with_classification

# Get all stocks
stocks = get_all_stocks_with_classification()
print(f"Total stocks: {len(stocks)}")

# Iterate through stocks
for symbol, cap_size in stocks:
    print(f"{symbol}: {cap_size}")
```

### Statistics
- Total: 675 stocks
- Large Cap: ~150 stocks
- Mid Cap: ~200 stocks
- Small Cap: ~325 stocks

---

# 5. SETUP SCRIPTS

## 5.1. fresh_start.py

**Location**: `scripts/setup/fresh_start.py`
**Lines**: ~200
**Purpose**: Complete database reset and preparation

### Functionality
- Deletes all existing pages in Notion database
- Verifies database schema
- Prepares clean database for fresh data
- Does NOT repopulate (use bots for that)

### How to Run
```bash
python scripts/setup/fresh_start.py
```

### Expected Runtime
- 5-15 minutes (depending on existing data)
- ~0.3 seconds per page deletion

### Output
- Deletes all existing Notion pages
- Shows progress: "Deleted 100/675..."
- Final summary with success/failure count

### Use Cases
- Fresh installation
- Corrupted database cleanup
- Monthly/quarterly full refresh
- After schema changes

### Caution
⚠️ **DESTRUCTIVE**: Deletes ALL data in Notion database. Cannot be undone.

### Testing
```bash
# Dry run not available - use test database
# Recommendation: Clone your database first
```

---

## 5.2. add_analyst_columns.py

**Location**: `scripts/setup/add_analyst_columns.py`
**Lines**: ~150
**Purpose**: Add and populate analyst rating columns

### Functionality
- Ensures Consensus and Ratings columns exist
- Fetches analyst ratings for all stocks
- Populates columns in Notion database

### How to Run
```bash
python scripts/setup/add_analyst_columns.py
```

### Expected Runtime
- 15-30 minutes (675 stocks × ~1-2 seconds)

### Output
- Updates Consensus column with Buy/Hold/Sell
- Updates Ratings column with average rating
- Log of each stock processed

### Use Cases
- Initial setup
- After adding new stocks
- Refresh analyst data

---

## 5.3. setup_models.py

**Location**: `scripts/setup/setup_models.py`
**Purpose**: Download and verify AI models for market_bot_ai.py

### Functionality
- Checks for required packages
- Downloads FinBERT model
- Verifies installation
- Tests model loading

### How to Run
```bash
python scripts/setup/setup_models.py
```

### Expected Runtime
- First run: 5-10 minutes (downloads ~500MB model)
- Subsequent runs: <1 minute (verification only)

### Output
```
✓ pandas
✓ yfinance
✓ transformers
✓ torch
✓ requests
✅ All packages installed!

Downloading FinBERT model...
✅ Model downloaded successfully!
```

### Requirements
- HuggingFace account and token
- ~1GB free disk space
- Internet connection

---

# 6. MAINTENANCE SCRIPTS

## 6.1. check_database.py

**Location**: `scripts/maintenance/check_database.py`
**Lines**: ~100
**Purpose**: Quick health check of Notion database

### Functionality
- Connects to Notion database
- Lists all properties/columns
- Counts total pages
- Shows recent updates
- Verifies connectivity

### How to Run
```bash
python scripts/maintenance/check_database.py
```

### Expected Runtime
- <5 seconds

### Output
```
======================================================================
📊 NOTION DATABASE STATUS CHECK
======================================================================

✅ Database Properties:
   • Ticker (title)
   • Rank (number)
   • Market Cap (select)
   • Price (₹) (number)
   ...

📊 Total Stocks: 675
📅 Last Updated: 2026-05-24 10:30:00
✅ Database is healthy!
```

### Use Cases
- Daily health checks
- Verify API connectivity
- Check column setup
- Monitor database size

### Troubleshooting
**Issue**: Connection timeout
**Solution**: Check NOTION_TOKEN in .env

**Issue**: Missing columns
**Solution**: Run setup scripts to add columns

---

## 6.2. update_prices.py

**Location**: `scripts/maintenance/update_prices.py`
**Lines**: ~180
**Purpose**: Quick price update for all stocks (no news)

### Functionality
- Fetches latest prices from yfinance
- Updates Price column only
- Recalculates Score based on momentum/volume
- Updates "Last Updated" timestamp
- Fast execution (no news fetching)

### How to Run
```bash
python scripts/maintenance/update_prices.py
```

### Expected Runtime
- 8-12 minutes (675 stocks)
- ~1 second per stock

### Output
- Updated Price column for all stocks
- Recalculated Score column
- Updated Last Updated timestamp
- Progress log

### Use Cases
- Intraday price updates
- Quick refresh without news
- Automated hourly updates
- Pre-market preparation

### Monitoring
```bash
# Monitor progress
tail -f logs/update_prices.log

# Check completion
grep "✅ Complete" logs/update_prices.log
```

---

## 6.3. load_missing_stocks.py

**Location**: `scripts/maintenance/load_missing_stocks.py`
**Lines**: ~200
**Purpose**: Add any missing stocks from NSE universe

### Functionality
- Compares NSE universe (675 stocks) with Notion database
- Identifies missing stocks
- Fetches data for missing stocks
- Adds them to Notion database

### How to Run
```bash
python scripts/maintenance/load_missing_stocks.py
```

### Expected Runtime
- Variable (depends on missing stocks)
- ~20 seconds per missing stock

### Output
```
======================================================================
📊 MISSING STOCKS SUMMARY
======================================================================
Total NSE universe: 675
Already in Notion: 670
Missing (to add now): 5

Adding missing stocks:
✅ [1/5] Added: NEWSTOCK.NS
✅ [2/5] Added: ANOTHER.NS
...

✅ Complete! Added 5 stocks successfully.
```

### Use Cases
- After NSE universe updates
- Quarterly rebalancing
- Add newly listed stocks
- Fix incomplete database

---

# 7. ANALYSIS SCRIPTS

## 7.1. top_recommendations.py

**Location**: `scripts/analysis/top_recommendations.py`
**Lines**: ~150
**Purpose**: Generate curated top 25 stock recommendations

### Functionality
- Fetches all stocks from Notion
- Filters by criteria:
  - Strong Buy signal
  - High momentum (>10%)
  - High volume surge (>1.5x)
  - Positive sentiment
- Sorts by composite score
- Returns top 25 recommendations

### How to Run
```bash
python scripts/analysis/top_recommendations.py
```

### Expected Runtime
- 5-10 seconds

### Output
```
======================================================================
🏆 TOP 25 STOCK RECOMMENDATIONS
======================================================================

Rank 1: RELIANCE.NS
   • Signal: 🚀 Strong Buy
   • Price: ₹2,450.50
   • Momentum: +15.3%
   • Volume Surge: 2.1x
   • Score: 1,450
   • Sentiment: Positive

Rank 2: TCS.NS
   ...

======================================================================
📊 SUMMARY
======================================================================
Total Strong Buy: 25
Average Momentum: +12.5%
Average Score: 1,200
```

### Use Cases
- Daily trading ideas
- Portfolio recommendations
- Client reports
- Newsletter generation

---

## 7.2. analyze_institutional_top.py

**Location**: `scripts/analyze_institutional_top.py`
**Purpose**: Analyze top institutional holdings

### Functionality
- Analyzes FII/DII holding patterns
- Identifies stocks with increasing institutional interest
- Correlates with price momentum
- Generates insights

### How to Run
```bash
python scripts/analyze_institutional_top.py
```

---

## 7.3. inspect_ranking_samples.py

**Location**: `scripts/inspect_ranking_samples.py`
**Purpose**: Inspect and debug ranking algorithm

### Functionality
- Shows detailed ranking breakdown for sample stocks
- Displays each metric's contribution
- Helps understand ranking logic
- Useful for debugging

### How to Run
```bash
python scripts/inspect_ranking_samples.py
```

### Output
```
Analyzing ranking for RELIANCE.NS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Metric              Value    Weight  Contribution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Momentum            0.15     20%     3.0
Volume Surge        1.5      15%     2.25
Sentiment           0.8      15%     1.2
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Score:  85.5
Final Rank:   12
```

---

# 8. UTILITY SCRIPTS

## 8.1. delete_notion_entries.py

**Location**: `scripts/delete_notion_entries.py`
**Lines**: 150
**Purpose**: Safely delete all Notion database entries

### Functionality
- Fetches all pages from Notion database
- Requires explicit confirmation ("DELETE")
- Deletes entries with progress tracking
- Rate limiting to avoid API issues
- Safety checks

### How to Run
```bash
python scripts/delete_notion_entries.py

# Will prompt:
# ⚠️ WARNING: This will delete *all* 675 entries!
# Type 'DELETE' to confirm: DELETE
```

### Expected Runtime
- 5-10 minutes (675 stocks)
- ~0.3 seconds per deletion

### Output
```
🗑️ NOTION DATABASE CLEANUP
📍 Database ID: 664b007...
📊 Found 675 entries to delete

⚠️ WARNING: This will delete *all* 675 entries!
Type 'DELETE' to confirm: DELETE

🗑️ Deleting 675 entries...
✅ [1/675] Deleted: RELIANCE.NS
✅ [2/675] Deleted: TCS.NS
...

📊 DELETION SUMMARY
Total entries: 675
✅ Successfully deleted: 675
❌ Failed: 0

🎉 All entries deleted successfully!
```

### Safety Features
- Interactive confirmation required
- Cannot be run accidentally
- Progress tracking
- Error recovery

### Use Cases
- Before fresh data load
- Database cleanup
- Testing/development
- Schema migration

---

## 8.2. check_total_stocks.py

**Location**: `scripts/check_total_stocks.py`
**Lines**: ~50
**Purpose**: Quick count of stocks in Notion database

### Functionality
- Fetches all pages from Notion
- Counts total stocks
- Groups by market cap
- Shows breakdown

### How to Run
```bash
python scripts/check_total_stocks.py
```

### Output
```
📊 Total stocks in database: 675

Breakdown by Market Cap:
• Large Cap: 150
• Mid Cap: 200
• Small Cap: 325
```

---

## 8.3. create_stock_excel.py

**Location**: `scripts/create_stock_excel.py`
**Lines**: ~150
**Purpose**: Export Notion database to Excel file

### Functionality
- Fetches all stocks from Notion
- Extracts all columns
- Creates formatted Excel file
- Includes FII/DII data if available
- Saves to output/ folder

### How to Run
```bash
python scripts/create_stock_excel.py
```

### Output
- File: `output/stocks_analysis_YYYYMMDD_HHMMSS.xlsx`
- Contains all stocks with all columns
- Formatted and ready for analysis

### Use Cases
- Offline analysis
- Sharing with team
- Excel-based analysis
- Backup/archival

---

## 8.4. create_ranking_flowcharts.py

**Location**: `utilities/create_ranking_flowcharts.py`
**Lines**: 185
**Purpose**: Generate visual flowcharts for ranking system

### Functionality
- Creates two high-resolution flowcharts:
  1. Ranking System Flow (14" × 16", 300 DPI)
  2. Ranking Weights Distribution (12" × 10", 300 DPI)
- Professional quality graphics
- Saves to docs/ folder

### How to Run
```bash
python utilities/create_ranking_flowcharts.py
```

### Output
- `docs/Ranking_System_Flow.png`
- `docs/Ranking_Weights_Distribution.png`
- Console confirmation message

### Requirements
- matplotlib>=3.7.0
- numpy>=1.24.0

---

## 8.5. convert_to_word.py

**Location**: `utilities/convert_to_word.py`
**Lines**: 136
**Purpose**: Convert markdown documentation to Word format

### Functionality
- Converts markdown files to .docx
- Preserves formatting
- Adds styling
- Useful for sharing documentation

### How to Run
```bash
python utilities/convert_to_word.py
```

### Requirements
- python-docx>=0.8.11 (optional dependency)

### Output
- Word documents in docs/ folder
- Formatted and styled

---

## 8.6. check_dependencies.py

**Location**: `scripts/check_dependencies.py`
**Lines**: 145
**Purpose**: Verify all dependencies are installed correctly

### Functionality
- Scans all Python files
- Extracts imports
- Compares with requirements.txt
- Identifies missing dependencies
- Checks for conflicts

### How to Run
```bash
python scripts/check_dependencies.py
```

### Output
```
🔍 Scanning Python files...
Found 25 Python files

======================================================================
📦 DEPENDENCY ANALYSIS
======================================================================

✅ All dependencies present!

======================================================================
📋 CURRENT REQUIREMENTS
======================================================================
  ✓ requests>=2.31.0
  ✓ pandas>=2.0.0
  ✓ yfinance>=0.2.28
  ✓ python-dotenv>=1.0.0
  ...

======================================================================
📊 SUMMARY
======================================================================
Python files scanned: 25
Unique imports found: 35
Required packages: 9
Missing dependencies: 0
```

---

## 8.7. check_links.py

**Location**: `scripts/check_links.py`
**Lines**: 150
**Purpose**: Verify all markdown documentation links

### Functionality
- Scans all .md files
- Extracts all links
- Checks if file links exist
- Reports broken links
- Validates documentation integrity

### How to Run
```bash
python scripts/check_links.py
```

### Output
- List of all markdown files checked
- Any broken links found
- Summary statistics

---

# 9. TEST FILES

## 9.1. test_ranking_engine.py

**Location**: `tests/test_ranking_engine.py`
**Purpose**: Unit tests for ranking engine

### Functionality
- Tests all ranking functions
- Validates normalization logic
- Tests edge cases (NaN, missing data)
- Ensures consistency

### How to Run
```bash
# Run all tests
python tests/test_ranking_engine.py

# Or use pytest
pytest tests/test_ranking_engine.py -v
```

### Expected Output
```
Testing rank_stocks...
✅ Test 1: Basic ranking
✅ Test 2: Edge cases
✅ Test 3: Missing data
✅ Test 4: Normalization

All tests passed! ✅
```

### Test Coverage
- Basic functionality
- Edge cases
- Error handling
- Performance

---

## 9.2. test_excel_bot.py

**Location**: `scripts/test_excel_bot.py`
**Purpose**: Test Excel export bot functionality

### Functionality
- Tests with small dataset (5 stocks)
- Validates Excel creation
- Checks column presence
- Verifies data integrity

### How to Run
```bash
python scripts/test_excel_bot.py
```

---

# 10. HELPER SCRIPTS

## 10.1. run_large_caps_lite.py

**Location**: `scripts/run_large_caps_lite.py`
**Purpose**: Run lite bot on large caps only (for testing)

### Functionality
- Filters for large cap stocks only
- Quick testing without full run
- Validates bot functionality

### How to Run
```bash
python scripts/run_large_caps_lite.py
```

### Expected Runtime
- 3-5 minutes (150 stocks)

---

## 10.2. debug_holdings.py

**Location**: `scripts/debug_holdings.py`
**Purpose**: Debug institutional holdings data

### Functionality
- Analyzes holdings data structure
- Identifies data issues
- Helps troubleshoot holdings-related problems

### How to Run
```bash
python scripts/debug_holdings.py
```

---

# APPENDIX A: COMMON WORKFLOWS

## Workflow 1: Fresh Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup environment
cp .env.example .env
# Edit .env with your credentials

# 3. Setup AI models (if using AI bot)
python scripts/setup/setup_models.py

# 4. Prepare database
python scripts/setup/fresh_start.py

# 5. Add analyst columns
python scripts/setup/add_analyst_columns.py

# 6. Run initial data load
python src/bots/market_bot_lite.py
```

## Workflow 2: Daily Updates

```bash
# Morning quick update (18-20 min)
python src/bots/market_bot_lite.py

# Or comprehensive update (30-35 min)
python src/bots/market_bot_pro.py
```

## Workflow 3: Weekly Deep Analysis

```bash
# Weekend comprehensive AI analysis (4-5 hours)
python src/bots/market_bot_ai.py
```

## Workflow 4: Database Maintenance

```bash
# Check database health
python scripts/maintenance/check_database.py

# Load any missing stocks
python scripts/maintenance/load_missing_stocks.py

# Quick price update
python scripts/maintenance/update_prices.py
```

## Workflow 5: Analysis & Reports

```bash
# Generate top recommendations
python scripts/analysis/top_recommendations.py

# Export to Excel
python scripts/create_stock_excel.py

# Analyze institutional activity
python scripts/analyze_institutional_top.py
```

---

# APPENDIX B: TROUBLESHOOTING GUIDE

## Common Issues

### Issue: "NOTION_TOKEN not found"
**Files Affected**: All bots and scripts
**Solution**: Create `.env` file from `.env.example` and add credentials

### Issue: "ModuleNotFoundError: dotenv"
**Files Affected**: All files
**Solution**: `pip install -r requirements.txt`

### Issue: "Out of memory" (AI bot)
**Files Affected**: market_bot_ai.py
**Solution**: Close other applications, need minimum 8GB RAM

### Issue: "yfinance returns None"
**Files Affected**: All bots
**Solution**: Automatic NSE fallback activates, no action needed

### Issue: "API rate limit exceeded"
**Files Affected**: All bots
**Solution**: Built-in rate limiting, will retry automatically

### Issue: "News fetching timeout"
**Files Affected**: market_bot_pro.py, market_bot_ai.py
**Solution**: Normal for some sources, bot continues with available news

---

# APPENDIX C: PERFORMANCE BENCHMARKS

| File | Runtime | Memory | Success Rate |
|------|---------|--------|--------------|
| market_bot_ai.py | 3-4 hrs | 3-4 GB | >95% |
| market_bot_pro.py | 30-35 min | 500 MB | >98% |
| market_bot_lite.py | 18-20 min | 300 MB | >99% |
| update_prices.py | 8-12 min | 200 MB | >99% |
| ranking_engine.py | <0.1 sec | <50 MB | 100% |
| analyst_ratings.py | 1-2 sec/stock | <100 MB | >90% |
| news_aggregator.py | 3-5 sec/stock | <200 MB | >85% |

---

# APPENDIX D: SCALING RECOMMENDATIONS

## For High-Frequency Updates (Every Hour)

Use `market_bot_lite.py` or `update_prices.py`:
```bash
# Cron job (Linux/Mac)
0 * * * * cd /path/to/market-bot && python src/bots/market_bot_lite.py

# Task Scheduler (Windows)
# Run every hour during market hours
```

## For Large-Scale Deployment

1. **Use Docker**:
   ```bash
   docker build -t market-bot .
   docker run -e NOTION_TOKEN=$TOKEN market-bot python src/bots/market_bot_lite.py
   ```

2. **Cloud Functions** (AWS Lambda, Google Cloud Functions):
   - Use market_bot_lite.py (smallest memory footprint)
   - Set timeout to 900 seconds (15 minutes)
   - Allocate 512MB RAM minimum

3. **Parallel Processing**:
   - Split stocks by market cap
   - Run separate instances for each cap size
   - Aggregate results

---

# APPENDIX E: MONITORING & ALERTING

## Log Monitoring

```bash
# Watch real-time logs
tail -f logs/market_bot_pro.log

# Count successes
grep "✅" logs/market_bot_pro.log | wc -l

# Find errors
grep "❌" logs/market_bot_pro.log

# Success rate
python -c "
import re
log = open('logs/market_bot_pro.log').read()
success = len(re.findall(r'✅', log))
fail = len(re.findall(r'❌', log))
print(f'Success rate: {success/(success+fail)*100:.1f}%')
"
```

## Health Checks

```bash
# Daily health check script
python scripts/maintenance/check_database.py

# Verify stock count
python scripts/check_total_stocks.py

# Check dependencies
python scripts/check_dependencies.py
```

---

# APPENDIX F: SECURITY BEST PRACTICES

1. **Never commit .env file** (already in .gitignore)
2. **Rotate credentials** quarterly
3. **Use different credentials** for dev/staging/prod
4. **Limit API token permissions** in Notion
5. **Monitor API usage** for unusual activity
6. **Keep dependencies updated**: `pip list --outdated`

---

**END OF DOCUMENTATION**

**Document Version**: 1.0
**Last Updated**: 2026-05-24
**Total Files Documented**: 25+
**Status**: ✅ Complete and Production Ready

For questions or issues, refer to:
- README.md - Project overview
- CREDENTIALS_MIGRATION_GUIDE.md - Environment setup
- docs/TECHNICAL_DOCUMENTATION.md - Additional technical details
