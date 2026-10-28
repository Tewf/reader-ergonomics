"""Document mode: a long page leans clearly to one of the four modes of documentation.

The opening of each page of at least `min_statements` statements is compared with a description
of each mode (tutorial, how-to, reference, explanation). When the two closest modes are within
`margin` of each other, the page becomes a judgment question: does it mix two modes?

Semantic, so judgment. Time O(pages).
"""
from __future__ import annotations

from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any, prose_only
from meaning import embeddings
from program.logical_lines import logical_line_count

NAME = "document-mode"
EXACT = False
TIER = "meaning"
available = embeddings.available
MODES = {
    "tutorial": "A lesson that takes a beginner through doing something, step by step, to learn by doing it.",
    "how-to": "Directions for accomplishing one specific task, for a reader who already knows the basics.",
    "reference": "Facts to look up: a description of what each thing is, in lists, tables and definitions.",
    "explanation": "A discussion of why things are as they are: background, reasons, evidence and trade-offs.",
}


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("document_mode", {})
    pages = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        text = (root / path).read_text(encoding="utf-8", errors="replace")
        if not matches_any(path, settings.get("exempt", [])) and logical_line_count(text) >= settings.get("min_statements", 20):
            pages.append((path, prose_only(text)[:1500]))
    if not pages:
        return []
    names = list(MODES)
    mode_vectors = embeddings.embed(list(MODES.values()))
    page_vectors = embeddings.embed([opening for _, opening in pages])
    findings = []
    for (path, _), scores in zip(pages, page_vectors @ mode_vectors.T):
        ranked = sorted(range(len(names)), key=lambda index: -scores[index])
        if scores[ranked[0]] - scores[ranked[1]] < settings.get("margin", 0.02):
            findings.append(Finding(NAME, path, 1, f"reads about equally as {names[ranked[0]]} and {names[ranked[1]]}: "
                                    "one mode per document?", "judgment"))
    return findings
