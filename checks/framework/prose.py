"""The units the reading checks count: the blocks of a markdown file, and the sentences of a paragraph.

A block is a heading, a paragraph, a list, a table, a quote, an image or a fenced block (a fenced
block whose info string is `text` is a figure). Front matter is skipped. Time O(text).
"""
from __future__ import annotations

import re
from dataclasses import dataclass

SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀ-Ý\[\$`(0-9*])")
FENCE = re.compile(r"^(`{3,}|~{3,})\s*(\S*)")
LIST_ITEM = re.compile(r"^([-*+]|\d+[.)])\s")
IMAGE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)$")


@dataclass(frozen=True)
class Block:
    kind: str  # heading | paragraph | list | table | quote | image | fence
    line: int
    text: str
    info: str = ""  # heading level, or the fence's info string


def blocks(text: str) -> list[Block]:
    lines = text.splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        start = next((index + 1 for index in range(1, len(lines)) if lines[index].strip() == "---"), 0)
    found, index = [], start
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped:
            index += 1
            continue
        fence = FENCE.match(stripped)
        if fence:
            run, body, first = fence.group(1), [], index
            index += 1
            while index < len(lines):
                closing = lines[index].strip()
                if closing.startswith(run[0] * len(run)) and not closing.strip(run[0] + " "):
                    break
                body.append(lines[index])
                index += 1
            found.append(Block("fence", first + 1, "\n".join(body), fence.group(2)))
            index += 1
            continue
        if stripped.startswith("#"):
            found.append(Block("heading", index + 1, stripped.lstrip("#").strip(), str(len(stripped) - len(stripped.lstrip("#")))))
            index += 1
            continue
        kind = ("table" if stripped.startswith("|") else "list" if LIST_ITEM.match(stripped)
                else "quote" if stripped.startswith(">") else "image" if IMAGE.match(stripped) else "paragraph")
        body, first = [], index
        while index < len(lines):
            current = lines[index].strip()
            if not current or current.startswith("#") or FENCE.match(current):
                break
            if kind == "paragraph" and body and (current.startswith("|") or LIST_ITEM.match(current)):
                break
            body.append(current)
            index += 1
        found.append(Block(kind, first + 1, " ".join(body) if kind == "paragraph" else "\n".join(body)))
    return found


def sentences(paragraph: str) -> list[str]:
    return [sentence for sentence in SENTENCE_BOUNDARY.split(paragraph) if sentence.strip()]


def title(text: str) -> str:
    """The front-matter title, or the first heading."""
    match = re.search(r'^title:\s*"?(.+?)"?\s*$', text.split("\n---", 1)[0], re.MULTILINE) if text.startswith("---") else None
    if match:
        return match.group(1)
    return next((block.text for block in blocks(text) if block.kind == "heading"), "")
