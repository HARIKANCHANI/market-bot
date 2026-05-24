#!/usr/bin/env python3
"""
Unit tests for the ranking engine
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.ranking_engine import (
    rank_stocks,
    calculate_composite_rank_score,
    signal_to_score,
    news_sentiment_to_score,
    consensus_to_score,
    normalize_value
)

def test_normalization():
    """Test value normalization"""
    print("Testing normalization...")
    
    # Test basic normalization
    assert normalize_value(5, 0, 10) == 0.5, "Mid-point normalization failed"
    assert normalize_value(0, 0, 10) == 0.0, "Min normalization failed"
    assert normalize_value(10, 0, 10) == 1.0, "Max normalization failed"
    
    # Test edge cases
    assert normalize_value(5, 5, 5) == 0.5, "Equal min-max failed"
    
    print("✅ Normalization tests passed")

def test_signal_conversion():
    """Test signal to score conversion"""
    print("Testing signal conversion...")
    
    assert signal_to_score("🚀 Strong Buy") == 1.0
    assert signal_to_score("👀 Watch") == 0.6
    assert signal_to_score("❄️ Neutral") == 0.3
    assert signal_to_score("❄️ N/A") == 0.0
    assert signal_to_score("Unknown") == 0.0
    
    print("✅ Signal conversion tests passed")

def test_sentiment_conversion():
    """Test news sentiment conversion"""
    print("Testing news sentiment conversion...")
    
    assert news_sentiment_to_score("Positive") == 1.0
    assert news_sentiment_to_score("Neutral") == 0.5
    assert news_sentiment_to_score("Negative") == 0.0
    assert news_sentiment_to_score(None) == 0.5
    
    print("✅ News sentiment conversion tests passed")

def test_consensus_conversion():
    """Test consensus conversion"""
    print("Testing consensus conversion...")
    
    assert consensus_to_score("Strong Buy") == 1.0
    assert consensus_to_score("Buy") == 0.8
    assert consensus_to_score("Hold") == 0.5
    assert consensus_to_score("Sell") == 0.2
    assert consensus_to_score("No Consensus") == 0.5
    assert consensus_to_score(None) == 0.5
    
    print("✅ Consensus conversion tests passed")

def test_ranking():
    """Test complete ranking system"""
    print("Testing complete ranking system...")
    
    # Create sample stock data
    stocks = [
        {
            "ticker": "STOCK1.NS",
            "market_cap": 100000,
            "mom": 0.15,
            "vol": 1.5,
            "sent": 0.8,
            "score": 1200,
            "signal": "🚀 Strong Buy",
            "news_sentiment": "Positive",
            "consensus": "Strong Buy",
            "rating_numeric": 4.5,
            "has_data": True
        },
        {
            "ticker": "STOCK2.NS",
            "market_cap": 50000,
            "mom": 0.05,
            "vol": 1.1,
            "sent": 0.2,
            "score": 600,
            "signal": "👀 Watch",
            "news_sentiment": "Neutral",
            "consensus": "Hold",
            "rating_numeric": 3.0,
            "has_data": True
        },
        {
            "ticker": "STOCK3.NS",
            "market_cap": 25000,
            "mom": -0.05,
            "vol": 0.8,
            "sent": -0.3,
            "score": 200,
            "signal": "❄️ Neutral",
            "news_sentiment": "Negative",
            "consensus": "Sell",
            "rating_numeric": 2.0,
            "has_data": True
        },
        {
            "ticker": "STOCK4.NS",
            "market_cap": None,
            "mom": 0.0,
            "vol": 0.0,
            "sent": 0.0,
            "score": 0,
            "signal": "❄️ N/A",
            "news_sentiment": None,
            "consensus": None,
            "rating_numeric": None,
            "has_data": False
        }
    ]
    
    # Rank stocks
    ranked = rank_stocks(stocks)
    
    # Verify ranking order
    assert ranked[0]["ticker"] == "STOCK1.NS", "Best stock should be ranked #1"
    assert ranked[0]["rank"] == 1, "Rank should be 1"
    assert ranked[-1]["ticker"] == "STOCK4.NS", "Worst stock should be last"
    assert ranked[-1]["rank"] == 4, "Last rank should be 4"
    
    # Verify all stocks have rank_score
    for stock in ranked:
        assert "rank_score" in stock, f"{stock['ticker']} missing rank_score"
        assert "rank" in stock, f"{stock['ticker']} missing rank"
    
    # Verify descending order of rank_scores
    for i in range(len(ranked) - 1):
        assert ranked[i]["rank_score"] >= ranked[i+1]["rank_score"], \
            f"Rank scores not in descending order at position {i}"
    
    print(f"✅ Ranking tests passed")
    print(f"   Stock rankings:")
    for stock in ranked:
        print(f"   #{stock['rank']}: {stock['ticker']} - Score: {stock['rank_score']}")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 RANKING ENGINE UNIT TESTS")
    print("="*60 + "\n")
    
    test_normalization()
    test_signal_conversion()
    test_sentiment_conversion()
    test_consensus_conversion()
    test_ranking()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_all_tests()
