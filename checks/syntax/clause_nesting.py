"""Shallow nesting: no sentence centre-embeds a clause inside a centre-embedded clause.

Each sentence is parsed; a clause is a token attached as a relative, adverbial, complement or
clausal subject. A clause is centre-embedded when words of the clause around it stand on both
sides of it, as in "the rat that the cat killed ate". The depth of a clause is the number of
centre-embedded clauses on its path to the root, Karlsson's degree of centre-embedding. A clause
at the end of its sentence adds nothing: the principle prefers it, and the evidence (Gibson &
Thomas 1999; Karlsson 2007) is about clauses in the middle. A sentence deeper than `max_depth`
warns.

Exact given the parse; the parse itself is a model. Time O(words x depth x words).
"""
from __future__ import annotations

from pathlib import Path

from framework.check_api import Finding
from syntax import parser
from syntax.dependency_length import BETWEEN_CLAUSES, BOUNDARIES
from syntax.sentences_of import parsed_paragraphs

NAME = "clause-nesting"
EXACT = False
TIER = "syntax"
available = parser.available
CLAUSES = {"relcl", "acl", "advcl", "ccomp", "csubj"}


def enclosing(token):
    """The head of the clause that contains this one: the nearest clause above it, or the root."""
    head = token.head
    while head.head.i != head.i and head.dep_ not in CLAUSES:
        head = head.head
    return head


def centred(token) -> bool:
    """Whether words of the enclosing clause stand on both sides of this clause.

    A clause coordinated with the enclosing one is not part of it, and neither is what follows a
    semicolon or colon after this clause: the enclosing clause has ended there.
    """
    head = enclosing(token)
    inside = {word.i for word in token.subtree}
    apart = {word.i for child in head.children if child.dep_ in BETWEEN_CLAUSES for word in child.subtree}
    stop = next((word.i for word in token.doc[token.right_edge.i + 1:head.right_edge.i + 1] if word.text in BOUNDARIES),
                head.right_edge.i + 1)
    around = [word.i for word in head.subtree if word.i not in inside and word.i not in apart and not word.is_punct
              and word.i < stop]
    return any(i < token.left_edge.i for i in around) and any(i > token.right_edge.i for i in around)


def depth(token) -> int:
    count = 0
    while token.head.i != token.i:
        count += token.dep_ in CLAUSES and centred(token)
        token = token.head
    return count


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("clause_nesting", {})
    limit, findings = settings.get("max_depth", 1), []
    for path, line, document in parsed_paragraphs(root, config, settings.get("exempt", [])):
        for sentence in document.sents:
            deepest = max((depth(token) for token in sentence), default=0)
            if deepest > limit:
                findings.append(Finding(NAME, path, line, f"a sentence centre-embedding clauses {deepest} deep, past {limit}: "
                                        f"split it (\"{sentence.text[:60]} ...\")", "warning"))
    return findings
