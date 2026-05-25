# 🚀 Quick Start Guide
# Market Bot - Get Running in 10 Minutes

**Total Time**: ~10 minutes  
**Difficulty**: Beginner-friendly

---

## 📋 Prerequisites

- ✅ Python 3.8+
- ✅ Notion account with API access
- ✅ Internet connection

---

## ⚡ 3-Step Quick Start

### Step 1: Install Dependencies (2 minutes)

```bash
# Clone or navigate to project
cd market-bot

# Install required packages
pip install -r requirements.txt
```

**Expected Output**: All packages installed successfully ✅

---

### Step 2: Configure Credentials (3 minutes)

```bash
# Copy example environment file
cp .env.example .env
```

**Edit `.env` file** with your credentials:

```bash
# Required for all bots
NOTION_TOKEN=ntn_YOUR_TOKEN_HERE
DATABASE_ID=YOUR_DATABASE_ID_HERE

# Required for AI bot only (optional for quick start)
HF_TOKEN=hf_YOUR_TOKEN_HERE
```

**How to get credentials:**
- **NOTION_TOKEN**: Notion Settings → Integrations → New Integration → Copy token
- **DATABASE_ID**: Open your Notion database → Share → Copy link → Extract 32-char ID
- **HF_TOKEN**: HuggingFace.co → Settings → Access Tokens → New token

---

### Step 3: Run Your First Bot (5 minutes)

```bash
# Test configuration
python scripts/maintenance/check_database.py
```

**Expected Output**: ✅ Database is healthy!

```bash
# Run quick update (fastest - 18-20 min)
python src/bots/market_bot_lite.py
```

**Expected Output**: 
```
🤖 MARKET BOT LITE - QUICK UPDATE
📊 Processing 675 stocks...
✅ [1/675] RELIANCE.NS updated
✅ [2/675] TCS.NS updated
...
🎉 Complete! Success: 675/675 (100%)
```

---

## 🎯 What Just Happened?

You've successfully:
1. ✅ Installed all dependencies
2. ✅ Configured secure credentials
3. ✅ Connected to Notion database
4. ✅ Updated all 675 stocks with latest data

**Your Notion database now contains:**
- 📈 Current prices
- 📊 Momentum indicators
- 📰 Market sentiment
- 🎯 Investment signals
- ⭐ Intelligent rankings

---

## 📚 Next Steps

### For Daily Use

```bash
# Quick morning update (18-20 min)
python src/bots/market_bot_lite.py

# Comprehensive update (30-35 min)
python src/bots/market_bot_pro.py
```

### For Deep Analysis

```bash
# AI-powered sentiment analysis (4-5 hours, weekends)
# First time: Downloads FinBERT model (~500MB)
python src/bots/market_bot_ai.py
```

### For Analysis & Reports

```bash
# Get top 25 recommendations
python scripts/analysis/top_recommendations.py

# Export to Excel
python scripts/create_stock_excel.py
```

---

## 🔧 Common Commands

| Task | Command | Time |
|------|---------|------|
| Quick update | `python src/bots/market_bot_lite.py` | 18-20 min |
| Full update | `python src/bots/market_bot_pro.py` | 30-35 min |
| AI analysis | `python src/bots/market_bot_ai.py` | 4-5 hours |
| Check health | `python scripts/maintenance/check_database.py` | <5 sec |
| Top picks | `python scripts/analysis/top_recommendations.py` | <10 sec |
| Export Excel | `python scripts/create_stock_excel.py` | <30 sec |

---

## ❓ Troubleshooting

### Issue: "NOTION_TOKEN not found"
**Solution**: Check `.env` file exists and has correct credentials

### Issue: "pip install fails"
**Solution**: Upgrade pip: `pip install --upgrade pip`

### Issue: "Database connection error"
**Solution**: Verify DATABASE_ID in `.env` is correct (32 characters)

### Issue: Bot runs slow
**Solution**: Normal! First run is slower. Subsequent runs are faster.

---

## 📖 Learn More

- **Full Documentation**: See `COMPLETE_PYTHON_FILES_DOCUMENTATION.md`
- **Quick Reference**: See `QUICK_REFERENCE.md`
- **Architecture**: See visual diagram in this folder
- **Credentials Setup**: See `CREDENTIALS_MIGRATION_GUIDE.md`

---

## 🎉 You're Ready!

You now have a fully functional Indian stock market intelligence system!

**Recommended Schedule:**
- 🌅 **Morning (9:00 AM)**: Run `market_bot_lite.py` before market opens
- 🌆 **Evening (4:00 PM)**: Run `market_bot_pro.py` after market closes
- 🌙 **Weekend**: Run `market_bot_ai.py` for deep AI analysis

**Pro Tips:**
- ⏰ Set up cron jobs for automatic updates
- 📊 Use Excel exports for offline analysis
- 🎯 Check top recommendations daily
- 📈 Monitor success rates in logs

---

**Status**: ✅ You're all set! Happy trading! 📈

For questions, check `COMPLETE_PYTHON_FILES_DOCUMENTATION.md` or troubleshooting guide.
