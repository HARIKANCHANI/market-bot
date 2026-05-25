# 📊 Market Bot - Detailed Data Flow Documentation

## Complete Step-by-Step Processing Pipeline

**Document Purpose**: Human-readable guide to how a single stock is processed through the Market Bot system  
**Version**: 1.0.0  
**Date**: May 19, 2026  
**Status**: Production Ready

---

## 🎯 Overview

This document explains the complete data flow for processing a single stock through the Market Bot system, from initial configuration loading to final Notion database update. The flow applies to all three bot versions (Lite, AI, Pro) with minor variations noted.

**Total Processing Time**: 5-10 seconds per stock  
**Total Stocks**: 675 NSE stocks  
**Total Run Time**: 5-45 minutes (depending on bot version)

---

## 📋 Table of Contents

1. [Initialization Phase](#1-initialization-phase)
2. [Stock Iteration Phase](#2-stock-iteration-phase)
3. [Data Fetching Phase](#3-data-fetching-phase)
4. [Data Processing Phase](#4-data-processing-phase)
5. [Intelligence Gathering Phase](#5-intelligence-gathering-phase)
6. [Calculation Phase](#6-calculation-phase)
7. [Notion Update Phase](#7-notion-update-phase)
8. [Completion Phase](#8-completion-phase)
9. [Error Handling](#9-error-handling)
10. [Summary Statistics](#10-summary-statistics)

---

## 1. Initialization Phase

### Step 1.1: Start Bot Execution
**Action**: User runs bot script  
**Command**: `python src/bots/market_bot_lite.py` (or AI/Pro version)  
**Duration**: Instant  

**What Happens**:
- Script execution begins
- Python interpreter loads the file
- All import statements executed
- Global variables initialized

---

### Step 1.2: Load Configuration
**Action**: Read environment variables and configuration  
**Duration**: < 1 second  

**Configuration Loaded**:
1. **NOTION_TOKEN**: Authentication token for Notion API
   - Source: Environment variable or hardcoded
   - Format: `ntn_xxxxxxxxxxxxxxxxxxxxx`
   - Required: Yes

2. **DATABASE_ID**: Notion database identifier
   - Source: Environment variable or hardcoded
   - Format: 32-character hexadecimal string
   - Required: Yes

3. **HF_TOKEN**: HuggingFace token (AI version only)
   - Source: Environment variable or hardcoded
   - Format: `hf_xxxxxxxxxxxxxxxx`
   - Required: Only for AI version

4. **Logging Configuration**:
   - Log file path: `logs/market_bot_*.log`
   - Log level: INFO
   - Format: Timestamp + Level + Message

**Validation**:
- Check if tokens are present
- Verify they are not empty
- Test Notion API connection (optional)

**Output**: Configuration dictionary ready for use

---

### Step 1.3: Load Stock List
**Action**: Import and process stock data  
**Duration**: < 1 second  
**Source**: `data/nse_stocks_650.py`  

**What Happens**:
```python
from data.nse_stocks_650 import get_all_stocks_with_classification

stocks = get_all_stocks_with_classification()
# Returns: [("RELIANCE.NS", "Large Cap"), ("TCS.NS", "Large Cap"), ...]
```

**Data Structure**:
- Total stocks: 675
- Format: List of tuples (ticker, market_cap_classification)
- Large Cap: 150 stocks (Nifty 150)
- Mid Cap: 200 stocks (Midcap 200)
- Small Cap: 325 stocks (Smallcap 300+)

**Validation**:
- Verify list is not empty
- Check each ticker ends with ".NS"
- Confirm market cap is valid ("Large Cap", "Mid Cap", or "Small Cap")

**Output**: List of 675 stock tuples ready for iteration

---

## 2. Stock Iteration Phase

### Step 2.1: Begin Loop
**Action**: Start iterating through stock list  
**Duration**: Entire processing time  

**Loop Structure**:
```python
for idx, (ticker, cap_size) in enumerate(stocks, 1):
    # idx = Sequential rank (1-675)
    # ticker = Stock symbol (e.g., "RELIANCE.NS")
    # cap_size = Market cap classification (e.g., "Large Cap")
    
    # Process this stock...
```

**For Each Stock**:
- Index: Current position (1 to 675)
- Ticker: NSE stock symbol
- Market Cap: Size classification

---

### Step 2.2: Get Current Stock Details
**Action**: Extract ticker and market cap for current iteration  
**Duration**: Instant  

**Example**:
- Ticker: `RELIANCE.NS`
- Market Cap: `Large Cap`
- Rank: `1` (first stock)

**Log Output**:
```
INFO - Processing stock 1/675: RELIANCE.NS (Large Cap)
```

---

## 3. Data Fetching Phase

### Step 3.1: Fetch Historical Price Data
**Action**: Download 6-month price and volume history from Yahoo Finance  
**Duration**: 1-3 seconds  
**API**: yfinance library  

**API Call**:
```python
import yfinance as yf

hist = yf.download(
    ticker,           # "RELIANCE.NS"
    period="6mo",     # Last 6 months
    progress=False    # Disable progress bar
)
```

**Data Retrieved**:
- **Columns**: Open, High, Low, Close, Volume, Adj Close
- **Rows**: ~120-130 trading days (6 months)
- **Format**: Pandas DataFrame
- **Size**: ~10 KB per stock

**Sample Data**:
```
Date         Open      High      Low       Close     Volume
2025-11-19   2,450.00  2,475.00  2,440.00  2,456.75  5,234,567
2025-11-20   2,460.00  2,480.00  2,455.00  2,470.30  4,876,234
...
```

---

### Step 3.2: Check Data Availability
**Action**: Verify if sufficient data was retrieved  
**Duration**: Instant  

**Validation Checks**:
1. **Data exists**: DataFrame is not empty
2. **Sufficient rows**: At least 120 days of data
3. **Valid prices**: No NaN or zero values
4. **Recent data**: Latest date is within last 7 days

**Decision Point**: Does data exist and is valid?

---

### Path A: Data Available (Normal Processing)
**Condition**: Valid price data retrieved  
**Percentage**: ~65-70% of stocks (420-450 stocks)  

**Continue to**: Step 4.1 (Calculate Momentum)

---

### Path B: No Data Available (NA Handling)
**Condition**: No data or insufficient data  
**Percentage**: ~30-35% of stocks (225-255 stocks)  
**Common Reasons**:
- Stock delisted
- Very low trading volume
- Recent IPO (< 6 months old)
- Suspended trading
- Data fetch error

**Action**: Set Default NA Values  
**Duration**: Instant  

**Default Values Set**:
```python
data = {
    "ticker": ticker,          # e.g., "XYZ.NS"
    "cap": cap_size,          # e.g., "Small Cap"
    "price": None,            # No price available
    "market_cap": None,       # No market cap
    "mom": 0.0,               # Zero momentum
    "vol": 0.0,               # Zero volume surge
    "sent": 0.0,              # Neutral sentiment
    "news": None,             # No news
    "news_sentiment": None,   # No news sentiment
    "news_types": [],         # No news types
    "has_data": False         # Flag for NA stock
}
```

**Skip to**: Step 6.4 (Calculate Score with NA values)

---

## 4. Data Processing Phase

### Step 4.1: Calculate Momentum (6-Month Return)
**Action**: Calculate price change over 6 months  
**Duration**: Instant  
**Applies to**: Stocks with data only  

**Formula**:
```
Momentum = (Current Price - 6-Month-Ago Price) / 6-Month-Ago Price
```

**Python Code**:
```python
current_price = hist['Close'].iloc[-1]   # Most recent close
old_price = hist['Close'].iloc[0]        # 6 months ago close

momentum = (current_price - old_price) / old_price
```

**Example Calculation**:
- 6 months ago price: ₹2,100
- Current price: ₹2,456.75
- Momentum = (2,456.75 - 2,100) / 2,100 = 0.1699 (16.99% gain)

**Result Range**:
- Typical: -0.50 to +2.00 (-50% to +200%)
- Extreme gains: > 2.00 (> 200%)
- Extreme losses: < -0.50 (< -50%)

**Interpretation**:
- `> 0.20`: Strong upward momentum (> 20% gain)
- `0.10 to 0.20`: Moderate upward momentum
- `0 to 0.10`: Slight upward momentum
- `< 0`: Downward momentum (loss)

**Output**: Decimal value (e.g., 0.1699)

**Log Output**:
```
INFO - RELIANCE.NS: Momentum = 16.99%
```

---

### Step 4.2: Calculate Volume Surge
**Action**: Calculate current volume vs 20-day average
**Duration**: Instant
**Applies to**: Stocks with data only

**Formula**:
```
Volume Surge = Current Volume / 20-Day Average Volume
```

**Python Code**:
```python
recent_volume = hist['Volume'].iloc[-1]      # Latest day volume
avg_volume = hist['Volume'].tail(20).mean()  # Last 20 days average

volume_surge = recent_volume / avg_volume if avg_volume > 0 else 0
```

**Example Calculation**:
- Current volume: 5,234,567 shares
- 20-day average: 3,600,000 shares
- Volume Surge = 5,234,567 / 3,600,000 = 1.45

**Result Range**:
- Typical: 0.50 to 2.00
- High volume: > 2.00 (unusual activity)
- Low volume: < 0.80 (below average)

**Interpretation**:
- `> 2.0`: Very high volume (news event, institutional buying)
- `1.2 - 2.0`: High volume (positive signal)
- `0.8 - 1.2`: Normal trading volume
- `< 0.8`: Low volume (caution)

**Output**: Decimal value (e.g., 1.45)

**Log Output**:
```
INFO - RELIANCE.NS: Volume Surge = 1.45x average
```

---

## 5. Intelligence Gathering Phase

### Step 5.1: Fetch News Articles
**Action**: Retrieve latest news about the stock
**Duration**: 3-5 seconds
**Applies to**: All stocks (different sources per bot)

**Bot-Specific Sources**:

#### Lite Bot:
- Yahoo Finance News API
- Google News Search
- Total sources: 2

#### AI Bot:
- Yahoo Finance News API
- Google News Search
- 70+ sources via news_aggregator.py
- Total sources: 70+

#### Pro Bot:
- Yahoo Finance News API only
- Total sources: 1 (for speed/reliability)

**API Calls**:
```python
# Lite/Pro version
news_items_yahoo = fetch_yahoo_news(ticker)
news_items_google = fetch_google_news(ticker, company_name)

# AI version
news_text, news_titles = fetch_comprehensive_news(ticker)
```

**Data Retrieved**:
- **Headlines**: News titles
- **Snippets**: Brief descriptions
- **Publish dates**: When published
- **Sources**: Publication names
- **URLs**: Links to full articles

**Sample Output**:
```
News Text: "Reliance Industries announces Q3 earnings with 15% YoY growth.
Company reported revenue of ₹2.3 lakh crore. New retail expansion plans..."

News Titles: [
  "Reliance Q3 Earnings Beat Estimates",
  "RIL announces retail expansion",
  "Reliance shares surge on earnings"
]
```

**Handling No News**:
- If no news found: Set news to None
- Continue processing
- News columns will be empty in Notion

---

### Step 5.2: Analyze News Sentiment
**Action**: Determine sentiment (Positive/Neutral/Negative) from news
**Duration**: 1-3 seconds
**Applies to**: Stocks with news only

**Bot-Specific Methods**:

#### Lite Bot - Keyword Matching:
```python
POSITIVE_KEYWORDS = [
    "wins", "won", "award", "beats", "surges", "jumps",
    "profit", "growth", "dividend", "expansion", "upgrade"
]

NEGATIVE_KEYWORDS = [
    "falls", "drops", "crashes", "loss", "downgrade",
    "debt", "penalty", "lawsuit", "decline"
]

# Count occurrences
pos_count = count_keywords(news_text, POSITIVE_KEYWORDS)
neg_count = count_keywords(news_text, NEGATIVE_KEYWORDS)

# Determine sentiment
if pos_count > neg_count:
    sentiment = "Positive"
    sentiment_score = 0.7
elif neg_count > pos_count:
    sentiment = "Negative"
    sentiment_score = -0.7
else:
    sentiment = "Neutral"
    sentiment_score = 0.0
```

#### AI Bot - FinBERT Model:
```python
from transformers import pipeline

# Initialize model (first run only)
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)

# Analyze each news title
sentiments = []
for title in news_titles:
    result = sentiment_analyzer(title)[0]
    # Result: {'label': 'positive', 'score': 0.95}
    sentiments.append(result)

# Average sentiment
avg_sentiment = calculate_average(sentiments)
# Returns: -1.0 to +1.0
```

#### Pro Bot - Same as Lite:
- Keyword matching method
- Fast and reliable
- No AI model required

**Output**:
- **Sentiment Label**: "Positive", "Neutral", or "Negative"
- **Sentiment Score**: -1.0 to +1.0 (for calculations)

**Example**:
- News: "Company beats earnings, announces dividend"
- Keywords: "beats" (positive), "dividend" (positive)
- Result: "Positive", score = 0.85

---

### Step 5.3: Classify News Type
**Action**: Categorize news into types
**Duration**: Instant
**Applies to**: Stocks with news only
**Method**: Keyword matching (all bots)

**News Type Categories**:
1. **Earnings**: Quarterly results, revenue, profit/loss
2. **Product**: Product launches, releases, unveils
3. **Legal**: Lawsuits, court cases, settlements
4. **M&A**: Mergers, acquisitions, deals, takeovers
5. **Management**: CEO/CFO changes, board appointments
6. **Dividend**: Dividend announcements, payouts
7. **Regulatory**: SEBI, compliance, investigations
8. **Expansion**: New plants, facilities, capacity

**Classification Logic**:
```python
NEWS_TYPE_KEYWORDS = {
    "Earnings": ["earnings", "quarter", "q1", "q2", "revenue", "profit"],
    "Product": ["launch", "product", "unveils", "introduces"],
    "Legal": ["lawsuit", "court", "legal", "settlement"],
    "M&A": ["merger", "acquisition", "deal", "takeover"],
    "Management": ["ceo", "cfo", "resign", "appoint", "director"],
    "Dividend": ["dividend", "payout", "shareholder"],
    "Regulatory": ["sebi", "regulator", "compliance", "probe"],
    "Expansion": ["expansion", "plant", "facility", "invest"]
}

# Classify
news_types = []
for category, keywords in NEWS_TYPE_KEYWORDS.items():
    if any(kw in news_text.lower() for kw in keywords):
        news_types.append(category)

# Limit to 3 types
news_types = news_types[:3]
```

**Example**:
- News: "Reliance announces Q3 earnings, launches new product"
- Keywords found: "earnings" (Earnings), "launches" (Product)
- Result: ["Earnings", "Product"]

**Output**: List of 0-3 news types

---

### Step 5.4: Fetch Analyst Ratings
**Action**: Aggregate professional analyst opinions
**Duration**: 2-4 seconds
**Applies to**: Stocks with data only (skipped for NA stocks)

**Decision Point**: Does stock have data?
- **Yes** → Fetch analyst ratings
- **No** → Skip to calculation phase

**API Call**:
```python
from src.core.analyst_ratings import aggregate_all_analyst_ratings

ratings_data = aggregate_all_analyst_ratings(ticker)
```

**Data Sources** (50+ analysts):

**Global Investment Banks**:
- JP Morgan
- Goldman Sachs
- Morgan Stanley
- Bank of America
- Citi
- Credit Suisse
- Deutsche Bank
- UBS
- Barclays

**Indian Brokerages**:
- Motilal Oswal
- IIFL Securities
- Kotak Securities
- ICICI Direct
- HDFC Securities
- Sharekhan
- Angel Broking

**Rating Agencies**:
- CRISIL
- ICRA
- CARE Ratings
- India Ratings

**Process**:
1. Fetch ratings from Yahoo Finance API
2. Fetch ratings from Indian sources (web scraping/APIs)
3. Normalize all ratings to 1-5 scale
4. Calculate average rating
5. Determine consensus label

**Normalization Examples**:
```
"Strong Buy" → 5.0
"Buy" → 4.0
"Outperform" → 4.5
"Hold" → 3.0
"Underperform" → 2.5
"Sell" → 2.0
"Strong Sell" → 1.0
```

**Output**:
```python
{
    'rating_numeric': 4.35,           # Average rating
    'consensus': 'Strong Buy',        # Consensus label
    'analyst_count': 23,              # Number of analysts
    'has_data': True                  # Data available
}
```

**Consensus Mapping**:
- 4.5-5.0 → "Strong Buy"
- 4.0-4.5 → "Buy"
- 3.5-4.0 → "Moderate Buy"
- 2.5-3.5 → "Hold"
- 2.0-2.5 → "Moderate Sell"
- 1.5-2.0 → "Sell"
- 1.0-1.5 → "Strong Sell"

**Example**:
- 23 analysts covering stock
- Average rating: 4.35/5.0
- Consensus: "Strong Buy"
- Display: "4.35/5.0 (23 analysts)"

---

## 6. Calculation Phase

### Step 6.1: Determine Investment Signal
**Action**: Calculate buy/watch/neutral signal
**Duration**: Instant
**Logic**: Based on momentum and volume surge

**Signal Logic**:
```python
if has_data:
    if momentum > 0.10 and volume_surge > 1.2:
        signal = "🚀 Strong Buy"
    elif momentum > 0.05 or volume_surge > 1.1:
        signal = "👀 Watch"
    else:
        signal = "😴 Neutral"
else:
    signal = "❄️ N/A"
```

**Conditions Explained**:

**🚀 Strong Buy** (Both conditions must be true):
- Momentum > 10% (strong price increase)
- Volume Surge > 1.2x (high trading volume)
- Interpretation: Strong upward trend with institutional interest

**👀 Watch** (Either condition true):
- Momentum > 5% (moderate price increase)
- OR Volume Surge > 1.1x (above average volume)
- Interpretation: Potential opportunity, needs monitoring

**😴 Neutral** (Neither condition met):
- Momentum ≤ 5% AND Volume Surge ≤ 1.1x
- Interpretation: No clear trend, hold or avoid

**❄️ N/A** (No data available):
- Stock has no price data
- Cannot calculate momentum or volume
- Interpretation: Insufficient data for recommendation

**Example**:
- Momentum: 16.99% (> 10% ✓)
- Volume Surge: 1.45x (> 1.2x ✓)
- Result: "🚀 Strong Buy"

---

### Step 6.2: Calculate Investment Score
**Action**: Compute composite numerical score
**Duration**: Instant
**Purpose**: Rank stocks for recommendations

**Score Formula**:
```python
score = 0

# Signal bonus
if signal == "🚀 Strong Buy":
    score += 1000
elif signal == "👀 Watch":
    score += 500
elif signal == "😴 Neutral":
    score += 0
elif signal == "❄️ N/A":
    score += 0

# Momentum contribution
score += momentum * 500

# Volume contribution
score += volume_surge * 50

# Round to 2 decimal places
score = round(score, 2)
```

**Example Calculation**:
- Signal: "🚀 Strong Buy" → +1000
- Momentum: 0.1699 → +84.95 (0.1699 × 500)
- Volume: 1.45 → +72.50 (1.45 × 50)
- **Total Score**: 1157.45

**Score Interpretation**:
- **1200+**: Excellent (Strong Buy + high momentum)
- **800-1200**: Very Good (Strong Buy or high momentum)
- **500-800**: Good (Watch signal)
- **200-500**: Fair (Moderate metrics)
- **0-200**: Weak (Neutral or low metrics)

**Output**: Decimal number (e.g., 1157.45)

---

## 7. Notion Update Phase

### Step 7.1: Build Notion Payload
**Action**: Construct JSON payload for Notion API
**Duration**: Instant

**Payload Structure** (All 16 columns):
```python
payload = {
    "parent": {"database_id": DATABASE_ID},
    "properties": {
        "Ticker": {
            "title": [{"text": {"content": "RELIANCE.NS"}}]
        },
        "Rank": {
            "number": 1
        },
        "Market Cap": {
            "select": {"name": "Large Cap"}
        },
        "Price (₹)": {
            "number": 2456.75
        },
        "Capital Market (₹)": {
            "number": 1664823  # in Crores
        },
        "Sentiment": {
            "number": 0.85
        },
        "Momentum (%)": {
            "number": 0.1699
        },
        "Volume Surge": {
            "number": 1.45
        },
        "Score": {
            "number": 1157.45
        },
        "Signal": {
            "select": {"name": "🚀 Strong Buy"}
        },
        "News & Updates": {
            "rich_text": [{"text": {"content": "Reliance announces..."}}]
        },
        "News Sentiment": {
            "select": {"name": "Positive"}
        },
        "News Type": {
            "multi_select": [
                {"name": "Earnings"},
                {"name": "Product"}
            ]
        },
        "Consensus": {
            "select": {"name": "Strong Buy"}
        },
        "Ratings": {
            "rich_text": [{"text": {"content": "4.35/5.0 (23 analysts)"}}]
        },
        "Last Updated": {
            "date": {"start": "2026-05-19T09:30:00"}
        }
    }
}
```

**Data Validation**:
- Check all required fields present
- Validate data types (number, string, date)
- Truncate text fields if > 2000 chars
- Ensure select values match column options

---

### Step 7.2: Send to Notion API
**Action**: POST request to create/update page
**Duration**: 0.5-1 second
**API Endpoint**: `https://api.notion.com/v1/pages`

**HTTP Request**:
```python
import requests

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://api.notion.com/v1/pages",
    headers=headers,
    json=payload
)
```

**Response Handling**:
- **Status 200**: Success - page created/updated
- **Status 400**: Bad request - data validation error
- **Status 401**: Unauthorized - invalid token
- **Status 404**: Not found - invalid database ID
- **Status 429**: Rate limit - too many requests

---

### Step 7.3: Check Response Status
**Action**: Verify if update was successful
**Duration**: Instant

**Decision Point**: Was the API call successful?

#### Success Path (Status 200):
- Page created or updated in Notion
- Increment success counter
- Log success message
- Continue to next stock

**Log Output**:
```
INFO - ✅ RELIANCE.NS: Successfully updated (Rank: 1, Score: 1157.45, Signal: 🚀 Strong Buy)
```

#### Error Path (Status 4xx/5xx):
- Update failed
- Increment error counter
- Log error details
- Store error message
- Continue to next stock (don't crash)

**Log Output**:
```
ERROR - ❌ RELIANCE.NS: Failed to update - 400 Bad Request: Invalid property value
```

---

### Step 7.4: Write to Log File
**Action**: Record operation in log file
**Duration**: Instant
**Log File**: `logs/market_bot_*.log`

**Log Entry Format**:
```
2026-05-19 09:30:15 - INFO - Stock 1/675: RELIANCE.NS
2026-05-19 09:30:15 - INFO - Price: ₹2456.75, Momentum: 16.99%, Volume: 1.45x
2026-05-19 09:30:15 - INFO - Signal: 🚀 Strong Buy, Score: 1157.45
2026-05-19 09:30:16 - INFO - ✅ Successfully updated in Notion
```

**Log Levels**:
- **INFO**: Normal operations (fetch, calculate, update)
- **WARNING**: Minor issues (no news, missing data)
- **ERROR**: Failures (API errors, invalid data)

---

## 8. Completion Phase

### Step 8.1: Check for More Stocks
**Action**: Determine if iteration should continue
**Duration**: Instant

**Decision Point**: Are there more stocks to process?

**Yes** → Return to Step 2.1 (Next stock)
**No** → Continue to Step 8.2 (Print statistics)

**Loop Counter**:
- Current: idx (1-675)
- Total: 675
- Remaining: 675 - idx

---

### Step 8.2: Print Summary Statistics
**Action**: Display final execution report
**Duration**: Instant

**Statistics Tracked**:
```python
stats = {
    "total": 675,
    "success": 658,           # Successfully updated
    "failed": 17,             # Failed to update
    "with_data": 450,         # Stocks with price data
    "na_stocks": 225,         # Stocks with NA values
    "strong_buy": 87,         # 🚀 Strong Buy signals
    "watch": 203,             # 👀 Watch signals
    "neutral": 160,           # 😴 Neutral signals
    "na_signal": 225,         # ❄️ N/A signals
    "with_news": 620,         # Stocks with news
    "with_ratings": 580,      # Stocks with analyst ratings
    "positive_sentiment": 312, # Positive news
    "negative_sentiment": 98,  # Negative news
    "neutral_sentiment": 210   # Neutral news
}
```

**Console Output**:
```
═══════════════════════════════════════════════════
📊 MARKET BOT EXECUTION SUMMARY
═══════════════════════════════════════════════════

✅ Total Stocks Processed: 675
   ├─ Successfully Updated: 658 (97.5%)
   └─ Failed: 17 (2.5%)

📈 Stock Analysis:
   ├─ With Price Data: 450 (66.7%)
   └─ NA Stocks: 225 (33.3%)

🎯 Investment Signals:
   ├─ 🚀 Strong Buy: 87 (12.9%)
   ├─ 👀 Watch: 203 (30.1%)
   ├─ 😴 Neutral: 160 (23.7%)
   └─ ❄️ N/A: 225 (33.3%)

📰 News Coverage:
   ├─ With News: 620 (91.9%)
   ├─ Positive: 312 (50.3%)
   ├─ Neutral: 210 (33.9%)
   └─ Negative: 98 (15.8%)

⭐ Analyst Ratings:
   └─ With Ratings: 580 (85.9%)

⏱️  Total Execution Time: 8 minutes 34 seconds
📝 Log File: logs/market_bot_lite.log

═══════════════════════════════════════════════════
```

---

### Step 8.3: End Bot Execution
**Action**: Terminate script
**Duration**: Instant

**Final Actions**:
- Close log file
- Release memory
- Exit program
- Return to command prompt

**Exit Code**: 0 (success)

---

## 9. Error Handling

### 9.1: Network Errors
**Scenario**: Internet connection issues, API timeouts

**Handling**:
- Retry up to 3 times with exponential backoff
- If still fails: Log error, skip stock, continue
- Don't crash entire program

**Example**:
```python
try:
    hist = yf.download(ticker, period="6mo")
except Exception as e:
    logger.error(f"Failed to fetch data for {ticker}: {e}")
    # Use NA values
    data = get_default_na_values(ticker, cap_size)
```

---

### 9.2: API Rate Limits
**Scenario**: Too many requests to Notion/Yahoo

**Handling**:
- Sleep between requests (0.5-1 second)
- Respect rate limits (3 requests/sec for Notion)
- Retry with longer delays if hit

---

### 9.3: Data Validation Errors
**Scenario**: Invalid data format, missing fields

**Handling**:
- Validate before sending to Notion
- Use default values for missing data
- Log warnings for invalid data
- Continue processing

---

### 9.4: FinBERT Model Errors (AI Bot)
**Scenario**: Model not downloaded, CUDA errors

**Handling**:
- First run: Download model automatically
- Memory errors: Fall back to CPU
- Model errors: Use keyword sentiment instead

---

## 10. Summary Statistics

### 10.1: Performance Metrics

**Per Stock**:
- Fetch price data: 1-3 seconds
- Fetch news: 3-5 seconds (AI), 1-2 seconds (Lite/Pro)
- Analyst ratings: 2-4 seconds
- Calculations: < 0.1 seconds
- Notion update: 0.5-1 second
- **Total**: 5-10 seconds per stock

**Full Run**:
- Lite Bot: 5-10 minutes (675 stocks)
- AI Bot: 15-20 minutes (first run: 30-45 mins)
- Pro Bot: 5-10 minutes

---

### 10.2: Data Volume

**Per Stock**:
- Price data: ~10 KB
- News data: ~5-20 KB
- Analyst data: ~2 KB
- Total: ~17-32 KB per stock

**Full Run**:
- Total data fetched: ~12-22 MB
- Log file size: ~500 KB - 2 MB
- Notion database: ~100 KB (metadata only)

---

### 10.3: Success Rates

**Typical Results**:
- Data fetch success: 97-99%
- Notion update success: 98-99%
- News fetch success: 90-95%
- Analyst ratings success: 85-90%

---

## Conclusion

This detailed data flow documentation explains every step of processing a single stock through the Market Bot system. The process is:

- ✅ **Systematic**: Follows consistent flow for all stocks
- ✅ **Robust**: Handles errors gracefully
- ✅ **Comprehensive**: Gathers data from multiple sources
- ✅ **Efficient**: Processes 675 stocks in 5-45 minutes
- ✅ **Reliable**: High success rates (>97%)

**For visual representation**, see the Data Flow Diagram in `docs/ARCHITECTURE_DIAGRAMS.md`.

---

**Document Version**: 1.0.0
**Last Updated**: May 19, 2026
**Total Sections**: 10
**Total Steps**: 30+
**Status**: ✅ Complete

**This completes the detailed data flow documentation!**
