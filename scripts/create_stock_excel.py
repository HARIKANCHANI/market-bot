"""Create comprehensive Excel sheet with stock data including FII/DII information."""

import os
import sys
from pathlib import Path
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# Notion credentials
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('DATABASE_ID') or os.getenv('NOTION_DATABASE_ID')

if not NOTION_TOKEN or not DATABASE_ID:
    print("❌ ERROR: NOTION_TOKEN or DATABASE_ID not found in environment variables")
    print("   Please set them in your .env file")
    sys.exit(1)

# Notion API headers
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

print("=" * 70)
print("📊 CREATING COMPREHENSIVE STOCK EXCEL SHEET")
print("=" * 70)

print("\n🔍 Fetching all stocks from Notion database...")

# Fetch all pages from the database
all_stocks = []
has_more = True
start_cursor = None

while has_more:
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {}
    if start_cursor:
        payload["start_cursor"] = start_cursor

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        print(f"❌ Error fetching pages: {response.text}")
        break

    data = response.json()
    all_stocks.extend(data.get('results', []))
    has_more = data.get('has_more', False)
    start_cursor = data.get('next_cursor')

    print(f"   Fetched {len(all_stocks)} stocks so far...")

print(f"\n✅ Total stocks fetched: {len(all_stocks)}")

# Extract stock data
stock_data = []

print("\n📝 Extracting stock information...")
for page in all_stocks:
    props = page['properties']

    try:
        # Extract ticker/symbol
        ticker_prop = props.get('Ticker', {}) or props.get('Symbol', {})
        ticker_text = 'N/A'
        if ticker_prop.get('title'):
            ticker_text = ticker_prop['title'][0]['text']['content'] if ticker_prop['title'] else 'N/A'

        stock_info = {
            'Symbol': ticker_text,
            'Rank': props.get('Rank', {}).get('number') or 0,
            'Price': props.get('Price (₹)', {}).get('number') or props.get('Price', {}).get('number') or 0,
            'Momentum': props.get('Momentum (%)', {}).get('number') or props.get('Momentum', {}).get('number') or 0,
            'Volume': props.get('Volume Surge', {}).get('number') or props.get('Volume', {}).get('number') or 0,
            'Trend': (props.get('Trend', {}).get('select') or {}).get('name', 'N/A'),
            'Score': props.get('Score', {}).get('number') or 0,
            'Signal': (props.get('Signal', {}).get('select') or {}).get('name', 'N/A'),
            'Sector': (props.get('Sector', {}).get('select') or {}).get('name', 'Unknown'),
            'Market Cap': (props.get('Market Cap', {}).get('select') or {}).get('name', 'N/A'),
            'News Sentiment': (props.get('News Sentiment', {}).get('select') or {}).get('name', 'N/A'),
        }
        stock_data.append(stock_info)
    except Exception as e:
        print(f"   ⚠️  Error extracting stock: {e}")

print(f"✅ Extracted {len(stock_data)} stocks successfully")

# Create DataFrame
if len(stock_data) == 0:
    print("\n❌ No stock data extracted! Please check the database.")
    exit(1)

df = pd.DataFrame(stock_data)

# Sort by Rank (if Rank column exists and has valid data)
if 'Rank' in df.columns and df['Rank'].notna().any() and (df['Rank'] > 0).any():
    df = df.sort_values('Rank', ascending=True).reset_index(drop=True)
else:
    print("\n⚠️  Warning: No valid rank data found, sorting by Symbol instead")
    df = df.sort_values('Symbol', ascending=True).reset_index(drop=True)

# Add FII/DII columns (will be filled with placeholder data for now)
df['FII Holdings %'] = 'Data Required'
df['DII Holdings %'] = 'Data Required'
df['Promoter Holdings %'] = 'Data Required'
df['MF Holdings %'] = 'Data Required'
df['FII Trend'] = 'Data Required'
df['DII Trend'] = 'Data Required'
df['Institutional Confidence'] = 'Data Required'

print("\n💡 Note: FII/DII data requires additional API calls.")
print("   Placeholder values added. You can update manually or run a separate script.")

# Create output directory if it doesn't exist
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Generate filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{output_dir}/stocks_analysis_{timestamp}.xlsx"

print(f"\n💾 Creating Excel file: {filename}")

# Create Excel file with formatting
with pd.ExcelWriter(filename, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='All Stocks', index=False)
    
    # Get the worksheet
    worksheet = writer.sheets['All Stocks']
    
    # Auto-adjust column widths
    for column in worksheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except Exception:
                # Safely ignore cells that can't be measured
                pass
        adjusted_width = min(max_length + 2, 50)
        worksheet.column_dimensions[column_letter].width = adjusted_width

print("✅ Excel file created successfully!")
print(f"\n📁 File location: {os.path.abspath(filename)}")
print(f"📊 Total stocks: {len(df)}")
print("📈 Top 5 ranked stocks:")
for idx, row in df.head(5).iterrows():
    print(f"   {row['Rank']:3.0f}. {row['Symbol']:<15} - ₹{row['Price']:.2f} ({row['Momentum']:+.1f}%) - {row['Sector']}")

print("\n" + "=" * 70)
print("✅ EXCEL CREATION COMPLETE!")
print("=" * 70)
