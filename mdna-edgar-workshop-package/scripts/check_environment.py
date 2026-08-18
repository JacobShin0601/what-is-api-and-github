#!/usr/bin/env python3
"""Check the local environment for the EDGAR MD&A workshop."""

from __future__ import annotations

import argparse
import importlib.metadata
import os
import platform
import sys
from pathlib import Path


EXPECTED_EDGARTOOLS = "5.49.0"
EXPECTED_TAVILY = "0.7.27"


def row(name: str, ok: bool, detail: str) -> tuple[str, str, str]:
    return name, "PASS" if ok else "FAIL", detail


def optional_row(name: str, configured: bool, required: bool, missing: str) -> tuple[str, str, str]:
    if configured:
        return name, "PASS", "configured (value hidden)"
    return name, "FAIL" if required else "SKIP", missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-tavily", action="store_true")
    parser.add_argument("--require-fred", action="store_true")
    args = parser.parse_args()
    package_root = Path(__file__).resolve().parents[1]
    workspace = package_root / "workspace"
    checks: list[tuple[str, str, str]] = []

    checks.append(
        row(
            "Python",
            sys.version_info >= (3, 10),
            f"{platform.python_version()} · {sys.executable}",
        )
    )

    try:
        edgar_version = importlib.metadata.version("edgartools")
        checks.append(
            row(
                "EdgarTools",
                edgar_version == EXPECTED_EDGARTOOLS,
                f"installed={edgar_version}, expected={EXPECTED_EDGARTOOLS}",
            )
        )
    except importlib.metadata.PackageNotFoundError:
        checks.append(row("EdgarTools", False, "not installed"))

    try:
        tavily_version = importlib.metadata.version("tavily-python")
        checks.append(
            row(
                "Tavily SDK",
                tavily_version == EXPECTED_TAVILY,
                f"installed={tavily_version}, expected={EXPECTED_TAVILY}",
            )
        )
    except importlib.metadata.PackageNotFoundError:
        checks.append(row("Tavily SDK", False, "not installed"))

    identity = os.getenv("SEC_IDENTITY", "").strip()
    checks.append(
        row(
            "SEC identity",
            bool(identity and "@" in identity),
            "configured" if identity else "SEC_IDENTITY is not set",
        )
    )

    checks.append(
        optional_row(
            "Tavily key",
            bool(os.getenv("TAVILY_API_KEY", "").strip()),
            args.require_tavily,
            "TAVILY_API_KEY is not set",
        )
    )
    checks.append(
        optional_row(
            "FRED key",
            bool(os.getenv("FRED_API_KEY", "").strip()),
            args.require_fred,
            "FRED_API_KEY is not set (optional track)",
        )
    )

    checks.append(
        row(
            "Workspace",
            workspace.is_dir() and os.access(workspace, os.W_OK),
            str(workspace),
        )
    )
    checks.append(row("Operating system", True, f"{platform.system()} {platform.release()}"))
    checks.append(row("Architecture", True, platform.machine()))

    widths = [max(len(r[i]) for r in checks + [("Check", "Status", "Detail")]) for i in range(3)]
    header = ("Check", "Status", "Detail")
    print("  ".join(header[i].ljust(widths[i]) for i in range(3)))
    print("  ".join("-" * widths[i] for i in range(3)))
    for check in checks:
        print("  ".join(check[i].ljust(widths[i]) for i in range(3)))

    failed = [name for name, status, _ in checks if status == "FAIL"]
    if failed:
        print(f"\nNOT READY: {', '.join(failed)}")
        return 1

    print("\nREADY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
