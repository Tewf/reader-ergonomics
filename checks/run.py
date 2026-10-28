"""Run the checks on a repository: exact findings fail, heuristics warn, the rest is judgment.

Usage: python3 checks/run.py [ROOT] [--config FILE] [--tiers program,meaning,syntax] [--only NAME[,NAME]]
                             [--online] [--judge BACKEND]
ROOT defaults to the current folder. The config is ROOT/checks/config.toml when it exists,
else the one next to this file. Exit status 1 when any exact check fails, else 0.

Three tiers, cheapest first: `program` needs only the Python standard library (3.11 or later);
`meaning` needs fastembed and `syntax` needs spaCy with en_core_web_sm. A tier whose library is
missing is skipped with a notice, never failed. The default tiers are in config.
"""
from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

from framework import judgment
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
    config_path = Path(arguments.config) if arguments.config else root / "checks" / "config.toml"
    if not config_path.exists():
        config_path = Path(__file__).with_name("config.toml")
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    config["online"] = arguments.online
    config["registered_checks"] = [module.NAME for module in CHECKS]
    tiers = set((arguments.tiers or ",".join(config.get("run", {}).get("tiers", ["program"]))).split(","))
    selected = set(arguments.only.split(",")) if arguments.only else None

    findings, skipped = [], set()
    for module in CHECKS:
        tier = getattr(module, "TIER", "program")
        if tier not in tiers or (selected is not None and module.NAME not in selected):
            continue
        if not getattr(module, "available", lambda: True)():
            skipped.add(tier)
            continue
        findings += module.check(root, config)
    errors = [finding for finding in findings if finding.kind == "error"]
    warnings = [finding for finding in findings if finding.kind == "warning"]
    for finding in errors + warnings:
        location = f"{finding.path}:{finding.line}" if finding.line else finding.path
        print(f"{finding.kind:8} {finding.check:20} {location}  {finding.message}")
    for tier in sorted(skipped):
        print(f"notice   tier '{tier}' skipped: its library is not installed (see checks/README.md)")
    settings = config.get("judgment", {})
    print(judgment.dispatch(root, findings, arguments.judge or settings.get("backend", "flag"), settings))
    print(f"{len(errors)} error(s), {len(warnings)} warning(s); tiers: {', '.join(sorted(tiers))}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
