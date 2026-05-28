"""Test Yahoo Finance info fields for analyst data"""
import yfinance as yf
import sys

# Redirect all output to a file
output_file = open('yahoo_test_output.txt', 'w', encoding='utf-8')
sys.stdout = output_file
sys.stderr = output_file

print("=" * 80)
print("TESTING YAHOO FINANCE ANALYST DATA")
print("=" * 80)

test_tickers = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]

for ticker in test_tickers:
    print(f"\n{'=' * 80}")
    print(f"Testing: {ticker}.NS")
    print("=" * 80)
    
    try:
        stock = yf.Ticker(f"{ticker}.NS")
        info = stock.info
        
        # Check analyst fields
        print("\nAnalyst fields from .info:")
        print(f"  recommendationKey: {info.get('recommendationKey', 'N/A')}")
        print(f"  recommendationMean: {info.get('recommendationMean', 'N/A')}")
        print(f"  numberOfAnalystOpinions: {info.get('numberOfAnalystOpinions', 'N/A')}")
        print(f"  targetMeanPrice: {info.get('targetMeanPrice', 'N/A')}")
        print(f"  targetHighPrice: {info.get('targetHighPrice', 'N/A')}")
        print(f"  targetLowPrice: {info.get('targetLowPrice', 'N/A')}")
        print(f"  targetMedianPrice: {info.get('targetMedianPrice', 'N/A')}")
        
        # Check if we have usable data
        rec_mean = info.get('recommendationMean')
        num_analysts = info.get('numberOfAnalystOpinions', 0)
        
        if rec_mean is not None and num_analysts > 0:
            print(f"\n  ✅ HAS ANALYST DATA!")
            print(f"     Rating: {rec_mean}/5.0 from {num_analysts} analysts")
        else:
            print(f"\n  ❌ NO ANALYST DATA")
            
        # Also check recommendations
        print("\nRecommendations from .recommendations:")
        recs = stock.recommendations
        if recs is not None and not recs.empty:
            print(f"  ✅ Found {len(recs)} historical recommendations")
            print("\n  Latest 5:")
            for idx, row in recs.tail(5).iterrows():
                print(f"    {idx.date()}: {row.get('Firm', 'Unknown')} - {row.get('To Grade', 'N/A')}")
        else:
            print(f"  ❌ No historical recommendations")
            
    except Exception as e:
        print(f"\n  ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)

output_file.close()
print("Results written to yahoo_test_output.txt")
