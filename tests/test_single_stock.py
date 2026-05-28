#!/usr/bin/env python3
"""
Test script to process a single stock
Usage: python test_single_stock.py MAKEINDIA
"""

import sys
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add project to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the AI bot's data collection function
from src.bots.market_bot_ai import get_market_intelligence, send_to_notion

def test_single_stock(ticker, cap_size="Small Cap"):
    """Test processing a single stock"""
    print(f"\n{'='*70}")
    print(f"Testing Stock: {ticker}")
    print(f"{'='*70}\n")
    
    # Fetch data
    print(f"📊 Fetching market intelligence for {ticker}...")
    data = get_market_intelligence(ticker, cap_size)
    
    if not data:
        print(f"❌ Failed to fetch data for {ticker}")
        return False
    
    print(f"\n✅ Data fetched successfully!")
    print(f"\n📋 Stock Details:")
    print(f"   Ticker: {data.get('ticker')}")
    print(f"   Sector: {data.get('sector')}")
    print(f"   Price: ₹{data.get('price', 0):.2f}")
    print(f"   Momentum: {data.get('mom', 0)*100:.1f}%")
    print(f"   Volume: {data.get('vol', 0):.2f}x")
    print(f"   Sentiment: {data.get('sent', 0):.2f}")
    
    # Calculate trend (same logic as in bot)
    momentum = data.get('mom', 0)
    volume = data.get('vol', 0)
    
    if momentum > 0.02 and volume > 1.0:
        trend = "📈 Upward (volume-confirmed)"
    elif momentum < -0.02 and volume > 1.0:
        trend = "📉 Downward (volume-confirmed)"
    else:
        trend = "➡️ Neutral"
    
    print(f"   Trend: {trend}")
    
    # Send to Notion
    print(f"\n📤 Uploading to Notion...")
    success = send_to_notion(data)
    
    if success:
        print(f"\n🎉 SUCCESS! {ticker} uploaded to Notion successfully!")
        print(f"\n✅ Sector validation working: '{data.get('sector')}' accepted by Notion")
        return True
    else:
        print(f"\n❌ FAILED! {ticker} could not be uploaded to Notion")
        return False

if __name__ == "__main__":
    # Get ticker from command line or use default
    ticker = sys.argv[1] if len(sys.argv) > 1 else "MAKEINDIA"
    cap_size = sys.argv[2] if len(sys.argv) > 2 else "Small Cap"
    
    success = test_single_stock(ticker, cap_size)
    
    if success:
        print(f"\n{'='*70}")
        print(f"✅ TEST PASSED - {ticker} processed successfully!")
        print(f"{'='*70}\n")
        exit(0)
    else:
        print(f"\n{'='*70}")
        print(f"❌ TEST FAILED - {ticker} processing failed")
        print(f"{'='*70}\n")
        exit(1)
