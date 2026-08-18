#!/usr/bin/env python3
"""Collect recent company-specific evidence with Tavily; never store the API key."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from tavily import TavilyClient


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", required=True, help="Ticker, e.g. AAPL")
    parser.add_argument("--company", required=True, help="Legal or common company name")
    parser.add_argument("--claim-id", required=True, help="Claim being checked, e.g. C001")
    parser.add_argument("--query", required=True, help="Focused evidence question")
    parser.add_argument("--time-range", choices=("day", "week", "month", "year"), default="month")
    parser.add_argument("--start-date", help="Optional YYYY-MM-DD; overrides time-range")
    parser.add_argument("--end-date", help="Optional YYYY-MM-DD")
    parser.add_argument("--max-results", type=int, choices=range(1, 11), default=5)
    parser.add_argument("--output-root", default="workspace")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    api_key = os.getenv("TAVILY_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("TAVILY_API_KEY is not set. Add it to this terminal session and retry.")

    ticker = args.ticker.upper().strip()
    output_dir = Path(args.output_root) / ticker
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "tavily_evidence.json"
    if output_path.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite {output_path}; use --force after review.")

    search_args: dict[str, object] = {
        "query": f"{args.company} {ticker} {args.query}",
        "topic": "news",
        "search_depth": "basic",
        "max_results": args.max_results,
        "include_answer": False,
    }
    if args.start_date:
        search_args["start_date"] = args.start_date
        if args.end_date:
            search_args["end_date"] = args.end_date
    else:
        search_args["time_range"] = args.time_range

    response = TavilyClient(api_key=api_key).search(**search_args)
    evidence = []
    for index, item in enumerate(response.get("results", []), start=1):
        evidence.append(
            {
                "external_id": f"TV{index:03d}",
                "claim_id": args.claim_id,
                "provider": "Tavily",
                "evidence_role": "unresolved",
                "supports_or_contradicts": "unreviewed",
                "title": item.get("title"),
                "url": item.get("url"),
                "published_date": item.get("published_date"),
                "score": item.get("score"),
                "content": item.get("content"),
            }
        )

    payload = {
        "schema_version": "1.0",
        "ticker": ticker,
        "company": args.company,
        "claim_id": args.claim_id,
        "query": search_args["query"],
        "topic": "news",
        "date_filter": {
            "time_range": None if args.start_date else args.time_range,
            "start_date": args.start_date,
            "end_date": args.end_date,
        },
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "warning": "Search results are discovery evidence, not a substitute for the original source.",
        "results": evidence,
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"WROTE {output_path} ({len(evidence)} results; API key not stored)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
