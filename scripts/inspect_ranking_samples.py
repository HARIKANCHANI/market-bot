"""Inspect sample rankings for LITE, Excel, and PRO bots using the shared ranking engine.

This script runs the core data-collection functions for a small set of large-cap
stocks in each bot, feeds the results into src.core.ranking_engine.rank_stocks,
and prints the resulting Rank and rank_score for comparison.

AI bot is intentionally excluded (heavy FinBERT model).
"""

import os
import sys

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.core.ranking_engine import rank_stocks  # noqa: E402

# Import bots (these will print their own startup banners, which is fine)
from src.bots import market_bot_lite as lite  # noqa: E402
from src.bots import market_bot_excel as excel  # noqa: E402
from src.bots import market_bot_pro as pro  # noqa: E402

SAMPLES = [
    ("RELIANCE", "Large Cap"),
    ("TCS", "Large Cap"),
    ("INFY", "Large Cap"),
    ("HDFCBANK", "Large Cap"),
    ("ICICIBANK", "Large Cap"),
]


def _prepare_common_defaults(d: dict) -> dict:
    """Ensure minimal fields expected by ranking_engine exist.

    We leave institutional_score as None so the engine treats it as neutral
    (50/100) for bots that don't provide institutional data.
    """

    d.setdefault("has_data", True)
    d.setdefault("consensus", "No Consensus")
    d.setdefault("news_sentiment", None)
    d.setdefault("rating_numeric", 0.0)
    d.setdefault("institutional_score", None)
    return d


def run_for_lite():
    all_data = []
    print("\n================ LITE BOT (sample) ================")
    for sym, cap in SAMPLES:
        print(f"[LITE] Collecting {sym} ({cap})...")
        d = lite.get_market_intelligence(sym, cap)
        d = _prepare_common_defaults(d)
        all_data.append(d)

    ranked = rank_stocks(all_data)
    print("\nLITE – ranked sample:")
    for s in ranked:
        print(f"  Rank {s['rank']}: {s['ticker']}  |  rank_score={s['rank_score']}")


def run_for_excel():
    all_data = []
    print("\n================ EXCEL BOT (sample) ================")
    for sym, cap in SAMPLES:
        print(f"[EXCEL] Collecting {sym} ({cap})...")
        d = excel.get_market_intelligence(sym, cap)
        d = _prepare_common_defaults(d)
        all_data.append(d)

    ranked = rank_stocks(all_data)
    print("\nEXCEL – ranked sample:")
    for s in ranked:
        print(f"  Rank {s['rank']}: {s['ticker']}  |  rank_score={s['rank_score']}")


def run_for_pro():
    all_data = []
    print("\n================ PRO BOT (sample) ================")
    for sym, cap in SAMPLES:
        print(f"[PRO] Collecting {sym} ({cap})...")
        d = pro.get_market_data(sym, cap)
        d = _prepare_common_defaults(d)
        all_data.append(d)

    ranked = rank_stocks(all_data)
    print("\nPRO – ranked sample:")
    for s in ranked:
        print(f"  Rank {s['rank']}: {s['ticker']}  |  rank_score={s['rank_score']}")


def main() -> None:
    run_for_lite()
    run_for_excel()
    run_for_pro()


if __name__ == "__main__":
    main()
