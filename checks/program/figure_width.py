"""Figure width: a figure drawn in characters stays within `max_columns`, so it fits the column its text fits.

A fenced block marked `text` (or `txt`, `plaintext`), or with no language, is a figure drawn in characters: a tree,
a flow, a map. Past the width of the text around it, a site shows it behind a horizontal scrollbar and a phone cuts it
off, so the reader sees half the relation the figure was drawn to show. A block with a language is code and is left
alone, since code cannot be reflowed. The usual fix keeps the figure: put each node's description on the line under
the node, not beside it. A wide character (CJK) counts as two columns. Written from a check of the presentations
extension, after a figure on the topic extension's front page was cut off on a phone.

Exact for the width; the limit is a convention, PROVISIONAL in config, set at the narrow end of the readable measure
(45 to 75 characters), so a warning. Time O(text).
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any

NAME = "figure-width"
EXACT = False
FENCE = re.compile(r"^(`{3,}|~{3,})[ \t]*([\w-]*)[^\n]*\n(.*?)^\1[`~]*[ \t]*$", re.MULTILINE | re.DOTALL)
FIGURES = {"", "text", "txt", "plaintext"}


def columns(line: str) -> int:
    """The width of a line on a monospace screen: two columns for a wide character, one for any other."""
    return sum(2 if unicodedata.east_asian_width(character) in ("W", "F") else 1 for character in line.rstrip())


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("figure_width", {})
    limit, exempt = settings.get("max_columns", 60), settings.get("exempt", [])
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, exempt):
            continue
        text = (root / path).read_text(encoding="utf-8", errors="replace")
        for fence in FENCE.finditer(text):
            if fence.group(2).lower() not in FIGURES:
                continue
            width = max((columns(line) for line in fence.group(3).splitlines()), default=0)
            if width > limit:
                findings.append(Finding(NAME, path, text.count("\n", 0, fence.start()) + 1,
                                        f"a text figure {width} columns wide, past {limit}: it overflows the column; "
                                        "put each description on the line under its node", "warning"))
    return findings
