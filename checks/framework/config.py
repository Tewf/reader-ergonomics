"""The config a check run reads: the repository's own, else the standard's; an extension's is merged onto it."""
from __future__ import annotations

import tomllib
from pathlib import Path

STANDARD = Path(__file__).resolve().parents[1] / "config.toml"


def load_config(root: Path, explicit: Path | None = None) -> dict:
    """The repository's config, else the standard's; a config that extends the standard is merged onto it."""
    standard = STANDARD
    path = explicit or root / "checks" / "config.toml"
    if not path.exists():
        path = standard
    config = tomllib.loads(path.read_text(encoding="utf-8"))
    if config.pop("extends", None) == "reader-ergonomics" and path != standard:
        config = merged(tomllib.loads(standard.read_text(encoding="utf-8")), config)
    return config


def merged(base: dict, extra: dict) -> dict:
    """Tables merge key by key; any other value in the extension replaces the standard's."""
    result = dict(base)
    for key, value in extra.items():
        result[key] = merged(result[key], value) if isinstance(value, dict) and isinstance(result.get(key), dict) else value
    return result
