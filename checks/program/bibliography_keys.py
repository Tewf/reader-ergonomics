"""Bibliography keys: a key names one work, and a work carries one key, in the bibliography and across its family.

A row of the bibliography (the table `Key | Citation | Link`) names its work by its link: the DOI, else the arXiv id
without its version, else the address without its scheme, `www.`, fragment or trailing slash. A DOI or arXiv id named
in the citation too (a preprint beside its journal version) is the same work, so two rows that share any identifier
name one work. Keys are compared as `citations` compares them, without case, accents, spaces or punctuation.

In the file, a key held twice is an error: a citation cannot say which row it means. A work held under two keys is a
warning. `family` in config names the repositories that share one set of keys with this one, as folders beside it;
each is read at the same bibliography path. This standard names none, so it never reads an extension
([decision 0003](../../decisions/0003-one-key-one-work-across-the-family.md)). Against the family, a key that another
repository gives another work, or a work it gives another key, is a warning reported at the row in this
repository's bibliography; a pair between two other repositories is theirs to report. A family member that is not
found is a warning, so a comparison is never passed over unread. `shared_links` lists the links that more than one
work carries on purpose: two editions on their author's page, a book and its author's site.

Exact for a key held twice in one file. Heuristic otherwise: one work at two addresses reads as two works, and a
work cited by a DOI in one row and by its preprint in another is seen as one only when a row names both.
Time O(rows of the family), space O(rows of the family).
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import Finding
from program.citations import normalised
from program.references import ARXIV, DOI, URL

NAME = "bibliography-keys"
EXACT = True


def work(link: str) -> str:
    """The identity of the work a link names: a DOI, an arXiv id, or a normalised address; empty when there is none."""
    if doi := DOI.search(link):
        return "doi:" + doi.group(1).rstrip(".").lower()
    if arxiv := ARXIV.search(link):
        return "arxiv:" + arxiv.group(1).lower()
    address = url.group(0) if (url := URL.search(link)) else link
    return re.sub(r"^(?:https?://)?(?:www\.)?", "", address.strip().lower()).split("#")[0].rstrip("/.")


def identities(citation: str, link: str) -> tuple[str, ...]:
    """Every identifier a row names: its link's first, then each DOI or arXiv id in its citation."""
    named = [work(link)] + sorted({"doi:" + found.group(1).rstrip(".").lower() for found in DOI.finditer(citation)}
                                  | {"arxiv:" + found.group(1).lower() for found in ARXIV.finditer(citation)})
    return tuple(dict.fromkeys(identity for identity in named if identity))


def rows(path: Path) -> list[tuple[str, tuple[str, ...], int]]:
    """(key, identities, line) for every row of a bibliography table whose first cell holds a year."""
    found = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and len(cells) >= 3 and re.search(r"\d{4}", cells[0]):
            found.append((cells[0], identities(" ".join(cells[1:-1]), cells[-1]), number))
    return found


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("bibliography_keys", {})
    bibliography = config.get("citations", {}).get("bibliography", "evidence/bibliography.md")
    if not (root / bibliography).is_file():
        return []
    shared = {work(link) for link in settings.get("shared_links", [])}
    own, findings = rows(root / bibliography), []
    first_key, first_work = {}, {}
    for key, named, number in own:
        if normalised(key) in first_key:
            findings.append(Finding(NAME, bibliography, number,
                                    f"key '{key}' is also the key of line {first_key[normalised(key)]}: a citation cannot say which it means"))
        first_key.setdefault(normalised(key), number)
        for identity in (identity for identity in named if identity not in shared):
            if identity in first_work and normalised(first_work[identity][0]) != normalised(key):
                other, line = first_work[identity]
                findings.append(Finding(NAME, bibliography, number,
                                        f"'{key}' and '{other}' (line {line}) name one work, {identity}: give it one key", "warning"))
                break
        for identity in named:
            first_work.setdefault(identity, (key, number))
    for name in settings.get("family", []):
        folder = root.resolve().parent / name
        if folder == root.resolve():
            continue
        if not (folder / bibliography).is_file():
            findings.append(Finding(NAME, bibliography, 0, f"family member '{name}' has no {bibliography} beside this "
                                    "repository: its keys were not compared", "warning"))
            continue
        keys, works = {}, {}
        for key, named, number in rows(folder / bibliography):
            keys.setdefault(normalised(key), []).append((named, number))
            for identity in named:
                works.setdefault(identity, []).append((key, number))
        for key, named, number in own:
            for theirs, line in keys.get(normalised(key), []):
                if named and theirs and not set(named) & set(theirs):
                    findings.append(Finding(NAME, bibliography, number, f"'{key}' names another work in {name} "
                                            f"(line {line}, {theirs[0]}): one key, one work across the family", "warning"))
            reported = set()
            for identity in (identity for identity in named if identity not in shared):
                for theirs, line in works.get(identity, []):
                    if normalised(theirs) != normalised(key) and line not in reported:
                        reported.add(line)
                        findings.append(Finding(NAME, bibliography, number, f"'{key}' is '{theirs}' in {name} (line "
                                                f"{line}, {identity}): one work, one key across the family", "warning"))
    return findings
