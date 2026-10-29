"""Citations: every work cited in the text has one entry in the bibliography, and every entry is cited.

An in-text citation is `Surname Year`, `Surname & Surname Year`, `Surname and Surname Year` or
`Surname et al. Year`, with an optional letter after the year (2008a) and possibly a list of
years for one author (`Kester 2001, 2004`). It matches the
bibliography entry keyed by the first surname and the year, compared without case, accents,
spaces or punctuation. The bibliography is a markdown table whose first column is the key.

An organisation that publishes many pages a year may key them by a title word after the year
instead of a letter (`Microsoft 2026 icons`). The word after the last year joins the key only when
the bibliography holds that longer key, so "Microsoft 2026 recommends" still cites `Microsoft 2026`
([decision 0004](../../decisions/0004-an-organisation-key-may-carry-a-title-word.md)).

An organisation as author ("Ad Hoc Working Group 1987") is found by trying the capitalised
words just before the match; a name written in lower case ("eLife 2020") counts as a
citation only when it matches an entry, and is never reported.

Heuristic: a capitalised word before a year can be a false citation ("Colon Classification
1933"); config lists words that never start one. Time O(text), space O(entries).
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, line_of, matches_any, prose_only

NAME = "citations"
EXACT = False
PARTICLE = r"(?:(?:[Vv]an|[Vv]on|[Dd]e|[Dd]er|[Dd]en|[Dd]u|[Dd]a|[Dd]i|[Dd]os|[Dd]as|[Ee]l|[Ll]e|[Ll]a|[Tt]er|[Tt]en)\s)"
SURNAME = rf"{PARTICLE}*(?:[A-Z][a-z]{{0,3}}\.\s)?[A-ZÀ-Ý][\w'’-]+"
YEAR = r"(?:1[89]|20)\d\d[a-z]?"
LOWERCASE_NAME = re.compile(r"\b([a-z][a-z]*[A-Za-z]*)\s((?:1[89]|20)\d\d[a-z]?)\b")
TITLE_WORD = re.compile(r"[ \t]+([A-Za-z0-9][A-Za-z0-9-]*)")  # "Microsoft 2026 icons"
CITATION = re.compile(rf"\b({SURNAME})(?:\s+(?:et al\.|(?:&|and)\s+{SURNAME}(?:\s[A-ZÀ-Ý][\w'’-]+)?))?,?\s+({YEAR}(?:,\s{YEAR})*)\b")


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
            before = re.findall(r"[A-ZÀ-Ý][\w'’-]*", text[max(0, match.start() - 60):match.start()])[-4:]
            title = TITLE_WORD.match(text, match.end())
            years = re.findall(YEAR, match.group(2))
            for year in years:  # "Kester 2001, 2004" cites two works
                # an organisation: "Ad Hoc Working Group 1987", longest name first
                stems = [normalised("".join(before[-words:]) + surname + year) for words in range(len(before), 0, -1)]
                stems.append(normalised(surname + year))
                titled = [stem + normalised(title.group(1)) for stem in stems] if title and year == years[-1] else []
                key = next((candidate for candidate in titled + stems if candidate in keys), stems[-1])
                cited.add(key)
                if key not in keys and normalised(surname + year.rstrip("abcdefgh")) not in keys:
                    findings.append(Finding(NAME, path, line_of(text, match.start()),
                        f"'{surname} {year}' has no entry in {bibliography}", "warning"))
        cited.update(key for key in (normalised(name + year) for name, year in LOWERCASE_NAME.findall(text)) if key in keys)
    for key, number in sorted(keys.items(), key=lambda item: item[1]):
        if key not in cited:
            findings.append(Finding(NAME, bibliography, number, f"entry '{key}' is cited nowhere", "warning"))
    return findings
