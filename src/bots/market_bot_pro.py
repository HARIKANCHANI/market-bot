#!/usr/bin/env python3
"""MARKET INTELLIGENCE BOT - PROFESSIONAL VERSION

Production-grade market bot with news aggregation, keyword-based
sentiment, analyst ratings, and intelligent multi-factor ranking.
Uses yfinance as primary data source with NSE quote API fallback.
"""

from __future__ import annotations

import os
import re
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor
import threading

import requests
import yfinance as yf
from urllib.parse import quote


# ---------------------------------------------------------------------------
# Python path setup
# ---------------------------------------------------------------------------

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Setup centralized logging
from src.config.logging_config import setup_bot_logging
logger = setup_bot_logging("market_bot_pro")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# News configuration: choose coverage strategy
USE_COMPREHENSIVE_NEWS = True
"""If True, use 70+ sources via news_aggregator; else use basic Yahoo+Google."""


# Analyst ratings
try:
    from src.core.analyst_ratings import aggregate_all_analyst_ratings

    HAS_ANALYST_RATINGS = True
except ImportError:  # pragma: no cover - defensive
    HAS_ANALYST_RATINGS = False
    print("⚠️  Analyst ratings module not found. Ratings will not be included.")


# Comprehensive news aggregator
if USE_COMPREHENSIVE_NEWS:
    try:
        from src.core.news_aggregator import fetch_comprehensive_news

        HAS_COMPREHENSIVE_NEWS = True
        print("✅ Comprehensive news aggregator loaded (70+ sources)")
    except ImportError:  # pragma: no cover - defensive
        HAS_COMPREHENSIVE_NEWS = False
        print("⚠️  Comprehensive news module not found. Falling back to basic news.")
        print("   Install requirements: pip install beautifulsoup4")
else:
    HAS_COMPREHENSIVE_NEWS = False
    print("ℹ️  Using basic news sources (Yahoo + Google) - configured for reliability")


# Intelligent ranking engine
try:
    from src.core.ranking_engine import rank_stocks

    HAS_RANKING_ENGINE = True
except ImportError:  # pragma: no cover - defensive
    HAS_RANKING_ENGINE = False
    print("⚠️  Ranking engine not found. Using serial ranking.")


# Stock universe
try:
    from data.nse_stocks_650 import (
        get_all_stocks_with_classification,
        get_validated_stocks,
        get_current_ticker,
        is_delisted
    )
except ImportError:  # pragma: no cover - defensive
    print("⚠️  Stock data module not found. Please check data/nse_stocks_650.py")
    get_current_ticker = lambda x: x
    is_delisted = lambda x: False
    get_validated_stocks = None
    get_all_stocks_with_classification = None


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




# Valid Notion sectors - maps yfinance sectors to Notion select options
VALID_NOTION_SECTORS = {
    # Technology
    "Technology": "Technology",
    "Communication Services": "Technology",
    "Telecommunication Services": "Technology",
    "Information Technology": "Technology",
    "Software": "Technology",

    # Financial Services
    "Financial Services": "Financial Services",
    "Financial": "Financial Services",
    "Banks": "Financial Services",
    "Insurance": "Financial Services",

    # Healthcare
    "Healthcare": "Healthcare",
    "Pharmaceuticals": "Healthcare",
    "Biotechnology": "Healthcare",
    "Medical Devices": "Healthcare",

    # Consumer
    "Consumer Cyclical": "Consumer Cyclical",
    "Consumer Defensive": "Consumer Defensive",
    "Consumer Goods": "Consumer Defensive",
    "Retail": "Consumer Cyclical",

    # Industrials
    "Industrials": "Industrials",
    "Industrial": "Industrials",
    "Industrial Goods": "Industrials",
    "Machinery": "Industrials",
    "Construction": "Industrials",

    # Energy
    "Energy": "Energy",
    "Oil & Gas": "Energy",
    "Utilities": "Energy",

    # Basic Materials
    "Basic Materials": "Basic Materials",
    "Materials": "Basic Materials",
    "Metals & Mining": "Basic Materials",
    "Chemicals": "Basic Materials",

    # Real Estate
    "Real Estate": "Real Estate",
}

def validate_sector(sector_name):
    """
    Validate and normalize sector name for Notion.
    Maps yfinance sector names to valid Notion select options.
    Returns 'Unknown' if sector is not recognized.

    Args:
        sector_name: Raw sector name from yfinance

    Returns:
        Valid Notion sector name or 'Unknown'
    """
    if not sector_name or sector_name == "Unknown":
        return "Unknown"

    # Direct match
    if sector_name in VALID_NOTION_SECTORS:
        return VALID_NOTION_SECTORS[sector_name]

    # Try partial match (case-insensitive)
    from src.config.logging_config import setup_bot_logging
    logger = setup_bot_logging("market_bot_pro")
    sector_lower = sector_name.lower()
    for key, value in VALID_NOTION_SECTORS.items():
        if key.lower() in sector_lower or sector_lower in key.lower():
            logger.debug(f"Mapped sector '{sector_name}' -> '{value}'")
            return value

    # No match found - default to Unknown
    logger.warning(f"Unknown sector '{sector_name}' mapped to 'Unknown'")
    return "Unknown"

# Validate configuration
try:
    if 'validate_notion_config' in dir():
        validate_notion_config()
    elif not NOTION_TOKEN or not DATABASE_ID:
        logger.error("CRITICAL ERROR: NOTION_TOKEN or DATABASE_ID missing from environment")
        logger.error("Please create a .env file from .env.example and set your credentials")
        exit(1)
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    exit(1)

# Notion headers
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


# News sentiment and classification keywords
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

# Single shared HTTP session for all outbound requests (NSE, Google News,
# Notion). This avoids the overhead of creating a new TCP connection for
# every request across hundreds of stocks.
SESSION = requests.Session()


# ---------------------------------------------------------------------------
# Data fetching helpers (NSE + yfinance)
# ---------------------------------------------------------------------------


def fetch_price_from_nse(symbol: str) -> Optional[Dict[str, Any]]:
    """Fetch latest price and basic info from NSE's official quote API.

    Returns a dict with keys: price, pchange, volume, sector, market_cap
    or None if the request fails.
    """

    base_url = "https://www.nseindia.com/api/quote-equity"
    params = {"symbol": symbol}
    nse_headers = {
        "User-Agent": USER_AGENT,
        "Referer": f"https://www.nseindia.com/get-quotes/equity?symbol={quote(symbol)}",
        "Accept": "application/json, text/plain, */*",
    }

    try:
        resp = SESSION.get(base_url, params=params, headers=nse_headers, timeout=8)
        if resp.status_code != 200:
            logger.warning("⚠️ NSE quote HTTP %s for %s", resp.status_code, symbol)
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
        raw_sector = industry_info.get("sector") or info.get("industry") or "Unknown"
        sector = validate_sector(raw_sector)

        sec_info = data.get("securityInfo") or {}
        issued_size = sec_info.get("issuedSize")
        market_cap = None
        try:
            if issued_size is not None:
                market_cap_raw = float(last_price) * float(issued_size)
                # Convert to ₹ Crores (same convention as yfinance branch)
                market_cap = round(market_cap_raw / 10_000_000, 2)
        except Exception:
            market_cap = None

        return {
            "price": float(last_price),
            "pchange": float(pchange) if pchange is not None else None,
            "volume": float(volume) if volume is not None else None,
            "sector": sector,
            "market_cap": market_cap,
        }
    except Exception as exc:  # pragma: no cover - defensive
        logger.warning("⚠️ NSE quote failed for %s: %s", symbol, exc)
        return None


def get_market_data_from_nse(symbol: str, cap_size: str) -> Optional[Dict[str, Any]]:
    """Fallback: build technical snapshot using NSE quote data.

    Used when yfinance cannot provide a usable price history.
    """

    nse = fetch_price_from_nse(symbol)
    if not nse:
        return None

    latest_price = nse["price"]
    pchange = nse["pchange"]
    market_cap = nse["market_cap"]
    sector = nse["sector"]

    # Use daily percentage change as a short-term momentum proxy
    momentum = (pchange / 100.0) if pchange is not None else 0.0

    # Without a long history we treat volume as neutral (1.0x)
    vol_surge = 1.0

    # Sentiment proxy from daily move
    if pchange is not None:
        sentiment = 1.0 if momentum > 0.02 else (-1.0 if momentum < -0.02 else 0.0)
    else:
        sentiment = 0.0

    logger.info(
        "✅ %s: (NSE) Price=₹%.2f, Momentum≈%.1f%% (1D), Volume≈%.2fx",
        symbol,
        latest_price,
        momentum * 100,
        vol_surge,
    )

    return {
        "ticker": symbol,
        "cap": cap_size,
        "sector": sector,
        "price": round(latest_price, 2),
        "market_cap": market_cap,
        "momentum": round(momentum, 4),
        "volume_surge": round(vol_surge, 2),
        "sentiment": sentiment,
        "has_data": True,
    }


def get_market_data(symbol: str, cap_size: str) -> Dict[str, Any]:
    """Fetch market data and calculate technical indicators.

    Primary source: yfinance. Fallback: NSE quote API.
    Always returns a data dict, marking ``has_data=False`` if all sources fail.
    """

    try:
        # Use current ticker (handles renamed companies)
        current_symbol = get_current_ticker(symbol)

        # Check if delisted or pump & dump
        if is_delisted(current_symbol):
            logger.debug(f"{symbol} is delisted, skipping")
            return None

        stock = yf.Ticker(f"{current_symbol}.NS")
        df = stock.history(period="7mo", auto_adjust=True)

        # Check if we have sufficient data
        has_data = not df.empty and len(df) >= 20

        if has_data:
            # Normal case: sufficient data available
            latest_price = df["Close"].iloc[-1]
            momentum = (df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0]
            avg_vol = df["Volume"].tail(20).mean()
            vol_surge = df["Volume"].iloc[-1] / avg_vol if avg_vol > 0 else 0.0

            # Recent trend (last ~5 sessions)
            recent_change = (
                df["Close"].iloc[-1] - df["Close"].iloc[-6]
            ) / df["Close"].iloc[-6]
            sentiment = (
                1.0 if recent_change > 0.02 else (-1.0 if recent_change < -0.02 else 0.0)
            )

            # Get market capitalization and sector
            market_cap = None
            sector = "Unknown"
            try:
                info = stock.info
                market_cap_raw = info.get("marketCap")
                if market_cap_raw:
                    # Convert to ₹ Crores (1 crore = 10 million)
                    market_cap = round(market_cap_raw / 10_000_000, 2)

                raw_sector = info.get("sector", info.get("industry", "Unknown"))
                sector = validate_sector(raw_sector)
            except Exception:  # pragma: no cover - best-effort
                pass

            logger.info(
                "✅ %s: Price=₹%.2f, Momentum=%.1f%%, Volume=%.2fx",
                symbol,
                latest_price,
                momentum * 100,
                vol_surge,
            )

            return {
                "ticker": symbol,
                "cap": cap_size,
                "sector": sector,
                "price": round(latest_price, 2),
                "market_cap": market_cap,
                "momentum": round(momentum, 4),
                "volume_surge": round(vol_surge, 2),
                "sentiment": sentiment,
                "has_data": True,
            }

        # No data from yfinance – try NSE fallback
        logger.warning("⚠️  %s: No data from yfinance, trying NSE fallback", symbol)
        alt = get_market_data_from_nse(symbol, cap_size)
        if alt:
            return alt

        logger.warning("⚠️  %s: No data from any source - adding with NA values", symbol)
        return {
            "ticker": symbol,
            "cap": cap_size,
            "sector": "Unknown",
            "price": None,
            "market_cap": None,
            "momentum": 0.0,
            "volume_surge": 0.0,
            "sentiment": 0.0,
            "has_data": False,
        }

    except Exception as exc:  # pragma: no cover - defensive
        logger.warning(
            "⚠️  %s: yfinance error (%s). Trying NSE fallback...", symbol, exc
        )
        alt = get_market_data_from_nse(symbol, cap_size)
        if alt:
            return alt

        logger.warning(
            "⚠️  %s: Error - adding with NA values (%s)",
            symbol,
            exc,
        )
        return {
            "ticker": symbol,
            "cap": cap_size,
            "sector": "Unknown",
            "price": None,
            "market_cap": None,
            "momentum": 0.0,
            "volume_surge": 0.0,
            "sentiment": 0.0,
            "has_data": False,
        }


# ---------------------------------------------------------------------------
# News & sentiment
# ---------------------------------------------------------------------------


def fetch_news(ticker: str) -> Optional[str]:
    """Fetch news from Yahoo Finance and Google News (basic mode).

    Returns a single concatenated news string or ``None``.
    """

    try:
        # Use current ticker (handles renamed companies)
        current_ticker = get_current_ticker(ticker)

        stock = yf.Ticker(f"{current_ticker}.NS")
        yf_news = stock.news or []

        # Get company name
        info = stock.info
        company_name = info.get("longName") or info.get("shortName") or ticker

        all_news: List[Dict[str, str]] = []

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

                for title in titles[1:4]:  # Skip feed title
                    all_news.append({"title": title, "date": "Recent"})
        except Exception:  # pragma: no cover - best-effort
            # Silently fail if Google News is unavailable
            pass

        # Return top 3 news
        if all_news:
            news_items: List[str] = []
            for news in all_news[:3]:
                title = re.sub(r"\s+", " ", news["title"]).strip()
                title = re.sub(r"&amp;", "&", title)
                if len(title) > 150:
                    title = title[:147] + "..."
                news_items.append(f"[{news['date']}] {title}")

            return " | ".join(news_items)

        return None

    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Error fetching news for %s: %s", ticker, exc)
        return None


def analyze_news_sentiment(news_text: Optional[str]) -> str:
    """Analyze news sentiment using simple keyword matching."""

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


def classify_news_type(news_text: Optional[str]) -> List[str]:
    """Classify news into types using keyword buckets."""

    if not news_text:
        return []

    news_lower = news_text.lower()
    types: List[str] = []

    for news_type, keywords in NEWS_TYPE_KEYWORDS.items():
        if any(keyword in news_lower for keyword in keywords):
            types.append(news_type)

    # Return unique types, max 3
    return list(set(types))[:3] if types else []


def calculate_score(momentum: float, volume_surge: float, signal: str) -> float:
    """Calculate simple investment score from momentum, volume, and signal."""

    score = 0.0

    if signal == "🚀 Strong Buy":
        score += 1000
    elif signal == "👀 Watch":
        score += 500

    score += momentum * 500
    score += volume_surge * 50

    return round(score, 2)


# ---------------------------------------------------------------------------
# Notion integration
# ---------------------------------------------------------------------------


def send_to_notion(
    data: Dict[str, Any],
    news_text: Optional[str],
    news_sentiment: Optional[str],
    news_types: Optional[List[str]] = None,
    rank: Optional[int] = None,
) -> bool:
    """Send a single stock's data to the Notion database."""

    try:
        # Sanitize NaN values using centralized utility
        from src.utils.data_sanitization import sanitize_stock_data, sanitize_number
        data = sanitize_stock_data(data)

        # Get pre-calculated signal and score (or calculate if not present)
        signal = data.get("signal")
        score = data.get("score")

        if signal is None:
            if not data.get("has_data", True):
                signal = "❄️ N/A"
                score = 0.0
            else:
                signal = "❄️ Neutral"
                if data["momentum"] > 0.10 and data["volume_surge"] > 1.2:
                    signal = "🚀 Strong Buy"
                elif data["momentum"] > 0.05 or data["volume_surge"] > 1.1:
                    signal = "👀 Watch"
                score = calculate_score(
                    data["momentum"], data["volume_surge"], signal
                )

        # Sanitize score
        score = sanitize_number(score, 0.0)

        # Calculate Trend based on momentum + volume confirmation
        momentum_val = data.get("momentum", 0.0)
        volume_val = data.get("volume_surge", 0.0)
        if momentum_val > 0.02 and volume_val > 1.0:  # Upward with volume confirmation
            trend = "📈"
        elif momentum_val < -0.02 and volume_val > 1.0:  # Downward with volume confirmation
            trend = "📉"
        else:  # Neutral (weak momentum or low volume)
            trend = "➡️"

        payload: Dict[str, Any] = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Ticker": {"title": [{"text": {"content": data["ticker"]}}]},
                "Market Cap": {"select": {"name": data["cap"]}},
                "Sector": {"select": {"name": data.get("sector", "Unknown")}},
                "Sentiment": {"number": data.get("sentiment", 0.0)},
                "Momentum (%)": {"number": data.get("momentum", 0.0)},
                "Volume Surge": {
                    "number": round(float(data.get("volume_surge", 0.0)), 2)
                },
                "Score": {"number": float(score)},
                "Signal": {"select": {"name": signal}},
                "Trend": {"select": {"name": trend}},
                "Last Updated": {
                    "date": {"start": datetime.now().isoformat()}
                },
            },
        }

        # Add price only if available
        if data.get("price") is not None:
            payload["properties"]["Price (₹)"] = {
                "number": round(float(data["price"]), 2)
            }

        # Add rank if provided
        if rank is not None:
            payload["properties"]["Rank"] = {"number": int(rank)}

        # Add market cap if available
        if data.get("market_cap") is not None:
            payload["properties"]["Capital Market (₹)"] = {
                "number": float(data["market_cap"])
            }

        # Add news if available
        if news_text:
            payload["properties"]["News & Updates"] = {
                "rich_text": [{"text": {"content": news_text[:2000]}}]
            }

        # Add news sentiment if available
        if news_sentiment:
            payload["properties"]["News Sentiment"] = {
                "select": {"name": news_sentiment}
            }

        # Add news types if available
        if news_types:
            payload["properties"]["News Type"] = {
                "multi_select": [{"name": nt} for nt in news_types]
            }

        # Add analyst ratings if already fetched
        if data.get("consensus") and data.get("rating_numeric") is not None and "analyst_count" in data:
            # We have complete ratings data
            payload["properties"]["Consensus"] = {
                "select": {"name": data["consensus"]}
            }
            rating_text = (
                f"{data['rating_numeric']:.2f}/5.0 "
                f"({data['analyst_count']} analysts)"
            )
            payload["properties"]["Ratings"] = {
                "rich_text": [{"text": {"content": rating_text}}]
            }
        else:
            # No analyst data available - set defaults
            payload["properties"]["Consensus"] = {
                "select": {"name": "No Consensus"}
            }
            payload["properties"]["Ratings"] = {
                "rich_text": [{"text": {"content": "N/A"}}]
            }

        # Send to Notion
        url = "https://api.notion.com/v1/pages"
        response = SESSION.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            logger.info(
                "✅ %s: %s, Score: %.2f, News: %s",
                data["ticker"],
                signal,
                score,
                news_sentiment or "N/A",
            )
            return True

        logger.error(
            "Notion error for %s: %s",
            data["ticker"],
            response.text[:100],
        )
        return False

    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Error sending %s to Notion: %s", data.get("ticker", "?"), exc)
        return False


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------


def main() -> None:
    """Main execution function with intelligent ranking."""

    logger.info("=" * 70)
    logger.info("🚀 MARKET INTELLIGENCE BOT - PROFESSIONAL VERSION")
    if HAS_RANKING_ENGINE:
        logger.info("🏆 Intelligent Multi-Factor Ranking: ENABLED")

    # Log news configuration
    if HAS_COMPREHENSIVE_NEWS:
        logger.info("📰 News Sources: COMPREHENSIVE (70+ sources)")
    else:
        logger.info("📰 News Sources: BASIC (Yahoo + Google)")

    logger.info("=" * 70)

    # Load watchlist
    if get_all_stocks_with_classification is None:
        logger.error("Stock data module not available!")
        logger.error(
            "Please ensure data/nse_stocks_650.py exists and is accessible."
        )
        return

    # Prefer validated stocks if available
    if get_validated_stocks:
        logger.info(
            "🔍 Using validated stock list (removes stocks without data)..."
        )
        watchlist = get_validated_stocks()
    else:
        logger.info("🔍 Using full stock list...")
        watchlist = get_all_stocks_with_classification()

    logger.info("📊 Total stocks: %d", len(watchlist))
    logger.info("⏱️  Estimated time: ~%d minutes", len(watchlist) * 3 // 60)
    logger.info("")

    stats: Dict[str, Any] = {
        "total": len(watchlist),
        "processed": 0,
        "success": 0,
        "errors": 0,
        "strong_buy": 0,
        "watch": 0,
        "neutral": 0,
        "with_news": 0,
        "positive_sentiment": 0,
        "negative_sentiment": 0,
    }

    # PHASE 1: Collect all stock data (PARALLEL PROCESSING)
    logger.info("📊 PHASE 1: Collecting market intelligence...")
    logger.info("="*70)

    start_time = time.time()

    # Setup parallel processing
    results: List[Optional[Dict[str, Any]]] = [None] * len(watchlist)
    lock = threading.Lock()
    max_workers = min(12, max(4, len(watchlist)))
    logger.info("🚀 Using %d parallel workers for optimal performance", max_workers)
    logger.info("="*70)

    def process_stock_parallel(idx: int, ticker: str, cap: str) -> None:
        """Worker function to process a single stock in parallel"""
        try:
            logger.info("[%d/%d] 🔍 %s", idx, len(watchlist), ticker)

            # Get market data (always returns data, even for NA stocks)
            data = get_market_data(ticker, cap)
            if not data:
                with lock:
                    stats["errors"] += 1
                return

            with lock:
                stats["processed"] += 1

            # Fetch news (only for stocks with data)
            news_text: Optional[str] = None
            news_sentiment: Optional[str] = None
            news_types: List[str] = []

            if data.get("has_data", True):
                if HAS_COMPREHENSIVE_NEWS:
                    try:
                        news_text, _ = fetch_comprehensive_news(ticker)
                        logger.debug(
                            "   📰 Fetched comprehensive news from 70+ sources"
                        )
                    except Exception as exc:  # pragma: no cover
                        logger.warning(
                            "   ⚠️  Comprehensive news failed, using basic: %s",
                            exc,
                        )
                        news_text = fetch_news(ticker)
                else:
                    news_text = fetch_news(ticker)

                if news_text:
                    news_sentiment = analyze_news_sentiment(news_text)
                    news_types = classify_news_type(news_text)

                    with lock:
                        stats["with_news"] += 1
                        if news_sentiment == "Positive":
                            stats["positive_sentiment"] += 1
                        elif news_sentiment == "Negative":
                            stats["negative_sentiment"] += 1

            # Calculate signal and score (needed for ranking)
            if not data.get("has_data", True):
                signal = "❄️ N/A"
                score = 0.0
            else:
                signal = "❄️ Neutral"
                if data["momentum"] > 0.10 and data["volume_surge"] > 1.2:
                    signal = "🚀 Strong Buy"
                elif data["momentum"] > 0.05 or data["volume_surge"] > 1.1:
                    signal = "👀 Watch"
                score = calculate_score(
                    data["momentum"], data["volume_surge"], signal
                )

            # Attach calculated fields
            data["signal"] = signal
            data["score"] = score
            data["sentiment"] = data.get("sentiment", 0.0)
            data["news"] = news_text
            data["news_sentiment"] = news_sentiment
            data["news_types"] = news_types

            # Fetch analyst ratings if available
            if HAS_ANALYST_RATINGS and data.get("has_data", True):
                try:
                    logger.info("   📊 Fetching analyst ratings...")
                    ratings_data = aggregate_all_analyst_ratings(ticker)
                    if ratings_data["has_data"]:
                        data["consensus"] = ratings_data["consensus"]
                        data["rating_numeric"] = ratings_data["rating_numeric"]
                        data["analyst_count"] = ratings_data["analyst_count"]
                        logger.info(
                            "   ✅ Ratings: %s (%.2f/5.0)",
                            ratings_data["consensus"],
                            ratings_data["rating_numeric"],
                        )
                    else:
                        data["consensus"] = "No Consensus"
                        data["rating_numeric"] = None
                        data["analyst_count"] = 0
                except Exception as exc:  # pragma: no cover - best-effort
                    logger.warning("   ⚠️  Failed to fetch ratings: %s", exc)
                    data["consensus"] = "No Consensus"
                    data["rating_numeric"] = None
                    data["analyst_count"] = 0

            with lock:
                results[idx - 1] = data

            time.sleep(0.7)  # Rate limiting (optimized)

        except Exception as exc:  # pragma: no cover - defensive
            logger.error("❌ Error processing %s: %s", ticker, exc)
            with lock:
                stats["errors"] += 1

        # Progress update every 50 stocks
        if idx % 50 == 0:
            elapsed = time.time() - start_time
            rate = idx / elapsed if elapsed > 0 else 1.0
            remaining = (len(watchlist) - idx) / rate if rate > 0 else 0.0
            with lock:
                processed = stats["processed"]
            logger.info(
                "📈 Progress: %d/%d, ~%.1f min remaining, Processed: %d",
                idx,
                len(watchlist),
                remaining / 60.0,
                processed,
            )

    # Execute parallel processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for idx, (ticker, cap) in enumerate(watchlist, 1):
            executor.submit(process_stock_parallel, idx, ticker, cap)

    # Filter out None results
    all_stocks_data: List[Dict[str, Any]] = [r for r in results if r is not None]
    logger.info("✅ Phase 1 complete: Collected data for %d stocks", len(all_stocks_data))

    # PHASE 2: Intelligent ranking
    logger.info("\n" + "=" * 70)
    logger.info("🏆 PHASE 2: Calculating intelligent rankings...")
    logger.info("=" * 70)

    if HAS_RANKING_ENGINE and all_stocks_data:
        ranked_stocks = rank_stocks(all_stocks_data)
        logger.info("✅ Ranked %d stocks successfully", len(ranked_stocks))
        top_3 = ", ".join([
            f"{s['ticker']}#{s['rank']}" for s in ranked_stocks[:3]
        ])
        logger.info("   Top 3: %s", top_3)
    else:
        logger.info("⚠️  Using serial ranking (ranking engine not available)")
        ranked_stocks = all_stocks_data
        for i, stock in enumerate(ranked_stocks, 1):
            stock["rank"] = i

    # PHASE 3: Send to Notion with ranks
    logger.info("\n" + "=" * 70)
    logger.info("📤 PHASE 3: Sending ranked data to Notion...")
    logger.info("=" * 70)

    for stock_data in ranked_stocks:
        try:
            ok = send_to_notion(
                stock_data,
                stock_data.get("news"),
                stock_data.get("news_sentiment"),
                stock_data.get("news_types", []),
                rank=stock_data["rank"],
            )
            if ok:
                stats["success"] += 1

                signal = stock_data.get("signal", "❄️ Neutral")
                if signal == "🚀 Strong Buy":
                    stats["strong_buy"] += 1
                elif signal == "👀 Watch":
                    stats["watch"] += 1
                else:
                    stats["neutral"] += 1
            else:
                stats["errors"] += 1

            time.sleep(0.3)  # Light rate limiting (optimized)

        except Exception as exc:  # pragma: no cover - defensive
            logger.error(
                "❌ Error sending %s to Notion: %s",
                stock_data.get("ticker", "?"),
                exc,
            )
            stats["errors"] += 1

    # Final summary
    elapsed_total = time.time() - start_time

    logger.info("")
    logger.info("=" * 70)
    logger.info("✅ MARKET ANALYSIS COMPLETE!")
    logger.info("=" * 70)
    logger.info("✅ Successfully sent: %d stocks", stats["success"])
    logger.info("❌ Errors/Skipped: %d stocks", stats["errors"])
    logger.info("")
    logger.info("📊 Signal Distribution:")
    logger.info("   🚀 Strong Buy: %d stocks", stats["strong_buy"])
    logger.info("   👀 Watch: %d stocks", stats["watch"])
    logger.info("   ❄️ Neutral: %d stocks", stats["neutral"])
    logger.info("")
    logger.info("📰 News Analysis:")
    logger.info("   📄 Stocks with news: %d", stats["with_news"])
    logger.info("   📈 Positive sentiment: %d", stats["positive_sentiment"])
    logger.info("   📉 Negative sentiment: %d", stats["negative_sentiment"])
    logger.info("")
    logger.info("⏱️  Total time: %.1f minutes", elapsed_total / 60.0)
    logger.info("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:  # pragma: no cover - interactive
        logger.info("\n\n⏹️  Analysis stopped by user")
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("❌ Critical error: %s", exc, exc_info=True)
