"""The repository's generated indexes: the principle table in standard.md, llms.txt, and the check tables.

The site, title and description come from the checked repository's _quarto.yml, and the principle
groups from its config ([standard_card] facets), so an extension of the standard gets its own
indexes (see extending.md); without them, the values are this repository's own.

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
from framework.config import load_config
from framework.check_api import Finding

NAME = "standard-card"
EXACT = True
START, END = "<!-- principles:start -->", "<!-- principles:end -->"
CHECKS_START, CHECKS_END = "<!-- checks:start -->", "<!-- checks:end -->"
SITE = "https://tewf.github.io/reader-ergonomics/"
TITLE = "Reader ergonomics"
DESCRIPTION = ("How to write notes, documents and files that cost the reader least, by what cognitive science, "
               "psycholinguistics and software engineering have measured. Every principle carries its grade of evidence.")
FACETS = [("collection", "Collection: files and folders"), ("document", "Document: order and depth"),
          ("sentence", "Sentence: density, locality and nesting"), ("page", "Page: figures, layout and type")]


def field(text: str, label: str) -> str:
    match = re.search(rf"^(?:- )?\*\*{label}:\*\*\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def facets(root: Path, config: dict | None) -> list[tuple[str, str]]:
    """The principle groups in order: [standard_card] facets, each headed by its README's first line."""
    names = (config or {}).get("standard_card", {}).get("facets")
    if not names:
        return FACETS
    found = []
    for name in names:
        readme = root / "principles" / name / "README.md"
        heading = readme.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip() if readme.is_file() else name
        found.append((name, heading))
    return found


def site(root: Path) -> dict:
    """site-url, title and description from the checked repository's _quarto.yml, else this one's."""
    text = (root / "_quarto.yml").read_text(encoding="utf-8") if (root / "_quarto.yml").is_file() else ""
    value = lambda key, default: (re.search(rf'^\s+{key}:\s*"([^"]+)"', text, re.MULTILINE) or [None, default])[1]
    return {"url": value("site-url", SITE), "title": value("title", TITLE), "description": value("description", DESCRIPTION)}


def principles(root: Path, groups: list[tuple[str, str]] = FACETS) -> list[dict]:
    found = []
    for facet, _ in groups:
        for path in sorted((root / "principles" / facet).glob("*.md")):
            if path.name == "README.md":
                continue
            text = path.read_text(encoding="utf-8")
            found.append({"facet": facet, "path": path.relative_to(root).as_posix(),
                          "title": text.splitlines()[0].lstrip("# ").strip(),
                          "claim": field(text, "Claim"), "grade": field(text, "Grade").rstrip(".")})
    return found


def table(items: list[dict], groups: list[tuple[str, str]] = FACETS) -> str:
    lines = [START, ""]
    for facet, heading in groups:
        rows = [item for item in items if item["facet"] == facet]
        if not rows:
            continue
        lines += [f"### {heading}", "", "| Principle | Claim | Grade |", "|---|---|---|"]
        lines += [f"| [{item['title']}]({item['path']}) | {item['claim']} | {item['grade']} |" for item in rows]
        lines.append("")
    return "\n".join(lines + [END])


def llms_index(items: list[dict], root: Path, groups: list[tuple[str, str]] = FACETS) -> str:
    about = site(root)
    url = about["url"]
    lines = [f"# {about['title']}", "", f"> {about['description']}",
             "", "Each page's markdown source is served at the same path with a .md extension.", "",
             "## Standard", "",
             f"- [Standard]({url}standard.md): the one-page card to follow, with every principle and its grade",
             f"- [Contributing]({url}AGENTS.md): rules for changing this repository"]
    if (root / "extending.md").is_file():
        lines.append(f"- [Extending]({url}extending.md): what an extension of this standard can rely on")
    lines.append("")
    for facet, heading in groups:
        rows = [item for item in items if item["facet"] == facet]
        if rows:
            lines += [f"## {heading}", ""] + [f"- [{item['title']}]({url}{item['path']}): {item['claim']}" for item in rows] + [""]
    if (root / "reader-styles" / "README.md").is_file():
        styles = sorted(path for path in (root / "reader-styles").glob("*.md") if path.name not in ("README.md", "template.md"))
        lines += ["## Reader styles", "", f"- [Reader styles]({url}reader-styles/README.md): how a known reader changes the optimum"]
        lines += [f"- [{path.read_text(encoding='utf-8').splitlines()[0].lstrip('# ')}]({url}{path.relative_to(root).as_posix()})" for path in styles]
        lines.append("")
    optional = [("evidence/README.md", "Evidence", "one literature review per topic, with the evidence against"),
                ("evidence/bibliography.md", "Bibliography", "every cited work, once"),
                ("shapes/README.md", "Shapes", "skeletons for kinds of documents"),
                ("checks/README.md", "Checks", "the programs that verify the standard"),
                ("decisions/README.md", "Decisions", "the choices this repository made, one record each")]
    lines += ["## Optional", ""] + [f"- [{label}]({url}{path}): {what}" for path, label, what in optional if (root / path).is_file()] + [""]
    return "\n".join(lines)


def guarantee(docstring: str) -> str:
    """What a check's findings can be trusted for: the words before `Time O(` in its cost paragraph."""
    for paragraph in docstring.split("\n\n"):
        if "Time O(" in paragraph:
            lines = [line for line in paragraph.splitlines() if not line.startswith("Usage")]
            return " ".join(" ".join(lines).split("Time O(")[0].split())
    return ""


def check_table(folder: Path) -> str:
    entries = []
    for module in sorted(folder.glob("*.py")):
        tree = ast.parse(module.read_text(encoding="utf-8"))
        docstring = ast.get_docstring(tree) or ""
        is_check = any(isinstance(node, ast.Assign) and any(getattr(target, "id", "") == "NAME" for target in node.targets)
                       for node in tree.body)
        entries.append((module.name, docstring.split("\n")[0].rstrip("."), guarantee(docstring) if is_check else ""))
    header = "| Check | What it verifies |" if folder.name == "program" else "| File | Role |"
    if not any(promise for _, _, promise in entries):  # a folder of helpers has no guarantee to show
        return "\n".join([CHECKS_START, header, "|---|---|", *(f"| [{name}]({name}) | {role} |" for name, role, _ in entries),
                          CHECKS_END])
    rows = [f"| [{name}]({name}) | {role} | {promise} |" for name, role, promise in entries]
    return "\n".join([CHECKS_START, header + " Guarantee |", "|---|---|---|", *rows, CHECKS_END])


def expected(root: Path, config: dict | None = None) -> dict[str, str]:
    groups = facets(root, config)
    items = principles(root, groups)
    card = (root / "standard.md").read_text(encoding="utf-8")
    built = re.sub(re.escape(START) + ".*?" + re.escape(END), lambda _: table(items, groups), card, flags=re.DOTALL)
    outputs = {"standard.md": built, "llms.txt": llms_index(items, root, groups)}
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
    for name, text in expected(root, config).items():
        current = (root / name).read_text(encoding="utf-8") if (root / name).is_file() else ""
        if current != text:
            findings.append(Finding(NAME, name, 0, "stale: rebuild with python3 checks/program/standard_card.py --write"))
    return findings


if __name__ == "__main__":
    arguments = [argument for argument in sys.argv[1:] if argument != "--write"]
    root = Path(arguments[0] if arguments else ".").resolve()
    for name, text in expected(root, load_config(root)).items():
        if "--write" in sys.argv:
            (root / name).write_text(text, encoding="utf-8")
            print(f"wrote {name}")
        elif ((root / name).read_text(encoding="utf-8") if (root / name).is_file() else "") != text:
            print(f"stale: {name}")
