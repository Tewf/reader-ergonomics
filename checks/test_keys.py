"""The citation checks' oracle: a key names one work, in one bibliography and across the family.

Run: python3 -m unittest discover checks
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


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
            "error 3 'Yang 2021' names another work in that (line 3, doi:10.1037/a): one key, one work across the family; "
            "if the two rows are one work, give them one link",
            "warning 4 'Hartley 2004a' is 'Hartley 2004' in that (line 4, pmc.example/pmc4): one work, one key across the family"])

    def test_a_preprint_named_in_the_citation_is_the_same_work(self) -> None:
        self.bibliography("this", "Liang 2024 | Model cards. Nature Machine Intelligence; preprint arXiv:2402.05160 | https://doi.org/10.1038/s42256",
                          "Gebru 2021 | Datasheets; preprint arXiv:1803.09010 | https://doi.org/10.1145/3458723")
        self.bibliography("that", "Liang 2024 | Model cards, preprint | https://arxiv.org/abs/2402.05160v2",
                          "Gebru 2018 | Datasheets, preprint | https://arxiv.org/abs/1803.09010")
        self.assertEqual(self.found(family=["that"]), [
            "warning 4 'Gebru 2021' is 'Gebru 2018' in that (line 4, arxiv:1803.09010): one work, one key across the family"])

    def test_title_words_tell_an_organisation_s_keys_apart(self) -> None:
        self.bibliography("this", "Microsoft 2026 icons | Icons | https://example.org/icons",
                          "Microsoft 2026 ADR | Records | https://example.org/adr",
                          "Microsoft 2026 Icons | Icons again | https://example.org/icons-2")
        self.assertEqual(self.found(), ["error 5 key 'Microsoft 2026 Icons' is also the key of line 3: a citation cannot say which it means"])

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

    def test_an_organisation_s_title_word_joins_its_key_only_when_the_bibliography_holds_it(self) -> None:
        from program import citations
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "evidence").mkdir()
            (root / "evidence" / "bibliography.md").write_text(
                "| Key | Citation | Link |\n|---|---|---|\n| Microsoft 2026 icons | Icons | https://example.org/icons |\n"
                "| Microsoft 2026 ADR | Records | https://example.org/adr |\n| Google 2024 | Style | https://example.org/style |\n"
                "| Unused 2020 word | Unused | https://example.org/unused |\n", encoding="utf-8")
            (root / "evidence" / "note.md").write_text(
                "# Note\n\nMicrosoft 2026 icons and Microsoft 2026 ADR differ. Google 2024 recommends a plain style. "
                "Unused 2020 alone names no row.\n", encoding="utf-8")
            found = sorted(finding.message for finding in citations.check(root, {"citations": {"files": ["evidence/"]}}))
        self.assertEqual(found, ["'Unused 2020' has no entry in evidence/bibliography.md",
                                 "entry 'unused2020word' is cited nowhere"])


if __name__ == "__main__":
    unittest.main()
