#!/usr/bin/env python3
"""Add and populate analyst ratings columns in the Notion database.

This script:

1. Ensures the database has ``Consensus`` (select) and ``Ratings`` (rich text)
   columns.
2. Iterates through all stocks and fills these columns using aggregated
   analyst ratings from :mod:`src.core.analyst_ratings`.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import List, Optional

import requests
from dotenv import load_dotenv

from src.core.analyst_ratings import aggregate_all_analyst_ratings

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


def add_analyst_columns() -> bool:
    """Ensure the Consensus and Ratings columns exist on the database."""

    print("=" * 70)
    print("📊 Adding Analyst Ratings Columns to Notion Database")
    print("=" * 70)
    print()

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"

    # Fetch current schema
    print("🔍 Fetching current database schema...")
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ Failed to fetch database: {response.status_code}")
        return False

    db_data = response.json()
    current_properties = db_data.get("properties", {})
    print(f"✅ Current schema retrieved ({len(current_properties)} columns)")
    print()

    has_consensus = "Consensus" in current_properties
    has_ratings = "Ratings" in current_properties

    if has_consensus and has_ratings:
        print("✅ Consensus and Ratings columns already exist!")
        return True

    # Build updated properties payload
    new_properties = dict(current_properties)

    if not has_consensus:
        print("➕ Adding 'Consensus' column...")
        new_properties["Consensus"] = {
            "select": {
                "options": [
                    {"name": "Strong Buy", "color": "green"},
                    {"name": "Buy", "color": "blue"},
                    {"name": "Moderate Buy", "color": "default"},
                    {"name": "Hold", "color": "yellow"},
                    {"name": "Moderate Sell", "color": "orange"},
                    {"name": "Sell", "color": "pink"},
                    {"name": "Strong Sell", "color": "red"},
                    {"name": "No Consensus", "color": "gray"},
                ]
            }
        }

    if not has_ratings:
        print("➕ Adding 'Ratings' column...")
        new_properties["Ratings"] = {"rich_text": {}}

    payload = {"properties": new_properties}
    update = requests.patch(url, json=payload, headers=HEADERS)
    if update.status_code != 200:
        print(f"❌ Failed to add columns: {update.status_code}")
        print(f"   Error: {update.text}")
        return False

    print("✅ Successfully added analyst columns!")
    print()
    print("📋 Column Details:")
    if not has_consensus:
        print("   • Consensus: Select (Strong Buy to Strong Sell)")
    if not has_ratings:
        print("   • Ratings: Rich Text (X.XX/5.0 + analyst count)")
    print()
    return True


def get_all_stocks() -> Optional[List[dict]]:
    """Fetch all stock pages from the database."""

    print("🔍 Fetching all stocks from database...")

    all_stocks: List[dict] = []
    has_more = True
    start_cursor: Optional[str] = None
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    while has_more:
        payload: dict = {}
        if start_cursor:
            payload["start_cursor"] = start_cursor

        response = requests.post(url, json=payload, headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ Failed to fetch stocks: {response.status_code}")
            return None

        data = response.json()
        all_stocks.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")

    print(f"✅ Found {len(all_stocks)} stocks in database")
    print()
    return all_stocks


def update_stock_with_ratings(page_id: str, ticker: str, consensus: str, rating_text: str) -> bool:
    """Patch a single stock page with consensus + ratings text."""

    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            "Consensus": {"select": {"name": consensus}},
            "Ratings": {"rich_text": [{"text": {"content": rating_text}}]},
        }
    }
    response = requests.patch(url, json=payload, headers=HEADERS)
    return response.status_code == 200


def populate_analyst_ratings() -> None:
    """Populate all stocks with analyst ratings using the core ratings module."""

    print("=" * 70)
    print("📊 Populating Analyst Ratings for All Stocks")
    print("=" * 70)
    print()

    stocks = get_all_stocks()
    if not stocks:
        return

    print(f"🔄 Processing {len(stocks)} stocks...")
    print(f"⏱️  Estimated time: ~{len(stocks) * 2 / 60:.0f} minutes (with delays)")
    print()

    success_count = 0
    no_data_count = 0

    for i, stock in enumerate(stocks, start=1):
        page_id = stock["id"]

        # Get ticker (defensive against malformed pages)
        ticker = "Unknown"
        try:
            title_prop = stock.get("properties", {}).get("Ticker", {})
            title = title_prop.get("title") or []
            if title:
                text = title[0].get("text", {})
                ticker = text.get("content", ticker)
        except Exception:
            pass

        if ticker == "Unknown":
            print(f"[{i}/{len(stocks)}] ⚠️  No ticker found, skipping...")
            continue

        print(f"[{i}/{len(stocks)}] 🔍 {ticker}...", end=" ")

        # Get analyst ratings
        ratings_data = aggregate_all_analyst_ratings(ticker)

        if ratings_data["has_data"]:
            consensus = ratings_data["consensus"]
            rating_numeric = ratings_data["rating_numeric"]
            analyst_count = ratings_data["analyst_count"]
            rating_text = f"{rating_numeric:.2f}/5.0 ({analyst_count} analysts)"

            if update_stock_with_ratings(page_id, ticker, consensus, rating_text):
                print(f"✅ {consensus} | {rating_text}")
                success_count += 1
            else:
                print("❌ Failed to update")
        else:
            if update_stock_with_ratings(page_id, ticker, "No Consensus", "N/A"):
                print("⚠️  No Consensus | N/A")
                no_data_count += 1
            else:
                print("❌ Failed to update")

        # Rate limiting
        if i % 10 == 0:
            time.sleep(1)
        else:
            time.sleep(0.5)

    print()
    print("=" * 70)
    print("📊 ANALYST RATINGS UPDATE COMPLETE")
    print("=" * 70)
    print()
    print(f"✅ Successfully updated: {success_count}")
    print(f"⚠️  No consensus available: {no_data_count}")
    print(f"📊 Total processed: {len(stocks)}")
    print()


def main() -> None:
    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "ANALYST RATINGS & CONSENSUS SYSTEM" + " " * 19 + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    if not add_analyst_columns():
        print("❌ Failed to add columns. Exiting.")
        return

    print()
    populate_analyst_ratings()

    print()
    print("=" * 70)
    print("🎉 COMPLETE!")
    print("=" * 70)
    print()
    print("📊 Your database now has:")
    print("   ✅ Consensus column (Strong Buy to Strong Sell)")
    print("   ✅ Ratings column (X.XX/5.0 with analyst count)")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user")
    except Exception as e:  # pragma: no cover - defensive
        print(f"\n❌ Error: {e}")
