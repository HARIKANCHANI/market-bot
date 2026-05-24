#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRODUCTION-GRADE BOT TEMPLATE - NEVER CRASHES
Demonstrates best practices for using the ticker system
"""

import sys
import io

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from data.nse_stocks_650 import (
    get_all_stocks_with_classification,
    fetch_stock_history_safe,
    fetch_stock_info_safe,
    get_stock_for_notion
)

def send_to_notion(data):
    """Dummy function - replace with actual Notion API call"""
    print(f"   💾 Sending to Notion: {data['ticker']}")
    # Your Notion API code here
    return True

def process_stock_safe(ticker, cap_size):
    """
    Process a single stock with production-grade error handling
    
    Returns:
        str: "success", "skipped", or "failed"
    """
    print(f"\n📊 Processing {ticker} ({cap_size})...")
    
    # STEP 1: Fetch historical data (SAFE - never crashes)
    hist, ticker_name, success, error_msg = fetch_stock_history_safe(ticker, period="1y")
    
    if not success:
        # Primary and fallback both failed - skip gracefully
        print(f"   ⚠️  Skipping {ticker_name}: {error_msg}")
        return "skipped"
    
    print(f"   ✅ Got {len(hist)} days of historical data")
    
    # STEP 2: Fetch company info (SAFE - never crashes)
    info, ticker_name, success_info, error_msg_info = fetch_stock_info_safe(ticker)
    
    if not success_info:
        # Info failed but we have historical data - can proceed with limited data
        print(f"   ⚠️  No company info: {error_msg_info}")
        info = {}  # Use empty dict as fallback
    else:
        print(f"   ✅ Got company info")
    
    # STEP 3: Process data (with error handling)
    try:
        # Calculate metrics from historical data
        current_price = hist['Close'].iloc[-1]
        price_change_pct = ((hist['Close'].iloc[-1] / hist['Close'].iloc[0]) - 1) * 100
        avg_volume = hist['Volume'].mean()
        
        # Get company info with defaults
        company_name = info.get('longName', ticker_name)
        sector = info.get('sector', 'Unknown')
        market_cap = info.get('marketCap', 0)
        
        print(f"   📈 Price: ₹{current_price:.2f} ({price_change_pct:+.2f}%)")
        print(f"   🏢 Company: {company_name[:40]}")
        
    except Exception as e:
        print(f"   ❌ Error processing data: {e}")
        return "failed"
    
    # STEP 4: Send to Notion (ALWAYS use current ticker)
    try:
        # Get current ticker for Notion (prevents duplicates)
        notion_ticker = get_stock_for_notion(ticker_name)
        
        data = {
            "ticker": notion_ticker,  # ✅ Always current symbol
            "company_name": company_name,
            "market_cap": cap_size,
            "sector": sector,
            "price": current_price,
            "price_change_1y_pct": price_change_pct,
            "avg_volume": avg_volume,
            # Add more fields as needed
        }
        
        send_to_notion(data)
        print(f"   ✅ Sent to Notion as '{notion_ticker}'")
        return "success"
        
    except Exception as e:
        print(f"   ❌ Error sending to Notion: {e}")
        return "failed"

def main():
    """Main bot execution - NEVER CRASHES"""
    print("=" * 80)
    print("🤖 PRODUCTION-GRADE STOCK BOT - NEVER CRASHES")
    print("=" * 80)
    print()
    
    # Get all stocks (current tickers only, no duplicates)
    print("📋 Loading stock list...")
    stocks = get_all_stocks_with_classification()
    print(f"✅ Loaded {len(stocks)} stocks")
    print()
    
    # Statistics tracking
    stats = {
        "total": len(stocks),
        "success": 0,
        "skipped": 0,
        "failed": 0
    }
    
    # Process each stock (NEVER CRASHES)
    for i, (ticker, cap_size) in enumerate(stocks[:10], 1):  # Process first 10 for demo
        print(f"[{i}/{len(stocks[:10])}] ", end="")
        
        # Process with comprehensive error handling
        try:
            result = process_stock_safe(ticker, cap_size)
            stats[result] += 1
        
        except Exception as e:
            # Catch-all for any unexpected errors
            print(f"   ❌ Unexpected error: {e}")
            stats["failed"] += 1
            continue  # ✅ Move to next stock, don't crash
    
    # Final statistics
    print()
    print("=" * 80)
    print("📊 FINAL STATISTICS")
    print("=" * 80)
    print(f"Total stocks: {stats['total']}")
    print(f"✅ Success: {stats['success']}")
    print(f"⚠️  Skipped: {stats['skipped']}")
    print(f"❌ Failed: {stats['failed']}")
    print()
    
    success_rate = (stats['success'] / (stats['success'] + stats['skipped'] + stats['failed'])) * 100
    print(f"Success Rate: {success_rate:.1f}%")
    print()
    print("✅ Bot completed successfully - NO CRASHES!")
    print("=" * 80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        import traceback
        traceback.print_exc()
