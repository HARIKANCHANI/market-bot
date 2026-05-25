# 🚀 Market Intelligence Bot - Complete System Guide

> **Note:** This guide describes the original complete system, including some
> historical helper scripts that are no longer present in this repo
> (e.g. `update-market-cap-values.py`, `fix-duplicates.py`). For the
> **current production folder structure and commands**, use
> `PRODUCTION_READY.md`, `README.md`, and `DOCUMENTATION_INDEX.md` as the
> primary references. For the **live Notion database schema and how to use
> it for stock analysis**, see `NOTION_SCHEMA.md` (usage & scenarios) and
> `DATABASE_COLUMN_REFERENCE.md` (canonical column reference).

## 📖 Table of Contents
1. [System Overview](#system-overview)
2. [Main Components](#main-components)
3. [How to Use](#how-to-use)
4. [Utility Scripts](#utility-scripts)
5. [Database Schema](#database-schema)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 System Overview

**Market Intelligence Bot** is an enterprise-grade Python suite for analyzing Indian stock market data from NSE. It provides:

- ✅ **675 Stocks Coverage**: Nifty 150 + Midcap 200 + Smallcap 300
- ✅ **16+ Database Columns**: Complete market intelligence
- ✅ **AI Sentiment Analysis**: Using FinBERT (financial-specific BERT model)
- ✅ **Multi-source News**: Aggregation from 20+ sources
- ✅ **Technical Analysis**: Momentum, Volume, Scoring algorithms
- ✅ **Notion Integration**: Automatic database updates
- ✅ **Automated Scheduling**: Daily/weekly analysis runs

---

## 🏗️ Main Components

### **1. Main Analysis Scripts (3 versions)**

#### **A. market_bot_ai.py** - Full AI Version ⭐ Most Advanced
- **Features**: Complete AI sentiment analysis + News aggregation
- **Processing**: ~2-3 stocks/minute (AI model inference)
- **Use When**: You want full AI analysis with news sentiment
- **Columns Populated**: All 14 columns
- **Time for 675 stocks**: ~4-5 hours
- **Best For**: Weekend/overnight runs for comprehensive analysis

```bash
python src/bots/market_bot_ai.py
```

**What it does:**
1. Loads FinBERT AI model for sentiment analysis
2. Fetches stock data from Yahoo Finance
3. Aggregates news from Yahoo Finance + Google News
4. Analyzes news sentiment using AI
5. Classifies news by type (Financial, Corporate, etc.)
6. Calculates technical indicators
7. Generates investment scores and signals
8. Updates Notion database with all data

---

#### **B. market_bot_pro.py** - Production Version ⚡ Balanced
- **Features**: News aggregation + Basic sentiment (no AI model)
- **Processing**: ~20-25 stocks/minute
- **Use When**: You want news but faster than AI version
- **Columns Populated**: All 14 columns (News Sentiment without AI)
- **Time for 675 stocks**: ~30-35 minutes
- **Best For**: Daily updates with news coverage

```bash
python src/bots/market_bot_pro.py
```

**What it does:**
1. Fetches stock data from Yahoo Finance
2. Aggregates news from multiple sources
3. Calculates basic news sentiment (keyword-based)
4. Calculates technical indicators
5. Generates investment scores and signals
6. Updates Notion database

---

#### **C. market_bot_lite.py** - Fast Version 🚀 Fastest
- **Features**: Technical analysis only (no news, no AI)
- **Processing**: ~30-35 stocks/minute
- **Use When**: You need quick technical analysis
- **Columns Populated**: 11/14 columns (excludes News columns)
- **Time for 675 stocks**: ~18-20 minutes
- **Best For**: Quick daily scans, technical screening

```bash
python src/bots/market_bot_lite.py
```

**What it does:**
1. Fetches stock data from Yahoo Finance
2. Calculates technical indicators
3. Generates investment scores and signals
4. Updates Notion database (no news data)

---

### **2. Stock Data Module**

#### **nse_stocks_data_650.py**
- Contains list of 675 NSE stocks with classification
- Automatically validates stocks against Yahoo Finance
- Removes stocks with insufficient data
- Provides helper functions for stock retrieval

**Functions:**
- `get_all_stocks_with_classification()`: Returns all 675 stocks
- `get_validated_stocks()`: Returns only validated stocks
- `get_stock_by_ticker(ticker)`: Lookup specific stock

---

### **3. News & Sentiment Utilities**

#### **comprehensive-news-fetcher.py**
- Standalone utility to fetch news for existing stocks
- Aggregates from 20+ sources
- Updates only News & Updates column
- Can be run separately from main analysis

```bash
python comprehensive-news-fetcher.py
```

---

#### **news-sentiment-analyzer.py**
- Analyzes sentiment of existing news in database
- Uses FinBERT AI model
- Updates News Sentiment column
- Run after news-fetcher for AI sentiment

```bash
python news-sentiment-analyzer.py
```

---

#### **news-type-classifier.py**
- Classifies news by category/type
- Updates News Type column
- Categories: Financial Results, Corporate Actions, Regulatory, etc.

```bash
python news-type-classifier.py
```

---

## 🛠️ Utility Scripts

### **Database Management**

#### **scripts/setup/fresh_start.py** - Complete Database Reset
```bash
python scripts/setup/fresh_start.py
```
- Archives all existing entries
- Verifies database schema (13 columns)
- Starts fresh data load with `src/bots/market_bot_lite.py`
- **Use When**: You want to completely refresh all data

---

#### **clear-database.py** - Clear All Entries
```bash
python clear-database.py
```
- Deletes all pages/entries from database
- Keeps schema intact
- **Use When**: You want to clear data but keep structure

---

#### **update-market-cap-values.py** - Backfill Market Cap ⭐ NEW
```bash
python update-market-cap-values.py
```
- Fetches latest market capitalization for all stocks
- Updates "Capital Market (₹)" column
- Converts to Indian Crores (1 Cr = ₹10 Million)
- **Use When**: You want to update market cap values for existing stocks
- **Time**: ~5-7 minutes for all stocks

---

### **Column Management**

#### **add-serial-number-column.py** (Historical)
- Initially added the "Rank" column
- Assigned sequential numbers to stocks
- Now integrated in main scripts

---

#### **reorder-rank-column.py** (Historical)
- Moved "Rank" column to first position
- Now schema maintains proper order

---

#### **add-capital-market-column.py** (Historical)
- Initially added "Capital Market (₹)" column
- Now integrated in all three main scripts

---

### **Duplicate & Data Validation**

#### **fix-duplicates.py**
```bash
python fix-duplicates.py
```
- Identifies and removes duplicate stock entries
- Keeps only the most recent entry for each ticker
- **Use When**: You suspect duplicate entries

---

#### **verify-no-duplicates.py**
```bash
python verify-no-duplicates.py
```
- Verifies database has no duplicates
- Shows count of each ticker
- **Use When**: Checking database integrity

---

### **Testing & Validation**

#### **test-650-stocks.py**
```bash
python test-650-stocks.py
```
- Tests all 675 stocks for data availability
- Validates Yahoo Finance access
- Shows success/failure rate

---

#### **quick-test.py**
```bash
python quick-test.py
```
- Quick test with small sample of stocks
- Validates system functionality

---

### **Scheduling & Automation**

#### **automated-scheduler.py**
```bash
python automated-scheduler.py
```
- Schedules automatic daily/weekly analysis
- Runs `src/bots/market_bot_pro.py` at specified times
- Keeps running in background
- **Configuration**: Edit schedule times in script

---

## 📊 Database Schema (14 Columns)

| # | Column | Type | Contains |
|---|--------|------|----------|
| 1 | Ticker | Title | Stock symbol (RELIANCE, TCS, etc.) |
| 2 | Rank | Number | Sequential number 1-675 |
| 3 | Market Cap | Select | Large/Mid/Small Cap category |
| 4 | Price (₹) | Number | Current stock price in Rupees |
| 5 | **Capital Market (₹)** | Number | **Market capitalization in Crores** ⭐ |
| 6 | Sentiment | Number | AI/Technical sentiment score |
| 7 | Momentum (%) | Number | 6-month price momentum |
| 8 | Volume Surge | Number | Volume vs average ratio |
| 9 | Score | Number | Investment attractiveness score |
| 10 | Signal | Select | 🚀 Strong Buy / 👀 Watch / ❄️ Neutral |
| 11 | News & Updates | Rich Text | Latest news headlines |
| 12 | News Sentiment | Select | 🟢 Positive / 🟡 Neutral / 🔴 Negative |
| 13 | News Type | Multi-select | Financial Results, Corporate Actions, etc. |
| 14 | Last Updated | Date | Timestamp of last analysis |

**📖 For detailed column descriptions, see:** `DATABASE-COLUMNS-GUIDE.md`

---

## 🎯 How to Use - Common Scenarios

### **Scenario 1: First Time Setup**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test system
python src/bots/market_bot_lite.py

# 3. Start with lite version (fastest)
python src/bots/market_bot_lite.py

# 4. Add news later (optional)
python comprehensive-news-fetcher.py

# 5. Add AI sentiment (optional)
python news-sentiment-analyzer.py
```

---

### **Scenario 2: Daily Quick Update**
```bash
# Option A: Technical analysis only (20 min)
python src/bots/market_bot_lite.py

# Option B: With news (35 min)
python src/bots/market_bot_pro.py
```

---

### **Scenario 3: Weekend Comprehensive Analysis**
```bash
# Full AI analysis (4-5 hours)
python src/bots/market_bot_ai.py
```

---

### **Scenario 4: Fresh Start**
```bash
# Clear and reload all data
python fresh-start.py
```

---

### **Scenario 5: Update Market Cap Only**
```bash
# Update market capitalization values
python update-market-cap-values.py
```

---

### **Scenario 6: Fix Data Issues**
```bash
# Remove duplicates
python fix-duplicates.py

# Verify clean database
python verify-no-duplicates.py
```

---

## 🔧 Configuration

### **Environment Variables / Constants**

All scripts use the same configuration:

```python
NOTION_TOKEN = "ntn_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
DATABASE_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
HF_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # For AI model
```

**Stock Suffix**: All stocks use `.NS` (NSE) suffix for Yahoo Finance

---

## ⚡ Performance Comparison

| Version | Speed | Time (675 stocks) | Features |
|---------|-------|-------------------|----------|
| **Lite** | 30-35 stocks/min | 18-20 min | Technical only |
| **Pro** | 20-25 stocks/min | 30-35 min | + News (keyword sentiment) |
| **AI Full** | 2-3 stocks/min | 4-5 hours | + AI sentiment + Classification |

---

## 📋 File Structure

```
market-bot/
├── src/bots/market_bot_ai.py      # AI full version
├── src/bots/market_bot_pro.py     # Production version
├── src/bots/market_bot_lite.py    # Fast lite version
├── data/nse_stocks_650.py         # Stock data (675 stocks)
├── comprehensive-news-fetcher.py
├── news-sentiment-analyzer.py
├── news-type-classifier.py
├── fresh-start.py
├── clear-database.py
├── update-market-cap-values.py  ⭐ NEW
├── fix-duplicates.py
├── verify-no-duplicates.py
├── automated-scheduler.py
├── requirements.txt
	├── DATABASE_COLUMN_REFERENCE.md   # Column reference
	└── SYSTEM_GUIDE.md               # This file
```

---

## 🐛 Troubleshooting

### **Issue: UnicodeEncodeError in terminal**
**Solution**: System already handles this - emoji output adjusted for terminal compatibility

### **Issue: 429 Rate Limit Error from Notion**
**Solution**: Scripts include 1-2 second delays between API calls

### **Issue: Insufficient data for stock**
**Solution**: Stocks with <20 days of data are automatically skipped

### **Issue: Duplicate entries**
**Solution**: Run `python fix-duplicates.py`

### **Issue: Missing columns**
**Solution**: Columns are auto-created if not present in database

---

## 💡 Best Practices

1. **Daily Updates**: Use `src/bots/market_bot_lite.py` or `src/bots/market_bot_pro.py`
2. **Weekend Deep Analysis**: Use `src/bots/market_bot_ai.py` (AI version)
3. **Fresh Start**: Monthly or when major data issues occur
4. **Market Cap Updates**: Weekly via update-market-cap-values.py
5. **Duplicate Check**: After major data loads
6. **Automated Runs**: Set up automated-scheduler.py for hands-free operation

---

## 🎯 Quick Reference

### **What Each Script Does**

| Script | Purpose | Time | Output |
|--------|---------|------|--------|
| src/bots/market_bot_ai.py | Full AI analysis | 4-5 hrs | All 14 columns |
| src/bots/market_bot_pro.py | News + Technical | 30-35 min | All 14 columns |
| src/bots/market_bot_lite.py | Technical only | 18-20 min | 11/14 columns |
| fresh-start.py | Complete reset | Variable | Fresh database |
| update-market-cap-values.py | Market cap update | 5-7 min | Capital Market column |
| fix-duplicates.py | Remove duplicates | 2-3 min | Clean database |
| comprehensive-news-fetcher.py | Add news | 30-40 min | News column |
| news-sentiment-analyzer.py | AI sentiment | 10-15 min | Sentiment column |

---

## 🆕 What's New in Latest Version

### **Version 3.0 - Capital Market Integration** (Current)

✅ **New Column**: Capital Market (₹) - Market capitalization in Crores
✅ **All Versions Updated**: market_bot_ai.py, market_bot_pro.py, market_bot_lite.py
✅ **Utility Script**: update-market-cap-values.py for existing stocks
✅ **14 Total Columns**: Complete market intelligence coverage
✅ **Documentation**: DATABASE-COLUMNS-GUIDE.md + SYSTEM-COMPLETE-GUIDE.md

**What Changed:**
- All three main scripts now fetch and store market cap
- New standalone utility to backfill market cap for existing stocks
- Complete documentation of all 14 columns
- Comprehensive system guide for all utilities

---

## 📖 Additional Resources

### **Documentation Files**

1. **DATABASE-COLUMNS-GUIDE.md** - Detailed explanation of all 14 columns
2. **SYSTEM-COMPLETE-GUIDE.md** - This file (complete system reference)
3. **README-650-STOCKS.md** - Information about 675 stock coverage
4. **IMPLEMENTATION-COMPLETE.md** - Implementation history and milestones

---

## 🎓 Learning Path

### **For Beginners:**
1. Read this guide (`SYSTEM_GUIDE.md`)
2. Read `DATABASE_COLUMN_REFERENCE.md` to understand data
3. Run `python src/bots/market_bot_lite.py` on a small sample of stocks to verify setup
4. Use `src/bots/market_bot_lite.py` for your first full analysis
5. View your Notion database to see results

### **For Advanced Users:**
1. Set up `automated-scheduler.py` for daily runs (optional, legacy)
2. Use `src/bots/market_bot_pro.py` for daily updates
3. Run `src/bots/market_bot_ai.py` weekly for deep AI analysis
4. Create custom filters in Notion based on columns
5. Export data for further analysis

---

## 🔮 Future Enhancements (Roadmap)

- [ ] Real-time price alerts
- [ ] Portfolio tracking integration
- [ ] Custom scoring algorithms
- [ ] Email/SMS notifications for Strong Buy signals
- [ ] Historical trend tracking
- [ ] Sector-wise analysis
- [ ] Comparison with market indices
- [ ] Performance backtesting

---

## 📞 Support & Maintenance

### **Common Commands Cheatsheet**

```bash
# Quick daily update (fastest)
python src/bots/market_bot_lite.py

# Daily with news
python src/bots/market_bot_pro.py

# Weekly deep analysis
python src/bots/market_bot_ai.py

# Update market cap only
python update-market-cap-values.py

# Fresh start
python fresh-start.py

# Fix duplicates
python fix-duplicates.py

# Schedule automation
python automated-scheduler.py
```

---

## ✅ System Status

**Current Configuration:**
- ✅ 675 NSE Stocks (Nifty 150 + Midcap 200 + Smallcap 300)
- ✅ 14 Database Columns (Complete intelligence)
- ✅ 3 Analysis Versions (Lite/Pro/AI)
- ✅ 10+ Utility Scripts (Management & maintenance)
- ✅ Notion Integration (Automatic updates)
- ✅ AI Sentiment Analysis (FinBERT model)
- ✅ Multi-source News (20+ sources)
- ✅ Automated Scheduling (Hands-free operation)
- ✅ Complete Documentation (This guide + columns guide)

**Status**: ✅ **PRODUCTION READY** - All features implemented and tested!

---

## 🎉 Summary

You now have a complete, enterprise-grade market intelligence system with:

1. **Comprehensive Coverage**: 675 stocks across all market caps
2. **Complete Data**: 14 columns covering all aspects of market intelligence
3. **Multiple Versions**: Choose speed vs depth based on your needs
4. **Flexible Operation**: Run manually or automated
5. **Rich Documentation**: Complete guides for all features
6. **Production Quality**: Error handling, logging, rate limiting
7. **Easy Maintenance**: Utilities for all common tasks

**Your Market Intelligence Bot is ready to analyze the Indian stock market! 🚀📊**

---

**Document Version**: 3.0
**Last Updated**: May 2026
**System Status**: Production Ready ✅
