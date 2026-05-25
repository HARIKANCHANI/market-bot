# 🗑️ DELETE ALL NOTION DATABASE ENTRIES

## 📍 LOCATION

**Script:** `scripts/delete_notion_entries.py`

This script safely deletes ALL entries from your Notion database with interactive confirmation.

---

## ⚡ QUICK START

### **Simple Command:**
```bash
python scripts/delete_notion_entries.py
```

### **Or from project root:**
```bash
cd c:\Users\HARI KANCHANI\source\repos\market-bot
python scripts/delete_notion_entries.py
```

---

## 🎯 USE CASES

### **When to Use This Script:**

1. **Fresh Start** - Clean database before running full bot for first time
2. **After Bug Fix** - Clear corrupted/incorrect data (like the analyst ratings bug!)
3. **Testing** - Clean database before running test
4. **Database Reorganization** - Start fresh with new structure
5. **Performance Issues** - Remove duplicate/stale entries

### **When NOT to Use:**

- ❌ If you want to keep existing data
- ❌ For incremental updates (use incremental bots instead)
- ❌ If you only want to update specific stocks

---

## 📋 HOW IT WORKS

### **Step-by-Step Process:**

```
1. Load Environment Variables (.env)
   ↓
2. Connect to Notion API
   ↓
3. Fetch ALL Pages from Database
   ↓
4. Show Count & Ask for Confirmation
   ↓
5. Delete All Entries (one by one)
   ↓
6. Show Summary Report
```

---

## 🚀 USAGE EXAMPLE

### **Run the Script:**

```bash
(.venv) PS C:\Users\HARI KANCHANI\source\repos\market-bot> python scripts/delete_notion_entries.py
```

### **Expected Output:**

```
======================================================================
🗑️  NOTION DATABASE CLEANUP
======================================================================

📍 Database ID: abc123xyz789...
🔐 Using Notion API Token

🔍 Fetching all pages from database...
📊 Fetched 906 pages so far...

📊 Found 906 entries to delete

⚠️  WARNING: This will delete *all* 906 entries from your Notion database!
Type 'DELETE' to confirm: DELETE

🗑️  Deleting 906 entries...
======================================================================
✅ [1/906] Deleted: RELIANCE
✅ [2/906] Deleted: TCS
✅ [3/906] Deleted: INFY
...
✅ [50/906] Deleted: HDFCBANK

📈 Progress: 50/906 (5.5%)
   ✅ Successful: 50
   ❌ Failed: 0

...
✅ [906/906] Deleted: ZOMATO

======================================================================
📊 DELETION SUMMARY
======================================================================
Total entries: 906
✅ Successfully deleted: 906
❌ Failed: 0
======================================================================

🎉 All entries deleted successfully!
✅ Database is now empty and ready for fresh data upload.
```

---

## 🔐 SAFETY FEATURES

### **1. Interactive Confirmation**
```
Type 'DELETE' to confirm:
```
- Must type exactly `DELETE` (case-sensitive)
- Any other input cancels the operation
- Safe from accidental execution

### **2. Progress Tracking**
- Shows current progress every 50 deletions
- Displays success/failure counts
- Easy to monitor

### **3. Rate Limiting**
```python
time.sleep(0.3)  # 0.3 seconds between deletions
```
- Respects Notion API rate limits (3 req/sec)
- Prevents API throttling

### **4. Error Handling**
- Continues even if some deletions fail
- Reports failed deletions at the end
- Shows which tickers failed

---

## ⚙️ CONFIGURATION

### **Prerequisites:**

1. **Environment Variables** (`.env` file):
   ```
   NOTION_TOKEN=your_notion_integration_token
   DATABASE_ID=your_notion_database_id
   ```

2. **Notion Permissions:**
   - Integration must have access to the database
   - Must have delete/archive permissions

---

## ⏱️ PERFORMANCE

### **Deletion Speed:**

| Entries | Estimated Time |
|---------|---------------|
| 100 | ~30 seconds |
| 500 | ~2.5 minutes |
| 906 | ~4.5 minutes |
| 1000 | ~5 minutes |

**Calculation:** ~0.3 seconds per entry (due to rate limiting)

---

## 🧪 TESTING WORKFLOW

### **Recommended Flow for Testing Analyst Ratings Fix:**

```bash
# 1. Delete all existing entries (with wrong data)
python scripts/delete_notion_entries.py
# Type: DELETE

# 2. Run full AI bot with fixed code
python -m src.bots.market_bot_ai

# 3. Verify in Notion:
#    - Check Consensus column has actual values
#    - Check Ratings column shows numeric ratings
```

---

## 🔄 ALTERNATIVE: SELECTIVE DELETION

If you don't want to delete ALL entries, you can:

### **Option 1: Delete Manually in Notion**
- Select entries in Notion database
- Press Delete key
- Good for small numbers

### **Option 2: Use Filters + Manual Delete**
- Filter by specific criteria in Notion
- Select all filtered results
- Delete manually

### **Option 3: Custom Script**
- Modify `delete_notion_entries.py`
- Add filter logic to only delete specific stocks
- Example: Delete only stocks with "No Consensus"

---

## ⚠️ IMPORTANT NOTES

### **Data Loss Warning:**
- ⚠️ **This action is IRREVERSIBLE!**
- ⚠️ All data will be permanently deleted (archived in Notion)
- ⚠️ Make sure you have backups if needed
- ⚠️ Notion's trash keeps items for 30 days

### **Recovery:**
- Deleted entries are "archived" in Notion (not permanently deleted)
- Can be restored from Notion trash within 30 days
- Or simply re-run your bot to repopulate

---

## 🐛 TROUBLESHOOTING

### **Issue: "Database is already empty!"**
**Solution:** No action needed - database is clean!

### **Issue: "NOTION_TOKEN or DATABASE_ID not found"**
**Solution:** 
1. Check `.env` file exists
2. Verify credentials are set correctly
3. No quotes needed around values

### **Issue: "Error fetching pages"**
**Solution:**
1. Check internet connection
2. Verify Notion integration has database access
3. Check DATABASE_ID is correct

### **Issue: "Some entries failed to delete"**
**Solution:**
1. Run the script again (will only delete remaining entries)
2. Check Notion permissions
3. Delete failed entries manually in Notion

---

## 📊 AFTER DELETION

### **Next Steps:**

1. **Verify Empty Database:**
   - Open Notion database
   - Should show 0 entries

2. **Run Full Bot:**
   ```bash
   python -m src.bots.market_bot_ai
   ```

3. **Verify New Data:**
   - Check Notion database has new entries
   - Verify all columns populated correctly
   - Especially check Consensus and Ratings columns!

---

## 💡 PRO TIPS

### **Tip 1: Use Before Major Updates**
Always clean database before running full bot after major code changes.

### **Tip 2: Keep Logs**
Save the output of deletion script for reference:
```bash
python scripts/delete_notion_entries.py > deletion_log.txt 2>&1
```

### **Tip 3: Test with Small Database First**
If nervous, test on a separate test database first.

### **Tip 4: Backup Important Data**
Export Notion database to CSV before deletion if needed.

---

## 🔗 RELATED DOCUMENTATION

- **Bot Usage:** `docs/guides/bot-usage/INCREMENTAL_BOTS_GUIDE.md`
- **Analyst Ratings Fix:** `docs/reports/verification/ANALYST_RATINGS_FIX.md`
- **Notion Schema:** `docs/technical/NOTION_SCHEMA.md`

---

**Last Updated:** 2026-05-25  
**Script Version:** 1.0  
**Status:** ✅ Production-Ready
