"""Figures present: a long document with no figure, table or diagram is asked whether a relation went undrawn.

A markdown file of at least `min_statements` statements that holds no figure (a fenced block,
an image) and no table becomes a judgment question: relations, sets, quantities and processes
are cheaper to read drawn.

The count is exact; whether a figure is needed is judgment. Time O(text).
"""
from __future__ import annotations

from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any
from framework.prose import blocks
from program.logical_lines import logical_line_count

NAME = "figures-present"
EXACT = True


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("figures_present", {})
    minimum, exempt = settings.get("min_statements", 40), settings.get("exempt", [])
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, exempt):
            continue
        text = (root / path).read_text(encoding="utf-8", errors="replace")
        if logical_line_count(text) >= minimum and not any(block.kind in ("fence", "image", "table") for block in blocks(text)):
            findings.append(Finding(NAME, path, 1, "a long text with no figure, table or diagram: is a relation, set, "
                                    "quantity or process described only in words?", "judgment"))
    return findings
