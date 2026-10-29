# Contributing to this repository

For anyone changing this repository, person or language model. To apply the standard
somewhere else, read [standard.md](standard.md) instead; this file is about this repository only.
To extend it to one genre in a repository of its own, read [extending.md](extending.md), and change nothing
it lists as the interface without raising the major version.

## Before writing

1. Read [standard.md](standard.md). This repository is its own first example, so it obeys every principle it states.
2. Pick the shape of what you write from [shapes/](shapes/), and the reader style if the reader is known ([reader-styles/](reader-styles/)).

## Rules for claims

- Every principle carries a grade: **measured**, **supported with caveat**, **convention** or **not supported**. A grade moves only with a cited source.
- Cite in the text as `Author Year`. The full entry goes once into [evidence/bibliography.md](evidence/bibliography.md), with a DOI, an arXiv id or a stable URL. A key names one work, here and in every extension ([decision 0003](decisions/0003-one-key-one-work-across-the-family.md)).
- Evidence against a principle goes into the topic's `against.md`, never deleted to make a principle look stronger.
- A number read in a summary rather than in the paper is marked "(secondary)".
- A limit or caveat added to a principle carries its own grade and its kind of source (study, thesis, standard,
  company page, opinion), and the change obeys the principle it changes. Practice shows what is done; an outcome it reports is its owner's claim.

## Before handing back

```sh
python3 -m unittest discover -s checks     # the checks' own oracle
python3 checks/run.py .                    # the repository against the standard
python3 checks/run.py . --online --only references   # resolve every reference (network)
```

- Fix every `error`. Read every `warning`.
- Answer the questions in `checks/out/needs-judgment.md`, and keep each answer in `checks/judgments.toml`, quoting what in the file the reason rests on. A model does
  not review its own text in place of the checks.
- The paid judgment backend stays off (`[judgment.api] enabled = false`) unless the maintainer turns it on.

## House conventions (this repository, not the standard)

- English throughout; the two READMEs are kept in English and French, in step.
- No em dash or en dash in prose; use a comma, a colon, parentheses, or a hyphen for ranges.
- A new folder gets a `README.md` and a one-line `index.qmd` that includes it (copy any existing `index.qmd`), because the site generator skips files named README.
- Commit messages follow [shapes/commit.md](shapes/commit.md).

## The site

`quarto render` builds `_site/` locally. A push to `master` publishes it through `.github/workflows/pages.yml`.
