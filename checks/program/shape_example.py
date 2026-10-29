"""Shape example: a shape links at least one filled example of itself, and the example links back to the shape.

A shape teaches a writer a method: how to write one kind of document. Worked examples beat problem solving for
novices (reader-ergonomics, worked examples with subgoals: measured, for novices); a skeleton of placeholders alone
leaves the first document to be solved unaided. This check asks each shape that `[shape_example] files` declares to
show one filled example, in one of two ways:

- inline: a heading of the shape names an example (`example_headings`, such as "Worked example");
- linked: the shape links a document of the repository that announces it, on a line labelled `Shape:` that links
  back to the shape, the topic's rule of announcing the shape. A page that only cites the shape is not an example. An HTML or LaTeX file cannot link back in Markdown, so
  it counts when its name says it is an example (`example-talk.html`), never a template named after its shape. A
  declared shape is never an example of another: a derived shape is not a filled instance of its base.

A shape that does neither gets a warning: the rule applies the worked-example evidence, measured on learners of a
domain, to writers learning a genre, by analogy. Written from the learning extension's check, which on the family's
masters of 2026-10-29 agreed with a reading of every shape by hand.

What a run with no warning guarantees: every declared shape points to at least one document that declares it
follows that shape. What it does not: that the example is good, complete, or written with real content rather than
placeholders (judgment). Time O(links of the declared shapes and of their targets).
"""
from __future__ import annotations

import posixpath
import re
from pathlib import Path

from framework.check_api import Finding, files_in_scope, matches_any, prose_only

HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*$", re.MULTILINE)

NAME = "shape-example"
EXACT = False

LINK = re.compile(r"\[[^\]]*\]\(([^)\s#]+)(?:#[^)\s]*)?\)")


def targets(root: Path, path: str) -> set[str]:
    """The repository paths a file links to by relative path, resolved against its folder."""
    text = prose_only((root / path).read_text(encoding="utf-8", errors="replace"))
    found = set()
    for target in LINK.findall(text):
        if re.match(r"^[a-z]+:", target) or target.startswith("/"):
            continue
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
        if (root / resolved).is_dir():
            resolved = posixpath.join(resolved, "README.md")
        found.add(resolved)
    return found


def announces(root: Path, document: str, shape: str) -> bool:
    """True when a line of the document labelled Shape: links the shape."""
    lines = prose_only((root / document).read_text(encoding="utf-8", errors="replace")).splitlines()
    for line in lines:
        if re.search(r"\bshape\s*:", line, re.IGNORECASE):
            for target in LINK.findall(line):
                if posixpath.normpath(posixpath.join(posixpath.dirname(document), target)) == shape:
                    return True
    return False


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("shape_example", {})
    patterns = settings.get("files", [])
    if not patterns:
        return []
    in_repo = set(files_in_scope(root, config))
    findings = []
    for path in sorted(in_repo):
        if not path.endswith(".md") or not matches_any(path, patterns) or matches_any(path, settings.get("exempt", [])):
            continue
        text = prose_only((root / path).read_text(encoding="utf-8", errors="replace"))
        labels = [label.lower() for label in settings.get("example_headings", ["Worked example", "Example"])]
        inline = any(any(label in heading.lower() for label in labels) for heading in HEADING.findall(text))
        shapes = {other for other in in_repo if matches_any(other, patterns) and not matches_any(other, settings.get("exempt", []))}
        linked = [target for target in targets(root, path) - {path} - shapes if target in in_repo and
                  ((target.endswith((".html", ".tex")) and "example" in target.rsplit("/", 1)[-1].lower()) or
                   (target.endswith((".md", ".qmd")) and announces(root, target, path)))]
        if not inline and not linked:
            findings.append(Finding(NAME, path, 1, "the shape links no example of itself: link a document that follows "
                                                   "it and says so, since a worked example teaches a method better "
                                                   "than a skeleton alone", "warning"))
    return findings
