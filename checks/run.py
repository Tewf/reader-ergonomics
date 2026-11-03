"""Run the checks on a repository: exact findings fail, heuristics warn, the rest is judgment.

Usage: python3 checks/run.py [ROOT] [--config FILE] [--tiers program,meaning,syntax] [--only NAME[,NAME]]
                             [--online] [--judge BACKEND] [--out FILE]
ROOT defaults to the current folder. The config is ROOT/checks/config.toml when it exists,
else the one next to this file. Exit status 1 when any exact check fails, else 0.

An extension of the standard can add to it (the contract is extending.md): a config with
`extends = "reader-ergonomics"` is merged onto the standard's, table by table, and the modules in
ROOT/checks/local/ run beside the standard's checks. Those modules are code from the checked
repository: run this only on repositories you trust.

Three tiers, cheapest first: `program` needs only the Python standard library (3.11 or later);
`meaning` needs fastembed and `syntax` needs spaCy with en_core_web_sm. A tier whose library is
missing is skipped with a notice, never failed. The default tiers are in config.

`--out FILE` also writes the verdicts to FILE, replacing the last run's: one line per finding,
`kind check path:line message` (kind is error, warning or judgment; the line is left out when the check
knows none), then a summary line `summary errors=N warnings=N judgments=N seconds=S tiers=...`, then
`exit N`. Only the questions still open are listed. Standard output is unchanged.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
import time
import tomllib
from pathlib import Path

from framework import judgment
from framework.check_api import Finding, repository_paths
from framework.config import load_config
from meaning import document_mode, name_content, paraphrase, section_cohesion
from figures import (figure_alt, figure_captions, figure_contrast, figure_source, figure_source_inline, figure_width,
                     figures_present, typed_figure)
from program import (bibliography_keys, changelog_pin, citations, co_change, cross_file_terms, decision_records, defined_before_use,
                     duplication, judgment_quotes, links, logical_lines, long_sentences, name_matches_title,
                     outline_depth, overview_first, paragraph_length, portable_paths, principle_coverage,
                     provisional_tags, readable_measure, references, release_version, shape_conformance, shape_example, standard_card,
                     standard_links, standard_pin, sufficient_contrast, tree_shape, type_buckets)
from syntax import clause_nesting, dependency_length, sentence_links

CHECKS = [portable_paths, tree_shape, type_buckets, links, logical_lines, outline_depth, overview_first,
          name_matches_title, duplication, defined_before_use, cross_file_terms, shape_conformance, long_sentences,
          paragraph_length, figures_present, figure_captions, figure_width, figure_source_inline, figure_alt, figure_source,
          figure_contrast, typed_figure, readable_measure, sufficient_contrast, citations,
          bibliography_keys, standard_card, standard_pin, standard_links, changelog_pin, release_version, provisional_tags, co_change, principle_coverage, references, judgment_quotes,
          decision_records, shape_example,
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
    parser.add_argument("--out", help="also write the verdicts, one line per finding, to this file")
    arguments = parser.parse_args()

    started = time.monotonic()
    root = Path(arguments.root).resolve()
    if not root.is_dir():
        parser.error(f"{root} is not a folder")
    try:
        config = load_config(root, Path(arguments.config) if arguments.config else None)
    except (OSError, ValueError, tomllib.TOMLDecodeError) as error:
        parser.error(str(error))
    if not repository_paths(root):
        print(f"error    run                  no file in scope under {root}: nothing was checked (is the folder git-ignored?)")
        if arguments.out:
            write_verdicts(Path(arguments.out), [Finding("run", ".", 0, "no file in scope: nothing was checked")], 2,
                           set(), time.monotonic() - started)
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
    status = 1 if errors else 0
    if arguments.out:
        known = judgment.answered(root, settings)
        open_questions = [finding for finding in findings if finding.kind == "judgment"
                          and (finding.check, finding.path, finding.message, judgment.fingerprint(root, finding.path)) not in known]
        write_verdicts(Path(arguments.out), errors + warnings + open_questions, status, ran, time.monotonic() - started)
    return status


def write_verdicts(path: Path, findings: list[Finding], status: int, ran: set[str], seconds: float) -> None:
    """The verdicts file: a line per finding, a summary line, then the exit status; a complete file ends in `exit N`."""
    lines = []
    for finding in findings:
        location = f"{finding.path}:{finding.line}" if finding.line else finding.path
        lines.append(f"{finding.kind} {finding.check} {location} {' '.join(finding.message.split())}")
    count = lambda kind: sum(1 for finding in findings if finding.kind == kind)
    lines.append(f"summary errors={count('error')} warnings={count('warning')} judgments={count('judgment')} "
                 f"seconds={seconds:.1f} tiers={','.join(sorted(ran)) or 'none'}")
    lines.append(f"exit {status}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
