"""The meaning and syntax tiers' own oracle: a planted case per check, skipped when the tier's library is missing.

They need an embedding model or a parser that the program tier does not, and change with those tiers; the program
tier's checks are tested in test_checks.py, beside this file. Run: python3 -m unittest discover checks
"""
from __future__ import annotations

import unittest

from meaning import document_mode, embeddings, name_content, paraphrase, section_cohesion
from syntax import clause_nesting, dependency_length, parser, sentence_links
from test_checks import CONFIG, ScratchRepository


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


class TestParserInput(unittest.TestCase):
    def test_the_parser_reads_what_the_reader_reads(self) -> None:
        from syntax import sentences_of
        self.assertEqual(sentences_of.as_read("**Claim:** see [the guide](https://example.org/a_(b))."),
                         "Claim: see the guide.")


if __name__ == "__main__":
    unittest.main()
