#!/usr/bin/env python3
"""
Test script for incremental bots
Tests the upsert functionality with a small sample of stocks
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.notion_incremental import (
    query_ticker_in_database,
    upsert_notion_entry
)

print("=" * 70)
print("🧪 TESTING INCREMENTAL BOT UTILITIES")
print("=" * 70)
print()

# Test stocks
test_tickers = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS"
]

print("📊 Testing upsert functionality with 3 sample tickers")
print()

for ticker in test_tickers:
    print(f"\n{'='*70}")
    print(f"Testing: {ticker}")
    print(f"{'='*70}")
    
    # Check if exists
    existing = query_ticker_in_database(ticker)
    
    if existing:
        print(f"✅ Ticker EXISTS in database")
        print(f"   Page ID: {existing['page_id'][:20]}...")
    else:
        print(f"❌ Ticker NOT FOUND in database")
    
    # Create sample properties
    properties = {
        "Ticker": {"title": [{"text": {"content": ticker}}]},
        "Market Cap": {"select": {"name": "Large Cap"}},
        "Sector": {"select": {"name": "Technology"}},
        "Sentiment": {"number": 0.5},
        "Momentum (%)": {"number": 5.0},
        "Volume Surge": {"number": 1.2},
        "Score": {"number": 500},
        "Signal": {"select": {"name": "👀 Watch"}},
        "Last Updated": {"date": {"start": "2026-05-24T10:00:00"}}
    }
    
    # Test upsert
    print(f"\n🔄 Testing upsert...")
    success, action = upsert_notion_entry(ticker, properties)
    
    if success:
        if action == "updated":
            print(f"✅ Successfully UPDATED {ticker}")
        elif action == "created":
            print(f"✅ Successfully CREATED {ticker}")
    else:
        print(f"❌ Failed to upsert {ticker}")

print()
print("=" * 70)
print("✅ TEST COMPLETE")
print("=" * 70)
print()
print("Next steps:")
print("1. Check your Notion database")
print("2. Verify tickers were updated/created")
print("3. Run full incremental bot:")
print("   python src/bots/market_bot_lite_incremental.py")
print()
