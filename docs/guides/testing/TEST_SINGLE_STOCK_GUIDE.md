# 🧪 Standalone AI-Enabled Stock Tester

## Overview

`test_single_stock.py` is a standalone script for testing any single stock with **full AI intelligence** (FinBERT sentiment analysis, news aggregation, analyst ratings, and sector validation) without modifying the master 650-stock data file.

---

## ✨ Features

- ✅ **Full AI Analysis** - FinBERT sentiment analysis on news
- ✅ **Comprehensive News** - Aggregates news from multiple sources
- ✅ **Analyst Ratings** - Fetches and aggregates analyst recommendations
- ✅ **Sector Validation** - Ensures sector names match Notion dropdown
- ✅ **Volume-Confirmed Trends** - Uses 2-factor trend logic (Momentum + Volume)
- ✅ **Notion Upload** - Creates or updates entries in Notion database
- ✅ **Standalone** - Does NOT modify `nse_stocks_650.py`
- ✅ **UTF-8 Support** - Handles emoji and special characters on Windows

---

## 🚀 Usage

### **Basic Usage:**

```powershell
python test_single_stock.py TICKER [CAP_SIZE]
```

### **Examples:**

```powershell
# Test MAKEINDIA (defaults to Small Cap)
python test_single_stock.py MAKEINDIA

# Test RELIANCE with Large Cap classification
python test_single_stock.py RELIANCE "Large Cap"

# Test TCS
python test_single_stock.py TCS "Large Cap"

# Test any Small Cap stock
python test_single_stock.py SAIL "Small Cap"
```

---

## 📊 What It Does

### **1. Data Collection**
- Fetches 7-month price history from yfinance
- Calculates momentum, volume surge, market cap
- Resolves renamed tickers automatically
- Validates sector names for Notion compatibility

### **2. AI Analysis**
- Aggregates news from multiple sources
- Analyzes sentiment using FinBERT AI model
- Fetches analyst ratings and consensus
- Generates composite intelligence score

### **3. Trend Calculation**
- **📈 Upward:** Momentum > 2% AND Volume > 1.0x
- **📉 Downward:** Momentum < -2% AND Volume > 1.0x
- **➡️ Neutral:** All other cases

### **4. Notion Upload**
- Checks if ticker exists in database
- Updates existing entry OR creates new one
- Uploads all metrics, trend, signal, news, ratings

---

## 📋 Output Example

```
======================================================================
🤖 STANDALONE AI-ENABLED STOCK TESTER
======================================================================

📥 Loading FinBERT AI model...
✅ FinBERT model loaded successfully!
======================================================================

======================================================================
🎯 Testing Stock: MAKEINDIA
======================================================================

📊 Fetching market intelligence for MAKEINDIA...
   ✅ Price data: ₹160.38, Momentum: 4.5%, Volume: 1.29x
   📌 Mapped sector 'Industrial Machinery' -> 'Industrials'
   📰 Fetching news...
   ✅ Found 5 news articles
   🤖 AI Sentiment: Neutral (0.02)
   📊 Fetching analyst ratings...
   ✅ Ratings: 3.8/5.0 (12 analysts) - Hold

✅ Data fetched successfully!

📋 Stock Details:
   Ticker: MAKEINDIA
   Sector: Industrials
   Cap Size: Small Cap
   Price: ₹160.38
   Market Cap: ₹2,450.50 Cr
   Momentum: 4.5%
   Volume Surge: 1.29x
   AI Sentiment: 0.02 (Neutral)
   Analyst Rating: 3.8/5.0 - Hold
   Analyst Count: 12
   Trend: 📈 Upward (volume-confirmed)
   Signal: 👀 Watch
   Score: 68.44

📤 Uploading to Notion...
   🔄 Updating existing entry...

🎉 SUCCESS! MAKEINDIA uploaded to Notion successfully!

✅ All validations passed:
   ✓ Sector validation: 'Industrials' accepted
   ✓ AI sentiment analyzed
   ✓ Trend calculated: 📈
   ✓ Signal determined: 👀 Watch

======================================================================
✅ TEST PASSED - MAKEINDIA processed successfully!
======================================================================
```

---

## 🎯 Use Cases

### **1. Testing Sector Validation**
Verify that unknown sectors map correctly:
```powershell
python test_single_stock.py MAKEINDIA
# Check output for: "📌 Mapped sector 'X' -> 'Y'"
```

### **2. Debugging Failed Stocks**
Test individual stocks that failed in full bot runs:
```powershell
python test_single_stock.py PROBLEMATIC_TICKER
```

### **3. Quick Stock Analysis**
Get instant AI-powered analysis for any stock:
```powershell
python test_single_stock.py RELIANCE "Large Cap"
```

### **4. Verifying Notion Upload**
Test that data uploads correctly to Notion:
```powershell
python test_single_stock.py TCS "Large Cap"
# Check Notion database for updated entry
```

---

## ⚙️ Requirements

- Python 3.8+
- `.env` file with:
  - `NOTION_TOKEN`
  - `DATABASE_ID`
  - `HF_TOKEN` (Hugging Face token for FinBERT)
- Dependencies from `requirements.txt`

---

## 🔧 Technical Details

### **AI Model:**
- **Model:** ProsusAI/finbert
- **Device:** CPU (-1)
- **Cache:** `./models/`

### **Sector Validation:**
- Uses `VALID_NOTION_SECTORS` dictionary
- Supports partial matching (case-insensitive)
- Defaults to "Unknown" for unrecognized sectors
- **52 sector mappings** → 10 Notion categories

### **Trend Logic:**
Same as all production bots:
- Momentum threshold: ±2%
- Volume threshold: 1.0x
- Both must be satisfied for 📈/📉

---

## 🆚 Comparison with Other Scripts

| Feature | test_single_stock.py | update_makeindia.py | test_makeindia.py |
|---------|---------------------|---------------------|-------------------|
| **AI Enabled** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Loads FinBERT** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Any Stock** | ✅ Yes | ❌ MAKEINDIA only | ❌ MAKEINDIA only |
| **Standalone** | ✅ Yes | ❌ Uses bot file | ❌ Uses bot file |
| **Clean Output** | ✅ Yes | ❌ Full bot logs | ❌ Full bot logs |
| **Speed** | 🐌 3-5 min | 🐌 3-5 min | 🐌 3-5 min |

---

## ✅ Advantages

1. **Standalone** - Doesn't modify `nse_stocks_650.py`
2. **Flexible** - Test any stock, any cap size
3. **Complete** - Full AI analysis included
4. **Clean** - Focused output, easy to read
5. **Safe** - Isolated from production data

---

## 🚨 Important Notes

- **Does NOT modify** the 650-stock data file
- **Loads AI model** every time (takes 2-3 minutes)
- **Uploads to Notion** (creates or updates entry)
- **Uses production credentials** from `.env`
- **Respects sector validation** to prevent errors

---

## 📚 Related Documentation

- **SECTOR_MAPPING_REFERENCE.md** - Complete sector mapping guide
- **SECTOR_VALIDATION_FIX.md** - Sector validation implementation
- **TREND_LOGIC_WITH_VOLUME.md** - Volume-confirmed trend logic
- **COMPLETE_PYTHON_FILES_DOCUMENTATION.md** - All bots documentation

---

**Last Updated:** 2026-05-25  
**Version:** 1.0  
**Status:** ✅ Production Ready
