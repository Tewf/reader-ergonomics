# Checks

The standard's oracle. Every principle names at least one check that tests it, and CI fails if one names none. A rule
a program can verify exactly is verified by a program, for free; a model is used only where meaning is at stake; a
question no model should settle is left for judgment. Every check runs in polynomial time and space, and none costs
money: the one paid backend exists but is off.

## Tiers, and how often they run

```text
 tier       needs                            runs                    finds
 program    the Python standard library      every push              errors, warnings, questions
 meaning    sentence embeddings (fastembed)  every push, model cached questions
 syntax     a parser (spaCy)                 weekly, and on demand   warnings
 judgment   a person, or a model if given    every push: listed      answers
```

| Folder | Holds |
|---|---|
| [program/](program/) | the checks that need no model: paths, folders, links, size, outline, copies, terms, shapes, sentences, figures, stylesheet, citations, history |
| [meaning/](meaning/) | the checks that compare meaning: paraphrased copies, page mode, name against content, section cohesion |
| [syntax/](syntax/) | the checks that read a parse: [dependency length](../evidence/psycholinguistics/review.md), clause nesting, links between sentences |
| [framework/](framework/) | what every check is built on: the interface, the prose units, the judgment backends |
| [run.py](run.py) | the one entry point |
| [config.toml](config.toml) | every threshold, tagged PROVISIONAL where it is a convention, and the default tiers |
| [test_checks.py](test_checks.py) | the checks' own oracle: a planted violation per check |

Which principle each check serves is said once, on the principle's **Check:** line; `principle-coverage` holds every
principle to naming at least one registered check.

## Kinds of finding

```text
 a finding
  ├─ exact ─────▶ error     the run fails
  ├─ heuristic ─▶ warning   fix it, or say why it is false
  └─ open ──────▶ judgment  to a backend: none, flag
                            (default), local model,
                            or api (paid, off)
```

| Backend | What happens | Cost |
|---|---|---|
| `none` | questions dropped | free |
| `flag` (default) | questions written to `checks/out/needs-judgment.md` for the person or agent already at work | free |
| `local` | each question sent to a model on this machine through an OpenAI-compatible endpoint, set only by `READER_ERGONOMICS_LOCAL_URL` and `READER_ERGONOMICS_LOCAL_MODEL` | free, local |
| `api` | the same protocol to a paid provider (`READER_ERGONOMICS_API_URL`, `_KEY`, `_MODEL`); refuses to run unless `[judgment.api] enabled = true` | paid, off |

A model's answer is recorded as advice next to its question; it never fails the run.

## Use

```sh
python3 checks/run.py .                    # tiers from config
python3 checks/run.py . --tiers program    # no model at all
python3 checks/run.py path/to/repo         # another; its config wins
python3 checks/run.py . --online --only references
python3 -m unittest discover -s checks     # test the checks
pip install -r checks/meaning/requirements.txt   # the meaning tier
pip install -r checks/syntax/requirements.txt    # the syntax tier
```

A tier whose library is missing is skipped with a notice, never failed. `.github/workflows/checks.yml` runs the program
and meaning tiers on every push and pull request. It runs the syntax tier and the online references once a week.

## What is not checked here

The rendered page: contrast and measure are checked on the stylesheet's declared values, not on the pixels. A browser
accessibility checker measures the rendered page exactly.
