"""The checks' own oracle: each check must find a violation planted in a scratch repository,
and nothing in a clean one. Run: python3 -m unittest discover checks
"""
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from meaning import document_mode, embeddings, paraphrase
from program import (co_change, cross_file_terms, defined_before_use, duplication, figure_captions, figures_present, links,
                     logical_lines, long_sentences, name_matches_title, outline_depth, overview_first, paragraph_length,
                     portable_paths, principle_coverage, provisional_tags, readable_measure, references, shape_conformance,
                     sufficient_contrast, tree_shape, type_buckets)
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

    def test_clause_nesting(self) -> None:
        self.write("a.md", "The rat that the cat that the dog chased killed ate the malt.\n\nThe cat sat on the mat.\n")
        found = clause_nesting.check(self.root, dict(CONFIG, clause_nesting={"max_depth": 1}))
        self.assertEqual(len(found), 1, found)


class TestCleanRepository(ScratchRepository):
    def test_nothing_found(self) -> None:
        self.write("guide/README.md", "See [the note](note.md).\n")
        self.write("guide/note.md", "**Locality** is the distance between a word and its head. Locality matters.\n")
        self.write("guide/other.md", "A different sentence entirely.\n")
        for module in (portable_paths, links, duplication, defined_before_use):
            self.assertEqual(self.messages(module), [], module.NAME)


if __name__ == "__main__":
    unittest.main()
