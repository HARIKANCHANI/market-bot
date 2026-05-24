#!/usr/bin/env python3
"""
Quick status check for Notion database
"""

import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

if not NOTION_TOKEN or not DATABASE_ID:
    print("❌ ERROR: NOTION_TOKEN or DATABASE_ID not found in environment variables")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

print("=" * 70)
print("📊 NOTION DATABASE STATUS CHECK")
print("=" * 70)
print()

# Check database properties
db_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
db_response = requests.get(db_url, headers=headers)
db_data = db_response.json()
props = db_data.get("properties", {})

print("✅ Database Properties:")
for prop_name in props.keys():
    prop_type = props[prop_name].get("type", "unknown")
    print(f"   • {prop_name} ({prop_type})")

print()

# Count stocks with Price and Score
query_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
response = requests.post(query_url, headers=headers, json={"page_size": 100})
data = response.json()
results = data.get("results", [])

stocks_with_price = 0
stocks_with_score = 0
total_stocks = len(results)

for page in results[:10]:  # Check first 10
    props = page["properties"]
    
    price_prop = props.get("Price (₹)", {})
    if price_prop.get("number") is not None:
        stocks_with_price += 1
    
    score_prop = props.get("Score", {})
    if score_prop.get("number") is not None:
        stocks_with_score += 1

print(f"📈 Sample Check (first {min(10, total_stocks)} stocks):")
print(f"   • Stocks with Price: {stocks_with_price}/{min(10, total_stocks)}")
print(f"   • Stocks with Score: {stocks_with_score}/{min(10, total_stocks)}")
print()

# Show sample stock
if results:
    sample = results[0]["properties"]
    ticker = sample.get("Ticker", {}).get("title", [{}])[0].get("plain_text", "N/A") if sample.get("Ticker", {}).get("title") else "N/A"
    price = sample.get("Price (₹)", {}).get("number")
    score = sample.get("Score", {}).get("number")
    signal = sample.get("Signal", {}).get("select", {}).get("name", "N/A") if sample.get("Signal", {}).get("select") else "N/A"
    
    print("📋 Sample Stock:")
    print(f"   Ticker: {ticker}")
    print(f"   Price: ₹{price if price else 'Not set'}")
    print(f"   Score: {score if score else 'Not set'}")
    print(f"   Signal: {signal}")

print()
print("=" * 70)
