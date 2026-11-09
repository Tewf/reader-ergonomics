"""Overview first: a long document opens with what it is and how it is organised, not with a heading.

In a markdown file of at least `min_statements` statements, the block right after the title must
be a paragraph, a list, a quote, a table or a figure: a sentence or a map of the parts. A second
heading straight after the title means the reader starts in the detail. A document that puts such a
block before its title, a summary above the heading, already opens with it and is not flagged.

Heuristic (the opening may be there and still not be an overview). Time O(text).
"""
from __future__ import annotations

from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any
from framework.prose import blocks
from program.logical_lines import logical_line_count

NAME = "overview-first"
EXACT = False


def opens(block) -> bool:
    """True for a block a reader can open on: prose, a list, a quote, a table or a figure, not a bare rule."""
    return block.kind in {"paragraph", "list", "quote", "table", "image", "embed"} and bool(block.text.strip("-*_ \n"))


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("overview_first", {})
    minimum, exempt = settings.get("min_statements", 20), settings.get("exempt", [])
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, exempt):
            continue
        text = (root / path).read_text(encoding="utf-8", errors="replace")
        if logical_line_count(text) < minimum:
            continue
        units = blocks(text)
        first_heading = next((index for index, block in enumerate(units) if block.kind == "heading"), None)
        if first_heading is not None and any(opens(block) for block in units[:first_heading]):
            continue  # a summary stands above the title
        if first_heading is not None and first_heading + 1 < len(units) and units[first_heading + 1].kind == "heading":
            findings.append(Finding(NAME, path, units[first_heading + 1].line,
                "the title is followed by another heading: open with what the document is and how it is organised",
                "warning"))
    return findings
