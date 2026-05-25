# 📚 Market Bot Documentation Hub

Welcome to the comprehensive documentation for the Market Bot - Enterprise-Grade Indian Stock Market Intelligence Suite.

---

## 🚀 Quick Navigation

### New Users - Start Here!
- **[Getting Started Guide](./getting-started/QUICK_START.md)** - Installation and first run
- **[Quick Reference](./reference/QUICK_REFERENCE.md)** - Command cheat sheet

### Bot Usage Guides
- **[Bot Usage Documentation](./guides/bot-usage/)** - How to use all 7 bot versions
- **[Features Guide](./guides/features/)** - Ranking, ticker mapping, sector validation
- **[Testing Guide](./guides/testing/)** - Test individual stocks

### Technical Documentation
- **[Technical Documentation](./technical/TECHNICAL_DOCUMENTATION.md)** - Complete API reference
- **[Code Documentation](./technical/CODE_DOCUMENTATION.md)** - All Python files documented
- **[Database Schema](./technical/DATABASE_SCHEMA.md)** - Notion database structure

### Architecture & Design
- **[Architecture Diagrams](./architecture/ARCHITECTURE_DIAGRAMS.md)** - System design
- **[Data Flow](./architecture/DATA_FLOW_DETAILED.md)** - How data moves through the system
- **[Folder Structure](./architecture/FOLDER_STRUCTURE.md)** - Project organization

### Performance & Optimization
- **[Optimization Guide](./optimization/README.md)** - 7-11x speedup details
- **[Parallel Processing](./optimization/PARALLEL_PROCESSING.md)** - ThreadPool implementation

### Deployment & Production
- **[Production Deployment](./deployment/PRODUCTION_READY.md)** - Deploy to production
- **[GitHub Setup](./deployment/GITHUB_PUSH_QUICK_GUIDE.md)** - Version control setup
- **[Credentials Migration](./deployment/CREDENTIALS_MIGRATION_GUIDE.md)** - Env config

### Maintenance & Troubleshooting
- **[Dependency Management](./maintenance/DEPENDENCY_AUDIT_COMPLETE.md)** - Keep dependencies updated
- **[Link Checking](./maintenance/LINK_AUDIT_COMPLETE.md)** - Verify documentation links

---

## 📖 Documentation Structure

```
docs/
├── getting-started/        # New user onboarding
├── guides/
│   ├── bot-usage/         # Using the 7 bot versions
│   ├── features/          # Ranking, mapping, validation
│   └── testing/           # Testing tools
├── architecture/          # System design & diagrams
├── technical/             # API reference & code docs
├── optimization/          # Performance optimization
├── deployment/            # Production deployment
├── maintenance/           # Ongoing maintenance
├── reports/               # Historical reports & audits
└── reference/             # Quick reference guides
```

---

## 🎯 Common Tasks

### Running Your First Bot
1. Read [Quick Start Guide](./getting-started/QUICK_START.md)
2. Choose a bot from [Bot Usage Guide](./guides/bot-usage/INCREMENTAL_BOTS_GUIDE.md)
3. Run: `python -m src.bots.market_bot_lite`

### Understanding the System
1. Review [Architecture Diagrams](./architecture/ARCHITECTURE_DIAGRAMS.md)
2. Check [Data Flow](./architecture/DATA_FLOW_DETAILED.md)
3. See [Technical Documentation](./technical/TECHNICAL_DOCUMENTATION.md)

### Optimizing Performance
1. Read [Optimization Guide](./optimization/README.md)
2. Review [Parallel Processing Details](./optimization/PARALLEL_PROCESSING.md)
3. Check performance metrics and benchmarks

### Deploying to Production
1. Follow [Production Ready Guide](./deployment/PRODUCTION_READY.md)
2. Set up [GitHub Integration](./deployment/GITHUB_PUSH_QUICK_GUIDE.md)
3. Configure [CI/CD](./deployment/GITHUB_ACTIONS_GUIDE.md)

---

## 📊 Key Features

- **7 Bot Versions:** Lite, AI, Pro, Excel, and incremental variants
- **906 NSE Stocks:** Nifty 150 + Midcap 200 + Smallcap 300
- **AI Sentiment:** FinBERT-powered analysis
- **70+ News Sources:** Comprehensive aggregation
- **Intelligent Ranking:** Multi-factor scoring system
- **Real-time Data:** Live prices and momentum analysis
- **Notion Integration:** Automatic database updates
- **Production-Ready:** 7-11x optimized performance

---

## 🔧 Technical Highlights

- **Parallel Processing:** 12 concurrent workers
- **Thread-Safe:** Proper locking mechanisms
- **Error Handling:** Comprehensive exception management
- **Logging:** Centralized logging system
- **Smart Filtering:** Auto-removes delisted stocks
- **Ticker Mapping:** Handles company renames
- **Sector Validation:** 52 sectors + fallbacks

---

## 📚 Documentation Categories

### 1. Getting Started (New Users)
Essential guides for first-time users and initial setup.

### 2. Guides (How-To)
Step-by-step instructions for common tasks and features.

### 3. Architecture (System Design)
High-level system design, data flow, and structure diagrams.

### 4. Technical (Developers)
Detailed API reference, code documentation, and database schemas.

### 5. Optimization (Performance)
Performance tuning, parallel processing, and optimization results.

### 6. Deployment (Production)
Production deployment, GitHub setup, and CI/CD configuration.

### 7. Maintenance (Ongoing)
Dependency management, troubleshooting, and upkeep tasks.

### 8. Reports (Historical)
Audit reports, test summaries, and verification results.

### 9. Reference (Quick Lookup)
Quick reference cards, sector mappings, and command cheat sheets.

---

## 🎓 Learning Paths

### Path 1: Complete Beginner
1. Getting Started → Quick Start
2. Guides → Bot Usage → Lite Bot
3. Reference → Quick Reference

### Path 2: Advanced User
1. Technical → Technical Documentation
2. Architecture → System Design
3. Optimization → Performance Tuning

### Path 3: Developer/Contributor
1. Technical → Code Documentation
2. Architecture → Data Flow
3. Maintenance → Development Setup

---

## 🔗 External Resources

- [Python 3.8+ Documentation](https://docs.python.org/3/)
- [yfinance API](https://github.com/ranaroussi/yfinance)
- [Notion API](https://developers.notion.com/)
- [FinBERT Model](https://huggingface.co/ProsusAI/finbert)

---

## 📞 Support & Contributing

- **Issues:** Check troubleshooting guides in maintenance/
- **Updates:** See reports/ for latest changes
- **Contributing:** Follow code documentation standards

---

**Last Updated:** 2026-05-25  
**Version:** 2.0 - Fully Organized Documentation  
**Status:** ✅ Production Ready
