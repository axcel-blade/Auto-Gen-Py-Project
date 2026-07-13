"""User configuration loading (TOML / YAML / JSON)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Optional

import yaml

from auto_gen_py_project.core.exceptions import ConfigurationError
from auto_gen_py_project.core.models import UserPreferences

CONFIG_FILENAMES = (
    "auto-gen-py-project.toml",
    "auto-gen-py-project.yaml",
    "auto-gen-py-project.yml",
    "auto-gen-py-project.json",
    ".auto-gen-py-project.toml",
    ".auto-gen-py-project.yaml",
    ".auto-gen-py-project.json",
)


def config_search_paths() -> list[Path]:
    home = Path.home()
    cwd = Path.cwd()
    return [
        cwd,
        home / ".config" / "auto-gen-py-project",
        home,
    ]


def find_config_file() -> Optional[Path]:
    for base in config_search_paths():
        for name in CONFIG_FILENAMES:
            candidate = base / name
            if candidate.is_file():
                return candidate
    return None


def _load_raw(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix == ".toml":
        if sys.version_info >= (3, 11):
            import tomllib
        else:
            import tomli as tomllib  # type: ignore[no-redef]
        data = tomllib.loads(text)
    elif suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(text) or {}
    elif suffix == ".json":
        data = json.loads(text)
    else:
        raise ConfigurationError(f"Unsupported config format: {path}")
    if not isinstance(data, dict):
        raise ConfigurationError(f"Config root must be a mapping: {path}")
    # Allow nested under [defaults] / defaults key
    if "defaults" in data and isinstance(data["defaults"], dict):
        merged = {**data["defaults"], **{k: v for k, v in data.items() if k != "defaults"}}
        return merged
    return data


def load_preferences(path: Optional[Path] = None) -> tuple[UserPreferences, Optional[Path]]:
    config_path = path or find_config_file()
    if config_path is None:
        return UserPreferences(), None
    try:
        raw = _load_raw(config_path)
        return UserPreferences.model_validate(raw), config_path
    except Exception as exc:  # noqa: BLE001
        raise ConfigurationError(f"Invalid config {config_path}: {exc}") from exc


def save_preferences(prefs: UserPreferences, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = prefs.model_dump(mode="json")
    suffix = path.suffix.lower()
    if suffix == ".json":
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    elif suffix in {".yaml", ".yml"}:
        path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    else:
        # Minimal TOML writer for flat prefs
        lines = ["# auto-gen-py-project user defaults", "[defaults]"]
        for key, value in payload.items():
            if isinstance(value, bool):
                lines.append(f"{key} = {'true' if value else 'false'}")
            elif isinstance(value, list):
                items = ", ".join(json.dumps(v) for v in value)
                lines.append(f"{key} = [{items}]")
            elif isinstance(value, (int, float)):
                lines.append(f"{key} = {value}")
            elif value is None:
                continue
            else:
                lines.append(f'{key} = "{value}"')
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
