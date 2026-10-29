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

## Worked example

A problem solved in this repository, written up to this shape:

```markdown
# Fit a text figure on a phone

> What is asked: a figure drawn in characters, 60 columns wide, shows whole on a 375 px phone, and body text keeps
> its size. Done when the figure needs no more width than its column gives.

**What this tests:** the readable measure, applied to figures.

## The plan
1. Measure what the figure needs and what the column gives.
2. Find the type size at which 60 columns fit.
3. Apply it to figures only, on narrow screens.

## Step 1: Measure what the figure needs and what the column gives
   In a browser at 375 by 812, the card's flow figure needs 606 px; its column gives 324 px.
   Predict before running: does a 60-column figure fit a phone? It does not: at the body's size a phone shows
   about 32 columns.
   Trap: trusting the column count; 60 columns fit the desktop column, not a phone.

## Step 2: Find the type size at which 60 columns fit
   A monospace character is about 0.6 em wide, so 60 columns take 36 em: 324 px / 36 = 9 px.

## Step 3: Apply it to figures only, on narrow screens
   Under 600 px, `pre` takes `clamp(9px, calc((100vw - 3.5rem) / 36), 1rem)`; body text keeps its size.

## Checks
   Measured again at 375 px: the figure needs 328 px of 324, its last letter clipped by a fraction; body text
   stays at 19 px.

**If you meet this again:** measure a figure on the narrowest screen it must serve, not in columns.
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
