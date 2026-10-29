"""Figure alt: an image's alt text says what it shows, never its file name or a word for its kind.

reader-ergonomics' figure-captions already fails an empty alt text. This check fails the two other failures WCAG
names for an image (W3C 2023e): the file name as the alternative, and a generic word ("diagram", "figure") that
says what the image is, not what it shows.

Exact. Time O(text).
"""
from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any, prose_only

NAME = "figure-alt"
EXACT = True
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)")
GENERIC = {"diagram", "figure", "image", "chart", "graph", "picture", "screenshot", "illustration", "photo", "svg"}


def failure(alt: str, target: str) -> str | None:
    """Why this alt text fails, or None when it does not."""
    words = alt.strip().lower().rstrip(".")
    name = PurePosixPath(target.split("#")[0].split("?")[0]).name.lower()
    if not words:
        return None  # figure-captions reports it
    if words in (name, PurePosixPath(name).stem) or re.fullmatch(r"[\w.\-/]+\.(svg|png|jpe?g|gif|webp)", words):
        return "the alt text is a file name: say what the figure shows"
    if words in GENERIC:
        return f"the alt text '{alt.strip()}' names the kind of image: say what it shows"
    return None


def check(root: Path, config: dict) -> list[Finding]:
    exempt = config.get("figure_alt", {}).get("exempt", [])
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, exempt):
            continue
        text = prose_only((root / path).read_text(encoding="utf-8", errors="replace"))
        for image in IMAGE.finditer(text):
            reason = failure(image.group(1), image.group(2))
            if reason:
                findings.append(Finding(NAME, path, text.count("\n", 0, image.start()) + 1, reason))
    return findings
