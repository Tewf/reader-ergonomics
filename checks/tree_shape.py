"""Tree shape: folders stay browsable, and dependencies between folders never form a cycle.

- Breadth: a folder past `max_entries` visible entries fails (menu-breadth studies put
  the optimum at 8 to 16 items per level; the threshold is in config).
- Narrowness: a folder under `min_entries` is a question, not a failure: fold it into its
  parent unless it is one record of a collection (a job folder, a chapter).
- Depth: a file deeper than `max_depth` folders warns.
- Cycles: Python imports are resolved to files of the repository and lifted to their
  folders; a strongly connected component of more than one folder fails. A link between
  documents is a reference, not a dependency, and may cycle.

Exact for breadth, depth and static imports; dynamic imports are invisible.
Time O(paths + imports) with Tarjan's algorithm, space O(paths + imports).
"""
from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path, PurePosixPath

from check_api import Finding, matches_any, repository_paths

NAME = "tree-shape"
EXACT = True


def visible(path: str) -> bool:
    return not any(part.startswith(".") for part in path.split("/"))


def folder_entries(paths: list[str]) -> dict[str, set[str]]:
    entries = defaultdict(set)
    for path in paths:
        parts = path.split("/")
        for depth in range(len(parts)):
            entries["/".join(parts[:depth])].add(parts[depth])
    return entries


def imported_files(source: str, importer: str, known: set[str]) -> set[str]:
    """Repository files a Python module imports statically, found next to it or from the root."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    here = PurePosixPath(importer).parent
    found = set()

    def resolve(base: PurePosixPath, dotted: str) -> None:
        stem = base.joinpath(*dotted.split(".")) if dotted else base
        for candidate in (f"{stem}.py", f"{stem}/__init__.py"):
            candidate = candidate.removeprefix("./")
            if candidate in known:
                found.add(candidate)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                resolve(here, alias.name)
                resolve(PurePosixPath("."), alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level > 1 and node.level - 2 >= len(here.parents):
                continue  # a relative import above the repository root
            bases = [here.parents[node.level - 2] if node.level > 1 else here] if node.level else [here, PurePosixPath(".")]
            for base in bases:
                resolve(base, node.module or "")
                for alias in node.names:
                    resolve(base, f"{node.module}.{alias.name}" if node.module else alias.name)
    return found


def strongly_connected_components(graph: dict[str, set[str]]) -> list[list[str]]:
    """Tarjan's algorithm, iterative."""
    index, lowlink, on_stack, stack, components, counter = {}, {}, set(), [], [], 0
    for start in sorted(graph):
        if start in index:
            continue
        work = [(start, iter(sorted(graph[start])))]
        index[start] = lowlink[start] = counter
        counter += 1
        stack.append(start)
        on_stack.add(start)
        while work:
            node, successors = work[-1]
            advanced = False
            for successor in successors:
                if successor not in index:
                    index[successor] = lowlink[successor] = counter
                    counter += 1
                    stack.append(successor)
                    on_stack.add(successor)
                    work.append((successor, iter(sorted(graph.get(successor, ())))))
                    advanced = True
                    break
                if successor in on_stack:
                    lowlink[node] = min(lowlink[node], index[successor])
            if advanced:
                continue
            work.pop()
            if work:
                lowlink[work[-1][0]] = min(lowlink[work[-1][0]], lowlink[node])
            if lowlink[node] == index[node]:
                component = []
                while True:
                    member = stack.pop()
                    on_stack.discard(member)
                    component.append(member)
                    if member == node:
                        break
                components.append(sorted(component))
    return components


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("tree_shape", {})
    excluded = config.get("scope", {}).get("exclude", []) + settings.get("exempt", [])
    paths = [path for path in repository_paths(root) if visible(path)]
    findings = []
    for folder, entries in sorted(folder_entries(paths).items()):
        if matches_any(folder + "/", excluded) or (folder and matches_any(folder, excluded)):
            continue
        shown = folder or "(root)"
        if len(entries) > settings.get("max_entries", 16):
            findings.append(Finding(NAME, shown, 0,
                f"{len(entries)} entries, over {settings.get('max_entries', 16)}: split it by purpose"))
        if folder and len(entries) < settings.get("min_entries", 3):
            findings.append(Finding(NAME, shown, 0,
                f"{len(entries)} entries: fold into the parent folder, unless this folder is one record "
                "of a collection (a job, a chapter, a topic).", "judgment"))
    for path in paths:
        if path.count("/") > settings.get("max_depth", 4) and not matches_any(path, excluded):
            findings.append(Finding(NAME, path, 0, f"{path.count('/')} folders deep", "warning"))
    known = {path for path in repository_paths(root) if path.endswith(".py")}
    folder_graph = defaultdict(set)
    for path in known:
        source = (root / path).read_text(encoding="utf-8", errors="replace")
        for target in imported_files(source, path, known):
            source_folder, target_folder = str(PurePosixPath(path).parent), str(PurePosixPath(target).parent)
            if source_folder != target_folder:
                folder_graph[source_folder].add(target_folder)
    for component in strongly_connected_components(folder_graph):
        if len(component) > 1:
            findings.append(Finding(NAME, component[0], 0, f"import cycle between folders: {' -> '.join(component)}"))
    return findings
