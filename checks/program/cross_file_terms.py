"""Short reference distance across files: a term defined in one file is linked where another uses it.

Definitions are found the way define-before-use marks them: a bold term followed by a definition
cue. A file that uses such a term (of at least `min_length` letters), does not define it itself,
and holds no link to the file that does, warns once per term. A term used in more than
`max_files` files is the repository's shared vocabulary rather than a reference, and is skipped,
as is a use in the same folder as the definition: files of one folder are read as a set.

Heuristic. Time O(terms x text), space O(terms).
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, line_of, matches_any, prose_only
from program.defined_before_use import DEFINITION

NAME = "cross-file-terms"
EXACT = False
LINK = re.compile(r"\]\(([^)#\s]+)")


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("cross_file_terms", {})
    min_length, exempt = settings.get("min_length", 6), settings.get("exempt", [])
    texts = {path: prose_only((root / path).read_text(encoding="utf-8", errors="replace"))
             for path in files_in_scope(root, config, MARKDOWN_SUFFIXES) if not matches_any(path, exempt)}
    defined_in = {}
    for path, text in texts.items():
        for match in DEFINITION.finditer(text):
            term = match.group(1).strip().lower()
            if (len(term) >= min_length and term[0].isalpha() and not term.endswith(":")  # "Check:" is a label
                    and term not in settings.get("ignore_terms", [])):
                defined_in.setdefault(term, path)
    pattern = {term: re.compile(rf"(?<![\w*]){re.escape(term)}(?![\w*])", re.IGNORECASE) for term in defined_in}
    spread = {term: sum(1 for text in texts.values() if pattern[term].search(text)) for term in defined_in}
    defined_in = {term: source for term, source in defined_in.items() if spread[term] <= settings.get("max_files", 5)}
    findings = []
    for path, text in texts.items():
        linked = {str((root / path).parent.joinpath(target).resolve().relative_to(root.resolve()))
                  for target in LINK.findall(text) if not target.startswith(("http", "mailto"))
                  and (root / path).parent.joinpath(target).resolve().is_relative_to(root.resolve())}
        own = {match.group(1).strip().lower() for match in DEFINITION.finditer(text)}
        for term, source in defined_in.items():
            if source == path or term in own or source in linked or Path(source).parent == Path(path).parent:
                continue
            use = pattern[term].search(text)
            if use:
                findings.append(Finding(NAME, path, line_of(text, use.start()),
                    f"'{term}' is defined in {source}, which this file does not link to", "warning"))
    return findings
