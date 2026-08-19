#!/usr/bin/env python3
"""Extract and validate Item 7 MD&A from the latest two 10-K filings.

The script uses public EdgarTools section access first. If the current parser
detects Item 7 but returns empty text, it records and uses a guarded fallback.
Every output preserves the filing accession number and SEC source URL.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from env_loader import load_workshop_env


MIN_SECTION_CHARS = 3_000
MAX_SECTION_CHARS = 250_000
EXPECTED_EDGARTOOLS = "5.49.0"


@dataclass
class ValidationResult:
    status: str
    checks: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def clean_ticker(value: str) -> str:
    ticker = value.strip().upper()
    if not re.fullmatch(r"[A-Z0-9.-]{1,15}", ticker):
        raise argparse.ArgumentTypeError("ticker must contain only A-Z, 0-9, dot, or hyphen")
    return ticker


def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    text_attr = getattr(value, "text", None)
    if callable(text_attr):
        result = text_attr()
        return result.strip() if isinstance(result, str) else ""
    if isinstance(text_attr, str):
        return text_attr.strip()
    return ""


def regex_fallback(filing_text: str) -> str:
    """Find the strongest Item 7-to-7A candidate in plain filing text."""
    start_pattern = re.compile(
        r"(?im)^[ \t]*item[ \t]+7(?:\.|:|\s|-)+management(?:['’]s)?\s+discussion\s+and\s+analysis"
    )
    end_pattern = re.compile(r"(?im)^[ \t]*item[ \t]+7a(?:\.|:|\s|-)+")
    candidates: list[str] = []

    starts = list(start_pattern.finditer(filing_text))
    ends = list(end_pattern.finditer(filing_text))
    for start in starts:
        end = next((match for match in ends if match.start() > start.start()), None)
        if not end:
            continue
        candidate = filing_text[start.start() : end.start()].strip()
        if MIN_SECTION_CHARS <= len(candidate) <= MAX_SECTION_CHARS:
            candidates.append(candidate)

    if not candidates:
        return ""

    def score(text: str) -> tuple[int, int]:
        topic_hits = sum(
            phrase.lower() in text.lower()
            for phrase in ("results of operations", "liquidity", "financial condition")
        )
        return topic_hits, len(text)

    return max(candidates, key=score)


def extract_section(report: Any, filing: Any) -> tuple[str, str, list[str], dict[str, Any]]:
    warnings: list[str] = []
    metadata: dict[str, Any] = {}

    value = coerce_text(getattr(report, "management_discussion", None))
    if len(value) >= MIN_SECTION_CHARS:
        return value, "TenK.management_discussion", warnings, metadata

    try:
        value = coerce_text(report["Item 7"])
    except Exception as exc:  # library-specific parser errors are recorded
        value = ""
        warnings.append(f"public Item 7 lookup raised {type(exc).__name__}")
    if len(value) >= MIN_SECTION_CHARS:
        return value, "TenK['Item 7']", warnings, metadata

    sections = getattr(report, "sections", None)
    if sections:
        try:
            section = sections.get("part_ii_item_7") if hasattr(sections, "get") else None
            if section is not None:
                metadata = {
                    "section_confidence": getattr(section, "confidence", None),
                    "section_validated": getattr(section, "validated", None),
                    "section_warnings": list(getattr(section, "warnings", []) or []),
                }
        except Exception as exc:
            warnings.append(f"section metadata unavailable: {type(exc).__name__}")

    legacy = getattr(report, "_chunked_document", None)
    if legacy is not None:
        try:
            value = coerce_text(legacy["Item 7"])
        except Exception as exc:
            value = ""
            warnings.append(f"legacy Item 7 fallback raised {type(exc).__name__}")
        if len(value) >= MIN_SECTION_CHARS:
            warnings.append("public section text was empty; guarded legacy fallback used")
            return value, "legacy_chunked_document['Item 7']", warnings, metadata

    try:
        filing_text = filing.text()
        value = regex_fallback(filing_text)
    except Exception as exc:
        value = ""
        warnings.append(f"plain-text fallback raised {type(exc).__name__}")
    if value:
        warnings.append("heuristic plain-text Item 7-to-7A fallback used; manual review required")
        return value, "filing.text() regex Item 7→7A", warnings, metadata

    return "", "not_found", warnings, metadata


def validate_section(text: str, method: str, warnings: list[str]) -> ValidationResult:
    checks: list[dict[str, str]] = []
    severity = "PASS"

    def add(name: str, status: str, detail: str) -> None:
        nonlocal severity
        checks.append({"check": name, "status": status, "detail": detail})
        if status == "FAIL":
            severity = "FAIL"
        elif status == "REVIEW" and severity == "PASS":
            severity = "REVIEW"

    length = len(text)
    add(
        "section length",
        "PASS" if MIN_SECTION_CHARS <= length <= MAX_SECTION_CHARS else "FAIL",
        f"{length:,} characters",
    )

    opening = text[:2_500].lower()
    heading_signal = "management" in opening and "discussion" in opening
    add(
        "MD&A opening",
        "PASS" if heading_signal else "REVIEW",
        "management/discussion signal found" if heading_signal else "confirm the opening in SEC source",
    )

    item_7a_heading = re.search(r"(?im)^[ \t]*item[ \t]+7a(?:\.|:|\s|-)+", text)
    add(
        "Item 7A boundary",
        "FAIL" if item_7a_heading else "PASS",
        "Item 7A heading detected inside extraction" if item_7a_heading else "no Item 7A heading detected",
    )

    item_8_heading = re.search(r"(?im)^[ \t]*item[ \t]+8(?:\.|:|\s|-)+", text)
    add(
        "Item 8 boundary",
        "FAIL" if item_8_heading else "PASS",
        "Item 8 heading detected inside extraction" if item_8_heading else "no Item 8 heading detected",
    )

    body_signal = "results of operations" in text.lower() or "liquidity" in text.lower()
    add(
        "MD&A body",
        "PASS" if body_signal else "REVIEW",
        "results/liquidity discussion found" if body_signal else "confirm substantive MD&A content",
    )

    if method.startswith("filing.text() regex") and severity == "PASS":
        severity = "REVIEW"
        checks.append(
            {
                "check": "fallback method",
                "status": "REVIEW",
                "detail": "heuristic extraction requires manual boundary confirmation",
            }
        )

    return ValidationResult(status=severity, checks=checks, warnings=warnings)


def filing_record(filing: Any, role: str, method: str, validation: ValidationResult, text: str, section_meta: dict[str, Any]) -> dict[str, Any]:
    report_date = getattr(filing, "report_date", None) or getattr(filing, "period_of_report", None)
    return {
        "role": role,
        "company": str(getattr(filing, "company", "")),
        "cik": str(getattr(filing, "cik", "")),
        "form": str(getattr(filing, "form", "")),
        "filing_date": str(getattr(filing, "filing_date", "")),
        "period_of_report": str(report_date or ""),
        "accession_number": str(getattr(filing, "accession_number", "")),
        "sec_filing_url": str(getattr(filing, "homepage_url", "")),
        "extraction_method": method,
        "extracted_characters": len(text),
        "validation_status": validation.status,
        "section_metadata": section_meta,
        "warnings": validation.warnings,
    }


def markdown_document(record: dict[str, Any], text: str) -> str:
    warning_lines = "\n".join(f"> - {warning}" for warning in record["warnings"])
    fallback_notice = ""
    if warning_lines:
        fallback_notice = f"\n> **Extraction note**\n{warning_lines}\n"
    return (
        f"# {record['company']} — {record['role'].title()} MD&A\n\n"
        f"- Form: {record['form']}\n"
        f"- Period of report: {record['period_of_report']}\n"
        f"- Filing date: {record['filing_date']}\n"
        f"- Accession number: `{record['accession_number']}`\n"
        f"- SEC source: {record['sec_filing_url']}\n"
        f"- Extraction method: `{record['extraction_method']}`\n"
        f"- Validation: **{record['validation_status']}**\n"
        f"{fallback_notice}\n"
        f"---\n\n{text.strip()}\n"
    )


def check_markdown(ticker: str, results: list[dict[str, Any]], final_status: str) -> str:
    lines = [
        f"# {ticker} MD&A Extraction Check",
        "",
        f"**Final status: {final_status}**",
        "",
        "| Filing | Check | Status | Detail |",
        "|---|---|---|---|",
    ]
    for result in results:
        role = result["record"]["role"]
        for check in result["validation"]["checks"]:
            detail = check["detail"].replace("|", "\\|")
            lines.append(f"| {role} | {check['check']} | {check['status']} | {detail} |")
        for warning in result["validation"]["warnings"]:
            safe_warning = warning.replace("|", "\\|")
            lines.append(f"| {role} | parser note | NOTE | {safe_warning} |")
    lines.extend(
        [
            "",
            "## Decision rule",
            "",
            "- PASS: Agent Turn 1로 진행 가능",
            "- REVIEW: SEC 원문에서 Item 7 시작·끝을 사람이 확인한 뒤 진행",
            "- FAIL: 분석 중단 후 추출 문제 해결",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    package_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", required=True, type=clean_ticker)
    parser.add_argument(
        "--identity",
        help="SEC identity. Prefer the SEC_IDENTITY environment variable to avoid shell history.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=package_root / "workspace",
        help="Directory that will contain <TICKER>/ outputs.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite generated extraction files.")
    return parser.parse_args()


def main() -> int:
    load_workshop_env()
    args = parse_args()
    identity = (args.identity or os.getenv("SEC_IDENTITY", "")).strip()
    if not identity or "@" not in identity:
        print("ERROR: fill SEC_IDENTITY in .env, then retry", file=sys.stderr)
        return 2

    try:
        version = importlib.metadata.version("edgartools")
        from edgar import Company, set_identity
    except Exception as exc:
        print(f"ERROR: EdgarTools is not ready: {exc}", file=sys.stderr)
        return 2

    if version != EXPECTED_EDGARTOOLS:
        print(
            f"ERROR: this package was tested with edgartools {EXPECTED_EDGARTOOLS}; installed={version}",
            file=sys.stderr,
        )
        return 2

    set_identity(identity)
    ticker_dir = args.output_root.resolve() / args.ticker
    targets = [
        ticker_dir / "filing_manifest.json",
        ticker_dir / "mdna_current.md",
        ticker_dir / "mdna_prior.md",
        ticker_dir / "extraction_check.md",
    ]
    existing = [path for path in targets if path.exists()]
    if existing and not args.force:
        names = ", ".join(path.name for path in existing)
        print(f"ERROR: output exists ({names}). Use --force only after reviewing those files.", file=sys.stderr)
        return 2
    ticker_dir.mkdir(parents=True, exist_ok=True)

    try:
        company = Company(args.ticker)
        filings = company.get_filings(form="10-K", amendments=False)
        if len(filings) < 2:
            raise RuntimeError(f"only {len(filings)} non-amended 10-K filing(s) found")
        selected = sorted([filings[0], filings[1]], key=lambda filing: str(filing.filing_date), reverse=True)
    except Exception as exc:
        print(f"ERROR: could not load filings: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    results: list[dict[str, Any]] = []
    for role, filing in zip(("current", "prior"), selected):
        try:
            report = filing.obj()
            text, method, warnings, section_meta = extract_section(report, filing)
            validation = validate_section(text, method, warnings)
        except Exception as exc:
            text = ""
            method = "error"
            section_meta = {}
            validation = ValidationResult(
                status="FAIL",
                checks=[
                    {
                        "check": "extraction",
                        "status": "FAIL",
                        "detail": f"{type(exc).__name__}: {exc}",
                    }
                ],
            )

        record = filing_record(filing, role, method, validation, text, section_meta)
        results.append(
            {
                "record": record,
                "validation": asdict(validation),
                "text": text,
            }
        )
        if text:
            (ticker_dir / f"mdna_{role}.md").write_text(
                markdown_document(record, text), encoding="utf-8"
            )

    statuses = [item["record"]["validation_status"] for item in results]
    final_status = "FAIL" if "FAIL" in statuses else "REVIEW" if "REVIEW" in statuses else "PASS"
    manifest = {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "ticker": args.ticker,
        "edgartools_version": version,
        "records": [item["record"] for item in results],
        "final_status": final_status,
        "identity_stored": False,
    }
    (ticker_dir / "filing_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ticker_dir / "extraction_check.md").write_text(
        check_markdown(args.ticker, results, final_status), encoding="utf-8"
    )

    print(f"Ticker: {args.ticker}")
    for item in results:
        record = item["record"]
        print(
            f"{record['role']}: {record['period_of_report']} · {record['extracted_characters']:,} chars "
            f"· {record['extraction_method']} · {record['validation_status']}"
        )
    print(f"Final status: {final_status}")
    print(f"Output: {ticker_dir}")
    return 2 if final_status == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
