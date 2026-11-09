"""Duplication: the same run of words held in two files means one fact kept in two places.

Prose is normalised (lower case, words only, code and link addresses removed) and cut into overlapping
windows of `words` words. A window seen in two different files is a copy. One finding is
reported per pair of files, at the first shared window, with the number of shared windows.
Headings and table rows are skipped: they are the skeleton files of one kind share. So are a heading or a table row
inside a quote, the title line of a callout (`> [!NOTE] Title`), and a leading YAML front matter block, which holds
metadata such as tags, not prose.
In a file that declares a shape (a line labelled `Shape:` that links the shape), every line that appears verbatim,
after whitespace normalisation, in a fenced block under the shape's "Skeleton" heading is skipped too (also the text of
a skeleton line before its first run of two spaces, where the shape writes a comment): headings, labels and pointer lines
that the shape prescribes are not a fact held many times. The shape file is read from disk only: a relative link is
resolved against the file; a github.com link is resolved in this repository when it names it, or in a sibling checkout
beside it (`../<repository>/<path>`), never over the network. When the shape cannot be read (no link, no such file, no
Skeleton block), nothing is skipped and the file counts as before.
A deliberate quotation is exempted by path in config.

Exact for the copy; whether the copy is a fact or a quotation is judgment.
Time O(total words) expected (hashing), space O(total words).
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any, prose_only, reading_text

NAME = "duplication"
EXACT = True
WORD = re.compile(r"[^\W_]+(?:'[^\W_]+)?")
LINK_TARGET = re.compile(r"\]\(<[^>\n]*>\)|\]\([^)]*\)|https?://\S+")  # addresses are not prose; one in <...> may hold parentheses
SHAPE_LINE = re.compile(r"\bshape\s*:", re.IGNORECASE)
LINK = re.compile(r"\[[^\]]*\]\(([^)\s#]+)(?:#[^)\s]*)?\)")
GITHUB = re.compile(r"^https?://github\.com/[^/]+/([^/]+)/blob/[^/]+/(.+)$")
SKELETON_HEADING = re.compile(r"^#{1,6}\s+.*skeleton", re.IGNORECASE)
QUOTE_PREFIX = re.compile(r"^(?:\s*>)+\s?")  # a line inside a quote or a callout, at any depth
CALLOUT_TITLE = re.compile(r"^\s*\[![A-Za-z-]+\][+-]?")  # > [!NOTE] Title: the label of a callout or an alert


def squash(line: str) -> str:
    return " ".join(line.split())


def shape_file(root: Path, path: str) -> Path | None:
    """The file of the shape a document declares, found on disk only; None when it cannot be read."""
    text = prose_only((root / path).read_text(encoding="utf-8", errors="replace"))
    for line in text.splitlines():
        if not SHAPE_LINE.search(line):
            continue
        for target in LINK.findall(line):
            github = GITHUB.match(target)
            if github:
                repository, inside = github.groups()
                base = root if repository == root.name else root.parent / repository
                candidate = base / inside
            elif re.match(r"^[a-z]+:", target) or target.startswith("/"):
                continue
            else:
                candidate = (root / path).parent / target
            if candidate.is_file():
                return candidate
    return None


def skeleton_lines(shape: Path) -> set[str]:
    """The squashed lines of the fenced blocks under a heading naming the skeleton."""
    lines, inside, fenced, found = shape.read_text(encoding="utf-8", errors="replace").splitlines(), False, False, set()
    for line in lines:
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif fenced and inside:
            found.add(squash(line))
            found.add(squash(re.split(r"\s{2,}", line.strip())[0]))
        elif not fenced:
            inside = bool(SKELETON_HEADING.match(line)) or (inside and not line.startswith("#"))
    found.discard("")
    return found


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("duplication", {})
    size, exempt = settings.get("words", 20), settings.get("exempt", [])
    first_seen = {}
    shared = defaultdict(list)  # (first file, second file) -> [(line in first, line in second)]
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, exempt):
            continue
        words = []  # (word, line)
        raw = (root / path).read_text(encoding="utf-8", errors="replace")
        shape = shape_file(root, path)
        prescribed = skeleton_lines(shape) if shape else set()
        for line_number, (line, original) in enumerate(zip(reading_text(raw).splitlines(), raw.splitlines()), 1):
            inner = QUOTE_PREFIX.sub("", line)
            if inner.lstrip().startswith(("|", "#")) or CALLOUT_TITLE.match(inner) or squash(original) in prescribed:
                continue  # table rows, headings, callout titles and the lines a declared shape prescribes: the skeleton files of a kind share
            words += [(word.lower(), line_number) for word in WORD.findall(LINK_TARGET.sub("]", line))]
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
