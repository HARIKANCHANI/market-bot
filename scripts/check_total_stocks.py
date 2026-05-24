import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
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

# Fetch all pages
all_pages = []
has_more = True
start_cursor = None

while has_more:
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {"page_size": 100}
    if start_cursor:
        payload["start_cursor"] = start_cursor
    
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    
    all_pages.extend(data.get("results", []))
    has_more = data.get("has_more", False)
    start_cursor = data.get("next_cursor")
    
    print(f"Fetched {len(all_pages)} stocks so far...")

print(f"\nTotal stocks in database: {len(all_pages)}")
