# 🎯 Quick Ranking Guide

## What Changed?

Your Market Bot now ranks stocks from **best to worst** based on 9 key metrics!

## Before vs After

### ❌ Before (Simple Serial Ranking)
```
Rank 1: First stock in list
Rank 2: Second stock in list
Rank 3: Third stock in list
```
*No intelligence - just input order*

### ✅ After (Intelligent Multi-Factor Ranking)
```
Rank 1: Best overall stock (highest composite score)
Rank 2: Second-best stock
Rank 3: Third-best stock
```
*Smart ranking based on 9 weighted metrics*

## Ranking Metrics (Quick Reference)

| # | Metric | Weight | What It Measures |
|---|--------|--------|------------------|
| 1 | **Momentum** | 20% | 7-month price change - HIGHEST WEIGHT |
| 2 | **Volume Surge** | 15% | Trading activity vs average |
| 3 | **Sentiment** | 15% | AI/keyword-based market mood |
| 4 | **Investment Score** | 15% | Composite technical score |
| 5 | **Market Cap** | 10% | Company size/stability |
| 6 | **Signal** | 10% | Strong Buy/Watch/Neutral |
| 7 | **News Sentiment** | 8% | Positive/Neutral/Negative news |
| 8 | **Analyst Consensus** | 5% | Professional recommendations |
| 9 | **Analyst Ratings** | 2% | Numeric rating (1-5) |

## How to Use

### 1. Run Your Bot (No Changes Needed!)
```bash
# Pick any version
python src/bots/market_bot_ai.py
# OR
python src/bots/market_bot_pro.py
# OR
python src/bots/market_bot_lite.py
```

### 2. Watch the 3 Phases
```
📊 PHASE 1: Collecting market intelligence...
   [Processing 650 stocks...]

🏆 PHASE 2: Calculating intelligent rankings...
   ✅ Ranked 650 stocks successfully
   Top 3: RELIANCE.NS#1, TCS.NS#2, INFY.NS#3

📤 PHASE 3: Sending ranked data to Notion...
   [Uploading stocks in ranked order...]
```

### 3. Check Notion Database
- Sort by **Rank** column (ascending)
- Rank 1 = Best investment opportunity
- Rank 650 = Lowest ranked stock

## What Makes a Stock Rank High?

✅ **Strong positive momentum** (20% weight - most important!)  
✅ **High volume surge** (active trading)  
✅ **Positive sentiment** (AI + news)  
✅ **High investment score** (technical indicators)  
✅ **Strong Buy signal**  
✅ **Positive news coverage**  
✅ **Strong analyst consensus**  
✅ **High analyst ratings**  
✅ **Large market cap** (stability)

## Example: Top-Ranked Stock

```
Rank: 1
Ticker: RELIANCE.NS
Market Cap: 150,000 Cr ✅
Price: ₹2,450
Momentum: +12% ✅✅ (highest weight!)
Volume Surge: 1.8x ✅
Sentiment: +0.6 ✅
Score: 1,250 ✅
Signal: 🚀 Strong Buy ✅
News Sentiment: Positive ✅
Consensus: Buy ✅
Rating: 4.2/5.0 ✅

Composite Score: 86.2/100
```

## Customize Weights (Optional)

Edit `src/core/ranking_engine.py`:

```python
RANKING_WEIGHTS = {
    'momentum': 0.30,      # Increase to 30% for growth focus
    'market_cap': 0.20,    # Increase to 20% for large-cap bias
    # ... adjust others accordingly
}
```

**Must sum to 1.0 (100%)**

## FAQs

**Q: Do I need to change anything?**  
A: No! It works automatically.

**Q: Can I still use the old ranking?**  
A: The new system is better. If needed, you can sort by other columns in Notion.

**Q: What if a stock has no data?**  
A: It gets a score of 0 and ranks last.

**Q: How is the composite score calculated?**  
A: All metrics are normalized to 0-1, multiplied by their weights, then summed and scaled to 0-100.

**Q: Can I add more metrics?**  
A: Yes! Edit `src/core/ranking_engine.py` and add new factors.

## Top Strategies Using Ranks

### Growth Strategy
Filter: Rank 1-50 + Momentum > 10%

### Value Strategy  
Filter: Rank 1-100 + Market Cap = "Large Cap"

### Momentum Strategy
Filter: Rank 1-30 + Volume Surge > 1.5x

### Conservative Strategy
Filter: Rank 1-25 + Signal = "Strong Buy" + Consensus = "Buy"

## Summary

🎯 **Smart ranking** replaces dumb serial numbering  
📊 **9 weighted metrics** for comprehensive analysis  
🚀 **Zero configuration** - works out of the box  
⚡ **Highly customizable** - adjust weights as needed  
✅ **Thoroughly tested** - all unit tests passing  

**Your Market Bot is now smarter! 🧠**

---

For detailed documentation, see: `docs/RANKING_SYSTEM.md`
