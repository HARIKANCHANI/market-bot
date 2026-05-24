"""
Generate PNG images from Mermaid diagrams using mermaid.ink API
Standalone script - run with: python generate_diagram_images.py
"""

import urllib.request
import urllib.parse
import base64
import os

# Create docs directory if it doesn't exist
os.makedirs("docs", exist_ok=True)

print("=" * 70)
print("🎨 MERMAID DIAGRAM IMAGE GENERATOR")
print("=" * 70)
print()

# Diagram 1: File Relationships
diagram1_code = """graph TB
    subgraph "USER ENTRY POINTS"
        LITE[market_bot_lite.py]
        PRO[market_bot_pro.py]
        AI[market_bot_ai.py]
    end
    subgraph "CORE MODULES"
        RANK[ranking_engine.py]
        NEWS[news_aggregator.py]
        ANALYST[analyst_ratings.py]
    end
    subgraph "CONFIGURATION"
        ENV[env_config.py]
        ENVFILE[.env file]
    end
    subgraph "DATA SOURCES"
        NSE[nse_stocks_650.py]
        YFINANCE[yfinance API]
        FINBERT[FinBERT Model]
    end
    subgraph "OUTPUT"
        NOTION[(Notion Database)]
        LOGS[Log Files]
        EXCEL[Excel Export]
    end
    LITE --> RANK
    PRO --> RANK
    AI --> RANK
    LITE --> NEWS
    PRO --> NEWS
    AI --> NEWS
    LITE --> ANALYST
    PRO --> ANALYST
    AI --> ANALYST
    AI --> FINBERT
    LITE --> ENV
    PRO --> ENV
    AI --> ENV
    ENV --> ENVFILE
    LITE --> NSE
    PRO --> NSE
    AI --> NSE
    NEWS --> YFINANCE
    ANALYST --> YFINANCE
    LITE --> YFINANCE
    PRO --> YFINANCE
    AI --> YFINANCE
    RANK --> NOTION
    LITE --> NOTION
    PRO --> NOTION
    AI --> NOTION
    LITE --> LOGS
    PRO --> LOGS
    AI --> LOGS
    style LITE fill:#90EE90
    style PRO fill:#87CEEB
    style AI fill:#DDA0DD
    style RANK fill:#FFD700
    style NEWS fill:#FFD700
    style ANALYST fill:#FFD700
    style NOTION fill:#FF6B6B
    style ENV fill:#FFA07A"""

diagrams = {
    "1_File_Relationships_Architecture": diagram1_code
}

for filename, diagram_code in diagrams.items():
    print(f"📊 Generating: {filename}.png")
    
    try:
        # Encode to base64
        encoded = base64.urlsafe_b64encode(diagram_code.encode('utf-8')).decode('utf-8')
        
        # Create URL for mermaid.ink
        url = f"https://mermaid.ink/img/{encoded}"
        
        print(f"   🔗 URL: {url[:80]}...")
        
        # Download image
        output_file = f"docs/{filename}.png"
        urllib.request.urlretrieve(url, output_file)
        
        # Check if file was created
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"   ✅ Saved: {output_file} ({file_size:,} bytes)")
        else:
            print(f"   ❌ Failed to save file")
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()

print("=" * 70)
print("🎉 GENERATION COMPLETE!")
print("=" * 70)
print()
print("📁 Check the 'docs/' folder for generated PNG images")
print()
print("Generated URLs (you can also open these in browser):")
for filename in diagrams.keys():
    filepath = f"docs/{filename}.png"
    if os.path.exists(filepath):
        print(f"  ✅ {filepath}")
    else:
        print(f"  ❌ {filepath} (not created)")
print()
print("💡 TIP: If images didn't generate, you can:")
print("   1. Copy diagram code from ARCHITECTURE_DIAGRAMS_MERMAID.md")
print("   2. Go to https://mermaid.live")
print("   3. Paste and click 'Download PNG'")
print()
