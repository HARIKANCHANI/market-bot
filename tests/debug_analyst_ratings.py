"""
Debug script to test analyst ratings fetching from all sources
"""

import yfinance as yf
import requests
from statistics import mean

# Test tickers
TEST_TICKERS = [
    "RELIANCE",
    "TCS", 
    "INFY",
    "HDFCBANK",
    "ICICIBANK",
]

print("="*80)
print("ANALYST RATINGS DEBUG - Testing All Data Sources")
print("="*80)

for ticker in TEST_TICKERS:
    print(f"\n{'='*80}")
    print(f"Testing: {ticker}")
    print(f"{'='*80}")
    
    # ========================================
    # 1. YAHOO FINANCE
    # ========================================
    print(f"\n📊 1. YAHOO FINANCE ({ticker}.NS)")
    print("-" * 80)
    try:
        stock = yf.Ticker(f"{ticker}.NS")
        
        # Test recommendations
        print("   Fetching recommendations...")
        recommendations = stock.recommendations
        
        if recommendations is not None and not recommendations.empty:
            print(f"   ✅ SUCCESS: Found {len(recommendations)} recommendations")
            print(f"   Latest 5 recommendations:")
            recent = recommendations.tail(5)
            for idx, row in recent.iterrows():
                firm = row.get('Firm', 'Unknown')
                to_grade = row.get('To Grade', 'N/A')
                action = row.get('Action', 'N/A')
                print(f"      - {firm}: {to_grade} / {action} (Date: {idx})")
        else:
            print("   ❌ FAILED: No recommendations data available")
            print(f"   Recommendations type: {type(recommendations)}")
            print(f"   Is None: {recommendations is None}")
            if recommendations is not None:
                print(f"   Is Empty: {recommendations.empty}")
        
        # Test other fields
        print("\n   Additional Yahoo Finance fields:")
        try:
            info = stock.info
            print(f"      - recommendationKey: {info.get('recommendationKey', 'N/A')}")
            print(f"      - recommendationMean: {info.get('recommendationMean', 'N/A')}")
            print(f"      - numberOfAnalystOpinions: {info.get('numberOfAnalystOpinions', 'N/A')}")
            print(f"      - targetMeanPrice: {info.get('targetMeanPrice', 'N/A')}")
        except Exception as e:
            print(f"      ❌ Error getting info: {e}")
            
    except Exception as e:
        print(f"   ❌ EXCEPTION: {str(e)}")
    
    # ========================================
    # 2. MONEYCONTROL
    # ========================================
    print(f"\n📊 2. MONEYCONTROL")
    print("-" * 80)
    try:
        # MoneyControl URL format (need to map ticker to MC URL)
        # Example: https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id=RI
        print("   Testing MoneyControl access...")
        
        # Try to access MoneyControl homepage first
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get('https://www.moneycontrol.com/', headers=headers, timeout=5)
        print(f"   Homepage status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ MoneyControl is accessible")
            print("   ⚠️  Note: Need proper ticker-to-URL mapping to fetch ratings")
        else:
            print(f"   ❌ FAILED: Status {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ EXCEPTION: {str(e)}")
    
    # ========================================
    # 3. TICKERTAPE
    # ========================================
    print(f"\n📊 3. TICKERTAPE (Smallcase)")
    print("-" * 80)
    try:
        # TickerTape API format
        url = f"https://api.tickertape.in/stocks?sids={ticker}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"   Testing: {url}")
        response = requests.get(url, headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS: Got JSON response")
            print(f"   Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            print(f"   Response preview: {str(data)[:200]}...")
        else:
            print(f"   ❌ FAILED: Status {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ EXCEPTION: {str(e)}")
    
    # ========================================
    # 4. SCREENER.IN
    # ========================================
    print(f"\n📊 4. SCREENER.IN")
    print("-" * 80)
    try:
        url = f"https://www.screener.in/company/{ticker}/consolidated/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"   Testing: {url}")
        response = requests.get(url, headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ SUCCESS: Page accessible")
            print(f"   Content length: {len(response.text)} bytes")
            # Check if there's analyst data
            if "analyst" in response.text.lower():
                print(f"   ✅ Found 'analyst' in page content")
            else:
                print(f"   ⚠️  'analyst' not found in page")
        else:
            print(f"   ❌ FAILED: Status {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ EXCEPTION: {str(e)}")

print("\n" + "="*80)
print("DEBUG COMPLETE")
print("="*80)
