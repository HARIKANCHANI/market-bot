# 🚀 Getting Started with Market Bot

Welcome! This guide will help you get up and running with the Market Bot in minutes.

---

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Notion account (for database integration)
- HuggingFace account (for AI version only)

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Clone & Install
```bash
# Clone the repository
git clone <your-repo-url>
cd market-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy example config
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env and add your credentials:
# NOTION_TOKEN=your_notion_integration_token
# DATABASE_ID=your_notion_database_id
# HF_TOKEN=your_huggingface_token  # Only for AI version
```

### Step 3: Run Your First Bot
```bash
# Lightweight version (recommended for first run)
python -m src.bots.market_bot_lite

# Or test a single stock
python test_single_stock.py RELIANCE
```

---

## 🎯 Choose Your Bot

### 1. Lite Bot (Recommended for Beginners)
**Best for:** Daily updates, fast execution
```bash
python -m src.bots.market_bot_lite
```
- ✅ No AI model download
- ✅ Fast (5-10 minutes for 631 stocks)
- ✅ Technical indicators only

### 2. AI Bot (Most Accurate)
**Best for:** Weekly analysis with sentiment
```bash
python -m src.bots.market_bot_ai
```
- 🤖 FinBERT sentiment analysis
- 📰 AI-powered news analysis
- ⏱️ Slower first run (model download)

### 3. Pro Bot (Most Robust)
**Best for:** Monthly reports, production use
```bash
python -m src.bots.market_bot_pro
```
- 📊 Comprehensive logging
- 🔒 Extra error handling
- 📈 Analyst ratings included

### 4. Excel Bot (Offline Analysis)
**Best for:** Excel reports, no Notion needed
```bash
python -m src.bots.market_bot_excel
```
- 📑 Generates .xlsx files
- 💾 Saves to output/ folder
- 📊 Includes FII/DII holdings

---

## 📖 Next Steps

### Learn the Basics
1. **[Quick Start Guide](./QUICK_START.md)** - Detailed walkthrough
2. **[Bot Usage Guide](../guides/bot-usage/INCREMENTAL_BOTS_GUIDE.md)** - All bot versions explained
3. **[Quick Reference](../reference/QUICK_REFERENCE.md)** - Common commands

### Understand the System
4. **[Architecture Overview](../architecture/ARCHITECTURE_DIAGRAMS.md)** - How it works
5. **[Features Guide](../guides/features/RANKING_SYSTEM.md)** - Intelligent ranking explained
6. **[Data Flow](../architecture/DATA_FLOW_DETAILED.md)** - Data pipeline

### Advanced Topics
7. **[Optimization Guide](../optimization/README.md)** - Performance tuning
8. **[Technical Docs](../technical/TECHNICAL_DOCUMENTATION.md)** - API reference
9. **[Testing Guide](../guides/testing/TEST_SINGLE_STOCK_GUIDE.md)** - Test individual stocks

---

## 🛠️ Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**2. Notion API Errors**
- Check your NOTION_TOKEN is correct
- Verify DATABASE_ID matches your database
- Ensure integration has access to the database

**3. yfinance Data Issues**
- Check internet connection
- Try a different stock ticker
- Wait a few minutes and retry

**4. AI Model Download Issues**
- Check HF_TOKEN is valid
- Ensure stable internet connection
- Model downloads to `models/` folder (~500MB)

### Get Help
- Check **[Troubleshooting Guide](../maintenance/)** for more solutions
- Review **[Technical Documentation](../technical/TECHNICAL_DOCUMENTATION.md)**
- Check logs in `logs/` folder

---

## ✅ Verification Checklist

Before running in production, verify:

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list` shows all packages)
- [ ] .env file configured with valid tokens
- [ ] Notion database accessible
- [ ] Test run successful on small dataset
- [ ] Logs directory exists and writable
- [ ] Output directory exists (for Excel bot)

---

## 🎓 Learning Resources

### Video Tutorials (Recommended)
1. **Setup & Installation** (Coming soon)
2. **Running Your First Bot** (Coming soon)
3. **Understanding the Results** (Coming soon)

### Documentation
- **[Complete Documentation Hub](../README.md)** - All docs
- **[Bot Comparison Guide](../guides/bot-usage/)** - Choose the right bot
- **[Feature Highlights](../guides/features/)** - Key capabilities

---

## 🚀 Quick Commands Reference

```bash
# Activate environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run bots
python -m src.bots.market_bot_lite          # Lite version
python -m src.bots.market_bot_ai            # AI version
python -m src.bots.market_bot_pro           # Pro version
python -m src.bots.market_bot_excel         # Excel version

# Incremental updates (faster)
python -m src.bots.market_bot_lite_incremental
python -m src.bots.market_bot_ai_incremental
python -m src.bots.market_bot_pro_incremental

# Test single stock
python test_single_stock.py <TICKER>

# Check dependencies
pip list
pip check

# Update dependencies
pip install -r requirements.txt --upgrade
```

---

**Ready to start?** Head to **[Quick Start Guide](./QUICK_START.md)** for detailed instructions!
