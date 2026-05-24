#!/usr/bin/env python3
"""Update all existing stocks in Notion with latest price and recalculated score.

This maintenance script:

1. Fetches all stock pages from the configured Notion database.
2. Pulls the latest price from Yahoo Finance (yfinance) for each ticker.
3. Recomputes the composite "Score" using the same simple formula used in
   the LITE bot (signal + momentum + volume surge).
4. Writes the updated price, score, and "Last Updated" timestamp back to Notion.
"""

from __future__ import annotations

import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
import yfinance as yf
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

if not NOTION_TOKEN or not DATABASE_ID:
    print("❌ ERROR: NOTION_TOKEN or DATABASE_ID not found in environment variables")
    print("   Please set them in your .env file")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


print("=" * 70)
print("🔄 UPDATING ALL STOCKS WITH PRICE & SCORE")
print("=" * 70)
print()


# ---------------------------------------------------------------------------
# Step 1: Fetch all stocks from Notion
# ---------------------------------------------------------------------------

print("Step 1: Fetching all stocks from Notion database...")
all_stocks: list[dict] = []
has_more = True
start_cursor: str | None = None

while has_more:
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload: dict = {"page_size": 100}
    if start_cursor:
        payload["start_cursor"] = start_cursor

    response = requests.post(url, headers=HEADERS, json=payload)
    data = response.json()
    all_stocks.extend(data.get("results", []))
    has_more = data.get("has_more", False)
    start_cursor = data.get("next_cursor")

print(f"✅ Found {len(all_stocks)} stocks to update")
print()


# ---------------------------------------------------------------------------
# Step 2: Update each stock with latest price & score
# ---------------------------------------------------------------------------

print("Step 2: Fetching latest prices and updating scores...")
print()

success_count = 0
error_count = 0
skip_count = 0

for idx, page in enumerate(all_stocks, start=1):
    page_id = page["id"]
    props = page["properties"]

    # Get ticker
    ticker_prop = props.get("Ticker", {})
    title = ticker_prop.get("title") or []
    ticker = title[0].get("plain_text", "") if title else ""

    if not ticker or ticker == "TEST":
        skip_count += 1
        continue

    # Existing attributes used in score calculation
    signal_prop = props.get("Signal", {})
    signal = (
        signal_prop.get("select", {}).get("name", "❄️ Neutral")
        if signal_prop.get("select")
        else "❄️ Neutral"
    )

    momentum_prop = props.get("Momentum (%)", {})
    momentum = (
        momentum_prop.get("number", 0)
        if momentum_prop.get("number") is not None
        else 0
    )

    volume_prop = props.get("Volume Surge", {})
    volume = (
        volume_prop.get("number", 0)
        if volume_prop.get("number") is not None
        else 0
    )

    print(f"[{idx}/{len(all_stocks)}] 🔄 {ticker}...", end=" ")

    try:
        # Fetch latest price from Yahoo Finance
        stock = yf.Ticker(f"{ticker}.NS")
        hist = stock.history(period="5d")

        if hist.empty:
            print("⚠️  No price data")
            error_count += 1
            continue

        latest_price = hist["Close"].iloc[-1]

        # Recalculate score (simple version, consistent with LITE bot logic)
        score = 0.0
        if signal == "🚀 Strong Buy":
            score += 1000
        elif signal == "👀 Watch":
            score += 500

        score += momentum * 500  # Momentum contribution
        score += volume * 50      # Volume contribution
        score = round(score, 2)

        # Update Notion page
        update_url = f"https://api.notion.com/v1/pages/{page_id}"
        update_payload = {
            "properties": {
                "Price (₹)": {"number": round(float(latest_price), 2)},
                "Score": {"number": score},
                "Last Updated": {"date": {"start": datetime.now().isoformat()}},
            }
        }

        update_response = requests.patch(
            update_url, headers=HEADERS, json=update_payload
        )

        if update_response.status_code == 200:
            print(f"✅ Price: ₹{latest_price:.2f}, Score: {score:.0f}")
            success_count += 1
        else:
            print("❌ Update failed")
            error_count += 1

        time.sleep(0.5)  # Rate limit protection

    except Exception as e:  # pragma: no cover - defensive
        print(f"❌ Error: {str(e)[:50]}")
        error_count += 1


print()
print("=" * 70)
print("✅ UPDATE COMPLETE!")
print("=" * 70)
print()
print("📊 Summary:")
print(f"   ✅ Successfully updated: {success_count} stocks")
print(f"   ❌ Errors: {error_count} stocks")
print(f"   ⏭️  Skipped: {skip_count} stocks")
print()
print("🎯 All stocks now have latest price and investment score!")
