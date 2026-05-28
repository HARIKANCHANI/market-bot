# 📋 Changelog - Market Bot

All notable changes to the Market Bot project are documented here.

---

## [2026-05-28] - 🛡️ Reliability & Transparency Improvements

### ✨ Added

#### **Retry Logic with Exponential Backoff**
- **Feature:** 3 automatic retry attempts for failed Yahoo Finance API calls
- **Implementation:** `retry_with_backoff()` function in `analyst_ratings.py`
- **Backoff Strategy:** Exponential delays of 2s → 4s → 8s
- **Coverage:** Applied to both `stock.info` and `stock.recommendations` API calls
- **Impact:** Improved success rate from ~90-95% to ~99-100%

#### **Enhanced Logging & Visibility**
- **Ticker Names in Ratings:** All ratings output now includes stock ticker for clarity
  - Before: `✅ Ratings: Buy (4.27/5.0), Target: ₹490 (+17.3%)`
  - After: `✅ SAREGAMA Ratings: Buy (4.27/5.0), Target: ₹490 (+17.3%)`
- **Verbose Error Messages:** Full error output (200 chars) for debugging
- **Retry Progress Logging:** Real-time visibility into retry attempts
  - `⚠️ Attempt 1/3 failed: HTTPError...`
  - `⏳ Waiting 2s before retry...`
  - `✅ Retry attempt 3 succeeded!`
- **Failure Notifications:** Clear indication when all retries exhausted
  - `❌ All 3 attempts failed for this request`

### ⚙️ Changed

#### **Parallel Processing Optimization**
- **Workers:** Reduced from 12 to **4 parallel workers**
- **Rationale:** Better API stability, avoids Yahoo Finance & NSE rate limiting
- **Sleep Time:** Increased to **1.0 seconds** between stocks
- **Trade-off:** Slightly longer runtime (~17-20 min vs ~16 min) for much higher reliability

#### **Performance Metrics**
- **Processing Time:** ~17-20 minutes for 631 stocks (was ~16 min with higher failure rate)
- **Processing Rate:** ~35-40 stocks/minute (was ~40-45 with more errors)
- **Success Rate:** ~99-100% (was ~90-95%)
- **Data Completeness:** Significantly improved with retry logic

### 🐛 Fixed

#### **API Reliability Issues**
- **HTTP 400 Errors:** Now automatically retried with exponential backoff
- **HTTP 404 Errors:** Handled gracefully with retry mechanism
- **Rate Limiting:** Resolved by reducing parallel workers from 12 to 4
- **Missing Analyst Data:** Recovered through intelligent retry attempts
- **Transient Failures:** No longer result in N/A values after single attempt

### 📁 Files Modified

**Core Files:**
- `src/core/analyst_ratings.py` - Added retry logic, enhanced error handling
- `src/bots/market_bot_ai.py` - Updated worker count to 4, added ticker to ratings log

**Configuration Files:**
- `src/config/logging_config.py` - Already configured for verbose logging

---

## [2026-05-27] - 🎯 Analyst Ratings Feature Enhancement

### ✨ Added

#### **New Notion Database Columns**
- **Target Mean Price** (₹) - Average analyst price target
- **Target High Price** (₹) - Highest analyst price target
- **Target Low Price** (₹) - Lowest analyst price target
- **Upside/Downside Percentage** (%) - Potential gain/loss vs current price
- **Upgrades Count** (#) - Number of recent analyst upgrades
- **Downgrades Count** (#) - Number of recent analyst downgrades
- **Analyst Firms** (Text) - List of firms providing ratings

#### **Data Source Enhancement**
- Transitioned from `yf.Ticker.recommendations` (often empty for Indian stocks)
- Now using `yf.Ticker.info` fields for aggregate metrics
- Fallback to `recommendations` for historical firm-level data
- Better coverage for NSE-listed stocks

### 🐛 Fixed

#### **NaN Value Handling**
- **Issue:** Notion API doesn't accept NaN values, causing update failures
- **Solution:** Comprehensive sanitization in `utils/data_sanitization.py`
- **Coverage:** All numeric fields converted NaN → None for Notion compatibility

---

## [2026-05-26] - 📚 Major Architectural Cleanup

### ♻️ Refactored

#### **Codebase Organization**
- Cleaned up test files from root directory
- Organized all tests into `tests/` directory
- Archived old log files to `logs/archive/`
- Removed temporary debug output files

#### **GitHub Actions Configuration**
- Disabled automatic daily workflow schedules
- Kept `workflow_dispatch` for manual triggering
- Allows controlled execution of bot updates

---

## [Earlier] - 🏗️ Historical Features

### ✨ Core Features Implemented

#### **Multi-Bot Architecture**
- `market_bot_ai.py` - Full AI-powered analysis with FinBERT sentiment
- `market_bot_lite.py` - Fast updates with keyword sentiment
- `market_bot_pro.py` - Comprehensive analysis with configurable news
- Incremental versions of all bots for faster Notion upserts

#### **Intelligent Ranking System**
- 9-factor multi-dimensional ranking algorithm
- Weighted scoring: Momentum (30%), Volume (20%), News (25%), etc.
- Handles missing data gracefully with smart defaults

#### **AI Sentiment Analysis**
- FinBERT model integration for financial news sentiment
- Centralized `sentiment_analyzer.py` module
- Confidence scoring for sentiment predictions

#### **News Aggregation**
- 70+ news sources (Yahoo, Economic Times, Moneycontrol, etc.)
- Intelligent fallback from comprehensive to basic sources
- News type classification (Earnings, Product, Legal, M&A, etc.)

#### **Analyst Ratings Aggregation**
- Data from 50+ global and Indian analysts
- Buy/Hold/Sell consensus calculation
- Numeric rating aggregation (1-5 scale)

#### **Notion Database Integration**
- 16 comprehensive columns per stock
- Automatic updates with error handling
- Incremental update support for faster syncs

#### **Ticker Mapping System**
- Automatic handling of 13+ company renames
- Transparent mapping (e.g., IIFLSEC → IIFLCAPS)
- Zero configuration needed

---

## 📊 Version History Summary

| Version | Date | Key Feature | Impact |
|---------|------|-------------|--------|
| **Latest** | 2026-05-28 | Retry Logic + 4 Workers | 99% success rate |
| 2.1 | 2026-05-27 | Enhanced Analyst Columns | 7 new data points |
| 2.0 | 2026-05-26 | Architectural Cleanup | Organized codebase |
| 1.x | Earlier | Core Features | Full bot suite |

---

## 🔮 Planned Improvements

### Future Enhancements
- [ ] Configurable retry count and backoff strategy
- [ ] Per-source retry configuration
- [ ] Adaptive worker count based on API response times
- [ ] Enhanced error categorization and reporting
- [ ] Retry statistics in final summary report

---

**Last Updated:** 2026-05-28  
**Maintained By:** Development Team
