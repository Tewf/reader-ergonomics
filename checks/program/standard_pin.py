"""Standard pin: every workflow checks out the standard at one commit, so one bump moves the checks and the site together.

An extension's CI checks out the standard by its commit ([extending](../../extending.md), Versions): the checks job
to run them, the site job to load `site.css`. Each checkout holds the release a second time, so a bump that moves one
line leaves the other behind; on 2026-10-29 one extension ran the checks of v1.11.0 and built its site with the
stylesheet of v1.4.1. So, in `.github/workflows/`, every step that checks out `[standard_pin] repository` names a
`ref:`, and all of them name the same one. A checkout without a ref loads the latest commit, against Versions.

The standard never checks itself out, so it finds nothing in this repository.

Exact for a checkout step written on separate lines, as the template writes it; a step in flow style
(`with: {repository: ...}`) is not read. Time O(size of the workflows).

Run as a program, it also moves a pin: `python3 checks/program/standard_pin.py <repository> <old commit> <new commit>
<new tag> [--dry-run]` replaces, in every text file git tracks except CHANGELOG.md, the old commit's 40 characters,
its 7-character prefix where it stands alone (`archive bfbe9f7`), and `# vOLD` beside a checkout, by the new ones; it
lists the lines where the old version is written in prose, and what is left to the person: the changelog line, a
figure whose label names the version, the judgment answers of the files that changed. Exact in what it replaces; a
dry run writes nothing.
"""
from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

if __name__ == "__main__":  # run as a program, from any folder: the checks package is beside this file's folder
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from framework.check_api import Finding  # noqa: E402

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


def tracked_text_files(root: Path) -> list[Path]:
    out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], check=True, capture_output=True).stdout
    files = []
    for name in out.decode("utf-8", "surrogateescape").split("\0"):
        if not name or name == "CHANGELOG.md":
            continue
        path = root / name
        try:
            path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        files.append(path)
    return files


def old_tag(root: Path, files: list[Path], old: str) -> str | None:
    """The tag named in a comment beside the old commit, `ref: <old>   # v1.18.2 ...`."""
    pattern = re.compile(re.escape(old) + r"[^\n]*#\s*(v\d+\.\d+\.\d+)")
    for path in files:
        match = pattern.search(path.read_text(encoding="utf-8"))
        if match:
            return match.group(1)
    return None


def move(root: Path, old: str, new: str, tag: str, dry_run: bool = False) -> dict[str, int]:
    files = tracked_text_files(root)
    previous = old_tag(root, files, old)
    short_old, short_new = old[:7], new[:7]
    touched: dict[str, int] = {}
    prose: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        changed = text.replace(old, new)
        changed = re.sub(r"(?<![0-9a-f])" + re.escape(short_old) + r"(?![0-9a-f])", short_new, changed)
        if previous:
            changed = re.sub(r"#(\s*)" + re.escape(previous) + r"\b", lambda m: "#" + m.group(1) + tag, changed)
            for number, line in enumerate(changed.splitlines(), 1):
                if previous in line and "#" not in line.split(previous)[0][-3:]:
                    prose.append(f"{path.relative_to(root)}:{number}: {line.strip()[:100]}")
        if changed != text:
            touched[str(path.relative_to(root))] = sum(1 for a, b in zip(text.splitlines(), changed.splitlines()) if a != b) + abs(
                len(changed.splitlines()) - len(text.splitlines()))
            if not dry_run:
                path.write_text(changed, encoding="utf-8")
    verb = "would change" if dry_run else "changed"
    for name, lines in sorted(touched.items()):
        print(f"{verb} {name}: {lines} line(s)")
    print(f"{len(touched)} file(s); old tag {previous or 'not found beside the old commit'} -> {tag}")
    if prose:
        print("the old version is still written in prose on these lines; read each and decide:")
        for line in prose:
            print("  " + line)
    print("left to you: the CHANGELOG.md pin line, any figure whose label names the version, checks/judgments.toml.")
    return touched


def main(argv: list[str]) -> int:
    args = [a for a in argv if a != "--dry-run"]
    if len(args) != 4:
        print(__doc__)
        return 2
    root, old, new, tag = Path(args[0]).resolve(), args[1], args[2], args[3]
    if len(old) != 40 or len(new) != 40 or not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        print("the commits are 40 characters and the tag is vMAJOR.MINOR.PATCH")
        return 2
    move(root, old, new, tag, dry_run="--dry-run" in argv)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
