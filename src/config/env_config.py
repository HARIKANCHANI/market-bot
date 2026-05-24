#!/usr/bin/env python3
"""
Environment Configuration Module
Handles loading environment variables from .env file
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Find the project root (where .env should be)
def find_project_root():
    """Find the project root directory (where .env file is located)."""
    current_dir = Path(__file__).resolve().parent
    # Go up until we find .env or reach root
    while current_dir != current_dir.parent:
        if (current_dir / '.env').exists() or (current_dir / '.env.example').exists():
            return current_dir
        current_dir = current_dir.parent
    # Default to 2 levels up from this file (src/config/)
    return Path(__file__).resolve().parent.parent.parent

# Load environment variables
PROJECT_ROOT = find_project_root()
ENV_FILE = PROJECT_ROOT / '.env'

# Load .env file if it exists
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    print(f"⚠️  Warning: .env file not found at {ENV_FILE}")
    print(f"   Create one from .env.example: cp .env.example .env")

# Notion Configuration
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('DATABASE_ID')
NOTION_API_VERSION = os.getenv('NOTION_API_VERSION', '2022-06-28')

# HuggingFace Configuration (for AI bot)
HF_TOKEN = os.getenv('HF_TOKEN')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_DIR = os.getenv('LOG_DIR', 'logs')

def validate_notion_config():
    """Validate that required Notion credentials are set."""
    if not NOTION_TOKEN:
        raise ValueError(
            "NOTION_TOKEN not found in environment variables.\n"
            "Please set it in your .env file or environment."
        )
    if not DATABASE_ID:
        raise ValueError(
            "DATABASE_ID not found in environment variables.\n"
            "Please set it in your .env file or environment."
        )
    return True

def validate_hf_config():
    """Validate that HuggingFace token is set (for AI bot)."""
    if not HF_TOKEN:
        raise ValueError(
            "HF_TOKEN not found in environment variables.\n"
            "This is required for the AI bot. Please set it in your .env file."
        )
    return True

def get_notion_headers():
    """Get Notion API headers with proper authentication."""
    validate_notion_config()
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json"
    }

# For backwards compatibility - export the values
__all__ = [
    'NOTION_TOKEN',
    'DATABASE_ID',
    'NOTION_API_VERSION',
    'HF_TOKEN',
    'LOG_LEVEL',
    'LOG_DIR',
    'validate_notion_config',
    'validate_hf_config',
    'get_notion_headers',
    'PROJECT_ROOT',
]
