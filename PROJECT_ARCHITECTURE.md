# 🏗️ PROJECT ARCHITECTURE

**Market Bot - Complete System Architecture**

---

## 📊 SYSTEM OVERVIEW

The Market Bot is a multi-bot trading intelligence system that processes 906 NSE stocks through parallel processing, intelligent ranking, and automated Notion database updates.

---

## 🎯 HIGH-LEVEL ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────┐
│                     MARKET BOT ECOSYSTEM                             │
│                                                                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │   LITE     │  │     AI     │  │    PRO     │  │   EXCEL    │   │
│  │    BOT     │  │    BOT     │  │    BOT     │  │    BOT     │   │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘   │
│        │               │               │               │           │
│        └───────────────┴───────────────┴───────────────┘           │
│                            │                                        │
│  ┌─────────────────────────┴──────────────────────────┐            │
│  │            CORE PROCESSING ENGINE                   │            │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │            │
│  │  │   Parallel   │  │   Ranking    │  │ Sentiment│ │            │
│  │  │  Processing  │  │   Engine     │  │ Analyzer │ │            │
│  │  │  (4 workers) │  │ (Multi-factor)│  │ (FinBERT)│ │            │
│  │  │  + 3 retries │  │   9 factors  │  │  + Retry │ │            │
│  │  └──────┬───────┘  └──────┬───────┘  └────┬─────┘ │            │
│  │         │                 │                │       │            │
│  └─────────┼─────────────────┼────────────────┼───────┘            │
│            │                 │                │                    │
│  ┌─────────┴─────────────────┴────────────────┴───────┐            │
│  │              DATA INTEGRATION LAYER                │            │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │            │
│  │  │ yfinance │  │   News   │  │  Notion  │         │            │
│  │  │   API    │  │   APIs   │  │   API    │         │            │
│  │  └──────────┘  └──────────┘  └──────────┘         │            │
│  └────────────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 DATA FLOW DIAGRAM

```
START
  │
  ├─► Load Stock List (906 NSE stocks)
  │     │
  │     ├─► Apply Ticker Mapping (13 company renames)
  │     └─► Filter Delisted/Pump-Dump (10 stocks)
  │
  ├─► Create ThreadPool (4 parallel workers, 1.0s sleep, 3 retries)
  │
  ├─► For Each Stock (Parallel Processing):
  │     │
  │     ├─► Fetch Price Data (yfinance)
  │     │     ├─► Current Price
  │     │     ├─► Day High/Low
  │     │     ├─► Volume
  │     │     └─► Market Cap
  │     │
  │     ├─► Calculate Technical Indicators
  │     │     ├─► Momentum (%)
  │     │     ├─► Volume Ratio
  │     │     ├─► RSI
  │     │     └─► Trend (📈/📉/➡️)
  │     │
  │     ├─► Aggregate News (70+ sources)
  │     │     ├─► Company News
  │     │     ├─► Industry News
  │     │     └─► Market News
  │     │
  │     ├─► Analyze Sentiment (AI Bot only)
  │     │     ├─► FinBERT Model
  │     │     ├─► Positive/Negative/Neutral
  │     │     └─► Confidence Score
  │     │
  │     ├─► Fetch Analyst Ratings (with 3 retries + exponential backoff)
  │     │     ├─► Retry delays: 2s → 4s → 8s
  │     │     ├─► Buy/Hold/Sell consensus
  │     │     ├─► Target Price (Mean/High/Low)
  │     │     └─► Upgrades/Downgrades count
  │     │
  │     ├─► Calculate Ranking Score (0-100)
  │     │     ├─► Momentum Weight: 30%
  │     │     ├─► Volume Weight: 20%
  │     │     ├─► News Weight: 25%
  │     │     ├─► Sentiment Weight: 15%
  │     │     ├─► Analyst Weight: 8%
  │     │     └─► RSI Weight: 2%
  │     │
  │     └─► Validate & Map Data
  │           ├─► Sector Mapping (52 sectors + fallback)
  │           ├─► Emoji Support (UTF-8)
  │           └─► Handle N/A values
  │
  ├─► Aggregate Results (Thread-Safe)
  │
  ├─► Upload to Notion Database
  │     ├─► Upsert operation (Incremental bots)
  │     └─► Rate limiting (3 req/sec)
  │
  └─► Generate Excel Report (Excel bot only)
        └─► Save to output/ folder

END
```

---

## 🏛️ MODULE ARCHITECTURE

### **1. Bot Layer** (`src/bots/`)
```
src/bots/
├── market_bot_lite.py                # Lightweight, fast
├── market_bot_lite_incremental.py    # Daily updates
├── market_bot_ai.py                  # AI-powered sentiment
├── market_bot_ai_incremental.py      # Weekly AI updates
├── market_bot_pro.py                 # Robust with logging
├── market_bot_pro_incremental.py     # Monthly Pro updates
└── market_bot_excel.py               # Excel export
```

**Responsibilities:**
- Orchestrate data collection
- Coordinate parallel processing
- Handle user interaction
- Upload to Notion/Excel

---

### **2. Core Layer** (`src/core/`)
```
src/core/
├── ranking_engine.py          # Intelligent multi-factor ranking
├── news_aggregator.py         # 70+ news sources
├── sentiment_analyzer.py      # FinBERT AI sentiment
└── analyst_ratings.py         # Analyst recommendations
```

**Responsibilities:**
- Business logic
- Ranking calculations
- Sentiment analysis
- News classification

---

### **3. Utilities Layer** (`src/utils/`)
```
src/utils/
├── ticker_mapper.py           # Company rename handling
├── sector_validator.py        # 52 sectors + fallback
├── notion_uploader.py         # Notion API integration
└── emoji_handler.py           # UTF-8 emoji support
```

**Responsibilities:**
- Data transformation
- Validation
- API integration
- Error handling

---

### **4. Configuration Layer** (`src/config/`)
```
src/config/
├── env_config.py              # Environment variables
└── logging_config.py          # Centralized logging
```

**Responsibilities:**
- Configuration management
- Logging setup
- Environment validation

---

### **5. Data Layer** (`data/`)
```
data/
└── nse_stocks_650.py          # Stock list + mappings
    ├── NSE_STOCKS (906 stocks)
    ├── TICKER_MAPPING (13 renames)
    ├── DELISTED_STOCKS (6 filtered)
    └── PUMP_AND_DUMP (4 filtered)
```

**Responsibilities:**
- Stock universe
- Ticker mappings
- Filtering rules

---

## ⚡ PARALLEL PROCESSING ARCHITECTURE

### Current Configuration (Optimized for API Stability)

**Settings:**
- **Workers:** 4 (reduced from 12 for reliability)
- **Sleep:** 1.0s between stocks
- **Retries:** 3 attempts with exponential backoff (2s, 4s, 8s)
- **Success Rate:** ~99-100%

```
┌─────────────────────────────────────────────────┐
│       ThreadPoolExecutor (4 Workers)            │
│       + Retry Logic + Rate Limiting             │
├─────────────────────────────────────────────────┤
│                                                 │
│  Worker 1  ───► Stock 1, 5, 9, 13, ...         │
│  Worker 2  ───► Stock 2, 6, 10, 14, ...        │
│  Worker 3  ───► Stock 3, 7, 11, 15, ...        │
│  Worker 4  ───► Stock 4, 8, 12, 16, ...        │
│                                                 │
│  Each worker:                                   │
│  - Sleeps 1.0s between stocks                   │
│  - Retries API calls up to 3 times              │
│  - Uses exponential backoff on failures         │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │     Thread-Safe Statistics (Lock)         │ │
│  │  - Total Processed                        │ │
│  │  - Success Count                          │ │
│  │  - Error Count                            │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘

Performance: 7-11x faster than sequential processing
Execution Time: 4-7 minutes (vs 46 minutes sequential)
```

---

## 🎯 RANKING ENGINE ARCHITECTURE

```
RANKING ENGINE (Multi-Factor Scoring)
│
├─► Factor 1: Momentum (30%)
│   ├─► Price change percentage
│   └─► Normalized to 0-100
│
├─► Factor 2: Volume (20%)
│   ├─► Current / Average volume
│   └─► Normalized to 0-100
│
├─► Factor 3: News Activity (25%)
│   ├─► News count (0-50+)
│   └─► Normalized to 0-100
│
├─► Factor 4: AI Sentiment (15%)
│   ├─► FinBERT score (-1 to +1)
│   └─► Mapped to 0-100
│
├─► Factor 5: Analyst Ratings (8%)
│   ├─► Buy/Hold/Sell (1-5)
│   └─► Normalized to 0-100
│
└─► Factor 6: RSI (2%)
    ├─► RSI value (0-100)
    └─► Direct mapping

FINAL SCORE = Σ (Factor × Weight)
Range: 0-100
```

---

## 📚 COMPLETE ARCHITECTURE DOCUMENTATION

For detailed architecture diagrams and data flows:
- **Architecture Overview:** `docs/architecture/ARCHITECTURE_DIAGRAMS.md`
- **Data Flow Details:** `docs/architecture/DATA_FLOW_DETAILED.md`
- **Folder Structure:** `docs/architecture/FOLDER_STRUCTURE.md`
- **System Guide:** `docs/architecture/SYSTEM_GUIDE.md`

---

**Last Updated:** 2026-05-25  
**Version:** 2.0  
**Status:** ✅ Production-Ready
