# 🚀 Ticker Mapping System - Quick Reference

## 📝 TL;DR

**Before fetching data, ALWAYS:**
```python
# Step 1: Import functions
from data.nse_stocks_650 import get_current_ticker, is_delisted

# Step 2: Get current ticker
current_symbol = get_current_ticker(symbol)

# Step 3: Check if should filter
if is_delisted(current_symbol):
    return None

# Step 4: Fetch data with CURRENT ticker
stock = yf.Ticker(f"{current_symbol}.NS")
```

---

## 🔧 Two Functions - That's It!

### `get_current_ticker(ticker)`
Maps old ticker → new ticker
```python
get_current_ticker("IIFLSEC")  # → "IIFLCAPS"
get_current_ticker("TCS")      # → "TCS" (no change)
```

### `is_delisted(ticker)`
Returns `True` if stock should be filtered out
```python
is_delisted("DHFL")     # → True (delisted)
is_delisted("DISHTV")   # → True (pump & dump)
is_delisted("TCS")      # → False (active)
```

---

## 📊 Quick Stats

| Category | Count |
|----------|-------|
| Ticker Renames | 13 |
| Delisted Stocks | 6 |
| Pump & Dump | 4 |
| Total Filtered | 10 |
| Active Stocks | ~906 |

---

## 🎯 Common Mappings (Quick Lookup)

| Old → New | Why |
|-----------|-----|
| IIFLSEC → IIFLCAPS | Company renamed |
| IIFLWAM → 360ONE | Company renamed |
| INFIBEAM → CCAVENUE | Company renamed |
| LAXMIMACH → LMW | Ticker shortened |
| MAHINDCIE → CIEINDIA | Company renamed |
| MEGASOFT → SIGMAADV | Company renamed |
| ORIENTREF → RHIM | Company renamed |
| KSBL → KSL | Typo correction |

---

## 🚫 Filtered Stocks (Quick Lookup)

### Delisted (6):
`DHFL`, `ISEC`, `JPINFRATEC`, `KHAITANELE`, `KRIPAINDU`, `PRESSMAN`

### Pump & Dump (4):
`DISHTV`, `GTLINFRA`, `JETAIRWAYS`, `INFORMEDIA`

---

## ✅ Integration Checklist

- [ ] Import `get_current_ticker` and `is_delisted`
- [ ] Call `get_current_ticker()` before data fetch
- [ ] Call `is_delisted()` to filter
- [ ] Use **current ticker** for API calls
- [ ] Use **original ticker** for display

---

## 🛠️ Maintenance

**Add Renamed Ticker:**
```python
# In data/nse_stocks_650.py
TICKER_RENAME_MAP = {
    "OLDTICKER": "NEWTICKER",  # Add here
}
```

**Add Delisted Stock:**
```python
# In data/nse_stocks_650.py
DELISTED_STOCKS = {
    "DEADSTOCK",  # Add here
}
```

**Add Pump & Dump:**
```python
# In data/nse_stocks_650.py
PUMP_AND_DUMP_STOCKS = {
    "RISKSTOCK",  # Add here
}
```

---

## 🔍 Quick Tests

```python
# Test ticker mapping
from data.nse_stocks_650 import get_current_ticker
assert get_current_ticker("IIFLSEC") == "IIFLCAPS"

# Test filtering
from data.nse_stocks_650 import is_delisted
assert is_delisted("DHFL") == True
assert is_delisted("TCS") == False
```

---

## 📚 Full Documentation

See **`PRODUCTION_TICKER_MAPPING_SYSTEM.md`** for complete details.

---

**Last Updated:** May 24, 2026  
**Version:** 1.0  
**Status:** Production Ready ✅
