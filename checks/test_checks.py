"""The checks' own oracle: each check must find a violation planted in a scratch repository,
and nothing in a clean one. Run: python3 -m unittest discover checks
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from meaning import document_mode, embeddings, paraphrase
from program import (co_change, cross_file_terms, defined_before_use, duplication, figure_captions, figures_present, judgment_quotes, links,
                     logical_lines, long_sentences, name_matches_title, outline_depth, overview_first, paragraph_length,
                     portable_paths, principle_coverage, provisional_tags, readable_measure, references, shape_conformance,
                     standard_card, sufficient_contrast, tree_shape, type_buckets)
import run
from syntax import clause_nesting, dependency_length, parser

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


@unittest.skipUnless(embeddings.available(), "fastembed is not installed")
class TestMeaningTier(ScratchRepository):
    def test_paraphrase(self) -> None:
        self.write("a/x.md", "Readers remember the ideas at the top of a text much better than the details that sit deep below them.\n")
        self.write("b/y.md", "People recall the top-level ideas of a text far better than the details placed deep underneath them.\n")
        self.write("c/z.md", "The build runs on every push and stores its cache between runs so that installs stay quick today.\n")
        found = paraphrase.check(self.root, dict(CONFIG, paraphrase={"threshold": 0.8, "min_words": 10}))
        self.assertEqual([finding.path for finding in found], ["a/x.md"], found)

    def test_document_mode_runs(self) -> None:
        self.write("a.md", "\n".join(f"Step {index}: do the next thing." for index in range(25)) + "\n")
        self.assertIsInstance(document_mode.check(self.root, CONFIG), list)


@unittest.skipUnless(parser.available(), "spaCy with en_core_web_sm is not installed")
class TestSyntaxTier(ScratchRepository):
    def test_dependency_length(self) -> None:
        self.write("a.md", "The cat sat.\n\nThe report that the committee which the board appointed in the spring of the year "
                   "before last after long and careful deliberation finally wrote was rejected.\n")
        found = dependency_length.check(self.root, dict(CONFIG, dependency_length={"max_distance": 10}))
        self.assertEqual(len(found), 1, found)

    def test_dependency_length_skips_links_between_complete_clauses(self) -> None:
        self.write("a.md", "The program checks the form of every identifier in the bibliography without the network, and "
                   "the weekly job resolves each one.\n\nThe tests run on every push of every branch to the "
                   "repository; the site is rendered again.\n")
        self.write("README.fr.md", "Les notes que le lecteur garde en mémoire pendant toute la lecture du long "
                   "paragraphe restent cognitives.\n")
        found = dependency_length.check(self.root, dict(CONFIG, dependency_length={"max_distance": 10}))
        self.assertEqual(found, [])

    def test_clause_nesting(self) -> None:
        self.write("a.md", "The rat that the cat that the dog chased killed ate the malt.\n\nThe cat sat on the mat.\n")
        found = clause_nesting.check(self.root, dict(CONFIG, clause_nesting={"max_depth": 1}))
        self.assertEqual(len(found), 1, found)

    def test_clause_nesting_ignores_clauses_at_the_end(self) -> None:
        self.write("a.md", "The board said that the committee thought that the report showed that the plan failed.\n\n"
                   "The man left before it rained, and the dog barked.\n\n"
                   "The text is plain before it is read: headings name it.\n")
        found = clause_nesting.check(self.root, dict(CONFIG, clause_nesting={"max_depth": 0}))
        self.assertEqual(found, [])


class TestCleanRepository(ScratchRepository):
    def test_nothing_found(self) -> None:
        self.write("guide/README.md", "See [the note](note.md).\n")
        self.write("guide/note.md", "**Locality** is the distance between a word and its head. Locality matters.\n")
        self.write("guide/other.md", "A different sentence entirely.\n")
        for module in (portable_paths, links, duplication, defined_before_use):
            self.assertEqual(self.messages(module), [], module.NAME)


class TestJudgmentAnswers(ScratchRepository):
    def test_an_answer_holds_until_its_file_changes(self) -> None:
        from framework import judgment
        from framework.check_api import Finding
        self.write("long.md", "first version\n")
        question = [Finding("logical-lines", "long.md", 0, "state this file's role in one sentence", "judgment")]
        self.assertIn("1 written", judgment.dispatch(self.root, question, "flag", {}))
        stub = (self.root / "checks" / "out" / "judgments-to-answer.toml").read_text(encoding="utf-8")
        self.write("checks/judgments.toml", stub.replace('answer = ""', 'answer = "one role: the long note"'))
        self.assertIn("1 answered in checks/judgments.toml, backend flag", judgment.dispatch(self.root, question, "flag", {}))
        self.assertFalse((self.root / "checks" / "out" / "needs-judgment.md").exists())
        self.write("long.md", "second version\n")
        self.assertIn("0 answered in checks/judgments.toml, 1 written", judgment.dispatch(self.root, question, "flag", {}))


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


class TestGuarantees(unittest.TestCase):
    def test_every_check_states_what_it_guarantees_and_its_cost(self) -> None:
        import ast
        for module in run.CHECKS:
            docstring = ast.get_docstring(ast.parse(Path(module.__file__).read_text(encoding="utf-8"))) or ""
            self.assertIn("Time O(", docstring, module.NAME)
            self.assertTrue(standard_card.guarantee(docstring), module.NAME)


class TestFailurePaths(ScratchRepository):
    """Each way a run can go wrong is reported, never passed over: most severe failures come from error paths."""

    def test_an_unreachable_reference_is_reported_and_not_cached(self) -> None:
        import json
        import urllib.error
        self.write("refs.md", "https://down.example/a\n")

        def refuse(url, method="GET", timeout=20):
            raise urllib.error.URLError("unreachable")
        original, references.fetch = references.fetch, refuse
        try:
            found = [f"{finding.kind} {finding.message}" for finding in references.check(self.root, {**CONFIG, "online": True})]
        finally:
            references.fetch = original
        self.assertEqual(found, ["error link https://down.example/a: URLError"])
        cache = json.loads((self.root / "checks" / "out" / "references-cache.json").read_text())
        self.assertEqual(cache, {})

    def test_a_server_that_does_not_answer_in_time_is_a_warning(self) -> None:
        import socket
        import urllib.error
        self.write("refs.md", "https://slow.example/a and https://slower.example/b\n")

        def wait(url, method="GET", timeout=20):
            if "slower" in url:
                raise urllib.error.URLError(socket.timeout("timed out"))
            raise TimeoutError("timed out")
        original, references.fetch = references.fetch, wait
        try:
            found = sorted(f"{finding.kind} {finding.message}" for finding in references.check(self.root, {**CONFIG, "online": True}))
        finally:
            references.fetch = original
        self.assertEqual(found, ["warning link https://slow.example/a: no answer in time; open it by hand",
                                 "warning link https://slower.example/b: no answer in time; open it by hand"])

    def test_a_missing_judgment_backend_falls_back_to_flag(self) -> None:
        import os
        from unittest import mock
        from framework import judgment
        from framework.check_api import Finding
        self.write("a.md")
        question = [Finding("logical-lines", "a.md", 0, "state its role", "judgment")]
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertIn("fell back to flag", judgment.dispatch(self.root, question, "local", {}))
            self.assertIn("paid and is off", judgment.dispatch(self.root, question, "api", {}))
        self.assertTrue((self.root / "checks" / "out" / "needs-judgment.md").exists())

    def test_an_unreachable_model_leaves_the_question_open(self) -> None:
        import os
        from unittest import mock
        from framework import judgment
        from framework.check_api import Finding
        self.write("a.md")
        question = [Finding("logical-lines", "a.md", 0, "state its role", "judgment")]
        address = {"READER_ERGONOMICS_LOCAL_URL": "http://127.0.0.1:9", "READER_ERGONOMICS_LOCAL_MODEL": "none"}
        with mock.patch.dict(os.environ, address, clear=True):
            judgment.dispatch(self.root, question, "local", {"timeout_seconds": 2})
        self.assertIn("(no answer: URLError)", (self.root / "checks" / "out" / "needs-judgment.md").read_text())

    def test_a_missing_config_or_an_unknown_parent_fails_loudly(self) -> None:
        with self.assertRaises(FileNotFoundError):
            run.load_config(self.root, self.root / "checks" / "nowhere.toml")
        self.write("checks/config.toml", 'extends = "reader-ergonomic"\n')
        with self.assertRaises(ValueError):
            run.load_config(self.root)

    def test_a_missing_stylesheet_is_reported(self) -> None:
        config = dict(CONFIG, readable_measure={"stylesheets": ["gone.css"]}, sufficient_contrast={"stylesheets": ["gone.css"]})
        for module in (readable_measure, sufficient_contrast):
            found = [f"{finding.kind} {finding.message}" for finding in module.check(self.root, config)]
            self.assertEqual(found, ["warning a stylesheet listed in config does not exist, so it was not measured"], module.NAME)

    def test_a_run_that_reads_nothing_fails(self) -> None:
        import sys
        script = Path(__file__).with_name("run.py")
        empty = subprocess.run([sys.executable, str(script), str(self.root)], capture_output=True, text=True)
        self.assertEqual(empty.returncode, 2)
        self.assertIn("nothing was checked", empty.stdout)
        absent = subprocess.run([sys.executable, str(script), str(self.root / "absent")], capture_output=True, text=True)
        self.assertEqual(absent.returncode, 2)
        self.assertIn("is not a folder", absent.stderr)


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


class TestCitationKeys(unittest.TestCase):
    def test_a_surname_keeps_its_particle(self) -> None:
        from program import citations
        keys = [match.group(1) for match in citations.CITATION.finditer(
            "ter Beek 2022, ten Cate 2014 and van der Meer 2019 agree; after 2022, nothing.")]
        self.assertEqual(keys, ["ter Beek", "ten Cate", "van der Meer"])


class TestParserInput(unittest.TestCase):
    def test_the_parser_reads_what_the_reader_reads(self) -> None:
        from syntax import sentences_of
        self.assertEqual(sentences_of.as_read("**Claim:** see [the guide](https://example.org/a_(b))."),
                         "Claim: see the guide.")


class TestSummary(unittest.TestCase):
    def test_a_skipped_tier_is_not_listed_as_run(self) -> None:
        self.assertEqual(run.summary(0, 1, {"program"}, {"meaning"}),
                         "0 error(s), 1 warning(s); tiers run: program; skipped: meaning")
        self.assertEqual(run.summary(2, 0, {"program", "syntax"}, set()), "2 error(s), 0 warning(s); tiers run: program, syntax")


class TestExtension(ScratchRepository):
    """An extension of the standard: its config extends the standard's, its own checks run, its card is its own."""

    def test_config_extends_the_standard(self) -> None:
        self.write("checks/config.toml", 'extends = "reader-ergonomics"\n\n[logical_lines]\ntrigger = 5\n')
        config = run.load_config(self.root)
        self.assertEqual(config["logical_lines"]["trigger"], 5)
        self.assertIn("ceiling", config["logical_lines"])  # kept from the standard's table
        self.assertIn("citations", config)                 # a table the extension did not name
        self.assertNotIn("extends", config)

    def test_config_without_extends_replaces(self) -> None:
        self.write("checks/config.toml", "[logical_lines]\ntrigger = 5\n")
        self.assertNotIn("citations", run.load_config(self.root))

    def test_local_checks_run_and_register(self) -> None:
        self.write("checks/local/demo.py", "from framework.check_api import Finding\nNAME = 'demo-local'\n"
                   "def check(root, config):\n    return [Finding(NAME, 'a.md', 1, 'planted')]\n")
        self.write("a.md", "# A\n\nOne line.\n")
        names = [module.NAME for module in run.local_checks(self.root)]
        self.assertEqual(names, ["demo-local"])
        result = subprocess.run([sys.executable, str(Path(run.__file__)), str(self.root), "--only", "demo-local"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("demo-local", result.stdout)

    def test_card_is_the_extension_s_own(self) -> None:
        self.write("_quarto.yml", 'website:\n  title: "Talks"\n  site-url: "https://example.org/talks/"\n'
                   '  description: "How to give a talk."\n')
        self.write("standard.md", f"# Talks\n\n{standard_card.START}\n{standard_card.END}\n")
        self.write("principles/talk/README.md", "# Talk: a paced medium\n\nWhat changes when a speaker sets the pace.\n")
        self.write("principles/talk/key-terms.md", "# Key terms on screen\n\n**Claim:** show key terms, not the sentences said.\n\n"
                   "- **Grade:** measured.\n")
        built = standard_card.expected(self.root, {"standard_card": {"facets": ["talk"]}})
        self.assertTrue(built["llms.txt"].startswith("# Talks\n\n> How to give a talk."))
        self.assertIn("(https://example.org/talks/principles/talk/key-terms.md)", built["llms.txt"])
        self.assertNotIn("Reader styles", built["llms.txt"])  # this extension has none
        self.assertIn("### Talk: a paced medium", built["standard.md"])


if __name__ == "__main__":
    unittest.main()
