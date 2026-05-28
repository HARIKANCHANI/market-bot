"""Test the aggregate_all_analyst_ratings function"""
import sys
sys.path.insert(0, '.')

from src.core.analyst_ratings import aggregate_all_analyst_ratings

# Write to file
output = open('aggregate_test_results.txt', 'w', encoding='utf-8')

def log(msg):
    print(msg)
    output.write(msg + '\n')
    output.flush()

# Test with 3 stocks
test_tickers = ["RELIANCE", "TCS", "INFY"]

log("=" * 80)
log("TESTING aggregate_all_analyst_ratings()")
log("=" * 80)

for ticker in test_tickers:
    log(f"\n{'='*80}")
    log(f"Testing: {ticker}")
    log(f"{'='*80}")

    result = aggregate_all_analyst_ratings(ticker)

    log(f"\n✅ RESULT:")
    log(f"   has_data: {result['has_data']}")
    log(f"   consensus: {result['consensus']}")
    log(f"   rating: {result.get('rating', 'N/A')}")
    log(f"   rating_numeric: {result.get('rating_numeric', 'N/A')}")
    log(f"   analyst_count: {result['analyst_count']}")
    log(f"   sources_count: {result['sources_count']}")

    if result['breakdown']:
        log(f"\n   Breakdown:")
        for source in result['breakdown']:
            log(f"      - {source['source']}: {source.get('consensus', 'N/A')} ({source.get('avg_rating', 'N/A')}/5.0, {source.get('count', 0)} analysts)")

log(f"\n{'='*80}")
log("TEST COMPLETE")
log(f"{'='*80}")

output.close()
log("Results written to aggregate_test_results.txt")
