"""The release checks' oracle: the copies of a pinned release, in workflows, links, changelog and citation, must agree.

Run: python3 -m unittest discover checks
"""
from __future__ import annotations

import unittest

from program import changelog_pin, release_version, standard_links, standard_pin
from test_checks import ScratchRepository


class TestStandardPin(ScratchRepository):
    STEP = "      - uses: actions/checkout@v4\n        with:\n          repository: Tewf/reader-ergonomics\n{ref}          path: standard\n"

    def workflow(self, name: str, *refs: str) -> None:
        steps = "".join(self.STEP.format(ref=f"          ref: {ref}   # v1.0.0\n" if ref else "") for ref in refs)
        self.write(f".github/workflows/{name}.yml", "jobs:\n  build:\n    steps:\n      - uses: actions/checkout@v4\n" + steps)

    def found(self) -> list[str]:
        return [f"{finding.path}:{finding.line} {finding.message}" for finding in standard_pin.check(self.root, {})]

    def test_one_release_in_every_job_passes(self) -> None:
        self.workflow("checks", "a" * 40, "a" * 40)
        self.workflow("pages", "a" * 40)
        self.assertEqual(self.found(), [])

    def test_a_job_left_on_an_older_release_fails(self) -> None:
        self.workflow("checks", "a" * 40, "a" * 40)
        self.workflow("pages", "b" * 40)
        self.assertEqual(self.found(), [".github/workflows/pages.yml:8 checks out Tewf/reader-ergonomics at bbbbbbb, and "
                                        ".github/workflows/checks.yml:8 at aaaaaaa: one release for the whole repository, "
                                        "so one bump moves every job"])

    def test_a_checkout_without_a_ref_fails_and_other_repositories_are_not_read(self) -> None:
        self.workflow("pages", "")
        self.write(".github/workflows/other.yml", "jobs:\n  a:\n    steps:\n      - uses: actions/checkout@v4\n"
                   "        with:\n          repository: Tewf/another\n          ref: main\n")
        self.assertEqual(self.found(), [".github/workflows/pages.yml:7 checks out Tewf/reader-ergonomics with no ref, "
                                        "so the latest commit: pin it to the release's commit"])


class TestStandardLinks(ScratchRepository):
    PIN = "6980fa64583912922d6f5b5c01316749d654345f"
    WORKFLOW = ("jobs:\n  checks:\n    steps:\n      - uses: actions/checkout@v4\n        with:\n"
                "          repository: Tewf/reader-ergonomics\n          ref: {pin}   # v1.11.0\n")
    LINK = "See [a rule](https://github.com/Tewf/reader-ergonomics/{kind}/{ref}/a.md).\n"

    def setUp(self) -> None:
        super().setUp()
        self.write(".github/workflows/checks.yml", self.WORKFLOW.format(pin=self.PIN))

    def found(self, text: str) -> list[str]:
        self.write("page.md", text)
        return [finding.message for finding in standard_links.check(self.root, {})]

    def test_a_link_at_the_pinned_commit_or_its_tag_passes(self) -> None:
        self.assertEqual(self.found(self.LINK.format(kind="blob", ref=self.PIN)), [])
        self.assertEqual(self.found(self.LINK.format(kind="tree", ref="v1.11.0")), [])

    def test_a_link_at_a_branch_another_commit_or_another_tag_fails(self) -> None:
        for ref in ("master", "d48ffbe96aed32dd63e1974ee60f69472fe36932", "v1.4.1"):
            found = self.found(self.LINK.format(kind="blob", ref=ref))
            self.assertEqual(len(found), 1, ref)
            self.assertIn(f"at {ref[:12]}, but the workflows pin 6980fa6", found[0])

    def test_a_link_quoted_in_code_is_not_read(self) -> None:
        self.assertEqual(self.found("Every `" + self.LINK.format(kind="blob", ref="master").strip()[4:-1] + "` moves.\n"), [])

    def test_workflows_with_two_refs_leave_it_to_standard_pin(self) -> None:
        self.write(".github/workflows/pages.yml", self.WORKFLOW.format(pin="d" * 40))
        self.assertEqual(self.found(self.LINK.format(kind="blob", ref="master")), [])


class TestChangelogPin(ScratchRepository):
    PIN = "397a5553d2adbdd136bc3239bf304eb4ae62e2d2"
    WORKFLOW = ("jobs:\n  checks:\n    steps:\n      - uses: actions/checkout@v4\n        with:\n"
                "          repository: Tewf/reader-ergonomics\n          ref: {pin}   # v1.16.1\n")
    ENTRY = "- Pinned reader-ergonomics v{new} (`{commit}`), from v1.13.0 (`7a76cc6`): what it carries.\n"

    def found(self, changelog: str | None, pin: str = PIN) -> list[str]:
        self.write(".github/workflows/checks.yml", self.WORKFLOW.format(pin=pin))
        if changelog is not None:
            self.write("CHANGELOG.md", "# Changelog\n\n## 2026-10-30\n\n### Changed\n\n" + changelog)
        return [f"{finding.kind} {finding.message}" for finding in changelog_pin.check(self.root, {})]

    def test_a_newest_line_naming_the_pin_passes(self) -> None:
        self.assertEqual(self.found(self.ENTRY.format(new="1.16.1", commit="397a555")), [])

    def test_a_newest_line_left_on_the_old_release_fails(self) -> None:
        found = self.found(self.ENTRY.format(new="1.13.0", commit="7a76cc6"))
        self.assertEqual(found, ["error the newest pin line names v1.13.0 (7a76cc6), but the workflows pin 397a555: "
                                 "record the move above it"])

    def test_no_changelog_or_no_pin_line_warns(self) -> None:
        self.assertTrue(self.found(None)[0].startswith("warning the workflows pin Tewf/reader-ergonomics at 397a555"))
        self.assertTrue(self.found("- Fixed a typo.\n")[0].startswith("warning no line names Tewf/reader-ergonomics"))

    def test_the_standard_itself_finds_nothing(self) -> None:
        self.write("CHANGELOG.md", "# Changelog\n")
        self.assertEqual([finding for finding in changelog_pin.check(self.root, {})], [])


class TestReleaseVersion(ScratchRepository):
    CHANGELOG = "# Changelog\n\n## [1.19.0] - 2026-10-29\n\n### Added\n\n- A check.\n\n## [1.18.2] - 2026-10-28\n"

    def found(self, citation: str, changelog: str = CHANGELOG) -> list[str]:
        self.write("CHANGELOG.md", changelog)
        self.write("CITATION.cff", "cff-version: 1.2.0\ntitle: \"x\"\n" + citation)
        return [f"{finding.line} {finding.message}" for finding in release_version.check(self.root, {})]

    def test_a_citation_naming_the_newest_release_passes(self) -> None:
        self.assertEqual(self.found('version: "1.19.0"\ndate-released: "2026-10-29"\n'), [])
        self.assertEqual(self.found("version: 1.19.0\ndate-released: 2026-10-29\n"), [])

    def test_a_citation_left_on_the_last_release_fails_for_each_field(self) -> None:
        self.assertEqual(self.found('version: "1.18.2"\ndate-released: "2026-10-28"\n'), [
            "3 version is 1.18.2, but the changelog's newest release is 1.19.0: set both in the release commit",
            "4 date-released is 2026-10-28, but the changelog's newest release is 2026-10-29: set both in the release commit"])

    def test_dated_headings_or_no_version_field_are_not_compared(self) -> None:
        self.assertEqual(self.found('version: "0.1.0"\n', changelog="# Changelog\n\n## 2026-10-29\n"), [])
        self.assertEqual(self.found(""), [])


if __name__ == "__main__":
    unittest.main()
