# 📊 Sector Column Update - Complete Guide

## Overview

The Market Bot has been updated to include a **Sector** column in the Notion database. This column provides industry classification for each stock, making it easier to analyze sector-wise performance and build diversified portfolios.

---

## 🆕 What's New?

### Added Sector Column
- **Column Name**: `Sector`
- **Type**: Select (dropdown)
- **Source**: Yahoo Finance API (`stock.info['sector']`)
- **Fallback**: Uses `industry` field if sector is not available
- **Default**: "Unknown" (for stocks with no sector data)

---

## 📋 Sector Categories

Common sectors you'll see:

- **Technology** - IT services, software
- **Financial Services** - Banks, insurance, NBFCs
- **Consumer Cyclical** - Auto, retail, durables
- **Consumer Defensive** - FMCG, food & beverages
- **Healthcare** - Pharma, hospitals, diagnostics
- **Industrials** - Engineering, capital goods
- **Energy** - Oil & gas, power
- **Basic Materials** - Metals, chemicals, mining
- **Communication Services** - Telecom, media
- **Real Estate** - Real estate, construction
- **Utilities** - Power utilities
- **Unknown** - Stocks with no sector information

---

## 🛠️ Implementation Details

### Changes Made to All Bot Versions

#### 1. **market_bot_lite.py**
- Added sector extraction in `get_market_intelligence()` function
- Sector data included in stock data dictionary
- Sector sent to Notion in `send_to_notion()` function

#### 2. **market_bot_pro.py**
- Added sector extraction in `get_market_data()` function
- Sector data included in all return dictionaries
- Sector field added to Notion payload

#### 3. **market_bot_ai.py**
- Added sector extraction in `get_market_intelligence()` function
- Sector information preserved through AI analysis pipeline
- Sector uploaded to Notion database

### Code Changes

```python
# In all bot versions - market data function
sector = "Unknown"
try:
    info = stock.info
    # Get sector information
    sector = info.get('sector', info.get('industry', 'Unknown'))
except:
    pass

# Return dictionary now includes:
return {
    "ticker": symbol,
    "cap": cap_size,
    "sector": sector,  # ← NEW FIELD
    "price": latest_price,
    # ... other fields
}

# Notion payload updated:
payload = {
    "parent": {"database_id": DATABASE_ID},
    "properties": {
        "Ticker": {...},
        "Market Cap": {...},
        "Sector": {"select": {"name": data.get('sector', 'Unknown')}},  # ← NEW
        # ... other properties
    }
}
```

---

## 🗄️ Notion Database Setup

### Creating the Sector Column

**Option 1: Manual Setup**
1. Open your Notion database
2. Click "+" to add new column
3. Name it "Sector"
4. Select type: **Select**
5. Add sector options as needed (they will auto-populate when bot runs)

**Option 2: Automatic Creation**
- The bot will attempt to create the column on first run
- If column doesn't exist, you may see errors - just add it manually

---

## 🗑️ Clean Database and Fresh Upload

### Step 1: Delete All Existing Entries

Run the deletion script:

```bash
python scripts/delete_notion_entries.py
```

**What it does:**
- Fetches all pages from your Notion database
- Asks for confirmation (type 'DELETE')
- Archives all entries (deletes them)
- Shows progress and summary

**Output:**
```
🗑️  NOTION DATABASE CLEANUP
📊 Found 675 entries to delete
⚠️  WARNING: This will delete all 675 entries
Type 'DELETE' to confirm: DELETE

🗑️  Deleting 675 entries...
✅ [1/675] Deleted: RELIANCE
✅ [2/675] Deleted: TCS
...
🎉 All entries deleted successfully!
```

### Step 2: Run Fresh Upload

```bash
# Run the LITE version (fastest)
python -m venv\Scripts\activate
python src\bots\market_bot_lite.py
```

**What happens:**
- Analyzes all 675 stocks
- Fetches sector information for each
- Uploads to Notion with new Sector column
- Estimated time: ~25-30 minutes

---

## 📊 Using the Sector Column

### Portfolio Analysis

**Group by Sector:**
1. In Notion, click "View Options"
2. Select "Group by" → "Sector"
3. See stocks organized by industry

**Sector Performance:**
- Sort by "Momentum (%)" within each sector group
- Identify which sectors are performing best
- Build sector-diversified portfolios

### Example Queries

**Top stocks in Technology:**
```
Filter: Sector = Technology
Sort: Score (descending)
```

**Best performing sectors:**
```
Group by: Sector
Sort: Momentum (%) avg (descending)
```

---

## 🎯 Benefits

1. **Better Portfolio Diversification**
   - See sector allocation at a glance
   - Avoid over-concentration in one sector

2. **Sector Rotation Strategy**
   - Identify trending sectors
   - Move capital to outperforming sectors

3. **Risk Management**
   - Balance defensive vs cyclical sectors
   - Reduce sector-specific risk

4. **Market Analysis**
   - Understand which sectors are leading the market
   - Spot sector-wide trends

---

## 🔧 Troubleshooting

### Issue: "Sector" column not found error

**Solution:**
1. Open Notion database
2. Add column named "Sector" (case-sensitive)
3. Set type to "Select"
4. Re-run the bot

### Issue: All stocks showing "Unknown" sector

**Possible causes:**
- Yahoo Finance API issue
- Network connectivity problem
- Stock delisted or insufficient data

**Solution:**
- Wait and retry after some time
- Check internet connection
- Stocks with no data will always show "Unknown"

### Issue: Too many sector options in dropdown

**Solution:**
- This is normal - Yahoo Finance returns many sector variations
- You can manually merge similar sectors in Notion
- Or let them auto-populate (recommended)

---

## 📈 Example Output

After running the bot, your Notion database will look like:

| Ticker | Rank | Sector | Market Cap | Price | Momentum | Score | Signal |
|--------|------|--------|------------|-------|----------|-------|--------|
| HFCL | 1 | Technology | Large Cap | ₹140.42 | +83.8% | 1542 | 🚀 Strong Buy |
| NATIONALUM | 2 | Basic Materials | Large Cap | ₹398.70 | +82.2% | 1537 | 🚀 Strong Buy |
| SAIL | 3 | Basic Materials | Large Cap | ₹196.50 | +51.3% | 1281 | 🚀 Strong Buy |
| BHARATFORG | 4 | Industrials | Mid Cap | ₹1881.90 | +51.0% | 1279 | 🚀 Strong Buy |

---

## 🚀 Next Steps

1. ✅ Run deletion script to clear database
2. ✅ Ensure "Sector" column exists in Notion
3. ✅ Run market_bot_lite.py for fresh upload
4. ✅ Group stocks by sector in Notion
5. ✅ Analyze sector-wise performance
6. ✅ Build diversified portfolio

---

## 📝 Version Compatibility

- **All Bot Versions Updated**: LITE, PRO, AI
- **Backward Compatible**: Works with existing databases
- **No Breaking Changes**: Old data structure still supported
- **Automatic Fallback**: Uses "Unknown" if sector not available

---

**Happy Analyzing! 🎉**
