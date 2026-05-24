#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stock List Validation and Correction Script
Identifies delisted/invalid stocks and suggests corrections for ticker names
"""

import sys
import io
import yfinance as yf
from collections import defaultdict

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Import stock lists
from data.nse_stocks_650 import NIFTY_150, MIDCAP_200, SMALLCAP_300

# Known ticker corrections (old_ticker -> new_ticker)
TICKER_CORRECTIONS = {
    "TATAMOTORS": "TATAMOTORSLTD",  # Tata Motors renamed
    "CADILAHC": "ZYDUSLIFE",  # Cadila Healthcare renamed to Zydus Lifesciences
    "AMARAJABAT": "AMARA",  # Amara Raja changed symbol
    "POLYCA": None,  # Delisted
    "NLCINDCOM": "NLCINDIA",  # NLC India proper name
    "SEQUENT": None,  # Delisted
    "SUVENPHAR": None,  # Delisted/merged
    "SWANENERGY": None,  # Delisted
    "TCNSBRANDS": None,  # Delisted
    "ADANITRANS": "ADANIPOWER",  # Merged/renamed
    "AEGISCHEM": None,  # Delisted
    "AGCNET": None,  # Delisted
    "BURGERKING": None,  # Delisted
    "CENTURYTEX": None,  # Delisted
    "CHEMPLAST": None,  # Delisted
    "DHANI": None,  # Delisted
    "DHFL": None,  # Delisted (bankrupt)
    "EQUITAS": "EQUITASBNK",  # Equitas Small Finance Bank
    "ESSELPACK": None,  # Delisted
    "GANESHHOUC": None,  # Delisted
    "GET&D": "GETD",  # Special character fix
    "HBLPOWER": None,  # Delisted
    "HDFCPRIVATE": None,  # Never existed (confusion with HDFCBANK)
    "HIL": None,  # Delisted
    "IDFC": "IDFCFIRSTB",  # Merged into IDFC FIRST Bank
}

def validate_ticker(ticker):
    """Check if ticker has valid data on Yahoo Finance"""
    try:
        stock = yf.Ticker(f"{ticker}.NS")
        df = stock.history(period="1mo")
        if not df.empty and len(df) >= 5:
            return True, "Valid"
    except Exception as e:
        return False, f"Error: {str(e)[:50]}"
    
    return False, "No data/Delisted"

def main():
    print("=" * 80)
    print("📊 NSE STOCK LIST VALIDATION & CORRECTION")
    print("=" * 80)
    print()
    
    all_stocks = []
    all_stocks.extend([(t, "NIFTY_150") for t in NIFTY_150])
    all_stocks.extend([(t, "MIDCAP_200") for t in MIDCAP_200])
    all_stocks.extend([(t, "SMALLCAP_300") for t in SMALLCAP_300])
    
    print(f"🔍 Total stocks to validate: {len(all_stocks)}")
    print()
    
    invalid_stocks = defaultdict(list)
    valid_count = 0
    
    for i, (ticker, list_name) in enumerate(all_stocks, 1):
        if i % 50 == 0:
            print(f"Progress: {i}/{len(all_stocks)}...")
        
        is_valid, reason = validate_ticker(ticker)
        
        if not is_valid:
            correction = TICKER_CORRECTIONS.get(ticker)
            invalid_stocks[list_name].append({
                "ticker": ticker,
                "reason": reason,
                "correction": correction
            })
        else:
            valid_count += 1
    
    print()
    print("=" * 80)
    print("📈 VALIDATION RESULTS")
    print("=" * 80)
    print(f"✅ Valid stocks: {valid_count}/{len(all_stocks)}")
    print(f"❌ Invalid stocks: {len(all_stocks) - valid_count}/{len(all_stocks)}")
    print()
    
    # Display invalid stocks by category
    for list_name, stocks in invalid_stocks.items():
        if stocks:
            print(f"\n🔴 {list_name} - Invalid Stocks ({len(stocks)}):")
            print("-" * 80)
            for stock in stocks:
                correction_str = f" → {stock['correction']}" if stock['correction'] else " → DELETE (Delisted)"
                print(f"  {stock['ticker']:<20} {stock['reason']:<30} {correction_str}")
    
    print()
    print("=" * 80)
    print("📝 RECOMMENDED ACTIONS")
    print("=" * 80)
    
    # Generate removal and correction lists
    to_remove = []
    to_rename = []
    
    for list_name, stocks in invalid_stocks.items():
        for stock in stocks:
            if stock['correction']:
                to_rename.append((stock['ticker'], stock['correction']))
            else:
                to_remove.append(stock['ticker'])
    
    print(f"\n🗑️  Stocks to REMOVE ({len(to_remove)}):")
    for ticker in sorted(to_remove):
        print(f"  - {ticker}")
    
    print(f"\n✏️  Stocks to RENAME ({len(to_rename)}):")
    for old, new in sorted(to_rename):
        print(f"  - {old} → {new}")
    
    print()
    print("=" * 80)
    print("✅ Validation complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
