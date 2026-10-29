"""Standard links: every link from the text into the standard names the commit the workflows pin.

An extension links the standard's principles and shapes at the release it checks against
([extending](../../extending.md), Versions), and moves those links with the pin. standard-pin holds the workflows to one commit; the text is the other copy of that release.
A link left at an older commit, or at a branch such as `master`, shows a reader a rule CI does not run. So every
markdown link whose target is `github.com/<[standard_pin] repository>/blob/<ref>/...` or `.../tree/<ref>/...` must
name the commit the workflows name, or the release tag their checkout line names in its comment (`# v1.12.0`), which
is the same release by another name.

It reads the workflows as standard-pin reads them, and does nothing when they name no ref, or several: standard-pin
reports those. Links in code, inline or fenced, are quotations, not links, and are skipped. It does not check that
the target exists at that commit (references does, online). Written by the software-design extension, adopted in v1.13.0.

Exact for links written `[text](target)`. Time O(text).
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, line_of, prose_only
from program.standard_pin import checkouts

NAME = "standard-links"
EXACT = True


def check(root: Path, config: dict) -> list[Finding]:
    repository = config.get("standard_pin", {}).get("repository", "Tewf/reader-ergonomics")
    found = [(path, line, ref) for path, line, ref in checkouts(root, repository) if ref]
    if len({ref for _, _, ref in found}) != 1:
        return []
    pinned = found[0][2]
    accepted = {pinned} | {tag for path, line, _ in found for tag in release_tags(root / path, line)}
    link = re.compile(rf"\]\(https?://github\.com/{re.escape(repository)}/(?:blob|tree)/([^/)\s]+)[/)]")
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        text = prose_only((root / path).read_text(encoding="utf-8", errors="replace"))
        for match in link.finditer(text):
            if match.group(1) not in accepted:
                findings.append(Finding(NAME, path, line_of(text, match.start()),
                                        f"links {repository} at {match.group(1)[:12]}, but the workflows pin "
                                        f"{pinned[:7]}: move the link with the pin, so the text shows the rules CI runs"))
    return findings


def release_tags(workflow: Path, line: int) -> set[str]:
    """The release tag a checkout's ref line names in its comment, such as `# v1.12.0`; empty when it names none."""
    lines = workflow.read_text(encoding="utf-8", errors="replace").splitlines()
    comment = lines[line - 1].partition("#")[2] if 0 < line <= len(lines) else ""
    return set(re.findall(r"\bv\d+\.\d+\.\d+\b", comment)[:1])
