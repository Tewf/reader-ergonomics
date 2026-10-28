"""The checks' own oracle: each check must find a violation planted in a scratch repository,
and nothing in a clean one. Run: python3 -m unittest discover checks
"""
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

import defined_before_use
import duplication
import links
import logical_lines
import portable_paths
import tree_shape

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
    def test_portable_paths(self) -> None:
        self.write("notes/a:b.md")
        self.write("notes/Same.md")
        self.write("notes/same.md")
        self.write("notes/draft .md")
        self.write("notes/NUL.txt")
        self.write("notes/ends.")
        found = " ".join(self.messages(portable_paths))
        self.assertIn("forbidden character", found)
        self.assertIn("only by case", found)
        self.assertIn("space before the extension", found)
        self.assertIn("reserved device name", found)
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


class TestCleanRepository(ScratchRepository):
    def test_nothing_found(self) -> None:
        self.write("guide/README.md", "See [the note](note.md).\n")
        self.write("guide/note.md", "**Locality** is the distance between a word and its head. Locality matters.\n")
        self.write("guide/other.md", "A different sentence entirely.\n")
        for module in (portable_paths, links, duplication, defined_before_use):
            self.assertEqual(self.messages(module), [], module.NAME)


if __name__ == "__main__":
    unittest.main()
