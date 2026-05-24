"""
Generate PNG images from Mermaid diagrams using mermaid.ink API
"""

import requests
import base64
import os
from pathlib import Path

# Create docs directory if it doesn't exist
docs_dir = Path("docs")
docs_dir.mkdir(exist_ok=True)

# Mermaid diagrams
diagrams = {
    "File_Relationships_Architecture": """graph TB
    subgraph "USER ENTRY POINTS"
        LITE[market_bot_lite.py<br/>18-20 min]
        PRO[market_bot_pro.py<br/>30-35 min]
        AI[market_bot_ai.py<br/>4-5 hours]
    end

    subgraph "CORE MODULES"
        RANK[ranking_engine.py<br/>9-metric ranking]
        NEWS[news_aggregator.py<br/>70+ sources]
        ANALYST[analyst_ratings.py<br/>50+ analysts]
    end

    subgraph "CONFIGURATION"
        ENV[env_config.py<br/>Credentials]
        ENVFILE[.env file<br/>Secrets]
    end

    subgraph "DATA SOURCES"
        NSE[nse_stocks_650.py<br/>675 stocks]
        YFINANCE[yfinance API<br/>Market data]
        FINBERT[FinBERT Model<br/>AI sentiment]
    end

    subgraph "OUTPUT"
        NOTION[(Notion Database<br/>16 columns)]
        LOGS[Log Files<br/>Monitoring]
        EXCEL[Excel Export<br/>Reports]
    end

    subgraph "MAINTENANCE SCRIPTS"
        CHECK[check_database.py]
        UPDATE[update_prices.py]
        MISSING[load_missing_stocks.py]
    end

    subgraph "SETUP SCRIPTS"
        FRESH[fresh_start.py]
        ADDCOL[add_analyst_columns.py]
        MODELS[setup_models.py]
    end

    subgraph "ANALYSIS SCRIPTS"
        TOP[top_recommendations.py]
        INST[analyze_institutional.py]
        INSPECT[inspect_ranking.py]
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
    CHECK --> NOTION
    UPDATE --> NOTION
    MISSING --> NOTION
    FRESH --> NOTION
    ADDCOL --> NOTION
    TOP --> NOTION
    INST --> NOTION
    INSPECT --> NOTION
    TOP --> EXCEL
    MODELS --> FINBERT
    CHECK --> ENV
    UPDATE --> ENV
    MISSING --> ENV
    FRESH --> ENV
    ADDCOL --> ENV
    TOP --> ENV

    style LITE fill:#90EE90
    style PRO fill:#87CEEB
    style AI fill:#DDA0DD
    style RANK fill:#FFD700
    style NEWS fill:#FFD700
    style ANALYST fill:#FFD700
    style NOTION fill:#FF6B6B
    style ENV fill:#FFA07A
    style ENVFILE fill:#FFA07A""",

    "Data_Flow_Architecture": """flowchart LR
    subgraph "INPUT LAYER"
        A[User Runs Bot]
        B[.env Config]
    end
    subgraph "DATA COLLECTION"
        C[Load 675 NSE Stocks]
        D[Fetch Market Data<br/>yfinance API]
        E[Fetch News<br/>70+ sources]
        F[Fetch Analyst Ratings<br/>50+ analysts]
        G[AI Sentiment<br/>FinBERT]
    end
    subgraph "PROCESSING LAYER"
        H[Calculate Momentum<br/>Volume Surge]
        I[Aggregate News<br/>Deduplicate]
        J[Sentiment Analysis<br/>Keyword/AI]
        K[Calculate Score<br/>Multi-factor]
    end
    subgraph "RANKING ENGINE"
        L[Normalize Metrics<br/>9 factors]
        M[Calculate Composite<br/>Weighted Score]
        N[Rank Stocks<br/>1 to 675]
    end
    subgraph "OUTPUT LAYER"
        O[(Update Notion<br/>16 columns)]
        P[Generate Logs<br/>Success/Fail]
        Q[Excel Export<br/>Optional]
    end
    subgraph "ANALYSIS LAYER"
        R[Top 25 Picks<br/>Strong Buy]
        S[Institutional<br/>Analysis]
        T[Ranking<br/>Insights]
    end
    A --> B
    B --> C
    C --> D
    C --> E
    C --> F
    D --> H
    E --> I
    F --> K
    E --> G
    G --> J
    I --> J
    H --> K
    J --> K
    K --> L
    L --> M
    M --> N
    N --> O
    N --> P
    O --> Q
    O --> R
    O --> S
    O --> T
    style A fill:#90EE90
    style B fill:#FFA07A
    style C fill:#FFD700
    style D fill:#87CEEB
    style E fill:#87CEEB
    style F fill:#87CEEB
    style G fill:#DDA0DD
    style H fill:#FFB6C1
    style I fill:#FFB6C1
    style J fill:#FFB6C1
    style K fill:#FFB6C1
    style L fill:#F0E68C
    style M fill:#F0E68C
    style N fill:#F0E68C
    style O fill:#FF6B6B
    style P fill:#D3D3D3
    style Q fill:#98FB98
    style R fill:#87CEEB
    style S fill:#87CEEB
    style T fill:#87CEEB"""
}

print("🎨 Generating diagram images from Mermaid code...\n")

for name, diagram in diagrams.items():
    print(f"📊 Generating: {name}.png")

    try:
        # Encode diagram to base64
        diagram_bytes = diagram.encode('utf-8')
        base64_encoded = base64.urlsafe_b64encode(diagram_bytes).decode('utf-8')

        # Use mermaid.ink API to generate image
        url = f"https://mermaid.ink/img/{base64_encoded}"

        # Download image
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            # Save image
            output_path = docs_dir / f"{name}.png"
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"   ✅ Saved to: {output_path}")
        else:
            print(f"   ❌ Failed: HTTP {response.status_code}")

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    print()

print("=" * 70)
print("🎉 Image generation complete!")
print("=" * 70)
print(f"\n📁 Images saved to: {docs_dir.absolute()}\n")
print("Generated files:")
for name in diagrams.keys():
    print(f"  ✅ {name}.png")
