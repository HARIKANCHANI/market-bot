"""
INCREMENTAL UPDATE VERSION - Market Bot Lite
Only updates existing tickers or adds new ones - does NOT process all stocks
Perfect for daily updates after initial database population
Uses only technical indicators (momentum & volume) - NO MODEL DOWNLOAD NEEDED
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

# Import stock data
try:
    from data.nse_stocks_650 import get_all_stocks_with_classification, get_validated_stocks
except ImportError:
    print("⚠️  Stock data module not found. Please check data/nse_stocks_650.py")
    get_validated_stocks = None
    get_all_stocks_with_classification = None

# Import incremental update utilities
try:
    from src.utils.notion_incremental import upsert_notion_entry, query_ticker_in_database
    HAS_INCREMENTAL_UTILS = True
except ImportError:
    HAS_INCREMENTAL_UTILS = False
    print("⚠️  Incremental utilities not found. This bot requires src/utils/notion_incremental.py")
    exit(1)

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
    "wins", "won", "award", "beats", "surges", "jumps", "rallies", "gains",
    "record", "profit", "growth", "dividend", "expansion", "order", "contract",
    "partnership", "approval", "innovation", "breakthrough", "upgrade"
]

NEGATIVE_KEYWORDS = [
    "falls", "drops", "plunges", "crashes", "loss", "decline", "weak",
    "poor", "disappoints", "concern", "risk", "lawsuit", "probe", "investigation",
    "downgrade", "warning", "cuts", "misses", "slump", "recession"
]

# Constants
SESSION = requests.Session()
LOCK = threading.Lock()

print("\n" + "=" * 70)
print("📈 MARKET INTELLIGENCE BOT - LITE INCREMENTAL VERSION")
print("=" * 70)
print("✅ Incremental update mode: Only updates existing + adds new tickers")
print("✅ Fast execution: Skips full database rebuild")
print("=" * 70)


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


def classify_news_type(news_text: str) -> list:
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

    return types[:3]  # Max 3 types


def fetch_news(ticker: str) -> tuple:
    """Fetch news from available sources"""
    try:
        # Try comprehensive news first
        if HAS_COMPREHENSIVE_NEWS:
            news_items = fetch_news_comprehensive(ticker)
            if news_items:
                news_text = " ".join([item.get("title", "") + " " + item.get("description", "") for item in news_items[:5]])
                news_titles = " | ".join([item.get("title", "") for item in news_items[:3]])
                return (news_text[:2000], news_titles[:500])

        # Fallback to basic Yahoo Finance news
        stock = yf.Ticker(ticker)
        news = stock.news
        if news:
            news_text = " ".join([item.get("title", "") for item in news[:5]])
            news_titles = " | ".join([item.get("title", "") for item in news[:3]])
            return (news_text[:2000], news_titles[:500])
    except:
        pass

    return ("", "")


def get_market_intelligence(symbol: str, cap_size: str) -> dict:
    """Fetch comprehensive market data for a stock"""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="3mo")

        if hist.empty or len(hist) < 2:
            return {
                "ticker": symbol,
                "cap": cap_size,
                "sector": "Unknown",
                "price": None,
                "sent": 0,
                "mom": 0,
                "vol": 0,
                "market_cap": None,
                "has_data": False
            }

        # Get sector
        sector = "Unknown"
        try:
            info = stock.info
            sector = info.get('sector', info.get('industry', 'Unknown'))
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
                market_cap = round(market_cap_inr / 10000000, 2)  # Convert to Crores
        except:
            pass

        return {
            "ticker": symbol,
            "cap": cap_size,
            "sector": sector,
            "price": round(latest_price, 2),
            "sent": 0,  # Lite version doesn't use AI sentiment
            "mom": round(momentum * 100, 2),
            "vol": round(volume_surge, 2),
            "market_cap": market_cap,
            "has_data": True
        }

    except Exception as e:
        print(f"⚠️  Error fetching data for {symbol}: {str(e)}")
        return {
            "ticker": symbol,
            "cap": cap_size,
            "sector": "Unknown",
            "price": None,
            "sent": 0,
            "mom": 0,
            "vol": 0,
            "market_cap": None,
            "has_data": False
        }


def upsert_to_notion(data: dict, rank: int | None = None) -> tuple:
    """Update existing ticker or create new one in Notion database"""
    try:
        # Determine signal
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

        # Build properties
        properties = {
            "Ticker": {"title": [{"text": {"content": data["ticker"]}}]},
            "Market Cap": {"select": {"name": data["cap"]}},
            "Sector": {"select": {"name": data.get("sector", "Unknown")}},
            "Sentiment": {"number": data["sent"]},
            "Momentum (%)": {"number": data["mom"]},
            "Volume Surge": {"number": round(data["vol"], 2)},
            "Score": {"number": score},
            "Signal": {"select": {"name": signal}},
            "Last Updated": {"date": {"start": datetime.now().isoformat()}}
        }

        # Add price if available
        if data.get("price") is not None:
            properties["Price (₹)"] = {"number": round(data["price"], 2)}

        # Add rank if provided
        if rank is not None:
            properties["Rank"] = {"number": rank}

        # Add market cap if available
        if data.get("market_cap") is not None:
            properties["Capital Market (₹)"] = {"number": data["market_cap"]}

        # Add news if available
        if data.get("news"):
            properties["News & Updates"] = {
                "rich_text": [{"text": {"content": data["news"][:2000]}}]
            }

        # Add news sentiment if available
        if data.get("news_sentiment"):
            properties["News Sentiment"] = {"select": {"name": data["news_sentiment"]}}

        # Add news types if available
        if data.get("news_types"):
            properties["News Type"] = {
                "multi_select": [{"name": news_type} for news_type in data["news_types"]]
            }

        # Add analyst ratings if available
        if HAS_ANALYST_RATINGS and data.get("has_data", True):
            try:
                ratings_data = aggregate_all_analyst_ratings(data["ticker"])
                if ratings_data["has_data"]:
                    properties["Consensus"] = {"select": {"name": ratings_data["consensus"]}}
                    rating_text = f"{ratings_data['rating_numeric']:.2f}/5.0 ({ratings_data['analyst_count']} analysts)"
                    properties["Ratings"] = {"rich_text": [{"text": {"content": rating_text}}]}
                else:
                    properties["Consensus"] = {"select": {"name": "No Consensus"}}
                    properties["Ratings"] = {"rich_text": [{"text": {"content": "N/A"}}]}
            except:
                pass

        # Upsert to Notion
        success, action = upsert_notion_entry(data["ticker"], properties)

        if success:
            action_symbol = "🔄" if action == "updated" else "✨"
            print(f"{action_symbol} {data['ticker']} {action.upper()}: {signal}, Score: {score:.0f}, Rank: {rank if rank else 'N/A'}")
            return (True, action)
        else:
            print(f"❌ Failed to {action} {data['ticker']}")
            return (False, action)

    except Exception as e:
        print(f"❌ Error upserting {data.get('ticker', '?')}: {str(e)}")
        return (False, "error")


def process_stock(ticker: str, cap_size: str) -> dict:
    """Process a single stock and return data"""
    print(f"\n{'='*70}")
    print(f"Processing: {ticker} ({cap_size})")
    print(f"{'='*70}")

    # Get market data
    data = get_market_intelligence(ticker, cap_size)

    # Fetch news
    news_text, news_titles = fetch_news(ticker)
    data["news"] = news_titles

    # Analyze news sentiment
    if news_text:
        data["news_sentiment"] = analyze_news_sentiment(news_text)
        data["news_types"] = classify_news_type(news_text)

    return data


if __name__ == "__main__":
    start_time = time.time()

    print("\n" + "=" * 70)
    print("🚀 STARTING INCREMENTAL UPDATE")
    print("=" * 70)

    # Get stock list
    if get_validated_stocks:
        stocks_list = get_validated_stocks()
    elif get_all_stocks_with_classification:
        stocks_list = get_all_stocks_with_classification()
    else:
        print("❌ No stock data available")
        exit(1)

    total_stocks = len(stocks_list)
    print(f"📊 Total stocks to process: {total_stocks}")
    print("=" * 70)

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

    # Process all stocks
    all_stock_data = []

    for idx, (ticker, cap_size) in enumerate(stocks_list, 1):
        try:
            print(f"\n[{idx}/{total_stocks}] Processing {ticker}...")

            # Get stock data
            data = process_stock(ticker, cap_size)
            all_stock_data.append(data)

            stats["processed"] += 1
            time.sleep(0.3)  # Rate limiting

        except Exception as e:
            print(f"❌ Error processing {ticker}: {str(e)}")
            stats["errors"] += 1

    # Rank stocks
    print("\n" + "=" * 70)
    print("📊 RANKING STOCKS")
    print("=" * 70)

    if HAS_RANKING_ENGINE:
        ranked_stocks = rank_stocks(all_stock_data)
    else:
        # Simple ranking by score
        valid_stocks = [s for s in all_stock_data if s.get("has_data", True)]
        sorted_stocks = sorted(valid_stocks, key=lambda x: (
            x.get("mom", 0) * 500 + x.get("vol", 0) * 50
        ), reverse=True)
        for idx, stock in enumerate(sorted_stocks, 1):
            stock["rank"] = idx
        ranked_stocks = sorted_stocks

    print(f"✅ Ranked {len(ranked_stocks)} stocks")

    # Upsert to Notion
    print("\n" + "=" * 70)
    print("📤 UPSERTING TO NOTION")
    print("=" * 70)

    for stock_data in ranked_stocks:
        try:
            success, action = upsert_to_notion(stock_data, rank=stock_data.get("rank"))

            if success:
                if action == "updated":
                    stats["updated"] += 1
                elif action == "created":
                    stats["created"] += 1

                # Track signals
                signal = stock_data.get("signal", "❄️ Neutral")
                if "Strong Buy" in signal:
                    stats["strong_buy"] += 1
                elif "Watch" in signal:
                    stats["watch"] += 1
                else:
                    stats["neutral"] += 1
            else:
                stats["errors"] += 1

            time.sleep(0.5)  # Rate limiting

        except Exception as e:
            print(f"❌ Error upserting {stock_data.get('ticker', '?')}: {str(e)}")
            stats["errors"] += 1

    # Final summary
    elapsed_time = time.time() - start_time

    print("\n" + "=" * 70)
    print("✅ INCREMENTAL UPDATE COMPLETE!")
    print("=" * 70)
    print(f"⏱️  Total time: {elapsed_time/60:.1f} minutes")
    print(f"📊 Stocks processed: {stats['processed']}")
    print(f"🔄 Updated: {stats['updated']}")
    print(f"✨ Created: {stats['created']}")
    print(f"❌ Errors: {stats['errors']}")
    print(f"\n📈 Signals:")
    print(f"   🚀 Strong Buy: {stats['strong_buy']}")
    print(f"   👀 Watch: {stats['watch']}")
    print(f"   ❄️  Neutral: {stats['neutral']}")
    print("=" * 70)
