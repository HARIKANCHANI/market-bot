## Notion Schema Guide for Market Bots

This document defines the **single Notion database schema** used by all bots:

- `src/bots/market_bot_lite.py` (LITE bot)
- `src/bots/market_bot_pro.py` (PRO bot)
- `src/bots/market_bot_ai.py` (AI Sentiment bot)
- `scripts/maintenance/load_missing_stocks.py` (incremental loader)

The Excel bot (`src/bots/market_bot_excel.py`) does **not** write to Notion; it only reads similar fields and outputs an Excel file.

---

## Consolidated Notion Schema (All Bots)

Each row in the Notion database represents **one stock**. The table below lists all properties the bots may read/write.

| Property name        | Type        | Used by                                  | Purpose (short)                                   |
|----------------------|------------|------------------------------------------|---------------------------------------------------|
| Ticker               | Title      | LITE, PRO, AI, loader                    | Stock symbol and primary identifier               |
| Market Cap           | Select     | LITE, PRO, AI, loader                    | Size bucket: Large / Mid / Small Cap              |
| Sector               | Select     | LITE, PRO, AI, loader                    | Sector / industry classification                  |
| Price (₹)            | Number     | LITE, PRO, AI, loader                    | Latest price in INR                               |
| Capital Market (₹)   | Number     | LITE, PRO, AI, loader                    | Market cap (numeric) in INR                       |
| Sentiment            | Number     | LITE, PRO, AI, loader                    | Numeric sentiment score from news / AI            |
| Momentum (%)         | Number     | LITE, PRO, AI, loader                    | Recent percentage price change                    |
| Volume Surge         | Number     | LITE, PRO, AI, loader                    | Volume vs average (e.g. 2.0 = 2× normal)          |
| Score                | Number     | LITE, PRO, AI, loader                    | Combined ranking score                            |
| Rank                 | Number     | LITE, PRO, AI                            | Position in ranking (1 = best)                    |
| Signal               | Select     | LITE, PRO, AI, loader                    | Qualitative signal: Strong Buy / Watch / Neutral  |
| Last Updated         | Date       | LITE, PRO, AI, loader                    | Timestamp of last update                          |
| News & Updates       | Rich text  | LITE, PRO, AI, loader                    | Concise recent headlines / summaries              |
| News Sentiment       | Select     | LITE, PRO, AI, loader                    | Overall tone of news (Positive / Negative / etc.) |
| News Type            | Multi-select | LITE, PRO, AI, loader                  | Tags for type of news (Earnings, Product, etc.)   |
| Consensus            | Select     | LITE, PRO, AI, loader                    | Street consensus: Strong Buy / Hold / Sell / etc. |
| Ratings              | Rich text  | LITE, PRO, AI, loader                    | Text like `4.20/5.0 (12 analysts)` or `N/A`       |

> **Note:** `load_missing_stocks.py` uses the LITE bot’s `send_to_notion` function, so it writes the same columns **except** `Rank` (it passes `rank=None`).

---

## Column Definitions and Interpretation

### 1. Core Identification

- **Ticker (Title)**  
  Primary key for each row (e.g. `RELIANCE`, `SULA`). Use this to join with external data or charts.

- **Market Cap (Select)**  
  Buckets such as `Large Cap`, `Mid Cap`, `Small Cap`. Use this to:
  - Filter for only large caps (safer, more liquid), or
  - Hunt for multi-bagger potential in small caps.

- **Sector (Select)**  
  Sector or industry (e.g. `IT`, `Banks`, `FMCG`, `Pharma`). Useful for:
  - Sector rotation (e.g. favour sectors with many high-score names).
  - Ensuring diversification across sectors.

### 2. Price & Size

- **Price (₹) (Number)**  
  Latest price in INR. Mainly informational, but also useful to:
  - Sort by price level (e.g. avoid very low-priced names if desired).

- **Capital Market (₹) (Number)**  
  Approximate market capitalisation. Use this to:
  - Rank by absolute size within a sector.
  - Filter out illiquid micro-caps below your comfort threshold.

### 3. Technical & Ranking Metrics

- **Momentum (%) (Number)**  
  Recent percentage price change over a fixed look-back window.  
  - Positive & large → strong uptrend.  
  - Negative & large in magnitude → strong downtrend.

- **Volume Surge (Number)**  
  Ratio of current volume to average volume.  
  - `1.0` ≈ normal; `>1.5` means heavy trading interest.  
  - Combine with momentum to detect **high-conviction moves**.

- **Score (Number)**  
  Composite score from the ranking engine (momentum, volume and internal rules).  
  - Higher = more attractive according to your model.  
  - Use as your primary numeric ranking measure.

- **Rank (Number)**  
  The relative position of the stock in the universe (1 = best).  
  - Use to pick the **top N** candidates quickly (e.g. top 20 by rank).

- **Signal (Select)**  
  Human-friendly classification derived from the underlying metrics:  
  - `🚀 Strong Buy` – high score; strong positive setup.  
  - `👀 Watch` – interesting but not top-tier.  
  - `❄️ Neutral` – nothing special, mostly hold/ignore.  
  - `❄️ N/A` – insufficient or missing data.

- **Last Updated (Date)**  
  When the bots last refreshed the row. Use this to:
  - Filter to only recently updated names.
  - Detect stale data that should be refreshed.

### 4. News & Sentiment

- **News & Updates (Rich text)**  
  Concise concatenation of recent headlines and snippets, truncated to ~2000 characters.  
  - Gives fast context without opening an external news page.

- **News Sentiment (Select)**  
  Aggregate tone of recent news: typically `Positive`, `Negative`, or a neutral/other bucket.  
  - Positive + strong momentum often supports trend continuation.  
  - Negative + strong downtrend may indicate fundamentally-driven sell-offs.

- **News Type (Multi-select)**  
  Tags describing *what the news is about*: examples include `Earnings`, `Product`, `Regulatory`, `Debt`, `Management`, `M&A`, etc.  
  - Lets you focus on specific catalysts (e.g. only earnings-related moves).

### 5. Analyst Ratings

- **Consensus (Select)**  
  Aggregated Street view: `Strong Buy`, `Buy`, `Moderate Buy`, `Hold`, `Moderate Sell`, `Sell`, `Strong Sell`, `No Consensus`.  
  - High conviction (`Strong Buy` / `Buy`) with many analysts generally means strong institutional support.

- **Ratings (Rich text)**  
  Text such as `4.20/5.0 (12 analysts)` or `N/A`.  
  - Encodes both the average rating and coverage depth.  
  - Few analysts → the number is less reliable; many analysts → more robust consensus.

---

## Usage Notes and Screening Scenarios

This section shows practical ways to combine columns to find strong candidates.

### Scenario A – High-conviction momentum trades

Goal: find stocks with strong technicals and supportive news.

**Filter:**
- `Signal = 🚀 Strong Buy`
- `Momentum (%) > 0`
- `Volume Surge ≥ 1.5`
- `News Sentiment = Positive` (or at least not Negative)

**Interpretation:**
- Price is moving up with above-average volume (real interest, not noise).  
- Bot’s signal is top tier, and news tone is supportive → good for short‑ to medium‑term trades.

### Scenario B – Quality compounders with strong Street support

Goal: longer-term names with both technical and fundamental backing.

**Filter:**
- `Market Cap ∈ {Large Cap, Mid Cap}`
- `Signal ∈ {🚀 Strong Buy, 👀 Watch}`
- `Consensus ∈ {Strong Buy, Buy}`
- `Ratings` text shows rating ≥ ~4.0 with **analyst_count ≥ 10**

**Interpretation:**
- Solid businesses (larger caps) with constructive signals.  
- Many analysts agree it’s a buy → lower information risk.  
- Good candidates for core portfolio positions.

### Scenario C – Early-stage potential / small-cap ideas

Goal: find interesting smaller names that might become multi-baggers.

**Filter:**
- `Market Cap = Small Cap`
- `Signal ∈ {🚀 Strong Buy, 👀 Watch}`
- `Momentum (%) > 15` and `Volume Surge ≥ 1.5`
- `News Type` includes `Earnings` or `Product`

**Interpretation:**
- Smaller companies with strong recent moves and heavy volume.  
- Moves are driven by earnings or product news, not just rumours.  
- Higher risk; position sizing and risk control are important.

### Scenario D – Contrarian or turnaround candidates

Goal: stocks where the bots are positive but analysts are cautious, or vice versa.

**Filter 1 (technical > analysts):**
- `Signal = 🚀 Strong Buy`
- `Consensus ∈ {Hold, Sell, Strong Sell}` or `No Consensus`

**Filter 2 (analysts > technicals):**
- `Signal = ❄️ Neutral`
- `Consensus ∈ {Strong Buy, Buy}`

**Interpretation:**
- Filter 1: price action is strong but analysts are sceptical → potential **contrarian** trades, but higher risk.  
- Filter 2: analysts like the name but technicals haven’t moved yet → possible **early entry** before the move, or a value trap; investigate deeper.

### Scenario E – Sector rotation / thematic baskets

Goal: identify strong names within a sector or theme.

**Filter:**
- `Sector = <target sector>` (e.g. `Banks`, `IT`)
- Sort by `Score` or `Rank` ascending
- Optionally require `Signal ∈ {🚀 Strong Buy, 👀 Watch}`

**Interpretation:**
- Gives a ranked list of leaders in that sector.  
- Use this for building themed baskets (e.g. top 10 banks, top 15 IT names).

### Scenario F – Quiet compounders (low news noise)

Goal: stable names that perform without constant news flow.

**Filter:**
- `Signal ∈ {🚀 Strong Buy, 👀 Watch}`
- `News & Updates` is empty or very short
- `News Sentiment` not strongly Negative
- `Consensus ∈ {Buy, Strong Buy}` (optional)

**Interpretation:**
- Fewer news events, but good technical and/or analyst outlook.  
- Often suitable for lower-stress, longer-term holdings.

---

## Notion Views Cookbook

The table below gives **ready-made Notion views** you can create using the
schema above. Use these as templates and adjust the exact thresholds to your
risk profile.

| View name                      | Cadence       | Core filter (Notion)                                                                                           | Purpose / Notes                                                                                 |
|--------------------------------|--------------|-----------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| Daily Momentum Picks           | Daily        | `Signal = "🚀 Strong Buy" AND Momentum (%) > 0 AND Volume Surge >= 1.5`                                         | High-conviction breakouts with strong volume; good for short‑ to medium‑term trades.           |
| Weekly Large-Cap Review        | Weekly       | `Market Cap ∈ ["Large Cap", "Mid Cap"] AND Signal ∈ ["🚀 Strong Buy", "👀 Watch"]`                          | Focus on quality larger names; good for core portfolio adjustments.                            |
| Small-Cap Breakout Radar       | 2–3× / week  | `Market Cap = "Small Cap" AND Momentum (%) >= 15 AND Volume Surge >= 1.5`                                      | Aggressive ideas with strong moves; higher risk, size positions smaller.                       |
| Contrarian Watchlist           | Weekly       | `Signal = "🚀 Strong Buy" AND Consensus ∈ ["Hold", "Sell", "Strong Sell", "No Consensus"]`                | Technically strong but Street is cautious; investigate story before acting.                    |
| Analyst-Favoured, Not Moving   | Weekly       | `Signal = "❄️ Neutral" AND Consensus ∈ ["Strong Buy", "Buy"]`                                               | Names analysts like but price hasn’t moved yet; possible early entries or value traps.         |
| Sector Leaders (e.g. Banks)    | Weekly       | `Sector = "Banks" AND Signal ∈ ["🚀 Strong Buy", "👀 Watch"]` (sort by Score / Rank)                        | Build sector baskets; repeat view per sector (IT, FMCG, etc.).                                 |
| Quiet Compounders              | Monthly      | `Signal ∈ ["🚀 Strong Buy", "👀 Watch"] AND News & Updates is empty AND News Sentiment != "Negative"`        | Lower-news, steady names for long-term holds; fewer headline risks.                            |
| High-Conviction Street Support | Weekly       | `Signal = "🚀 Strong Buy" AND Consensus ∈ ["Strong Buy", "Buy"] AND Ratings contains "(≥ 10 analysts)"`    | Strong alignment between bots and analysts; good for higher-conviction allocations.            |
| Recently Updated Ideas         | Ad hoc       | `Last Updated within past 1–3 days AND Signal ∈ ["🚀 Strong Buy", "👀 Watch"]`                                | Quickly see what changed most recently across the universe.                                    |
| News-Driven Opportunities      | Daily/News   | `News Sentiment = "Positive" AND News Type contains "Earnings" OR "Product"`                                | Moves backed by concrete positive catalysts (results or launches), not only rumours.           |

> **Tip:** In Notion, implement these as separate **views** on the same
> database: one board/table per strategy. You can also add sorts on `Score`,
> `Rank`, or `Last Updated` to refine ordering.

---

## Summary

- The bots share a **single, consistent Notion schema** so you can run LITE, PRO, AI, and the loader against the same database.
- Core columns (`Score`, `Rank`, `Signal`, `Momentum (%)`, `Volume Surge`) drive the ranking; news and analyst columns provide context.
- Use the scenarios and cookbook views above as starting points and adjust filters to match your risk profile and investment style.
