"""Define before use: a term is not used in a file before the line that defines it.

A definition is marked the way the standard asks: the term in bold, followed on the same
line by a definition cue (a colon, "is", "are", "means", "=", or an opening parenthesis).
A term set in bold more than once in a file is a label (**Claim**, **Verdict**), not a definition.
Any earlier plain use of the same term in the file's prose, outside headings, is reported.

Heuristic: bold is also used for emphasis, and a term can be defined in another file.
Time O(terms x text), space O(text).
"""
from __future__ import annotations

import re
from pathlib import Path

from check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, prose_only

NAME = "defined-before-use"
EXACT = False
DEFINITION = re.compile(r"\*\*([^*\n]{3,40}?)\*\*\s*(?::|\(|=|\bis\b|\bare\b|\bmeans\b)")


def check(root: Path, config: dict) -> list[Finding]:
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        lines = prose_only((root / path).read_text(encoding="utf-8", errors="replace")).splitlines()
        body = [(number, line) for number, line in enumerate(lines, 1) if not line.lstrip().startswith("#")]
        defined_at = {}
        for number, line in body:
            for match in DEFINITION.finditer(line):
                term = match.group(1).strip().lower()
                if any(character.isalpha() for character in term):
                    defined_at.setdefault(term, number)
        bold_count = {}
        for _, line in body:
            for bold in re.findall(r"\*\*([^*\n]+?)\*\*", line):
                bold_count[bold.strip().lower()] = bold_count.get(bold.strip().lower(), 0) + 1
        for term, definition_line in defined_at.items():
            if bold_count.get(term, 0) > 1:
                continue
            pattern = re.compile(rf"(?<![\w*]){re.escape(term)}(?![\w*])", re.IGNORECASE)
            earlier = next((number for number, line in body if number < definition_line and pattern.search(line)), None)
            if earlier:
                findings.append(Finding(NAME, path, earlier,
                    f"'{term}' is used here, before its definition on line {definition_line}", "warning"))
    return findings
