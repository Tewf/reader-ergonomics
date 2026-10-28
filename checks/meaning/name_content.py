"""Name and content: what a file's name means is close to what its opening says.

The words of the name and the first 600 characters are embedded; below `threshold`, the pair
becomes a judgment question. It catches a name that is spelled right but means something else,
which the word-matching check cannot. A name used in `role_name_folders` folders or more names a
part of a repeated skeleton (frame.md, baseline.md), not a topic, and is skipped.

Semantic, so judgment. Time O(files).
"""
from __future__ import annotations

from pathlib import Path, PurePosixPath

from framework.check_api import MARKDOWN_SUFFIXES, Finding, files_in_scope, matches_any, prose_only
from meaning import embeddings
from program.name_matches_title import SKIPPED_STEMS, name_words

NAME = "name-content"
EXACT = False
TIER = "meaning"
available = embeddings.available


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("name_content", {})
    paths = files_in_scope(root, config, MARKDOWN_SUFFIXES)
    folders_per_name = {}
    for path in paths:
        folders_per_name.setdefault(PurePosixPath(path).name, set()).add(str(PurePosixPath(path).parent))
    files = []
    for path in paths:
        role_name = len(folders_per_name[PurePosixPath(path).name]) >= settings.get("role_name_folders", 3)
        words = name_words(path)
        if words and not role_name and PurePosixPath(path).stem.lower() not in SKIPPED_STEMS and not matches_any(path, settings.get("exempt", [])):
            files.append((path, " ".join(words), prose_only((root / path).read_text(encoding="utf-8", errors="replace"))[:600]))
    if not files:
        return []
    names = embeddings.embed([name for _, name, _ in files])
    openings = embeddings.embed([opening for _, _, opening in files])
    return [Finding(NAME, path, 1, f"the name '{name}' and the opening are far apart in meaning ({float(score):.2f}): "
                    "does the name predict the content?", "judgment")
            for (path, name, _), score in zip(files, (names * openings).sum(axis=1)) if score < settings.get("threshold", 0.2)]
