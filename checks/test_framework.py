"""The framework's own oracle: the runner, the config, the judgment step and each way a run can fail.

The checks' planted violations are in test_checks.py, beside this file. Run: python3 -m unittest discover checks
"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

import run
from program import readable_measure, references, standard_card, sufficient_contrast
from test_checks import CONFIG, ScratchRepository


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


class TestStandardConfig(unittest.TestCase):
    def test_the_answers_file_never_asks_about_itself(self) -> None:
        import tomllib
        config = tomllib.loads((Path(run.__file__).with_name("config.toml")).read_text(encoding="utf-8"))
        self.assertIn("checks/judgments.toml", config["co_change"]["exempt"])
        self.assertIn("checks/judgments.toml", config["logical_lines"]["exempt_from_ceiling"])


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
                   "- **Grade:** measured for terms;\n  convention for the rest.\n")
        built = standard_card.expected(self.root, {"standard_card": {"facets": ["talk"]}})
        self.assertTrue(built["llms.txt"].startswith("# Talks\n\n> How to give a talk."))
        self.assertIn("(https://example.org/talks/principles/talk/key-terms.md)", built["llms.txt"])
        self.assertNotIn("Reader styles", built["llms.txt"])  # this extension has none
        self.assertIn("### Talk: a paced medium", built["standard.md"])
        self.assertIn("| measured for terms; convention for the rest |", built["standard.md"])  # a wrapped grade is read whole

    def test_a_count_marker_holds_the_number_of_checks(self) -> None:
        self.write("standard.md", "# Card\n")
        self.write("checks/program/a.py", 'NAME = "a"\n')
        self.write("checks/figures/b.py", 'NAME = "b"\n')
        self.write("checks/framework/c.py", 'NAME = "not a check"\n')
        self.write("checks/program/_helper.py", "x = 1\n")
        self.write("notes.md", "It runs <!-- count:checks -->7<!-- /count --> checks; <!-- count:other -->3<!-- /count -->.\n")
        built = standard_card.expected(self.root)
        self.assertEqual(built["notes.md"], "It runs <!-- count:checks -->2<!-- /count --> checks; <!-- count:other -->3<!-- /count -->.\n")

    def test_a_card_without_principles_does_not_promise_them(self) -> None:
        self.write("standard.md", "# Papers\n\nHow to use the shapes.\n")
        self.write("shapes/README.md", "# Shapes\n\nSkeletons.\n")
        built = standard_card.expected(self.root)
        self.assertIn("standard.md): the one-page card to follow, how to use this standard and its shapes\n", built["llms.txt"])
        self.write("principles/talk/key-terms.md", "# Key terms on screen\n")
        self.assertIn("with every principle and its grade", standard_card.expected(self.root)["llms.txt"])


if __name__ == "__main__":
    unittest.main()
