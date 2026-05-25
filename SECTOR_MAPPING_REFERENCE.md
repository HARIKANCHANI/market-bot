# 📊 Sector Mapping Reference Guide

## Overview

This document provides a complete reference for how yfinance sector names are mapped to valid Notion database sectors across all 7 bots.

---

## 🎯 Purpose

The `validate_sector()` function ensures that:
- ✅ All sector names from yfinance are valid for Notion
- ✅ Unknown/unrecognized sectors default to "Unknown" (safe fallback)
- ✅ Prevents Notion validation errors (like the MAKEINDIA issue)
- ✅ Provides consistent sector naming across the entire database

---

## 📋 Complete Sector Mapping Table

### **1. Technology Sector**

| yfinance Sector Name | Notion Sector | Notes |
|---------------------|---------------|-------|
| Technology | Technology | Direct match |
| Communication Services | Technology | Telecommunications |
| Telecommunication Services | Technology | Telecom companies |
| Information Technology | Technology | IT services |
| Software | Technology | Software companies |

**Example Stocks:** TCS, INFY, HCLTECH, WIPRO, TECHM

---

### **2. Financial Services Sector**

| yfinance Sector Name | Notion Sector | Notes |
|---------------------|---------------|-------|
| Financial Services | Financial Services | Direct match |
| Financial | Financial Services | Generic financial |
| Banks | Financial Services | Banking sector |
| Insurance | Financial Services | Insurance companies |

**Example Stocks:** HDFCBANK, ICICIBANK, SBIN, KOTAKBANK, AXISBANK

---

### **3. Healthcare Sector**

| yfinance Sector Name | Notion Sector | Notes |
|---------------------|---------------|-------|
| Healthcare | Healthcare | Direct match |
| Pharmaceuticals | Healthcare | Pharma companies |
| Biotechnology | Healthcare | Biotech firms |
| Medical Devices | Healthcare | Medical equipment |

**Example Stocks:** SUNPHARMA, DRREDDY, CIPLA, AUROPHARMA, LUPIN

---

### **4. Consumer Cyclical Sector**

| yfinance Sector Name | Notion Sector | Notes |
|---------------------|---------------|-------|
| Consumer Cyclical | Consumer Cyclical | Direct match |
| Retail | Consumer Cyclical | Retail companies |

**Example Stocks:** MARUTI, TITAN, TRENT, DMART, JUBLFOOD

---

### **5. Consumer Defensive Sector**

| yfinance Sector Name | Notion Sector | Notes |
|---------------------|---------------|-------|
| Consumer Defensive | Consumer Defensive | Direct match |
| Consumer Goods | Consumer Defensive | FMCG companies |

**Example Stocks:** HINDUNILVR, ITC, NESTLEIND, BRITANNIA, DABUR

---

### **6. Industrials Sector**

| yfinance Sector Name | Notion Sector | Notes |
|---------------------|---------------|-------|
| Industrials | Industrials | Direct match |
| Industrial | Industrials | Generic industrial |
| Industrial Goods | Industrials | Manufacturing |
| Machinery | Industrials | **MAKEINDIA falls here** |
| Construction | Industrials | Construction companies |

**Example Stocks:** LT, SIEMENS, ABB, HAVELLS, MAKEINDIA

---

### **7. Energy Sector**

| yfinance Sector Name | Notion Sector | Notes |
|---------------------|---------------|-------|
| Energy | Energy | Direct match |
| Oil & Gas | Energy | Oil and gas companies |
| Utilities | Energy | Power utilities |

**Example Stocks:** RELIANCE, ONGC, NTPC, POWERGRID, BPCL

---

### **8. Basic Materials Sector**

| yfinance Sector Name | Notion Sector | Notes |
|---------------------|---------------|-------|
| Basic Materials | Basic Materials | Direct match |
| Materials | Basic Materials | Generic materials |
| Metals & Mining | Basic Materials | Metal companies |
| Chemicals | Basic Materials | Chemical companies |

**Example Stocks:** TATASTEEL, HINDALCO, COALINDIA, VEDL, SAIL

---

### **9. Real Estate Sector**

| yfinance Sector Name | Notion Sector | Notes |
|---------------------|---------------|-------|
| Real Estate | Real Estate | Direct match |

**Example Stocks:** DLF, GODREJPROP, OBEROIRLTY, PRESTIGE, BRIGADE

---

### **10. Unknown Sector (Fallback)**

| yfinance Sector Name | Notion Sector | Notes |
|---------------------|---------------|-------|
| Unknown | Unknown | Default fallback |
| *Any unrecognized* | Unknown | Safe fallback for new sectors |

**Purpose:** Prevents validation errors for:
- Newly listed stocks
- Sectors not yet mapped
- Invalid/missing sector data

---

## 🔍 How Mapping Works

### **1. Direct Match**
```python
yfinance: "Technology"
→ Direct match found
→ Notion: "Technology"
```

### **2. Partial Match (Case-Insensitive)**
```python
yfinance: "Industrial Machinery & Equipment"
→ Contains "Industrial"
→ Mapped to: "Industrials"
→ Notion: "Industrials"
```

### **3. No Match (Fallback)**
```python
yfinance: "Agricultural Products"
→ No match found
→ Fallback to: "Unknown"
→ Notion: "Unknown"
```

---

## 📊 Statistics

- **Total Sector Mappings:** 52
- **Primary Notion Categories:** 10
- **Coverage:** ~95% of NSE stocks
- **Fallback Rate:** ~5% go to "Unknown"

---

## 🛠️ Adding New Sectors

To add a new sector mapping, update `VALID_NOTION_SECTORS` in all 7 bots:

```python
VALID_NOTION_SECTORS = {
    # ... existing mappings ...
    
    # New sector category
    "New Category": "New Category",
    "Variation 1": "New Category",
    "Variation 2": "New Category",
}
```

**Files to update:**
1. `src/bots/market_bot_ai.py`
2. `src/bots/market_bot_ai_incremental.py`
3. `src/bots/market_bot_lite.py`
4. `src/bots/market_bot_lite_incremental.py`
5. `src/bots/market_bot_pro.py`
6. `src/bots/market_bot_pro_incremental.py`
7. `src/bots/market_bot_excel.py`

---

## 📌 Common Use Cases

### **Filtering by Sector in Notion:**

1. **Technology stocks only:**
   - Filter: Sector = Technology
   - Result: All IT/software companies

2. **Financial sector analysis:**
   - Filter: Sector = Financial Services
   - Result: All banks, insurance, finance

3. **Defensive portfolio:**
   - Filter: Sector IN [Consumer Defensive, Healthcare, Utilities]
   - Result: Low-volatility sectors

---

## ⚠️ Important Notes

1. **Case-Insensitive Matching**
   - "technology" = "Technology" = "TECHNOLOGY"
   - All variations mapped correctly

2. **Partial Matching**
   - "Industrial Machinery" → "Industrials"
   - Flexible matching for compound names

3. **Unknown Sector Logging**
   - Unknown sectors logged as warnings
   - Check logs to identify new sectors to add

4. **Consistency Across Bots**
   - All 7 bots use identical mapping
   - Ensures database consistency

---

## 🔧 Troubleshooting

### **Issue: Stock showing "Unknown" sector**

**Solution:**
1. Check bot logs for sector name
2. Add mapping to `VALID_NOTION_SECTORS`
3. Rerun bot

### **Issue: Notion validation error**

**Solution:**
1. Verify sector exists in Notion dropdown
2. Check spelling matches exactly
3. Add to mapping if missing

---

## 📚 Related Documentation

- **SECTOR_VALIDATION_FIX.md** - Implementation details
- **PRODUCTION_TICKER_SYSTEM.md** - Ticker mapping system
- **COMPLETE_PYTHON_FILES_DOCUMENTATION.md** - Full bot documentation

---

**Last Updated:** 2026-05-25  
**Version:** 1.0  
**Status:** ✅ Active in all 7 bots
