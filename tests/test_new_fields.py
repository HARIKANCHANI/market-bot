"""Test the updated analyst ratings with new fields"""
import sys
sys.path.insert(0, '.')

from src.core.analyst_ratings import aggregate_all_analyst_ratings

# Test with RELIANCE and current price
ticker = "RELIANCE"
current_price = 1356.30  # Example current price

print("=" * 80)
print(f"TESTING: {ticker} (Current Price: ₹{current_price})")
print("=" * 80)

result = aggregate_all_analyst_ratings(ticker, current_price=current_price)

print(f"\n📊 ANALYST RATINGS RESULT:")
print(f"{'='*80}")
print(f"  Has Data: {result['has_data']}")
print(f"  Consensus: {result['consensus']}")
print(f"  Rating: {result['rating']}")
print(f"  Analyst Count: {result['analyst_count']}")
print(f"\n💰 TARGET PRICES:")
print(f"  Mean Target: ₹{result.get('target_mean', 'N/A')}")
print(f"  High Target: ₹{result.get('target_high', 'N/A')}")
print(f"  Low Target: ₹{result.get('target_low', 'N/A')}")
print(f"\n📈 UPSIDE/DOWNSIDE:")
if result.get('price_to_target_pct') is not None:
    upside = result['price_to_target_pct']
    direction = "🟢 UPSIDE" if upside > 0 else "🔴 DOWNSIDE"
    print(f"  {direction}: {upside:+.2f}%")
    print(f"  Current: ₹{current_price:.2f} → Target: ₹{result.get('target_mean', 0):.2f}")
else:
    print(f"  N/A")

print(f"\n📊 RECENT ANALYST ACTIONS:")
print(f"  Upgrades: {result.get('upgrades_count', 0)}")
print(f"  Downgrades: {result.get('downgrades_count', 0)}")

print(f"\n🏢 TOP ANALYST FIRMS:")
firms = result.get('analyst_firms', [])
if firms:
    for firm in firms:
        print(f"  • {firm}")
else:
    print(f"  No firm data available")

print(f"\n{'='*80}")
print("TEST COMPLETE")
print(f"{'='*80}")
