# 📊 Sector Mapping - Quick Reference Card

## 🎯 At a Glance

| # | Notion Sector | yfinance Variations | Example Stocks |
|---|---------------|---------------------|----------------|
| 1 | **Technology** | Technology, Communication Services, Information Technology, Software | TCS, INFY, WIPRO |
| 2 | **Financial Services** | Financial Services, Financial, Banks, Insurance | HDFCBANK, SBIN, ICICIBANK |
| 3 | **Healthcare** | Healthcare, Pharmaceuticals, Biotechnology, Medical Devices | SUNPHARMA, DRREDDY, CIPLA |
| 4 | **Consumer Cyclical** | Consumer Cyclical, Retail | MARUTI, TITAN, TRENT |
| 5 | **Consumer Defensive** | Consumer Defensive, Consumer Goods | HINDUNILVR, ITC, NESTLEIND |
| 6 | **Industrials** | Industrials, Industrial, Machinery, Construction | LT, SIEMENS, MAKEINDIA |
| 7 | **Energy** | Energy, Oil & Gas, Utilities | RELIANCE, ONGC, NTPC |
| 8 | **Basic Materials** | Basic Materials, Materials, Metals & Mining, Chemicals | TATASTEEL, HINDALCO, SAIL |
| 9 | **Real Estate** | Real Estate | DLF, GODREJPROP, PRESTIGE |
| 10 | **Unknown** | *Anything unrecognized* | Fallback category |

---

## 🔍 Quick Lookup

### **How to find a stock's sector:**

1. **Known sector name?**
   - Find it in the table above
   - Use the Notion Sector name

2. **Unknown sector name?**
   - It will map to "Unknown"
   - Check logs to see what yfinance returned
   - Add mapping if needed

### **MAKEINDIA Example:**

```
yfinance: "Industrial Machinery & Equipment"
↓ (partial match on "Industrial")
Notion: "Industrials" ✅
```

---

## 📌 Most Common Mappings

| yfinance Says | Bot Maps To | Why |
|---------------|-------------|-----|
| "Technology" | Technology | Direct match |
| "Banks" | Financial Services | Banking = Financial |
| "Pharmaceuticals" | Healthcare | Pharma = Healthcare |
| "Machinery" | Industrials | Manufacturing = Industrial |
| "Oil & Gas" | Energy | Energy sector |
| "Metals & Mining" | Basic Materials | Metal = Materials |

---

## ⚡ Quick Actions

### **Add a new sector mapping:**
1. Open any bot file (e.g., `market_bot_ai.py`)
2. Find `VALID_NOTION_SECTORS` dictionary
3. Add new mapping:
   ```python
   "New Sector Name": "Notion Category",
   ```
4. Repeat for all 7 bots

### **Check unknown sectors in logs:**
```bash
cat logs/market_bot_*.log | Select-String "Unknown sector"
```

---

## 📊 Statistics

- **Total Mappings:** 52
- **Notion Categories:** 10
- **Coverage:** ~95% of stocks
- **Unknown Rate:** ~5%

---

**For full details, see:** `SECTOR_MAPPING_REFERENCE.md`
