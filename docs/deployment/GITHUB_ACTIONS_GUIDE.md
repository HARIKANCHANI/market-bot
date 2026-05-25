# 🤖 Running Market Bot on GitHub Actions

This guide shows you how to run your bots automatically on GitHub using GitHub Actions with secure secrets.

---

## 🔐 Step 1: Add Secrets to GitHub (One-Time Setup)

### Go to Repository Settings

1. Visit: https://github.com/HARIKANCHANI/market-bot
2. Click **Settings** (top right)
3. In left sidebar: **Secrets and variables** → **Actions**
4. Click **"New repository secret"**

### Add These 3 Secrets

**Secret 1: NOTION_TOKEN**
- Name: `NOTION_TOKEN`
- Secret: `<your-notion-token-here>`
- Click "Add secret"

**Secret 2: DATABASE_ID**
- Name: `DATABASE_ID`
- Secret: `<your-database-id-here>`
- Click "Add secret"

**Secret 3: HF_TOKEN** (for AI bot)
- Name: `HF_TOKEN`
- Secret: `<your-huggingface-token-here>`
- Click "Add secret"

✅ **Done! Your secrets are now securely stored.**

---

## 📁 Step 2: Push Workflow Files to GitHub

I've created 2 workflow files for you:

1. **`.github/workflows/run-market-bot.yml`** - Manual trigger (any bot)
2. **`.github/workflows/daily-update.yml`** - Automatic daily updates

### Push them to GitHub:

```bash
git add .github/workflows/
git commit -m "Add GitHub Actions workflows for automated bot execution"
git push
```

---

## 🚀 Step 3: Run the Bots

### **Option A: Manual Trigger (Any Time)**

1. Go to: https://github.com/HARIKANCHANI/market-bot/actions
2. Click on **"Run Market Bot"** workflow (left sidebar)
3. Click **"Run workflow"** button (top right)
4. Choose which bot to run:
   - **lite** - Fast update (18-20 min)
   - **pro** - Comprehensive (30-35 min)
   - **ai** - AI analysis (4-5 hours)
5. Click **"Run workflow"**
6. Watch it run in real-time!

### **Option B: Automatic Daily Updates**

The **"Daily Market Update"** workflow runs automatically:
- **When**: Every weekday at 9 AM IST (3:30 AM UTC)
- **What**: Runs `market_bot_lite.py` for quick updates
- **Duration**: ~20 minutes

You can also trigger it manually:
1. Go to: https://github.com/HARIKANCHANI/market-bot/actions
2. Click **"Daily Market Update"**
3. Click **"Run workflow"**

---

## 📊 View Results

### During Execution

1. Go to: https://github.com/HARIKANCHANI/market-bot/actions
2. Click on the running workflow
3. Click on the job name
4. Watch real-time logs

### After Completion

1. Workflow shows ✅ (success) or ❌ (failed)
2. Download logs:
   - Scroll to bottom of completed workflow
   - Click **"Artifacts"**
   - Download **bot-logs** or **daily-update-logs**
3. Check your Notion database for updated data

---

## ⏰ Workflow Schedules

### Daily Update Workflow
```yaml
schedule:
  - cron: '30 3 * * 1-5'  # 9 AM IST, Monday-Friday
```

**Customize the schedule:**
- `30 3 * * 1-5` = 3:30 AM UTC (9 AM IST), weekdays
- `0 16 * * 1-5` = 4:00 PM UTC (9:30 PM IST), weekdays
- `0 */6 * * *` = Every 6 hours
- `0 0 * * 0` = Every Sunday at midnight

**Cron format**: `minute hour day month weekday`

### Enable/Disable Scheduled Runs

**To Enable**: Uncomment the `schedule` section in the workflow file
**To Disable**: Comment out the `schedule` section with `#`

---

## 🔍 Workflow Features

### What Each Workflow Does

**run-market-bot.yml** (Manual):
✅ Choose which bot to run (Lite/Pro/AI)
✅ Creates .env file from GitHub secrets
✅ Installs dependencies
✅ Runs selected bot
✅ Uploads logs as artifacts

**daily-update.yml** (Automatic):
✅ Runs every weekday at 9 AM IST
✅ Runs market_bot_lite.py (fastest)
✅ Checks database health after run
✅ Uploads logs
✅ Can also be triggered manually

---

## 💰 GitHub Actions Usage

### Free Tier Limits
- **Public repos**: Unlimited minutes
- **Private repos**: 2,000 minutes/month (free tier)

### Usage Per Run
- **Lite bot**: ~20 minutes
- **Pro bot**: ~35 minutes
- **AI bot**: ~240 minutes (4 hours)

### Monthly Usage (Daily Lite Bot)
- 20 min/day × 22 workdays = ~440 minutes/month
- ✅ Well within free tier!

---

## 🐛 Troubleshooting

### Issue: Secrets not found
**Solution**: Make sure secrets are named exactly:
- `NOTION_TOKEN` (not `notion_token`)
- `DATABASE_ID` (not `database_id`)
- `HF_TOKEN` (not `hf_token`)

### Issue: Workflow doesn't trigger
**Solution**: 
- Check the `.github/workflows/` folder exists
- Files must have `.yml` extension
- Must be on `main` branch

### Issue: Bot fails with import errors
**Solution**: Check that all dependencies are in `requirements.txt`

### Issue: Timeout error
**Solution**: AI bot may take >6 hours. Increase timeout:
```yaml
timeout-minutes: 360  # 6 hours
```

---

## 🎯 Best Practices

### For Daily Updates
✅ Use **Lite bot** - Fast and efficient
✅ Run before market opens (9 AM IST)
✅ Check logs regularly

### For Weekly Deep Analysis
✅ Use **AI bot** on weekends
✅ Manually trigger Saturday morning
✅ Download logs for analysis

### For Production Use
✅ Run **Pro bot** after market closes (4 PM IST)
✅ Set up email notifications for failures
✅ Monitor GitHub Actions usage

---

## 📧 Email Notifications

GitHub automatically emails you when:
- ❌ Workflow fails
- ✅ Workflow succeeds (optional)

**Configure in**: Settings → Notifications → Actions

---

## 🔄 Update Workflows

To modify workflows:

```bash
# 1. Edit the workflow file locally
# 2. Commit and push
git add .github/workflows/
git commit -m "Update workflow schedule"
git push

# Changes take effect immediately
```

---

## 📚 Example: Custom Weekend AI Analysis

Create `.github/workflows/weekend-ai.yml`:

```yaml
name: Weekend AI Analysis

on:
  schedule:
    - cron: '0 4 * * 6'  # Saturday 9:30 AM IST
  workflow_dispatch:

jobs:
  ai-analysis:
    runs-on: ubuntu-latest
    timeout-minutes: 360
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Configure secrets
        run: |
          echo "NOTION_TOKEN=${{ secrets.NOTION_TOKEN }}" >> .env
          echo "DATABASE_ID=${{ secrets.DATABASE_ID }}" >> .env
          echo "HF_TOKEN=${{ secrets.HF_TOKEN }}" >> .env
      
      - name: Run AI Bot
        run: python src/bots/market_bot_ai.py
```

---

## ✅ Quick Start Checklist

- [ ] Add 3 secrets to GitHub (NOTION_TOKEN, DATABASE_ID, HF_TOKEN)
- [ ] Push workflow files to GitHub
- [ ] Go to Actions tab
- [ ] Manually trigger "Run Market Bot" to test
- [ ] Verify it works (check Notion database)
- [ ] Enable daily automatic updates if desired

---

**Your bots can now run automatically on GitHub with secure secrets!** 🎉

**Next**: Visit https://github.com/HARIKANCHANI/market-bot/actions to get started!
