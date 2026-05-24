"""
Notion Incremental Update Utilities
Provides helper functions for incremental database updates:
- Check if ticker exists in Notion database
- Update existing ticker entry
- Create new ticker entry
"""

import os
import sys
import requests
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import environment configuration
try:
    from src.config.env_config import NOTION_TOKEN, DATABASE_ID, get_notion_headers
except ImportError:
    from dotenv import load_dotenv
    load_dotenv()
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    DATABASE_ID = os.getenv("DATABASE_ID")
    
    def get_notion_headers():
        return {
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }


def query_ticker_in_database(ticker: str) -> Optional[Dict[str, Any]]:
    """
    Query Notion database for a specific ticker.
    
    Args:
        ticker: Stock ticker symbol (e.g., "RELIANCE.NS")
    
    Returns:
        Dictionary with page_id and properties if found, None if not found
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = get_notion_headers()
    
    # Query filter to find the ticker
    payload = {
        "filter": {
            "property": "Ticker",
            "title": {
                "equals": ticker
            }
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                # Return first matching page
                return {
                    "page_id": results[0]["id"],
                    "properties": results[0]["properties"]
                }
        return None
    except Exception as e:
        print(f"⚠️  Error querying ticker {ticker}: {str(e)}")
        return None


def update_notion_page(page_id: str, properties: Dict[str, Any]) -> bool:
    """
    Update an existing Notion page with new properties.
    
    Args:
        page_id: The Notion page ID to update
        properties: Dictionary of properties to update
    
    Returns:
        True if successful, False otherwise
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = get_notion_headers()
    
    payload = {"properties": properties}
    
    try:
        response = requests.patch(url, json=payload, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print(f"⚠️  Error updating page {page_id}: {str(e)}")
        return False


def create_notion_page(properties: Dict[str, Any]) -> bool:
    """
    Create a new Notion page with given properties.
    
    Args:
        properties: Dictionary of properties for the new page
    
    Returns:
        True if successful, False otherwise
    """
    url = "https://api.notion.com/v1/pages"
    headers = get_notion_headers()
    
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": properties
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print(f"⚠️  Error creating page: {str(e)}")
        return False


def upsert_notion_entry(ticker: str, properties: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Update existing ticker or create new one (upsert operation).
    
    Args:
        ticker: Stock ticker symbol
        properties: Dictionary of properties to set/update
    
    Returns:
        Tuple of (success: bool, action: str) where action is "updated" or "created"
    """
    # Check if ticker exists
    existing = query_ticker_in_database(ticker)
    
    if existing:
        # Update existing entry
        success = update_notion_page(existing["page_id"], properties)
        return (success, "updated")
    else:
        # Create new entry
        success = create_notion_page(properties)
        return (success, "created")
