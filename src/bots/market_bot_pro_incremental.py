#!/usr/bin/env python3
"""
INCREMENTAL UPDATE VERSION - Market Bot Pro
Only updates existing tickers or adds new ones - does NOT process all stocks
Perfect for daily updates after initial database population
Includes comprehensive news aggregation, analyst ratings, and keyword-based sentiment
"""

from __future__ import annotations

import os
import re
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor
import threading

import requests
import yfinance as yf
from urllib.parse import quote

# Python path setup
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Setup centralized logging
from src.config.logging_config import setup_bot_logging
logger = setup_bot_logging("market_bot_pro_incremental")

# Configuration
USE_COMPREHENSIVE_NEWS = True

# Import incremental update utilities
try:
    from src.utils.notion_incremental import upsert_notion_entry, query_ticker_in_database
    HAS_INCREMENTAL_UTILS = True
except ImportError:
    HAS_INCREMENTAL_UTILS = False
    print("⚠️  Incremental utilities not found. This bot requires src/utils/notion_incremental.py")
    exit(1)

# Analyst ratings
try:
    from src.core.analyst_ratings import aggregate_all_analyst_ratings
    HAS_ANALYST_RATINGS = True
except ImportError:
    HAS_ANALYST_RATINGS = False
    print("⚠️  Analyst ratings module not found. Ratings will not be included.")

# Comprehensive news aggregator
if USE_COMPREHENSIVE_NEWS:
    try:
        from src.core.news_aggregator import fetch_comprehensive_news
        HAS_COMPREHENSIVE_NEWS = True
        print("✅ Comprehensive news aggregator loaded (70+ sources)")
    except ImportError:
        HAS_COMPREHENSIVE_NEWS = False
        print("⚠️  Comprehensive news module not found. Falling back to basic news.")
else:
    HAS_COMPREHENSIVE_NEWS = False
    print("ℹ️  Using basic news sources (Yahoo + Google)")

# Intelligent ranking engine
try:
    from src.core.ranking_engine import rank_stocks
    HAS_RANKING_ENGINE = True
except ImportError:
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
except ImportError:
    print("⚠️  Stock data module not found. Please check data/nse_stocks_650.py")
    get_validated_stocks = None
    get_all_stocks_with_classification = None
    get_current_ticker = lambda x: x
    is_delisted = lambda x: False

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



# Validate configuration
try:
    if 'validate_notion_config' in dir():
        validate_notion_config()
    elif not NOTION_TOKEN or not DATABASE_ID:
        logger.error("CRITICAL ERROR: NOTION_TOKEN or DATABASE_ID missing")
        exit(1)
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    exit(1)

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
    sector_lower = sector_name.lower()
    for key, value in VALID_NOTION_SECTORS.items():
        if key.lower() in sector_lower or sector_lower in key.lower():
            logger.debug(f"Mapped sector '{sector_name}' -> '{value}'")
            return value

    # No match found - default to Unknown
    logger.warning(f"Unknown sector '{sector_name}' mapped to 'Unknown'")
    return "Unknown"

# News sentiment keywords
POSITIVE_KEYWORDS = [
    "wins", "won", "award", "beats", "surges", "jumps", "rallies", "gains",
    "record", "profit", "growth", "dividend", "expansion", "order", "contract",
    "partnership", "approval", "innovation", "breakthrough", "upgrade"
]

NEGATIVE_KEYWORDS = [
    "falls", "drops", "plunges", "crashes", "loss", "decline", "weak",
    "poor", "disappoints", "concern", "risk", "lawsuit", "probe",
    "investigation", "downgrade", "warning", "cuts", "misses", "slump"
]

# Session for API calls
SESSION = requests.Session()

logger.info("=" * 70)
logger.info("📈 MARKET INTELLIGENCE BOT - PRO INCREMENTAL VERSION")
logger.info("=" * 70)
logger.info("✅ Incremental update mode: Only updates existing + adds new tickers")
logger.info("✅ Comprehensive news + analyst ratings enabled")
logger.info("=" * 70)


def analyze_news_sentiment(news_text: str) -> str:
    """Analyze news sentiment using keyword matching"""
    if not news_text:
        return "Neutral"

    text_lower = news_text.lower()
    positive_count = sum(1 for kw in POSITIVE_KEYWORDS if kw in text_lower)
    negative_count = sum(1 for kw in NEGATIVE_KEYWORDS if kw in text_lower)

    if positive_count > negative_count:
        return "Positive"
    elif negative_count > positive_count:
        return "Negative"
    return "Neutral"


def classify_news_type(news_text: str) -> List[str]:
    """Classify news into categories"""
    if not news_text:
        return []

    text_lower = news_text.lower()
    types = []

    if any(kw in text_lower for kw in ["earnings", "profit", "revenue", "quarter"]):
        types.append("Earnings")
    if any(kw in text_lower for kw in ["product", "launch", "service"]):
        types.append("Product")
    if any(kw in text_lower for kw in ["merger", "acquisition", "deal", "partnership"]):
        types.append("M&A")
    if any(kw in text_lower for kw in ["expand", "plant", "facility", "capacity"]):
        types.append("Expansion")
    if any(kw in text_lower for kw in ["dividend", "buyback", "split"]):
        types.append("Corporate Action")
    if any(kw in text_lower for kw in ["regulation", "approval", "ban", "policy"]):
        types.append("Regulatory")

    return types[:3]


def fetch_news(ticker: str) -> Tuple[str, str]:
    """Fetch news from available sources"""
    try:
        # Try comprehensive news first
        if HAS_COMPREHENSIVE_NEWS:
            news_items = fetch_comprehensive_news(ticker)
            if news_items:
                news_text = " ".join([
                    item.get("title", "") + " " + item.get("description", "")
                    for item in news_items[:5]
                ])
                news_titles = " | ".join([item.get("title", "") for item in news_items[:3]])
                return (news_text[:2000], news_titles[:500])

        # Fallback to Yahoo Finance news
        # Use current ticker (handles renamed companies)
        current_ticker = get_current_ticker(ticker)

        stock = yf.Ticker(current_ticker)
        news = stock.news
        if news:
            news_text = " ".join([item.get("title", "") for item in news[:5]])
            news_titles = " | ".join([item.get("title", "") for item in news[:3]])
            return (news_text[:2000], news_titles[:500])
    except:
        pass

    return ("", "")


def get_market_intelligence(symbol: str, cap_size: str) -> Dict[str, Any]:
    """Fetch comprehensive market data for a stock"""
    try:
        # Use current ticker (handles renamed companies)
        current_symbol = get_current_ticker(symbol)

        # Check if delisted or pump & dump
        if is_delisted(current_symbol):
            logger.debug(f"{symbol} is delisted, skipping")
            return None

        stock = yf.Ticker(current_symbol)
        hist = stock.history(period="3mo")

        if hist.empty or len(hist) < 2:
            return {
                "ticker": symbol,
                "cap": cap_size,
                "sector": "Unknown",
                "price": None,
                "sentiment": 0.0,
                "momentum": 0.0,
                "volume_surge": 0.0,
                "market_cap": None,
                "has_data": False
            }

        # Get sector and validate for Notion
        sector = "Unknown"
        try:
            info = stock.info
            raw_sector = info.get('sector', info.get('industry', 'Unknown'))
            sector = validate_sector(raw_sector)
        except:
            pass

        # Calculate metrics
        latest_price = hist['Close'].iloc[-1]
        momentum = (hist['Close'].iloc[-1] - hist['Close'].iloc[-20]) / hist['Close'].iloc[-20] if len(hist) >= 20 else 0
        avg_volume_20d = hist['Volume'].iloc[-20:].mean() if len(hist) >= 20 else hist['Volume'].mean()
        latest_volume = hist['Volume'].iloc[-1]
        volume_surge = latest_volume / avg_volume_20d if avg_volume_20d > 0 else 1.0

        # Get market cap
        market_cap = None
        try:
            info = stock.info
            market_cap_inr = info.get('marketCap', 0)
            if market_cap_inr:
                market_cap = round(market_cap_inr / 10000000, 2)
        except:
            pass

        return {
            "ticker": symbol,
            "cap": cap_size,
            "sector": sector,
            "price": round(latest_price, 2),
            "sentiment": 0.0,  # Pro version uses keyword-based sentiment
            "momentum": round(momentum * 100, 2),
            "volume_surge": round(volume_surge, 2),
            "market_cap": market_cap,
            "has_data": True
        }

    except Exception as e:
        logger.warning(f"Error fetching data for {symbol}: {str(e)}")
        return {
            "ticker": symbol,
            "cap": cap_size,
            "sector": "Unknown",
            "price": None,
            "sentiment": 0.0,
            "momentum": 0.0,
            "volume_surge": 0.0,
            "market_cap": None,
            "has_data": False
        }


def calculate_score(momentum: float, volume_surge: float, signal: str) -> float:
    """Calculate score based on momentum, volume, and signal"""
    score = 0.0

    if signal == "🚀 Strong Buy":
        score += 1000
    elif signal == "👀 Watch":
        score += 500

    score += momentum * 500
    score += volume_surge * 50

    return round(score, 2)


def upsert_to_notion(
    data: Dict[str, Any],
    news_text: Optional[str],
    news_sentiment: Optional[str],
    news_types: Optional[List[str]] = None,
    rank: Optional[int] = None
) -> Tuple[bool, str]:
    """Update existing ticker or create new one in Notion database"""
    try:
        # Determine signal
        if not data.get("has_data", True):
            signal = "❄️ N/A"
            score = 0.0
        else:
            signal = "❄️ Neutral"
            if data["momentum"] > 0.10 and data["volume_surge"] > 1.2:
                signal = "🚀 Strong Buy"
            elif data["momentum"] > 0.05 or data["volume_surge"] > 1.1:
                signal = "👀 Watch"
            score = calculate_score(data["momentum"], data["volume_surge"], signal)

        # Sanitize NaN values using centralized utility
        from src.utils.data_sanitization import sanitize_stock_data, sanitize_number
        data = sanitize_stock_data(data)
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

        # Build properties
        properties = {
            "Ticker": {"title": [{"text": {"content": data["ticker"]}}]},
            "Market Cap": {"select": {"name": data["cap"]}},
            "Sector": {"select": {"name": data.get("sector", "Unknown")}},
            "Sentiment": {"number": data.get("sentiment", 0.0)},
            "Momentum (%)": {"number": data.get("momentum", 0.0)},
            "Volume Surge": {"number": round(float(data.get("volume_surge", 0.0)), 2)},
            "Score": {"number": float(score)},
            "Signal": {"select": {"name": signal}},
            "Trend": {"select": {"name": trend}},
            "Last Updated": {"date": {"start": datetime.now().isoformat()}}
        }

        # Add price if available
        if data.get("price") is not None:
            properties["Price (₹)"] = {"number": round(float(data["price"]), 2)}

        # Add rank if provided
        if rank is not None:
            properties["Rank"] = {"number": int(rank)}

        # Add market cap if available
        if data.get("market_cap") is not None:
            properties["Capital Market (₹)"] = {"number": float(data["market_cap"])}

        # Add news if available
        if news_text:
            properties["News & Updates"] = {
                "rich_text": [{"text": {"content": news_text[:2000]}}]
            }

        # Add news sentiment if available
        if news_sentiment:
            properties["News Sentiment"] = {"select": {"name": news_sentiment}}

        # Add news types if available
        if news_types:
            properties["News Type"] = {
                "multi_select": [{"name": nt} for nt in news_types]
            }

        # Add analyst ratings if available
        if HAS_ANALYST_RATINGS and data.get("has_data", True):
            try:
                logger.info(f"   📊 Fetching analyst ratings for {data['ticker']}...")
                ratings_data = aggregate_all_analyst_ratings(data["ticker"])
                if ratings_data and ratings_data.get("has_data"):
                    properties["Consensus"] = {"select": {"name": ratings_data["consensus"]}}
                    rating_text = f"{ratings_data['rating_numeric']:.2f}/5.0 ({ratings_data['analyst_count']} analysts)"
                    properties["Ratings"] = {"rich_text": [{"text": {"content": rating_text}}]}
                    logger.info(f"   ✅ Ratings: {ratings_data['consensus']} ({rating_text})")
                else:
                    properties["Consensus"] = {"select": {"name": "No Consensus"}}
                    properties["Ratings"] = {"rich_text": [{"text": {"content": "N/A"}}]}
                    logger.info(f"   ℹ️  No analyst ratings available")
            except Exception as e:
                logger.warning(f"   ⚠️  Failed to fetch ratings: {str(e)}")
                # Still set default values even if fetch fails
                properties["Consensus"] = {"select": {"name": "No Consensus"}}
                properties["Ratings"] = {"rich_text": [{"text": {"content": "N/A"}}]}

        # Upsert to Notion
        success, action = upsert_notion_entry(data["ticker"], properties)

        if success:
            action_symbol = "🔄" if action == "updated" else "✨"
            logger.info(
                f"{action_symbol} {data['ticker']} {action.upper()}: {signal}, "
                f"Score: {score:.0f}, News: {news_sentiment or 'N/A'}, Rank: {rank or 'N/A'}"
            )
            return (True, action)
        else:
            logger.error(f"Failed to {action} {data['ticker']}")
            return (False, action)

    except Exception as e:
        logger.error(f"Error upserting {data.get('ticker', '?')}: {str(e)}")
        return (False, "error")


def process_stock(ticker: str, cap_size: str) -> Dict[str, Any]:
    """Process a single stock and return comprehensive data"""
    logger.info(f"Processing: {ticker} ({cap_size})")

    # Get market data
    data = get_market_intelligence(ticker, cap_size)

    # Fetch news
    news_text, news_titles = fetch_news(ticker)
    data["news_text"] = news_text
    data["news_titles"] = news_titles

    # Analyze news sentiment
    if news_text:
        data["news_sentiment"] = analyze_news_sentiment(news_text)
        data["news_types"] = classify_news_type(news_text)
    else:
        data["news_sentiment"] = None
        data["news_types"] = []

    return data


def main() -> None:
    """Main execution function"""
    start_time = time.time()

    logger.info("=" * 70)
    logger.info("🚀 STARTING INCREMENTAL UPDATE")
    logger.info("=" * 70)

    # Get stock list
    if get_validated_stocks:
        stocks_list = get_validated_stocks()
    elif get_all_stocks_with_classification:
        stocks_list = get_all_stocks_with_classification()
    else:
        logger.error("❌ No stock data available")
        exit(1)

    total_stocks = len(stocks_list)
    logger.info(f"📊 Total stocks to process: {total_stocks}")
    logger.info("=" * 70)

    # Statistics
    stats = {
        "processed": 0,
        "updated": 0,
        "created": 0,
        "errors": 0,
        "strong_buy": 0,
        "watch": 0,
        "neutral": 0
    }

    # Process all stocks (PARALLEL PROCESSING)
    logger.info("🚀 Using parallel processing for faster data collection")

    results = [None] * total_stocks
    lock = threading.Lock()
    max_workers = 4  # Fixed at 4 workers to prevent API rate limiting

    def process_stock_parallel(idx, ticker, cap_size):
        """Worker function to process a single stock in parallel"""
        try:
            logger.info(f"[{idx}/{total_stocks}] Processing {ticker}...")

            # Get stock data
            data = process_stock(ticker, cap_size)

            with lock:
                results[idx - 1] = data
                stats["processed"] += 1

            time.sleep(0.7)  # Rate limiting (optimized)

        except Exception as e:
            logger.error(f"Error processing {ticker}: {str(e)}")
            with lock:
                stats["errors"] += 1

    # Execute parallel processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for idx, (ticker, cap_size) in enumerate(stocks_list, 1):
            executor.submit(process_stock_parallel, idx, ticker, cap_size)

    # Filter out None results
    all_stock_data = [r for r in results if r is not None]
    logger.info(f"✅ Collected data for {len(all_stock_data)} stocks")

    # Rank stocks
    logger.info("=" * 70)
    logger.info("📊 RANKING STOCKS")
    logger.info("=" * 70)

    if HAS_RANKING_ENGINE:
        ranked_stocks = rank_stocks(all_stock_data)
    else:
        # Simple ranking by score
        valid_stocks = [s for s in all_stock_data if s.get("has_data", True)]
        sorted_stocks = sorted(valid_stocks, key=lambda x: (
            x.get("momentum", 0) * 500 + x.get("volume_surge", 0) * 50
        ), reverse=True)
        for idx, stock in enumerate(sorted_stocks, 1):
            stock["rank"] = idx
        ranked_stocks = sorted_stocks

    logger.info(f"✅ Ranked {len(ranked_stocks)} stocks")

    # Upsert to Notion
    logger.info("=" * 70)
    logger.info("📤 UPSERTING TO NOTION")
    logger.info("=" * 70)

    for stock_data in ranked_stocks:
        try:
            success, action = upsert_to_notion(
                stock_data,
                stock_data.get("news_titles"),
                stock_data.get("news_sentiment"),
                stock_data.get("news_types", []),
                rank=stock_data.get("rank")
            )

            if success:
                if action == "updated":
                    stats["updated"] += 1
                elif action == "created":
                    stats["created"] += 1

                # Track signals (need to recalculate from data)
                if stock_data.get("has_data", True):
                    if stock_data.get("momentum", 0) > 0.10 and stock_data.get("volume_surge", 0) > 1.2:
                        stats["strong_buy"] += 1
                    elif stock_data.get("momentum", 0) > 0.05 or stock_data.get("volume_surge", 0) > 1.1:
                        stats["watch"] += 1
                    else:
                        stats["neutral"] += 1
            else:
                stats["errors"] += 1

            time.sleep(0.3)  # Rate limiting (optimized)

        except Exception as e:
            logger.error(f"Error upserting {stock_data.get('ticker', '?')}: {str(e)}")
            stats["errors"] += 1

    # Final summary
    elapsed_time = time.time() - start_time

    logger.info("=" * 70)
    logger.info("✅ INCREMENTAL UPDATE COMPLETE!")
    logger.info("=" * 70)
    logger.info(f"⏱️  Total time: {elapsed_time/60:.1f} minutes")
    logger.info(f"📊 Stocks processed: {stats['processed']}")
    logger.info(f"🔄 Updated: {stats['updated']}")
    logger.info(f"✨ Created: {stats['created']}")
    logger.info(f"❌ Errors: {stats['errors']}")
    logger.info("")
    logger.info("📈 Signals:")
    logger.info(f"   🚀 Strong Buy: {stats['strong_buy']}")
    logger.info(f"   👀 Watch: {stats['watch']}")
    logger.info(f"   ❄️  Neutral: {stats['neutral']}")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()
