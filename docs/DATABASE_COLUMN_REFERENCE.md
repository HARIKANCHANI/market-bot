# 📊 Market Bot - Database Column Reference

## Complete Guide to All 16 Notion Database Columns

This document provides comprehensive information about each column in the Notion database, including its purpose, data type, format, interactions, and testing procedures.

---

## Table of Contents

1. [Column Overview](#column-overview)
2. [Detailed Column Documentation](#detailed-column-documentation)
3. [Column Interactions](#column-interactions)
4. [Data Flow](#data-flow)
5. [Testing Guide](#testing-guide)
6. [Validation Rules](#validation-rules)

---

## 1. Column Overview

### Summary Table

| # | Column Name | Type | Purpose | Source | Populated By |
|---|-------------|------|---------|--------|--------------|
| 1 | Ticker | Title | Stock symbol | NSE | All bots |
| 2 | Rank | Number | Sequential order | Calculated | All bots |
| 3 | Market Cap | Select | Size classification | NSE indices | All bots |
| 4 | Price (₹) | Number | Current price | yfinance | All bots |
| 5 | Capital Market (₹) | Number | Market cap (Cr) | yfinance | All bots |
| 6 | Sentiment | Number | Sentiment score | AI/Keywords | All bots |
| 7 | Momentum (%) | Number | 6-month return | yfinance | All bots |
| 8 | Volume Surge | Number | Volume ratio | yfinance | All bots |
| 9 | Score | Number | Investment score | Calculated | All bots |
| 10 | Signal | Select | Buy/Watch/NA | Calculated | All bots |
| 11 | News & Updates | Rich Text | Latest news | 70+ sources | All bots |
| 12 | News Sentiment | Select | Pos/Neut/Neg | AI/Keywords | All bots |
| 13 | News Type | Multi-select | Category tags | Keywords | All bots |
| 14 | Consensus | Select | Analyst view | 50+ analysts | All bots |
| 15 | Ratings | Rich Text | Avg rating | 50+ analysts | All bots |
| 16 | Last Updated | Date | Timestamp | System time | All bots |

---

## 2. Detailed Column Documentation

### Column 1: Ticker (Title)

**Type**: Title (Notion primary field)  
**Format**: `<SYMBOL>.NS`  
**Example**: `RELIANCE.NS`, `TCS.NS`, `INFY.NS`

**Purpose**:
- Unique identifier for each stock
- Primary key in Notion database
- Used for all API queries (yfinance, news, ratings)

**Data Source**:
- Static list from `data/nse_stocks_650.py`
- Total: 675 stocks
- Suffix: `.NS` indicates NSE (National Stock Exchange)

**Validation Rules**:
- Must be unique (no duplicates)
- Must end with `.NS`
- Must be valid NSE ticker symbol
- Cannot be empty

**How It's Populated**:
```python
# In all bot versions
payload["properties"]["Ticker"] = {
    "title": [{"text": {"content": data['ticker']}}]
}
```

**Interactions**:
- Used by: All other columns (lookup key)
- Referenced in: yfinance API calls, news searches, rating queries
- Triggers: New page creation in Notion

**Testing**:
```python
# Verify ticker format
assert ticker.endswith(".NS")
assert len(ticker) > 3

# Check uniqueness
tickers = get_all_tickers()
assert len(tickers) == len(set(tickers))
```

**Common Issues**:
- Duplicate tickers: Notion will reject
- Missing `.NS`: yfinance won't find data
- Invalid symbol: Returns NA values

---

### Column 2: Rank (Number)

**Type**: Number  
**Format**: Integer (1-675)  
**Example**: `1`, `2`, `3`, ..., `675`

**Purpose**:
- Sequential numbering for all stocks
- Provides stable ordering
- Helps in pagination and reporting

**Data Source**:
- Generated during iteration (enumerate)
- Range: 1 to 675

**Validation Rules**:
- Must be integer
- Range: 1 to 675
- Should be unique (but not enforced)

**How It's Populated**:
```python
# In all bot versions
for idx, (ticker, cap_size) in enumerate(stocks, 1):
    payload["properties"]["Rank"] = {"number": idx}
```

**Interactions**:
- Used for: Sorting, display order
- Independent of: All other columns
- Stable: Doesn't change unless reordered

**Testing**:
```python
# Verify sequential
ranks = get_all_ranks()
assert ranks == list(range(1, 676))
```

**Common Issues**:
- Gaps in sequence: Re-run fresh_start.py
- Duplicates: Not critical but undesirable

---

### Column 3: Market Cap (Select)

**Type**: Select (dropdown)  
**Options**: `Large Cap`, `Mid Cap`, `Small Cap`  
**Example**: `Large Cap`

**Purpose**:
- Classifies stock size based on market capitalization
- Based on NSE index membership
- Used for filtering and analysis

**Data Source**:
- Pre-classified in `data/nse_stocks_650.py`
- Based on NSE indices:
  - Large Cap: Nifty 150 (150 stocks)
  - Mid Cap: Midcap 200 (200 stocks)
  - Small Cap: Smallcap 300 + extras (325 stocks)

**Validation Rules**:
- Must be one of three options
- Cannot be empty
- Static (doesn't change based on price)

**How It's Populated**:
```python
# In all bot versions
stocks = get_all_stocks_with_classification()
# Returns: [("RELIANCE.NS", "Large Cap"), ...]

payload["properties"]["Market Cap"] = {
    "select": {"name": cap_size}
}
```

**Interactions**:
- Used with: Price analysis, risk assessment
- Correlates with: Liquidity, volatility
- Independent of: Current price

**Distribution**:
- Large Cap: 150 stocks (22.2%)
- Mid Cap: 200 stocks (29.6%)
- Small Cap: 325 stocks (48.1%)

**Testing**:
```python
# Verify distribution
caps = get_all_market_caps()
assert caps.count("Large Cap") == 150
assert caps.count("Mid Cap") == 200
assert caps.count("Small Cap") == 325
```

---

### Column 4: Price (₹) (Number)

**Type**: Number  
**Format**: Decimal (2 decimal places)  
**Unit**: Indian Rupees (₹)  
**Example**: `2456.75`, `3421.30`, `None` (for NA stocks)

**Purpose**:
- Current stock price
- Used for momentum calculation
- Key metric for investment decisions

**Data Source**:
- yfinance API
- Real-time or last available price
- Returns `None` for delisted/no-data stocks

**Validation Rules**:
- Must be positive number or None
- Decimals: 2 places
- Reasonable range: 1 to 100,000 (typical NSE range)

**How It's Populated**:
```python
# In all bot versions
hist = yf.download(symbol, period="6mo", progress=False)
latest_price = float(hist['Close'].iloc[-1])

payload["properties"]["Price (₹)"] = {
    "number": round(latest_price, 2)
}
```

**Interactions**:
- Used for: Momentum calculation, scoring
- Drives: Signal generation
- Updates: Daily/Weekly/Monthly (depends on bot)

**Testing**:
```python
# Verify price sanity
price = get_price("RELIANCE.NS")
assert price is None or (1 <= price <= 100000)
assert price is None or round(price, 2) == price
```

**Common Issues**:
- Price = None: Stock delisted or no data
- Stale price: yfinance data delay
- Extreme prices: Check for stock split

---

### Column 5: Capital Market (₹) (Number)

**Type**: Number  
**Format**: Integer (in Crores)  
**Unit**: Crores (1 Crore = 10 Million)  
**Example**: `1664823` (₹16.64 Lakh Crores), `None`

**Purpose**:
- Market capitalization in Crores
- Actual numerical value (not just classification)
- Used for detailed analysis and sorting

**Data Source**:
- yfinance API (`info['marketCap']`)
- Converted from USD/Rs to Crores
- Returns `None` for NA stocks

**Validation Rules**:
- Must be positive integer or None
- Unit: Crores (divided by 10,000,000)
- Typical range: 100 to 20,00,000 Crores

**How It's Populated**:
```python
# In all bot versions
info = yf.Ticker(symbol).info
market_cap_inr = info.get('marketCap', 0)
market_cap_crores = int(market_cap_inr / 10000000)  # Convert to Crores

payload["properties"]["Capital Market (₹)"] = {
    "number": market_cap_crores
}
```

**Interactions**:
- Complements: Market Cap (classification)
- Used for: Precise sorting, filtering
- Correlates with: Liquidity, stability

**Testing**:
```python
# Verify market cap
cap = get_market_cap("RELIANCE.NS")
assert cap is None or cap > 0
assert cap is None or isinstance(cap, int)
```

---

### Column 6: Sentiment (Number)

**Type**: Number  
**Format**: Decimal (-1.0 to +1.0)  
**Example**: `0.85` (very positive), `-0.32` (negative), `0.0` (neutral/NA)

**Purpose**:
- Overall sentiment score
- Varies by bot version:
  - **Lite**: Technical (price trend)
  - **AI**: FinBERT AI model
  - **Pro**: Keyword-based

**Data Source**:
- **Lite Bot**: Price momentum (positive = bullish)
- **AI Bot**: FinBERT model on news
- **Pro Bot**: Keyword matching

**Validation Rules**:
- Range: -1.0 to +1.0
- Default: 0.0 (for NA stocks)
- Precision: 4 decimal places

**How It's Populated**:
```python
# Lite version (technical)
sentiment = momentum if momentum > 0 else momentum * 0.5

# AI version (FinBERT)
sentiment = analyze_ai_sentiment(news_titles)

# Pro version (keywords)
sentiment_label = analyze_news_sentiment(news_text)
# Converted to numeric

payload["properties"]["Sentiment"] = {
    "number": round(sentiment, 4)
}
```

**Interactions**:
- Used for: Score calculation, Signal
- Driven by: News, price action
- Updates: With each bot run

**Sentiment Scale**:
- `0.7 to 1.0`: Very Positive
- `0.3 to 0.7`: Positive
- `-0.3 to 0.3`: Neutral
- `-0.7 to -0.3`: Negative
- `-1.0 to -0.7`: Very Negative

**Testing**:
```python
# Verify range
sentiment = get_sentiment("RELIANCE.NS")
assert -1.0 <= sentiment <= 1.0
```

---

### Column 7: Momentum (%) (Number)

**Type**: Number  
**Format**: Decimal (4 decimal places)  
**Displayed As**: Percentage (multiply by 100)  
**Example**: `0.1543` (15.43% return), `-0.0823` (-8.23% decline)

**Purpose**:
- 6-month price return (momentum indicator)
- Key metric for identifying trends
- Used in score calculation

**Data Source**:
- yfinance historical data (6 months)
- Calculated: (current_price - 6mo_price) / 6mo_price
- Returns `0.0` for NA stocks

**Validation Rules**:
- Typical range: -0.5 to +2.0 (-50% to +200%)
- Default: 0.0 (no data)
- Extreme values possible (volatile stocks)

**How It's Populated**:
```python
# In all bot versions
hist = yf.download(symbol, period="6mo", progress=False)
momentum = (hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]

payload["properties"]["Momentum (%)"] = {
    "number": round(momentum, 4)
}
```

**Interactions**:
- Drives: Signal ("Strong Buy" if > 10%)
- Used in: Score calculation
- Correlates with: Sentiment, Volume Surge

**Testing**:
```python
# Verify calculation
momentum = get_momentum("RELIANCE.NS")
assert -1.0 <= momentum <= 5.0  # Sanity check
```

---

### Column 8: Volume Surge (Number)

**Type**: Number
**Format**: Decimal (2 decimal places)
**Example**: `1.45` (45% above average), `0.87` (13% below average)

**Purpose**:
- Measures current volume vs 20-day average
- Indicates unusual trading activity
- Key indicator for momentum trades

**Data Source**:
- yfinance historical volume data
- Calculated: current_volume / avg_20day_volume
- Returns `0.0` for NA stocks

**Validation Rules**:
- Must be positive or 0
- Typical range: 0.5 to 3.0
- Extreme values possible (news-driven spikes)

**How It's Populated**:
```python
# In all bot versions
hist = yf.download(symbol, period="6mo", progress=False)
recent_volume = hist['Volume'].iloc[-1]
avg_volume = hist['Volume'].tail(20).mean()
vol_surge = recent_volume / avg_volume if avg_volume > 0 else 0

payload["properties"]["Volume Surge"] = {
    "number": round(vol_surge, 2)
}
```

**Interactions**:
- Drives: Signal ("Strong Buy" if > 1.2)
- Used in: Score calculation
- Indicates: Institutional interest, news impact

**Interpretation**:
- `> 2.0`: Very high volume (investigate)
- `1.2 - 2.0`: High volume (positive signal)
- `0.8 - 1.2`: Normal volume
- `< 0.8`: Low volume (caution)

**Testing**:
```python
# Verify range
vol_surge = get_volume_surge("RELIANCE.NS")
assert vol_surge >= 0
```

---

### Column 9: Score (Number)

**Type**: Number
**Format**: Decimal (2 decimal places)
**Range**: 0 to 1500+ (no upper limit)
**Example**: `1245.50`, `523.25`, `0.0`

**Purpose**:
- Composite investment score
- Combines momentum, volume, signal
- Used for ranking stocks

**Data Source**:
- Calculated from other columns
- Formula varies by bot version
- Returns `0.0` for NA stocks

**Calculation**:
```python
def calculate_score(momentum, volume_surge, signal):
    score = 0

    # Signal bonus
    if signal == "🚀 Strong Buy":
        score += 1000
    elif signal == "👀 Watch":
        score += 500

    # Momentum contribution
    score += momentum * 500

    # Volume contribution
    score += volume_surge * 50

    return round(score, 2)
```

**Validation Rules**:
- Must be non-negative
- Decimals: 2 places
- No upper limit

**How It's Populated**:
```python
# In all bot versions
score = calculate_score(data['momentum'], data['volume_surge'], signal)

payload["properties"]["Score"] = {
    "number": score
}
```

**Interactions**:
- Driven by: Momentum, Volume, Signal
- Used for: Sorting top recommendations
- Independent of: News, analyst ratings

**Score Ranges**:
- `1200+`: Excellent (Strong Buy with high momentum)
- `800-1200`: Very Good (Strong Buy or high momentum)
- `500-800`: Good (Watch signal)
- `0-500`: Neutral/Weak

**Testing**:
```python
# Verify score calculation
score = calculate_score(0.15, 1.5, "🚀 Strong Buy")
assert 1000 <= score <= 1200
```

---

### Column 10: Signal (Select)

**Type**: Select (dropdown)
**Options**: `🚀 Strong Buy`, `👀 Watch`, `😴 Neutral`, `❄️ N/A`
**Example**: `🚀 Strong Buy`

**Purpose**:
- Investment recommendation
- Based on momentum and volume
- Clear action signal for traders

**Data Source**:
- Calculated from Momentum + Volume Surge
- Logic-based determination
- "❄️ N/A" for stocks without data

**Signal Logic**:
```python
def determine_signal(momentum, volume_surge, has_data):
    if not has_data:
        return "❄️ N/A"

    if momentum > 0.10 and volume_surge > 1.2:
        return "🚀 Strong Buy"
    elif momentum > 0.05 or volume_surge > 1.1:
        return "👀 Watch"
    else:
        return "😴 Neutral"
```

**Validation Rules**:
- Must be one of 4 options
- Cannot be empty
- Driven by logic, not manual

**How It's Populated**:
```python
# In all bot versions
signal = determine_signal(momentum, vol_surge, has_data)

payload["properties"]["Signal"] = {
    "select": {"name": signal}
}
```

**Interactions**:
- Drives: Score calculation
- Driven by: Momentum, Volume Surge
- Used for: Quick filtering, alerts

**Signal Distribution** (typical):
- 🚀 Strong Buy: ~10-15% of stocks
- 👀 Watch: ~25-30% of stocks
- 😴 Neutral: ~35-40% of stocks
- ❄️ N/A: ~20-30% of stocks

**Testing**:
```python
# Verify signal logic
signal = determine_signal(0.15, 1.5, True)
assert signal == "🚀 Strong Buy"

signal = determine_signal(0.02, 0.8, True)
assert signal == "😴 Neutral"
```

---

### Column 11: News & Updates (Rich Text)

**Type**: Rich Text
**Format**: Plain text (max 2000 characters)
**Example**: "Reliance announces Q3 earnings with 15% YoY growth..."

**Purpose**:
- Latest news summary
- Aggregated from 70+ sources
- Context for sentiment and signals

**Data Source**:
- Yahoo Finance news
- Google News search
- 70+ sources (if using news_aggregator.py)
- Returns `None` for NA stocks or no news

**Validation Rules**:
- Max length: 2000 characters (Notion limit)
- Can be empty/None
- Plain text only (no HTML)

**How It's Populated**:
```python
# Lite version
news_text = fetch_news(ticker)  # Yahoo + Google

# AI version
news_text, news_titles = fetch_comprehensive_news(ticker)  # 70+ sources

# Truncate if needed
if news_text:
    news_text = news_text[:2000]

payload["properties"]["News & Updates"] = {
    "rich_text": [{"text": {"content": news_text}}]
}
```

**Interactions**:
- Drives: News Sentiment, News Type
- Used for: Sentiment analysis (AI version)
- Updates: With each bot run

**Testing**:
```python
# Verify news length
news = get_news("RELIANCE.NS")
assert news is None or len(news) <= 2000
```

**Common Issues**:
- No news found: Normal for small caps
- Truncated: 2000 char limit
- Old news: yfinance data lag

---

### Column 12: News Sentiment (Select)

**Type**: Select (dropdown)
**Options**: `Positive`, `Neutral`, `Negative`
**Example**: `Positive`

**Purpose**:
- Categorized news sentiment
- Complements numeric Sentiment column
- Easy filtering and visualization

**Data Source**:
- **Lite/Pro**: Keyword matching
- **AI**: FinBERT analysis fallback
- Based on News & Updates content

**Validation Rules**:
- Must be one of 3 options
- Can be empty (no news)
- Independent of numeric Sentiment

**How It's Populated**:
```python
# Keyword-based (Lite/Pro)
def get_news_sentiment_label(news_text):
    if not news_text:
        return None

    pos_count = sum(1 for word in POSITIVE_KEYWORDS if word in news_text.lower())
    neg_count = sum(1 for word in NEGATIVE_KEYWORDS if word in news_text.lower())

    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    return "Neutral"

news_sentiment = get_news_sentiment_label(news_text)

if news_sentiment:
    payload["properties"]["News Sentiment"] = {
        "select": {"name": news_sentiment}
    }
```

**Keywords**:
- **Positive**: wins, award, beats, surges, profit, growth, dividend, expansion
- **Negative**: falls, drops, loss, downgrade, debt, penalty, resignation

**Interactions**:
- Driven by: News & Updates
- Complements: Sentiment (number)
- Used for: Quick filtering

**Testing**:
```python
# Test keyword logic
sentiment = get_news_sentiment_label("Company beats earnings estimates")
assert sentiment == "Positive"
```

---

### Column 13: News Type (Multi-select)

**Type**: Multi-select (multiple tags)
**Options**: `Earnings`, `Product`, `Legal`, `M&A`, `Management`, `Dividend`, `Regulatory`, `Expansion`
**Example**: `[Earnings, Product]`

**Purpose**:
- Categorize news by type
- Enable filtering by news category
- Identify specific events

**Data Source**:
- Keyword-based classification
- Analyzes News & Updates content
- Returns empty list if no news

**Classification Keywords**:
```python
NEWS_TYPE_KEYWORDS = {
    "Earnings": ["earnings", "quarter", "q1", "q2", "q3", "q4", "revenue", "profit", "loss", "results"],
    "Product": ["launch", "product", "unveils", "introduces", "release", "model", "variant"],
    "Legal": ["lawsuit", "court", "legal", "case", "trial", "settlement", "penalty", "fine"],
    "M&A": ["merger", "acquisition", "acquires", "deal", "buyout", "takeover", "stake"],
    "Management": ["ceo", "cfo", "resign", "appoint", "director", "board", "executive"],
    "Dividend": ["dividend", "payout", "shareholder", "distribution"],
    "Regulatory": ["sebi", "regulator", "compliance", "violation", "probe", "investigation"],
    "Expansion": ["expansion", "plant", "facility", "capacity", "invest", "capex"]
}
```

**How It's Populated**:
```python
def classify_news_type(news_text):
    if not news_text:
        return []

    news_lower = news_text.lower()
    types = []

    for news_type, keywords in NEWS_TYPE_KEYWORDS.items():
        if any(keyword in news_lower for keyword in keywords):
            types.append(news_type)

    return list(set(types))[:3]  # Max 3 types

news_types = classify_news_type(news_text)

if news_types:
    payload["properties"]["News Type"] = {
        "multi_select": [{"name": t} for t in news_types]
    }
```

**Validation Rules**:
- Can have 0-3 types
- Each type must be from predefined list
- Duplicates removed

**Interactions**:
- Driven by: News & Updates
- Independent of: Other columns
- Used for: Filtering specific event types

**Testing**:
```python
# Test classification
types = classify_news_type("Company announces Q1 earnings, launches new product")
assert "Earnings" in types
assert "Product" in types
assert len(types) <= 3
```

---

### Column 14: Consensus (Select)

**Type**: Select (dropdown)
**Options**: `Strong Buy`, `Buy`, `Moderate Buy`, `Hold`, `Moderate Sell`, `Sell`, `Strong Sell`, `No Consensus`
**Example**: `Strong Buy`

**Purpose**:
- Aggregate analyst opinion
- Professional investment guidance
- Based on 50+ analyst ratings

**Data Source**:
- analyst_ratings.py module
- 50+ analysts/agencies
- Normalized to 1-5 scale, then categorized

**Consensus Mapping**:
```python
def calculate_consensus(avg_rating):
    if avg_rating >= 4.5:
        return "Strong Buy"
    elif avg_rating >= 4.0:
        return "Buy"
    elif avg_rating >= 3.5:
        return "Moderate Buy"
    elif avg_rating >= 2.5:
        return "Hold"
    elif avg_rating >= 2.0:
        return "Moderate Sell"
    elif avg_rating >= 1.5:
        return "Sell"
    else:
        return "Strong Sell"
```

**How It's Populated**:
```python
# In all bot versions (if has_data)
from src.core.analyst_ratings import aggregate_all_analyst_ratings

ratings_data = aggregate_all_analyst_ratings(ticker)

if ratings_data['has_data']:
    payload["properties"]["Consensus"] = {
        "select": {"name": ratings_data['consensus']}
    }
```

**Validation Rules**:
- Must be one of 8 options
- Can be empty (no ratings available)
- Skipped for NA stocks

**Interactions**:
- Complements: Ratings column
- Independent of: Technical signals
- Used for: Professional validation

**Testing**:
```python
# Test consensus
ratings = aggregate_all_analyst_ratings("RELIANCE.NS")
assert ratings['consensus'] in ["Strong Buy", "Buy", "Moderate Buy", "Hold",
                                "Moderate Sell", "Sell", "Strong Sell", "No Consensus"]
```

---

### Column 15: Ratings (Rich Text)

**Type**: Rich Text
**Format**: "X.XX/5.0 (N analysts)"
**Example**: "4.35/5.0 (23 analysts)", "No ratings available"

**Purpose**:
- Numeric analyst rating with source count
- Transparency on rating strength
- Complements Consensus text

**Data Source**:
- analyst_ratings.py module
- Average of all analyst ratings
- Count of analysts providing ratings

**Validation Rules**:
- Rating: 1.00 to 5.00
- Analysts: Integer count
- Format strictly: "X.XX/5.0 (N analysts)"

**How It's Populated**:
```python
# In all bot versions (if has_data)
ratings_data = aggregate_all_analyst_ratings(ticker)

if ratings_data['has_data']:
    rating_text = f"{ratings_data['rating_numeric']:.2f}/5.0 ({ratings_data['analyst_count']} analysts)"

    payload["properties"]["Ratings"] = {
        "rich_text": [{"text": {"content": rating_text}}]
    }
```

**Interactions**:
- Driven by: Same source as Consensus
- Complements: Consensus column
- Provides: Transparency (analyst count)

**Testing**:
```python
# Verify format
rating_text = get_ratings("RELIANCE.NS")
assert "/5.0" in rating_text
assert "analysts)" in rating_text
```

---

### Column 16: Last Updated (Date)

**Type**: Date
**Format**: ISO 8601 (YYYY-MM-DDTHH:MM:SS)
**Example**: "2026-05-19T09:30:00"

**Purpose**:
- Timestamp of last update
- Data freshness indicator
- Audit trail

**Data Source**:
- System time at moment of update
- UTC or local timezone
- Auto-generated

**Validation Rules**:
- Must be valid ISO 8601 date
- Typically current date/time
- Updated with each bot run

**How It's Populated**:
```python
# In all bot versions
from datetime import datetime

payload["properties"]["Last Updated"] = {
    "date": {"start": datetime.now().isoformat()}
}
```

**Interactions**:
- Independent of: All data columns
- Used for: Determining stale data
- Updates: Every bot run

**Testing**:
```python
# Verify timestamp
last_updated = get_last_updated("RELIANCE.NS")
assert isinstance(last_updated, datetime)
```

---

## 3. Column Interactions

### Primary Interactions

**Price → Momentum → Signal → Score**:
```
Price (6mo history)
  ↓
Momentum (calculated)
  ↓
Signal (Strong Buy/Watch/Neutral)
  ↓
Score (composite)
```

**News → Sentiment & Type**:
```
News & Updates (text)
  ↓
News Sentiment (Positive/Neutral/Negative)
News Type (Earnings/Product/etc.)
```

**Analyst Data → Consensus & Ratings**:
```
50+ Analyst Sources
  ↓
Ratings (numeric + count)
Consensus (categorical)
```

### Independence

- **Ticker**: Independent (primary key)
- **Rank**: Independent (sequential)
- **Market Cap**: Independent (static classification)
- **Last Updated**: Independent (timestamp)

### Derived Columns

- **Momentum**: From Price history
- **Volume Surge**: From Volume history
- **Signal**: From Momentum + Volume Surge
- **Score**: From Signal + Momentum + Volume Surge
- **News Sentiment**: From News & Updates
- **News Type**: From News & Updates
- **Consensus**: From Ratings
- **Ratings**: From 50+ analyst sources

---

## 4. Data Flow

### Complete Update Flow

```
1. Load Stock List (data/nse_stocks_650.py)
   ↓
2. For each stock:
   a. Fetch Price Data (yfinance)
   b. Calculate Momentum
   c. Calculate Volume Surge
   d. Fetch News (70+ sources)
   e. Analyze News Sentiment
   f. Classify News Type
   g. Fetch Analyst Ratings
   h. Determine Signal
   i. Calculate Score
   j. Generate Timestamp
   ↓
3. Send to Notion (all 16 columns)
   ↓
4. Log Success/Failure
```

---

## 5. Testing Guide

### Column Validation Tests

```python
# Test all columns populated
def test_all_columns():
    page = get_notion_page("RELIANCE.NS")
    required_columns = [
        "Ticker", "Rank", "Market Cap", "Price (₹)", "Capital Market (₹)",
        "Sentiment", "Momentum (%)", "Volume Surge", "Score", "Signal",
        "News & Updates", "News Sentiment", "News Type", "Consensus",
        "Ratings", "Last Updated"
    ]
    for col in required_columns:
        assert col in page['properties']

# Test data types
def test_data_types():
    page = get_notion_page("RELIANCE.NS")
    assert isinstance(page['properties']['Price (₹)']['number'], float)
    assert isinstance(page['properties']['Rank']['number'], int)
    assert isinstance(page['properties']['News Type']['multi_select'], list)

# Test ranges
def test_value_ranges():
    page = get_notion_page("RELIANCE.NS")
    sentiment = page['properties']['Sentiment']['number']
    assert -1.0 <= sentiment <= 1.0
```

---

## 6. Validation Rules Summary

| Column | Type | Required | Range/Format | Default |
|--------|------|----------|--------------|---------|
| Ticker | Title | Yes | `*.NS` | - |
| Rank | Number | Yes | 1-675 | - |
| Market Cap | Select | Yes | 3 options | - |
| Price (₹) | Number | No | > 0 | None |
| Capital Market (₹) | Number | No | > 0 | None |
| Sentiment | Number | Yes | -1.0 to 1.0 | 0.0 |
| Momentum (%) | Number | Yes | -1.0 to 5.0 | 0.0 |
| Volume Surge | Number | Yes | ≥ 0 | 0.0 |
| Score | Number | Yes | ≥ 0 | 0.0 |
| Signal | Select | Yes | 4 options | ❄️ N/A |
| News & Updates | Rich Text | No | ≤ 2000 chars | None |
| News Sentiment | Select | No | 3 options | None |
| News Type | Multi-select | No | 0-3 tags | [] |
| Consensus | Select | No | 8 options | None |
| Ratings | Rich Text | No | Format | None |
| Last Updated | Date | Yes | ISO 8601 | Now |

---

## Conclusion

This comprehensive column reference documents all 16 database columns, their purposes, interactions, and testing procedures. Each column is critical to the Market Bot system's ability to provide enterprise-grade stock market intelligence.

**For additional help**:
- Technical details: See `TECHNICAL_DOCUMENTATION.md`
- Project overview: See `COMPREHENSIVE_FINAL_REPORT.md`
- Quick start: See `QUICK_START.md`

---

**Last Updated**: May 19, 2026
**Version**: 1.0.0
**Status**: ✅ Complete & Production Ready
