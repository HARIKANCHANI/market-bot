"""Run only Large Cap stocks through the LITE bot pipeline and send to Notion.

This script reuses the existing LITE bot logic:
- get_market_intelligence (with NSE fallback)
- rank_stocks from src.core.ranking_engine
- send_to_notion from src.bots.market_bot_lite

It is intended for quicker, focused runs when you only want Large Caps
loaded into Notion.
"""

import os
import sys
import time

# Ensure project root on path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from data.nse_stocks_650 import get_all_stocks_with_classification  # noqa: E402
from src.bots.market_bot_lite import (  # noqa: E402
    get_market_intelligence,
    send_to_notion,
    HAS_RANKING_ENGINE,
)
from src.core.ranking_engine import rank_stocks  # noqa: E402


def main() -> None:
    watchlist = get_all_stocks_with_classification()
    large_caps = [(t, cap) for t, cap in watchlist if cap == "Large Cap"]

    print("\n" + "=" * 70)
    print("📈 LITE BOT – LARGE CAP ONLY RUN")
    print("=" * 70)
    print(f"Total Large Cap stocks: {len(large_caps)}")
    print("🏆 Intelligent Multi-Factor Ranking:", "ENABLED" if HAS_RANKING_ENGINE else "DISABLED")
    print("=" * 70 + "\n")

    stats = {
        "total": len(large_caps),
        "processed": 0,
        "errors": 0,
        "success": 0,
    }

    # PHASE 1 – collect data only for Large Caps
    print("\n" + "=" * 70)
    print("📊 PHASE 1: Collecting market intelligence (Large Caps)...")
    print("=" * 70 + "\n")

    all_stocks_data = []
    start_time = time.time()

    for idx, (ticker, cap) in enumerate(large_caps, 1):
        print(f"[{idx}/{len(large_caps)}] 🔍 Analyzing {ticker} ({cap})...")
        try:
            metrics = get_market_intelligence(ticker, cap)
            if metrics:
                all_stocks_data.append(metrics)
                stats["processed"] += 1
            else:
                stats["errors"] += 1
        except Exception as e:  # noqa: BLE001
            print(f"❌ Error processing {ticker}: {e}")
            stats["errors"] += 1

        # Keep it reasonably gentle on APIs
        time.sleep(1)

    # PHASE 2 – ranking
    print("\n" + "=" * 70)
    print("🏆 PHASE 2: Calculating intelligent rankings (Large Caps)...")
    print("=" * 70 + "\n")

    if HAS_RANKING_ENGINE and all_stocks_data:
        ranked_stocks = rank_stocks(all_stocks_data)
        print(f"✅ Ranked {len(ranked_stocks)} Large Cap stocks")
        top_3 = ", ".join([f"{s['ticker']}#{s['rank']}" for s in ranked_stocks[:3]])
        print(f"   🥇 Top 3 Large Caps: {top_3}")
    else:
        print("⚠️  Ranking engine not available or no data - using serial ranking")
        ranked_stocks = all_stocks_data
        for i, stock in enumerate(ranked_stocks, 1):
            stock["rank"] = i

    # PHASE 3 – send to Notion
    print("\n" + "=" * 70)
    print("📤 PHASE 3: Sending Large Cap data to Notion...")
    print("=" * 70 + "\n")

    for stock in ranked_stocks:
        try:
            send_to_notion(stock, rank=stock.get("rank"))
            stats["success"] += 1
            time.sleep(0.5)
        except Exception as e:  # noqa: BLE001
            print(f"❌ Error sending {stock.get('ticker', '?')} to Notion: {e}")

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print("📊 LARGE CAP RUN COMPLETE")
    print("=" * 70)
    print(f"   Total Large Caps: {stats['total']}")
    print(f"   ✅ Processed: {stats['processed']}")
    print(f"   ✅ Sent to Notion: {stats['success']}")
    print(f"   ❌ Errors: {stats['errors']}")
    print(f"   Total Time: {elapsed/60:.1f} minutes")
    print("=" * 70)


if __name__ == "__main__":
    main()
