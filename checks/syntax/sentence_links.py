"""Given before new: each sentence of a paragraph picks up something the one before it gave.

Two consecutive sentences are linked when they share a noun or a name (by lemma), or when the
second opens with a word that points back (it, this, these, they, such). A paragraph of at least
four sentences in which more than `max_unlinked` of the consecutive pairs are unlinked warns:
the reader keeps restarting.

Heuristic, on top of a parse. Time O(words).
"""
from __future__ import annotations

from pathlib import Path

from framework.check_api import Finding
from syntax import parser
from syntax.sentences_of import parsed_paragraphs

NAME = "sentence-links"
EXACT = False
TIER = "syntax"
available = parser.available
POINTERS = {"it", "this", "these", "that", "those", "they", "such", "its", "their"}


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("sentence_links", {})
    findings = []
    for path, line, document in parsed_paragraphs(root, config, settings.get("exempt", [])):
        sentences = list(document.sents)
        if len(sentences) < 4:
            continue
        nouns = [{token.lemma_.lower() for token in sentence if token.pos_ in ("NOUN", "PROPN")} for sentence in sentences]
        unlinked = sum(1 for index in range(1, len(sentences)) if not (nouns[index] & nouns[index - 1])
                       and sentences[index][0].lower_ not in POINTERS)
        share = unlinked / (len(sentences) - 1)
        if share > settings.get("max_unlinked", 0.5):
            findings.append(Finding(NAME, path, line, f"{unlinked} of {len(sentences) - 1} sentences share nothing with the "
                                    "one before: link each to what the reader already has", "warning"))
    return findings
