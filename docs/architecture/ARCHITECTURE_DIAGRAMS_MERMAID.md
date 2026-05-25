# 🎨 Architecture Diagrams - Mermaid Code
# Market Bot Visual Diagrams

This file contains all the Mermaid diagram definitions. You can:
1. **View in GitHub** - GitHub automatically renders Mermaid diagrams
2. **View in VS Code** - Use Mermaid preview extension
3. **Convert to PNG** - Use https://mermaid.live or https://mermaid.ink
4. **Embed in docs** - Copy code blocks into any Markdown file

---

## Diagram 1: File Relationships & Architecture

Shows how all files connect together, data sources, and outputs.

```mermaid
graph TB
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
    style ENVFILE fill:#FFA07A
```

---

## Diagram 2: Data Flow Architecture

Shows how data flows through the system from input to output.

```mermaid
flowchart LR
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
    style T fill:#87CEEB
```

---

## Diagram 3: Module Hierarchy & Dependencies

Shows the 4-layer architecture and how modules depend on each other.

```mermaid
graph TD
    subgraph "LAYER 1: USER BOTS"
        B1[market_bot_lite.py<br/>Fast: 18-20min]
        B2[market_bot_pro.py<br/>Standard: 30-35min]
        B3[market_bot_ai.py<br/>Deep: 4-5hr]
    end

    subgraph "LAYER 2: CORE ENGINE"
        C1[ranking_engine.py<br/>Intelligent Ranking]
        C2[news_aggregator.py<br/>News Collection]
        C3[analyst_ratings.py<br/>Analyst Data]
    end

    subgraph "LAYER 3: CONFIGURATION"
        D1[env_config.py<br/>Credentials Manager]
        D2[nse_stocks_650.py<br/>Stock Universe]
    end

    subgraph "LAYER 4: EXTERNAL APIS"
        E1[yfinance<br/>Market Data]
        E2[Notion API<br/>Database]
        E3[News APIs<br/>70+ Sources]
        E4[HuggingFace<br/>FinBERT AI]
    end

    subgraph "SUPPORTING SCRIPTS"
        S1[Setup Scripts<br/>fresh_start<br/>add_analyst_columns<br/>setup_models]
        S2[Maintenance Scripts<br/>check_database<br/>update_prices<br/>load_missing_stocks]
        S3[Analysis Scripts<br/>top_recommendations<br/>analyze_institutional<br/>inspect_ranking]
    end

    B1 --> C1
    B1 --> C2
    B1 --> C3
    B2 --> C1
    B2 --> C2
    B2 --> C3
    B3 --> C1
    B3 --> C2
    B3 --> C3
    B3 --> E4

    C1 --> D1
    C2 --> D1
    C3 --> D1
    B1 --> D1
    B2 --> D1
    B3 --> D1

    B1 --> D2
    B2 --> D2
    B3 --> D2

    C2 --> E1
    C3 --> E1
    B1 --> E1
    B2 --> E1
    B3 --> E1

    B1 --> E2
    B2 --> E2
    B3 --> E2
    C1 --> E2

    C2 --> E3

    S1 --> E2
    S1 --> D1
    S2 --> E2
    S2 --> D1
    S3 --> E2
    S3 --> D1

    D1 -.-> |reads| ENV[.env file]

    classDef botClass fill:#90EE90,stroke:#2d5016,stroke-width:3px
    classDef coreClass fill:#FFD700,stroke:#8b7500,stroke-width:2px
    classDef configClass fill:#FFA07A,stroke:#8b4513,stroke-width:2px
    classDef apiClass fill:#87CEEB,stroke:#4682b4,stroke-width:2px
    classDef scriptClass fill:#DDA0DD,stroke:#8b008b,stroke-width:2px
    classDef envClass fill:#FF6B6B,stroke:#8b0000,stroke-width:2px

    class B1,B2,B3 botClass
    class C1,C2,C3 coreClass
    class D1,D2 configClass
    class E1,E2,E3,E4 apiClass
    class S1,S2,S3 scriptClass
    class ENV envClass
```

---

## Diagram 4: User Journey & Recommended Workflow

Shows the recommended path from beginner to expert.

```mermaid
flowchart TD
    START([New User Starts Here]) --> INDEX[Read DOCUMENTATION_INDEX.md<br/>Navigation Hub]

    INDEX --> QUICK[Read QUICK_START_GUIDE.md<br/>10 minutes]

    QUICK --> INSTALL[Install Dependencies<br/>pip install -r requirements.txt]

    INSTALL --> ENV[Configure .env File<br/>Add NOTION_TOKEN & DATABASE_ID]

    ENV --> CHECK{Test Connection}

    CHECK -->|Success| FIRST[Run First Bot<br/>market_bot_lite.py<br/>18-20 min]
    CHECK -->|Failed| TROUBLE[Check CREDENTIALS_MIGRATION_GUIDE.md<br/>Troubleshoot]

    TROUBLE --> ENV

    FIRST --> SUCCESS{Success?}

    SUCCESS -->|Yes| KEEP[Keep QUICK_REFERENCE.md<br/>at Your Desk]
    SUCCESS -->|No| DEBUG[Check Logs & Troubleshooting<br/>Appendix B]

    DEBUG --> FIRST

    KEEP --> DAILY{Daily Use}

    DAILY -->|Morning| LITE[market_bot_lite.py<br/>Before Market Opens]
    DAILY -->|Evening| PRO[market_bot_pro.py<br/>After Market Closes]
    DAILY -->|Weekend| AI[market_bot_ai.py<br/>Deep AI Analysis]

    LITE --> REPORTS[Generate Reports<br/>top_recommendations.py]
    PRO --> REPORTS
    AI --> REPORTS

    REPORTS --> EXPORT[Export to Excel<br/>create_stock_excel.py]

    EXPORT --> ANALYZE[Analyze & Trade<br/>Make Decisions]

    ANALYZE --> MAINTAIN{Maintenance}

    MAINTAIN -->|Daily| HEALTHCHECK[check_database.py<br/>Health Check]
    MAINTAIN -->|As Needed| PRICE[update_prices.py<br/>Price Update Only]
    MAINTAIN -->|Weekly| MISSING[load_missing_stocks.py<br/>Add New Stocks]

    HEALTHCHECK --> DAILY
    PRICE --> DAILY
    MISSING --> DAILY

    KEEP --> EXPLORE{Want to Learn More?}

    EXPLORE -->|Yes| COMPLETE[Read COMPLETE_PYTHON_FILES_DOCUMENTATION.md<br/>Deep Dive]
    EXPLORE -->|Architecture| DIAGRAMS[View Visual Diagrams<br/>Understand System]
    EXPLORE -->|Customize| CODE[Modify Python Files<br/>Customize Weights]

    COMPLETE --> EXPERT([You're an Expert!])
    DIAGRAMS --> EXPERT
    CODE --> EXPERT

    EXPERT --> SCALE{Scale Up?}

    SCALE -->|Docker| DOCKER[Deploy with Docker<br/>Appendix D]
    SCALE -->|Cloud| CLOUD[AWS Lambda / GCP<br/>Appendix D]
    SCALE -->|Parallel| PARALLEL[Parallel Processing<br/>Appendix D]

    style START fill:#90EE90,stroke:#2d5016,stroke-width:3px
    style INDEX fill:#FFD700,stroke:#8b7500,stroke-width:2px
    style QUICK fill:#FFD700,stroke:#8b7500,stroke-width:2px
    style KEEP fill:#87CEEB,stroke:#4682b4,stroke-width:2px
    style FIRST fill:#98FB98,stroke:#2d5016,stroke-width:2px
    style LITE fill:#90EE90,stroke:#2d5016,stroke-width:2px
    style PRO fill:#87CEEB,stroke:#4682b4,stroke-width:2px
    style AI fill:#DDA0DD,stroke:#8b008b,stroke-width:2px
    style EXPERT fill:#FFD700,stroke:#8b7500,stroke-width:3px
    style REPORTS fill:#FFA07A,stroke:#8b4513,stroke-width:2px
    style ANALYZE fill:#FF6B6B,stroke:#8b0000,stroke-width:2px
```

---

## 📝 How to Use These Diagrams

### Option 1: View in GitHub ⭐ EASIEST
- Push this file to GitHub
- GitHub automatically renders Mermaid diagrams
- View directly in your browser

### Option 2: View in VS Code
- Install "Markdown Preview Mermaid Support" extension
- Open this file and press `Ctrl+Shift+V` (Windows) or `Cmd+Shift+V` (Mac)
- See diagrams rendered instantly

### Option 3: Convert to PNG/SVG Images
1. Go to https://mermaid.live
2. Copy/paste any diagram code above
3. Click "Download PNG" or "Download SVG"
4. Save to `docs/` folder

### Option 4: View in Documentation Sites
- Works automatically in: GitLab, Bitbucket, Notion (with plugins)
- Copy/paste code blocks as-is

---

## 🎨 Color Legend

- 🟢 **Green** - User-facing bots/entry points
- 🟡 **Gold** - Core processing modules/important docs
- 🟠 **Orange** - Configuration/credentials
- 🔵 **Blue** - External APIs/data sources/standard operations
- 🟣 **Purple** - AI/Advanced features
- 🔴 **Red** - Database/Output/Critical decisions
- ⚫ **Gray** - Logs/Supporting features

---

**Created**: 2026-05-24
**Total Diagrams**: 4
**Format**: Mermaid (Markdown-compatible)
**Status**: ✅ Ready to use!

**Tip**: For best results, view in GitHub or VS Code with Mermaid extension!

