"""The repository's generated indexes: the principle table in standard.md, llms.txt, and the check tables.

The first two are built from the principle files (their title, claim and grade), so a grade is
written once, in its principle, and every index follows it. Each check tier's README lists its
modules with the first line of their docstrings, so a check says what it does once, in its
code. As a check, it fails when a committed index differs from what its sources give.

Usage: python3 checks/program/standard_card.py [ROOT] [--write]
Exact. Time O(size of the principle files), space O(number of principles).
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # run alone, it still finds framework/
from framework.check_api import Finding

NAME = "standard-card"
EXACT = True
START, END = "<!-- principles:start -->", "<!-- principles:end -->"
CHECKS_START, CHECKS_END = "<!-- checks:start -->", "<!-- checks:end -->"
SITE = "https://tewf.github.io/reader-ergonomics/"
FACETS = [("collection", "Collection: files and folders"), ("document", "Document: order and depth"),
          ("sentence", "Sentence: density, locality and nesting"), ("page", "Page: figures, layout and type")]


def field(text: str, label: str) -> str:
    match = re.search(rf"^(?:- )?\*\*{label}:\*\*\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def principles(root: Path) -> list[dict]:
    found = []
    for facet, _ in FACETS:
        for path in sorted((root / "principles" / facet).glob("*.md")):
            if path.name == "README.md":
                continue
            text = path.read_text(encoding="utf-8")
            found.append({"facet": facet, "path": path.relative_to(root).as_posix(),
                          "title": text.splitlines()[0].lstrip("# ").strip(),
                          "claim": field(text, "Claim"), "grade": field(text, "Grade").rstrip(".")})
    return found


def table(items: list[dict]) -> str:
    lines = [START, ""]
    for facet, heading in FACETS:
        rows = [item for item in items if item["facet"] == facet]
        if not rows:
            continue
        lines += [f"### {heading}", "", "| Principle | Claim | Grade |", "|---|---|---|"]
        lines += [f"| [{item['title']}]({item['path']}) | {item['claim']} | {item['grade']} |" for item in rows]
        lines.append("")
    return "\n".join(lines + [END])


def llms_index(items: list[dict], root: Path) -> str:
    lines = ["# Reader ergonomics", "",
             "> How to write notes, documents and files that cost the reader least, by what cognitive science, "
             "psycholinguistics and software engineering have measured. Every principle carries its grade of evidence.",
             "", "Each page's markdown source is served at the same path with a .md extension.", "",
             "## Standard", "",
             f"- [Standard]({SITE}standard.md): the one-page card to follow, with every principle and its grade",
             f"- [Contributing]({SITE}AGENTS.md): rules for changing this repository", ""]
    for facet, heading in FACETS:
        rows = [item for item in items if item["facet"] == facet]
        if rows:
            lines += [f"## {heading}", ""] + [f"- [{item['title']}]({SITE}{item['path']}): {item['claim']}" for item in rows] + [""]
    styles = sorted(path for path in (root / "reader-styles").glob("*.md") if path.name not in ("README.md", "template.md"))
    lines += ["## Reader styles", "", f"- [Reader styles]({SITE}reader-styles/README.md): how a known reader changes the optimum"]
    lines += [f"- [{path.read_text(encoding='utf-8').splitlines()[0].lstrip('# ')}]({SITE}{path.relative_to(root).as_posix()})" for path in styles]
    lines += ["", "## Optional", "", f"- [Evidence]({SITE}evidence/README.md): one literature review per topic, with the evidence against",
              f"- [Bibliography]({SITE}evidence/bibliography.md): every cited work, once",
              f"- [Shapes]({SITE}shapes/README.md): skeletons for kinds of documents",
              f"- [Checks]({SITE}checks/README.md): the programs that verify the standard", ""]
    return "\n".join(lines)


def check_table(folder: Path) -> str:
    header = "| Check | What it verifies |" if folder.name == "program" else "| File | Role |"
    rows = []
    for module in sorted(folder.glob("*.py")):
        purpose = (ast.get_docstring(ast.parse(module.read_text(encoding="utf-8"))) or "").split("\n")[0].rstrip(".")
        rows.append(f"| [{module.name}]({module.name}) | {purpose} |")
    return "\n".join([CHECKS_START, header, "|---|---|", *rows, CHECKS_END])


def expected(root: Path) -> dict[str, str]:
    items = principles(root)
    card = (root / "standard.md").read_text(encoding="utf-8")
    built = re.sub(re.escape(START) + ".*?" + re.escape(END), lambda _: table(items), card, flags=re.DOTALL)
    outputs = {"standard.md": built, "llms.txt": llms_index(items, root)}
    for readme in sorted((root / "checks").glob("*/README.md")):
        text = readme.read_text(encoding="utf-8")
        if CHECKS_START in text:
            outputs[readme.relative_to(root).as_posix()] = re.sub(re.escape(CHECKS_START) + ".*?" + re.escape(CHECKS_END),
                lambda _: check_table(readme.parent), text, flags=re.DOTALL)
    return outputs


def check(root: Path, config: dict) -> list[Finding]:
    if not (root / "standard.md").is_file() or not (root / "principles").is_dir():
        return []
    findings = []
    for name, text in expected(root).items():
        current = (root / name).read_text(encoding="utf-8") if (root / name).is_file() else ""
        if current != text:
            findings.append(Finding(NAME, name, 0, "stale: rebuild with python3 checks/program/standard_card.py --write"))
    return findings


if __name__ == "__main__":
    arguments = [argument for argument in sys.argv[1:] if argument != "--write"]
    root = Path(arguments[0] if arguments else ".").resolve()
    for name, text in expected(root).items():
        if "--write" in sys.argv:
            (root / name).write_text(text, encoding="utf-8")
            print(f"wrote {name}")
        elif ((root / name).read_text(encoding="utf-8") if (root / name).is_file() else "") != text:
            print(f"stale: {name}")
