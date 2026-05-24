# 📊 Market Bot - Enterprise-Grade Indian Stock Market Intelligence Suite

> Comprehensive NSE stock analysis with AI sentiment, analyst ratings, and real-time news aggregation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

- **Complete NSE Coverage**: Track ~906 active NSE stocks (Nifty 150, Midcap 200, Smallcap 300)
- **Smart Ticker Mapping** 🆕: Automatic handling of company renames and ticker changes
- **Intelligent Filtering** 🆕: Auto-filters delisted stocks and pump & dump schemes
- **Three Bot Versions**: Lite (fast), AI (accurate), Pro (robust)
- **Intelligent Ranking System** ⭐: Multi-factor ranking based on 9 metrics
- **AI Sentiment Analysis**: FinBERT-powered news sentiment (AI version)
- **70+ News Sources**: Comprehensive news aggregation from major financial outlets
- **Analyst Ratings**: Aggregate consensus from 50+ global and Indian analysts
- **Real-time Data**: Live price, momentum, volume analysis
- **Notion Integration**: Automatic database updates with 16 comprehensive columns
- **Production Ready**: Robust error handling, logging, and monitoring

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd market-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy `.env.example` to `.env` and configure:

```bash
NOTION_TOKEN=your_notion_token_here
DATABASE_ID=your_database_id_here
HF_TOKEN=your_huggingface_token_here  # Only for AI version
```

### 3. Run Your Preferred Version

```bash
# Lightweight - Fast daily updates (no AI model download)
python src/bots/market_bot_lite.py

# AI Version - Weekly analysis with FinBERT sentiment
python src/bots/market_bot_ai.py

# Professional - Monthly reports with robust logging
python src/bots/market_bot_pro.py
```

## 📁 Project Structure

```
market-bot/
├── src/
│   ├── bots/              # Main bot versions (7 bots)
│   │   ├── market_bot_lite.py
│   │   ├── market_bot_lite_incremental.py
│   │   ├── market_bot_ai.py
│   │   ├── market_bot_ai_incremental.py
│   │   ├── market_bot_pro.py
│   │   ├── market_bot_pro_incremental.py
│   │   └── market_bot_excel.py
│   ├── core/              # Core functionality
│   │   ├── analyst_ratings.py
│   │   ├── news_aggregator.py
│   │   ├── ranking_engine.py      # ⭐ Intelligent ranking
│   │   └── sentiment_analyzer.py  # 🆕 Centralized FinBERT
│   ├── utils/             # Utility functions
│   └── config/            # Configuration & logging
│       ├── env_config.py
│       └── logging_config.py      # 🆕 Centralized logging
├── utilities/             # ⭐ Utility scripts
│   ├── create_ranking_flowcharts.py
│   ├── create_flowchart.py
│   ├── create_visual_flowchart.py
│   └── convert_to_word.py
├── scripts/               # Automation scripts
│   ├── setup/            # Initial setup scripts
│   ├── maintenance/      # Database maintenance
│   └── analysis/         # Analysis tools
├── data/                  # 🆕 Stock data & mappings
│   └── nse_stocks_650.py # Master list + ticker mapping system
├── docs/                  # ⭐ UPDATED - All documentation
│   ├── Core Documentation (8 files)
│   ├── Ranking Documentation (7 files) ⭐
│   └── Visual Assets (3 PNG files)
├── logs/                  # Log files
├── tests/                 # Test files
│   └── test_ranking_engine.py     # ⭐
├── PRODUCTION_TICKER_MAPPING_SYSTEM.md  # 🆕 Ticker mapping guide
├── TICKER_MAPPING_QUICK_REFERENCE.md    # 🆕 Quick reference
└── requirements.txt       # Dependencies
```

**📚 See [docs/FOLDER_STRUCTURE.md](docs/FOLDER_STRUCTURE.md) for complete details**

## 📋 Bot Versions Comparison

| Feature | Lite | AI | Pro |
|---------|------|-----|-----|
| Speed | ⚡ Fastest | 🐢 Slow (1st run) | ⚡ Fast |
| Sentiment | Technical | AI (FinBERT) | Keyword |
| News Sources | 70+ (optional) | 70+ | 2 or 70+ ⚙️ |
| News Configuration | Auto fallback | Fixed | **Configurable** ⭐ |
| Analyst Ratings | ✅ | ✅ | ✅ |
| Intelligent Ranking | ✅ ⭐ | ✅ ⭐ | ✅ ⭐ |
| NA Handling | ✅ | ✅ | ✅ |
| News Classification | ✅ | ✅ | ✅ |
| Logging | Basic | Advanced | Advanced |
| Best For | Daily updates | Weekly analysis | Monthly reports |

**⚙️ PRO Configuration**: Set `USE_COMPREHENSIVE_NEWS = True` for 70+ sources or `False` for basic (Yahoo + Google). See [PRO_VERSION_CONFIGURATION.md](docs/PRO_VERSION_CONFIGURATION.md)

## 🏆 Intelligent Ranking System ⭐ NEW

All stocks are automatically ranked from **1 (best) to 650+ (worst)** based on 9 weighted metrics:

| Metric | Weight | Description |
|--------|--------|-------------|
| **Momentum** | 20% | 7-month price change (highest weight) |
| **Volume Surge** | 15% | Trading activity vs average |
| **Sentiment** | 15% | AI/keyword-based sentiment |
| **Investment Score** | 15% | Composite technical score |
| **Market Cap** | 10% | Company size/stability |
| **Signal** | 10% | Strong Buy/Watch/Neutral |
| **News Sentiment** | 8% | Recent news analysis |
| **Analyst Consensus** | 5% | Professional recommendations |
| **Analyst Ratings** | 2% | Numeric ratings (1-5) |

**📚 See [docs/RANKING_INDEX.md](docs/RANKING_INDEX.md) for complete ranking documentation**

## 🔄 Ticker Mapping & Filtering System 🆕

All 7 bots now include automatic ticker mapping and intelligent filtering:

### **Smart Ticker Resolution**
- **13 Company Renames**: Automatically maps old tickers to current NSE symbols (e.g., IIFLSEC → IIFLCAPS)
- **Zero Configuration**: Works seamlessly across all bots
- **Historical Data**: Ensures renamed companies continue to appear in analysis

### **Intelligent Filtering**
- **6 Delisted Stocks**: Auto-filters genuinely delisted stocks (bankruptcy, mergers)
- **4 Pump & Dump Stocks**: Blocks high-risk manipulation schemes
- **~906 Active Stocks**: Final count after filtering and deduplication

### **Key Features**
- ✅ Automatic ticker resolution before API calls
- ✅ Zero false "possibly delisted" errors
- ✅ Single source of truth in `data/nse_stocks_650.py`
- ✅ Easy maintenance - update one file to update all bots

**📚 See [PRODUCTION_TICKER_MAPPING_SYSTEM.md](PRODUCTION_TICKER_MAPPING_SYSTEM.md) for complete details**

## 📊 Database Schema

The bot populates 16 comprehensive columns in Notion:

1. **Ticker** - Stock symbol (e.g., RELIANCE.NS)
2. **Rank** ⭐ - Intelligent rank (1 = best opportunity)
3. **Market Cap** - Size classification (Large/Mid/Small)
4. **Price (₹)** - Current stock price
5. **Capital Market (₹)** - Market cap in Crores
6. **Sentiment** - Sentiment score (-1 to +1)
7. **Momentum (%)** - 6-month price momentum
8. **Volume Surge** - Volume ratio vs 20-day average
9. **Score** - Investment score (0-1500+)
10. **Signal** - Buy/Watch/Neutral/N/A
11. **News & Updates** - Latest news summary
12. **News Sentiment** - Positive/Neutral/Negative
13. **News Type** - Earnings/Product/Legal/M&A/etc.
14. **Consensus** - Analyst consensus (Strong Buy to Strong Sell)
15. **Ratings** - Average rating (X.XX/5.0)
16. **Last Updated** - Timestamp

See [docs/DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) for full technical details.

## 🎯 For Traders (Using Notion Day-to-Day)

If you mainly care about **picking stocks in Notion** rather than the code:

- Start with **[docs/NOTION_SCHEMA.md](docs/NOTION_SCHEMA.md)**  
  Understand what each column (Score, Rank, Signal, Momentum, Volume Surge, Consensus, Ratings, etc.) means and how to interpret it.
- Then read **[docs/NOTION_VIEWS.md](docs/NOTION_VIEWS.md)**  
  Step-by-step instructions to create daily views in Notion (Daily Momentum, News-Driven, Small-Cap Radar, Recently Updated) and a ready-made workflow for managing **10–20 positions** with sensible position sizing.

## 🛠️ Utility Scripts

### Setup Scripts

```bash
# Fresh start - Reset and reload database
python scripts/setup/fresh_start.py

# Add analyst rating columns
python scripts/setup/add_analyst_columns.py

# Setup AI models (for AI version)
python scripts/setup/setup_models.py
```

### Maintenance Scripts

```bash
# Load missing stocks
python scripts/maintenance/load_missing_stocks.py

# Update prices and scores
python scripts/maintenance/update_prices.py

# Check database status
python scripts/maintenance/check_database.py
```

## 📚 Documentation

### Core Documentation
- [Quick Start Guide](docs/QUICK_START.md) - Detailed getting started guide
- [Database Schema](docs/DATABASE_SCHEMA.md) - Complete column reference
- [System Guide](docs/SYSTEM_GUIDE.md) - Architecture and design
- [Feature Implementation](docs/FEATURE_IMPLEMENTATION.md) - Feature details

### Ticker Mapping System 🆕
- [**Production Ticker Mapping System**](PRODUCTION_TICKER_MAPPING_SYSTEM.md) - Complete guide to ticker mapping, company renames, and filtering
- [**Ticker Mapping Quick Reference**](TICKER_MAPPING_QUICK_REFERENCE.md) - Quick lookup for common mappings and integrations

### Trading & Usage
- [Notion Schema](docs/NOTION_SCHEMA.md) - Understanding Notion columns for traders
- [Notion Views](docs/NOTION_VIEWS.md) - Daily trading workflows and position management

### Technical Guides
- [Ranking System](docs/RANKING_INDEX.md) - Complete ranking documentation
- [PRO Configuration](docs/PRO_VERSION_CONFIGURATION.md) - Configure PRO bot settings
- [Incremental Bots Guide](INCREMENTAL_BOTS_GUIDE.md) - Upsert pattern for faster updates

## 🔧 Configuration

### Notion Setup

1. Create a Notion integration at https://www.notion.so/my-integrations
2. Create a database with 16 columns (see Database Schema)
3. Share the database with your integration
4. Copy the token and database ID to `.env`

### HuggingFace Token (AI Version Only)

1. Create account at https://huggingface.co
2. Generate access token
3. Add to `.env` as `HF_TOKEN`

## 🎯 Use Cases

- **Daily Trading**: Use Lite version for fast morning updates
- **Weekly Analysis**: Use AI version for deep sentiment analysis
- **Monthly Reports**: Use Pro version for comprehensive reports
- **Incremental Updates**: Use incremental versions for faster Notion upserts
- **Research**: Analyze ~906 active stocks with analyst ratings
- **News Monitoring**: Track news across 70+ sources
- **Company Renames**: Automatic handling via ticker mapping system

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **yfinance** - Stock data retrieval
- **FinBERT** - Financial sentiment analysis
- **Notion API** - Database integration
- **NSE** - Stock market data

## 📞 Support

For issues and questions:
- Check [docs/](docs/) for detailed documentation
- Review [Quick Start Guide](docs/QUICK_START.md)
- Open an issue on GitHub

---

**Made with ❤️ for Indian Stock Market Intelligence**
