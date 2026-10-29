"""Decision records: every record in decisions/ follows the four rules of the decision-record shape.

A record is a file `decisions/NNNN-<name>.md`. A run with no error guarantees:
- rule 1: the records are numbered 1, 2, 3 ... with no gap and no repeat, and the folder's README links each one;
- rule 2: the title is `# NNNN: <title>`, with the number of its file name, and the first line under it opens
  `**Decision:**`, so a reader who stops there knows what holds;
- rule 4: a status that says superseded links the record that supersedes it, and every record a status links exists;
- the skeleton: a `**Status:**` line holds one of proposed, accepted, superseded or withdrawn and a date
  (YYYY-MM-DD), and a `**Shape:**` line links `shapes/decision-record.md`.

Rule 3 (the consequences include the bad ones) can only be asked, not decided. With `[decision_records] ask_costs`
on, a record whose Consequences hold no line labelled `Bad` becomes a judgment question, since only a reader can say
whether a decision really costs nothing. It is off by default, because the label is a convention a repository
chooses. The headings are checked by shape-conformance, as declared in checks/config.toml. It does not check that
the decision is right or the options complete. Files in decisions/ not named NNNN-*.md (the README) are not records.
Written from the software-design extension's local check, after a family audit found the shape's rules checked
nowhere.

Exact, except rule 3. Time O(records + README).
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import Finding

NAME = "decision-records"
EXACT = True

RECORD = re.compile(r"^(\d{4})-[a-z0-9.-]+\.md$")
SHAPE_LINK = re.compile(r"\*\*Shape:\*\*\s*\[[^\]]+\]\([^)]*shapes/decision-record\.md\)")
STATUS = re.compile(r"\*\*Status:\*\*([^\n]*)")
STATUS_WORD = re.compile(r"\b(proposed|accepted|superseded|withdrawn)\b", re.IGNORECASE)
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
RECORD_LINK = re.compile(r"\]\(((\d{4})-[^)#]+\.md)")
CONSEQUENCES = re.compile(r"^## Consequences[ \t]*$(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
BAD_LABEL = re.compile(r"^\s*(?:[-*]\s*)?(?:\*\*)?Bad\b", re.MULTILINE)


def check(root: Path, config: dict) -> list[Finding]:
    folder = root / "decisions"
    if not folder.is_dir():
        return []
    records = sorted(path for path in folder.iterdir() if RECORD.match(path.name))
    if not records:
        return []
    ask_costs = config.get("decision_records", {}).get("ask_costs", False)
    findings = numbering(records) + listed(folder, records)
    for path in records:
        findings += one_record(folder, path, ask_costs)
    return findings


def numbering(records: list[Path]) -> list[Finding]:
    """Rule 1: the numbers run 1, 2, 3 ... in file-name order."""
    for expected, path in enumerate(records, start=1):
        number = int(RECORD.match(path.name).group(1))
        if number != expected:
            return [Finding(NAME, f"decisions/{path.name}", 1,
                            f"record number {number:04d} where {expected:04d} was due: the records run 1, 2, 3 ... with no gap or repeat")]
    return []


def listed(folder: Path, records: list[Path]) -> list[Finding]:
    """Rule 1: the folder's README links every record."""
    readme = folder / "README.md"
    if not readme.is_file():
        return [Finding(NAME, "decisions/README.md", 1, "the decisions folder needs a README that lists its records")]
    text = readme.read_text(encoding="utf-8", errors="replace")
    return [Finding(NAME, "decisions/README.md", 1, f"the README does not link {path.name}")
            for path in records if f"({path.name})" not in text and f"(./{path.name})" not in text]


def one_record(folder: Path, path: Path, ask_costs: bool) -> list[Finding]:
    """Rules 2 to 4 and the skeleton, for one record."""
    number = RECORD.match(path.name).group(1)
    where = f"decisions/{path.name}"
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = [line for line in text.splitlines() if line.strip()]
    findings = []
    if not lines or not lines[0].startswith(f"# {number}: "):
        findings.append(Finding(NAME, where, 1, f"the title should open '# {number}: ', the record's number"))
    if len(lines) < 2 or not lines[1].startswith("**Decision:**"):
        findings.append(Finding(NAME, where, 1, "the first line under the title should open '**Decision:**' (rule 2: the decision first)"))
    status = STATUS.search(text)
    if not status:
        findings.append(Finding(NAME, where, 1, "a decision record needs a '**Status:**' line"))
    else:
        findings += status_line(folder, where, status.group(1))
    if not SHAPE_LINK.search(text):
        findings.append(Finding(NAME, where, 1, "a decision record names its shape: a '**Shape:**' line linking shapes/decision-record.md"))
    consequences = CONSEQUENCES.search(text)
    if ask_costs and consequences and not BAD_LABEL.search(consequences.group(1)):
        line = text[:consequences.start()].count("\n") + 1
        findings.append(Finding(NAME, where, line, "the Consequences hold no line labelled 'Bad': does this decision cost nothing, or is its cost unnamed (rule 3)?", "judgment"))
    return findings


def status_line(folder: Path, where: str, status: str) -> list[Finding]:
    """The status word, the date, and rule 4's forward link."""
    findings = []
    if not STATUS_WORD.search(status):
        findings.append(Finding(NAME, where, 1, "the status should say proposed, accepted, superseded or withdrawn"))
    if not DATE.search(status):
        findings.append(Finding(NAME, where, 1, "the status should carry its date, as YYYY-MM-DD"))
    links = RECORD_LINK.findall(status)
    if re.search(r"\bsuperseded\b", status, re.IGNORECASE) and not links:
        findings.append(Finding(NAME, where, 1, "a superseded record links the record that supersedes it (rule 4)"))
    for target, _ in links:
        if not (folder / target).is_file():
            findings.append(Finding(NAME, where, 1, f"the status links {target}, which is not in decisions/"))
    return findings
