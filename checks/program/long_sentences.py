"""Long sentences: a sentence past `max_words` words is the cheap sign of packed information.

Paragraphs and list items are split into sentences; code, tables and figures are left out.
Length is the proxy that needs no model for even information density and short dependencies.

Heuristic. Time O(text).
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any, prose_only
from framework.prose import blocks, sentences

LIST_ITEM_START = re.compile(r"\n(?=\s*(?:[-*+]|\d+[.)]|>)\s)")  # each item of a list is read on its own
NAME = "long-sentences"
EXACT = False


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("long_sentences", {})
    limit, exempt = settings.get("max_words", 35), settings.get("exempt", [])
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, exempt):
            continue
        for block in blocks(prose_only((root / path).read_text(encoding="utf-8", errors="replace"))):
            if block.kind not in ("paragraph", "list", "quote"):
                continue
            units = [block.text] if block.kind == "paragraph" else LIST_ITEM_START.split(block.text)
            for sentence in (part for unit in units for part in sentences(unit.replace("\n", " "))):
                words = len(sentence.split())
                if words > limit:
                    findings.append(Finding(NAME, path, block.line, f"a sentence of {words} words, past {limit}: "
                                            f"split it (\"{' '.join(sentence.split()[:8])} ...\")", "warning"))
    return findings
