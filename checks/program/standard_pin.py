"""Standard pin: every workflow checks out the standard at one commit, so one bump moves the checks and the site together.

An extension's CI checks out the standard by its commit ([extending](../../extending.md), Versions): the checks job
to run them, the site job to load `site.css`. Each checkout holds the release a second time, so a bump that moves one
line leaves the other behind; on 2026-10-29 one extension ran the checks of v1.11.0 and built its site with the
stylesheet of v1.4.1. So, in `.github/workflows/`, every step that checks out `[standard_pin] repository` names a
`ref:`, and all of them name the same one. A checkout without a ref loads the latest commit, against Versions.

The standard never checks itself out, so it finds nothing in this repository.

Exact for a checkout step written on separate lines, as the template writes it; a step in flow style
(`with: {repository: ...}`) is not read. Time O(size of the workflows).
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from framework.check_api import Finding

NAME = "standard-pin"
EXACT = True
STEP = re.compile(r"^[ \t]*-[ \t]+(?:uses|name|run|id|if|with|env|shell|working-directory):", re.MULTILINE)
REF = re.compile(r"^[ \t]*ref:[ \t]*['\"]?([^\s'\"#]+)", re.MULTILINE)


def checkouts(root: Path, repository: str) -> list[tuple[str, int, str]]:
    """(workflow, line, ref) for every step that checks out the repository; the ref is empty when the step has none."""
    named = re.compile(rf"^[ \t]*repository:[ \t]*['\"]?{re.escape(repository)}['\"]?[ \t]*(?:#.*)?$", re.MULTILINE)
    found = []
    for workflow in sorted((root / ".github" / "workflows").glob("*.y*ml")):
        text = workflow.read_text(encoding="utf-8", errors="replace")
        starts = [match.start() for match in STEP.finditer(text)] + [len(text)]
        for start, end in zip(starts, starts[1:]):
            step = text[start:end]
            if not (match := named.search(step)):
                continue
            ref = REF.search(step)
            line = text.count("\n", 0, start + (ref.start() if ref else match.start())) + 1
            found.append((workflow.relative_to(root).as_posix(), line, ref.group(1) if ref else ""))
    return found


def check(root: Path, config: dict) -> list[Finding]:
    repository = config.get("standard_pin", {}).get("repository", "Tewf/reader-ergonomics")
    found = checkouts(root, repository)
    findings = [Finding(NAME, path, line, f"checks out {repository} with no ref, so the latest commit: pin it to "
                                          "the release's commit") for path, line, ref in found if not ref]
    pinned = [(path, line, ref) for path, line, ref in found if ref]
    if len({ref for _, _, ref in pinned}) > 1:
        # the ref most steps name, and on a tie the first one met, is the release the others are compared with
        usual = Counter(ref for _, _, ref in pinned).most_common(1)[0][0]
        where = next(f"{path}:{line}" for path, line, ref in pinned if ref == usual)
        findings += [Finding(NAME, path, line, f"checks out {repository} at {ref[:7]}, and {where} at {usual[:7]}: "
                                               "one release for the whole repository, so one bump moves every job")
                     for path, line, ref in pinned if ref != usual]
    return findings
