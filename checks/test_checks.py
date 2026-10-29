"""The checks' own oracle: each check must find a violation planted in a scratch repository,
and nothing in a clean one. Run: python3 -m unittest discover checks
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from figures import figure_captions, figures_present
from program import (co_change, cross_file_terms, decision_records, defined_before_use, duplication, judgment_quotes,
                     links, logical_lines, long_sentences, name_matches_title, outline_depth, overview_first,
                     paragraph_length, portable_paths, principle_coverage, provisional_tags, readable_measure,
                     references, shape_conformance, shape_example, standard_card, sufficient_contrast, tree_shape,
                     type_buckets)
import run

CONFIG = {"scope": {"exclude": []}, "tree_shape": {"max_entries": 4, "min_entries": 2, "max_depth": 3},
          "duplication": {"words": 8}, "logical_lines": {"trigger": 3, "ceiling": 10}}
SENTENCE = "the reader holds what the page has not yet resolved in memory"


class ScratchRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.folder = tempfile.TemporaryDirectory()
        self.root = Path(self.folder.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)

    def tearDown(self) -> None:
        self.folder.cleanup()

    def write(self, path: str, text: str = "x\n") -> None:
        (self.root / path).parent.mkdir(parents=True, exist_ok=True)
        (self.root / path).write_text(text, encoding="utf-8")

    def messages(self, module) -> list[str]:
        return [f"{finding.kind} {finding.path} {finding.message}" for finding in module.check(self.root, CONFIG)]


class TestPlantedViolations(ScratchRepository):
    def test_references_keep_balanced_parentheses(self) -> None:
        found = references.cited("see https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming) and "
                                 "doi 10.1002/(SICI)1097-4571(199806)49:8 (Smith 2020).")
        self.assertIn(("link", "https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)"), found)
        self.assertIn(("doi", "10.1002/(SICI)1097-4571(199806)49:8"), found)

    def test_references_refusal_is_a_warning(self) -> None:
        self.write("refs.md", "https://refused.example/a and https://gone.example/b\n")
        answers = {"https://refused.example/a": "HTTP 403", "https://gone.example/b": "HTTP 404"}
        original, references.resolve = references.resolve, lambda kind, identifier: answers[identifier]
        try:
            found = [f"{finding.kind} {finding.message}" for finding in references.check(self.root, {**CONFIG, "online": True})]
        finally:
            references.resolve = original
        self.assertIn("warning link https://refused.example/a: HTTP 403, the server refused the checker; open it by hand", found)
        self.assertIn("error link https://gone.example/b: HTTP 404", found)

    def test_portable_paths(self) -> None:
        self.write("notes/a:b.md")
        self.write("notes/Same.md")
        self.write("notes/same.md")
        self.write("notes/draft .md")
        self.write("notes/NUL.txt")
        self.write("notes/COM¹.md")
        self.write("notes/ends.")
        found = " ".join(self.messages(portable_paths))
        self.assertIn("forbidden character", found)
        self.assertIn("only by case", found)
        self.assertIn("space before the extension", found)
        self.assertIn("reserved device name", found)
        self.assertIn("COM¹", found)
        self.assertIn("trailing period", found)

    def test_links(self) -> None:
        self.write("a.md", "[ok](b.md) [broken](missing.md) [[nowhere]] `[code](skipped.md)`\n")
        self.write("b.md")
        found = self.messages(links)
        self.assertEqual(len(found), 2, found)

    def test_tree_shape(self) -> None:
        for name in "abcde":
            self.write(f"wide/{name}.md")
        self.write("thin/only.md")
        self.write("deep/one/two/three/file.md")
        self.write("package_a/x.py", "import y\nfrom package_b import z\n")
        self.write("package_b/z.py", "from package_a import x\n")
        found = " ".join(self.messages(tree_shape))
        self.assertIn("5 entries, over 4", found)
        self.assertIn("judgment thin", found)
        self.assertIn("folders deep", found)
        self.assertIn("import cycle between folders: package_a -> package_b", found)

    def test_duplication(self) -> None:
        self.write("one.md", f"First. {SENTENCE}.\n")
        self.write("two.md", f"Again: {SENTENCE}!\n")
        self.write("three.md", "| " + SENTENCE + " |\n")
        found = self.messages(duplication)
        self.assertEqual(len(found), 1, found)

    def test_defined_before_use(self) -> None:
        self.write("a.md", "# Surprisal\n\nSurprisal rises here.\n\n**Surprisal** is the negative log probability.\n")
        found = self.messages(defined_before_use)
        self.assertEqual(len(found), 1, found)
        self.assertIn("line 5", found[0])

    def test_logical_lines(self) -> None:
        text = "---\ntitle: x\n---\n# Heading\n\nOne. Two. Three\nwraps on.\n\n- four\n| five |\n|---|\n```\nsix\n```\n"
        self.assertEqual(logical_lines.logical_line_count(text), 6)
        self.write("long.md", text)
        found = " ".join(self.messages(logical_lines))
        self.assertIn("judgment long.md 6 logical lines", found)
        self.assertIn("judgment long.md 14 lines, past the ceiling of 10", found)


    def commit(self, message: str, date: str | None = None) -> None:
        environment = {"GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "test@example.org",
                       "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "test@example.org", "PATH": "/usr/bin:/bin"}
        if date:
            environment.update({"GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date})
        subprocess.run(["git", "-C", str(self.root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(self.root), "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", message],
                       check=True, env=environment)

    def test_outline_depth(self) -> None:
        self.write("deep.md", "# Title\n\n## Part\n\n### Sub\n\n#### Too deep\n\n```\n#### not a heading\n```\n")
        found = self.messages(outline_depth)
        self.assertEqual(len(found), 1, found)
        self.assertIn("level 4", found[0])

    def test_provisional_tags(self) -> None:
        self.write("old.toml", "limit = 3   # PROVISIONAL\n")
        self.commit("old guess", "2020-01-01T00:00:00")
        self.write("new.toml", "limit = 4   # PROVISIONAL\n")
        self.commit("new guess")
        found = self.messages(provisional_tags)
        self.assertEqual(len(found), 1, found)
        self.assertIn("old.toml", found[0])

    def test_co_change(self) -> None:
        for round_number in range(3):
            self.write("a/x.md", f"version {round_number}\n")
            self.write("b/y.md", f"version {round_number}\n")
            self.commit(f"together {round_number}")
        self.write("c/z.md", "alone\n")
        self.commit("alone")
        found = self.messages(co_change)
        self.assertEqual(len(found), 1, found)
        self.assertIn("a/x.md changed together with b/y.md in 3 commits", found[0])


    def test_type_buckets(self) -> None:
        self.write("docs/a.md")
        self.write("guides/b.md")
        found = self.messages(type_buckets)
        self.assertEqual(len(found), 1, found)

    def test_name_matches_title(self) -> None:
        self.write("guides/folder-depth.md", "# Folder depth\n\nText.\n")
        self.write("guides/contrast-ratio.md", "# Something else entirely\n\nText.\n")
        found = self.messages(name_matches_title)
        self.assertEqual(len(found), 1, found)
        self.assertIn("contrast-ratio", found[0])

    def test_overview_first(self) -> None:
        body = "\n".join(f"- item {index}" for index in range(25))
        self.write("long.md", "# Title\n\n## Detail\n\n" + body + "\n")
        self.write("good.md", "# Title\n\nWhat this is, in two parts.\n\n## Detail\n\n" + body + "\n")
        found = self.messages(overview_first)
        self.assertEqual(len(found), 1, found)
        self.assertIn("long.md", found[0])

    def test_cross_file_terms(self) -> None:
        self.write("glossary/terms.md", "**Surprisal** is how unexpected a word is.\n")
        self.write("notes/linked.md", "Surprisal matters, see [terms](../glossary/terms.md).\n")
        self.write("notes/unlinked.md", "Surprisal matters here too.\n")
        found = self.messages(cross_file_terms)
        self.assertEqual(len(found), 1, found)
        self.assertIn("notes/unlinked.md", found[0])

    def test_shape_conformance(self) -> None:
        self.write("notes/a.md", "# A\n\n## In three points\n\n## Check yourself\n")
        self.write("notes/b.md", "# B\n\n## In three points\n")
        config = dict(CONFIG, shape_conformance={"shapes": [{"name": "note", "files": ["notes/*.md"], "required": ["In three points", "Check yourself"]}]})
        found = [finding.path for finding in shape_conformance.check(self.root, config)]
        self.assertEqual(found, ["notes/b.md"])

    def test_long_sentences(self) -> None:
        self.write("a.md", "Short one. " + " ".join(["word"] * 40) + ".\n\n- one item\n- " + " ".join(["word"] * 10) + "\n")
        found = self.messages(long_sentences)
        self.assertEqual(len(found), 1, found)

    def test_figures_present(self) -> None:
        self.write("plain.md", "\n".join(f"Sentence {index}." for index in range(45)) + "\n")
        self.write("drawn.md", "\n".join(f"Sentence {index}." for index in range(45)) + "\n\n| a | b |\n|---|---|\n")
        found = self.messages(figures_present)
        self.assertEqual(len(found), 1, found)
        self.assertIn("plain.md", found[0])

    def test_figure_captions(self) -> None:
        self.write("a.md", "# A\n\n![](x.png)\n\n## B\n\n```text\nA -> B\n```\n\n## C\n\nWords.\n\n```text\nC -> D\n```\n")
        found = self.messages(figure_captions)
        self.assertEqual(len(found), 2, found)

    def test_paragraph_length(self) -> None:
        self.write("a.md", "One. Two. Three. Four. Five.\n\nOne. Two.\n")
        found = self.messages(paragraph_length)
        self.assertEqual(len(found), 1, found)

    def test_site_stylesheet(self) -> None:
        self.write("site.css", "main p { max-width: 90ch; font-size: 14px; line-height: 1.2; }\n"
                   "body { color: #777777; background: #ffffff; }\n.ok { color: #101014; background: #F7F7F9; }\n")
        config = dict(CONFIG, readable_measure={"stylesheets": ["site.css"]}, sufficient_contrast={"stylesheets": ["site.css"]})
        self.assertEqual(len(readable_measure.check(self.root, config)), 3)
        contrast = sufficient_contrast.check(self.root, config)
        self.assertEqual(len(contrast), 1, contrast)
        self.assertAlmostEqual(sufficient_contrast.ratio("000000", "ffffff"), 21.0)

    def test_principle_coverage(self) -> None:
        self.write("principles/page/a.md", "# A\n\n- **Check:** `links` (exact).\n")
        self.write("principles/page/b.md", "# B\n\n- **Check:** judgment.\n")
        config = dict(CONFIG, registered_checks=["links"])
        found = [finding.path for finding in principle_coverage.check(self.root, config)]
        self.assertEqual(found, ["principles/page/b.md"])


class TestCleanRepository(ScratchRepository):
    def test_nothing_found(self) -> None:
        self.write("guide/README.md", "See [the note](note.md).\n")
        self.write("guide/note.md", "**Locality** is the distance between a word and its head. Locality matters.\n")
        self.write("guide/other.md", "A different sentence entirely.\n")
        for module in (portable_paths, links, duplication, defined_before_use):
            self.assertEqual(self.messages(module), [], module.NAME)


class TestJudgmentQuotes(ScratchRepository):
    """An answer quotes its own file, and only its own file (ported from two extensions' checks)."""

    def setUp(self) -> None:
        super().setUp()
        self.write("a.md", "# Against\n\n## Null results for the typed format\n\nText.\n")
        self.write("b.md", "# Frame\n\n## What the field calls it\n\nText.\n")
        self.write("notes/one.md", "x\n")

    def entry(self, check: str, path: str, answer: str, file: str | None = None) -> str:
        from framework.judgment import fingerprint
        import json
        stamp = fingerprint(self.root, path) if file is None else file
        return (f'[[answer]]\ncheck = "{check}"\npath = "{path}"\nquestion = "q"\nfile = "{stamp}"\n'
                f"answer = {json.dumps(answer)}\n")

    def found(self, *entries: str, **settings) -> list[str]:
        self.write("checks/judgments.toml", "\n".join(entries))
        return [finding.message for finding in judgment_quotes.check(self.root, dict(CONFIG, judgment_quotes=settings))]

    def test_a_quote_from_its_own_file_passes_whatever_its_case_and_spacing(self) -> None:
        self.assertEqual(self.found(self.entry("document-mode", "a.md", "Reference: under `null  RESULTS for the typed format`."),
                                    self.entry("document-mode", "b.md", 'Explanation: "What the field calls it".')), [])

    def test_a_reason_copied_from_another_file_fails(self) -> None:
        self.assertEqual(self.found(self.entry("document-mode", "a.md", "Reference: under `What the field calls it`.")),
                         ["the answer for a.md (document-mode) quotes `What the field calls it`, which is not in that file"])

    def test_an_answer_with_no_quote_fails_unless_its_check_is_optional(self) -> None:
        answer = self.entry("logical-lines", "b.md", "One role. It stays whole.")
        self.assertTrue(self.found(answer)[0].startswith("the answer for b.md (logical-lines) quotes nothing"))
        self.assertEqual(self.found(answer, optional=["logical-lines"]), [])

    def test_a_path_question_may_quote_an_entry_or_the_other_file(self) -> None:
        self.assertEqual(self.found(self.entry("tree-shape", "notes", "It stays: `one.md` is its only entry."),
                                    self.entry("co-change", "a.md", "No: `b.md` changed with it in one pass.")), [])
        self.assertEqual(len(self.found(self.entry("tree-shape", "notes", "It stays: `two.md`."))), 1)

    def test_a_stale_or_missing_answer_is_left_to_the_judgment_step(self) -> None:
        self.assertEqual(self.found(self.entry("document-mode", "a.md", "Reference: `anything`.", file="000000000000"),
                                    self.entry("document-mode", "gone.md", "Reference: `anything`.", file="")), [])

    def test_a_line_the_file_does_not_have_fails(self) -> None:
        found = self.found(self.entry("logical-lines", "a.md", "One role, `Text`, from line 5 to line 9."))
        self.assertEqual(found, ["the answer for a.md (logical-lines) cites line 9; the file has 5"])

    def test_no_answers_file_or_a_broken_one(self) -> None:
        self.assertEqual(judgment_quotes.check(self.root, CONFIG), [])
        self.write("checks/judgments.toml", "[[answer]\nbroken")
        found = [finding.message for finding in judgment_quotes.check(self.root, CONFIG)]
        self.assertTrue(found and found[0].startswith("the answers file cannot be read as TOML"), found)


DECISION_RECORD = ("# 0001: Pin the links\n\n**Decision:** Links name the commit.\n\n"
               "**Status:** accepted, 2026-10-29. **Shape:** [decision record](../shapes/decision-record.md).\n")


class TestDecisionRecords(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        self.config = {}
        (self.root / "decisions").mkdir()
        self.index("0001-pin-the-links.md", "0002-move-the-pin.md")

    def tearDown(self) -> None:
        shutil.rmtree(self.root)

    def index(self, *names: str) -> None:
        rows = "".join(f"| [{name[:4]}]({name}) |\n" for name in names)
        (self.root / "decisions" / "README.md").write_text(f"# Decisions\n\n{rows}", encoding="utf-8")

    def found(self, name: str, text: str, kind: str = "") -> list[str]:
        (self.root / "decisions" / name).write_text(text, encoding="utf-8")
        return [finding.message for finding in decision_records.check(self.root, self.config) if not kind or finding.kind == kind]

    def test_a_complete_record_passes(self) -> None:
        self.assertEqual(self.found("0001-pin-the-links.md", DECISION_RECORD), [])

    def test_the_readme_is_not_a_record(self) -> None:
        self.assertEqual(self.found("README.md", "# Decisions\n"), [])

    def test_a_title_with_another_number_fails(self) -> None:
        found = self.found("0001-pin-the-links.md", DECISION_RECORD.replace("# 0001:", "# 0002:"))
        self.assertEqual(len(found), 1)
        self.assertIn("'# 0001: '", found[0])

    def test_a_gap_in_the_numbers_fails(self) -> None:
        found = self.found("0002-move-the-pin.md", DECISION_RECORD.replace("# 0001:", "# 0002:"))
        self.assertEqual(len(found), 1)
        self.assertIn("0001 was due", found[0])

    def test_a_record_the_readme_does_not_link_fails(self) -> None:
        self.index("0002-move-the-pin.md")
        found = self.found("0001-pin-the-links.md", DECISION_RECORD)
        self.assertEqual(found, ["the README does not link 0001-pin-the-links.md"])

    def test_a_folder_without_a_readme_fails(self) -> None:
        (self.root / "decisions" / "README.md").unlink()
        found = self.found("0001-pin-the-links.md", DECISION_RECORD)
        self.assertEqual(len(found), 1)
        self.assertIn("needs a README", found[0])

    def test_a_decision_not_first_fails(self) -> None:
        text = DECISION_RECORD.replace("**Decision:** Links name the commit.\n\n", "Some context first.\n\n**Decision:** Links name the commit.\n\n")
        found = self.found("0001-pin-the-links.md", text)
        self.assertEqual(len(found), 1)
        self.assertIn("rule 2", found[0])

    def test_a_status_without_its_word_or_date_fails_twice(self) -> None:
        found = self.found("0001-pin-the-links.md", DECISION_RECORD.replace("accepted, 2026-10-29.", "in force."))
        self.assertEqual(len(found), 2)

    def test_a_superseded_record_without_its_successor_fails(self) -> None:
        found = self.found("0001-pin-the-links.md", DECISION_RECORD.replace("accepted, 2026-10-29.", "superseded, 2026-10-29."))
        self.assertEqual(len(found), 1)
        self.assertIn("rule 4", found[0])

    def test_a_status_linking_a_missing_record_fails(self) -> None:
        text = DECISION_RECORD.replace("accepted, 2026-10-29.", "superseded by [0002](0002-move-the-pin.md), 2026-10-29.")
        found = self.found("0001-pin-the-links.md", text)
        self.assertEqual(found, ["the status links 0002-move-the-pin.md, which is not in decisions/"])

    def test_consequences_without_a_bad_line_ask_a_question(self) -> None:
        text = DECISION_RECORD + "\n## Consequences\n\n- Good: the links hold.\n\n## See also\n"
        self.assertEqual(self.found("0001-pin-the-links.md", text), [])  # off by default
        self.config = {"decision_records": {"ask_costs": True}}
        self.assertEqual(self.found("0001-pin-the-links.md", text, "error"), [])
        asked = self.found("0001-pin-the-links.md", text, "judgment")
        self.assertEqual(len(asked), 1)
        self.assertIn("rule 3", asked[0])

    def test_consequences_with_a_bad_line_ask_nothing(self) -> None:
        text = DECISION_RECORD + "\n## Consequences\n\n- Good: the links hold.\n- Bad: long addresses.\n\n## See also\n"
        self.assertEqual(self.found("0001-pin-the-links.md", text), [])

    def test_a_record_without_its_shape_line_fails(self) -> None:
        found = self.found("0001-pin-the-links.md", DECISION_RECORD.replace(" **Shape:** [decision record](../shapes/decision-record.md).", ""))
        self.assertEqual(len(found), 1)
        self.assertIn("names its shape", found[0])

    def test_a_record_without_decision_or_status_fails_twice(self) -> None:
        text = DECISION_RECORD.replace("**Decision:**", "Decision:").replace("**Status:**", "Status:")
        self.assertEqual(len(self.found("0001-pin-the-links.md", text)), 2)

    def test_no_decisions_folder_means_nothing_to_check(self) -> None:
        shutil.rmtree(self.root / "decisions")
        self.assertEqual(decision_records.check(self.root, self.config), [])


class TestShapeExample(unittest.TestCase):
    """Ported from the learning extension's check: a shape shows, or links, a filled example of itself."""

    def found(self, files: dict[str, str]) -> list[str]:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name, text in files.items():
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                (root / name).write_text(text)
            config = {"shape_example": {"files": ["shapes/*.md"], "exempt": ["shapes/examples/"]}}
            return [finding.path for finding in shape_example.check(root, config)]

    def test_an_example_linked_both_ways_passes(self) -> None:
        self.assertEqual(self.found({"shapes/s.md": "# S\n\n[example](examples/e.md)\n",
                                     "shapes/examples/e.md": "# E\n\n**Shape:** [s](../s.md)\n"}), [])

    def test_a_skeleton_alone_warns(self) -> None:
        self.assertEqual(self.found({"shapes/s.md": "# S\n\nA skeleton only.\n"}), ["shapes/s.md"])

    def test_an_example_must_link_back(self) -> None:
        self.assertEqual(self.found({"shapes/s.md": "# S\n\n[example](examples/e.md)\n",
                                     "shapes/examples/e.md": "# E\n\nNo link back.\n"}), ["shapes/s.md"])

    def test_a_citation_is_not_an_example(self) -> None:
        self.assertEqual(self.found({"shapes/s.md": "# S\n\n[evidence](../evidence/r.md)\n",
                                     "evidence/r.md": "# R\n\nSee the [shape](../shapes/s.md).\n"}), ["shapes/s.md"])

    def test_an_html_example_counts_by_its_name(self) -> None:
        self.assertEqual(self.found({"shapes/s.md": "# S\n\n[deck](example-s.html)\n", "shapes/example-s.html": "<html></html>"}), [])
        self.assertEqual(self.found({"shapes/s.md": "# S\n\n[template](s.tex)\n", "shapes/s.tex": "% skeleton"}), ["shapes/s.md"])

    def test_an_inline_example_passes(self) -> None:
        self.assertEqual(self.found({"shapes/s.md": "# S\n\n## Worked example\n\nA filled one.\n"}), [])

    def test_a_derived_shape_is_not_an_example(self) -> None:
        self.assertEqual(self.found({"shapes/base.md": "# Base\n\n[derived](derived.md)\n",
                                     "shapes/derived.md": "# Derived\n\nDerives from [base](base.md).\n\n## Worked example\n\nx\n"}),
                         ["shapes/base.md"])


class TestContrast(ScratchRepository):
    def found(self, css: str, **settings) -> list[str]:
        self.write("site.css", css)
        config = dict(CONFIG, sufficient_contrast={"stylesheets": ["site.css"], **settings})
        return [f"{finding.kind} {finding.message}" for finding in sufficient_contrast.check(self.root, config)]

    def test_a_variable_is_read_from_its_theme(self) -> None:
        found = self.found(":root { --fg: #777; --paper: #fff; }\n.card { color: var(--fg); background: var(--paper); }\n"
                           "@media (prefers-color-scheme: dark) { :root { --paper: #111; --fg: #000; } }\n")
        self.assertEqual(len(found), 2, found)
        self.assertIn("error .card: color #777 on #fff is 4.48:1, under 4.5:1", found)
        self.assertTrue(any("theme @media (prefers-color-scheme: dark) :root" in line for line in found), found)

    def test_inherited_text_is_measured_on_the_page_and_named_surfaces(self) -> None:
        css = ("html, body { background: #131520; }\n.muted { color: #6B6B80; }\n"
               ".slide-light { background: #F9F5F0; color: #1B1B2F; }\n.title { color: #E8652D; }\n"
               "@keyframes glow { from { color: #fff; } to { color: #000; } }\n")
        page_only = self.found(css)
        self.assertEqual(page_only, ["warning #6b6b80 (.muted) on html or body (#131520) is 3.50:1, under 4.5:1, if it sits there"])
        with_surface = self.found(css, surfaces=[".slide-light"])
        self.assertIn("warning #e8652d (.title) on .slide-light (#f9f5f0) is 3.06:1, under 4.5:1, if it sits there", with_surface)

    def test_a_colour_and_a_background_set_in_two_rules_meet(self) -> None:
        found = self.found(".note { color: #777; }\n.note, .aside { background: #fff; }\n:is(.a, .b) { color: #000; }\n")
        self.assertEqual(found, ["error .note: color #777 on #fff is 4.48:1, under 4.5:1"])


if __name__ == "__main__":
    unittest.main()
