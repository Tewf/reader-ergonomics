"""Figure source inline: a drawn figure carries its Graphviz source under it, folded, and the copy equals its file.

A figure is shown to be read, not to show its code; but a reader who wants to reuse or change it should find the
source where the figure is, on GitHub as on the site, without searching the repository. So an image `X.svg` with an
`X.dot` beside it is followed by a folded block, `<details>`, holding the source in a fenced `dot` block. The copy is
a second place for one fact, so it must equal the file it copies: a copy that differs is an error, and a figure with
no folded source is a warning. An image with no `.dot` beside it (a photograph, a chart from data) is not checked.
Mohamed's rule for the family's figures, 2026-10-29.

Exact for the comparison; whether a figure needs its source shown is the rule's, not the reader's. Time O(text).
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any

NAME = "figure-source-inline"
EXACT = True
IMAGE = re.compile(r"^!\[[^\]]*\]\(([^)\s#]+\.svg)\)[ \t]*$", re.MULTILINE)
FOLDED = re.compile(r"\s*<details>\s*<summary>[^<]*</summary>\s*```dot[ \t]*\n(.*?)\n```\s*</details>", re.DOTALL)


def check(root: Path, config: dict) -> list[Finding]:
    exempt = config.get("figure_source_inline", {}).get("exempt", [])
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, exempt):
            continue
        text = (root / path).read_text(encoding="utf-8", errors="replace")
        for image in IMAGE.finditer(text):
            dot = ((root / path).parent / image.group(1)).with_suffix(".dot")
            if not dot.is_file():
                continue
            line = text.count("\n", 0, image.start()) + 1
            folded = FOLDED.match(text, image.end())
            if not folded:
                findings.append(Finding(NAME, path, line, f"{image.group(1)} has no folded source under it: add a "
                                        "<details> block with its .dot in a fenced dot block", "warning"))
            elif folded.group(1).strip() != dot.read_text(encoding="utf-8").strip():
                findings.append(Finding(NAME, path, line, f"the source folded under {image.group(1)} differs from "
                                        f"{dot.name}: copy the file into the block again"))
    return findings
