"""Load the first workshop .env found without exposing or overriding values."""

from __future__ import annotations

from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError as exc:  # pragma: no cover - exercised before dependencies exist
    raise SystemExit(
        "python-dotenv is missing. Run: python -m pip install -r requirements.txt"
    ) from exc


def load_workshop_env() -> Path | None:
    package_root = Path(__file__).resolve().parents[1]
    candidates = (
        Path.cwd() / ".env",
        package_root / ".env",
        package_root.parent / ".env",
    )
    for candidate in candidates:
        if candidate.is_file():
            load_dotenv(dotenv_path=candidate, override=False)
            return candidate.resolve()
    return None
