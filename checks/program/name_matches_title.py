"""Names predict content: the words of a file's name appear in its title or opening.

For a markdown file, the words of its name (a README takes its folder's name) are looked for in
its title and first 300 characters, ignoring short words and case, and matching a word by its
first five letters so that "folders" finds "folder". Fewer than half found warns.

Heuristic. Time O(text), space O(1) per file.
"""
from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any, prose_only
from framework.prose import title

NAME = "name-matches-title"
EXACT = False
SKIPPED_STEMS = {"readme", "index", "agents", "license", "changelog"}


def name_words(path: str) -> list[str]:
    pure = PurePosixPath(path)
    base = pure.name.split(".")[0]  # README.fr.md is a README
    stem = pure.parent.name if base.lower() in ("readme", "index") else base
    return [word for word in re.split(r"[-_. ]+", stem.lower()) if len(word) >= 4]


def check(root: Path, config: dict) -> list[Finding]:
    exempt = config.get("name_matches_title", {}).get("exempt", [])
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        stem = PurePosixPath(path).name.split(".")[0].lower()
        if matches_any(path, exempt) or (stem in SKIPPED_STEMS and "/" not in path):
            continue
        words = name_words(path)
        if not words:
            continue
        text = (root / path).read_text(encoding="utf-8", errors="replace")
        opening = (title(text) + " " + prose_only(text)[:300]).lower()
        found = [word for word in words if word[:5] in opening]
        if len(found) * 2 < len(words):
            findings.append(Finding(NAME, path, 1, f"the name's words {words} barely appear in the title or opening: "
                                    "rename the file, or say in its first lines what it holds", "warning"))
    return findings
