"""Delete all entries from the Notion database.

Use this before doing a full fresh upload. Interactive confirmation is
required so the script is safe to run accidentally.
"""

from __future__ import annotations

import os
import sys
import time
from typing import List
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    print(f"⚠️  Warning: .env file not found at {env_path}")
    print("   Please create .env from .env.example and set your credentials")

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


def get_all_pages() -> List[dict]:
    """Return all pages in the configured Notion database."""

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    all_pages: List[dict] = []
    has_more = True
    start_cursor: str | None = None

    while has_more:
        payload: dict = {}
        if start_cursor:
            payload["start_cursor"] = start_cursor

        response = requests.post(url, json=payload, headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ Error fetching pages: {response.text}")
            break

        data = response.json()
        all_pages.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")

        print(f"📊 Fetched {len(all_pages)} pages so far...")

    return all_pages


def delete_page(page_id: str) -> bool:
    """Archive/delete a page in Notion.

    We use the standard Notion page update API with ``archived=True``.
    """

    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"archived": True}
    response = requests.patch(url, json=payload, headers=HEADERS)
    return response.status_code == 200


if __name__ == "__main__":
    print("=" * 70)
    print("🗑️  NOTION DATABASE CLEANUP")
    print("=" * 70)
    print(f"\n📍 Database ID: {DATABASE_ID}")
    print("🔐 Using Notion API Token")

    # Fetch pages
    print("\n🔍 Fetching all pages from database...")
    pages = get_all_pages()

    if not pages:
        print("\n✅ Database is already empty!")
        raise SystemExit(0)

    total_pages = len(pages)
    print(f"\n📊 Found {total_pages} entries to delete")

    # Confirm deletion
    print(
        f"\n⚠️  WARNING: This will delete *all* {total_pages} entries "
        "from your Notion database!"
    )
    confirmation = input("Type 'DELETE' to confirm: ")

    if confirmation != "DELETE":
        print("\n❌ Deletion cancelled.")
        raise SystemExit(0)

    # Delete all pages
    print(f"\n🗑️  Deleting {total_pages} entries...")
    print("=" * 70)

    success_count = 0
    error_count = 0

    for idx, page in enumerate(pages, start=1):
        page_id = page["id"]

        # Try to get ticker name for better logging
        ticker = "Unknown"
        try:
            ticker_prop = page.get("properties", {}).get("Ticker", {})
            title = ticker_prop.get("title") or []
            if title:
                text = title[0].get("text", {})
                ticker = text.get("content", ticker)
        except Exception:
            # If ticker can't be read, keep as "Unknown" and continue
            pass

        if delete_page(page_id):
            success_count += 1
            print(f"✅ [{idx}/{total_pages}] Deleted: {ticker}")
        else:
            error_count += 1
            print(f"❌ [{idx}/{total_pages}] Failed: {ticker}")

        # Rate limiting
        time.sleep(0.3)

        # Progress update every 50 deletions
        if idx % 50 == 0:
            print(
                f"\n📈 Progress: {idx}/{total_pages} "
                f"({idx / total_pages * 100:.1f}%)"
            )
            print(f"   ✅ Successful: {success_count}")
            print(f"   ❌ Failed: {error_count}\n")

    # Final summary
    print("\n" + "=" * 70)
    print("📊 DELETION SUMMARY")
    print("=" * 70)
    print(f"Total entries: {total_pages}")
    print(f"✅ Successfully deleted: {success_count}")
    print(f"❌ Failed: {error_count}")
    print("=" * 70)

    if success_count == total_pages:
        print("\n🎉 All entries deleted successfully!")
        print("✅ Database is now empty and ready for fresh data upload.")
    else:
        print(f"\n⚠️  Warning: {error_count} entries failed to delete.")
        print("   You may need to delete them manually or run this script again.")
