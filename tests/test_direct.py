#!/usr/bin/env python
import sys
sys.path.insert(0, 'c:\\Users\\HARI KANCHANI\\source\\repos\\market-bot')

from src.core.analyst_ratings import aggregate_all_analyst_ratings

print("Testing analyst ratings for RELIANCE", flush=True)
result = aggregate_all_analyst_ratings("RELIANCE")

print("\nResult:", flush=True)
for key, value in result.items():
    print(f"  {key}: {value}", flush=True)
