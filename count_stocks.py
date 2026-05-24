"""Quick stock counter"""

# Import the data
import sys
sys.path.insert(0, '.')

from data.nse_stocks_650 import (
    NIFTY_150, 
    MIDCAP_200, 
    SMALLCAP_300, 
    DELISTED_STOCKS, 
    PUMP_AND_DUMP_STOCKS,
    get_current_ticker
)

# Count raw stocks
nifty_count = len(NIFTY_150)
midcap_count = len(MIDCAP_200)
smallcap_count = len(SMALLCAP_300)
total_raw = nifty_count + midcap_count + smallcap_count

# Count filters
delisted_count = len(DELISTED_STOCKS)
pump_dump_count = len(PUMP_AND_DUMP_STOCKS)
total_filter = delisted_count + pump_dump_count

# Calculate final
final_count = total_raw - total_filter

print("=" * 80)
print("STOCK COUNT ANALYSIS - MARKET BOT")
print("=" * 80)
print()
print("📊 RAW STOCK COUNTS (from lists):")
print(f"  Nifty 150 (Large Cap):  {nifty_count:>4} stocks")
print(f"  Midcap 200:             {midcap_count:>4} stocks") 
print(f"  Smallcap 300:           {smallcap_count:>4} stocks")
print(f"  {'-' * 50}")
print(f"  Total (raw):            {total_raw:>4} stocks")
print()
print("❌ STOCKS TO FILTER OUT:")
print(f"  Delisted stocks:        {delisted_count:>4} stocks")
print(f"  Pump & Dump stocks:     {pump_dump_count:>4} stocks")
print(f"  {'-' * 50}")
print(f"  Total to filter:        {total_filter:>4} stocks")
print()
print("✅ FINAL USABLE STOCKS:")
print(f"  Total after filtering:  {final_count:>4} stocks")
print()
print("📋 DELISTED STOCKS:")
for stock in sorted(DELISTED_STOCKS):
    print(f"  - {stock}")
print()
print("🚨 PUMP & DUMP STOCKS:")
for stock in sorted(PUMP_AND_DUMP_STOCKS):
    print(f"  - {stock}")
print()
print("=" * 80)
