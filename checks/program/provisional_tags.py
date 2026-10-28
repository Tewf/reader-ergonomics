"""PROVISIONAL tags: a value marked as a guess is measured, or kept knowingly, before it ages.

Every line holding the word PROVISIONAL, in the files where values live (configuration and
code, by default), is dated by git blame: the day the line was last written. Past
`max_age_days`, the tag becomes a judgment question: measure the value, or say why it stays
a guess. Outside a git repository the check finds nothing to date and reports nothing.

Exact for the date. Time O(text + lines blamed), space O(tags).
"""
from __future__ import annotations

import subprocess
import time
from pathlib import Path

from framework.check_api import Finding, files_in_scope, matches_any

NAME = "provisional-tags"
EXACT = True
TAG = "PROVISIONAL"


def line_dates(root: Path, path: str) -> list[int]:
    """The author time of every line of a file, in order; uncommitted lines count as today."""
    blame = subprocess.run(["git", "-C", str(root), "blame", "--line-porcelain", "--", path],
                           capture_output=True, text=True)
    if blame.returncode != 0:
        return []
    return [int(line.split()[1]) for line in blame.stdout.splitlines() if line.startswith("author-time ")]


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("provisional_tags", {})
    files = settings.get("files", ["*.toml", "*.py", "*.yml", "*.yaml", "*.json", "*.cfg", "*.ini"])
    max_age = settings.get("max_age_days", 90) * 86400
    findings = []
    for path in files_in_scope(root, config):
        if not matches_any(path, files) or matches_any(path, settings.get("exempt", [])):
            continue
        lines = (root / path).read_text(encoding="utf-8", errors="replace").splitlines()
        tagged = [number for number, line in enumerate(lines, 1) if TAG in line]
        if not tagged:
            continue
        dates = line_dates(root, path)
        for number in tagged:
            if number <= len(dates) and time.time() - dates[number - 1] > max_age:
                written = time.strftime("%Y-%m-%d", time.gmtime(dates[number - 1]))
                findings.append(Finding(NAME, path, number,
                    f"a {TAG} value written on {written}, older than {max_age // 86400} days: measure it, "
                    "or say why it stays a guess", "judgment"))
    return findings
