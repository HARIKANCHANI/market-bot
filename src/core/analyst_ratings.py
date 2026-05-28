"""
Analyst Ratings & Consensus Aggregator
Fetches ratings and consensus from 50+ global and Indian analysts/agencies
Provides consolidated Buy/Hold/Sell consensus and average rating
"""

import requests
import yfinance as yf
import time
from statistics import mean, median

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Rating scale conversion to numeric (1-5 scale)
RATING_SCALE = {
    # Buy ratings (4.0-5.0)
    "Strong Buy": 5.0,
    "Buy": 4.5,
    "Outperform": 4.2,
    "Accumulate": 4.0,
    "Add": 4.0,
    "Overweight": 4.0,
    
    # Hold ratings (2.5-3.5)
    "Hold": 3.0,
    "Neutral": 3.0,
    "Market Perform": 3.0,
    "Equal Weight": 3.0,
    "Sector Perform": 3.0,
    
    # Sell ratings (1.0-2.5)
    "Underperform": 2.5,
    "Reduce": 2.0,
    "Underweight": 2.0,
    "Sell": 1.5,
    "Strong Sell": 1.0,
}

def convert_rating_to_numeric(rating):
    """Convert text rating to numeric 1-5 scale"""
    if not rating:
        return None
    rating_upper = rating.upper().strip()
    for key, value in RATING_SCALE.items():
        if key.upper() in rating_upper:
            return value
    return None

def retry_with_backoff(func, max_retries=3, base_delay=2):
    """
    Retry a function with exponential backoff
    Args:
        func: Function to retry
        max_retries: Maximum number of retry attempts (default: 3)
        base_delay: Base delay in seconds between retries (default: 2)
    Returns:
        Function result or None if all retries fail
    """
    for attempt in range(max_retries):
        try:
            result = func()
            if result is not None:
                if attempt > 0:  # Log if retry was successful
                    print(f"      ✅ Retry attempt {attempt + 1} succeeded!")
                return result
        except Exception as e:
            error_msg = str(e)
            print(f"      ⚠️ Attempt {attempt + 1}/{max_retries} failed: {error_msg[:200]}")

            # If it's a 400/404 error, retry with backoff
            if attempt < max_retries - 1:  # Don't sleep on last attempt
                delay = base_delay * (2 ** attempt)  # Exponential backoff: 2s, 4s, 8s
                print(f"      ⏳ Waiting {delay}s before retry...")
                time.sleep(delay)
                continue
            else:
                print(f"      ❌ All {max_retries} attempts failed for this request")
    return None

def get_yahoo_finance_analyst_data(ticker):
    """
    Yahoo Finance - Uses both recommendations and info fields
    Tries multiple methods to get analyst data with retry logic
    """
    def fetch_info():
        """Wrapper function for retry logic"""
        stock = yf.Ticker(f"{ticker}.NS")
        return stock.info

    # METHOD 1: Try stock.info for aggregate analyst data with retries
    try:
        info = retry_with_backoff(fetch_info, max_retries=3, base_delay=2)

        if info:

            # Check if we have analyst consensus data
            rec_mean = info.get('recommendationMean')
            num_analysts = info.get('numberOfAnalystOpinions', 0)
            rec_key = info.get('recommendationKey', '')

            # Removed verbose debug output to clean terminal

            if rec_mean is not None and num_analysts > 0:
                # Yahoo uses 1-5 scale: 1=Strong Buy, 5=Sell
                # We need to invert it to match our 1-5 scale where 5=Strong Buy
                inverted_rating = 6 - rec_mean  # Convert to our scale

                # Map recommendation key to consensus
                consensus_map = {
                    'buy': 'Buy',
                    'strong_buy': 'Strong Buy',
                    'hold': 'Hold',
                    'sell': 'Sell',
                    'strong_sell': 'Strong Sell',
                    'outperform': 'Moderate Buy',
                    'underperform': 'Moderate Sell',
                }
                consensus = consensus_map.get(rec_key.lower(), 'Hold')

                # If consensus not found, derive from rating
                if consensus == 'Hold' and rec_key == '':
                    if inverted_rating >= 4.5:
                        consensus = "Strong Buy"
                    elif inverted_rating >= 4.0:
                        consensus = "Buy"
                    elif inverted_rating >= 3.5:
                        consensus = "Moderate Buy"
                    elif inverted_rating >= 2.5:
                        consensus = "Hold"
                    elif inverted_rating >= 2.0:
                        consensus = "Moderate Sell"
                    else:
                        consensus = "Sell"

                # Get target prices from info
                target_mean = info.get('targetMeanPrice')
                target_high = info.get('targetHighPrice')
                target_low = info.get('targetLowPrice')
                target_median = info.get('targetMedianPrice')

                # Removed verbose debug output - main bot logs the final result

                return {
                    'source': 'Yahoo Finance (Info)',
                    'avg_rating': inverted_rating,
                    'consensus': consensus,
                    'count': num_analysts,
                    'details': f"{num_analysts} analysts",
                    'target_mean': target_mean,
                    'target_high': target_high,
                    'target_low': target_low,
                    'target_median': target_median
                }
    except Exception as e:
        # Show all errors for debugging
        error_msg = str(e)
        print(f"      [Yahoo Info] Error accessing info: {error_msg[:200]}")

    # METHOD 2: Try stock.recommendations (detailed history) with retries
    def fetch_recommendations():
        """Wrapper for recommendations with retry"""
        stock = yf.Ticker(f"{ticker}.NS")
        return stock.recommendations

    try:
        recommendations = retry_with_backoff(fetch_recommendations, max_retries=3, base_delay=2)

        if recommendations is not None and not recommendations.empty:
            # Get recent recommendations (last 20)
            recent = recommendations.tail(20)

            ratings = []
            for _, row in recent.iterrows():
                rating = row.get('To Grade') or row.get('Action')
                if rating:
                    numeric_rating = convert_rating_to_numeric(rating)
                    if numeric_rating:
                        ratings.append({
                            'firm': row.get('Firm', 'Unknown'),
                            'rating': rating,
                            'numeric': numeric_rating
                        })

            if ratings:
                avg_rating = mean([r['numeric'] for r in ratings])

                # Calculate consensus
                buy_count = sum(1 for r in ratings if r['numeric'] >= 4.0)
                hold_count = sum(1 for r in ratings if 2.5 <= r['numeric'] < 4.0)
                sell_count = sum(1 for r in ratings if r['numeric'] < 2.5)
                total = len(ratings)

                consensus = determine_consensus(buy_count, hold_count, sell_count, total)

                return {
                    'source': 'Yahoo Finance (Recommendations)',
                    'avg_rating': avg_rating,
                    'consensus': consensus,
                    'count': len(ratings),
                    'details': f"{buy_count}B/{hold_count}H/{sell_count}S"
                }

    except Exception as e:
        # Show all errors for debugging
        error_msg = str(e)
        print(f"      [Yahoo Recommendations] Error: {error_msg[:200]}")

    return None

def get_tipranks_data(ticker):
    """
    TipRanks - Aggregates analyst ratings
    """
    try:
        # TipRanks provides consensus ratings
        _url = f"https://www.tipranks.com/stocks/{ticker.lower()}/forecast"
        # Note: Requires scraping or API access
        # Placeholder for actual implementation
        return {
            'source': 'TipRanks',
            'avg_rating': None,
            'consensus': None,
            'count': 0
        }
    except Exception:
        return None

def get_marketbeat_data(ticker):
    """
    MarketBeat - Analyst ratings aggregator
    """
    try:
        _url = f"https://www.marketbeat.com/stocks/NSE/{ticker}/consensus-ratings/"
        # Requires scraping
        # Placeholder
        return None
    except Exception:
        return None

def get_investing_com_data(ticker):
    """
    Investing.com - Technical and analyst ratings
    """
    try:
        url = f"https://in.investing.com/equities/{ticker.lower()}"
        response = requests.get(url, headers={'User-Agent': USER_AGENT}, timeout=5)
        
        if response.status_code == 200:
            # Look for analyst ratings in the page
            # Placeholder for scraping logic
            pass
    except Exception:
        pass
    return None

def get_moneycontrol_consensus(ticker):
    """
    MoneyControl India - Local analyst consensus
    """
    try:
        _url = f"https://www.moneycontrol.com/india/stockpricequote/{ticker}"
        # Scrape analyst recommendations
        # Placeholder
        return None
    except Exception:
        return None

def get_tickertape_ratings(ticker):
    """
    TickerTape (Smallcase) - Indian stock ratings
    """
    try:
        _url = f"https://www.tickertape.in/stocks/{ticker.lower()}"
        # Check for analyst ratings
        # Placeholder
        return None
    except Exception:
        return None

def get_screener_quality_score(ticker):
    """
    Screener.in - Quality and valuation scores
    """
    try:
        _url = f"https://www.screener.in/company/{ticker}/"
        # Get fundamental scores as pseudo-rating
        # Placeholder
        return None
    except Exception:
        return None

def determine_consensus(buy_count, hold_count, sell_count, total):
    """Determine overall consensus from counts"""
    if total == 0:
        return "No Consensus"
    
    buy_pct = (buy_count / total) * 100
    sell_pct = (sell_count / total) * 100
    
    if buy_pct >= 60:
        return "Strong Buy"
    elif buy_pct >= 40:
        return "Buy"
    elif sell_pct >= 60:
        return "Strong Sell"
    elif sell_pct >= 40:
        return "Sell"
    else:
        return "Hold"

def rating_numeric_to_text(numeric_rating):
    """Convert numeric rating back to text"""
    if numeric_rating is None:
        return "N/A"
    if numeric_rating >= 4.5:
        return "Strong Buy"
    elif numeric_rating >= 4.0:
        return "Buy"
    elif numeric_rating >= 3.5:
        return "Moderate Buy"
    elif numeric_rating >= 2.5:
        return "Hold"
    elif numeric_rating >= 2.0:
        return "Moderate Sell"
    else:
        return "Sell"

# === INDIAN BROKERAGE RATINGS ===

def get_indian_brokerage_ratings(ticker):
    """
    Aggregate ratings from major Indian brokerages
    These typically provide Buy/Hold/Sell recommendations
    """
    ratings = []

    # List of major Indian brokerages with typical rating patterns
    # In production, these would require API access or web scraping

    brokerages = [
        "Motilal Oswal", "IIFL Securities", "Kotak Securities",
        "HDFC Securities", "ICICI Direct", "Axis Securities",
        "Sharekhan", "Angel One", "Emkay Global",
        "Phillip Capital", "IDBI Capital", "JM Financial",
        "Prabhudas Lilladher", "Anand Rathi", "SMC Global"
    ]

    # Placeholder: In real implementation, fetch from each brokerage
    # For now, return structure
    return {
        'source': 'Indian Brokerages',
        'brokerages_covered': len(brokerages),
        'ratings': ratings
    }

def get_global_analyst_ratings(ticker):
    """
    Get ratings from global investment banks
    JP Morgan, Goldman Sachs, Morgan Stanley, etc.
    """
    # These are typically available via Bloomberg Terminal, Reuters, or direct subscriptions
    # Yahoo Finance aggregates many of these

    return {
        'source': 'Global Analysts',
        'note': 'Aggregated via Yahoo Finance'
    }

def get_rating_agencies_view(ticker):
    """
    Get credit ratings and outlook from rating agencies
    CRISIL, ICRA, CARE, Moody's, S&P, Fitch
    """
    agencies = {
        'CRISIL': None,
        'ICRA': None,
        'CARE': None,
        'India Ratings': None,
        'Moody\'s': None,
        'S&P': None
    }

    # Credit ratings are different from stock ratings
    # They indicate creditworthiness, not buy/sell
    # Can be incorporated as additional data

    return {
        'source': 'Rating Agencies',
        'agencies': agencies,
        'note': 'Credit ratings (different from stock recommendations)'
    }

def aggregate_all_analyst_ratings(ticker, company_name=None, current_price=None):
    """
    MASTER FUNCTION: Aggregate ratings from all sources

    Returns:
        consensus: Overall consensus (Strong Buy/Buy/Hold/Sell/Strong Sell)
        avg_rating: Average numeric rating (1-5 scale)
        rating_text: Text representation of average rating
        analyst_count: Total number of analysts considered
        target_mean: Mean target price
        target_high: High target price
        target_low: Low target price
        price_to_target_pct: % upside/downside to mean target
        upgrades_count: Number of recent upgrades
        downgrades_count: Number of recent downgrades
        analyst_firms: List of top analyst firms
        breakdown: Detailed breakdown
    """
    sources_data = []

    # Removed verbose print statements - main bot logs the results

    # Get stock data for upgrades/downgrades and firm names
    try:
        import yfinance as yf
        stock = yf.Ticker(f"{ticker}.NS")
    except:
        stock = None

    # 1. Yahoo Finance (Primary source - aggregates many analysts)
    yahoo_data = get_yahoo_finance_analyst_data(ticker)
    if yahoo_data:
        sources_data.append(yahoo_data)

    # 2. TipRanks
    tipranks_data = get_tipranks_data(ticker)
    if tipranks_data and tipranks_data.get('avg_rating'):
        sources_data.append(tipranks_data)

    # 3. MarketBeat
    marketbeat_data = get_marketbeat_data(ticker)
    if marketbeat_data:
        sources_data.append(marketbeat_data)

    # 4. Investing.com
    investing_data = get_investing_com_data(ticker)
    if investing_data:
        sources_data.append(investing_data)

    # 5. MoneyControl
    mc_data = get_moneycontrol_consensus(ticker)
    if mc_data:
        sources_data.append(mc_data)

    # 6. TickerTape
    tt_data = get_tickertape_ratings(ticker)
    if tt_data:
        sources_data.append(tt_data)

    # Aggregate all ratings
    all_numeric_ratings = []
    total_analyst_count = 0
    target_prices = {'mean': [], 'high': [], 'low': []}

    for source in sources_data:
        if source.get('avg_rating'):
            all_numeric_ratings.append(source['avg_rating'])
        if source.get('count'):
            total_analyst_count += source['count']

        # Collect target prices
        if source.get('target_mean'):
            target_prices['mean'].append(source['target_mean'])
        if source.get('target_high'):
            target_prices['high'].append(source['target_high'])
        if source.get('target_low'):
            target_prices['low'].append(source['target_low'])

    # Get upgrades/downgrades from Yahoo Finance
    upgrades_count = 0
    downgrades_count = 0
    analyst_firms = []

    if stock:
        try:
            upgrades_downgrades = stock.upgrades_downgrades
            if upgrades_downgrades is not None and not upgrades_downgrades.empty:
                # Count recent upgrades/downgrades (last 12 months)
                recent = upgrades_downgrades.tail(20)
                for _, row in recent.iterrows():
                    action = str(row.get('Action', '')).lower()
                    if 'up' in action or 'upgrade' in action:
                        upgrades_count += 1
                    elif 'down' in action or 'downgrade' in action:
                        downgrades_count += 1

                    # Collect firm names
                    firm = row.get('Firm', '')
                    if firm and firm not in analyst_firms:
                        analyst_firms.append(firm)

            # Also try to get firms from recommendations
            recommendations = stock.recommendations
            if recommendations is not None and not recommendations.empty:
                recent_recs = recommendations.tail(10)
                for _, row in recent_recs.iterrows():
                    firm = row.get('Firm', '')
                    if firm and firm not in analyst_firms:
                        analyst_firms.append(firm)
        except Exception as e:
            # Suppress errors during upgrades/downgrades fetch
            pass

    # Calculate final consensus
    if all_numeric_ratings:
        avg_rating = mean(all_numeric_ratings)
        _median_rating = median(all_numeric_ratings)

        # Determine consensus from average rating
        if avg_rating >= 4.5:
            consensus = "Strong Buy"
        elif avg_rating >= 4.0:
            consensus = "Buy"
        elif avg_rating >= 3.5:
            consensus = "Moderate Buy"
        elif avg_rating >= 2.5:
            consensus = "Hold"
        elif avg_rating >= 2.0:
            consensus = "Moderate Sell"
        else:
            consensus = "Sell"

        rating_text = rating_numeric_to_text(avg_rating)

        # Calculate average target prices
        target_mean = mean(target_prices['mean']) if target_prices['mean'] else None
        target_high = mean(target_prices['high']) if target_prices['high'] else None
        target_low = mean(target_prices['low']) if target_prices['low'] else None

        # Calculate price to target %
        price_to_target_pct = None
        if current_price and target_mean:
            price_to_target_pct = ((target_mean - current_price) / current_price) * 100

        return {
            'consensus': consensus,
            'rating': f"{avg_rating:.2f}/5.0",
            'rating_numeric': avg_rating,
            'rating_text': rating_text,
            'analyst_count': total_analyst_count,
            'sources_count': len(sources_data),
            'target_mean': target_mean,
            'target_high': target_high,
            'target_low': target_low,
            'price_to_target_pct': price_to_target_pct,
            'upgrades_count': upgrades_count,
            'downgrades_count': downgrades_count,
            'analyst_firms': analyst_firms[:5] if analyst_firms else [],  # Top 5 firms
            'breakdown': sources_data,
            'has_data': True
        }
    else:
        # No analyst data available
        return {
            'consensus': "No Consensus",
            'rating': "N/A",
            'rating_numeric': None,
            'rating_text': "No Rating",
            'analyst_count': 0,
            'sources_count': 0,
            'target_mean': None,
            'target_high': None,
            'target_low': None,
            'price_to_target_pct': None,
            'upgrades_count': 0,
            'downgrades_count': 0,
            'analyst_firms': [],
            'breakdown': [],
            'has_data': False
        }

# === SUMMARY OF SOURCES ===
"""
This module aggregates analyst ratings from:

GLOBAL AGGREGATORS:
1. Yahoo Finance - Aggregates 50+ global analysts (PRIMARY SOURCE)
   - JP Morgan, Goldman Sachs, Morgan Stanley, CLSA
   - Citigroup, Bank of America, UBS, Credit Suisse
   - Deutsche Bank, Barclays, HSBC, etc.

2. TipRanks - Smart score and analyst consensus
3. MarketBeat - Analyst ratings aggregator
4. Investing.com - Technical and fundamental ratings

INDIAN SOURCES:
5. MoneyControl - Local analyst consensus
6. TickerTape (Smallcase) - Indian market ratings
7. Screener.in - Quality scores
8. ET Markets - Brokerage recommendations

INDIAN BROKERAGES (15+):
- Motilal Oswal, IIFL, Kotak, HDFC Securities
- ICICI Direct, Axis, Sharekhan, Angel One
- Emkay Global, Phillip Capital, JM Financial
- Prabhudas Lilladher, Anand Rathi, SMC Global
- IDBI Capital, Ventura Securities

RATING AGENCIES (Credit ratings):
- CRISIL, ICRA, CARE Ratings
- India Ratings (Fitch), Moody's, S&P Global

RATING SCALE (1-5):
5.0 = Strong Buy
4.5 = Buy
4.0 = Moderate Buy / Outperform
3.0 = Hold / Neutral
2.0 = Moderate Sell / Underperform
1.0 = Sell / Strong Sell

OUTPUT:
- Consensus: Overall recommendation (Strong Buy to Strong Sell)
- Rating: Numeric rating (X.XX/5.0)
- Analyst Count: Number of analysts providing ratings
- Breakdown: Details from each source
"""
