"""Properties the checks must hold for every input, tried on generated inputs rather than one example each.

The generators are written with the standard library, as the checks are: each property draws its
cases from a seeded random source, so a run is reproducible. There is no shrinking: a failure
prints the case that broke the property, which is small by construction. Run:
python3 -m unittest discover checks
"""
from __future__ import annotations

import random
import string
import subprocess
import tempfile
import unittest
from pathlib import Path

import run
from framework import judgment
from framework.config import merged
from program import citations, logical_lines, portable_paths, references, sufficient_contrast
from syntax.sentences_of import as_read

CASES = 200


def hex_colour(rng: random.Random) -> str:
    return "".join(rng.choice("0123456789abcdef") for _ in range(6))


def word(rng: random.Random, letters: str = string.ascii_lowercase, low: int = 2, high: int = 9) -> str:
    return "".join(rng.choice(letters) for _ in range(rng.randint(low, high)))


class TestContrastProperties(unittest.TestCase):
    def test_the_ratio_is_symmetric_and_bounded(self) -> None:
        rng = random.Random(1)
        for _ in range(CASES):
            first, second = hex_colour(rng), hex_colour(rng)
            measured = sufficient_contrast.ratio(first, second)
            self.assertAlmostEqual(measured, sufficient_contrast.ratio(second, first), msg=(first, second))
            self.assertGreaterEqual(measured, 1.0, (first, second))
            self.assertLessEqual(measured, 21.0 + 1e-9, (first, second))
            self.assertAlmostEqual(sufficient_contrast.ratio(first, first), 1.0, msg=first)

    def test_a_variable_measures_as_its_literal_would(self) -> None:
        rng = random.Random(2)
        for _ in range(CASES):
            text, background = hex_colour(rng), hex_colour(rng)
            css = f":root {{ --t: #{text}; --b: #{background}; }}\n.x {{ color: var(--t); background: var(--b); }}\n"
            with tempfile.TemporaryDirectory() as folder:
                (Path(folder) / "site.css").write_text(css)
                found = sufficient_contrast.check(Path(folder), {"sufficient_contrast": {"stylesheets": ["site.css"]}})
            failing = sufficient_contrast.ratio(text, background) < 4.5
            self.assertEqual(bool(found), failing, css)


class TestReferenceProperties(unittest.TestCase):
    def test_a_doi_is_found_whole_whatever_surrounds_it(self) -> None:
        rng = random.Random(3)
        suffix_letters = string.ascii_letters + string.digits + "-_"
        for _ in range(CASES):
            doi = f"10.{rng.randint(1000, 999999999)}/{word(rng, suffix_letters, 1, 12)}.{word(rng, suffix_letters, 1, 6)}"
            before, after = rng.choice(["", "see ", "(", "doi:"]), rng.choice([" ", ")", ", ", "; ", ". ", ".\n"])
            text = f"{before}{doi}{after}then more"
            self.assertIn(("doi", doi), references.cited(text), text)


class TestCitationProperties(unittest.TestCase):
    def test_a_key_keeps_its_particle_and_surname(self) -> None:
        rng = random.Random(4)
        particles = ["", "van ", "von ", "de ", "van der ", "ter ", "ten ", "di ", "le "]
        for _ in range(CASES):
            surname = word(rng, string.ascii_uppercase, 1, 1) + word(rng)
            key = rng.choice(particles) + surname
            year = rng.randint(1800, 2099)
            text = f"As {key} {year} shows, it holds."
            found = [match.group(1) for match in citations.CITATION.finditer(text)]
            self.assertEqual(found, [key], text)


class TestPathProperties(unittest.TestCase):
    def test_a_name_is_flagged_exactly_when_it_holds_a_forbidden_character(self) -> None:
        rng = random.Random(5)
        safe = string.ascii_lowercase + string.digits + "-_"
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            bad = set()
            for index in range(60):
                name = f"n{index}-{word(rng, safe, 1, 8)}"
                if rng.random() < 0.5:
                    position = rng.randint(1, len(name) - 1)
                    name = name[:position] + rng.choice('<>:"|?*') + name[position:]
                    bad.add(f"{name}.md")
                (root / f"{name}.md").write_text("x\n")
            flagged = {finding.path for finding in portable_paths.check(root, {"scope": {"exclude": []}})
                       if "forbidden character" in finding.message}
        self.assertEqual(flagged, bad)


class TestProseProperties(unittest.TestCase):
    def test_blank_lines_never_change_the_logical_line_count(self) -> None:
        rng = random.Random(6)
        for _ in range(CASES):
            lines = [rng.choice(["One sentence here.", "- an item", "| a | b |", "Two. Sentences."]) for _ in range(rng.randint(1, 12))]
            text = "\n\n".join(lines) + "\n"
            padded = "\n\n\n".join(lines) + "\n\n"
            self.assertEqual(logical_lines.logical_line_count(text), logical_lines.logical_line_count(padded), lines)

    def test_the_parser_input_has_no_markup_and_is_stable(self) -> None:
        rng = random.Random(7)
        for _ in range(CASES):
            text = " ".join(rng.choice([f"**{word(rng)}**", word(rng), f"[{word(rng)}](https://x.org/{word(rng)})", "*"])
                            for _ in range(rng.randint(1, 10)))
            once = as_read(text)
            self.assertNotIn("*", once, text)
            self.assertNotIn("](", once, text)
            self.assertEqual(as_read(once), once, text)


class TestFrameworkProperties(unittest.TestCase):
    def test_the_extension_wins_and_nothing_else_moves(self) -> None:
        rng = random.Random(8)
        for _ in range(CASES):
            base = {word(rng): {word(rng): rng.randint(0, 9) for _ in range(3)} for _ in range(3)}
            table = rng.choice(list(base))
            key = word(rng)
            extra = {table: {key: "extension"}}
            result = merged(base, extra)
            self.assertEqual(result[table][key], "extension")
            for other in base:
                for name, value in base[other].items():
                    if (other, name) != (table, key):
                        self.assertEqual(result[other][name], value)
            self.assertEqual(merged(base, {}), base)

    def test_a_fingerprint_follows_the_content(self) -> None:
        rng = random.Random(9)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            seen = {}
            for _ in range(CASES):
                content = word(rng, string.printable, 0, 40)
                (root / "a.md").write_text(content)
                print_ = judgment.fingerprint(root, "a.md")
                self.assertEqual(seen.setdefault(content, print_), print_, content)
            self.assertEqual(len(set(seen.values())), len(seen))

    def test_the_summary_names_exactly_the_tiers_that_ran(self) -> None:
        rng = random.Random(10)
        tiers = ["program", "meaning", "syntax"]
        for _ in range(CASES):
            ran = set(rng.sample(tiers, rng.randint(0, 3)))
            skipped = set(rng.sample([tier for tier in tiers if tier not in ran], rng.randint(0, 3 - len(ran))))
            line = run.summary(rng.randint(0, 5), rng.randint(0, 5), ran, skipped)
            self.assertIn(f"tiers run: {', '.join(sorted(ran)) or 'none'}", line)
            self.assertEqual("skipped" in line, bool(skipped), line)


if __name__ == "__main__":
    unittest.main()
