# 📚 QUICK ACCESS GUIDE

**Market Bot - Enterprise-Grade Indian Stock Market Intelligence Suite**

---

## 🚀 Root Directory

### Start Here
- **Main Documentation:** `README.md`
- **Test a Stock:** `python test_single_stock.py RELIANCE`

---

## 📖 Documentation

### Master Documentation Hub
- **Complete Documentation:** `docs/README.md`
- **Getting Started:** `docs/getting-started/QUICK_START.md`
- **Quick Reference:** `docs/reference/QUICK_REFERENCE.md`

---

## 👥 FOR NEW USERS

### Your First Steps
1. **Read:** `README.md` (root)
2. **Setup:** `docs/getting-started/QUICK_START.md`
3. **Reference:** `docs/reference/QUICK_REFERENCE.md`

### Quick Start Commands
```bash
# 1. Install
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure .env
NOTION_TOKEN=your_token
DATABASE_ID=your_database_id

# 3. Run
python -m src.bots.market_bot_lite
```

---

## 💻 FOR DEVELOPERS

### Technical Documentation
1. **API Reference:** `docs/technical/TECHNICAL_DOCUMENTATION.md`
2. **System Architecture:** `docs/architecture/ARCHITECTURE_DIAGRAMS.md`
3. **Code Documentation:** `docs/technical/COMPLETE_PYTHON_FILES_DOCUMENTATION.md`

### Development Commands
```bash
# Run specific bot
python -m src.bots.market_bot_ai
python -m src.bots.market_bot_pro
python -m src.bots.market_bot_excel

# Run tests
python -m pytest tests/

# Test single stock
python test_single_stock.py <TICKER>
```

---

## 📈 FOR TRADERS

### Trading Documentation
1. **Ranking System:** `docs/guides/features/RANKING_SYSTEM.md`
2. **Bot Usage Guide:** `docs/guides/bot-usage/INCREMENTAL_BOTS_GUIDE.md`
3. **Trend Analysis:** `docs/guides/features/TREND_LOGIC_WITH_VOLUME.md`

### Trading Features
- **📊 Intelligent Ranking:** Multi-factor scoring system
- **📰 News Aggregation:** 70+ sources
- **🤖 AI Sentiment:** FinBERT-powered analysis
- **📈 Trend Logic:** Volume-confirmed trends
- **⚡ Performance:** 7-11x faster with parallel processing

---

## 🗂️ PROJECT STRUCTURE

```
market-bot/
├── src/                    # Source code
│   ├── bots/              # 7 bot versions
│   ├── core/              # Core functionality
│   ├── utils/             # Utility functions
│   └── config/            # Configuration
├── docs/                   # Documentation hub
│   ├── getting-started/   # New user guides
│   ├── guides/            # How-to guides
│   ├── architecture/      # System design
│   ├── technical/         # Developer docs
│   ├── optimization/      # Performance tuning
│   ├── deployment/        # Production setup
│   ├── maintenance/       # Troubleshooting
│   ├── reports/           # Historical records
│   └── reference/         # Quick reference
├── data/                   # Stock data & mappings
├── scripts/                # Automation scripts
├── tests/                  # Test files
├── logs/                   # Log files
├── output/                 # Excel outputs
└── README.md              # Main documentation
```

---

## 📊 PROJECT ARCHITECTURE

### Complete System Architecture

**📖 See detailed architecture documentation:**
- **Complete Architecture:** `PROJECT_ARCHITECTURE.md` (root)
- **Architecture Diagrams:** `docs/architecture/ARCHITECTURE_DIAGRAMS.md`
- **Data Flow:** `docs/architecture/DATA_FLOW_DETAILED.md`

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MARKET BOT SYSTEM                        │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐         ┌────▼────┐        ┌────▼────┐
   │ LITE    │         │   AI    │        │   PRO   │
   │ BOT     │         │  BOT    │        │   BOT   │
   └────┬────┘         └────┬────┘        └────┬────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐         ┌────▼────┐        ┌────▼────┐
   │  NEWS   │         │ RANKING │        │SENTIMENT│
   │AGGREG.  │         │ ENGINE  │        │ANALYZER │
   └────┬────┘         └────┬────┘        └────┬────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐         ┌────▼────┐        ┌────▼────┐
   │ yfinance│         │  News   │        │ Notion  │
   │   API   │         │  APIs   │        │   API   │
   └─────────┘         └─────────┘        └─────────┘
```

### Interactive Architecture Diagram
**See the interactive Mermaid diagram in:** `PROJECT_ARCHITECTURE.md`

---

## 🤖 BOT VERSIONS

| Bot | Best For | Speed | AI |
|-----|----------|-------|-----|
| **Lite** | Daily updates | ⚡ Fastest | ❌ |
| **Lite Incremental** | Quick daily sync | ⚡ Super Fast | ❌ |
| **AI** | Weekly analysis | 🐢 Slow (1st run) | ✅ FinBERT |
| **AI Incremental** | Weekly sync | ⚡ Fast | ✅ FinBERT |
| **Pro** | Monthly reports | ⚡ Fast | ❌ |
| **Pro Incremental** | Monthly sync | ⚡ Super Fast | ❌ |
| **Excel** | Offline analysis | ⚡ Fast | ❌ |

---

## ⚡ QUICK COMMANDS

```bash
# Run Bots
python -m src.bots.market_bot_lite              # Fastest
python -m src.bots.market_bot_ai                # Most accurate
python -m src.bots.market_bot_pro               # Most robust
python -m src.bots.market_bot_excel             # Excel output

# Incremental Updates (Faster)
python -m src.bots.market_bot_lite_incremental
python -m src.bots.market_bot_ai_incremental
python -m src.bots.market_bot_pro_incremental

# Test Single Stock
python test_single_stock.py RELIANCE
python test_single_stock.py TCS
python test_single_stock.py INFY
```

---

## 📚 COMPLETE DOCUMENTATION MAP

### Getting Started
- `docs/getting-started/QUICK_START.md` - Installation & setup
- `docs/getting-started/README.md` - Onboarding guide

### Bot Usage
- `docs/guides/bot-usage/INCREMENTAL_BOTS_GUIDE.md` - All bots explained
- `docs/guides/bot-usage/README_EXCEL_VERSION.md` - Excel bot guide

### Features
- `docs/guides/features/RANKING_SYSTEM.md` - Intelligent ranking
- `docs/guides/features/TREND_LOGIC_WITH_VOLUME.md` - Trend analysis
- `docs/guides/features/PRODUCTION_TICKER_MAPPING_SYSTEM.md` - Ticker mapping
- `docs/guides/features/SECTOR_VALIDATION_FIX.md` - Sector validation

### Testing
- `docs/guides/testing/TEST_SINGLE_STOCK_GUIDE.md` - Test individual stocks

### Architecture & Design
- `docs/architecture/ARCHITECTURE_DIAGRAMS.md` - System design
- `docs/architecture/DATA_FLOW_DETAILED.md` - Data pipeline
- `docs/architecture/FOLDER_STRUCTURE.md` - Project organization

---

**Last Updated:** 2026-05-25  
**Version:** 2.0  
**Status:** ✅ Enterprise-Ready
