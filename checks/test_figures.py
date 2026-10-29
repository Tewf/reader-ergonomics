"""The figure checks' oracle: each finds a fault planted in a page, and nothing in a figure drawn as the rule asks.

Run: python3 -m unittest discover checks
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from figures import figure_alt, figure_contrast, figure_source, figure_source_inline, figure_width, typed_figure
from test_checks import CONFIG, ScratchRepository


class TestFigureSourceInline(ScratchRepository):
    DOT = "digraph g { a -> b; }\n"

    def page(self, under: str) -> list[str]:
        self.write("fig.dot", self.DOT)
        self.write("fig.svg", "<svg/>\n")
        self.write("a.md", "# A\n\n![a goes to b](fig.svg)\n" + under)
        return [f"{finding.kind} {finding.message}" for finding in figure_source_inline.check(self.root, CONFIG)]

    def test_a_folded_copy_equal_to_its_file_passes(self) -> None:
        self.assertEqual(self.page("\n<details>\n<summary>Graphviz source</summary>\n\n```dot\n" + self.DOT + "```\n\n</details>\n"), [])

    def test_a_copy_that_drifted_is_an_error(self) -> None:
        found = self.page("\n<details>\n<summary>Graphviz source</summary>\n\n```dot\ndigraph g { a -> c; }\n```\n\n</details>\n")
        self.assertEqual(len(found), 1)
        self.assertTrue(found[0].startswith("error the source folded under fig.svg differs"), found)

    def test_a_figure_with_no_folded_source_warns(self) -> None:
        found = self.page("\nText.\n")
        self.assertEqual(len(found), 1)
        self.assertTrue(found[0].startswith("warning fig.svg has no folded source"), found)

    def test_an_image_with_no_dot_beside_it_is_not_checked(self) -> None:
        self.write("photo.svg", "<svg/>\n")
        self.write("b.md", "# B\n\n![a photograph](photo.svg)\n")
        self.assertEqual(figure_source_inline.check(self.root, CONFIG), [])


class TestFigureChecks(unittest.TestCase):
    """Ported from the presentations extension's figure checks, with their own planted cases."""
    TYPED = "Intro.\n\n```text\n a ──▶ b\n```\n"
    SETTINGS = {"typed_figure": {"exempt": ["*AGENTS.md", "*CLAUDE.md"]}}

    def run_on(self, module, files: dict[str, str]):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name, text in files.items():
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                (root / name).write_text(text, encoding="utf-8")
            return module.check(root, {**CONFIG, **self.SETTINGS})

    def test_typed_figure_flags_box_drawing_in_a_page(self) -> None:
        found = self.run_on(typed_figure, {"README.md": self.TYPED})
        self.assertEqual([(f.check, f.line, f.kind) for f in found], [("typed-figure", 3, "warning")])

    def test_typed_figure_spares_exempt_files_and_code(self) -> None:
        code = "```python\nprint('a ──▶ b')\n```\n"
        self.assertEqual(self.run_on(typed_figure, {"AGENTS.md": self.TYPED, "notes/AGENTS.md": self.TYPED, "x.md": code}), [])

    def test_figure_alt_flags_a_file_name_and_a_kind(self) -> None:
        page = "![flow.svg](flow.svg)\n\n![Diagram](levels.svg)\n\n![flow](figures/flow.svg)\n"
        self.assertEqual([f.line for f in self.run_on(figure_alt, {"a.md": page})], [1, 3, 5])

    def test_figure_alt_accepts_a_sentence_and_leaves_empty_alt_to_figure_captions(self) -> None:
        page = "![Three levels, each depending on the one below.](where.svg)\n\n![](x.svg)\n"
        self.assertEqual(self.run_on(figure_alt, {"a.md": page}), [])

    def test_figure_source_checks_the_stamp_against_the_dot(self) -> None:
        import hashlib
        dot = "digraph g { a -> b }\n"
        good = f"<?xml version='1.0'?>\n<!-- source-sha256: {hashlib.sha256(dot.encode()).hexdigest()} -->\n<svg></svg>"
        self.assertEqual(self.run_on(figure_source, {"f.dot": dot, "f.svg": good}), [])
        stale = self.run_on(figure_source, {"f.dot": dot + "// edited\n", "f.svg": good})
        unstamped = self.run_on(figure_source, {"f.dot": dot, "f.svg": "<svg></svg>"})
        self.assertEqual([len(stale), len(unstamped)], [1, 1])
        self.assertEqual(self.run_on(figure_source, {"lone.svg": "<svg></svg>"}), [])

    def test_figure_contrast_flags_faint_and_alpha_strokes(self) -> None:
        svg = ('<svg><style>.box { fill: #FFFFFF; stroke: #10101459; }\n'
               '@media (prefers-color-scheme: dark) { .box { fill: #1A1A20; stroke: #333333; } }</style>'
               '<path stroke="#dddddd" fill="none"/><text fill="#eeeeee">x</text></svg>')
        messages = [f.message for f in self.run_on(figure_contrast, {"f.svg": svg})]
        self.assertEqual(len(messages), 4, messages)  # alpha; dark stroke against page and fill; faint path
        self.assertTrue(any("alpha" in m for m in messages))

    def test_figure_contrast_accepts_the_family_palette(self) -> None:
        svg = ('<svg><style>.box { fill: #FFFFFF; stroke: #6A6D77; }\n'
               '@media (prefers-color-scheme: dark) { .box { fill: #1A1A20; stroke: #9A9CA4; } }</style>'
               '<path stroke="#2e7d4f" fill="#e6f2ea"/><polygon stroke="transparent" fill="white"/>'
               '<polygon fill="#3d434b" stroke="#3d434b"/></svg>')  # an arrowhead: a solid shape
        self.assertEqual(self.run_on(figure_contrast, {"f.svg": svg}), [])


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


if __name__ == "__main__":
    unittest.main()
