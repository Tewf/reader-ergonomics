"""Changelog pin: the newest pin line of an extension's changelog names the release its workflows check out.

A move to a new release is recorded in `CHANGELOG.md`, not in a decision record, since it had no alternative
([extending](../../extending.md), Versions). The changelog is then one more copy of the pin, beside the workflows and
the links: a bump that forgets it leaves the reader of the changelog on the old release. So, when the workflows check
out `[standard_pin] repository` at one commit, the first line of `CHANGELOG.md` that names the repository with a
version and a commit, `reader-ergonomics v1.16.1 (397a555)`, names that commit, newest first as the changelog is
written. A changelog with no such line, or no changelog, is a warning: an extension whose pins are still recorded in
`decisions/` starts its changelog at its next move.

It reads the workflows as standard-pin reads them, and does nothing when they name no ref, or several: standard-pin
reports those. The standard never checks itself out, so it finds nothing in this repository.

Exact for a pin line written as the form gives it. Time O(size of the changelog).
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import Finding
from program.standard_pin import checkouts

NAME = "changelog-pin"
EXACT = True


def check(root: Path, config: dict) -> list[Finding]:
    repository = config.get("standard_pin", {}).get("repository", "Tewf/reader-ergonomics")
    pins = {ref for _, _, ref in checkouts(root, repository) if ref}
    if len(pins) != 1:
        return []
    pinned = pins.pop()
    changelog = root / "CHANGELOG.md"
    if not changelog.is_file():
        return [Finding(NAME, "CHANGELOG.md", 0, f"the workflows pin {repository} at {pinned[:7]} and no CHANGELOG.md "
                                                 "records it: write each move there (extending.md, Versions)", "warning")]
    name = re.escape(repository.split("/")[-1])
    line = re.compile(rf"\b{name} (v\d+\.\d+\.\d+) \(`?([0-9a-f]{{7,40}})`?\)")
    text = changelog.read_text(encoding="utf-8", errors="replace")
    newest = line.search(text)
    if not newest:
        return [Finding(NAME, "CHANGELOG.md", 0, f"no line names {repository} with a version and a commit, so the "
                                                 f"pin {pinned[:7]} is not recorded: add the move, newest first", "warning")]
    if not pinned.startswith(newest.group(2)):
        return [Finding(NAME, "CHANGELOG.md", text.count("\n", 0, newest.start()) + 1,
                        f"the newest pin line names {newest.group(1)} ({newest.group(2)[:7]}), but the workflows pin "
                        f"{pinned[:7]}: record the move above it")]
    return []
