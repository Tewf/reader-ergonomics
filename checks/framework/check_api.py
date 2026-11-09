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
FENCED_BLOCK = re.compile(r"^(?:[ \t]*>[ \t]?)*(`{3,}|~{3,})[^\n]*\n.*?^(?:[ \t]*>[ \t]?)*\1[`~]*[ \t]*$", re.MULTILINE | re.DOTALL)  # closes on a run at least as long; a fence inside a quote or callout, `> ```\`, counts
INLINE_CODE = re.compile(r"`[^`\n]*`")
DISPLAY_MATH = re.compile(r"\$\$.*?\$\$", re.DOTALL)  # LaTeX display maths, on one line or several
INLINE_MATH = re.compile(r"(?<![\\$])\$(?=\S)(?:[^$\n]*?\S)\$(?!\d)")  # $x$: no space inside the dollars, not a price


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
    """The text with fenced blocks, inline code and LaTeX maths blanked out; line numbers and column positions are
    preserved. A formula is not prose: a sentence check that read it found 40-word sentences and undefined terms in
    the S7 notes of a mathematics vault (2026-11-07)."""
    text = FENCED_BLOCK.sub(lambda match: "\n" * match.group(0).count("\n"), text)
    text = INLINE_CODE.sub(lambda match: " " * len(match.group(0)), text)
    text = DISPLAY_MATH.sub(lambda match: re.sub(r"[^\n]", " ", match.group(0)), text)
    return INLINE_MATH.sub(lambda match: " " * len(match.group(0)), text)


def without_front_matter(text: str) -> str:
    """The text with a leading YAML front matter block blanked; line numbers are preserved.

    The block runs from a first line `---` to the next line `---`. A `---` later in the body is a
    thematic break, and a first `---` that never closes is left alone. Time O(text).
    """
    lines = text.split("\n")
    if lines[0].rstrip() != "---":
        return text
    end = next((index for index in range(1, len(lines)) if lines[index].rstrip() == "---"), None)
    if end is None:
        return text
    return "\n".join([""] * (end + 1) + lines[end + 1:])


HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def without_comments(text: str) -> str:
    """The text with HTML comments blanked: a reader never sees them; line numbers are preserved."""
    return HTML_COMMENT.sub(lambda match: re.sub(r"[^\n]", " ", match.group(0)), text)


DIV_FENCE = re.compile(r"^[ \t]*:{3,}[^\n]*$", re.MULTILINE)


def without_div_fences(text: str) -> str:
    """The text with the marker lines of fenced divs blanked (`::: {.callout-note title="..."}` and the closing
    `:::`): they are markup, and their attributes are not a sentence; line numbers are preserved."""
    return DIV_FENCE.sub(lambda match: " " * len(match.group(0)), text)


def reading_text(text: str) -> str:
    """The prose a sentence-reading check sees: no front matter, no code, no HTML comment, no div marker; line
    numbers are preserved."""
    return without_div_fences(without_comments(prose_only(without_front_matter(text))))


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1
