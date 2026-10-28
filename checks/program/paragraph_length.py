"""Signal the structure: no wall of prose, and no long run without a heading.

A paragraph of more than `max_sentences` sentences warns: parallel items read better as a list,
and a long argument reads better in short blocks. So does a run of more than `max_without_heading`
sentences of prose under one heading; lists, tables and figures do not count toward it.

Heuristic. Time O(text).
"""
from __future__ import annotations

from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any, prose_only
from framework.prose import blocks, sentences

NAME = "paragraph-length"
EXACT = False


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("paragraph_length", {})
    max_sentences, max_run = settings.get("max_sentences", 4), settings.get("max_without_heading", 25)
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, settings.get("exempt", [])):
            continue
        run, run_start = 0, 1
        for block in blocks(prose_only((root / path).read_text(encoding="utf-8", errors="replace"))):
            if block.kind == "heading":
                run, run_start = 0, block.line
                continue
            if block.kind != "paragraph":
                continue  # lists, tables and figures are structure the reader can already see
            count = len(sentences(block.text))
            if count > max_sentences:
                findings.append(Finding(NAME, path, block.line, f"a paragraph of {count} sentences: cut it, or make "
                                        "parallel items a list", "warning"))
            run += count
            if run > max_run:
                findings.append(Finding(NAME, path, run_start, f"more than {max_run} statements under one heading: "
                                        "give the part a structure the reader can see", "warning"))
                run = -10**9  # one finding per run
    return findings
