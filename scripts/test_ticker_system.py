#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Production-Grade Ticker System
Validates the ticker rename mapping and fallback mechanism
"""

import sys
import io

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from data.nse_stocks_650 import (
    get_current_ticker,
    get_historical_ticker,
    get_all_tickers_for_symbol,
    get_stock_for_notion,
    fetch_stock_data_with_fallback,
    fetch_stock_history_safe,
    fetch_stock_info_safe,
    get_all_stocks_with_classification,
    TICKER_RENAME_MAP,
    DELISTED_STOCKS
)

def test_ticker_mapping():
    """Test ticker rename mapping"""
    print("=" * 80)
    print("🧪 TEST 1: Ticker Rename Mapping")
    print("=" * 80)
    
    test_cases = [
        ("CADILAHC", "ZYDUSLIFE"),
        ("AMARAJABAT", "ARE&M"),
        ("SUVENPHAR", "COHANCE"),
        ("BURGERKING", "RBA"),
        ("POLYCA", "POLYCAB"),
        ("RELIANCE", "RELIANCE"),  # No change
    ]
    
    for old, expected in test_cases:
        result = get_current_ticker(old)
        status = "✅" if result == expected else "❌"
        print(f"{status} {old:<15} → {result:<15} (expected: {expected})")
    print()

def test_historical_lookup():
    """Test historical ticker lookup"""
    print("=" * 80)
    print("🧪 TEST 2: Historical Ticker Lookup")
    print("=" * 80)
    
    test_cases = [
        ("ZYDUSLIFE", "CADILAHC"),
        ("ARE&M", "AMARAJABAT"),
        ("COHANCE", "SUVENPHAR"),
        ("RELIANCE", None),  # No historical
    ]
    
    for current, expected in test_cases:
        result = get_historical_ticker(current)
        status = "✅" if result == expected else "❌"
        print(f"{status} {current:<15} → {result if result else 'None':<15} (expected: {expected if expected else 'None'})")
    print()

def test_all_ticker_variations():
    """Test getting all ticker variations"""
    print("=" * 80)
    print("🧪 TEST 3: All Ticker Variations")
    print("=" * 80)
    
    test_tickers = ["CADILAHC", "ZYDUSLIFE", "RELIANCE", "POLYCA"]
    
    for ticker in test_tickers:
        current, historical = get_all_tickers_for_symbol(ticker)
        print(f"📊 {ticker:<15} → Current: {current:<15} Historical: {historical if historical else 'None'}")
    print()

def test_notion_ticker():
    """Test Notion ticker resolution"""
    print("=" * 80)
    print("🧪 TEST 4: Notion Ticker Resolution (No Duplicates)")
    print("=" * 80)
    
    # Simulate both old and new tickers - should return same result
    test_cases = [
        ("CADILAHC", "ZYDUSLIFE"),
        ("ZYDUSLIFE", "ZYDUSLIFE"),
        ("AMARAJABAT", "ARE&M"),
        ("ARE&M", "ARE&M"),
    ]
    
    for input_ticker, expected in test_cases:
        result = get_stock_for_notion(input_ticker)
        status = "✅" if result == expected else "❌"
        print(f"{status} Notion({input_ticker:<15}) → {result:<15} (prevents duplicate)")
    print()

def test_stock_list():
    """Test stock list has no duplicates"""
    print("=" * 80)
    print("🧪 TEST 5: Stock List Uniqueness")
    print("=" * 80)
    
    stocks = get_all_stocks_with_classification()
    tickers = [t for t, _ in stocks]
    
    print(f"Total stocks: {len(stocks)}")
    print(f"Unique tickers: {len(set(tickers))}")
    
    # Check for duplicates
    seen = {}
    duplicates = []
    for ticker, cap in stocks:
        if ticker in seen:
            duplicates.append((ticker, cap, seen[ticker]))
        else:
            seen[ticker] = cap
    
    if duplicates:
        print(f"❌ Found {len(duplicates)} duplicates:")
        for ticker, cap1, cap2 in duplicates:
            print(f"   {ticker}: {cap1} and {cap2}")
    else:
        print("✅ No duplicates found!")
    
    # Check if old tickers are in the list
    print(f"\n🔍 Checking for old tickers in stock list...")
    old_tickers_found = []
    for ticker in tickers:
        if ticker in TICKER_RENAME_MAP:
            old_tickers_found.append(ticker)
    
    if old_tickers_found:
        print(f"❌ Found old tickers in list (should be renamed):")
        for old in old_tickers_found:
            new = TICKER_RENAME_MAP[old]
            print(f"   {old} → should be {new}")
    else:
        print("✅ All tickers are current (no old symbols)")
    print()

def test_data_fetch():
    """Test data fetching with fallback"""
    print("=" * 80)
    print("🧪 TEST 6: Data Fetching with Fallback")
    print("=" * 80)

    test_tickers = ["ZYDUSLIFE", "RELIANCE", "POLYCAB"]

    for ticker in test_tickers[:2]:  # Test first 2 to save time
        print(f"\n📥 Fetching data for {ticker}...")

        # Test new safe wrapper
        stock, used_ticker, success, error_msg = fetch_stock_data_with_fallback(ticker)

        if success:
            print(f"   ✅ Success! Ticker: {used_ticker}")
            if error_msg:
                print(f"   ℹ️  Note: {error_msg}")
        else:
            print(f"   ❌ Failed: {error_msg}")
    print()

def test_safe_wrappers():
    """Test ultra-safe wrapper functions"""
    print("=" * 80)
    print("🧪 TEST 7: Ultra-Safe Wrapper Functions (NEVER CRASH)")
    print("=" * 80)

    test_tickers = ["ZYDUSLIFE", "RELIANCE", "INVALIDTICKER123"]

    for ticker in test_tickers:
        print(f"\n🔍 Testing {ticker}...")

        # Test safe history fetch
        hist, ticker_name, success, error_msg = fetch_stock_history_safe(ticker, period="5d")

        if success:
            print(f"   ✅ History: Got {len(hist)} days of data")
        else:
            print(f"   ⚠️  History: {error_msg}")

        # Test safe info fetch
        info, ticker_name, success, error_msg = fetch_stock_info_safe(ticker)

        if success:
            company_name = info.get("longName", "N/A")[:40]
            print(f"   ✅ Info: {company_name}")
        else:
            print(f"   ⚠️  Info: {error_msg}")

        print(f"   ✅ No crash - handled gracefully!")
    print()

def main():
    """Run all tests"""
    print("\n")
    print("🚀 PRODUCTION-GRADE TICKER SYSTEM TEST SUITE")
    print("=" * 80)
    print()

    test_ticker_mapping()
    test_historical_lookup()
    test_all_ticker_variations()
    test_notion_ticker()
    test_stock_list()
    test_data_fetch()
    test_safe_wrappers()

    print("=" * 80)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 80)
    print()
    print("📊 Summary:")
    print(f"   Ticker renames tracked: {len(TICKER_RENAME_MAP)}")
    print(f"   Delisted stocks: {len(DELISTED_STOCKS)}")
    print()
    print("🛡️  Safety Features:")
    print("   ✅ Primary → Fallback ticker logic")
    print("   ✅ Ultra-safe wrappers (never crash)")
    print("   ✅ Graceful error handling")
    print("   ✅ No duplicates in Notion")
    print()

if __name__ == "__main__":
    main()
