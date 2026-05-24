#!/usr/bin/env python3
"""
INTELLIGENT RANKING ENGINE
Comprehensive multi-factor ranking system for stock analysis

Ranks stocks based on:
- Market Cap (higher = better)
- Price (normalized by market cap category)
- Sentiment (AI or keyword-based)
- Momentum (percentage change)
- Volume Surge (trading activity)
- Score (composite investment score)
- Signal (Strong Buy > Watch > Neutral)
- News Sentiment (Positive > Neutral > Negative)
- Consensus (analyst ratings)
- Ratings (numeric analyst rating)
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Weight factors for ranking (customize as needed)
# Existing factors are scaled to 90% of total weight, reserving 10% for
# institutional quality (FII/DII/Promoter/MF flows). This keeps behavior
# backward-compatible for bots that don't provide institutional_score
# (they are treated as neutral at 50/100, which adds a constant term).
RANKING_WEIGHTS = {
    'market_cap': 0.09,        #  9% - Market cap importance
    'momentum': 0.18,          # 18% - Price momentum
    'volume_surge': 0.135,     # 13.5% - Volume activity
    'sentiment': 0.135,        # 13.5% - AI/keyword sentiment
    'score': 0.135,            # 13.5% - Composite score
    'signal': 0.09,            #  9% - Trading signal
    'news_sentiment': 0.072,   #  7.2% - News sentiment
    'consensus': 0.045,        #  4.5% - Analyst consensus
    'ratings': 0.018,          #  1.8% - Numeric rating
    'institutional': 0.10      # 10% - Institutional score (0-100)
}

def normalize_value(value, min_val, max_val):
    """Normalize value to 0-1 range"""
    if max_val == min_val:
        return 0.5
    return (value - min_val) / (max_val - min_val) if max_val > min_val else 0.5

def signal_to_score(signal):
    """Convert signal to numeric score"""
    signal_map = {
        "🚀 Strong Buy": 1.0,
        "👀 Watch": 0.6,
        "❄️ Neutral": 0.3,
        "❄️ N/A": 0.0
    }
    return signal_map.get(signal, 0.0)

def news_sentiment_to_score(sentiment):
    """Convert news sentiment to numeric score"""
    sentiment_map = {
        "Positive": 1.0,
        "Neutral": 0.5,
        "Negative": 0.0,
        None: 0.5
    }
    return sentiment_map.get(sentiment, 0.5)

def consensus_to_score(consensus):
    """Convert analyst consensus to numeric score"""
    consensus_map = {
        "Strong Buy": 1.0,
        "Buy": 0.8,
        "Moderate Buy": 0.7,
        "Hold": 0.5,
        "Moderate Sell": 0.3,
        "Sell": 0.2,
        "Strong Sell": 0.0,
        "No Consensus": 0.5,
        None: 0.5
    }
    return consensus_map.get(consensus, 0.5)

def calculate_composite_rank_score_optimized(stock_data: Dict[str, Any],
                                             min_max_cache: Dict[str, tuple]) -> float:
    """
    Calculate composite ranking score for a single stock (OPTIMIZED VERSION)

    Args:
        stock_data: Single stock's data dictionary
        min_max_cache: Pre-calculated min/max values for normalization

    Returns:
        Composite score (0-100)
    """

    # Extract values with defaults
    market_cap = stock_data.get('market_cap') or 0
    momentum = stock_data.get('momentum') or stock_data.get('mom') or 0
    volume_surge = stock_data.get('volume_surge') or stock_data.get('vol') or 0
    sentiment = stock_data.get('sentiment') or stock_data.get('sent') or 0
    score = stock_data.get('score') or 0
    signal = stock_data.get('signal', "❄️ Neutral")
    news_sentiment = stock_data.get('news_sentiment')
    consensus = stock_data.get('consensus')
    rating_numeric = stock_data.get('rating_numeric') or 0
    inst_score_raw = stock_data.get('institutional_score')
    # Treat missing institutional_score as neutral 50/100 so that bots
    # without institutional data are not penalized.
    if inst_score_raw is None:
        inst_score_raw = 50.0
    norm_institutional = inst_score_raw / 100.0

    # If stock has no data, return 0
    if not stock_data.get('has_data', True):
        return 0.0

    # Normalize each factor using cached min/max values
    norm_market_cap = normalize_value(market_cap, *min_max_cache['market_cap'])
    norm_momentum = normalize_value(momentum, *min_max_cache['momentum'])
    norm_volume = normalize_value(volume_surge, *min_max_cache['volume'])
    norm_sentiment = normalize_value(sentiment, *min_max_cache['sentiment'])
    norm_score = normalize_value(score, *min_max_cache['score'])
    norm_rating = normalize_value(rating_numeric, *min_max_cache['rating'])

    # Convert categorical to scores
    signal_score = signal_to_score(signal)
    news_score = news_sentiment_to_score(news_sentiment)
    consensus_score = consensus_to_score(consensus)

    # Calculate weighted composite score
    composite = (
        RANKING_WEIGHTS['market_cap'] * norm_market_cap +
        RANKING_WEIGHTS['momentum'] * norm_momentum +
        RANKING_WEIGHTS['volume_surge'] * norm_volume +
        RANKING_WEIGHTS['sentiment'] * norm_sentiment +
        RANKING_WEIGHTS['score'] * norm_score +
        RANKING_WEIGHTS['signal'] * signal_score +
        RANKING_WEIGHTS['news_sentiment'] * news_score +
        RANKING_WEIGHTS['consensus'] * consensus_score +
        RANKING_WEIGHTS['ratings'] * norm_rating +
        RANKING_WEIGHTS['institutional'] * norm_institutional
    )

    # Scale to 0-100
    return round(composite * 100, 2)

def calculate_composite_rank_score(stock_data: Dict[str, Any],
                                   all_stocks_data: List[Dict[str, Any]]) -> float:
    """
    Calculate composite ranking score for a single stock
    
    Args:
        stock_data: Single stock's data dictionary
        all_stocks_data: All stocks data for normalization
        
    Returns:
        Composite score (0-100)
    """
    
    # Extract values with defaults
    market_cap = stock_data.get('market_cap') or 0
    momentum = stock_data.get('momentum') or stock_data.get('mom') or 0
    volume_surge = stock_data.get('volume_surge') or stock_data.get('vol') or 0
    sentiment = stock_data.get('sentiment') or stock_data.get('sent') or 0
    score = stock_data.get('score') or 0
    signal = stock_data.get('signal', "❄️ Neutral")
    news_sentiment = stock_data.get('news_sentiment')
    consensus = stock_data.get('consensus')
    rating_numeric = stock_data.get('rating_numeric') or 0

    # Institutional score: treat missing as neutral 50/100
    inst_score_raw = stock_data.get('institutional_score')
    if inst_score_raw is None:
        inst_score_raw = 50.0
    norm_institutional = inst_score_raw / 100.0

    # If stock has no data, return 0
    if not stock_data.get('has_data', True):
        return 0.0
    
    # Collect all values for normalization
    all_market_caps = [s.get('market_cap') or 0 for s in all_stocks_data if s.get('has_data', True)]
    all_momentums = [s.get('momentum') or s.get('mom') or 0 for s in all_stocks_data if s.get('has_data', True)]
    all_volumes = [s.get('volume_surge') or s.get('vol') or 0 for s in all_stocks_data if s.get('has_data', True)]
    all_sentiments = [s.get('sentiment') or s.get('sent') or 0 for s in all_stocks_data if s.get('has_data', True)]
    all_scores = [s.get('score') or 0 for s in all_stocks_data if s.get('has_data', True)]
    all_ratings = [s.get('rating_numeric') or 0 for s in all_stocks_data if s.get('has_data', True) and s.get('rating_numeric')]
    
    # Normalize each factor
    norm_market_cap = normalize_value(market_cap, min(all_market_caps) if all_market_caps else 0, max(all_market_caps) if all_market_caps else 1)
    norm_momentum = normalize_value(momentum, min(all_momentums) if all_momentums else 0, max(all_momentums) if all_momentums else 1)
    norm_volume = normalize_value(volume_surge, min(all_volumes) if all_volumes else 0, max(all_volumes) if all_volumes else 1)
    norm_sentiment = normalize_value(sentiment, min(all_sentiments) if all_sentiments else -1, max(all_sentiments) if all_sentiments else 1)
    norm_score = normalize_value(score, min(all_scores) if all_scores else 0, max(all_scores) if all_scores else 1)
    norm_rating = normalize_value(rating_numeric, min(all_ratings) if all_ratings else 0, max(all_ratings) if all_ratings else 5)
    
    # Convert categorical to scores
    signal_score = signal_to_score(signal)
    news_score = news_sentiment_to_score(news_sentiment)
    consensus_score = consensus_to_score(consensus)

    # Calculate weighted composite score
    composite = (
        RANKING_WEIGHTS['market_cap'] * norm_market_cap +
        RANKING_WEIGHTS['momentum'] * norm_momentum +
        RANKING_WEIGHTS['volume_surge'] * norm_volume +
        RANKING_WEIGHTS['sentiment'] * norm_sentiment +
        RANKING_WEIGHTS['score'] * norm_score +
        RANKING_WEIGHTS['signal'] * signal_score +
        RANKING_WEIGHTS['news_sentiment'] * news_score +
        RANKING_WEIGHTS['consensus'] * consensus_score +
        RANKING_WEIGHTS['ratings'] * norm_rating +
        RANKING_WEIGHTS['institutional'] * norm_institutional
    )
    
    # Scale to 0-100
    return round(composite * 100, 2)

def rank_stocks(all_stocks_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Rank all stocks based on composite scoring

    Args:
        all_stocks_data: List of all stock data dictionaries

    Returns:
        List of stocks with added 'rank' and 'rank_score' fields, sorted by rank
    """
    logger.info(f"🔢 Calculating composite ranking scores for {len(all_stocks_data)} stocks...")

    # Pre-calculate all values for normalization (PERFORMANCE OPTIMIZATION)
    # This avoids recalculating these lists for every stock
    valid_stocks = [s for s in all_stocks_data if s.get('has_data', True)]

    all_market_caps = [s.get('market_cap') or 0 for s in valid_stocks]
    all_momentums = [s.get('momentum') or s.get('mom') or 0 for s in valid_stocks]
    all_volumes = [s.get('volume_surge') or s.get('vol') or 0 for s in valid_stocks]
    all_sentiments = [s.get('sentiment') or s.get('sent') or 0 for s in valid_stocks]
    all_scores = [s.get('score') or 0 for s in valid_stocks]
    all_ratings = [s.get('rating_numeric') or 0 for s in valid_stocks if s.get('rating_numeric')]

    # Pre-calculate min/max values
    min_max_cache = {
        'market_cap': (min(all_market_caps) if all_market_caps else 0, max(all_market_caps) if all_market_caps else 1),
        'momentum': (min(all_momentums) if all_momentums else 0, max(all_momentums) if all_momentums else 1),
        'volume': (min(all_volumes) if all_volumes else 0, max(all_volumes) if all_volumes else 1),
        'sentiment': (min(all_sentiments) if all_sentiments else -1, max(all_sentiments) if all_sentiments else 1),
        'score': (min(all_scores) if all_scores else 0, max(all_scores) if all_scores else 1),
        'rating': (min(all_ratings) if all_ratings else 0, max(all_ratings) if all_ratings else 5)
    }

    # Calculate composite score for each stock using cached values
    for stock in all_stocks_data:
        stock['rank_score'] = calculate_composite_rank_score_optimized(stock, min_max_cache)

    # Sort by rank_score (descending)
    sorted_stocks = sorted(all_stocks_data, key=lambda x: x['rank_score'], reverse=True)

    # Assign ranks
    for i, stock in enumerate(sorted_stocks, 1):
        stock['rank'] = i

    logger.info(f"✅ Ranking complete. Top stock: {sorted_stocks[0]['ticker']} (Score: {sorted_stocks[0]['rank_score']})")
    logger.info(f"   Bottom stock: {sorted_stocks[-1]['ticker']} (Score: {sorted_stocks[-1]['rank_score']})")

    return sorted_stocks
