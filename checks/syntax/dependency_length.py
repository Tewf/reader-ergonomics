"""Short dependencies: no word sits more than `max_distance` words from the word it depends on.

Each sentence is parsed; the distance of a dependency is the number of words between the two
ends, punctuation left out of the count. A sentence whose longest dependency passes the limit
warns, with the two words named.

Two kinds of link are not measured, because the reader holds nothing open across them. A link
between two clauses joined by "and" or set side by side (`conj`, `cc`, `parataxis`) runs from a
complete clause to the next; the parser hangs the second on the first one's verb, so its length
belongs to the annotation, not to the reading. A link across a semicolon or a colon crosses a
clause boundary that the parser joined. The principle names subject and verb, a modifier and
what it modifies, a pronoun and what it refers to; those are still measured.

Exact given the parse; the parse itself is a model. Time O(words).
"""
from __future__ import annotations

from pathlib import Path

from framework.check_api import Finding
from syntax import parser
from syntax.sentences_of import parsed_paragraphs

NAME = "dependency-length"
EXACT = False
TIER = "syntax"
available = parser.available
BETWEEN_CLAUSES = {"conj", "cc", "parataxis"}  # the second clause, its "and", a clause set beside
BOUNDARIES = {";", ":"}


def measured(token, document) -> bool:
    """Whether the link from token to its head holds something open for the reader."""
    if token.dep_ in BETWEEN_CLAUSES:
        return False
    low, high = sorted((token.i, token.head.i))
    return not any(word.text in BOUNDARIES for word in document[low + 1:high])


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("dependency_length", {})
    limit, findings = settings.get("max_distance", 12), []
    for path, line, document in parsed_paragraphs(root, config, settings.get("exempt", [])):
        for sentence in document.sents:
            words = [token for token in sentence if not token.is_punct]
            position = {token.i: index for index, token in enumerate(words)}
            longest = max(((abs(position[token.i] - position[token.head.i]), token) for token in words
                           if token.head.i in position and token.head.i != token.i and measured(token, document)),
                          default=(0, None), key=lambda pair: pair[0])
            if longest[0] > limit:
                token = longest[1]
                findings.append(Finding(NAME, path, line, f"'{token.text}' sits {longest[0]} words from '{token.head.text}', "
                                        f"which it depends on: bring them closer", "warning"))
    return findings
