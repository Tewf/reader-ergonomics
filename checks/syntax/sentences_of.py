"""The parsed paragraphs of the files in scope, shared by the syntax checks. Time O(words).

The parser is English, so a translation named with a language suffix other than English
(README.fr.md) is left out: an English parse of French text measures the parser, not the text.
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, files_in_scope, matches_any, prose_only
from framework.prose import blocks
from syntax import parser

TRANSLATION = re.compile(r"\.(?!en\.)[a-z]{2}\.(?:md|qmd)$")  # README.fr.md, not README.en.md
LINK = re.compile(r"\[([^\]]*)\]\((?:[^()\s]|\([^()\s]*\))*\)")  # balanced ( ) kept, as in references
EMPHASIS = re.compile(r"\*+")


def as_read(text: str) -> str:
    """The paragraph as a reader sees it: link text without its address, bold without its asterisks.

    Left in, `**Claim:**` reaches the parser as asterisks with the colon glued to one of them.
    """
    return EMPHASIS.sub("", LINK.sub(r"\1", text))


def parsed_paragraphs(root: Path, config: dict, exempt: list[str]):
    """(path, line, parsed paragraph) for every prose paragraph in scope."""
    units = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, exempt) or TRANSLATION.search(path):
            continue
        for block in blocks(prose_only((root / path).read_text(encoding="utf-8", errors="replace"))):
            if block.kind == "paragraph":
                units.append((path, block.line, as_read(block.text)))
    return [(path, line, document) for (path, line, _), document in zip(units, parser.parse([text for _, _, text in units]))]
