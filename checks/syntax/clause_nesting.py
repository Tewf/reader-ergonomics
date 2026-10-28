"""Shallow nesting: no sentence puts a clause inside a clause inside a clause.

Each sentence is parsed; a clause is a token attached as a relative, adverbial, complement or
clausal subject. Its depth is the number of clauses on its path to the root. A sentence deeper
than `max_depth` warns.

Exact given the parse; the parse itself is a model. Time O(words x depth).
"""
from __future__ import annotations

from pathlib import Path

from framework.check_api import Finding
from syntax import parser
from syntax.sentences_of import parsed_paragraphs

NAME = "clause-nesting"
EXACT = False
TIER = "syntax"
available = parser.available
CLAUSES = {"relcl", "acl", "advcl", "ccomp", "csubj"}


def depth(token) -> int:
    count = 0
    while token.head.i != token.i:
        count += token.dep_ in CLAUSES
        token = token.head
    return count


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("clause_nesting", {})
    limit, findings = settings.get("max_depth", 2), []
    for path, line, document in parsed_paragraphs(root, config, settings.get("exempt", [])):
        for sentence in document.sents:
            deepest = max((depth(token) for token in sentence), default=0)
            if deepest > limit:
                findings.append(Finding(NAME, path, line, f"a sentence nesting {deepest} clauses deep, past {limit}: "
                                        f"split it (\"{sentence.text[:60]} ...\")", "warning"))
    return findings
