"""Links: every relative link in a markdown file resolves to a file or folder that exists.

Covers inline links and images `[text](target)`, reference definitions `[key]: target`
and wikilinks `[[name]]` (resolved by file name anywhere in the repository; a repository
whose wikilinks may point ahead sets `[links] wikilinks = "ignore"`). Links with a scheme
(web, mail, app links) and same-page anchors are left to the reference check. Code is ignored.

Exact for file links. Time O(total text + number of paths), space O(number of paths).
"""
from __future__ import annotations

import re
import urllib.parse
from pathlib import Path, PurePosixPath

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, line_of, prose_only, repository_paths

NAME = "links"
EXACT = True
INLINE_LINK = re.compile(r"\]\(<([^>]+)>\)|\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
REFERENCE_DEFINITION = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?([^\s>]+)>?", re.MULTILINE)
WIKILINK = re.compile(r"!?\[\[([^\]|#]+)")
URI_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")  # http:, mailto: and app links are not files


def check(root: Path, config: dict) -> list[Finding]:
    names = set()
    for path in repository_paths(root):
        names.update({PurePosixPath(path).name, PurePosixPath(path).stem})
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        text = prose_only((root / path).read_text(encoding="utf-8", errors="replace"))
        targets = [(match.group(1) or match.group(2), match.start()) for match in INLINE_LINK.finditer(text)]
        targets += [(match.group(1), match.start()) for match in REFERENCE_DEFINITION.finditer(text)]
        for target, offset in targets:
            if URI_SCHEME.match(target) or target.startswith("#") or "{{" in target:
                continue
            relative = urllib.parse.unquote(target.split("#")[0].split("?")[0])
            if relative and not ((root / path).parent / relative).exists():
                findings.append(Finding(NAME, path, line_of(text, offset), f"link does not resolve: {target}"))
        for match in WIKILINK.finditer(text) if config.get("links", {}).get("wikilinks", "resolve") == "resolve" else ():
            name = match.group(1).strip()
            if name and name not in names and f"{name}.md" not in names:
                findings.append(Finding(NAME, path, line_of(text, match.start()), f"wikilink to nothing: [[{name}]]"))
    return findings
