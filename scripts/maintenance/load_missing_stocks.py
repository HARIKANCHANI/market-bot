#!/usr/bin/env python3
"""Load missing stocks into the Notion database.

This maintenance script compares the full NSE universe from
``data/nse_stocks_650.py`` with the tickers currently present in the
Notion database and adds any missing stocks.

It reuses the **Lite bot's** market-intelligence and Notion upload logic
so new stocks are populated with the same fields and scoring model.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Set, List, Tuple

import requests
from dotenv import load_dotenv

from data.nse_stocks_650 import get_all_stocks_with_classification
from src.bots.market_bot_lite import get_market_intelligence, send_to_notion

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


def get_existing_tickers() -> Set[str]:
    """Return set of tickers already present in the Notion database."""

    print("🔍 Fetching existing stocks from database...")

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    all_tickers: Set[str] = set()
    has_more = True
    start_cursor: str | None = None

    while has_more:
        payload: dict = {"page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor

        response = requests.post(url, json=payload, headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ Failed to fetch pages: {response.status_code}")
            break

        data = response.json()
        for page in data.get("results", []):
            try:
                props = page.get("properties", {})
                title_prop = props.get("Ticker", {})
                title = title_prop.get("title") or []
                if title:
                    text = title[0].get("text", {})
                    ticker = text.get("content", "").strip()
                    if ticker:
                        all_tickers.add(ticker)
            except Exception:
                # Ignore pages where ticker cannot be parsed
                pass

        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")

        print(f"   ✅ Collected {len(all_tickers)} tickers so far...")

    print(f"✅ Found {len(all_tickers)} existing stocks in Notion")
    return all_tickers


def compute_missing_stocks() -> List[Tuple[str, str]]:
    """Return list of (ticker, cap_size) pairs that are missing in Notion."""

    universe = get_all_stocks_with_classification()
    universe_tickers = {t for (t, _cap) in universe}

    existing = get_existing_tickers()

    missing: List[Tuple[str, str]] = [
        (ticker, cap)
        for (ticker, cap) in universe
        if ticker not in existing
    ]

    print("")
    print("=" * 70)
    print("📊 MISSING STOCKS SUMMARY")
    print("=" * 70)
    print(f"Total NSE universe: {len(universe_tickers)}")
    print(f"Already in Notion: {len(existing)}")
    print(f"Missing (to add now): {len(missing)}")
    print("")

    return missing


def main() -> None:
    start_time = time.time()

    print("\n" + "=" * 70)
    print("📥 LOADING MISSING STOCKS INTO NOTION")
    print("=" * 70)
    print("")

    try:
        missing = compute_missing_stocks()
    except Exception as exc:  # pragma: no cover - defensive
        print(f"❌ Failed to determine missing stocks: {exc}")
        return

    if not missing:
        print("✅ Database already contains all stocks. Nothing to do.")
        return

    print("🚀 Starting incremental load for missing stocks...")
    print("(Reuses market_bot_lite intelligence + scoring + Notion schema)")
    print("")

    success = 0
    errors = 0

    for idx, (ticker, cap_size) in enumerate(missing, 1):
        print(f"[{idx}/{len(missing)}] 🔍 {ticker} ({cap_size})")
        try:
            metrics = get_market_intelligence(ticker, cap_size)
            if not metrics:
                print("   ❌ No data returned, skipping")
                errors += 1
                continue

            # Use the same Notion payload logic as the Lite bot
            send_to_notion(metrics, rank=None)
            success += 1
        except Exception as exc:  # pragma: no cover - defensive
            print(f"   ❌ Error processing {ticker}: {exc}")
            errors += 1

        # Light rate limiting to be kind to APIs
        time.sleep(1.0)

    elapsed = time.time() - start_time

    print("\n" + "=" * 70)
    print("📊 LOAD MISSING STOCKS - SUMMARY")
    print("=" * 70)
    print(f"✅ Successfully added: {success}")
    print(f"❌ Errors: {errors}")
    print(f"⏱️  Total time: {elapsed/60:.1f} minutes")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user")
    except Exception as e:  # pragma: no cover - defensive
        print(f"\n❌ Error: {e}")
