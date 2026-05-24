# 📦 Dependency Audit Report - Market Bot Repository

**Date**: 2026-05-24  
**Status**: ✅ COMPLETE

## Executive Summary

Comprehensive dependency audit completed. **2 missing dependencies found** (optional utilities). All core bot dependencies are correctly specified.

---

## Current Requirements (requirements.txt)

```
# Core Dependencies
requests>=2.31.0          ✅ Used by all bots
pandas>=2.0.0             ✅ Used by Excel bot
yfinance>=0.2.28          ✅ Used by all bots

# AI/ML (for market_bot_ai.py only)
transformers>=4.30.0      ✅ Used by AI bot
torch>=2.0.0              ✅ Used by AI bot (FinBERT)

# Visualization (for creating flowcharts)
matplotlib>=3.7.0         ✅ Used by utilities

# Optional: Scheduling
schedule>=1.2.0           ℹ️  Not used in current code
```

---

## Dependency Analysis by Component

### ✅ Core Bots (All Required Dependencies Present)

#### market_bot_ai.py
- ✅ requests
- ✅ yfinance
- ✅ transformers
- ✅ torch (indirect via transformers)

#### market_bot_pro.py
- ✅ requests
- ✅ yfinance

#### market_bot_lite.py
- ✅ requests
- ✅ yfinance

#### market_bot_excel.py
- ✅ pandas
- ✅ yfinance
- ✅ requests

### ✅ Core Modules

#### src/core/analyst_ratings.py
- ✅ requests
- ✅ yfinance
- ✅ statistics (stdlib)

#### src/core/news_aggregator.py
- ✅ requests
- ✅ re (stdlib)

#### src/core/ranking_engine.py
- ✅ statistics (stdlib)

### ❌ Utilities (Missing Optional Dependencies)

#### utilities/create_ranking_flowcharts.py
- ✅ matplotlib
- ❌ **numpy** - MISSING from requirements.txt
- 📝 Used for: Creating ranking system flowcharts

#### utilities/convert_to_word.py
- ❌ **python-docx** - MISSING from requirements.txt
- 📝 Used for: Converting markdown docs to Word format
- 📝 Has try/except with helpful error message

#### utilities/create_flowchart.py  
- ❌ **graphviz** - MISSING from requirements.txt
- 📝 Used for: Creating data flow diagrams
- 📝 Has try/except with helpful error message

#### utilities/create_visual_flowchart.py
- ✅ matplotlib

### ✅ Scripts (All Dependencies Present)

#### scripts/setup/fresh_start.py
- ✅ requests

#### scripts/maintenance/load_missing_stocks.py
- ✅ requests

#### scripts/maintenance/update_prices.py
- ✅ requests
- ✅ yfinance

---

## Issues Found

### 1. ❌ numpy - Missing (for utilities/create_ranking_flowcharts.py)
**Severity**: Low (utility script only)  
**Impact**: Flowchart generation will fail  
**Used in**: `utilities/create_ranking_flowcharts.py`  
**Recommendation**: Add to requirements.txt

### 2. ❌ python-docx - Missing (for utilities/convert_to_word.py)
**Severity**: Low (utility script only)  
**Impact**: Markdown to Word conversion will fail  
**Used in**: `utilities/convert_to_word.py`  
**Mitigation**: Script has try/except with helpful error message  
**Recommendation**: Add to optional dependencies section

### 3. ❌ graphviz - Missing (for utilities/create_flowchart.py)
**Severity**: Low (utility script only)  
**Impact**: Data flow diagram generation will fail  
**Used in**: `utilities/create_flowchart.py`  
**Mitigation**: Script has try/except with helpful error message  
**Recommendation**: Add to optional dependencies section

### 4. ℹ️  schedule - Unused
**Severity**: None (not an issue)  
**Impact**: Listed but not actively used  
**Recommendation**: Keep for future use or remove if not needed

---

## Recommendations

### Required Action: Update requirements.txt

Add missing dependency for flowchart generation:
```python
# Add to requirements.txt after matplotlib
numpy>=1.24.0             # For ranking flowchart generation
```

### Optional: Add Utilities Section

Create optional dependencies section:
```python
# Optional: Utilities (install as needed)
# python-docx>=0.8.11      # For convert_to_word.py
# graphviz>=0.20.0         # For create_flowchart.py (also needs system graphviz)
```

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Python files scanned | 20+ |
| Required dependencies | 7 |
| Missing core dependencies | 0 ✅ |
| Missing optional dependencies | 3 |
| Unused dependencies | 1 |

---

## Conclusion

✅ **Core dependency health: EXCELLENT**

All critical bot dependencies are properly specified. Only utility script dependencies are missing, and these scripts already have good error handling. The repository is production-ready for all bot operations.

**Priority**: 
1. 🔴 **HIGH**: Add `numpy` (breaks existing flowchart utility)
2. 🟡 **LOW**: Document optional utilities dependencies
3. 🟢 **OPTIONAL**: Remove or document `schedule` if unused

**Status**: 🟢 Core functionality ready. Minor updates recommended for utilities.
