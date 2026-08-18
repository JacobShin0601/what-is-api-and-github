#!/usr/bin/env python3
"""Collect official macro context from FRED; classify it as context_only."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


FRED_API = "https://api.stlouisfed.org/fred"


def get_json(endpoint: str, params: dict[str, str]) -> dict:
    url = f"{FRED_API}/{endpoint}?{urlencode(params)}"
    request = Request(url, headers={"User-Agent": "MDNA-Evidence-Lab/1.0"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--claim-id", required=True)
    parser.add_argument("--series", default="FEDFUNDS,CPIAUCSL,UNRATE", help="Comma-separated FRED series IDs")
    parser.add_argument("--observation-start", required=True, help="YYYY-MM-DD")
    parser.add_argument("--observation-end", help="YYYY-MM-DD")
    parser.add_argument("--output-root", default="workspace")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    api_key = os.getenv("FRED_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("FRED_API_KEY is not set. Add it to this terminal session and retry.")

    ticker = args.ticker.upper().strip()
    output_dir = Path(args.output_root) / ticker
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "fred_context.json"
    if output_path.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite {output_path}; use --force after review.")

    records = []
    for series_id in [value.strip().upper() for value in args.series.split(",") if value.strip()]:
        common = {"api_key": api_key, "file_type": "json", "series_id": series_id}
        metadata = get_json("series", common).get("seriess", [{}])[0]
        observation_params = {**common, "observation_start": args.observation_start}
        if args.observation_end:
            observation_params["observation_end"] = args.observation_end
        raw_observations = get_json("series/observations", observation_params).get("observations", [])
        observations = [
            {
                "date": row.get("date"),
                "realtime_start": row.get("realtime_start"),
                "realtime_end": row.get("realtime_end"),
                "value": None if row.get("value") == "." else row.get("value"),
            }
            for row in raw_observations
        ]
        records.append(
            {
                "series_id": series_id,
                "title": metadata.get("title"),
                "units": metadata.get("units"),
                "frequency": metadata.get("frequency"),
                "seasonal_adjustment": metadata.get("seasonal_adjustment"),
                "last_updated": metadata.get("last_updated"),
                "evidence_role": "context_only",
                "observations": observations,
            }
        )

    payload = {
        "schema_version": "1.0",
        "ticker": ticker,
        "claim_id": args.claim_id,
        "as_of_date": args.observation_end or datetime.now(timezone.utc).date().isoformat(),
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "warning": "Macro co-movement does not prove company-specific causation.",
        "series": records,
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"WROTE {output_path} ({len(records)} series; API key not stored)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
