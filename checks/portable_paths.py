"""Portable paths: every path must check out on filesystems other than the one it was made on.

Four rules, each a hard failure because git aborts the checkout ("unable to create
file") and leaves the clone half-written:
- no `: * ? " < > | \\` in a path component (reserved on FAT, exFAT and NTFS);
- no leading or trailing space in a component, nor before its extension (silently stripped);
- no two paths that differ only by case (the second overwrites the first);
- no versioned symbolic link (absent on some shared storage), unless config allows them.

Exact. Time O(total path length), space O(number of paths).
"""
from __future__ import annotations

from pathlib import Path

from check_api import Finding, repository_paths

NAME = "portable-paths"
EXACT = True
FORBIDDEN_CHARACTERS = set(':*?"<>|\\')


def check(root: Path, config: dict) -> list[Finding]:
    allow_symlinks = config.get("portable_paths", {}).get("allow_symlinks", False)
    findings, first_spelling = [], {}
    for path in repository_paths(root):
        components = path.split("/")
        for component in components:
            forbidden = FORBIDDEN_CHARACTERS & set(component)
            if forbidden:
                findings.append(Finding(NAME, path, 0, f"forbidden character {''.join(sorted(forbidden))!r} in {component!r}"))
            stem, dot, _ = component.rpartition(".")
            if component != component.strip():
                findings.append(Finding(NAME, path, 0, f"leading or trailing space in {component!r}"))
            elif dot and stem and stem != stem.rstrip():
                findings.append(Finding(NAME, path, 0, f"space before the extension in {component!r}"))
        for depth in range(1, len(components) + 1):
            prefix = "/".join(components[:depth])
            spelling = first_spelling.setdefault(prefix.lower(), prefix)
            if spelling != prefix:
                findings.append(Finding(NAME, path, 0, f"{prefix!r} differs from {spelling!r} only by case"))
                break
        if (root / path).is_symlink() and not allow_symlinks:
            findings.append(Finding(NAME, path, 0, "versioned symbolic link"))
    return findings
