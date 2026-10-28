# Checks

The checks are the standard's oracle. A rule a program can verify exactly is verified by a program,
for free; a model is asked only what no program can answer. Every check runs in polynomial time and
space, needs only the Python standard library (3.11 or later), and costs nothing to run. A check that
would cost money exists but stays off until the maintainer turns it on.

## Contents

| Check | Principle | Kind | Time |
|---|---|---|---|
| [portable_paths.py](portable_paths.py) | [portable paths](../principles/collection/portable-paths.md) | exact | O(path length) |
| [tree_shape.py](tree_shape.py) | [browsable folders](../principles/collection/browsable-folders.md), [dependencies without cycles](../principles/collection/dependencies-without-cycles.md) | exact, plus a judgment question | O(paths + imports) |
| [links.py](links.py) | [one place per fact](../principles/collection/one-place-per-fact.md): a link replaces a copy only if it resolves | exact | O(text) |
| [logical_lines.py](logical_lines.py) | [size is a prompt](../principles/collection/size-is-a-prompt.md) | judgment past the trigger and past the ceiling | O(text) |
| [duplication.py](duplication.py) | [one place per fact](../principles/collection/one-place-per-fact.md) | exact | O(words), expected |
| [outline_depth.py](outline_depth.py) | [shallow outline](../principles/document/shallow-outline.md) | exact count, warns past level 3 | O(text) |
| [defined_before_use.py](defined_before_use.py) | [define before use](../principles/document/define-before-use.md) | heuristic (warns) | O(terms x text) |
| [citations.py](citations.py) | every cited work listed once, every entry cited | heuristic (warns) | O(text) |
| [standard_card.py](standard_card.py) | the card's principle table and `llms.txt` match the principle files they are built from | exact; `--write` rebuilds | O(principle files) |
| [provisional_tags.py](provisional_tags.py) | [tunables in config](../principles/collection/tunables-in-config.md): a guess older than 90 days is asked about | exact date, judgment | O(text + lines blamed) |
| [co_change.py](co_change.py) | [one role per file](../principles/collection/one-role-per-file.md), [group by what changes together](../principles/collection/group-by-what-changes-together.md): files that keep changing together across folders | judgment | O(commits × 20²) |
| [references.py](references.py) | every DOI, arXiv id and link resolves | exact; offline by default | O(references) requests |

| Support file | Role |
|---|---|
| [run.py](run.py) | the one entry point: runs the checks, prints findings, sends judgment questions to the backend |
| [check_api.py](check_api.py) | the interface every check shares: files in scope, the finding it returns |
| [judgment.py](judgment.py) | the judgment backends |
| [config.toml](config.toml) | every threshold, tagged PROVISIONAL where it is a convention |
| [test_checks.py](test_checks.py) | the checks' own oracle: one planted violation per check |

## Kinds of finding

```text
 a finding
  ├─ exact ─────▶ error     the run fails
  ├─ heuristic ─▶ warning   fix it, or say why it is false
  └─ open ──────▶ judgment  to a backend: none, flag
                            (default), local model,
                            or api (paid, off)
```

- **error:** certain. The run exits with status 1.
- **warning:** a heuristic match. Read it; it may be wrong.
- **judgment:** a question no program can answer exactly, such as "does this file's role fit in one sentence?". It goes to the backend.

## Judgment backends

| Backend | What happens | Cost |
|---|---|---|
| `none` | questions dropped | free |
| `flag` (default) | questions written to `checks/out/needs-judgment.md` for the person or agent already at work | free |
| `local` | each question sent to a model on this machine through an OpenAI-compatible endpoint, set only by `READER_ERGONOMICS_LOCAL_URL` and `READER_ERGONOMICS_LOCAL_MODEL` | free, local |
| `api` | the same protocol to a paid provider (`READER_ERGONOMICS_API_URL`, `_KEY`, `_MODEL`); refuses to run unless `[judgment.api] enabled = true` | paid, off |

A model's answer is recorded as advice next to its question; it never fails the run.

## Use

```sh
python3 checks/run.py .                # this repository
python3 checks/run.py path/to/repo     # another; its config wins
python3 checks/run.py . --only links   # some checks only
python3 checks/run.py . --online --only references
python3 checks/run.py . --judge local  # needs the two variables
python3 -m unittest discover -s checks # test the checks
```

## On every push

`.github/workflows/checks.yml` runs the tests and every check on each push to any branch and on each pull request,
offline and for free, and lists the judgment questions in the log. Once a week it resolves every reference online,
since links rot. No paid backend runs there.

## What is not checked here

Contrast ratios, rendered line length and the shape of a figure are properties of the rendered page. A browser
accessibility checker measures them exactly; they are not reimplemented here.
