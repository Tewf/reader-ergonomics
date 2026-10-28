"""Co-change: files that keep changing together should sit together.

Every commit in the history that touches at most `max_files` files (a larger one is a rename
or a format pass, which couples files by accident) counts once for every pair of files it
touches. A pair that changed together at least `min_together` times, in at least `min_share`
of the commits of one of the two files, but that sits in two different folders, becomes a
judgment question: should the two share a folder, or should one link to a fact the other
holds? Files generated from others change with them by construction and are exempted in
config. Only files that still exist are counted.

Coupling in history is evidence, not proof, so every finding is judgment.
Time O(commits x max_files squared), space O(pairs).
"""
from __future__ import annotations

import subprocess
from collections import Counter
from itertools import combinations
from pathlib import Path, PurePosixPath

from framework.check_api import Finding, files_in_scope, matches_any

NAME = "co-change"
EXACT = False


def commits(root: Path) -> list[list[str]] | None:
    """The files each commit touched, or None when there is no readable history."""
    log = subprocess.run(["git", "-C", str(root), "log", "--no-merges", "--no-renames", "--name-only",
                          "--format=tformat:@@"], capture_output=True, text=True)
    if log.returncode != 0:
        return None
    return [[line for line in block.splitlines() if line.strip()] for block in log.stdout.split("@@") if block.strip()]


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("co_change", {})
    max_files, min_together = settings.get("max_files", 20), settings.get("min_together", 3)
    min_share, exempt = settings.get("min_share", 0.75), settings.get("exempt", [])
    present = {path for path in files_in_scope(root, config) if not matches_any(path, exempt)}
    history = commits(root)
    if history is None:
        is_repository = subprocess.run(["git", "-C", str(root), "rev-parse", "--git-dir"], capture_output=True).returncode == 0
        return [Finding(NAME, ".", 0, "git log failed, so co-change was not measured", "warning")] if is_repository else []
    file_commits, pair_commits = Counter(), Counter()
    for touched in history:
        files = sorted(set(touched) & present)
        if len(set(touched)) > max_files:
            continue
        file_commits.update(files)
        pair_commits.update(combinations(files, 2))
    findings = []
    for (first, second), together in sorted(pair_commits.items()):
        if PurePosixPath(first).parent == PurePosixPath(second).parent or together < min_together:
            continue
        share = together / min(file_commits[first], file_commits[second])
        if share >= min_share:
            findings.append(Finding(NAME, first, 0,
                f"changed together with {second} in {together} commits ({share:.0%} of the rarer one's), "
                "from another folder: should they share a folder, or should one link to the other?", "judgment"))
    return findings
