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

from meaning import document_mode, embeddings, name_content, paraphrase, section_cohesion
from program import (co_change, cross_file_terms, decision_records, defined_before_use, duplication, figure_captions, figure_width, figures_present, judgment_quotes, links,
                     logical_lines, long_sentences, name_matches_title, outline_depth, overview_first, paragraph_length,
                     portable_paths, principle_coverage, provisional_tags, readable_measure, references, shape_conformance,
                     standard_card, sufficient_contrast, tree_shape, type_buckets)
import run
from syntax import clause_nesting, dependency_length, parser, sentence_links

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

    def test_name_content(self) -> None:
        self.write("contrast-ratio.md", "# Contrast ratio\n\nThe contrast ratio between text and background, and how to measure it.\n")
        self.write("travel-budget.md", "A proof that every planar graph can be coloured with four colours.\n")
        found = [finding.path for finding in name_content.check(self.root, dict(CONFIG, name_content={"threshold": 0.3}))]
        self.assertEqual(found, ["travel-budget.md"])

    def test_section_cohesion(self) -> None:
        body = " ".join(["The reader keeps the structure of the text in mind while reading each part of it."] * 3)
        stray = " ".join(["Preheat the oven, butter the tin, and bake the sponge cake for twenty five minutes."] * 3)
        self.write("a.md", f"# A\n\n## One\n\n{body}\n\n## Two\n\n{body}\n\n## Three\n\n{body}\n\n## Cake\n\n{stray}\n")
        found = [finding.message for finding in section_cohesion.check(self.root, dict(CONFIG, section_cohesion={"min_words": 20, "threshold": 0.5}))]
        self.assertEqual(len(found), 1, found)
        self.assertIn("'Cake'", found[0])

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

    def test_sentence_links(self) -> None:
        self.write("a.md", "The parser reads each sentence. The parser names the subject. Its verb follows. This order holds.\n\n"
                   "Rain fell on Tuesday. Copper conducts heat. Owls hunt at night. Bread rises with yeast.\n")
        found = sentence_links.check(self.root, dict(CONFIG, sentence_links={"max_unlinked": 0.5}))
        self.assertEqual([finding.line for finding in found], [3], found)

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


class TestFigureWidth(ScratchRepository):
    def found(self, text: str) -> list[str]:
        self.write("a.md", "# A page\n\n" + text)
        return [finding.message for finding in figure_width.check(self.root, CONFIG)]

    def test_a_text_figure_wider_than_the_column_warns(self) -> None:
        self.assertEqual(len(self.found("```text\nnode " + "x" * 70 + "\n```\n")), 1)
        self.assertEqual(len(self.found("```\n" + "y" * 61 + "\n```\n")), 1)

    def test_descriptions_under_their_nodes_pass(self) -> None:
        self.assertEqual(self.found("```text\ntree\n ├─ a node\n │    its description, on the line below\n └─ another\n```\n"), [])

    def test_code_with_a_language_is_left_alone(self) -> None:
        self.assertEqual(self.found("```python\nx = " + "1 + " * 30 + "1\n```\n"), [])

    def test_a_wide_character_counts_twice(self) -> None:
        self.assertEqual(figure_width.columns("名前" + "a" * 3), 7)
        self.assertEqual(len(self.found("```text\n" + "名" * 31 + "\n```\n")), 1)


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


class TestBibliographyKeys(unittest.TestCase):
    """A family of two repositories side by side: this one, checked, and its sibling."""

    def setUp(self) -> None:
        self.folder = tempfile.TemporaryDirectory()
        self.family = Path(self.folder.name)

    def tearDown(self) -> None:
        self.folder.cleanup()

    def bibliography(self, repository: str, *rows: str) -> None:
        path = self.family / repository / "evidence" / "bibliography.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("| Key | Citation | Link |\n|---|---|---|\n" + "".join(f"| {row} |\n" for row in rows), encoding="utf-8")

    def found(self, **settings) -> list[str]:
        from program import bibliography_keys
        return [f"{finding.kind} {finding.line} {finding.message}"
                for finding in bibliography_keys.check(self.family / "this", {"bibliography_keys": settings})]

    def test_a_key_held_twice_in_one_file_is_an_error(self) -> None:
        self.bibliography("this", "Yang 2021 | Testing | https://doi.org/10.1037/a", "Yang 2021 | Passion | https://doi.org/10.3389/b")
        self.assertEqual(self.found(), ["error 4 key 'Yang 2021' is also the key of line 3: a citation cannot say which it means"])

    def test_one_work_under_two_keys_warns_unless_its_link_is_shared_on_purpose(self) -> None:
        self.bibliography("this", "Minto 1987 | The book | https://www.barbaraminto.com/", "Minto 2026 | The site | https://barbaraminto.com")
        self.assertEqual(self.found(), ["warning 4 'Minto 2026' and 'Minto 1987' (line 3) name one work, barbaraminto.com: give it one key"])
        self.assertEqual(self.found(shared_links=["https://www.barbaraminto.com/"]), [])

    def test_the_family_shares_one_set_of_keys(self) -> None:
        self.bibliography("this", "Yang 2021 | Passion | https://doi.org/10.3389/b", "Hartley 2004a | Abstracts | https://pmc.example/PMC4/",
                          "Chatlatanagulchai 2026 | Agent READMEs | arXiv:2511.12884", "Knuth 1989 | Writing | https://www.example.org/knuth.pdf")
        self.bibliography("that", "Yang 2021 | Testing | https://doi.org/10.1037/A", "Hartley 2004 | Abstracts | https://pmc.example/PMC4",
                          "Chatlatanagulchai 2026 | Agent READMEs | https://arxiv.org/abs/2511.12884v2", "Knuth 1989 | Writing | http://example.org/knuth.pdf")
        self.assertEqual(self.found(family=["that"]), [
            "warning 3 'Yang 2021' names another work in that (line 3, doi:10.1037/a): one key, one work across the family",
            "warning 4 'Hartley 2004a' is 'Hartley 2004' in that (line 4, pmc.example/pmc4): one work, one key across the family"])

    def test_a_preprint_named_in_the_citation_is_the_same_work(self) -> None:
        self.bibliography("this", "Liang 2024 | Model cards. Nature Machine Intelligence; preprint arXiv:2402.05160 | https://doi.org/10.1038/s42256",
                          "Gebru 2021 | Datasheets; preprint arXiv:1803.09010 | https://doi.org/10.1145/3458723")
        self.bibliography("that", "Liang 2024 | Model cards, preprint | https://arxiv.org/abs/2402.05160v2",
                          "Gebru 2018 | Datasheets, preprint | https://arxiv.org/abs/1803.09010")
        self.assertEqual(self.found(family=["that"]), [
            "warning 4 'Gebru 2021' is 'Gebru 2018' in that (line 4, arxiv:1803.09010): one work, one key across the family"])

    def test_this_repository_in_its_own_family_is_skipped_and_a_missing_member_is_reported(self) -> None:
        self.bibliography("this", "Liu 2024 | Lost in the middle | https://doi.org/10.1162/tacl")
        self.assertEqual(self.found(family=["this", "gone"]), [
            "warning 0 family member 'gone' has no evidence/bibliography.md beside this repository: its keys were not compared"])


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


if __name__ == "__main__":
    unittest.main()
