"""
LIGHTWEIGHT VERSION - Market Bot (No AI Sentiment)
Uses only technical indicators (momentum & volume) - NO MODEL DOWNLOAD NEEDED
Runs instantly! Use this if FinBERT download is too slow.
Includes intelligent multi-factor ranking system.
"""

import os
import sys
import time
import re
from datetime import datetime
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
import threading

import requests
import pandas as pd
import yfinance as yf

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Setup centralized logging
from src.config.logging_config import setup_bot_logging
logger = setup_bot_logging("market_bot_lite")

# Import stock data (prefer 650-stock version if available)
try:
    from data.nse_stocks_650 import (
        get_all_stocks_with_classification,
        get_validated_stocks,
        get_current_ticker,
        is_delisted
    )
except ImportError:
    print("⚠️  Stock data module not found. Please check data/nse_stocks_650.py")
    get_validated_stocks = None
    get_all_stocks_with_classification = None
    get_current_ticker = lambda x: x
    is_delisted = lambda x: False

# Import comprehensive news sources
try:
    from src.core.news_aggregator import fetch_comprehensive_news as fetch_news_comprehensive
    HAS_COMPREHENSIVE_NEWS = True
except ImportError:
    HAS_COMPREHENSIVE_NEWS = False
    print("⚠️  Comprehensive news module not found. Using basic news.")

# Import analyst ratings
try:
    from src.core.analyst_ratings import aggregate_all_analyst_ratings
    HAS_ANALYST_RATINGS = True
except ImportError:
    HAS_ANALYST_RATINGS = False
    print("⚠️  Analyst ratings module not found. Ratings will not be included.")

# Import intelligent ranking engine
try:
    from src.core.ranking_engine import rank_stocks
    HAS_RANKING_ENGINE = True
except ImportError:
    HAS_RANKING_ENGINE = False
    print("⚠️  Ranking engine not found. Using serial ranking.")

# Environment Configuration
try:
    from src.config.env_config import (
        NOTION_TOKEN, DATABASE_ID,
        validate_notion_config,
        get_notion_headers
    )
except ImportError:
    print("⚠️  Environment config not found. Loading from dotenv directly...")
    from dotenv import load_dotenv
    load_dotenv()
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    DATABASE_ID = os.getenv("DATABASE_ID")

# 1. AUTHENTICATION & VALIDATION
try:
    if 'validate_notion_config' in dir():
        validate_notion_config()
    elif not NOTION_TOKEN or not DATABASE_ID:
        print("CRITICAL ERROR: NOTION_TOKEN or DATABASE_ID missing from environment")
        print("Please create a .env file from .env.example and set your credentials")
        exit(1)
except ValueError as e:
    print(f"Configuration error: {e}")
    exit(1)

# News sentiment keywords
POSITIVE_KEYWORDS = [
    "wins",
    "won",
    "award",
    "beats",
    "surges",
    "jumps",
    "rallies",
    "gains",
    "record",
    "profit",
    "growth",
    "dividend",
    "expansion",
    "order",
    "contract",
    "upgrade",
    "acquisition",
    "launch",
    "partnership",
]

NEGATIVE_KEYWORDS = [
    "falls",
    "drops",
    "crashes",
    "plunges",
    "loss",
    "downgrade",
    "weak",
    "concern",
    "debt",
    "penalty",
    "resignation",
    "lawsuit",
    "decline",
]

# News type classification keywords
NEWS_TYPE_KEYWORDS = {
    "Earnings": [
        "earnings",
        "quarter",
        "q1",
        "q2",
        "q3",
        "q4",
        "revenue",
        "profit",
        "loss",
        "results",
    ],
    "Product": [
        "launch",
        "product",
        "unveils",
        "introduces",
        "release",
        "model",
        "variant",
    ],
    "Legal": [
        "lawsuit",
        "court",
        "legal",
        "case",
        "trial",
        "settlement",
        "penalty",
        "fine",
    ],
    "M&A": [
        "merger",
        "acquisition",
        "acquires",
        "deal",
        "buyout",
        "takeover",
        "stake",
    ],
    "Management": [
        "ceo",
        "cfo",
        "resign",
        "appoint",
        "director",
        "board",
        "executive",
    ],
    "Dividend": [
        "dividend",
        "payout",
        "shareholder",
        "distribution",
    ],
    "Regulatory": [
        "sebi",
        "regulator",
        "compliance",
        "violation",
        "probe",
        "investigation",
    ],
    "Expansion": [
        "expansion",
        "plant",
        "facility",
        "capacity",
        "invest",
        "capex",
    ],
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Reuse a single HTTP session for all outbound requests (NSE, Google News,
# Notion). This significantly reduces connection setup overhead across
# hundreds of requests when processing the full stock universe.
SESSION = requests.Session()

print("✅ Lightweight Market Bot Started (No AI - Technical Analysis Only)")


def fetch_news(ticker: str):
    """Fetch news from Yahoo Finance and Google News."""

    try:
        # Use current ticker (handles renamed companies)
        current_ticker = get_current_ticker(ticker)

        stock = yf.Ticker(f"{current_ticker}.NS")
        yf_news = stock.news or []

        # Get company info
        info = stock.info
        company_name = info.get("longName") or info.get("shortName") or ticker

        all_news = []

        # Yahoo Finance news
        for item in yf_news[:8]:
            title = item.get("title", "")
            pub_time = item.get("providerPublishTime", 0)
            date = (
                datetime.fromtimestamp(pub_time).strftime("%d-%b")
                if pub_time
                else "Recent"
            )
            all_news.append({"title": title, "date": date})

        # Google News RSS
        try:
            url = (
                "https://news.google.com/rss/search?q="
                f"{quote(company_name)}+stock+india&hl=en-IN&gl=IN&ceid=IN:en"
            )
            response = SESSION.get(
                url,
                timeout=5,
                headers={"User-Agent": USER_AGENT},
            )

            if response.status_code == 200:
                titles = re.findall(
                    r"<title><!\[CDATA\[(.*?)\]\]></title>", response.text
                )
                if not titles:
                    titles = re.findall(r"<title>(.*?)</title>", response.text)

                for title in titles[1:4]:
                    all_news.append({"title": title, "date": "Recent"})
        except Exception:
            # Ignore Google News failures; Yahoo Finance news is primary
            pass

        # Return top 3 news
        if all_news:
            news_items = []
            for news in all_news[:3]:
                title = re.sub(r"\s+", " ", news["title"]).strip()
                title = re.sub(r"&amp;", "&", title)
                if len(title) > 150:
                    title = title[:147] + "..."
                news_items.append(f"[{news['date']}] {title}")

            return " | ".join(news_items), [n["title"] for n in all_news[:5]]

        return None, []

    except Exception as e:
        print(f"⚠️  Error fetching news for {ticker}: {str(e)}")
        return None, []


def analyze_news_sentiment(news_text: str) -> str:
    """Analyze news sentiment using keywords."""

    if not news_text:
        return "Neutral"

    news_lower = news_text.lower()
    pos_count = sum(1 for word in POSITIVE_KEYWORDS if word in news_lower)
    neg_count = sum(1 for word in NEGATIVE_KEYWORDS if word in news_lower)

    if pos_count > neg_count:
        return "Positive"
    if neg_count > pos_count:
        return "Negative"
    return "Neutral"


def classify_news_type(news_text: str):
    """Classify news into types using keywords."""

    if not news_text:
        return []

    news_lower = news_text.lower()
    types = []

    for news_type, keywords in NEWS_TYPE_KEYWORDS.items():
        if any(keyword in news_lower for keyword in keywords):
            types.append(news_type)

    # Return unique types, max 3
    return list(set(types))[:3] if types else []


def fetch_price_from_nse(symbol: str):
    """Fetch latest price and basic info from NSE's official quote API.

    Returns a dict with keys: price, pchange, volume, sector, market_cap
    or None if the request fails.
    """

    base_url = "https://www.nseindia.com/api/quote-equity"
    params = {"symbol": symbol}
    headers = {
        "User-Agent": USER_AGENT,
        "Referer": f"https://www.nseindia.com/get-quotes/equity?symbol={quote(symbol)}",
        "Accept": "application/json, text/plain, */*",
    }

    try:
        resp = SESSION.get(base_url, params=params, headers=headers, timeout=8)
        if resp.status_code != 200:
            print(f"   ⚠️ NSE quote HTTP {resp.status_code} for {symbol}")
            return None

        data = resp.json()
        price_info = data.get("priceInfo") or {}
        last_price = price_info.get("lastPrice")
        if last_price is None:
            return None

        pchange = price_info.get("pChange")

        pre_open = data.get("preOpenMarket") or {}
        volume = None
        if isinstance(pre_open, dict):
            volume = pre_open.get("totalTradedVolume")
        if volume is None:
            volume = price_info.get("totalTradedVolume")

        industry_info = data.get("industryInfo") or {}
        info = data.get("info") or {}
        sector = industry_info.get("sector") or info.get("industry") or "Unknown"

        sec_info = data.get("securityInfo") or {}
        issued_size = sec_info.get("issuedSize")
        market_cap = None
        try:
            if issued_size is not None:
                market_cap_raw = float(last_price) * float(issued_size)
                # Convert to ₹ Crores (same convention as yfinance branch)
                market_cap = round(market_cap_raw / 10000000, 2)
        except Exception:
            market_cap = None

        return {
            "price": float(last_price),
            "pchange": float(pchange) if pchange is not None else None,
            "volume": float(volume) if volume is not None else None,
            "sector": sector,
            "market_cap": market_cap,
        }
    except Exception as e:
        print(f"   ⚠️ NSE quote failed for {symbol}: {e}")
        return None


def get_market_intelligence_from_nse(symbol: str, cap_size: str):
    """Fallback: build intelligence snapshot using NSE quote data.

    This is used when yfinance cannot provide a usable price history.
    """

    nse = fetch_price_from_nse(symbol)
    if not nse:
        return None

    latest_price = nse["price"]
    pchange = nse["pchange"]
    market_cap = nse["market_cap"]
    sector = nse["sector"]

    # Use daily percentage change as a short-term momentum proxy
    if pchange is not None:
        momentum = pchange / 100.0
    else:
        momentum = 0.0

    # Without a long history we treat volume as neutral (1.0x)
    vol_surge = 1.0

    if pchange is not None:
        simple_sentiment = 1.0 if momentum > 0.02 else (-1.0 if momentum < -0.02 else 0.0)
    else:
        simple_sentiment = 0.0

    # Fetch news (same logic as primary path)
    news_text = None
    news_titles = []
    news_sentiment = None
    news_types = []

    try:
        if HAS_COMPREHENSIVE_NEWS:
            news_text, news_titles = fetch_news_comprehensive(symbol)
        else:
            news_text, news_titles = fetch_news(symbol)

        if news_text:
            news_sentiment = analyze_news_sentiment(news_text)
            news_types = classify_news_type(news_text)
    except Exception as e:
        print(f"   ⚠️  Failed to fetch news (NSE fallback): {str(e)}")

    print(
        f"📊 {symbol}: (NSE) Price=₹{latest_price:.2f}, "
        f"Momentum≈{momentum*100:.1f}% (1D), Volume≈{vol_surge:.2f}x, "
        f"Trend={'📈' if simple_sentiment > 0 else '📉' if simple_sentiment < 0 else '➡️'}",
    )

    return {
        "ticker": symbol,
        "cap": cap_size,
        "sector": sector,
        "price": latest_price,
        "market_cap": market_cap,
        "mom": momentum,
        "vol": vol_surge,
        "sent": simple_sentiment,
        "news": news_text,
        "news_sentiment": news_sentiment,
        "news_types": news_types,
        "has_data": True,
    }


def get_market_intelligence(symbol: str, cap_size: str):
    """Fetch market intelligence for a stock using yfinance with NSE fallback."""

    try:
        # Use current ticker (handles renamed companies)
        current_symbol = get_current_ticker(symbol)

        # Check if delisted or pump & dump
        if is_delisted(current_symbol):
            logger.debug(f"{symbol} is delisted, skipping")
            return None

        stock = yf.Ticker(f"{current_symbol}.NS")
        df = stock.history(period="7mo", auto_adjust=True)

        # Check if we have sufficient data from yfinance
        has_data = not df.empty and len(df) >= 20

        if has_data:
            # Normal case: sufficient data available
            latest_price = df["Close"].iloc[-1]
            momentum = (df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0]
            avg_vol = df["Volume"].iloc[:-1].tail(20).mean()
            vol_surge = df["Volume"].iloc[-1] / avg_vol if avg_vol > 0 else 1.0
            recent_change = (
                df["Close"].iloc[-1] - df["Close"].iloc[-6]
            ) / df["Close"].iloc[-6]
            simple_sentiment = (
                1.0 if recent_change > 0.02 else (-1.0 if recent_change < -0.02 else 0.0)
            )

            # Guard against broken yfinance data returning NaN values.
            # Treat such cases as "no usable data" and fall back to NSE.
            if pd.isna(latest_price) or pd.isna(momentum) or pd.isna(vol_surge):
                print(f"⚠️  {symbol}: yfinance returned NaN values, trying NSE fallback...")
                alt_metrics = get_market_intelligence_from_nse(symbol, cap_size)
                if alt_metrics:
                    return alt_metrics

                # If NSE also fails, mark as no-data stock with safe defaults.
                print(
                    f"⚠️  {symbol}: No usable data from any source - adding with NA values"
                )
                return {
                    "ticker": symbol,
                    "cap": cap_size,
                    "sector": "Unknown",
                    "price": None,
                    "market_cap": None,
                    "mom": 0.0,
                    "vol": 0.0,
                    "sent": 0.0,
                    "news": None,
                    "news_sentiment": None,
                    "news_types": [],
                    "has_data": False,
                }

            # Get market capitalization and sector
            market_cap = None
            sector = "Unknown"
            try:
                info = stock.info
                market_cap_raw = info.get("marketCap", None)
                if market_cap_raw:
                    market_cap = round(market_cap_raw / 10000000, 2)

                # Get sector information
                sector = info.get("sector", info.get("industry", "Unknown"))
            except Exception:
                pass

            # Fetch news
            news_text = None
            news_titles = []
            news_sentiment = None
            news_types = []

            try:
                if HAS_COMPREHENSIVE_NEWS:
                    # Use comprehensive news sources (70+ sources)
                    news_text, news_titles = fetch_news_comprehensive(symbol)
                else:
                    # Use basic news (Yahoo + Google)
                    news_text, news_titles = fetch_news(symbol)

                if news_text:
                    news_sentiment = analyze_news_sentiment(news_text)
                    news_types = classify_news_type(news_text)
            except Exception as e:
                print(f"   ⚠️  Failed to fetch news: {str(e)}")

            print(
                f"📊 {symbol}: Price=₹{latest_price:.2f}, "
                f"Momentum={momentum*100:.1f}%, Volume={vol_surge:.2f}x, "
                f"Trend={'📈' if simple_sentiment > 0 else '📉' if simple_sentiment < 0 else '➡️'}",
            )

            return {
                "ticker": symbol,
                "cap": cap_size,
                "sector": sector,
                "price": latest_price,
                "market_cap": market_cap,
                "mom": momentum,
                "vol": vol_surge,
                "sent": simple_sentiment,
                "news": news_text,
                "news_sentiment": news_sentiment,
                "news_types": news_types,
                "has_data": True,
            }

        # yfinance returned no usable data – try alternate sources (NSE)
        print(f"⚠️  {symbol}: No data from yfinance, trying NSE fallback...")
        alt_metrics = get_market_intelligence_from_nse(symbol, cap_size)
        if alt_metrics:
            return alt_metrics

        # Still nothing: add with NA/default values
        print(f"⚠️  {symbol}: No data from any source - adding with NA values")
        return {
            "ticker": symbol,
            "cap": cap_size,
            "sector": "Unknown",
            "price": None,
            "market_cap": None,
            "mom": 0.0,
            "vol": 0.0,
            "sent": 0.0,
            "news": None,
            "news_sentiment": None,
            "news_types": [],
            "has_data": False,
        }

    except Exception as e:
        # yfinance raised an exception – attempt NSE-based fallback
        print(f"⚠️  {symbol}: yfinance error '{e}'. Trying NSE fallback...")
        alt_metrics = get_market_intelligence_from_nse(symbol, cap_size)
        if alt_metrics:
            return alt_metrics

        print(f"⚠️  {symbol}: Error - adding with NA values")
        return {
            "ticker": symbol,
            "cap": cap_size,
            "sector": "Unknown",
            "price": None,
            "market_cap": None,
            "mom": 0.0,
            "vol": 0.0,
            "sent": 0.0,
            "news": None,
            "news_sentiment": None,
            "news_types": [],
            "has_data": False,
        }


def send_to_notion(data: dict, rank: int | None = None) -> None:
    """Send a single stock's data to the Notion database."""

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    # Determine signal (use "N/A" if no data)
    if not data.get("has_data", True):
        signal = "❄️ N/A"
        score = 0
    else:
        signal = "❄️ Neutral"
        if data["mom"] > 0.10 and data["vol"] > 1.2:
            signal = "🚀 Strong Buy"
        elif data["mom"] > 0.05 or data["vol"] > 1.1:
            signal = "👀 Watch"

        score = 0
        if signal == "🚀 Strong Buy":
            score += 1000
        elif signal == "👀 Watch":
            score += 500
        score += data["mom"] * 500
        score += data["vol"] * 50
        score = round(score, 2)

    payload: dict = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Ticker": {"title": [{"text": {"content": data["ticker"]}}]},
            "Market Cap": {"select": {"name": data["cap"]}},
            "Sector": {"select": {"name": data.get("sector", "Unknown")}},
            "Sentiment": {"number": data["sent"]},
            "Momentum (%)": {"number": data["mom"]},
            "Volume Surge": {"number": round(data["vol"], 2)},
            "Score": {"number": score},
            "Signal": {"select": {"name": signal}},
            "Last Updated": {"date": {"start": pd.Timestamp.now().isoformat()}},
        },
    }

    # Add price only if available
    if data.get("price") is not None:
        payload["properties"]["Price (₹)"] = {
            "number": round(data["price"], 2)
        }

    # Add rank if provided
    if rank is not None:
        payload["properties"]["Rank"] = {"number": rank}

    # Add market cap if available
    if data.get("market_cap") is not None:
        payload["properties"]["Capital Market (₹)"] = {
            "number": data["market_cap"]
        }

    # Add news if available
    if data.get("news"):
        payload["properties"]["News & Updates"] = {
            "rich_text": [{"text": {"content": data["news"][:2000]}}]
        }

    # Add news sentiment if available
    if data.get("news_sentiment"):
        payload["properties"]["News Sentiment"] = {
            "select": {"name": data["news_sentiment"]}
        }

    # Add news types if available
    if data.get("news_types"):
        payload["properties"]["News Type"] = {
            "multi_select": [
                {"name": news_type} for news_type in data["news_types"]
            ]
        }

    # Add analyst ratings if available
    if HAS_ANALYST_RATINGS and data.get("has_data", True):
        # Only fetch ratings for stocks with data
        try:
            print(f"   📊 Fetching analyst ratings for {data['ticker']}...")
            ratings_data = aggregate_all_analyst_ratings(data["ticker"])
            if ratings_data and ratings_data.get("has_data"):
                payload["properties"]["Consensus"] = {
                    "select": {"name": ratings_data["consensus"]}
                }
                rating_text = (
                    f"{ratings_data['rating_numeric']:.2f}/5.0 "
                    f"({ratings_data['analyst_count']} analysts)"
                )
                payload["properties"]["Ratings"] = {
                    "rich_text": [{"text": {"content": rating_text}}]
                }
                print(
                    f"   ✅ Ratings: {ratings_data['consensus']} | {rating_text}"
                )
            else:
                # No analyst data
                payload["properties"]["Consensus"] = {
                    "select": {"name": "No Consensus"}
                }
                payload["properties"]["Ratings"] = {
                    "rich_text": [{"text": {"content": "N/A"}}]
                }
                print(f"   ℹ️  No analyst ratings available")
        except Exception as e:
            print(f"   ⚠️  Failed to fetch ratings: {str(e)}")
            # Still set default values even if fetch fails
            payload["properties"]["Consensus"] = {
                "select": {"name": "No Consensus"}
            }
            payload["properties"]["Ratings"] = {
                "rich_text": [{"text": {"content": "N/A"}}]
            }

    response = SESSION.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"❌ Notion Error for {data['ticker']}: {response.text}")
    else:
        print(
            f"✅ {data['ticker']} → Notion ("
            f"{signal}, Score: {score:.0f}, Rank: {rank if rank else 'N/A'})"
        )


if __name__ == "__main__":
    start_time = time.time()

    print("\n" + "=" * 70)
    print("📈 MARKET INTELLIGENCE BOT - LITE VERSION")
    print("=" * 70)
    print("🏆 Intelligent Multi-Factor Ranking: ENABLED")
    if HAS_RANKING_ENGINE:
        print("✅ Using optimized ranking engine")
    else:
        print("⚠️  Ranking engine not available - using serial ranking")
    print("=" * 70 + "\n")

    # Load all NSE stocks (Nifty 100, Midcap 150, Smallcap 250)
    if get_all_stocks_with_classification is None:
        print("❌ ERROR: Stock data module not available!")
        print("Please ensure data/nse_stocks_650.py exists and is accessible.")
        raise SystemExit(1)

    watchlist = get_all_stocks_with_classification()

    print(f"📊 Total stocks to analyze: {len(watchlist)}")
    print(f"⏱️  Estimated time: ~{len(watchlist) * 2 // 60} minutes\n")

    # Statistics tracking
    stats = {
        "total": len(watchlist),
        "processed": 0,
        "errors": 0,
        "success": 0,
        "strong_buy": 0,
        "watch": 0,
        "neutral": 0,
    }

    # =====================================================================
    # PHASE 1: COLLECT ALL STOCK DATA (CONCURRENT)
    # =====================================================================
    print("\n" + "=" * 70)
    print("📊 PHASE 1: Collecting market intelligence...")
    print("=" * 70 + "\n")

    # Use a results list indexed by original position so that, even with
    # concurrency, the final ordering of all_stocks_data matches the
    # original watchlist order. This preserves downstream behaviour,
    # including the serial ranking fallback when the ranking engine is
    # unavailable.
    results: list[dict | None] = [None] * len(watchlist)
    lock = threading.Lock()

    # Conservative level of concurrency: we are network-bound (yfinance,
    # NSE, news), so a small thread pool significantly reduces total
    # runtime without overwhelming external services.
    max_workers = min(8, max(2, len(watchlist)))

    def process_stock(idx: int, ticker: str, cap: str) -> None:
        """Worker function to fetch metrics for a single stock.

        Logs progress similarly to the original implementation and updates
        shared stats/results under a lock to remain thread-safe.
        """

        total = len(watchlist)
        print(f"[{idx}/{total}] 🔍 Analyzing {ticker}...")

        try:
            metrics = get_market_intelligence(ticker, cap)
            with lock:
                if metrics:
                    results[idx - 1] = metrics
                    stats["processed"] += 1
                else:
                    stats["errors"] += 1
        except Exception as e:  # pragma: no cover - defensive
            print(f"❌ Error processing {ticker}: {str(e)}")
            with lock:
                stats["errors"] += 1
        finally:
            # Preserve the original light rate limiting behaviour per
            # stock while still benefiting from concurrency.
            time.sleep(1)

            # Progress update roughly every 50 submitted stocks, using the
            # original index for a similar user-facing message.
            if idx % 50 == 0:
                elapsed = time.time() - start_time
                rate = idx / elapsed if elapsed > 0 else 1.0
                remaining = (total - idx) / rate if rate > 0 else 0.0
                with lock:
                    collected = stats["processed"]
                print(
                    f"📈 Progress: {idx}/{total}, "
                    f"~{remaining/60:.1f} min remaining, Collected: {collected}"
                )

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for idx, (ticker, cap) in enumerate(watchlist, 1):
            executor.submit(process_stock, idx, ticker, cap)

    # Filter out any stocks that failed to produce metrics
    all_stocks_data: list[dict] = [m for m in results if m is not None]

    # =====================================================================
    # PHASE 2: INTELLIGENT RANKING
    # =====================================================================
    print("\n" + "=" * 70)
    print("🏆 PHASE 2: Calculating intelligent rankings...")
    print("=" * 70 + "\n")

    if HAS_RANKING_ENGINE and all_stocks_data:
        ranked_stocks = rank_stocks(all_stocks_data)
        print(
            f"✅ Ranked {len(ranked_stocks)} stocks using intelligent "
            f"multi-factor algorithm"
        )
        top_3 = ", ".join(
            [f"{s['ticker']}#{s['rank']}" for s in ranked_stocks[:3]]
        )
        print(f"   🥇 Top 3: {top_3}")
    else:
        if not HAS_RANKING_ENGINE:
            print("⚠️  Ranking engine not available - using serial ranking")
        ranked_stocks = all_stocks_data
        for i, stock in enumerate(ranked_stocks, 1):
            stock["rank"] = i

    # =====================================================================
    # PHASE 3: SEND TO NOTION WITH RANKS
    # =====================================================================
    print("\n" + "=" * 70)
    print("📤 PHASE 3: Sending ranked data to Notion...")
    print("=" * 70 + "\n")

    # Extra safety: wrap the entire Notion upload phase so that
    # a single unexpected error cannot terminate the whole run.
    try:
        for stock in ranked_stocks:
            try:
                send_to_notion(stock, rank=stock.get("rank"))
                stats["success"] += 1

                # Track signals
                signal = stock.get("signal", "❄️ Neutral")
                if signal == "🚀 Strong Buy":
                    stats["strong_buy"] += 1
                elif signal == "👀 Watch":
                    stats["watch"] += 1
                else:
                    stats["neutral"] += 1

                time.sleep(0.5)  # Light rate limiting for Notion

            except Exception as e:
                # Be defensive when accessing ticker to avoid KeyError
                ticker = (
                    stock.get("ticker")
                    or stock.get("symbol")
                    or "UNKNOWN"
                )
                print(f"❌ Error sending {ticker} to Notion: {str(e)}")
                stats["errors"] += 1

    except Exception as e:
        # Catch any critical failure affecting the whole phase
        print(f"🔥 CRITICAL: PHASE 3 (Notion upload) failed: {str(e)}")
        stats["errors"] += 1

    # =====================================================================
    # FINAL STATISTICS
    # =====================================================================
    elapsed_time = time.time() - start_time

    print("\n" + "=" * 70)
    print("📊 ANALYSIS COMPLETE - FINAL STATISTICS")
    print("=" * 70)
    print("")
    print("📈 PROCESSING SUMMARY:")
    print(f"   Total Stocks: {stats['total']}")
    print(f"   ✅ Processed: {stats['processed']}")
    print(f"   ✅ Sent to Notion: {stats['success']}")
    print(f"   ❌ Errors: {stats['errors']}")
    print("")
    print("🎯 SIGNALS BREAKDOWN:")
    print(f"   🚀 Strong Buy: {stats['strong_buy']}")
    print(f"   👀 Watch: {stats['watch']}")
    print(f"   ❄️ Neutral: {stats['neutral']}")
    print("")
    print("⏱️  PERFORMANCE:")
    print(f"   Total Time: {elapsed_time/60:.1f} minutes")
    print(
        f"   Average: {elapsed_time / max(stats['processed'], 1):.1f}s per stock"
    )
    print("")
    if HAS_RANKING_ENGINE:
        print("🏆 RANKING: Intelligent multi-factor ranking applied")
    else:
        print(
            "⚠️  RANKING: Serial ranking used (install ranking engine for "
            "intelligent ranking)"
        )
    print("=" * 70)
    print("\n💡 Tip: For AI sentiment analysis, use 'market_bot_ai.py'")
    print("   (Requires one-time setup with setup-models.py)")
