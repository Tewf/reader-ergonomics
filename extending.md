# Extending this standard

An **extension** is a repository that applies this standard to one genre (research papers, talks, writing about
software) and adds only what that genre changes. Three exist:
[reader-ergonomics-academic](https://github.com/Tewf/reader-ergonomics-academic) (reports, papers, mathematical articles
and proofs), [reader-ergonomics-presentations](https://github.com/Tewf/reader-ergonomics-presentations) (talks) and
[reader-ergonomics-software-design](https://github.com/Tewf/reader-ergonomics-software-design) (writing about software).

This page is the contract between the standard and its extensions. It says how an extension is laid out, and which
parts of this repository it can rely on when this one changes.

```text
 this standard (the common ground)        an extension (one genre)
 standard.md, principles/  ◀── links ───  standard.md, principles/   only where the genre differs
 checks/run.py             ◀── runs ────  checks/local/              its own checks, run beside these
 checks/config.toml        ◀── extends ─  checks/config.toml         only the values it changes
```

The arrows point one way. This standard depends on no extension: it never reads, runs or copies what an extension
holds. It may list them, as this page does, since a link is a reference, not a dependency
([decision 0001](decisions/0001-extensions-depend-one-way.md)).

## The layout an extension mirrors

People read an extension on its site, and language models read it through `llms.txt` and `AGENTS.md`, as they
read this repository. So an extension keeps the same parts, each with the same role:

| Part | Role in an extension |
|---|---|
| `standard.md` | the genre's card: read this standard first, then the genre's principles; its table is generated |
| `principles/<group>/` | one file per principle the genre adds or changes, in the format below |
| `shapes/` | templates of the genre's documents |
| `reader-styles/` | only readers particular to the genre |
| `evidence/` | one review per topic, with its bibliography |
| `checks/` | the config that extends this one, and `local/` for the genre's own checks |
| `AGENTS.md`, `llms.txt` | how to change it, and its index for models |
| `README.md`, `README.fr.md` | the front page, in English and in French |

A principle this standard already holds is linked, never copied.

## The interface

These parts are stable within a major version. An extension relies on them and on nothing else in this repository.

| Part | Contract |
|---|---|
| Principle file | `principles/<group>/<name>.md`; a first line `# Title`; the lines `**Claim:**`, `**Grade:**`, `**Evidence:**`, `**Check:**` (check names in backticks) and `**Reader styles:**` |
| Group | `principles/<group>/README.md`, whose first line is the group's heading |
| Card | `standard.md` holds `<!-- principles:start -->` and `<!-- principles:end -->`; the table between them is built from the principle files |
| Bibliography | `evidence/bibliography.md`, a table `Key | Citation | Link`; a key is `Surname Year`, with one letter after the year at most |
| Command | `python3 checks/run.py ROOT [--tiers ...] [--only ...] [--online] [--judge ...]`; it exits with 1 when any exact check fails, and with 2 when it could check nothing: ROOT is not a folder, the config is missing or invalid, or no file is in scope |
| Config | `checks/config.toml` with `extends = "reader-ergonomics"` is merged onto this standard's config, table by table, and the extension's value wins; any other `extends` stops the run |
| Local checks | each module in `checks/local/` defines `NAME` and `check(root, config)`, which returns `Finding` objects from `framework.check_api`; `TIER` is optional |
| Indexes | `python3 checks/program/standard_card.py ROOT --write` builds the card's table and `llms.txt`, taking the site, title and description from the extension's `_quarto.yml` and the groups from `[standard_card] facets` |
| Judgment answers | `checks/judgments.toml`, optional: `[[answer]]` entries with `check`, `path`, `question`, `file` (the fingerprint of the file when answered) and `answer`; an edit to the file reopens its questions |
| Site | `site.css` at the root, which an extension's site may load |

A local check counts for `principle-coverage`, so an extension's principle can name a check of its own.

A stylesheet listed in config that does not exist is a warning, so an extension that loads this standard's `site.css`
rather than one of its own sets `stylesheets = []` under `[readable_measure]` and `[sufficient_contrast]`.

## Versions

Releases are tagged `vMAJOR.MINOR.PATCH`. A change that breaks any part of the interface raises the major number.

An extension's CI checks out a release by its commit. It never checks out the tag or the latest commit: a tag can be
moved, and a commit cannot. The tag is named in a comment beside the commit:

```yaml
ref: <the release's commit, all 40 characters>   # v1.0.0
```

The extension moves to a new release deliberately, by changing that line.

## Trust

`run.py` runs the code in the checked repository's `checks/local/`. Run it only on repositories you trust; in CI, an
extension runs its own code on its own runner.
