"""Typed figure: a figure in a page people read is drawn from a source file, not typed in characters.

A fenced block marked `text` (or `txt`, `plaintext`), or with no language, that holds box-drawing characters
(U+2500 to U+257F) or block arrows is a figure typed in characters. In a page read on GitHub or a site it is drawn
from a Graphviz `.dot` source instead, with the SVG embedded and its source folded under it (the author's
figure rule, 2026-10-29). Files read in a terminal or by a model keep their typed figures: they are listed under `exempt` in config.

Exact for what counts as a typed figure; the rule is a convention, so a warning. Time O(text).
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any

NAME = "typed-figure"
EXACT = True
FENCE = re.compile(r"^(`{3,}|~{3,})[ \t]*([\w-]*)[^\n]*\n(.*?)^\1[`~]*[ \t]*$", re.MULTILINE | re.DOTALL)
FIGURES = {"", "text", "txt", "plaintext"}
DRAWING = re.compile(r"[─-╿▲-◄▶◀]")


def check(root: Path, config: dict) -> list[Finding]:
    exempt = config.get("typed_figure", {}).get("exempt", [])
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if matches_any(path, exempt):
            continue
        text = (root / path).read_text(encoding="utf-8", errors="replace")
        for fence in FENCE.finditer(text):
            if fence.group(2).lower() in FIGURES and DRAWING.search(fence.group(3)):
                findings.append(Finding(NAME, path, text.count("\n", 0, fence.start()) + 1,
                                        "a figure typed in characters: draw it from a .dot source and embed the SVG, "
                                        "or list the file under [typed_figure] exempt if a terminal or a model reads it",
                                        "warning"))
    return findings
