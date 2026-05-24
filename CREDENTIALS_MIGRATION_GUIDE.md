# 🔐 Credentials Migration Guide

**Date**: 2026-05-24  
**Status**: ✅ COMPLETE

## 🎯 Overview

All hardcoded credentials have been removed and moved to environment variables for better security. This guide explains the changes and how to set up your environment.

---

## 📋 What Changed

### Before (Hardcoded Credentials) ❌
```python
NOTION_TOKEN = "ntn_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
DATABASE_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
HF_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### After (Environment Variables) ✅
```python
import os
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
HF_TOKEN = os.getenv("HF_TOKEN")
```

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Install python-dotenv
```bash
pip install -r requirements.txt
```

### Step 2: Create .env File
```bash
# Copy the example file
cp .env.example .env

# Or on Windows
copy .env.example .env
```

### Step 3: Edit .env File
Open `.env` in a text editor and add your credentials:

```bash
# Notion API Configuration
NOTION_TOKEN=your_notion_token_here
DATABASE_ID=your_database_id_here

# HuggingFace Token (for AI bot only)
HF_TOKEN=your_huggingface_token_here

# Optional: Notion API Version
NOTION_API_VERSION=2022-06-28
```

**⚠️ IMPORTANT**: Never commit the `.env` file to git! It's already in `.gitignore`.

---

## 📦 Files Updated

### Core Bots (3 files)
- ✅ `src/bots/market_bot_ai.py`
- ✅ `src/bots/market_bot_pro.py`
- ✅ `src/bots/market_bot_lite.py`

### Setup Scripts (2 files)
- ✅ `scripts/setup/fresh_start.py`
- ✅ `scripts/setup/add_analyst_columns.py`

### Maintenance Scripts (3 files)
- ✅ `scripts/maintenance/check_database.py`
- ✅ `scripts/maintenance/update_prices.py`
- ✅ `scripts/maintenance/load_missing_stocks.py`

### Analysis Scripts (1 file)
- ✅ `scripts/analysis/top_recommendations.py`

### Utility Scripts (3 files)
- ✅ `scripts/delete_notion_entries.py`
- ✅ `scripts/check_total_stocks.py`
- ✅ `scripts/create_stock_excel.py`

### New Files Created
- ✅ `src/config/env_config.py` - Centralized environment configuration module
- ✅ `.env.example` - Environment variable template (already existed, not modified)

---

## 🔧 New Configuration Module

A new centralized configuration module has been created:

**File**: `src/config/env_config.py`

**Features**:
- Automatic `.env` file detection
- Validation functions for required credentials
- Helper function to get Notion headers
- Better error messages if credentials are missing

**Usage Example**:
```python
from src.config.env_config import (
    NOTION_TOKEN,
    DATABASE_ID,
    validate_notion_config,
    get_notion_headers
)

# Validate before use
validate_notion_config()

# Get authenticated headers
headers = get_notion_headers()
```

---

## ✅ Testing Your Setup

### Test 1: Check Environment Variables
```bash
python -c "from src.config.env_config import NOTION_TOKEN, DATABASE_ID; print('✅ Credentials loaded successfully!' if NOTION_TOKEN and DATABASE_ID else '❌ Credentials missing')"
```

### Test 2: Run a Simple Script
```bash
python scripts/maintenance/check_database.py
```

### Test 3: Run a Bot (Dry Run)
```bash
# Test bot imports
python -c "from src.bots.market_bot_lite import *; print('✅ Bot loaded successfully!')"
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Store credentials in `.env` file
- Use different credentials for dev/staging/production
- Add `.env` to `.gitignore` (already done)
- Use environment variables in production/CI/CD
- Share `.env.example` with team (no real credentials)

### ❌ DON'T:
- Commit `.env` to version control
- Share your `.env` file
- Hardcode credentials in code
- Push credentials to public repositories
- Store production credentials in development `.env`

---

## 🐛 Troubleshooting

### Error: "NOTION_TOKEN not found in environment variables"

**Solution**:
1. Check that `.env` file exists in project root
2. Verify credentials are set in `.env`
3. Make sure no spaces around `=` in `.env`:
   ```bash
   # ❌ Wrong
   NOTION_TOKEN = your_token
   
   # ✅ Correct
   NOTION_TOKEN=your_token
   ```

### Error: "ModuleNotFoundError: No module named 'dotenv'"

**Solution**:
```bash
pip install python-dotenv
# Or
pip install -r requirements.txt
```

### Script Can't Find .env File

**Solution**:
The scripts now automatically look for `.env` in the project root. Make sure:
1. `.env` is in the root directory (same level as `src/`, `scripts/`, etc.)
2. Run scripts from project root: `python scripts/some_script.py`

---

## 🔄 Migration Checklist

- [x] ✅ `python-dotenv` added to requirements.txt
- [x] ✅ All bots updated to use environment variables
- [x] ✅ All scripts updated to use environment variables
- [x] ✅ Environment config module created (`src/config/env_config.py`)
- [x] ✅ Validation functions added
- [x] ✅ Error messages improved
- [x] ✅ Migration guide created (this document)

---

## 📞 Need Help?

1. **Missing .env**: Copy from `.env.example` and fill in your credentials
2. **Import errors**: Run `pip install -r requirements.txt`
3. **Credential errors**: Check your `.env` file for typos
4. **Still having issues**: Check the error message for specific guidance

---

## 🎉 Benefits of This Change

✅ **Security**: No more hardcoded credentials in code  
✅ **Flexibility**: Easy to switch between dev/prod environments  
✅ **Safety**: Credentials won't be accidentally committed  
✅ **Best Practice**: Industry standard for credential management  
✅ **Team Friendly**: Share code without sharing credentials  

---

**Migration completed successfully! All bots and scripts are now secure.**
