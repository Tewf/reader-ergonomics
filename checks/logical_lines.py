"""File size: a trigger on logical lines and a ceiling on physical lines, each asking a question.

A logical line of markdown is a statement: one sentence of prose, one list item, one
table row, one fenced or math block. Layout counts zero: headings, blank lines,
frontmatter, separators, callout markers, table separators. Re-cutting a paragraph into
bullets therefore changes nothing. Past the trigger, the file's role must be stated in
one sentence; past the ceiling, the file is reviewed for a split into pieces that change
separately. Size alone never decides a split (no defect threshold has held up), so both
are judgment questions, sent to the judgment backend.

The sentence count is a heuristic (abbreviations split badly).
Time O(n) in the size of the files, space O(longest paragraph).
Usage alone: python3 logical_lines.py FILE... [--over N]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any

NAME = "logical-lines"
EXACT = False
SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?:;])\s+(?=[A-ZÀ-Ý\[\$`(0-9*])")
LIST_ITEM = re.compile(r"^([-*+]|\d+[.)])\s")
TABLE_SEPARATOR = re.compile(r"^\|?\s*:?-{2,}")
CALLOUT_MARKER = re.compile(r"^\[!\w+\]")
TEXT_SUFFIXES = MARKDOWN_SUFFIXES | {".py", ".sh", ".js", ".ts", ".css", ".tex", ".yml", ".yaml", ".toml"}


def logical_line_count(text: str, ignored_prefixes: tuple[str, ...] = ()) -> int:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        closing = next((index for index in range(1, len(lines)) if lines[index].strip() == "---"), 0)
        lines = lines[closing + 1:]
    count, paragraph, fence = 0, [], ""  # fence: the backtick or tilde run that opened the block

    def close_paragraph() -> None:
        nonlocal count, paragraph
        if paragraph:
            sentences = [part for part in SENTENCE_BOUNDARY.split(" ".join(paragraph)) if part.strip()]
            count += max(1, len(sentences))
            paragraph = []

    for raw in lines:
        stripped = raw.strip()
        run = re.match(r"^(`{3,}|~{3,}|\$\$)", stripped)
        if fence:
            if run and run.group(1)[0] == fence[0] and len(run.group(1)) >= len(fence) and stripped.strip("`~$ ") == "":
                fence = ""
            continue
        if run and (run.group(1) != "$$" or stripped == "$$"):
            close_paragraph()
            count += 1
            fence = run.group(1)
            continue
        content = re.sub(r"^(>\s?)+", "", stripped).strip()  # a callout counts by its content
        is_layout = (not content or content == "---" or content.startswith("#")
                     or (CALLOUT_MARKER.match(content) and len(content) < 40)
                     or TABLE_SEPARATOR.match(content) or content.startswith(ignored_prefixes))
        if is_layout:
            close_paragraph()
        elif LIST_ITEM.match(content) or content.startswith("|"):
            close_paragraph()
            count += 1
        else:
            paragraph.append(content)
    close_paragraph()
    return count


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("logical_lines", {})
    trigger, ceiling = settings.get("trigger", 80), settings.get("ceiling", 500)
    exempt_from_trigger = settings.get("exempt_from_trigger", [])
    ignored_prefixes = tuple(settings.get("ignore_line_prefixes", []))
    findings = []
    for path in files_in_scope(root, config, TEXT_SUFFIXES):
        text = (root / path).read_text(encoding="utf-8", errors="replace")
        physical = len(text.splitlines())
        if physical > ceiling:
            findings.append(Finding(NAME, path, 1, f"{physical} lines, past the ceiling of {ceiling}. Review it: split it "
                "only into pieces that change separately and each stay whole, or state why it stays one file.", "judgment"))
        if Path(path).suffix in MARKDOWN_SUFFIXES and not matches_any(path, exempt_from_trigger):
            logical = logical_line_count(text, ignored_prefixes)
            if logical > trigger:
                findings.append(Finding(NAME, path, 1,
                    f"{logical} logical lines, past the trigger of {trigger}. State this file's role in one "
                    "sentence. If the sentence needs 'and', split the file; if not, it may stay.", "judgment"))
    return findings


if __name__ == "__main__":
    arguments, over = sys.argv[1:], 0
    if "--over" in arguments:
        position = arguments.index("--over")
        over = int(arguments[position + 1])
        arguments = arguments[:position] + arguments[position + 2:]
    for name in arguments:
        text = Path(name).read_text(encoding="utf-8", errors="replace")
        logical = logical_line_count(text)
        if logical > over:
            print(f"{logical:5} logical {len(text.splitlines()):5} physical  {name}")
