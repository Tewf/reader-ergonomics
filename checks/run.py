"""Run the checks on a repository: exact findings fail, heuristics warn, the rest is judgment.

Usage: python3 checks/run.py [ROOT] [--config FILE] [--tiers program,meaning,syntax] [--only NAME[,NAME]]
                             [--online] [--judge BACKEND]
ROOT defaults to the current folder. The config is ROOT/checks/config.toml when it exists,
else the one next to this file. Exit status 1 when any exact check fails, else 0.

An extension of the standard can add to it (the contract is extending.md): a config with
`extends = "reader-ergonomics"` is merged onto the standard's, table by table, and the modules in
ROOT/checks/local/ run beside the standard's checks. Those modules are code from the checked
repository: run this only on repositories you trust.

Three tiers, cheapest first: `program` needs only the Python standard library (3.11 or later);
`meaning` needs fastembed and `syntax` needs spaCy with en_core_web_sm. A tier whose library is
missing is skipped with a notice, never failed. The default tiers are in config.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
import tomllib
from pathlib import Path

from framework import judgment
from framework.check_api import repository_paths
from framework.config import load_config
from meaning import document_mode, name_content, paraphrase, section_cohesion
from program import (citations, co_change, cross_file_terms, defined_before_use, duplication, figure_captions,
                     figures_present, links, logical_lines, long_sentences, name_matches_title, outline_depth,
                     overview_first, paragraph_length, portable_paths, principle_coverage, provisional_tags,
                     readable_measure, references, shape_conformance, standard_card, sufficient_contrast, tree_shape,
                     type_buckets)
from syntax import clause_nesting, dependency_length, sentence_links

CHECKS = [portable_paths, tree_shape, type_buckets, links, logical_lines, outline_depth, overview_first,
          name_matches_title, duplication, defined_before_use, cross_file_terms, shape_conformance, long_sentences,
          paragraph_length, figures_present, figure_captions, readable_measure, sufficient_contrast, citations,
          standard_card, provisional_tags, co_change, principle_coverage, references,
          paraphrase, document_mode, name_content, section_cohesion,
          dependency_length, clause_nesting, sentence_links]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a repository against the reader-ergonomics standard.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--config", help="a config.toml other than the repository's own")
    parser.add_argument("--tiers", help="comma-separated tiers: program, meaning, syntax (default from config)")
    parser.add_argument("--only", help="comma-separated check names")
    parser.add_argument("--online", action="store_true", help="resolve references over the network")
    parser.add_argument("--judge", choices=["none", "flag", "local", "api"], help="override the judgment backend")
    arguments = parser.parse_args()

    root = Path(arguments.root).resolve()
    if not root.is_dir():
        parser.error(f"{root} is not a folder")
    try:
        config = load_config(root, Path(arguments.config) if arguments.config else None)
    except (OSError, ValueError, tomllib.TOMLDecodeError) as error:
        parser.error(str(error))
    if not repository_paths(root):
        print(f"error    run                  no file in scope under {root}: nothing was checked (is the folder git-ignored?)")
        return 2
    checks = CHECKS + local_checks(root)
    config["online"] = arguments.online
    config["registered_checks"] = [module.NAME for module in checks]
    tiers = set((arguments.tiers or ",".join(config.get("run", {}).get("tiers", ["program"]))).split(","))
    selected = set(arguments.only.split(",")) if arguments.only else None

    findings, ran, skipped = [], set(), set()
    for module in checks:
        tier = getattr(module, "TIER", "program")
        if tier not in tiers or (selected is not None and module.NAME not in selected):
            continue
        if not getattr(module, "available", lambda: True)():
            skipped.add(tier)
            continue
        findings += module.check(root, config)
        ran.add(tier)
    errors = [finding for finding in findings if finding.kind == "error"]
    warnings = [finding for finding in findings if finding.kind == "warning"]
    for finding in errors + warnings:
        location = f"{finding.path}:{finding.line}" if finding.line else finding.path
        print(f"{finding.kind:8} {finding.check:20} {location}  {finding.message}")
    for tier in sorted(skipped):
        print(f"notice   tier '{tier}' skipped: its library is not installed (see checks/README.md)")
    settings = config.get("judgment", {})
    print(judgment.dispatch(root, findings, arguments.judge or settings.get("backend", "flag"), settings))
    print(summary(len(errors), len(warnings), ran, skipped))
    return 1 if errors else 0


def local_checks(root: Path) -> list:
    """The modules in ROOT/checks/local/: each has a NAME and check(root, config), like the standard's own."""
    folder = root / "checks" / "local"
    if not folder.is_dir() or folder.resolve() == Path(__file__).resolve().with_name("local"):
        return []
    modules = []
    for path in sorted(folder.glob("*.py")):
        spec = importlib.util.spec_from_file_location(f"local_{path.stem}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "NAME") and callable(getattr(module, "check", None)):
            modules.append(module)
    return modules


def summary(errors: int, warnings: int, ran: set[str], skipped: set[str]) -> str:
    """The last line: the tiers that ran, and apart from them the tiers whose library was missing."""
    line = f"{errors} error(s), {warnings} warning(s); tiers run: {', '.join(sorted(ran)) or 'none'}"
    return line + (f"; skipped: {', '.join(sorted(skipped))}" if skipped else "")


if __name__ == "__main__":
    sys.exit(main())
