#!/usr/bin/env python3
"""Create a local .env from .env.example without overwriting existing values."""

from __future__ import annotations

import shutil
from pathlib import Path


def main() -> int:
    package_root = Path(__file__).resolve().parents[1]
    current_example = Path.cwd() / ".env.example"
    example = current_example if current_example.is_file() else package_root / ".env.example"
    target = example.with_name(".env")

    if not example.is_file():
        print(f"ERROR: .env.example was not found at {example}")
        return 2
    if target.exists():
        print(f"KEEP  {target} (already exists; no values were changed)")
        print("EDIT  that .env file, then run scripts/check_environment.py")
        return 0

    shutil.copyfile(example, target)
    print(f"CREATED {target}")
    print("EDIT    that .env file, then run scripts/check_environment.py")
    print("SAFE    .env is ignored by Git; .env.example contains names/placeholders only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
