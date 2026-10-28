"""Shape conformance: a document declared to be of a shape holds the parts that shape requires.

Config maps file patterns to a shape and lists the headings each shape requires, such as a
note's "Check yourself" (retrieval prompts) or a report's "The plan" (worked examples with
subgoals). A missing part fails. With no shape declared in config, nothing is checked.

Exact. Time O(text).
"""
from __future__ import annotations

from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any
from framework.prose import blocks

NAME = "shape-conformance"
EXACT = True


def check(root: Path, config: dict) -> list[Finding]:
    shapes = config.get("shape_conformance", {}).get("shapes", [])
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        for shape in shapes:
            if not matches_any(path, shape.get("files", [])):
                continue
            headings = [block.text.lower() for block in blocks((root / path).read_text(encoding="utf-8", errors="replace"))
                        if block.kind == "heading"]
            for part in shape.get("required", []):
                if not any(part.lower() in heading for heading in headings):
                    findings.append(Finding(NAME, path, 1, f"a {shape['name']} has no '{part}' heading"))
    return findings
