# 📊 Market Bot - Excel Version

## Overview

The **Excel Version** (`market_bot_excel.py`) is a new variant of the market bot that generates comprehensive Excel reports instead of uploading data to Notion. It includes all the features of the LITE version with intelligent multi-factor ranking.

---

## 🎯 Key Features

### ✅ **Same Analysis as LITE Version**
- Technical indicators (Momentum & Volume)
- News sentiment analysis (keyword-based)
- News type classification
- Sector information
- Market capitalization
- Analyst ratings (if module available)
- Intelligent multi-factor ranking system

### 📊 **Excel Output Instead of Notion**
- Creates formatted Excel (.xlsx) files
- **Timestamped filenames** - never overwrites previous reports
- Professional formatting with headers, borders, and colors
- Frozen header row for easy scrolling
- Optimized column widths
- All data in one comprehensive sheet

### 📁 **Organized Output**
- All Excel files saved to: `src/bots/excel/`
- Filename format: `market_analysis_YYYYMMDD_HHMMSS.xlsx`
- Example: `market_analysis_20260519_221530.xlsx`

---

## 📋 Excel Report Columns

The Excel report includes the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| **Rank** | Intelligent ranking (1 = best) | 1, 2, 3... |
| **Symbol** | Stock ticker symbol | RELIANCE, TCS, INFY |
| **Price (₹)** | Current stock price | 2450.50 |
| **Momentum (%)** | 7-month price momentum | +45.3% |
| **Volume Surge** | Volume vs 20-day average | 2.5x |
| **Trend** | Price trend indicator | 📈 📉 ➡️ |
| **Score** | Calculated score | 1250.5 |
| **Signal** | Buy/Watch/Neutral signal | 🚀 Strong Buy |
| **Sector** | Stock sector/industry | Technology, Banking |
| **Market Cap** | Size classification | Large Cap, Mid Cap |
| **Capital Market (₹Cr)** | Market cap in crores | 15234.56 |
| **News Sentiment** | News sentiment analysis | Positive, Neutral, Negative |
| **News Types** | News categories | Earnings, M&A, Product |
| **News & Updates** | Latest news headlines | [18-May] Company announces... |
| **Consensus** | Analyst consensus | Strong Buy, Buy, Hold |
| **Ratings** | Analyst ratings | 4.5/5.0 (12 analysts) |
| **FII (%)** | FII holdings (placeholder) | _Manual entry_ |
| **DII (%)** | DII holdings (placeholder) | _Manual entry_ |
| **Last Updated** | Timestamp | 2026-05-19 22:15 |

---

## 🚀 How to Run

### Basic Usage

```bash
python src/bots/market_bot_excel.py
```

### What It Does

1. **Phase 1: Data Collection**
   - Fetches data for all 675 stocks
   - Collects price, momentum, volume, news
   - Fetches sector and market cap
   - Gets analyst ratings (if available)

2. **Phase 2: Intelligent Ranking**
   - Ranks stocks using multi-factor algorithm
   - Calculates signals (Strong Buy/Watch/Neutral)
   - Computes composite scores

3. **Phase 3: Excel Creation**
   - Creates formatted Excel file
   - Saves to `src/bots/excel/` with timestamp
   - Shows top 5 ranked stocks
   - Displays summary statistics

---

## 📊 Example Output

```
======================================================================
📈 MARKET INTELLIGENCE BOT - EXCEL VERSION
======================================================================
🏆 Intelligent Multi-Factor Ranking: ENABLED
📊 Output Format: Excel (.xlsx)
✅ Using optimized ranking engine
======================================================================

📁 Excel output directory: C:\Users\...\market-bot\src\bots\excel

📊 Total stocks to analyze: 675
⏱️  Estimated time: ~22 minutes

======================================================================
📥 PHASE 1: DATA COLLECTION
======================================================================
[1/675] Analyzing RELIANCE (Large Cap)...
📊 RELIANCE: Price=₹2450.50, Momentum=+12.3%, Volume=1.5x, Trend=📈
...

======================================================================
🏆 PHASE 2: INTELLIGENT MULTI-FACTOR RANKING
======================================================================
⚡ Using optimized ranking engine...
✅ Ranked 675 stocks using intelligent multi-factor algorithm

======================================================================
📊 PHASE 3: CREATING EXCEL REPORT
======================================================================

💾 Creating Excel file: market_analysis_20260519_221530.xlsx
✅ Excel file created successfully!
📁 Location: C:\Users\...\market-bot\src\bots\excel\market_analysis_20260519_221530.xlsx
📊 Total stocks: 675

📈 Top 5 ranked stocks:
   1. MTARTECH        - ₹6810.00 (+212.0%) - Defense & Aerospace
   2. BAJAJCON        - ₹526.75 (+96.0%) - Consumer Goods
   3. KIRLOSENG       - ₹1660.30 (+88.4%) - Engineering
   4. MCX             - ₹3414.70 (+85.7%) - Exchange
   5. AVANTIFEED      - ₹1267.40 (+82.8%) - Aquaculture

======================================================================
✅ EXCEL REPORT CREATION COMPLETE!
======================================================================
```

---

## 📁 Output Files

All Excel files are saved with timestamps to prevent overwriting:

```
src/bots/excel/
├── market_analysis_20260519_120000.xlsx
├── market_analysis_20260519_140000.xlsx
├── market_analysis_20260519_221530.xlsx
└── ...
```

---

## 🆚 Comparison: Excel vs Notion Versions

| Feature | Excel Version | LITE Version (Notion) |
|---------|--------------|----------------------|
| **Analysis** | Same | Same |
| **Ranking** | Same | Same |
| **Output** | Excel files | Notion database |
| **Storage** | Local files | Cloud (Notion) |
| **Timestamping** | ✅ Yes | ❌ Overwrites |
| **Offline Access** | ✅ Yes | ❌ No |
| **Sharing** | Email/USB | Notion link |
| **FII/DII Data** | Placeholder columns | N/A |
| **Formatting** | Excel native | Notion tables |

---

## 💡 Use Cases

### When to Use Excel Version:
- ✅ Want historical snapshots of market analysis
- ✅ Need offline access to reports
- ✅ Prefer Excel for data manipulation
- ✅ Want to add FII/DII data manually
- ✅ Need to share via email or file
- ✅ Want to track changes over time

### When to Use Notion Version:
- ✅ Want real-time cloud access
- ✅ Prefer web-based interface
- ✅ Need team collaboration
- ✅ Want auto-sync across devices
- ✅ Prefer database filtering/sorting

---

## 🎯 Next Steps

1. **Run the Excel bot** to generate your first report
2. **Open the Excel file** in Microsoft Excel or Google Sheets
3. **Review the rankings** and analysis
4. **Add FII/DII data** manually in columns Q and R (if desired)
5. **Compare reports** over time to track market trends

---

## 🛠️ Technical Details

- **Dependencies**: pandas, openpyxl, yfinance, requests
- **Execution Time**: ~20-25 minutes for 675 stocks
- **File Size**: ~2-3 MB per report
- **Format**: Excel 2007+ (.xlsx)
- **Compatibility**: Excel, Google Sheets, LibreOffice Calc

---

## ✅ Summary

You now have **4 versions** of the market bot:

1. **AI Version** (`market_bot_ai.py`) - AI sentiment + Notion upload
2. **PRO Version** (`market_bot_pro.py`) - Advanced features + Notion upload
3. **LITE Version** (`market_bot_lite.py`) - Technical analysis + Notion upload
4. **EXCEL Version** (`market_bot_excel.py`) - Technical analysis + Excel export ⭐ **NEW!**

All versions use the same intelligent multi-factor ranking system! 🏆
