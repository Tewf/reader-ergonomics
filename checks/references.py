"""References: every DOI, arXiv id, GitHub repository and web link cited resolves.

Offline (the default), only the form of each identifier is checked, which is exact and
needs no network. Online (`--online`), each one is resolved against doi.org, the arXiv
API, GitHub and the link itself. Successes are cached in `checks/out/` for `cache_days`,
so a rerun costs nothing. Resolving shows that a reference exists, not that it supports
the claim it is cited for; that remains judgment.

Exact offline. Online depends on remote servers (a timeout is reported, never hidden).
Time O(references) requests, space O(references).
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ElementTree
from pathlib import Path

from check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any

NAME = "references"
EXACT = True
ARXIV = re.compile(r"(?:arxiv\.org/(?:abs|pdf|html)/|arXiv[:\s]\s*)(\d{4}\.\d{4,5}|[a-z\-]+(?:\.[A-Z]{2})?/\d{7})", re.IGNORECASE)
DOI = re.compile(r"\b(10\.\d{4,9}/[^\s)\]>\"'`,;|]+)")
GITHUB = re.compile(r"(?<![\w.-])(?:www\.)?github\.com/([A-Za-z0-9-]+)/([A-Za-z0-9_.-]+)")
URL = re.compile(r"https?://[^\s)\]>\"'`|]+")
HEADERS = {"User-Agent": "reader-ergonomics-reference-check/1.0"}
ATOM = "{http://www.w3.org/2005/Atom}"


def fetch(url: str, method: str = "GET", timeout: int = 20) -> bytes:
    request = urllib.request.Request(url, headers=HEADERS, method=method)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def resolve(kind: str, identifier: str) -> str | None:
    """None when the identifier resolves, else the reason it does not."""
    try:
        if kind == "doi":
            answer = json.loads(fetch(f"https://doi.org/api/handles/{identifier}"))
            return None if answer.get("responseCode") == 1 else "not registered"
        if kind == "arxiv":
            feed = ElementTree.fromstring(fetch(f"https://export.arxiv.org/api/query?id_list={identifier}&max_results=1", timeout=30))
            titles = [entry.findtext(f"{ATOM}title", "").strip() for entry in feed.findall(f"{ATOM}entry")]
            time.sleep(3)  # the arXiv API asks for three seconds between calls
            return None if titles and titles[0].lower() != "error" else "no such paper"
        target = f"https://github.com/{identifier}" if kind == "github" else identifier
        try:
            fetch(target, method="HEAD")
        except urllib.error.HTTPError as error:
            if error.code not in (403, 405, 429):
                raise
            fetch(target)  # some servers refuse HEAD but answer GET
        return None
    except urllib.error.HTTPError as error:
        return f"HTTP {error.code}"
    except Exception as error:  # a timeout fails this reference, not the run
        return error.__class__.__name__


def cited(text: str) -> set[tuple[str, str]]:
    found = {("arxiv", identifier) for identifier in ARXIV.findall(text)}
    found |= {("doi", doi.rstrip(".")) for doi in DOI.findall(text)}
    found |= {("github", f"{owner}/{re.sub(r'.git$', '', name).rstrip('.')}") for owner, name in GITHUB.findall(text)
              if owner.lower() not in ("orgs", "topics", "features", "sponsors", "marketplace")}
    found |= {("link", url.rstrip(".")) for url in URL.findall(text)
              if not GITHUB.search(url) and "arxiv.org/" not in url and "doi.org/" not in url}
    return found


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("references", {})
    online, files = config.get("online", False), settings.get("files", [])
    cache_path = root / "checks" / "out" / "references-cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    findings = []
    for path in files_in_scope(root, config, MARKDOWN_SUFFIXES):
        if files and not matches_any(path, files):  # only the files where references live
            continue
        for kind, identifier in sorted(cited((root / path).read_text(encoding="utf-8", errors="replace"))):
            if kind == "doi" and not re.fullmatch(r"10\.\d{4,9}/\S+", identifier):
                findings.append(Finding(NAME, path, 0, f"malformed DOI {identifier}"))
            if not online or time.time() - cache.get(f"{kind} {identifier}", 0) < settings.get("cache_days", 30) * 86400:
                continue
            reason = resolve(kind, identifier)
            if reason:
                findings.append(Finding(NAME, path, 0, f"{kind} {identifier}: {reason}"))
            else:
                cache[f"{kind} {identifier}"] = time.time()
    if online:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache, indent=0, sort_keys=True))
    return findings
