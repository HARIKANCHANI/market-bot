#!/usr/bin/env python3
"""
Curated top 25 stock recommendations based on comprehensive analysis
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

# Configuration
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

if not NOTION_TOKEN or not DATABASE_ID:
    print("❌ ERROR: NOTION_TOKEN or DATABASE_ID not found in environment variables")
    print("   Please set them in your .env file")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

print("=" * 70)
print("🎯 TOP 25 STOCKS TO BUY - CURATED RECOMMENDATIONS")
print("=" * 70)
print()

# Fetch all stocks
all_stocks = []
has_more = True
start_cursor = None

while has_more:
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {"page_size": 100}
    if start_cursor:
        payload["start_cursor"] = start_cursor
    
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    all_stocks.extend(data.get("results", []))
    has_more = data.get("has_more", False)
    start_cursor = data.get("next_cursor")

# Parse stocks
stocks = []
for page in all_stocks:
    props = page["properties"]
    
    ticker_prop = props.get("Ticker", {})
    ticker = ticker_prop.get("title", [{}])[0].get("plain_text", "") if ticker_prop.get("title") else ""
    
    signal_prop = props.get("Signal", {})
    signal = signal_prop.get("select", {}).get("name", "❄️ Neutral") if signal_prop.get("select") else "❄️ Neutral"
    
    momentum_prop = props.get("Momentum (%)", {})
    momentum = momentum_prop.get("number", 0) if momentum_prop.get("number") is not None else 0
    
    volume_prop = props.get("Volume Surge", {})
    volume = volume_prop.get("number", 0) if volume_prop.get("number") is not None else 0
    
    cap_prop = props.get("Market Cap", {})
    cap = cap_prop.get("select", {}).get("name", "") if cap_prop.get("select") else ""
    
    if ticker and ticker != "TEST":
        stocks.append({
            "ticker": ticker,
            "signal": signal,
            "momentum": momentum * 100,  # Convert to percentage
            "volume": volume,
            "cap": cap
        })

# Calculate scores
for stock in stocks:
    score = 0
    
    # Priority: Strong Buy signal
    if stock["signal"] == "🚀 Strong Buy":
        score += 1000
    elif stock["signal"] == "👀 Watch":
        score += 500
    
    # Momentum (very important)
    score += stock["momentum"] * 5
    
    # Volume surge (important)
    score += stock["volume"] * 50
    
    stock["score"] = score

# Sort and get top stocks
stocks.sort(key=lambda x: x["score"], reverse=True)

# Deduplicate first (remove duplicates)
seen = set()
unique_stocks = []
for stock in stocks:
    if stock["ticker"] not in seen:
        seen.add(stock["ticker"])
        unique_stocks.append(stock)

# Get top 25
unique_top_25 = unique_stocks[:25]

# Display
print(f"📊 Analyzed {len(stocks)} stocks from NSE (Nifty 100 + Midcap 150 + Smallcap 250)")
print()
print("=" * 70)
print()

for i, s in enumerate(unique_top_25, 1):
    emoji = "🔥" if s["signal"] == "🚀 Strong Buy" else "👁️"
    print(f"{i:2d}. {emoji} {s['ticker']:12s} │ {s['signal']:15s} │ "
          f"Momentum: {s['momentum']:7.1f}% │ Volume: {s['volume']:.2f}x │ {s['cap']}")

print()
print("=" * 70)
print("📈 INVESTMENT SUMMARY")
print("=" * 70)

strong_buy = sum(1 for s in unique_top_25 if s["signal"] == "🚀 Strong Buy")
watch = sum(1 for s in unique_top_25 if s["signal"] == "👀 Watch")
large = sum(1 for s in unique_top_25 if s["cap"] == "Large Cap")
mid = sum(1 for s in unique_top_25 if s["cap"] == "Mid Cap")
small = sum(1 for s in unique_top_25 if s["cap"] == "Small Cap")

print("\n🎯 SIGNALS:")
print(f"   • Strong Buy: {strong_buy} stocks")
print(f"   • Watch:      {watch} stocks")

print("\n🏢 MARKET CAP DISTRIBUTION:")
print(f"   • Large Cap:  {large} stocks (Stable, lower risk)")
print(f"   • Mid Cap:    {mid} stocks (Growth potential)")
print(f"   • Small Cap:  {small} stocks (Higher risk/reward)")

print("\n💡 TOP RECOMMENDATIONS (Top 10):")
print("   Focus on these for immediate action:")
for i, s in enumerate(unique_top_25[:10], 1):
    print(f"   {i:2d}. {s['ticker']}")

print()
print("=" * 70)
print("⚠️  IMPORTANT DISCLAIMERS")
print("=" * 70)
print("""
• This is NOT financial advice - do your own research
• Past performance doesn't guarantee future results  
• Consider your risk tolerance and investment goals
• Diversify your portfolio across sectors and market caps
• Set stop-loss orders to limit downside risk
• Monitor your positions regularly
""")
