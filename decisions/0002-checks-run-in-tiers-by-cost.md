# 0002: The checks run in tiers, each as often as its cost allows

**Status:** accepted, 2026-10-29, in v1.1.0.

## Context

A check that a program decides exactly costs nothing to run. A check that compares meaning needs an embedding model,
and one that reads a sentence's structure needs a parser. Some questions only a person, or a model, can answer. Run all of
them on every change, and a push waits for downloads; run them rarely, and a regression goes unseen for longer.

## Decision

- **Cost sets frequency.** The program tier runs on every push, and the meaning tier too, with its model cached. The
  syntax tier and the online resolution of references run weekly, and on demand
  ([checks](../checks/README.md)).
- **A program checks what a program can decide**, and a model is asked only what no program can.
- **Judgment is written down, never guessed.** A question is written to a file for whoever is at work, and its answer
  is kept in `checks/judgments.toml`. The paid backend exists but is off until the maintainer turns it on.
- **A missing library skips its tier with a notice**, and the last line of a run names the tiers that ran.
- **Nothing that should be checked passes unread.** A run that finds no file, a missing config or a missing
  stylesheet stops the run or warns.

## Consequences

- A sentence-level regression can surface up to a week late. The first weekly run, on 2026-10-29, found 114 warnings
  in the standard's own text that no push had shown.
- A run on a machine without the libraries checks less than CI does, and says so.
- Every rule of the standard can name a check, because judgment counts as one when a program cannot decide.

## Considered options

- **Every tier on every push.** Nothing would wait a week, but each push would install a parser and its model.
- **The program tier alone.** Free and fast, but meaning and sentence structure would never be checked.
- **A paid model as the default judge.** Answers without a person, at a cost on every push, and a model would be
  judging text that a model may have written.
