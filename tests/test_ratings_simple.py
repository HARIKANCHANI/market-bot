import yfinance as yf

# Test RELIANCE
print("Testing RELIANCE.NS")
print("="*60)

stock = yf.Ticker("RELIANCE.NS")

# Test recommendations
print("\n1. Recommendations:")
try:
    recs = stock.recommendations
    if recs is not None and not recs.empty:
        print(f"   Found {len(recs)} recommendations")
        print(recs.tail(10))
    else:
        print(f"   No recommendations. Type: {type(recs)}, Is None: {recs is None}")
except Exception as e:
    print(f"   Error: {e}")

# Test info
print("\n2. Stock Info:")
try:
    info = stock.info
    print(f"   recommendationKey: {info.get('recommendationKey', 'N/A')}")
    print(f"   recommendationMean: {info.get('recommendationMean', 'N/A')}")
    print(f"   numberOfAnalystOpinions: {info.get('numberOfAnalystOpinions', 'N/A')}")
    print(f"   targetMeanPrice: {info.get('targetMeanPrice', 'N/A')}")
    print(f"   targetHighPrice: {info.get('targetHighPrice', 'N/A')}")
    print(f"   targetLowPrice: {info.get('targetLowPrice', 'N/A')}")
except Exception as e:
    print(f"   Error: {e}")

# Test upgrades/downgrades
print("\n3. Upgrades/Downgrades:")
try:
    upgrades = stock.upgrades_downgrades
    if upgrades is not None and not upgrades.empty:
        print(f"   Found {len(upgrades)} upgrade/downgrade events")
        print(upgrades.tail(10))
    else:
        print(f"   No data. Type: {type(upgrades)}, Is None: {upgrades is None}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "="*60)
print("Test complete")
