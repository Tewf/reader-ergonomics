"""The interface every check shares: the files in scope, and the finding a check returns.

A check is a module with `NAME`, `EXACT` and `check(root, config) -> list[Finding]`.
`EXACT` is True when a finding is certain (it fails the run) and False for a heuristic
(it warns). Questions a program cannot answer are findings of kind "judgment"; they go
to the backend chosen in config.toml (see judgment.py).
"""
from __future__ import annotations

import fnmatch
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

MARKDOWN_SUFFIXES = {".md", ".qmd"}
FENCED_BLOCK = re.compile(r"^(`{3,}|~{3,})[^\n]*\n.*?^\1[`~]*[ \t]*$", re.MULTILINE | re.DOTALL)  # closes on a run at least as long
INLINE_CODE = re.compile(r"`[^`\n]*`")


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    line: int
    message: str
    kind: str = "error"  # error | warning | judgment


def repository_paths(root: Path) -> list[str]:
    """Every file git would track (tracked, or untracked and not ignored), as POSIX paths.

    Outside a git repository, every non-hidden file under root.
    """
    listing = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        capture_output=True, text=True)
    if listing.returncode == 0:
        return sorted({path for path in listing.stdout.split("\0")
                       if path and ((root / path).exists() or (root / path).is_symlink())})
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*")
                  if path.is_file() and not any(part.startswith(".") for part in path.relative_to(root).parts))


def matches_any(path: str, patterns: list[str]) -> bool:
    """True when path matches a pattern: one ending in "/" covers a folder and all under it; others are globs."""
    for pattern in patterns:
        if pattern.endswith("/"):
            if path == pattern.rstrip("/") or path.startswith(pattern):
                return True
        elif fnmatch.fnmatch(path, pattern):
            return True
    return False


def files_in_scope(root: Path, config: dict, suffixes: set[str] | None = None) -> list[str]:
    excluded = config.get("scope", {}).get("exclude", [])
    return [path for path in repository_paths(root)
            if not matches_any(path, excluded) and (suffixes is None or Path(path).suffix in suffixes)]


def prose_only(text: str) -> str:
    """The text with fenced blocks and inline code blanked out; line numbers are preserved."""
    text = FENCED_BLOCK.sub(lambda match: "\n" * match.group(0).count("\n"), text)
    return INLINE_CODE.sub(lambda match: " " * len(match.group(0)), text)


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1
