"""
Quick test script for the Excel bot version
Tests with a small sample of 5 stocks to verify functionality
"""
import sys
import os
from datetime import datetime

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print("="*70)
print("🧪 TESTING EXCEL BOT VERSION (5 STOCKS)")
print("="*70)

# Test imports
print("\n1️⃣ Testing imports...")
try:
    from src.bots.market_bot_excel import (
        get_market_intelligence,
        calculate_signal_score,
        create_excel_report,
    )
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)

# Test data collection
print("\n2️⃣ Testing data collection (5 stocks)...")
test_stocks = [
    ("RELIANCE", "Large Cap"),
    ("TCS", "Large Cap"),
    ("INFY", "Large Cap"),
    ("HDFCBANK", "Large Cap"),
    ("ICICIBANK", "Large Cap")
]

all_data = []
for symbol, cap in test_stocks:
    print(f"\n   Analyzing {symbol}...")
    data = get_market_intelligence(symbol, cap)
    
    # Calculate signal and score
    signal, score = calculate_signal_score(data)
    data['signal'] = signal
    data['score'] = score
    data['rank'] = 0  # Will be set after sorting
    data['consensus'] = 'N/A'
    data['ratings'] = 'N/A'
    
    all_data.append(data)
    print(f"   ✅ {symbol}: Price=₹{data.get('price', 0):.2f}, Signal={signal}, Score={score}")

# Rank stocks
print("\n3️⃣ Ranking stocks...")
ranked_data = sorted(all_data, key=lambda x: x.get('score', 0), reverse=True)
for idx, stock in enumerate(ranked_data, 1):
    stock['rank'] = idx

print(f"✅ Ranked {len(ranked_data)} stocks")
for stock in ranked_data:
    print(f"   Rank {stock['rank']}: {stock['ticker']} (Score: {stock['score']})")

# Create Excel report
print("\n4️⃣ Creating Excel report...")

excel_dir = os.path.join(project_root, "src", "bots", "excel")
os.makedirs(excel_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
test_filename = os.path.join(excel_dir, f"TEST_market_analysis_{timestamp}.xlsx")

try:
    create_excel_report(ranked_data, test_filename)
    print(f"\n✅ Test Excel file created: {test_filename}")
except Exception as e:
    print(f"\n❌ Error creating Excel file: {e}")
    exit(1)

# Verify file exists
if os.path.exists(test_filename):
    file_size = os.path.getsize(test_filename) / 1024  # KB
    print(f"✅ File verified: {file_size:.1f} KB")
else:
    print("❌ File was not created")
    exit(1)

print("\n" + "="*70)
print("✅ ALL TESTS PASSED!")
print("="*70)
print(f"\n📁 Test report: {test_filename}")
print("\n💡 You can now run the full bot with:")
print("   python src/bots/market_bot_excel.py")
print("="*70)
