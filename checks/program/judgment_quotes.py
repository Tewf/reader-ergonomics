"""Judgment quotes: every answer in the answers file quotes the file it answers for, and every quote is really there.

An answer is a claim about one file, and its reason is the evidence. A reason copied from another file's answer can
name words this file does not hold and still pass every other check. So, for each answer whose file exists and is
unchanged since the answer was given:

- the answer quotes at least one phrase, in backticks or double quotes, unless its check is listed in
  `[judgment_quotes] optional`;
- each quoted phrase occurs in the answered file, ignoring case and runs of spaces; for a folder, it names one of its
  entries; or it names a file beside the answered one, or a path from the repository's root (the other file of a
  co-change pair);
- each "line N" the answer cites is a line of the file.

An answer whose file is gone, or has changed since (its fingerprint no longer matches), is skipped: the judgment step
asks that question again, and the new answer is checked instead. Written from two extensions' checks, which found
most of their answers written once per kind of question, with reasons their files did not hold.

Exact for the presence of each quote; whether the quote supports the answer is judgment. Time O(answers x file size).
"""
from __future__ import annotations

import re
import tomllib
from pathlib import Path

from framework.check_api import Finding
from framework.judgment import fingerprint

NAME = "judgment-quotes"
EXACT = True
QUOTE = re.compile(r'`([^`\n]{2,})`|"([^"\n]{2,})"|“([^”\n]{2,})”')
LINE_REFERENCE = re.compile(r"\bline (\d+)\b")


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def found(quote: str, root: Path, path: str) -> bool:
    """Whether a quoted phrase is in the answered file, names an entry of the answered folder, or names a path."""
    target = root / path
    if target.is_dir() and any(entry.name == quote.rstrip("/") for entry in target.iterdir()):
        return True
    if target.is_file() and flat(quote) in flat(target.read_text(encoding="utf-8", errors="replace")):
        return True
    beside = target if target.is_dir() else target.parent
    return (beside / quote).exists() or (root / quote).exists()


def check(root: Path, config: dict) -> list[Finding]:
    name = config.get("judgment", {}).get("answers", "checks/judgments.toml")
    source = root / name
    if not source.is_file():
        return []
    raw = source.read_text(encoding="utf-8")
    try:
        answers = tomllib.loads(raw).get("answer", [])
    except tomllib.TOMLDecodeError as error:
        return [Finding(NAME, name, 1, f"the answers file cannot be read as TOML: {error}")]
    headers = [number for number, line in enumerate(raw.splitlines(), 1) if line.strip() == "[[answer]]"]
    optional = set(config.get("judgment_quotes", {}).get("optional", []))
    findings = []
    for index, answer in enumerate(answers):
        line = headers[index] if index < len(headers) else 1
        path, kind, reason = answer.get("path", ""), answer.get("check", ""), str(answer.get("answer", ""))
        if not path or not (root / path).exists() or answer.get("file", "") != fingerprint(root, path):
            continue
        quotes = [next(group for group in match.groups() if group) for match in QUOTE.finditer(reason)]
        if reason.strip() and not quotes and kind not in optional:
            findings.append(Finding(NAME, name, line, f"the answer for {path} ({kind}) quotes nothing from it: put a phrase "
                                                      "of that file in backticks, so its reason can be checked"))
        for quote in quotes:
            if not found(quote, root, path):
                findings.append(Finding(NAME, name, line, f"the answer for {path} ({kind}) quotes `{quote}`, "
                                                          "which is not in that file"))
        if (root / path).is_file():
            length = len((root / path).read_text(encoding="utf-8", errors="replace").splitlines())
            for number in LINE_REFERENCE.findall(reason):
                if not 1 <= int(number) <= length:
                    findings.append(Finding(NAME, name, line, f"the answer for {path} ({kind}) cites line {number}; "
                                                              f"the file has {length}"))
    return findings
