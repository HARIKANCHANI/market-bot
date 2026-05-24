#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check various ticker name variations to find correct NSE symbols
"""

import sys
import io
import yfinance as yf

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Stocks that were flagged as "delisted" - let's check variations
STOCKS_TO_CHECK = {
    "POLYCA": ["POLYCAB", "POLYCAB.NS", "POLYCA.NS"],
    "BURGERKING": ["BURGERKING.NS", "RBLBANK.NS", "BERGEPAINT.NS"],
    "DHFL": ["DHFL.NS", "DEWAN.NS"],
    "TATAMOTORS": ["TATAMOTORS.NS", "TATAMOTORSLTD.NS", "TATAMTRDVR.NS"],
    "CADILAHC": ["CADILAHC.NS", "ZYDUSLIFE.NS", "CADILA.NS"],
    "AMARAJABAT": ["AMARAJABAT.NS", "AMARA.NS", "AMARAJABATERY.NS"],
    "EQUITAS": ["EQUITAS.NS", "EQUITASBNK.NS"],
    "CENTURYTEX": ["CENTURYTEX.NS", "CENTURY.NS", "CENTEXT.NS"],
    "NLCINDCOM": ["NLCINDCOM.NS", "NLCINDIA.NS"],
    "SEQUENT": ["SEQUENT.NS", "SEQUENTSC.NS"],
    "SUVENPHAR": ["SUVENPHAR.NS", "SUVEN.NS", "SUVENPHRM.NS"],
    "SWANENERGY": ["SWANENERGY.NS", "SWAN.NS"],
    "TCNSBRANDS": ["TCNSBRANDS.NS", "TCNS.NS"],
    "ADANITRANS": ["ADANITRANS.NS", "ADANIPORTS.NS"],
    "AEGISCHEM": ["AEGISCHEM.NS", "AEGIS.NS"],
    "AGCNET": ["AGCNET.NS", "AGC.NS"],
    "CHEMPLAST": ["CHEMPLAST.NS", "CHEMPLASTS.NS"],
    "DHANI": ["DHANI.NS"],
    "ESSELPACK": ["ESSELPACK.NS", "ESSEL.NS"],
    "GANESHHOUC": ["GANESHHOUC.NS", "GANESH.NS"],
    "HBLPOWER": ["HBLPOWER.NS", "HBL.NS"],
    "HIL": ["HIL.NS", "HILINDS.NS"],
}

def check_ticker(ticker):
    """Check if ticker has valid data"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="5d")
        
        if not hist.empty and len(hist) > 0:
            name = info.get('longName') or info.get('shortName') or 'Unknown'
            return True, name, hist['Close'].iloc[-1] if not hist.empty else None
    except:
        pass
    return False, None, None

def main():
    print("=" * 100)
    print("🔍 CHECKING TICKER NAME VARIATIONS")
    print("=" * 100)
    print()
    
    results = {}
    
    for base_ticker, variations in STOCKS_TO_CHECK.items():
        print(f"\n🔎 Checking: {base_ticker}")
        print("-" * 100)
        
        found = False
        for variant in variations:
            is_valid, name, price = check_ticker(variant)
            
            if is_valid:
                print(f"  ✅ {variant:<25} VALID - {name[:50]:<50} Price: ₹{price:.2f}")
                results[base_ticker] = variant.replace('.NS', '')
                found = True
                break
            else:
                print(f"  ❌ {variant:<25} Not found")
        
        if not found:
            print(f"  ⚠️  No valid ticker found for {base_ticker}")
            results[base_ticker] = None
    
    print()
    print("=" * 100)
    print("📊 SUMMARY - CORRECT TICKER NAMES")
    print("=" * 100)
    print()
    
    print("VALID TICKERS (use these):")
    for base, correct in results.items():
        if correct:
            if correct != base:
                print(f"  {base:<20} → {correct}")
            else:
                print(f"  {base:<20} ✅ (already correct)")
    
    print("\nDELISTED/NOT FOUND:")
    for base, correct in results.items():
        if correct is None:
            print(f"  {base:<20} ❌ (truly delisted - remove)")
    
    print()

if __name__ == "__main__":
    main()
