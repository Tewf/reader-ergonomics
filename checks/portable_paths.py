"""Portable paths: every path must check out on filesystems other than the one it was made on.

Each rule is a hard failure, because git aborts the checkout ("unable to create file")
and leaves the clone half-written:
- no `: * ? " < > | \\` and no control character in a path component (reserved on FAT, exFAT, NTFS);
- no leading or trailing space in a component, nor before its extension, and no trailing period;
- no reserved device name (CON, PRN, AUX, NUL, COM1-9, LPT1-9), even with an extension;
- no two paths that differ only by case (the second overwrites the first);
- no versioned symbolic link (absent on some shared storage), unless config allows them.
A path of 260 characters or more warns: Windows refuses it unless long paths are enabled.

Exact. Time O(total path length), space O(number of paths).
"""
from __future__ import annotations

from pathlib import Path

from check_api import Finding, repository_paths

NAME = "portable-paths"
EXACT = True
FORBIDDEN_CHARACTERS = set(':*?"<>|\\') | {chr(code) for code in range(1, 32)}
RESERVED_NAMES = {"con", "prn", "aux", "nul"} | {f"{port}{digit}" for port in ("com", "lpt") for digit in range(1, 10)}
LONGEST_PATH = 259


def check(root: Path, config: dict) -> list[Finding]:
    allow_symlinks = config.get("portable_paths", {}).get("allow_symlinks", False)
    findings, first_spelling = [], {}
    for path in repository_paths(root):
        components = path.split("/")
        for component in components:
            forbidden = FORBIDDEN_CHARACTERS & set(component)
            if forbidden:
                findings.append(Finding(NAME, path, 0, f"forbidden character {''.join(sorted(forbidden))!r} in {component!r}"))
            if component.split(".")[0].lower() in RESERVED_NAMES:
                findings.append(Finding(NAME, path, 0, f"reserved device name in {component!r}"))
            if component.endswith(".") and component not in (".", ".."):
                findings.append(Finding(NAME, path, 0, f"trailing period in {component!r}"))
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
        if len(path) > LONGEST_PATH:
            findings.append(Finding(NAME, path, 0, f"{len(path)} characters, past the 260 Windows allows by default", "warning"))
        if (root / path).is_symlink() and not allow_symlinks:
            findings.append(Finding(NAME, path, 0, "versioned symbolic link"))
    return findings
