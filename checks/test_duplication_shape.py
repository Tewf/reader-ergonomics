"""Duplication and the lines a declared shape prescribes: read from a local file or a sibling checkout, never fetched."""
from __future__ import annotations

import shutil
import unittest

import test_checks
from program import duplication


class DuplicationWithShape(test_checks.ScratchRepository):
    SKELETON_LINE = "The pointer line that every instance of this shape repeats word for word."

    def shaped(self, name: str, link: str) -> None:
        self.write(name, f"**Shape:** [x]({link})\n\n{self.SKELETON_LINE}\n")

    def test_duplication_skips_the_skeleton_of_a_local_shape(self) -> None:
        self.write("shapes/x.md", f"# Shape: x\n\n## Skeleton\n\n```markdown\n{self.SKELETON_LINE}\n```\n")
        self.shaped("one.md", "shapes/x.md")
        self.shaped("two.md", "shapes/x.md")
        self.assertEqual(self.messages(duplication), [])

    def test_duplication_skips_the_skeleton_of_a_github_link(self) -> None:
        self.write("shapes/x.md", f"# Shape: x\n\n## Skeleton\n\n```markdown\n{self.SKELETON_LINE}  comment\n```\n")
        link = f"https://github.com/Tewf/{self.root.name}/blob/abc123/shapes/x.md"
        self.shaped("one.md", link)
        self.shaped("two.md", link)
        self.assertEqual(self.messages(duplication), [])
        sibling = self.root.parent / f"{self.root.name}-sibling"
        (sibling / "shapes").mkdir(parents=True)
        self.addCleanup(shutil.rmtree, sibling)
        (sibling / "shapes" / "y.md").write_text(f"## Skeleton\n\n```markdown\n{self.SKELETON_LINE}\n```\n")
        other = f"https://github.com/Tewf/{sibling.name}/blob/abc123/shapes/y.md"
        self.shaped("three.md", other)
        self.shaped("four.md", other)
        self.assertEqual(self.messages(duplication), [])

    def test_duplication_counts_as_before_when_the_shape_cannot_be_read(self) -> None:
        self.shaped("one.md", "shapes/missing.md")
        self.shaped("two.md", "shapes/missing.md")
        self.shaped("three.md", "https://github.com/Tewf/not-beside-here/blob/abc123/shapes/x.md")
        self.shaped("four.md", "https://github.com/Tewf/not-beside-here/blob/abc123/shapes/x.md")
        self.assertEqual(len(self.messages(duplication)), 3)


if __name__ == "__main__":
    unittest.main()
