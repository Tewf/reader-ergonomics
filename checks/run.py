"""Run every check on a repository: exact findings fail, heuristics warn, the rest is judgment.

Usage: python3 checks/run.py [ROOT] [--config FILE] [--only NAME[,NAME]] [--online] [--judge BACKEND]
ROOT defaults to the current folder. The config is ROOT/checks/config.toml when it exists,
else the one next to this file. Exit status 1 when any exact check fails, else 0.
Needs only the Python standard library (3.11 or later, for tomllib).
"""
from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

import citations
import defined_before_use
import duplication
import judgment
import links
import logical_lines
import portable_paths
import references
import standard_card
import tree_shape

CHECKS = [portable_paths, tree_shape, links, logical_lines, duplication, defined_before_use, citations, standard_card, references]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a repository against the reader-ergonomics standard.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--config", help="a config.toml other than the repository's own")
    parser.add_argument("--only", help="comma-separated check names")
    parser.add_argument("--online", action="store_true", help="resolve references over the network")
    parser.add_argument("--judge", choices=["none", "flag", "local", "api"], help="override the judgment backend")
    arguments = parser.parse_args()

    root = Path(arguments.root).resolve()
    config_path = Path(arguments.config) if arguments.config else root / "checks" / "config.toml"
    if not config_path.exists():
        config_path = Path(__file__).with_name("config.toml")
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    config["online"] = arguments.online
    selected = set(arguments.only.split(",")) if arguments.only else None

    findings = []
    for module in CHECKS:
        if selected is None or module.NAME in selected:
            findings += module.check(root, config)
    errors = [finding for finding in findings if finding.kind == "error"]
    warnings = [finding for finding in findings if finding.kind == "warning"]
    for finding in errors + warnings:
        location = f"{finding.path}:{finding.line}" if finding.line else finding.path
        print(f"{finding.kind:8} {finding.check:20} {location}  {finding.message}")
    settings = config.get("judgment", {})
    print(judgment.dispatch(root, findings, arguments.judge or settings.get("backend", "flag"), settings))
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
