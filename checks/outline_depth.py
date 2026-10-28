"""Outline depth: a document's headings stay within three levels.

The title is level 1, sections and subsections are levels 2 and 3. A heading at level 4 is a
part that has grown into a document of its own. Fenced code is ignored.

The count is exact; the limit of three is a convention, so a deeper heading warns.
Time O(text), space O(1) per file.
"""
from __future__ import annotations

import re
from pathlib import Path

from check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, line_of, matches_any, prose_only

NAME = "outline-depth"
EXACT = True
HEADING = re.compile(r"^(#{1,6})\s+\S", re.MULTILINE)


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("outline_depth", {})
    limit, exempt = settings.get("max_level", 3), settings.get("exempt", [])
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, exempt):
            continue
        text = prose_only((root / path).read_text(encoding="utf-8", errors="replace"))
        for match in HEADING.finditer(text):
            if len(match.group(1)) > limit:
                findings.append(Finding(NAME, path, line_of(text, match.start()),
                    f"heading at level {len(match.group(1))}, past {limit}: make the part a document of its own, "
                    "or flatten it", "warning"))
    return findings
