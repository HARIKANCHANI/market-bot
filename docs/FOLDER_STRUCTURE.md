# 📁 Market Bot - Complete Folder Structure

## Overview

This document describes the complete, organized folder structure of the Market Bot project after reorganization.

---

## 📂 Root Directory Structure

```
market-bot/
├── src/                    # Source code
├── tests/                  # Unit tests
├── data/                   # Stock data files
├── docs/                   # Documentation
├── utilities/              # Utility scripts
├── scripts/                # Automation scripts
├── logs/                   # Log files
├── archive/                # Archived files
├── venv/                   # Virtual environment
├── README.md               # Project overview
└── requirements.txt        # Python dependencies
```

---

## 📂 src/ - Source Code

```
src/
├── __init__.py
├── bots/                   # Market analysis bots
│   ├── __init__.py
│   ├── market_bot_ai.py        # AI-powered sentiment (FinBERT)
│   ├── market_bot_pro.py       # Professional version with ratings
│   └── market_bot_lite.py      # Lightweight version
│
├── core/                   # Core modules
│   ├── __init__.py
│   ├── analyst_ratings.py      # Analyst ratings aggregation
│   ├── news_aggregator.py      # Multi-source news fetching
│   └── ranking_engine.py       # Intelligent ranking system ⭐ NEW
│
├── config/                 # Configuration files
│   └── __init__.py
│
└── utils/                  # Utility functions
    └── __init__.py
```

---

## 📂 tests/ - Unit Tests

```
tests/
└── test_ranking_engine.py      # Ranking engine tests ⭐ NEW
```

---

## 📂 data/ - Stock Data

```
data/
├── __init__.py
└── nse_stocks_650.py          # 650+ NSE stocks with classification
```

---

## 📂 docs/ - Documentation

All documentation files are in the flat docs/ folder:

```
docs/
├── DOCUMENTATION_INDEX.md                  # Master index ⭐
├── COMPREHENSIVE_FINAL_REPORT.md           # Project overview
├── TECHNICAL_DOCUMENTATION.md              # Technical guide
├── DATABASE_COLUMN_REFERENCE.md            # Database schema
├── DATABASE_SCHEMA.md                      # Schema overview
├── QUICK_START.md                          # Getting started
├── SYSTEM_GUIDE.md                         # Architecture guide
├── FEATURE_IMPLEMENTATION.md               # Features
├── PRODUCTION_READY.md                     # Production status
├── FOLDER_STRUCTURE.md                     # This file
│
├── Ranking System Documentation ⭐
├── RANKING_INDEX.md                        # Ranking system index
├── COMPLETE_RANKING_DELIVERY.md            # Complete delivery
├── QUICK_RANKING_GUIDE.md                  # Quick reference
├── RANKING_SYSTEM.md                       # Technical docs
├── RANKING_VISUALIZATIONS.md               # Visual guide
├── VISUAL_FLOWCHARTS_SUMMARY.md            # Visual summary
├── RANKING_IMPLEMENTATION_SUMMARY.md       # Implementation summary
├── README_VISUALIZATIONS.md                # Quick access
│
├── Notion Documentation ⭐
├── NOTION_SCHEMA.md                        # Schema & usage guide
├── NOTION_VIEWS.md                         # Views & workflow
│
├── Visual Assets ⭐
├── Ranking_System_Flow.png                 # Flow diagram
├── Ranking_Weights_Distribution.png        # Pie chart
├── Final_Verification_Flowchart.png        # Verification flowchart
├── DATA_FLOW_DIAGRAM.png                   # Data flow
│
├── Verification & Testing
├── FINAL_VERIFICATION_REPORT.md            # Final verification
├── FINAL_VERIFICATION_FLOWCHART.md         # Verification guide
├── FINAL_CHECK_COMPLETE.md                 # Final check
├── PROJECT_AUDIT_REPORT.md                 # Audit report
├── AUDIT_COMPLETE_SUMMARY.md               # Audit summary
├── BOTS_VERIFICATION_REPORT.md             # Bots verification
├── VERIFICATION_COMPLETE.md                # Verification status
│
├── Test Run Reports
├── ALL_BOTS_FINAL_TEST_SUMMARY.md          # All bots test
├── PRO_AI_BOTS_TEST_RUN.md                 # Pro/AI test
├── LITE_BOT_TEST_RUN.md                    # Lite bot test
├── LITE_BOT_FIX_SUMMARY.md                 # Lite bot fixes
│
├── Project Organization
├── PROJECT_ORGANIZATION_SUMMARY.md         # Organization summary
├── PROJECT_REORGANIZATION_COMPLETE.md      # Reorganization
├── COMPLETE_WORK_SUMMARY.md                # Work summary
│
├── Architecture & Design
├── ARCHITECTURE_DIAGRAMS.md                # Architecture diagrams
├── ARCHITECTURE_DIAGRAMS_CREATED.md        # Diagrams created
├── DATA_FLOW_DETAILED.md                   # Data flow details
│
├── Configuration & Features
├── PRO_VERSION_CONFIGURATION.md            # Pro version config
├── PRO_NEWS_CONFIG_IMPLEMENTATION.md       # News config
├── EXCEL_BOT_VERSION.md                    # Excel version
├── SECTOR_COLUMN_UPDATE.md                 # Sector column
│
└── Microsoft Office Versions
    ├── DATA_FLOW_DETAILED.docx             # Word version
    └── DOCUMENTATION_SUMMARY.docx          # Word version
```

**Note**: All documentation files are in a flat structure in the `docs/` directory. The groupings above are conceptual categories for organization.

---

## 📂 utilities/ - Utility Scripts ⭐ NEW LOCATION

```
utilities/
├── create_ranking_flowcharts.py    # Generate ranking flowcharts ⭐
├── create_flowchart.py             # General flowchart generator
├── create_visual_flowchart.py      # Visual flowchart utility
└── convert_to_word.py              # Convert MD to DOCX
```

---

## 📂 scripts/ - Automation Scripts

```
scripts/
├── analysis/               # Analysis scripts
├── maintenance/            # Maintenance scripts
└── setup/                  # Setup scripts
```

---

## 📂 logs/ - Log Files

```
logs/
├── market_bot_ai.log       # AI bot logs
├── market_bot_pro.log      # Pro bot logs
└── market_bot_lite.log     # Lite bot logs
```

---

## 📂 archive/ - Archived Files

```
archive/
└── docs/                   # Old documentation versions
```

---

## 🎯 Key Changes from Reorganization

### ✅ What Moved

1. **Documentation Consolidation**
   - All ranking docs moved to `docs/`
   - Better organization within docs folder

2. **Utilities Folder Created** ⭐
   - `create_ranking_flowcharts.py` → `utilities/`
   - `create_flowchart.py` → `utilities/`
   - `create_visual_flowchart.py` → `utilities/`
   - `convert_to_word.py` → `utilities/`

3. **Ranking System Added** ⭐
   - New core module: `src/core/ranking_engine.py`
   - New tests: `tests/test_ranking_engine.py`
   - 6 new documentation files in `docs/`
   - 2 new visual assets (PNG flowcharts)

---

## 📊 File Count by Category

| Category | Count | Location |
|----------|-------|----------|
| Source Code | 9 | `src/` |
| Tests | 1 | `tests/` |
| Documentation | 20+ | `docs/` |
| Utilities | 4 | `utilities/` ⭐ |
| Data Files | 1 | `data/` |
| Visual Assets | 3 | `docs/` |
| **Total** | **38+** | Various |

---

## 🔍 Finding Files

### "Where is...?"

**Ranking system code?** → `src/core/ranking_engine.py`  
**Ranking documentation?** → `docs/RANKING_INDEX.md` (start here)  
**Flowchart generator?** → `utilities/create_ranking_flowcharts.py` ⭐  
**Visual assets?** → `docs/*.png`  
**Main bots?** → `src/bots/`  
**Tests?** → `tests/`  
**Documentation index?** → `docs/DOCUMENTATION_INDEX.md`  

---

## 📝 Summary

✅ **Clean structure** - Logical organization  
✅ **Clear separation** - Code, docs, utilities separate  
✅ **Easy navigation** - Everything has its place  
✅ **Well documented** - Comprehensive guides  
✅ **Production ready** - Professional organization  

**Last Updated**: 2026-05-18  
**Version**: 2.0 (with ranking system)
