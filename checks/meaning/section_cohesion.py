"""Section cohesion: no section of a file is far, in meaning, from all the others.

In a file with at least three sections (level-2 headings) of at least `min_words` words each,
each section is embedded; a section whose closest other section stays under `threshold` becomes
a judgment question: is it a second role, which belongs in a file of its own?

Semantic, so judgment. Time O(sections squared) per file.
"""
from __future__ import annotations

from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any, prose_only
from framework.prose import blocks
from meaning import embeddings

NAME = "section-cohesion"
EXACT = False
TIER = "meaning"
available = embeddings.available


def sections(text: str) -> list[tuple[str, int, str]]:
    found, current = [], None
    for block in blocks(prose_only(text)):
        if block.kind == "heading" and block.info == "2":
            current = [block.text, block.line, []]
            found.append(current)
        elif current is not None and block.kind != "heading":
            current[2].append(block.text)
    return [(heading, line, " ".join(parts)) for heading, line, parts in found]


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("section_cohesion", {})
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, settings.get("exempt", [])):
            continue
        parts = [part for part in sections((root / path).read_text(encoding="utf-8", errors="replace"))
                 if len(part[2].split()) >= settings.get("min_words", 30)]
        if len(parts) < 3:
            continue
        vectors = embeddings.embed([text for _, _, text in parts])
        similarity = vectors @ vectors.T
        for index, (heading, line, _) in enumerate(parts):
            closest = max(float(similarity[index, other]) for other in range(len(parts)) if other != index)
            if closest < settings.get("threshold", 0.25):
                findings.append(Finding(NAME, path, line, f"section '{heading}' is far from every other section "
                                        f"({closest:.2f}): a second role?", "judgment"))
    return findings
