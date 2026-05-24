# 📊 Database Columns Guide - Complete Reference

## Overview

Your Notion database contains **14 columns** that provide comprehensive market intelligence for Indian stocks. This guide explains each column in detail.

---

## 📋 Complete Column List (in order)

| # | Column Name | Type | Purpose |
|---|-------------|------|---------|
| 1 | **Ticker** | Title | Stock symbol identifier |
| 2 | **Rank** | Number | Sequential ranking (1-675) |
| 3 | **Market Cap** | Select | Company size category |
| 4 | **Price (₹)** | Number | Current stock price |
| 5 | **Capital Market (₹)** | Number | Market capitalization value |
| 6 | **Sentiment** | Number | AI/Technical sentiment score |
| 7 | **Momentum (%)** | Number | 6-month price momentum |
| 8 | **Volume Surge** | Number | Volume vs average ratio |
| 9 | **Score** | Number | Investment score |
| 10 | **Signal** | Select | Buy/Watch/Neutral recommendation |
| 11 | **News & Updates** | Rich Text | Latest news headlines |
| 12 | **News Sentiment** | Select | News sentiment label |
| 13 | **News Type** | Multi-select | News categories |
| 14 | **Last Updated** | Date | Last analysis timestamp |

---

## 📖 Detailed Column Descriptions

### 1️⃣ **Ticker** (Title)
- **Type**: Title (Primary identifier)
- **Format**: Stock symbol (e.g., RELIANCE, TCS, INFY)
- **Purpose**: Unique identifier for each stock
- **Source**: NSE stock list
- **Example**: `RELIANCE`, `HDFCBANK`, `TATAMOTORS`
- **Note**: All stocks use `.NS` suffix for Yahoo Finance queries

---

### 2️⃣ **Rank** (Number)
- **Type**: Number (Integer)
- **Format**: Sequential number 1-675
- **Purpose**: Serial number / Stock ranking
- **Source**: Auto-assigned during data load
- **Example**: `1`, `2`, `3`, ... `675`
- **Use Case**: Track processing order, create numbered lists
- **Note**: First data column (after Ticker)

---

### 3️⃣ **Market Cap** (Select)
- **Type**: Select (Category)
- **Format**: Large Cap / Mid Cap / Small Cap
- **Purpose**: Company size classification
- **Source**: Based on NSE indices
- **Values**:
  - `Large Cap`: Nifty 150 stocks
  - `Mid Cap`: Nifty Midcap 200 stocks
  - `Small Cap`: Nifty Smallcap 300 stocks
- **Example**: `Large Cap` (RELIANCE), `Mid Cap` (SAIL)
- **Use Case**: Filter by company size, portfolio diversification

---

### 4️⃣ **Price (₹)** (Number)
- **Type**: Number (Decimal, 2 places)
- **Format**: Indian Rupees
- **Purpose**: Current stock price
- **Source**: Yahoo Finance (real-time/latest close)
- **Example**: `1335.90`, `2283.20`, `768.65`
- **Update Frequency**: Every analysis run
- **Use Case**: Track current valuations, price comparisons

---

### 5️⃣ **Capital Market (₹)** (Number) ⭐ NEW
- **Type**: Number (Decimal, 2 places)
- **Format**: Crores (₹ Cr) - 1 Crore = ₹10 Million
- **Purpose**: Market capitalization (company valuation)
- **Source**: Yahoo Finance `marketCap` field
- **Calculation**: Market Cap (USD) ÷ 10,000,000 = Crores
- **Example**: 
  - `32,150.43` Cr (Large Cap)
  - `16,078.73` Cr (Mid Cap)
  - `4,895.06` Cr (Small Cap)
- **Use Case**: 
  - Compare company sizes within same sector
  - Filter by market cap ranges (>20k, 5k-20k, <5k)
  - Identify blue-chip stocks vs growth opportunities
  - Portfolio allocation based on company size

---

### 6️⃣ **Sentiment** (Number)
- **Type**: Number (Decimal, 1 decimal place)
- **Format**: -1.0 to +1.0 scale
- **Purpose**: Overall market sentiment indicator
- **Source**: 
  - **AI Version**: FinBERT sentiment analysis from news
  - **Lite Version**: Technical sentiment from recent price action
- **Values**:
  - `1.0`: Very Positive
  - `0.0`: Neutral
  - `-1.0`: Very Negative
- **Example**: `0.85` (Positive), `-0.45` (Negative)
- **Use Case**: Gauge market mood, sentiment-based screening

---

### 7️⃣ **Momentum (%)** (Number)
- **Type**: Number (Decimal, 4 places)
- **Format**: Decimal ratio (multiply by 100 for percentage)
- **Purpose**: 6-month price momentum
- **Source**: Calculated from price data
- **Calculation**: `(Current Price - Price 6mo ago) / Price 6mo ago`
- **Example**: 
  - `0.2531` = +25.31% (Strong uptrend)
  - `-0.2339` = -23.39% (Downtrend)
  - `0.0546` = +5.46% (Mild uptrend)
- **Use Case**: Identify trending stocks, momentum trading strategies

---

### 8️⃣ **Volume Surge** (Number)
- **Type**: Number (Decimal, 2 places)
- **Format**: Ratio (multiplier)
- **Purpose**: Current volume vs 20-day average
- **Source**: Calculated from volume data
- **Calculation**: `Current Volume / 20-day Average Volume`
- **Example**:
  - `2.44` = 244% of average (High interest)
  - `1.46` = 146% of average (Above average)
  - `0.67` = 67% of average (Below average)
- **Use Case**: Detect unusual trading activity, breakout confirmation

---

### 9️⃣ **Score** (Number)
- **Type**: Number (Decimal, 2 places)
- **Format**: Positive or negative score
- **Purpose**: Overall investment score/attractiveness
- **Source**: Calculated from multiple factors
- **Calculation**: Based on Signal + Momentum + Volume
  - Strong Buy: +1000 base points
  - Watch: +500 base points
  - Neutral: 0 base points
  - Plus: Momentum × 500
  - Plus: Volume × 50
- **Example**:
  - `723` (High score - attractive)
  - `571` (Good score - watch)
  - `-84` (Negative score - avoid)
- **Use Case**: Rank stocks by attractiveness, quick filtering

---

### 🔟 **Signal** (Select)
- **Type**: Select (Category)
- **Format**: Emoji + Text label
- **Purpose**: Investment recommendation
- **Source**: Algorithm based on Momentum + Volume
- **Values**:
  - `🚀 Strong Buy`: Momentum >10% AND Volume >1.2x
  - `👀 Watch`: Momentum >5% OR Volume >1.1x
  - `❄️ Neutral`: All other cases
- **Example**: `🚀 Strong Buy`, `👀 Watch`, `❄️ Neutral`
- **Use Case**: Quick visual screening, actionable recommendations

---

### 1️⃣1️⃣ **News & Updates** (Rich Text)
- **Type**: Rich Text (Long text)
- **Format**: Formatted news headlines with dates
- **Purpose**: Latest news and market updates
- **Source**: Multiple sources (Yahoo Finance + Google News)
- **Format**: `[Date] Headline | [Date] Headline | ...`
- **Example**:
  ```
  [12-May] Company announces record Q4 profit |
  [10-May] New expansion plans revealed |
  [08-May] Stock hits 52-week high
  ```
- **Availability**:
  - ✅ AI & PRO Versions (`market_bot_ai.py`, `market_bot_pro.py`)
  - ❌ Lite Version (not included)
- **Use Case**: Stay updated on company developments, news-based trading

---

### 1️⃣2️⃣ **News Sentiment** (Select)
- **Type**: Select (Category)
- **Format**: Emoji + Label
- **Purpose**: Overall news sentiment classification
- **Source**: AI sentiment analysis of news text
- **Values**:
  - `🟢 Positive`: Predominantly positive news
  - `🟡 Neutral`: Mixed or neutral news
  - `🔴 Negative`: Predominantly negative news
- **Example**: `🟢 Positive`, `🟡 Neutral`, `🔴 Negative`
- **Availability**:
  - ✅ AI & PRO Versions (`market_bot_ai.py`, `market_bot_pro.py`)
  - ❌ Lite Version (not included)
- **Use Case**: Quick sentiment check, filter by news sentiment

---

### 1️⃣3️⃣ **News Type** (Multi-select)
- **Type**: Multi-select (Categories, multiple allowed)
- **Format**: Category tags
- **Purpose**: Classify news by type/topic
- **Source**: AI classification of news headlines
- **Values**:
  - `📈 Financial Results`: Earnings, revenue reports
  - `💼 Corporate Actions`: M&A, dividends, splits
  - `📋 Regulatory`: Compliance, legal updates
  - `🚀 Product Launch`: New products/services
  - `🤝 Partnerships`: Deals, collaborations
  - `👥 Leadership`: Management changes
  - `📰 General`: Other market news
- **Example**: `📈 Financial Results`, `💼 Corporate Actions`
- **Availability**:
  - ✅ AI Version (`market_bot_ai.py`)
  - ⚠️ Pro Version (if classifier enabled)
  - ❌ Lite Version (not included)
- **Use Case**: Filter by news type, focus on specific events

---

### 1️⃣4️⃣ **Last Updated** (Date)
- **Type**: Date (Timestamp)
- **Format**: ISO 8601 date-time
- **Purpose**: Track when the stock was last analyzed
- **Source**: Auto-generated during analysis
- **Example**: `2026-05-18T23:30:45.123Z`
- **Display**: Shows as relative time (e.g., "2 hours ago")
- **Use Case**: Know data freshness, schedule re-analysis

---

## 🎯 Column Groups by Purpose

### **Identification**
- Ticker (Who)
- Rank (Order)
- Market Cap (Size Category)

### **Valuation**
- Price (₹) (Current Price)
- Capital Market (₹) (Company Valuation) ⭐

### **Technical Analysis**
- Momentum (%) (Trend)
- Volume Surge (Activity)
- Sentiment (Overall Mood)

### **Investment Decision**
- Score (Attractiveness)
- Signal (Recommendation)

### **News Intelligence** (AI versions only)
- News & Updates (Headlines)
- News Sentiment (News Mood)
- News Type (Categories)

### **Metadata**
- Last Updated (Freshness)

---

## 💡 How to Use These Columns

### **For Stock Screening:**
1. Filter by **Signal** = "🚀 Strong Buy"
2. Sort by **Score** (descending)
3. Check **Momentum** > 10%
4. Verify **Volume Surge** > 1.2x

### **For Company Size Analysis:**
1. Filter by **Market Cap** category
2. Sort by **Capital Market (₹)**
3. Compare valuations within same category

### **For Sentiment Trading:**
1. Filter by **News Sentiment** = "🟢 Positive"
2. Check **Sentiment** score > 0.5
3. Read **News & Updates** for context

### **For Value Discovery:**
1. Filter **Capital Market (₹)** < 5,000 Cr (Small Cap)
2. Filter **Momentum** > 15% (Strong growth)
3. Check **News & Updates** for catalysts

---

## 📊 Data Quality Notes

- **Real-time Data**: Price, Volume updated on each run
- **Historical Data**: Momentum calculated from 6-month history
- **News Data**: Aggregated from multiple sources (varies by version)
- **AI Analysis**: Available in `market_bot_ai.py` (full AI) version
- **Update Frequency**: Run scripts daily/weekly for latest data

---

## 🔄 Version Differences

| Column | Lite | Pro | AI Full |
|--------|------|-----|---------|
| Ticker - Last Updated | ✅ | ✅ | ✅ |
| All 14 columns | ✅ | ✅ | ✅ |
| News & Updates | ❌ | ✅ | ✅ |
| AI News Sentiment | ❌ | ⚠️ | ✅ |
| News Type Classification | ❌ | ⚠️ | ✅ |

**Legend**: ✅ Included | ❌ Not included | ⚠️ Optional/Partial

---

**Your database now has complete 14-column coverage for comprehensive market intelligence! 📊**

