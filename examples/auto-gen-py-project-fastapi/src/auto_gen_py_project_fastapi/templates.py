"""Template root helper for entry-point discovery."""

from __future__ import annotations

from pathlib import Path


def get_root() -> Path:
    return Path(__file__).resolve().parent / "templates"
