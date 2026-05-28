"""
Test analyst ratings fetching with detailed output
"""
import sys
sys.path.insert(0, '.')

from src.core.analyst_ratings import aggregate_all_analyst_ratings

# Test stocks
test_tickers = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]

print("="*80)
print("TESTING ANALYST RATINGS MODULE")
print("="*80)

for ticker in test_tickers:
    print(f"\n{'='*80}")
    print(f"Testing: {ticker}")
    print(f"{'='*80}")
    
    result = aggregate_all_analyst_ratings(ticker)
    
    print(f"\n✅ RESULT:")
    print(f"   Has Data: {result['has_data']}")
    print(f"   Consensus: {result['consensus']}")
    print(f"   Rating: {result.get('rating', 'N/A')}")
    print(f"   Analyst Count: {result['analyst_count']}")
    print(f"   Sources Count: {result['sources_count']}")
    
    if result['breakdown']:
        print(f"\n   Breakdown:")
        for source in result['breakdown']:
            print(f"      - {source['source']}: {source.get('avg_rating', 'N/A')}/5.0 ({source.get('count', 0)} analysts)")

print(f"\n{'='*80}")
print("TEST COMPLETE")
print(f"{'='*80}")
