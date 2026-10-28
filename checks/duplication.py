"""Duplication: the same run of words held in two files means one fact kept in two places.

Prose is normalised (lower case, words only, code removed) and cut into overlapping
windows of `words` words. A window seen in two different files is a copy. One finding is
reported per pair of files, at the first shared window, with the number of shared windows.
A deliberate quotation is exempted by path in config.

Exact for the copy; whether the copy is a fact or a quotation is judgment.
Time O(total words) expected (hashing), space O(total words).
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any, prose_only

NAME = "duplication"
EXACT = True
WORD = re.compile(r"[^\W_]+(?:'[^\W_]+)?")


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("duplication", {})
    size, exempt = settings.get("words", 20), settings.get("exempt", [])
    first_seen = {}
    shared = defaultdict(list)  # (first file, second file) -> [(line in first, line in second)]
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, exempt):
            continue
        words = []  # (word, line)
        for line_number, line in enumerate(prose_only((root / path).read_text(encoding="utf-8", errors="replace")).splitlines(), 1):
            if line.lstrip().startswith("|"):
                continue  # table rows repeat their column labels by design
            words += [(word.lower(), line_number) for word in WORD.findall(line)]
        seen_here = set()
        for start in range(len(words) - size + 1):
            window = tuple(word for word, _ in words[start:start + size])
            if window in seen_here:
                continue
            seen_here.add(window)
            if window in first_seen and first_seen[window][0] != path:
                other, other_line = first_seen[window]
                shared[(other, path)].append((other_line, words[start][1]))
            else:
                first_seen.setdefault(window, (path, words[start][1]))
    return [Finding(NAME, second, pairs[0][1],
                    f"{len(pairs)} runs of {size} words also in {first} (line {pairs[0][0]}): keep the fact in one file and link to it")
            for (first, second), pairs in sorted(shared.items())]
