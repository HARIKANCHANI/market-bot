# 🏆 Intelligent Multi-Factor Ranking System

## Overview

The Market Bot now includes an **intelligent multi-factor ranking system** that ranks stocks based on a comprehensive analysis of 9 key metrics. This replaces the simple serial ranking with a sophisticated weighted scoring algorithm.

## Ranking Metrics

The system evaluates stocks based on the following factors:

### 1. **Market Cap** (10% weight)
- Raw market capitalization in crores
- Higher market cap = better stability
- Normalized across all stocks

### 2. **Momentum** (20% weight) ⚡
- Price change over 7-month period
- Percentage change: (Current Price - Starting Price) / Starting Price
- **Highest weight** - critical for identifying growth stocks

### 3. **Volume Surge** (15% weight) 📊
- Current volume vs 20-day average volume
- Indicates increased trading interest
- Volume > 1.5x average = strong interest

### 4. **Sentiment** (15% weight) 🎭
- AI-powered (FinBERT) or keyword-based sentiment
- Range: -1 (very negative) to +1 (very positive)
- Reflects market mood and news impact

### 5. **Investment Score** (15% weight) 💯
- Composite score calculated from:
  - Signal type (Strong Buy = 1000, Watch = 500)
  - Momentum contribution (×500)
  - Volume surge contribution (×50)

### 6. **Signal** (10% weight) 🚀
- Trading signal classification:
  - 🚀 Strong Buy = 1.0
  - 👀 Watch = 0.6
  - ❄️ Neutral = 0.3
  - ❄️ N/A = 0.0

### 7. **News Sentiment** (8% weight) 📰
- Keyword-based news analysis:
  - Positive = 1.0
  - Neutral = 0.5
  - Negative = 0.0

### 8. **Analyst Consensus** (5% weight) 👔
- Professional analyst recommendations:
  - Strong Buy = 1.0
  - Buy = 0.8
  - Moderate Buy = 0.7
  - Hold = 0.5
  - Moderate Sell = 0.3
  - Sell = 0.2
  - Strong Sell = 0.0

### 9. **Analyst Ratings** (2% weight) ⭐
- Numeric rating (1-5 scale)
- Average of all analyst ratings
- Normalized across all stocks

## How It Works

### Phase 1: Data Collection
1. Fetch market data for all stocks
2. Calculate technical indicators (momentum, volume surge)
3. Fetch news and analyze sentiment
4. Fetch analyst ratings and consensus
5. Calculate investment score and signal

### Phase 2: Intelligent Ranking
1. Normalize all metrics to 0-1 scale
2. Apply weights to each metric
3. Calculate composite score (0-100)
4. Sort stocks by composite score (descending)
5. Assign ranks (1 = best, highest score)

### Phase 3: Notion Upload
1. Send stocks to Notion database in ranked order
2. Include rank number in each entry
3. Preserve all original metrics

## Formula

```
Composite Score = 
  (Market Cap × 0.10) +
  (Momentum × 0.20) +
  (Volume Surge × 0.15) +
  (Sentiment × 0.15) +
  (Investment Score × 0.15) +
  (Signal × 0.10) +
  (News Sentiment × 0.08) +
  (Consensus × 0.05) +
  (Ratings × 0.02)
```

Final score is scaled to 0-100 for easier interpretation.

## Benefits

### 1. **Comprehensive Analysis**
- Considers multiple factors simultaneously
- Not biased by single metric

### 2. **Balanced Weighting**
- Technical metrics (momentum, volume) = 35%
- Sentiment metrics (AI, news) = 23%
- Score & signal = 25%
- Analyst opinions = 7%
- Market cap = 10%

### 3. **Adaptable**
- Weights can be adjusted in `src/core/ranking_engine.py`
- Easy to add new metrics

### 4. **Transparent**
- Each stock shows its rank
- Composite score is logged
- All underlying metrics preserved

## Usage

The ranking system is **automatically enabled** in all bot versions:
- `market_bot_ai.py` - AI Sentiment version
- `market_bot_pro.py` - Professional version
- `market_bot_lite.py` - Lightweight version

No configuration needed - just run the bot normally!

## Customization

To adjust ranking weights, edit `src/core/ranking_engine.py`:

```python
RANKING_WEIGHTS = {
    'market_cap': 0.10,      # Adjust this
    'momentum': 0.20,         # Adjust this
    'volume_surge': 0.15,     # etc.
    # ...
}
```

**Note**: Weights should sum to 1.0 for balanced scoring.

## Example Output

```
🏆 PHASE 2: Calculating intelligent rankings...
✅ Ranked 650 stocks successfully
   Top 3: RELIANCE.NS#1, TCS.NS#2, INFY.NS#3
```

Each stock in Notion will show:
- **Rank**: 1-650 (lower is better)
- All original metrics preserved
- Sorted by rank for easy filtering
