"""Define before use: a term is not used in a file before the line that defines it.

A definition is marked the way the standard asks: the term in bold, followed on the same
line by a definition cue (a colon, "is", "are", "means", "=", or an opening parenthesis). `[defined_terms] cues`
sets the list for a repository that writes its definitions another way.
A term set in bold more than once in a file is a label (**Claim**, **Verdict**), not a definition.
Any earlier plain use of the same term in the file's prose, outside headings, is reported.
A use in a summary placed above the title is not: an overview names what the document goes on to define, and where
the two principles pull apart, overview first has the stronger grade. Nor is the term inside a link, which points at
its definition, or in the title line of a callout, which is a heading. `[defined_before_use] exempt` leaves files out.

Heuristic: bold is also used for emphasis, and a term can be defined in another file.
Time O(terms x text), space O(text).
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any, reading_text

NAME = "defined-before-use"
EXACT = False
HEADING = re.compile(r"#{1,6}\s")
LINKED = re.compile(r"!?\[\[[^\]\n]*\]\]|\[[^\]\n]*\]\([^)\n]*\)")  # [[a note]] or [a label](its address)
CALLOUT_TITLE = re.compile(r"^(?:\s*>)+\s*\[![A-Za-z-]+\]")  # > [!NOTE] Title
DEFINITION = re.compile(r"\*\*([^*\n]{3,40}?)\*\*\s*(?::|\(|=|\bis\b|\bare\b|\bmeans\b)")
CUES = [":", "(", "=", "is", "are", "means"]


def definition_pattern(config: dict) -> re.Pattern:
    """The pattern of a definition: a bold term followed by one of the cues `[defined_terms] cues` lists.

    A repository whose list items open on a bold label and a colon (`- **Practice**: ...`) drops the colon from the
    list, so that a label is not taken for a defined term. A cue made of letters is matched as a whole word."""
    cues = config.get("defined_terms", {}).get("cues", CUES)
    if list(cues) == CUES:
        return DEFINITION
    parts = [rf"\b{re.escape(cue)}\b" if cue.isalpha() else re.escape(cue) for cue in cues]
    return re.compile(r"\*\*([^*\n]{3,40}?)\*\*\s*(?:" + "|".join(parts) + ")") if parts else re.compile(r"(?!x)x")


def check(root: Path, config: dict) -> list[Finding]:
    findings = []
    exempt = config.get("defined_before_use", {}).get("exempt", [])
    definition = definition_pattern(config)
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, exempt):
            continue
        lines = reading_text((root / path).read_text(encoding="utf-8", errors="replace")).splitlines()
        body = [(number, line) for number, line in enumerate(lines, 1) if not line.lstrip().startswith("#")]
        title = next((number for number, line in enumerate(lines, 1) if HEADING.match(line)), 0)
        defined_at = {}
        for number, line in body:
            for match in definition.finditer(line):
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
            earlier = next((number for number, line in body
                            if title < number < definition_line and not CALLOUT_TITLE.match(line)
                            and pattern.search(LINKED.sub(" ", line))), None)
            if earlier:
                findings.append(Finding(NAME, path, earlier,
                    f"'{term}' is used here, before its definition on line {definition_line}", "warning"))
    return findings
