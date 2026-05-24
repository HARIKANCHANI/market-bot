#!/usr/bin/env python3
"""
MARKET INTELLIGENCE BOT - AI SENTIMENT VERSION
Complete market analysis with:
- 650 NSE stocks (Nifty 150, Midcap 200, Smallcap 300)
- AI-powered sentiment analysis (FinBERT)
- Multi-source news aggregation
- Comprehensive analytics
- Intelligent multi-factor ranking
- Production-grade reliability
"""

import os
import sys
import time
import logging
import re
from datetime import datetime
from urllib.parse import quote
import requests
import yfinance as yf
from transformers import pipeline

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

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

# Import stock data with validation
try:
    from data.nse_stocks_650 import get_all_stocks_with_classification, get_validated_stocks
except ImportError:
    print("⚠️  Stock data module not found. Please check data/nse_stocks_650.py")
    get_validated_stocks = None
    get_all_stocks_with_classification = None

# Import environment configuration
try:
    from src.config.env_config import (
        NOTION_TOKEN, DATABASE_ID, HF_TOKEN,
        validate_notion_config, validate_hf_config,
        get_notion_headers
    )
except ImportError:
    print("⚠️  Environment config not found. Loading from dotenv directly...")
    from dotenv import load_dotenv
    load_dotenv()
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    DATABASE_ID = os.getenv("DATABASE_ID")
    HF_TOKEN = os.getenv("HF_TOKEN")

# Setup logging
logs_dir = os.path.join(project_root, "logs")
os.makedirs(logs_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(logs_dir, "market_bot_ai.log")),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

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

# Validate HuggingFace token for AI functionality
try:
    if 'validate_hf_config' in dir():
        validate_hf_config()
    elif not HF_TOKEN:
        logger.error("CRITICAL ERROR: HF_TOKEN missing from environment")
        logger.error("AI bot requires HuggingFace token for sentiment analysis")
        exit(1)
except ValueError as e:
    logger.error(f"HuggingFace configuration error: {e}")
    exit(1)

# Set Hugging Face token
os.environ["HF_TOKEN"] = HF_TOKEN
os.environ["TRANSFORMERS_CACHE"] = os.path.join(os.getcwd(), "models")

# Notion headers
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Initialize AI Sentiment (FinBERT)
logger.info("🤖 Loading FinBERT AI model...")
try:
    sentiment_model = pipeline("sentiment-analysis", model="ProsusAI/finbert", device=-1)
    logger.info("✅ FinBERT model loaded successfully!")
except Exception as e:
    logger.error(f"❌ Failed to load FinBERT: {str(e)}")
    logger.info("Falling back to keyword-based sentiment...")
    sentiment_model = None

# News keywords for fallback sentiment
POSITIVE_KEYWORDS = [
    "wins", "won", "award", "beats", "surges", "jumps", "rallies", "gains",
    "record", "profit", "growth", "dividend", "expansion", "order", "contract",
    "upgrade", "acquisition", "launch", "partnership"
]

NEGATIVE_KEYWORDS = [
    "falls", "drops", "crashes", "plunges", "loss", "downgrade", "weak",
    "concern", "debt", "penalty", "resignation", "lawsuit", "decline"
]

# News type classification keywords
NEWS_TYPE_KEYWORDS = {
    "Earnings": ["earnings", "quarter", "q1", "q2", "q3", "q4", "revenue", "profit", "loss", "results"],
    "Product": ["launch", "product", "unveils", "introduces", "release", "model", "variant"],
    "Legal": ["lawsuit", "court", "legal", "case", "trial", "settlement", "penalty", "fine"],
    "M&A": ["merger", "acquisition", "acquires", "deal", "buyout", "takeover", "stake"],
    "Management": ["ceo", "cfo", "resign", "appoint", "director", "board", "executive"],
    "Dividend": ["dividend", "payout", "shareholder", "distribution"],
    "Regulatory": ["sebi", "regulator", "compliance", "violation", "probe", "investigation"],
    "Expansion": ["expansion", "plant", "facility", "capacity", "invest", "capex"]
}

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Shared HTTP session for all external calls (NSE, Google News, Notion) to
# reduce connection setup overhead during large batch runs.
SESSION = requests.Session()

def fetch_comprehensive_news(ticker):
    """Fetch news from multiple sources"""
    try:
        stock = yf.Ticker(f"{ticker}.NS")
        yf_news = stock.news or []

        # Get company info
        info = stock.info
        company_name = info.get("longName") or info.get("shortName") or ticker

        all_news = []

        # Yahoo Finance news
        for item in yf_news[:8]:
            title = item.get("title", "")
            pub_time = item.get("providerPublishTime", 0)
            date = datetime.fromtimestamp(pub_time).strftime("%d-%b") if pub_time else "Recent"
            all_news.append({"title": title, "date": date})

        # Google News
        try:
            url = f"https://news.google.com/rss/search?q={quote(company_name)}+stock+india&hl=en-IN&gl=IN&ceid=IN:en"
            response = SESSION.get(
                url,
                timeout=5,
                headers={'User-Agent': USER_AGENT},
            )

            if response.status_code == 200:
                titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', response.text)
                if not titles:
                    titles = re.findall(r'<title>(.*?)</title>', response.text)

                for title in titles[1:4]:
                    all_news.append({"title": title, "date": "Recent"})
        except Exception:
            # Ignore Google News failures; Yahoo Finance + AI sources are primary
            pass

        # Format top 3 news
        if all_news:
            news_items = []
            for news in all_news[:3]:
                title = re.sub(r'\s+', ' ', news["title"]).strip()
                title = re.sub(r'&amp;', '&', title)
                if len(title) > 150:
                    title = title[:147] + "..."
                news_items.append(f"[{news['date']}] {title}")

            return " | ".join(news_items), [n["title"] for n in all_news[:5]]

        return None, []

    except Exception as e:
        logger.error(f"Error fetching news for {ticker}: {str(e)}")
        return None, []

def analyze_ai_sentiment(news_titles):
    """Analyze sentiment using FinBERT AI or fallback to keywords"""
    if not news_titles:
        return 0

    try:
        if sentiment_model:
            # Use FinBERT AI
            results = sentiment_model(news_titles)
            score_map = {"positive": 1, "neutral": 0, "negative": -1}
            sent_score = sum([score_map.get(r['label'].lower(), 0) * r['score'] for r in results]) / len(results)
            return round(sent_score, 2)
        else:
            # Fallback to keyword-based
            combined_text = " ".join(news_titles).lower()
            pos_count = sum(1 for word in POSITIVE_KEYWORDS if word in combined_text)
            neg_count = sum(1 for word in NEGATIVE_KEYWORDS if word in combined_text)

            if pos_count + neg_count == 0:
                return 0

            return round((pos_count - neg_count) / (pos_count + neg_count), 2)
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        return 0

def get_news_sentiment_label(news_text):
    """Get sentiment label from news text"""
    if not news_text:
        return "Neutral"

    news_lower = news_text.lower()
    pos_count = sum(1 for word in POSITIVE_KEYWORDS if word in news_lower)
    neg_count = sum(1 for word in NEGATIVE_KEYWORDS if word in news_lower)

    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    return "Neutral"

def classify_news_type(news_text):
    """Classify news into types using keywords"""
    if not news_text:
        return []

    news_lower = news_text.lower()
    types = []

    for news_type, keywords in NEWS_TYPE_KEYWORDS.items():
        if any(keyword in news_lower for keyword in keywords):
            types.append(news_type)

    # Return unique types, max 3
    return list(set(types))[:3] if types else []

def fetch_price_from_nse(symbol):
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
            logger.warning(f"⚠️ NSE quote HTTP {resp.status_code} for {symbol}")
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
        logger.warning(f"⚠️ NSE quote failed for {symbol}: {e}")
        return None


def get_market_intelligence_from_nse(symbol, cap_size):
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

    # Fetch comprehensive news
    news_text, news_titles = fetch_comprehensive_news(symbol)

    # AI Sentiment analysis
    ai_sentiment = analyze_ai_sentiment(news_titles)

    # News sentiment label and type classification
    news_sentiment = get_news_sentiment_label(news_text) if news_text else None
    news_types = classify_news_type(news_text) if news_text else []

    logger.info(
        f"✅ {symbol}: (NSE) Price=₹{latest_price:.2f}, "
        f"Momentum≈{momentum*100:.1f}% (1D), Volume≈{vol_surge:.2f}x, AI_sent={ai_sentiment}"
    )

    return {
        "ticker": symbol,
        "cap": cap_size,
        "sector": sector,
        "price": round(latest_price, 2),
        "market_cap": market_cap,
        "mom": round(momentum, 4),
        "vol": round(vol_surge, 2),
        "sent": ai_sentiment,
        "news": news_text,
        "news_sentiment": news_sentiment,
        "news_types": news_types,
        "has_data": True,
    }


def get_market_intelligence(symbol, cap_size):
    """Complete market intelligence with AI sentiment and news"""
    try:
        stock = yf.Ticker(f"{symbol}.NS")
        df = stock.history(period="7mo", auto_adjust=True)

        # Check if we have sufficient data
        has_data = not df.empty and len(df) >= 20

        if has_data:
            # Normal case: sufficient data available
            # Calculate metrics
            latest_price = df['Close'].iloc[-1]
            momentum = (df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]
            avg_vol = df['Volume'].tail(20).mean()
            vol_surge = df['Volume'].iloc[-1] / avg_vol if avg_vol > 0 else 0

            # Get market capitalization and sector
            market_cap = None
            sector = "Unknown"
            try:
                info = stock.info
                market_cap_raw = info.get('marketCap', None)
                if market_cap_raw:
                    # Convert to crores (1 crore = 10 million)
                    market_cap = round(market_cap_raw / 10000000, 2)

                # Get sector information
                sector = info.get('sector', info.get('industry', 'Unknown'))
            except Exception:
                # Ignore failures in fetching static company metadata
                pass

            # Fetch comprehensive news
            news_text, news_titles = fetch_comprehensive_news(symbol)

            # AI Sentiment analysis
            ai_sentiment = analyze_ai_sentiment(news_titles)

            # News sentiment label and type classification
            news_sentiment = get_news_sentiment_label(news_text) if news_text else None
            news_types = classify_news_type(news_text) if news_text else []

            logger.info(
                f"✅ {symbol}: Price=₹{latest_price:.2f}, Momentum={momentum*100:.1f}%, Volume={vol_surge:.2f}x"
            )

            return {
                "ticker": symbol,
                "cap": cap_size,
                "sector": sector,
                "price": round(latest_price, 2),
                "market_cap": market_cap,
                "mom": round(momentum, 4),
                "vol": round(vol_surge, 2),
                "sent": ai_sentiment,
                "news": news_text,
                "news_sentiment": news_sentiment,
                "news_types": news_types,
                "has_data": True
            }
        else:
            # No data from yfinance – try NSE fallback
            logger.warning(f"⚠️  {symbol}: No data from yfinance, trying NSE fallback")
            alt = get_market_intelligence_from_nse(symbol, cap_size)
            if alt:
                return alt

            logger.warning(f"⚠️  {symbol}: No data from any source - adding with NA values")
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
                "has_data": False
            }
    except Exception as e:
        logger.warning(f"⚠️  {symbol}: yfinance error ({str(e)}). Trying NSE fallback...")
        alt = get_market_intelligence_from_nse(symbol, cap_size)
        if alt:
            return alt

        logger.warning(f"⚠️  {symbol}: Error - adding with NA values ({str(e)})")
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
            "has_data": False
        }

def calculate_score(momentum, volume_surge, signal):
    """Calculate investment score"""
    score = 0

    if signal == "🚀 Strong Buy":
        score += 1000
    elif signal == "👀 Watch":
        score += 500

    score += momentum * 500
    score += volume_surge * 50

    return round(score, 2)

def send_to_notion(data, rank=None):
    """Send comprehensive data to Notion"""
    try:
        # Get pre-calculated signal and score (or calculate if not present)
        signal = data.get('signal')
        score = data.get('score')

        if signal is None:
            # Fallback: calculate signal if not already done
            if not data.get('has_data', True):
                signal = "❄️ N/A"
                score = 0
            else:
                signal = "❄️ Neutral"
                if data['sent'] > 0.3 and data['mom'] > 0.10 and data['vol'] > 1.2:
                    signal = "🚀 Strong Buy"
                elif data['sent'] > 0 or data['mom'] > 0.05 or data['vol'] > 1.1:
                    signal = "👀 Watch"
                score = calculate_score(data['mom'], data['vol'], signal)

        # Build payload
        payload = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Ticker": {"title": [{"text": {"content": data['ticker']}}]},
                "Market Cap": {"select": {"name": data['cap']}},
                "Sector": {"select": {"name": data.get('sector', 'Unknown')}},
                "Sentiment": {"number": data['sent']},
                "Momentum (%)": {"number": data['mom']},
                "Volume Surge": {"number": data['vol']},
                "Score": {"number": score},
                "Signal": {"select": {"name": signal}},
                "Last Updated": {"date": {"start": datetime.now().isoformat()}}
            }
        }

        # Add price only if available
        if data.get('price') is not None:
            payload["properties"]["Price (₹)"] = {"number": data['price']}

        # Add rank if provided
        if rank is not None:
            payload["properties"]["Rank"] = {"number": rank}

        # Add market cap if available
        if data.get('market_cap') is not None:
            payload["properties"]["Capital Market (₹)"] = {"number": data['market_cap']}

        # Add news if available
        if data.get('news'):
            payload["properties"]["News & Updates"] = {
                "rich_text": [{"text": {"content": data['news'][:2000]}}]
            }

        # Add news sentiment if available
        if data.get('news_sentiment'):
            payload["properties"]["News Sentiment"] = {
                "select": {"name": data['news_sentiment']}
            }

        # Add news types if available
        if data.get('news_types'):
            payload["properties"]["News Type"] = {
                "multi_select": [{"name": news_type} for news_type in data['news_types']]
            }

        # Add analyst ratings if already fetched
        if data.get('consensus'):
            payload["properties"]["Consensus"] = {
                "select": {"name": data['consensus']}
            }

        if data.get('rating_numeric') and data.get('analyst_count'):
            rating_text = f"{data['rating_numeric']:.2f}/5.0 ({data['analyst_count']} analysts)"
            payload["properties"]["Ratings"] = {
                "rich_text": [{"text": {"content": rating_text}}]
            }
        elif data.get('has_data', True):
            # No analyst data available
            payload["properties"]["Consensus"] = {"select": {"name": "No Consensus"}}
            payload["properties"]["Ratings"] = {"rich_text": [{"text": {"content": "N/A"}}]}

        # Send to Notion
        url = "https://api.notion.com/v1/pages"
        response = SESSION.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            logger.info(f"✅ {data['ticker']}: {signal}, Score: {score}, News: {data.get('news_sentiment', 'N/A')}")
            return True
        else:
            logger.error(f"Notion error for {data['ticker']}: {response.text[:100]}")
            return False

    except Exception as e:
        logger.error(f"Error sending {data['ticker']} to Notion: {str(e)}")
        return False

def main():
    """Main execution loop with comprehensive statistics and intelligent ranking"""
    logger.info("="*70)
    logger.info("MARKET INTELLIGENCE BOT - AI SENTIMENT VERSION")
    logger.info("Analyzing 650 NSE stocks (Nifty 150 + Midcap 200 + Smallcap 300)")
    if HAS_RANKING_ENGINE:
        logger.info("🏆 Intelligent Multi-Factor Ranking: ENABLED")
    logger.info("="*70)

    # Get stocks (with validation if available)
    if get_validated_stocks:
        logger.info("🔍 Using validated stock list (removes stocks without data)...")
        stocks = get_validated_stocks()
    else:
        logger.info("🔍 Using full stock list...")
        if get_all_stocks_with_classification is None:
            logger.error("Stock data module not available!")
            logger.error("Please ensure data/nse_stocks_650.py exists and is accessible.")
            return
        stocks = get_all_stocks_with_classification()

    logger.info(f"📊 Total stocks to analyze: {len(stocks)}")
    logger.info(f"⏱️  Estimated time: ~{len(stocks) * 2 // 60} minutes")
    logger.info("")

    # Statistics tracking
    stats = {
        "total": len(stocks),
        "processed": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "strong_buy": 0,
        "watch": 0,
        "neutral": 0,
        "with_news": 0,
        "positive_news": 0,
        "negative_news": 0,
        "by_cap": {"Large Cap": 0, "Mid Cap": 0, "Small Cap": 0}
    }

    start_time = time.time()

    # PHASE 1: Collect all stock data
    logger.info("📊 PHASE 1: Collecting market intelligence for all stocks...")
    all_stocks_data = []

    for i, (ticker, cap_size) in enumerate(stocks, 1):
        logger.info(f"[{i}/{len(stocks)}] Processing {ticker} ({cap_size})...")

        try:
            data = get_market_intelligence(ticker, cap_size)

            if data:
                stats["processed"] += 1
                stats["by_cap"][cap_size] = stats["by_cap"].get(cap_size, 0) + 1

                # Calculate signal and score now (needed for ranking)
                if not data.get('has_data', True):
                    signal = "❄️ N/A"
                    score = 0
                else:
                    signal = "❄️ Neutral"
                    if data['sent'] > 0.3 and data['mom'] > 0.10 and data['vol'] > 1.2:
                        signal = "🚀 Strong Buy"
                    elif data['sent'] > 0 or data['mom'] > 0.05 or data['vol'] > 1.1:
                        signal = "👀 Watch"
                    score = calculate_score(data['mom'], data['vol'], signal)

                # Add signal and score to data
                data['signal'] = signal
                data['score'] = score

                # Fetch analyst ratings if available (needed for ranking)
                if HAS_ANALYST_RATINGS and data.get('has_data', True):
                    try:
                        logger.info(f"   📊 Fetching analyst ratings for {ticker}...")
                        ratings_data = aggregate_all_analyst_ratings(ticker)
                        if ratings_data['has_data']:
                            data['consensus'] = ratings_data['consensus']
                            data['rating_numeric'] = ratings_data['rating_numeric']
                            data['analyst_count'] = ratings_data['analyst_count']
                            logger.info(f"   ✅ Ratings: {ratings_data['consensus']} ({ratings_data['rating_numeric']:.2f}/5.0)")
                        else:
                            data['consensus'] = "No Consensus"
                            data['rating_numeric'] = None
                            data['analyst_count'] = 0
                    except Exception as e:
                        logger.warning(f"   ⚠️  Failed to fetch ratings: {str(e)}")
                        data['consensus'] = "No Consensus"
                        data['rating_numeric'] = None
                        data['analyst_count'] = 0

                # Track news
                if data.get('news'):
                    stats["with_news"] += 1
                    if data.get('news_sentiment') == "Positive":
                        stats["positive_news"] += 1
                    elif data.get('news_sentiment') == "Negative":
                        stats["negative_news"] += 1

                all_stocks_data.append(data)
            else:
                stats["skipped"] += 1

            time.sleep(1.5)  # Rate limiting

        except Exception as e:
            logger.error(f"❌ Error processing {ticker}: {str(e)}")
            stats["failed"] += 1

        # Progress update every 50 stocks
        if i % 50 == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed if elapsed > 0 else 1
            remaining = (len(stocks) - i) / rate if rate > 0 else 0
            logger.info(f"📈 Progress: {i}/{len(stocks)}, ~{remaining/60:.1f} min remaining, Processed: {stats['processed']}")

    # PHASE 2: Intelligent ranking
    logger.info("\n" + "="*70)
    logger.info("🏆 PHASE 2: Calculating intelligent rankings...")
    logger.info("="*70)

    if HAS_RANKING_ENGINE and all_stocks_data:
        ranked_stocks = rank_stocks(all_stocks_data)
        logger.info(f"✅ Ranked {len(ranked_stocks)} stocks successfully")
        top_3 = ', '.join([f"{s['ticker']}#{s['rank']}" for s in ranked_stocks[:3]])
        logger.info(f"   Top 3: {top_3}")
    else:
        logger.info("⚠️  Using serial ranking (ranking engine not available)")
        ranked_stocks = all_stocks_data
        for i, stock in enumerate(ranked_stocks, 1):
            stock['rank'] = i

    # PHASE 3: Send to Notion with ranks
    logger.info("\n" + "="*70)
    logger.info("📤 PHASE 3: Sending ranked data to Notion...")
    logger.info("="*70)

    for stock_data in ranked_stocks:
        try:
            if send_to_notion(stock_data, rank=stock_data['rank']):
                stats["success"] += 1

                # Track signals
                signal = stock_data.get('signal', "❄️ Neutral")
                if signal == "🚀 Strong Buy":
                    stats["strong_buy"] += 1
                elif signal == "👀 Watch":
                    stats["watch"] += 1
                else:
                    stats["neutral"] += 1
            else:
                stats["failed"] += 1

            time.sleep(0.5)  # Light rate limiting

        except Exception as e:
            logger.error(f"❌ Error sending {stock_data['ticker']} to Notion: {str(e)}")
            stats["failed"] += 1

    # Final statistics
    elapsed_time = time.time() - start_time

    logger.info("\n" + "="*70)
    logger.info("📊 ANALYSIS COMPLETE - FINAL STATISTICS")
    logger.info("="*70)
    logger.info("")
    logger.info("📈 PROCESSING SUMMARY:")
    logger.info(f"   Total Stocks: {stats['total']}")
    logger.info(f"   ✅ Successful: {stats['success']}")
    logger.info(f"   ❌ Failed: {stats['failed']}")
    logger.info(f"   ⏭️ Skipped: {stats['skipped']}")
    logger.info("")
    logger.info("🎯 SIGNALS BREAKDOWN:")
    logger.info(f"   � Strong Buy: {stats['strong_buy']}")
    logger.info(f"   👀 Watch: {stats['watch']}")
    logger.info(f"   ❄️ Neutral: {stats['neutral']}")
    logger.info("")
    logger.info("📰 NEWS COVERAGE:")
    logger.info(f"   Total with News: {stats['with_news']} ({stats['with_news']*100//max(stats['success'],1)}%)")
    logger.info(f"   Positive Sentiment: {stats['positive_news']}")
    logger.info(f"   Negative Sentiment: {stats['negative_news']}")
    logger.info("")
    logger.info("💼 BY MARKET CAP:")
    logger.info(f"   Large Cap: {stats['by_cap'].get('Large Cap', 0)}")
    logger.info(f"   Mid Cap: {stats['by_cap'].get('Mid Cap', 0)}")
    logger.info(f"   Small Cap: {stats['by_cap'].get('Small Cap', 0)}")
    logger.info("")
    logger.info("⏱️ PERFORMANCE:")
    logger.info(f"   Time Taken: {elapsed_time/60:.1f} minutes")
    logger.info(f"   Rate: {stats['success']/(elapsed_time/60):.1f} stocks/min")
    logger.info("="*70)
    logger.info("✅ Check your Notion database!")

    return stats

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⏹️ Analysis stopped by user")
    except Exception as e:
        logger.error(f"\n❌ Critical error: {str(e)}")
        import traceback
        traceback.print_exc()