"""Figure next to its text: every image says what it shows, and every drawn figure has words beside it.

An image needs alt text. A figure drawn as a `text` block needs a paragraph or list right before or
right after it, not only headings, so that the words that explain it sit next to it.

Exact for alt text; heuristic for the words beside a figure. Time O(text).
"""
from __future__ import annotations

from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any
from framework.prose import IMAGE, blocks

NAME = "figure-captions"
EXACT = True
WORDS = ("paragraph", "list", "quote", "table")


def check(root: Path, config: dict) -> list[Finding]:
    exempt = config.get("figure_captions", {}).get("exempt", [])
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, exempt):
            continue
        units = blocks((root / path).read_text(encoding="utf-8", errors="replace"))
        for index, block in enumerate(units):
            if block.kind == "image" and not IMAGE.match(block.text).group(1).strip():
                findings.append(Finding(NAME, path, block.line, "an image with no alt text: say what it shows"))
            if block.kind == "fence" and block.info == "text":
                neighbours = [units[index - 1].kind if index else "", units[index + 1].kind if index + 1 < len(units) else ""]
                if not any(kind in WORDS for kind in neighbours):
                    findings.append(Finding(NAME, path, block.line, "a figure with no words right before or after it",
                                            "warning"))
    return findings
