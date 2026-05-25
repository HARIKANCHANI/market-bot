# 🚀 Quick Start Guide - Market Intelligence Bot

## 📋 **WHAT TO RUN AND IN WHAT ORDER**

---

## 🎯 **FIRST TIME SETUP** (Run Once)

### **Step 1: Add Analyst Columns to Database** ⭐ NEW

```bash
python add-analyst-ratings-columns.py
```

**What it does**:
- ✅ Adds "Consensus" column (Select: Strong Buy to Strong Sell)
- ✅ Adds "Ratings" column (Rich Text: X.XX/5.0)
- ✅ Fetches analyst ratings for all existing stocks
- ✅ Updates database with ratings

**Time**: ~15-30 minutes (for existing ~400 stocks)

**Output**:
```
✅ Successfully added analyst columns!
📊 Populating Analyst Ratings for All Stocks
[1/412] 🔍 RELIANCE... ✅ Strong Buy | 4.35/5.0 (23 analysts)
[2/412] 🔍 TCS... ✅ Buy | 4.12/5.0 (18 analysts)
...
```

---

### **Step 2: Load All Missing Stocks** ⭐ REQUIRED

```bash
python load-missing-stocks.py
```

**What it does**:
- ✅ Loads ALL 675 stocks (no skipping)
- ✅ Stocks with data → Full analysis
- ✅ Stocks without data → NA values
- ✅ Includes analyst ratings
- ✅ Includes market cap in Crores

**Time**: ~20-30 minutes (for ~260 missing stocks)

**Output**:
```
🔄 Loading Missing Stocks with NA Support
✅ Found 412 existing stocks
📊 Need to load 263 missing stocks

[1/263] 🔍 TATAMOTORS...
   ✅ Data found → Full analysis
   📊 Fetching analyst ratings...
   ✅ Ratings: Buy | 4.15/5.0 (12 analysts)
   ✅ Added to database (Rank: 413)

[2/263] ⚠️  POLYCA...
   ⚠️  No data → NA values
   ✅ Added to database (Rank: 414)
...
```

---

## 🔄 **REGULAR UPDATES** (Run Daily/Weekly)

### **Option 1: Lightweight Bot** (Recommended - Fast!)

```bash
python src/bots/market_bot_lite.py
```

**Features**:
- ✅ Technical analysis (momentum + volume)
- ✅ NA handling
- ✅ Analyst ratings integration
- ✅ No AI model download needed
- ⚡ **FAST** - Runs instantly

**Time**: ~15-20 minutes

**Best for**: Daily/frequent updates

---

### **Option 2: Standard Bot** (With AI Sentiment)

```bash
python src/bots/market_bot_ai.py
```

**Features**:
- ✅ All features of Lite version
- ✅ **AI sentiment analysis** (FinBERT)
- ✅ More accurate sentiment scoring
- ⏱️ First run downloads FinBERT model (~1GB)

**Time**: ~25-35 minutes

**Best for**: Weekly in-depth analysis

---

### **Option 3: Pro Bot** (Maximum Features)

```bash
python src/bots/market_bot_pro.py
```

**Features**:
- ✅ All features of Standard version
- ✅ Advanced technical indicators
- ✅ Multi-timeframe analysis
- ✅ Enhanced scoring

**Time**: ~30-40 minutes

**Best for**: Weekly/monthly comprehensive analysis

---

## 📊 **WHAT EACH SCRIPT DOES**

### **scripts/setup/add_analyst_columns.py**
- Purpose: One-time setup for analyst ratings
- Frequency: Run once (or when adding new stocks)
- Updates: Consensus + Ratings columns

### **scripts/maintenance/load_missing_stocks.py**
- Purpose: Complete database with all 675 stocks
- Frequency: Run once, then when new stocks are added
- Updates: All columns including analyst ratings

### **src/bots/market_bot_lite.py**
- Purpose: Fast daily updates
- Frequency: Daily
- Updates: Price, momentum, volume, signal, score, timestamp

### **src/bots/market_bot_ai.py**
- Purpose: AI-powered weekly updates
- Frequency: Weekly
- Updates: All columns + AI sentiment

### **src/bots/market_bot_pro.py**
- Purpose: Comprehensive monthly updates
- Frequency: Monthly
- Updates: All columns + advanced analysis

---

## 🎯 **RECOMMENDED WORKFLOW**

### **Initial Setup** (Do Once):
1. ✅ Run `add-analyst-ratings-columns.py` - Adds new columns
2. ✅ Run `load-missing-stocks.py` - Complete 675 stock coverage
3. ✅ Verify in Notion - Check all columns exist

### **Daily Updates**:
```bash
python src/bots/market_bot_lite.py
```
- Updates prices, signals, scores
- Fast and efficient
- No model downloads

### **Weekly Deep Dive**:
```bash
python src/bots/market_bot_ai.py
```
- AI sentiment analysis
- News updates (70+ sources)
- Analyst ratings refresh

### **Monthly Review**:
```bash
python src/bots/market_bot_pro.py
```
- Full comprehensive analysis
- Advanced indicators
- Strategic decisions

---

## 📈 **EXPECTED RESULTS**

### **After Initial Setup**:
- **Total Stocks**: 675 (complete NSE coverage)
- **With Full Data**: ~420-450 (actively traded)
- **With NA Values**: ~225-255 (delisted/low liquidity)
- **Columns**: 16 total
- **Analyst Coverage**: 50+ analysts per stock

### **After Daily Updates**:
- **Updated**: Price, Momentum, Volume, Signal, Score
- **Time**: ~15-20 minutes
- **Frequency**: Daily (or as needed)

### **After Weekly Updates**:
- **Updated**: All columns + AI sentiment + news
- **Time**: ~25-35 minutes
- **Frequency**: Weekly

---

## 🔍 **TROUBLESHOOTING**

### **Problem**: "Notion API error 400"
**Solution**: Check if all columns exist in database. Run `add-analyst-ratings-columns.py` first.

### **Problem**: "Module not found: analyst_ratings_aggregator"
**Solution**: Make sure `analyst_ratings_aggregator.py` is in the same folder.

### **Problem**: "No analyst data found"
**Solution**: Normal for some stocks. System will add "No Consensus" + "N/A" rating.

### **Problem**: "Rate limit exceeded"
**Solution**: Script has built-in delays. If it happens, wait 1 minute and resume.

### **Problem**: "Stock skipped - no data"
**Solution**: Not an error! Stock will be added with NA values (check ❄️ N/A signal).

---

## 💡 **PRO TIPS**

1. **Run analyst ratings update monthly**: Ratings change frequently
   ```bash
   python add-analyst-ratings-columns.py
   ```

2. **Check stock count**:
   ```bash
   python check-stock-count.py
   ```

3. **View comprehensive news sources**:
   - Open `comprehensive_news_sources.py`
   - Check the summary at the end (70+ sources listed)

4. **Understand ratings scale**:
   - 5.0 = Strong Buy (highest)
   - 4.0 = Buy
   - 3.0 = Hold
   - 2.0 = Sell
   - 1.0 = Strong Sell (lowest)

5. **Filter in Notion**:
   - Consensus = "Strong Buy" + Signal = "🚀 Strong Buy" = Best picks
   - Consensus = "Strong Sell" + Signal = "❄️ Neutral" = Potential shorts
   - Signal = "❄️ N/A" = Delisted stocks (for reference only)

---

## 📚 **DOCUMENTATION FILES**

- `DOCUMENTATION_INDEX.md` - Entry point for all documentation
- `COMPREHENSIVE_FINAL_REPORT.md` - Complete project overview
- `DATABASE_COLUMN_REFERENCE.md` - Column definitions
- `NOTION_SCHEMA.md` - Notion schema + practical usage & screening scenarios
- `NOTION_VIEWS.md` - How to create daily views & workflows in Notion
- `SYSTEM_GUIDE.md` - Full system documentation
- `QUICK_START.md` - This file

---

## ✅ **SUMMARY**

**First Time**:
1. `scripts/setup/add_analyst_columns.py` (once)
2. `scripts/maintenance/load_missing_stocks.py` (once)

**Regular Use**:
- Daily: `src/bots/market_bot_lite.py`
- Weekly: `src/bots/market_bot_ai.py`
- Monthly: `src/bots/market_bot_pro.py`

**Your market intelligence system is ready! 🚀**
