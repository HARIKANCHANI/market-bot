#!/usr/bin/env python3
"""Fresh Start - complete database reset and basic schema verification.

Steps performed:

1. Fetch and archive (delete) all existing pages in the configured database.
2. Ensure a reasonable column set and order for the stock universe.

This script **does not** repopulate the database; it only cleans and
prepares it. After running, use one of the bots to load fresh data.
"""

from __future__ import annotations

import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict

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
    print("   Please set them in your .env file")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/fresh_start.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def get_all_pages() -> list[dict]:
    """Fetch all pages from the database."""

    logger.info("Fetching all pages from database...")

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    all_pages: list[dict] = []
    has_more = True
    start_cursor: str | None = None

    while has_more:
        payload: Dict[str, str] = {}
        if start_cursor:
            payload["start_cursor"] = start_cursor

        response = requests.post(url, json=payload, headers=HEADERS)
        if response.status_code != 200:
            logger.error("Failed to fetch pages: %s", response.status_code)
            return []

        data = response.json()
        all_pages.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")

    return all_pages


def delete_page(page_id: str) -> bool:
    """Archive a single page."""

    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"archived": True}
    response = requests.patch(url, json=payload, headers=HEADERS)
    return response.status_code == 200


def clear_all_entries() -> bool:
    """Step 1: clear all existing entries from the database."""

    logger.info("=" * 70)
    logger.info("STEP 1: CLEARING ALL EXISTING ENTRIES")
    logger.info("=" * 70)

    pages = get_all_pages()
    if not pages:
        logger.info("✅ Database is already empty!")
        return True

    logger.info("Found %d entries to delete", len(pages))

    success_count = 0
    for i, page in enumerate(pages, start=1):
        page_id = page["id"]

        ticker = "Unknown"
        try:
            title_prop = page.get("properties", {}).get("Ticker", {})
            title = title_prop.get("title") or []
            if title:
                text = title[0].get("text", {})
                ticker = text.get("content", ticker)
        except Exception:
            pass

        if delete_page(page_id):
            success_count += 1
            if i % 20 == 0:
                logger.info("   Deleted %d/%d entries...", i, len(pages))

        if i % 10 == 0:
            time.sleep(0.3)

    logger.info("✅ Successfully deleted %d/%d entries", success_count, len(pages))
    return success_count == len(pages)


def verify_schema() -> bool:
    """Step 2: ensure basic schema and ordering for core stock columns."""

    logger.info("")
    logger.info("=" * 70)
    logger.info("STEP 2: VERIFYING DATABASE SCHEMA")
    logger.info("=" * 70)

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        logger.error("Failed to fetch database schema: %s", response.status_code)
        return False

    db_data = response.json()
    current_properties: dict = db_data.get("properties", {})

    # Preserve existing definitions where possible
    existing = dict(current_properties)

    def keep_or(default_key: str, default_value: dict) -> dict:
        return existing.get(default_key, default_value)

    desired: dict = {}
    desired["Ticker"] = keep_or("Ticker", {"title": {}})
    desired["Rank"] = keep_or("Rank", {"number": {"format": "number"}})
    desired["Market Cap"] = keep_or("Market Cap", {"select": {}})
    desired["Price (₹)"] = keep_or("Price (₹)", {"number": {"format": "number"}})
    desired["Sentiment"] = keep_or("Sentiment", {"number": {"format": "number"}})
    desired["Momentum (%)"] = keep_or("Momentum (%)", {"number": {"format": "number"}})
    desired["Volume Surge"] = keep_or("Volume Surge", {"number": {"format": "number"}})
    desired["Score"] = keep_or("Score", {"number": {"format": "number"}})
    desired["Signal"] = keep_or("Signal", {"select": {}})
    desired["News & Updates"] = keep_or("News & Updates", {"rich_text": {}})
    desired["News Sentiment"] = keep_or("News Sentiment", {"select": {}})
    desired["Last Updated"] = keep_or("Last Updated", {"date": {}})

    payload = {"properties": desired}
    update = requests.patch(url, json=payload, headers=HEADERS)
    if update.status_code != 200:
        logger.error("Failed to update schema: %s", update.status_code)
        logger.error("Error: %s", update.text)
        return False

    logger.info("✅ Schema verified and updated successfully!")
    logger.info("")
    logger.info("Column Order:")
    for i, name in enumerate(desired.keys(), start=1):
        marker = "⭐" if name == "Rank" else "  "
        logger.info("   %s %d. %s", marker, i, name)
    return True


def main() -> None:
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 18 + "FRESH START - COMPLETE RESET" + " " * 20 + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    start_time = time.time()

    if not clear_all_entries():
        logger.error("❌ Failed to clear database")
        return

    if not verify_schema():
        logger.error("❌ Failed to verify schema")
        return

    logger.info("")
    logger.info("=" * 70)
    logger.info("✅ DATABASE RESET COMPLETE!")
    logger.info("=" * 70)
    logger.info("")
    logger.info("📊 Database Status:")
    logger.info("   ✅ All old entries cleared")
    logger.info("   ✅ Schema updated with proper column order")
    logger.info("   ✅ Ready for fresh data")
    logger.info("")

    elapsed = time.time() - start_time
    logger.info("⏱️  Reset completed in %.1f seconds", elapsed)
    logger.info("")
    logger.info("=" * 70)
    logger.info("🚀 NEXT STEP: LOAD FRESH DATA")
    logger.info("=" * 70)
    logger.info("")
    logger.info("Choose one of these commands to populate with all 675 stocks:")
    logger.info("")
    logger.info("   1. AI Sentiment Version (Recommended):")
    logger.info("      python src/bots/market_bot_ai.py")
    logger.info("")
    logger.info("   2. Production Version (With all features):")
    logger.info("      python src/bots/market_bot_pro.py")
    logger.info("")
    logger.info("   3. Fast Version (Technical analysis only):")
    logger.info("      python src/bots/market_bot_lite.py")
    logger.info("")
    logger.info("Expected processing time: ~20-25 minutes for 675 stocks")
    logger.info("")
    logger.info("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user")
    except Exception as e:  # pragma: no cover - defensive
        print(f"\n❌ Error: {e}")
