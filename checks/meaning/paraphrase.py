"""Paraphrase: the same fact said twice in different words, which the word-run duplication check cannot see.

Every paragraph of at least `min_words` words is embedded; two paragraphs in different files
whose similarity reaches `threshold` become a judgment question, the closest pairs first, at most
`max_findings` of them. Identical paragraphs are left to the duplication check.

Semantic, so judgment. Time O(paragraphs squared) for the similarity matrix.
"""
from __future__ import annotations

from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any, prose_only
from framework.prose import blocks
from meaning import embeddings

NAME = "paraphrase"
EXACT = False
TIER = "meaning"
available = embeddings.available


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("paraphrase", {})
    units = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, settings.get("exempt", [])):
            continue
        for block in blocks(prose_only((root / path).read_text(encoding="utf-8", errors="replace"))):
            if block.kind == "paragraph" and len(block.text.split()) >= settings.get("min_words", 15):
                units.append((path, block.line, block.text))
    if len(units) < 2:
        return []
    vectors = embeddings.embed([text for _, _, text in units])
    similarity = vectors @ vectors.T
    pairs = []
    for first in range(len(units)):
        for second in range(first + 1, len(units)):
            same_words = units[first][2].split() == units[second][2].split()  # exact copies are the duplication check's
            if units[first][0] != units[second][0] and not same_words and similarity[first, second] >= settings.get("threshold", 0.9):
                pairs.append((float(similarity[first, second]), first, second))
    pairs.sort(reverse=True)
    return [Finding(NAME, units[first][0], units[first][1], f"says nearly what {units[second][0]} (line {units[second][1]}) "
                    f"says, similarity {score:.2f}: one fact in two places?", "judgment")
            for score, first, second in pairs[:settings.get("max_findings", 20)]]
