"""Type buckets: no folder is named for a kind of file instead of what its files serve.

A folder called `docs`, `assets` or `misc` groups files by type, so the files that change
together for one purpose end up apart. The names are listed in config. A folder is read only from the files in
scope, so one under a path in `[scope] exclude` is never reported.

Exact. Time O(paths), space O(folders).
"""
from __future__ import annotations

from pathlib import Path

from framework.check_api import Finding, files_in_scope

NAME = "type-buckets"
EXACT = True


def check(root: Path, config: dict) -> list[Finding]:
    buckets = set(config.get("type_buckets", {}).get("names", ["docs", "assets", "misc", "utils", "stuff", "other"]))
    folders = {"/".join(path.split("/")[:depth]) for path in files_in_scope(root, config) for depth in range(1, path.count("/") + 1)}
    return [Finding(NAME, folder, 0, f"'{folder.rsplit('/', 1)[-1]}' names a kind of file, not a purpose: group by what the files serve",
                    "warning") for folder in sorted(folders) if folder.rsplit("/", 1)[-1].lower() in buckets]
