"""Citations: every work cited in the text has one entry in the bibliography, and every entry is cited.

An in-text citation is `Surname Year`, `Surname & Surname Year`, `Surname and Surname Year` or
`Surname et al. Year`, with an optional letter after the year (2008a) and possibly a list of
years for one author (`Kester 2001, 2004`). It matches the
bibliography entry keyed by the first surname and the year, compared without case, accents,
spaces or punctuation. The bibliography is a markdown table whose first column is the key.

Heuristic: a capitalised word before a year can be a false citation ("Colon Classification
1933"); config lists words that never start one. Time O(text), space O(entries).
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, line_of, matches_any, prose_only

NAME = "citations"
EXACT = False
PARTICLE = r"(?:(?:[Vv]an|[Vv]on|[Dd]e|[Dd]er|[Dd]en|[Dd]u|[Dd]a|[Dd]i|[Dd]os|[Dd]as|[Ee]l|[Ll]e|[Ll]a)\s)"
SURNAME = rf"{PARTICLE}*(?:[A-Z][a-z]{{0,3}}\.\s)?[A-ZÀ-Ý][\w'’-]+"
YEAR = r"(?:1[89]|20)\d\d[a-z]?"
CITATION = re.compile(rf"\b({SURNAME})(?:\s(?:et al\.|(?:&|and)\s{SURNAME}(?:\s[A-ZÀ-Ý][\w'’-]+)?))?,?\s({YEAR}(?:,\s{YEAR})*)\b")


def normalised(key: str) -> str:
    plain = unicodedata.normalize("NFKD", key).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", plain.lower())


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("citations", {})
    bibliography = settings.get("bibliography", "evidence/bibliography.md")
    never_surnames = set(settings.get("not_surnames", []))
    if not (root / bibliography).is_file():
        return []
    keys = {}
    for number, line in enumerate((root / bibliography).read_text(encoding="utf-8").splitlines(), 1):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and len(cells) >= 2 and re.search(r"\d{4}", cells[0]):
            keys.setdefault(normalised(cells[0]), number)
    cited, findings = set(), []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if path == bibliography or not matches_any(path, settings.get("files", ["evidence/", "principles/", "reader-styles/", "shapes/"])):
            continue
        text = prose_only((root / path).read_text(encoding="utf-8", errors="replace"))
        for match in CITATION.finditer(text):
            surname = match.group(1)
            if surname in never_surnames:
                continue
            for year in re.findall(YEAR, match.group(2)):  # "Kester 2001, 2004" cites two works
                key = normalised(surname + year)
                cited.add(key)
                if key not in keys and normalised(surname + year.rstrip("abcdefgh")) not in keys:
                    findings.append(Finding(NAME, path, line_of(text, match.start()),
                        f"'{surname} {year}' has no entry in {bibliography}", "warning"))
    for key, number in sorted(keys.items(), key=lambda item: item[1]):
        if key not in cited:
            findings.append(Finding(NAME, bibliography, number, f"entry '{key}' is cited nowhere", "warning"))
    return findings
