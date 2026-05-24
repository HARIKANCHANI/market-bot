# 🏭 Production-Grade Ticker System Documentation

## 🎯 Overview

The stock list (`data/nse_stocks_650.py`) now implements a **production-grade ticker management system** that:

✅ **Handles company renames** (e.g., CADILAHC → ZYDUSLIFE)  
✅ **Fetches historical data** using old ticker as fallback  
✅ **Prevents duplicates** in Notion database  
✅ **Never crashes** - graceful error handling  
✅ **Future-proof** - easy to add new renames

---

## 📊 How It Works

### **1. Ticker Rename Mapping**

When companies change names, their NSE ticker symbols change. The system tracks this:

```python
TICKER_RENAME_MAP = {
    "CADILAHC": "ZYDUSLIFE",      # Cadila Healthcare → Zydus Lifesciences (Mar 2022)
    "AMARAJABAT": "ARE&M",        # Amara Raja Batteries → Amara Raja Energy & Mobility
    "SUVENPHAR": "COHANCE",       # Suven Pharmaceuticals → Cohance Lifesciences (May 2025)
    "BURGERKING": "RBA",          # Burger King India → Restaurant Brands Asia (Feb 2022)
    "POLYCA": "POLYCAB",          # Polycab India (proper symbol)
    "EQUITAS": "EQUITASBNK",      # Equitas Small Finance Bank
    "IDFC": "IDFCFIRSTB",         # IDFC FIRST Bank (merged)
}
```

---

### **2. Automatic Current Ticker Resolution**

```python
from data.nse_stocks_650 import get_current_ticker

# Always returns current NSE symbol
get_current_ticker("CADILAHC")    # → "ZYDUSLIFE"
get_current_ticker("ZYDUSLIFE")   # → "ZYDUSLIFE"
get_current_ticker("RELIANCE")    # → "RELIANCE" (no change)
```

---

### **3. Historical Data Fallback**

When fetching data, the system tries:
1. **Current ticker** (e.g., ZYDUSLIFE)
2. **Old ticker** (e.g., CADILAHC) if current fails

```python
from data.nse_stocks_650 import fetch_stock_data_with_fallback

# Automatically tries both tickers
stock, ticker_used = fetch_stock_data_with_fallback("ZYDUSLIFE")
# Tries: ZYDUSLIFE.NS first, falls back to CADILAHC.NS if needed
```

---

### **4. Notion Database - No Duplicates**

```python
from data.nse_stocks_650 import get_stock_for_notion

# Always returns current ticker for Notion
get_stock_for_notion("CADILAHC")    # → "ZYDUSLIFE"
get_stock_for_notion("ZYDUSLIFE")   # → "ZYDUSLIFE"

# This prevents having both "CADILAHC" and "ZYDUSLIFE" in Notion
```

---

## 🤖 How to Use in Bots

### **Step 1: Get Stock List (Current Tickers Only)**

```python
from data.nse_stocks_650 import get_all_stocks_with_classification

stocks = get_all_stocks_with_classification()
# Returns: [("ZYDUSLIFE", "Large Cap"), ("RBA", "Small Cap"), ...]
# ✅ Only current symbols, no duplicates
```

### **Step 2: Fetch Data with Automatic Fallback**

```python
from data.nse_stocks_650 import fetch_stock_data_with_fallback

for ticker, cap_size in stocks:
    # Automatic fallback to historical ticker
    stock, _ = fetch_stock_data_with_fallback(ticker)
    
    # Get data (tries both current and old ticker)
    info = stock.info
    hist = stock.history(period="1y")
    news = stock.news
```

### **Step 3: Send to Notion (Current Ticker Only)**

```python
from data.nse_stocks_650 import get_stock_for_notion

for ticker, cap_size in stocks:
    # ... fetch data ...
    
    # Always use current ticker for Notion
    notion_ticker = get_stock_for_notion(ticker)
    
    send_to_notion({
        "ticker": notion_ticker,  # ✅ Always current symbol
        "name": info.get("longName"),
        "price": info.get("currentPrice"),
        # ...
    })
```

---

## 🛡️ Error Handling

The system **never crashes**:

```python
# If ZYDUSLIFE.NS fails → tries CADILAHC.NS
# If both fail → returns empty data (bot continues)
# Delisted stocks → automatically skipped
```

---

## 📝 Complete Bot Example

```python
from data.nse_stocks_650 import (
    get_all_stocks_with_classification,
    fetch_stock_data_with_fallback,
    get_stock_for_notion
)

def process_stocks():
    # Get all stocks (current tickers only)
    stocks = get_all_stocks_with_classification()
    
    for ticker, cap_size in stocks:
        print(f"Processing {ticker}...")
        
        # Fetch data (automatic fallback)
        stock, _ = fetch_stock_data_with_fallback(ticker)
        
        # Get data
        try:
            info = stock.info
            hist = stock.history(period="1y")
            
            # Always use current ticker for Notion
            notion_ticker = get_stock_for_notion(ticker)
            
            # Send to Notion
            send_to_notion({
                "ticker": notion_ticker,  # ✅ Current symbol only
                "market_cap": cap_size,
                "price": info.get("currentPrice"),
                "historical": hist.to_dict()
            })
            
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue  # ✅ Never crashes
```

---

## 🔄 Adding New Ticker Renames

When a company changes its name:

### **Step 1: Update `TICKER_RENAME_MAP`**

```python
# In data/nse_stocks_650.py
TICKER_RENAME_MAP = {
    # ... existing mappings ...
    "OLDNAME": "NEWNAME",  # Add new rename here
}
```

### **Step 2: Done!**

The system automatically:
- ✅ Returns new ticker in stock lists
- ✅ Falls back to old ticker for historical data
- ✅ Prevents duplicates in Notion
- ✅ No code changes needed in bots

---

## 🧪 Testing

Run the test suite:

```bash
python scripts/test_ticker_system.py
```

Tests verify:
- ✅ Ticker mapping works correctly
- ✅ Historical fallback works
- ✅ No duplicates in stock list
- ✅ Notion ticker resolution correct
- ✅ Data fetching works

---

## 📊 Current Mappings (May 2026)

| Old Ticker | Current Ticker | Company | Date Changed |
|------------|----------------|---------|--------------|
| **CADILAHC** | **ZYDUSLIFE** | Zydus Lifesciences | Mar 2022 |
| **AMARAJABAT** | **ARE&M** | Amara Raja Energy & Mobility | 2024 |
| **SUVENPHAR** | **COHANCE** | Cohance Lifesciences | May 2025 |
| **BURGERKING** | **RBA** | Restaurant Brands Asia | Feb 2022 |
| **POLYCA** | **POLYCAB** | Polycab India | - |
| **EQUITAS** | **EQUITASBNK** | Equitas Small Finance Bank | - |
| **IDFC** | **IDFCFIRSTB** | IDFC FIRST Bank | - |

---

## ✅ Benefits

1. **No Crashes**: Graceful fallback handling
2. **No Duplicates**: Single entry per company in Notion
3. **Historical Data**: Works for renamed companies
4. **Future-Proof**: Easy to add new renames
5. **Production-Ready**: Used by all bots

---

## 🎯 Key Takeaways

✅ Stock list contains **only current tickers**  
✅ Data fetching **automatically tries old ticker** as fallback  
✅ Notion gets **only current ticker** (no duplicates)  
✅ System **never crashes** on renamed companies  
✅ Easy to maintain when companies change names

**The ticker system is production-ready and handles all edge cases!** 🚀
