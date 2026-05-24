## Notion Views Guide for Market Bots

This guide shows how to set up **default Notion views** for the Market Bot
stocks database and how to use them for a **daily 10–20 stock workflow**.

If you are new:
- First read `NOTION_SCHEMA.md` to understand the columns.
- Then come back here to design views and daily workflows in Notion.

---

## 1. What You Need First

You should have:
- A single Notion database connected to the bots (with all columns from
  `NOTION_SCHEMA.md`).
- At least one bot run completed (e.g. `market_bot_lite.py`) so the
  database has data.

All views below are created on **this one database**.

---

## 2. Default Views (Overview)

Recommended core views:

| View Name                  | Icon | Main Purpose                                      |
|---------------------------|------|---------------------------------------------------|
| All Stocks (Master)       | 📊   | Full universe, debug and sanity checks           |
| Daily Momentum Picks      | ⚡   | Primary daily shortlist of strong technicals     |
| News‑Driven Opportunities | 📰   | Stocks moving on positive earnings/product news  |
| Small‑Cap Breakout Radar  | 🎯   | Optional higher‑risk small‑cap ideas             |
| Recently Updated Ideas    | ⏱️   | What changed today                                |

You can add weekly/monthly views later (see cookbook in `NOTION_SCHEMA.md`).

---

## 3. How to Create a View in Notion

For each view:
1. Open your stocks database in Notion.
2. Click the view dropdown (top left) → **Add a view**.
3. Choose **Table** (or **Board** for special cases) and give it the
   **name + icon** from the table above.
4. Click **Filter**, **Sort**, and **Group** in the view bar and apply the
   settings described below.
5. Hide/show columns so only the important ones are visible.

---

## 4. View Definitions (Daily Use)

### 4.1 All Stocks (Master) – 📊

- **Filter:** none
- **Sort:** `Rank` ascending, then `Ticker` ascending
- **Group (optional):** by `Market Cap`
- **Show columns:** at least `Rank`, `Ticker`, `Market Cap`, `Sector`,
  `Price (₹)`, `Momentum (%)`, `Volume Surge`, `Score`, `Signal`,
  `Last Updated`, `Consensus`, `Ratings`

Use this as your baseline reference and to check that all columns look sane.

### 4.2 Daily Momentum Picks – ⚡ (Primary)

- **Filter:**
  - `Signal` is `🚀 Strong Buy`
  - `Momentum (%)` > `0`
  - `Volume Surge` ≥ `1.5`
  - `Last Updated` is within `past 1 days`
  - (Optional) `Market Cap` is not `Small Cap` for safer core picks
- **Sort:** `Score` ascending, then `Momentum (%)` descending
- **Show columns:** `Rank`, `Ticker`, `Price (₹)`, `Momentum (%)`,
  `Volume Surge`, `Score`, `Signal`, `News Sentiment`, `Last Updated`

This is your **main daily shortlist**.

### 4.3 News‑Driven Opportunities – 📰

- **Filter:**
  - `News Sentiment` is `Positive`
  - `News Type` contains `Earnings` OR `Product`
  - `Last Updated` is within `past 3 days`
- **Sort:** `Last Updated` descending, then `Momentum (%)` descending
- **Show columns:** `Ticker`, `Sector`, `Momentum (%)`, `Volume Surge`,
  `Signal`, `News Sentiment`, `News Type`, `News & Updates`

Use this to find moves backed by **clear positive catalysts**.

### 4.4 Small‑Cap Breakout Radar – 🎯 (Optional)

- **Filter:**
  - `Market Cap` is `Small Cap`
  - `Signal` is `🚀 Strong Buy` OR `👀 Watch`
  - `Momentum (%)` ≥ `15`
  - `Volume Surge` ≥ `1.5`
  - `Last Updated` is within `past 3 days`
- **Sort:** `Momentum (%)` descending, then `Volume Surge` descending

Use this for **higher‑risk, high‑upside** ideas; keep sizes smaller.

### 4.5 Recently Updated Ideas – ⏱️

- **Filter:**
  - `Last Updated` is within `past 1 days`
  - `Signal` is `🚀 Strong Buy` OR `👀 Watch`
- **Sort:** `Last Updated` descending, then `Rank` ascending

Use this as a **sanity check**: what the bot actually touched today.

---

## 5. Daily Workflow for 10–20 Positions

Target: **10–20 active positions** split into core (safer) and satellite
(higher beta).

### 5.1 Core vs Satellite

- **Core positions:**
  - Mostly Large/Mid caps from **⚡ Daily Momentum Picks** and
    **📰 News‑Driven Opportunities**
  - 70–90% of portfolio capital depending on how aggressive you are
- **Satellite positions:**
  - Small caps from **🎯 Small‑Cap Breakout Radar** (and any contrarian
    ideas if you add that view)
  - 10–30% of portfolio capital

### 5.2 Suggested Split

For **10 positions (more conservative):
- 6–8 core positions from ⚡ and 📰
- 0–2 satellite positions from 🎯 (if any are truly compelling)

For **20 positions (more diversified):
- 10–12 core positions from ⚡ and 📰
- 2–4 satellite positions from 🎯

Always keep:
- Each **small‑cap** position ≤ ~4–5% of total capital
- Total small‑cap exposure ≤ ~20–30% of capital

---

## 6. Position Sizing Template

Let total portfolio value be `P`.

**For ~10 positions (concentrated):**
- Core (6–8 names): ~80% of `P` → **8–12% per core position**
- Satellite (0–2 names): ~20% of `P` → **3–5% per satellite position**

**For ~20 positions (more diversified):**
- Core (10–12 names): ~70–75% of `P` → **4–7% per core position**
- Satellite (2–4 names): ~25–30% of `P` → **2–4% per satellite position**

Review and rebalance regularly:
- Trim positions that grow far above their target weight.
- Replace weaker names with stronger ones from your daily views.
