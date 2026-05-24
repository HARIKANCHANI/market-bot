# ⚡ Quick Reference Card
# Market Bot - Essential Commands & Files

**Print this page for desk reference!**

---

## 🤖 CORE BOTS (Choose One)

| Bot | Runtime | Use Case | Command |
|-----|---------|----------|---------|
| **Lite** 🏃 | 18-20 min | Daily quick updates | `python src/bots/market_bot_lite.py` |
| **Pro** 💼 | 30-35 min | Comprehensive analysis | `python src/bots/market_bot_pro.py` |
| **AI** 🧠 | 4-5 hours | AI sentiment (weekends) | `python src/bots/market_bot_ai.py` |

---

## 🔧 MAINTENANCE (Keep System Healthy)

| Task | Command | When |
|------|---------|------|
| Check health | `python scripts/maintenance/check_database.py` | Daily |
| Update prices only | `python scripts/maintenance/update_prices.py` | Hourly |
| Add missing stocks | `python scripts/maintenance/load_missing_stocks.py` | Weekly |

---

## 📊 ANALYSIS (Get Insights)

| Report | Command | Output |
|--------|---------|--------|
| Top 25 picks | `python scripts/analysis/top_recommendations.py` | Console report |
| Export Excel | `python scripts/create_stock_excel.py` | `output/*.xlsx` |
| Count stocks | `python scripts/check_total_stocks.py` | Quick count |

---

## 🛠️ SETUP (One-Time Only)

| Task | Command | When |
|------|---------|------|
| Install dependencies | `pip install -r requirements.txt` | First time |
| Configure credentials | Edit `.env` file | First time |
| Reset database | `python scripts/setup/fresh_start.py` | Clean start |
| Setup AI models | `python scripts/setup/setup_models.py` | Before AI bot |

---

## 📁 KEY FILES

### Bots
- `src/bots/market_bot_lite.py` - Fast daily updates
- `src/bots/market_bot_pro.py` - Professional analysis
- `src/bots/market_bot_ai.py` - AI-powered sentiment

### Core Modules
- `src/core/ranking_engine.py` - Intelligent ranking (9 metrics)
- `src/core/news_aggregator.py` - 70+ news sources
- `src/core/analyst_ratings.py` - Analyst consensus

### Configuration
- `.env` - Your credentials (NEVER commit!)
- `src/config/env_config.py` - Config loader
- `requirements.txt` - Dependencies list

### Data
- `data/nse_stocks_650.py` - 675 NSE stocks universe

---

## 🔑 ENVIRONMENT VARIABLES

Required in `.env` file:

```bash
NOTION_TOKEN=ntn_xxxxx...     # Required for all
DATABASE_ID=664b00792a60...   # Required for all
HF_TOKEN=hf_xxxxx...          # Only for AI bot
```

---

## 📈 PERFORMANCE BENCHMARKS

| Bot | Time | Memory | Success Rate |
|-----|------|--------|--------------|
| Lite | 18-20 min | 300 MB | >99% |
| Pro | 30-35 min | 500 MB | >98% |
| AI | 4-5 hours | 3-4 GB | >95% |

---

## 🚨 EMERGENCY COMMANDS

```bash
# Check if system is working
python scripts/maintenance/check_database.py

# View logs
cat logs/market_bot_pro.log

# Count stocks
python scripts/check_total_stocks.py

# Delete all data (CAUTION!)
python scripts/delete_notion_entries.py
```

---

## 📊 NOTION DATABASE COLUMNS (16 Total)

1. **Ticker** - Stock symbol (e.g., RELIANCE.NS)
2. **Rank** - 1 (best) to 675 (worst)
3. **Market Cap** - Large/Mid/Small Cap
4. **Sector** - Industry sector
5. **Price (₹)** - Current price
6. **Momentum** - % change (1 month)
7. **Volume Surge** - Volume vs average
8. **Signal** - 🚀 Strong Buy / 📈 Buy / ⚠️ Hold / 📉 Sell
9. **Score** - Composite investment score
10. **Sentiment** - Overall sentiment (0-1)
11. **News** - Latest news summary
12. **News Sentiment** - News-based sentiment
13. **News Types** - News categories
14. **Consensus** - Analyst consensus
15. **Ratings** - Average analyst rating
16. **AI Sentiment** - FinBERT AI score (AI bot only)

---

## 🎯 RECOMMENDED SCHEDULE

### Weekday
- **9:00 AM**: `market_bot_lite.py` (before market opens)
- **4:00 PM**: `market_bot_pro.py` (after market closes)

### Weekend
- **Saturday**: `market_bot_ai.py` (deep AI analysis)
- **Sunday**: Review reports, export Excel

### Monthly
- **1st of month**: `fresh_start.py` + full bot run

---

## 🐛 QUICK TROUBLESHOOTING

| Error | Solution |
|-------|----------|
| "NOTION_TOKEN not found" | Create `.env` file with credentials |
| "ModuleNotFoundError" | Run `pip install -r requirements.txt` |
| "Out of memory" | Use Lite/Pro bot, close other apps |
| "API rate limit" | Wait 1 minute, built-in retry |
| Bot hangs | Normal, check logs for progress |

---

## 📞 GET HELP

1. **Full Docs**: `COMPLETE_PYTHON_FILES_DOCUMENTATION.md`
2. **Setup Guide**: `CREDENTIALS_MIGRATION_GUIDE.md`
3. **Quick Start**: `QUICK_START_GUIDE.md`
4. **Troubleshooting**: Appendix B in full docs

---

## 💡 PRO TIPS

✅ **Always check database health first**:
```bash
python scripts/maintenance/check_database.py
```

✅ **Monitor logs in real-time**:
```bash
tail -f logs/market_bot_pro.log
```

✅ **Calculate success rate**:
```bash
grep "✅" logs/market_bot_pro.log | wc -l
```

✅ **Quick test with 5 stocks**: Edit bot to use `[:5]` slice

✅ **Automate with cron** (Linux/Mac):
```bash
0 9 * * 1-5 cd /path/to/market-bot && python src/bots/market_bot_lite.py
```

---

**Last Updated**: 2026-05-24  
**Version**: 1.0  
**Status**: ✅ Production Ready

---

## 🎯 ONE-LINER CHEAT SHEET

```bash
# Most common command (daily use)
python src/bots/market_bot_lite.py

# Second most common (comprehensive)
python src/bots/market_bot_pro.py

# Check everything is OK
python scripts/maintenance/check_database.py

# Get top picks
python scripts/analysis/top_recommendations.py
```

**That's it! You're a Market Bot expert!** 🚀
