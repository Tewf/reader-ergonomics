# Shape: report

A report explains how a problem was solved, so that the reader can solve the next problem of the same kind. It
is a worked example written down: the steps are named by what they achieve, a figure comes before the
text it supports, and every result is checked.

## Skeleton

```markdown
# <The problem, named by what solving it achieves>

> What is asked: inputs, output, constraints, and what counts as done.

**What this tests:** the concept, with a link to the note that explains it.

## The plan                    numbered; each item is a subgoal label (what the step achieves)

## Step 1: <what the step achieves>
   the figure first, when the step is about a relation, a set, a shape or a process
   how and why, with the reference that settles it
   Predict before running: one question; then the run, with its real output
   Trap: the usual mistake and the wrong answer it gives (at most one per step)

## Checks                      how the result was verified: a known value, a limit case,
                               a second method, a unit

**If you meet this again:** the one rule that transfers to a new problem of the same kind.
```

## The principles it applies

| Part | Principle |
|---|---|
| The plan, step titles | [worked examples with subgoals](../principles/document/worked-examples-with-subgoals.md) |
| What is asked, the plan | [overview first](../principles/document/overview-first.md) |
| Figure first | [draw relations](../principles/page/draw-relations.md), [figure next to its text](../principles/page/figure-next-to-its-text.md) |
| Predict before running | [retrieval prompts](../principles/document/retrieval-prompts.md) |

## Fading

Across a series of reports on one method, solve the first in full and leave the last steps of the next to the reader.
Then give a later one as a whole problem with its answer under Checks (Renkl et al. 2004). See
[learning science](../evidence/learning-science/).
