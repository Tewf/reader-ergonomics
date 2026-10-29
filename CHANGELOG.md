# Changelog

Every release of the standard, newest first, in the form of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
(Lacan 2019). Versions follow `MAJOR.MINOR.PATCH` as [extending.md](extending.md) defines them. The commit to pin
a release by is the one its tag points to: `git rev-list -n 1 v1.16.1`, or the repository's tags page.

## [1.17.0] - 2026-10-29

### Added

- This changelog, of every release since 1.0.0.
- The check `changelog-pin`: an extension's newest changelog pin line names the release its workflows check out.
- On the front page, how a reader takes their own version: fork or copy, name the reader, pin a release, run the
  checks; and where a disagreement goes.

### Changed

- A pin move or a dependency bump is a changelog entry, not a decision record; the decision-record shape says so,
  and extending.md gives the entry's form.

## [1.16.1] - 2026-10-29

### Fixed

- Each evidence review opens with what it holds.
- The checks README names the checks not exercised here.

## [1.16.0] - 2026-10-29

### Changed

- A claim is graded clause by clause (decision 0006).

### Fixed

- The card reads wrapped fields whole.

## [1.15.0] - 2026-10-29

### Added

- Count markers filled by standard-card.

### Fixed

- The front page's counts are fixed, the audits are linked, and no person is named.

## [1.14.0] - 2026-10-29

### Changed

- A key that names another work in the family is an error (decision 0005).

## [1.13.0] - 2026-10-29

### Added

- The check `standard-links`, adopted from software-design.

## [1.12.2] - 2026-10-29

### Fixed

- W3C 2023b names one page.
- The extending page lists the five extensions.

## [1.12.1] - 2026-10-29

### Added

- The extending page says where to extract a release for a local run.

## [1.12.0] - 2026-10-29

### Added

- The check `standard-pin`: every workflow checks out the standard at one commit.

## [1.11.0] - 2026-10-29

### Added

- An organisation's key may carry a title word (decision 0004).

### Fixed

- The generated `llms.txt` describes a card without principles.

## [1.10.0] - 2026-10-29

### Added

- The checks `typed-figure`, `figure-alt`, `figure-source` and `figure-contrast`, adopted.

### Changed

- Figure checks in checks/figures.

## [1.9.0] - 2026-10-29

### Added

- The check `figure-source-inline` keeps the copy equal to its file.

### Changed

- Each figure folds its Graphviz source under it.

## [1.8.1] - 2026-10-29

### Fixed

- Inline code wraps instead of widening the page.

## [1.8.0] - 2026-10-29

### Changed

- The standard's figures drawn as SVG from Graphviz, with their sources.

## [1.7.0] - 2026-10-29

### Added

- The check `shape-example` warns on a shape with no filled example.
- Every shape has one.

## [1.6.0] - 2026-10-29

### Added

- The check `decision-records` checks the four rules of a record.
- Decisions listed in llms.txt.

## [1.5.3] - 2026-10-29

### Added

- Key year and older use defined.

### Changed

- A preprint named in a citation is the same work.

## [1.5.2] - 2026-10-29

### Added

- Tests for sentence-links, name-content and section-cohesion.

## [1.5.1] - 2026-10-29

### Fixed

- Four folder summaries within 60 words.

## [1.5.0] - 2026-10-29

### Added

- The check `bibliography-keys`: a key names one work across the family.
- The standard's key wins, and between extensions the older use.

## [1.4.3] - 2026-10-29

### Fixed

- The counts of sources below the bar, after the Sternadori rescore.

## [1.4.2] - 2026-10-29

### Fixed

- Tang 2006 and Sternadori 2008 read in full.

## [1.4.1] - 2026-10-29

### Fixed

- On a phone, a text figure shrinks to show its 60 columns.

## [1.4.0] - 2026-10-29

### Added

- The check `figure-width` warns on a text figure wider than 60 columns.
- The standard's figures fit.

## [1.3.2] - 2026-10-29

### Fixed

- The judgment answers file is exempt from the line ceiling.

## [1.3.1] - 2026-10-29

### Fixed

- Dickson 2005 points at the paper.
- Colfer 2016's counts stated from the article.

## [1.3.0] - 2026-10-29

### Added

- The decision-record shape.

### Changed

- The standard's records follow it.

## [1.2.0] - 2026-10-29

### Added

- The check `judgment-quotes`: every answer about a file's content quotes it.

### Changed

- The framework's tests in their own file.

## [1.1.2] - 2026-10-29

### Changed

- Generated tier READMEs and the judgment answers are exempt from co-change.

## [1.1.1] - 2026-10-29

### Changed

- A server that does not answer in time is a warning, not an error.

## [1.1.0] - 2026-10-29

### Added

- Decision records.
- A guarantee per check.
- Property and failure-path tests.

### Fixed

- Contrast resolves variables by theme, measures inherited text and merges rules per selector.
- Horn 1969 read first-hand.

## [1.0.1] - 2026-10-29

### Fixed

- Citation keys keep 'ter' and 'ten'.
- The extending page names the three extensions.

## [1.0.0] - 2026-10-29

### Added

- First release with a published interface for extensions (extending.md).
