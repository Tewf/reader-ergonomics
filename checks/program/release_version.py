"""Release version: the citation file names the release the changelog ends on, with its date.

A repository that keeps a changelog and a `CITATION.cff` states its release twice: in the changelog's newest heading,
`## [1.19.0] - 2026-10-29`, and in the citation's `version` and `date-released`. A release that updates one and not
the other has a reader cite a version that is not the one they hold. So, when the changelog's newest heading names a
version, the citation's `version`, if it has one, equals it, and its `date-released`, if it has one, equals that
heading's date. A changelog headed by dates alone, or a citation without these fields, is not compared.

Exact for a heading written as Keep a Changelog writes it. Time O(size of the two files).
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import Finding

NAME = "release-version"
EXACT = True
HEADING = re.compile(r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)


def field(text: str, key: str) -> tuple[str, int] | None:
    """A top-level field of the citation file, unquoted, with its line; None when it is absent."""
    match = re.search(rf"^{key}:[ \t]*['\"]?([^'\"\n#]+?)['\"]?[ \t]*(?:#.*)?$", text, re.MULTILINE)
    return (match.group(1), text.count("\n", 0, match.start()) + 1) if match else None


def check(root: Path, config: dict) -> list[Finding]:
    changelog, citation = root / "CHANGELOG.md", root / "CITATION.cff"
    if not (changelog.is_file() and citation.is_file()):
        return []
    newest = HEADING.search(changelog.read_text(encoding="utf-8", errors="replace"))
    if not newest:
        return []
    text = citation.read_text(encoding="utf-8", errors="replace")
    findings = []
    for key, expected in (("version", newest.group(1)), ("date-released", newest.group(2))):
        found = field(text, key)
        if found and found[0] != expected:
            findings.append(Finding(NAME, "CITATION.cff", found[1], f"{key} is {found[0]}, but the changelog's newest "
                                                                     f"release is {expected}: set both in the release commit"))
    return findings
