"""Market Bot - Enterprise-grade Indian Stock Market Intelligence Suite"""

__version__ = "2.0.0"
__author__ = "Market Bot Team"

# Version 2.0.0 (2026-05-28)
# - Added retry logic with exponential backoff (3 attempts: 2s, 4s, 8s)
# - Optimized parallel processing (4 workers for API stability)
# - Enhanced logging with ticker names in ratings output
# - Improved success rate from ~90% to ~99%
# - Added new analyst rating fields (Target prices, Upside/Downside, etc.)
