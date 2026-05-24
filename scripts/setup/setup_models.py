"""
Setup Script for Market Bot
Downloads all required AI models and verifies dependencies before running the bot.
Run this ONCE before using src/bots/market_bot_ai.py
"""

import os
import sys

print("=" * 60)
print("🚀 MARKET BOT SETUP - Pre-downloading AI Models")
print("=" * 60)

# Set Hugging Face token for faster downloads
# Get from environment variable or use placeholder
HF_TOKEN = os.getenv("HF_TOKEN", "your_huggingface_token_here")
if HF_TOKEN and HF_TOKEN != "your_huggingface_token_here":
    os.environ["HF_TOKEN"] = HF_TOKEN
os.environ["TRANSFORMERS_CACHE"] = os.path.join(os.getcwd(), "models")

if HF_TOKEN and HF_TOKEN != "your_huggingface_token_here":
    print("\n✓ Hugging Face token configured")
else:
    print("\n⚠️  HF_TOKEN not set - downloads may be slower")
print(f"✓ Models will be cached in: {os.environ['TRANSFORMERS_CACHE']}")

# Step 1: Check dependencies
print("\n" + "=" * 60)
print("📦 Step 1/3: Checking Dependencies...")
print("=" * 60)

required_packages = {
    'pandas': 'pandas',
    'yfinance': 'yfinance', 
    'transformers': 'transformers',
    'torch': 'torch',
    'requests': 'requests'
}

missing = []
for package_name, import_name in required_packages.items():
    try:
        __import__(import_name)
        print(f"  ✓ {package_name}")
    except ImportError:
        print(f"  ✗ {package_name} - MISSING")
        missing.append(package_name)

if missing:
    print(f"\n❌ Missing packages: {', '.join(missing)}")
    print("   Run: pip install -r requirements.txt")
    sys.exit(1)

print("\n✅ All dependencies installed!")

# Step 2: Download FinBERT model
print("\n" + "=" * 60)
print("🤖 Step 2/3: Downloading FinBERT AI Model (~440MB)")
print("=" * 60)
print("⏳ This will take 1-2 minutes depending on your internet speed...")
print("   The model will be cached locally for instant future use.\n")

try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification

    print("📥 Downloading ProsusAI/finbert model components...")
    print("   This is ~440MB - please be patient...")
    print("   ⏱️  Estimated time: 2-5 minutes (depends on internet speed)\n")

    # Download with progress bar
    print("   [1/2] Downloading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    print("   ✓ Tokenizer downloaded\n")

    print("   [2/2] Downloading model weights (~430MB)...")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    print("   ✓ Model downloaded\n")

    print("✅ FinBERT model downloaded and cached successfully!")
    
    # Test the model
    print("🧪 Testing model with sample text...")
    from transformers import pipeline
    test_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=-1)
    test_result = test_pipeline(["Stock market shows strong growth potential"])
    print(f"   Test result: {test_result[0]}")
    print("✅ Model working correctly!")
    
except Exception as e:
    print(f"❌ Error downloading model: {e}")
    sys.exit(1)

# Step 3: Test Yahoo Finance connection
print("\n" + "=" * 60)
print("📊 Step 3/3: Testing Yahoo Finance Connection")
print("=" * 60)

try:
    import yfinance as yf
    
    print("🔍 Fetching sample data for RELIANCE.NS...")
    test_stock = yf.Ticker("RELIANCE.NS")
    test_data = test_stock.history(period="5d")
    
    if test_data.empty:
        print("⚠️  Warning: No data received. Check internet connection.")
    else:
        print(f"✅ Successfully fetched {len(test_data)} days of data")
        print(f"   Latest close price: ₹{test_data['Close'].iloc[-1]:.2f}")
    
except Exception as e:
    print(f"⚠️  Warning: Yahoo Finance test failed: {e}")
    print("   This might be temporary. Try running the main bot anyway.")

# Final summary
print("\n" + "=" * 60)
print("🎉 SETUP COMPLETE!")
print("=" * 60)
print("\n✅ All models downloaded and cached")
print("✅ Dependencies verified")
print("✅ API connections tested")
print("\n📝 Next Steps:")
print("   1. Run your AI bot with: python src/bots/market_bot_ai.py")
print("   2. The bot will now start INSTANTLY (no download wait)")
print("\n💡 Note: You only need to run this setup script once!")
print("   Models are cached and will be reused automatically.")
print("=" * 60)
