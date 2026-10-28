"""Principle coverage: every principle names at least one check that exists, so CI tests every rule.

Each principle file states its checks on its **Check:** line, as backticked names. At least
one of them must be the name of a registered check, from any tier (program, meaning, syntax);
a principle that names none fails. A check that runs only weekly still counts.

Exact. Time O(principle files).
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import Finding

NAME = "principle-coverage"
EXACT = True


def check(root: Path, config: dict) -> list[Finding]:
    registered = set(config.get("registered_checks", []))
    findings = []
    for path in sorted((root / "principles").glob("*/*.md")) if (root / "principles").is_dir() else []:
        if path.name == "README.md":
            continue
        line = re.search(r"^(?:- )?\*\*Check:\*\*(.*)$", path.read_text(encoding="utf-8"), re.MULTILINE)
        named = set(re.findall(r"`([a-z][a-z-]+)`", line.group(1))) if line else set()
        if not named & registered:
            relative = path.relative_to(root).as_posix()
            findings.append(Finding(NAME, relative, 0, f"no registered check named on its Check line (named: {sorted(named) or 'none'})"))
    return findings
