# 0006: A claim is graded clause by clause

**Decision:** when the clauses of a principle's claim rest on evidence of different strength, its grade names each
clause with its own grade, and the claim keeps every clause.

**Status:** accepted, 2026-10-29, in v1.16.0. **Shape:** [decision record](../shapes/decision-record.md).

## Context

- A review of the family on 2026-10-29 found three grades coarser than their claims:
  - shallow nesting said measured, but its "two nested clauses" rests on English readers alone and does not hold in
    German;
  - signal the structure said measured, but only signalling is; its lists, tables and bold rest on a review of
    cognitive fit and on practice;
  - retrieval prompts asked for folded answers with no source.
- The card, [standard.md](../standard.md), shows each claim beside its grade. A grade coarser than its claim lends
  the weakest clause the strength of the strongest.
- Several principles already graded by clause, such as `shallow-outline` and `sufficient-contrast`.

## Decision

- **The grade names each clause** whose evidence differs, as in "measured for signals; tables for comparisons
  supported with caveat; lists and bold conventions". A claim whose clauses share one grade keeps one word.
- **The claim keeps its clauses.** The card is what a writer or a model follows. A rule taken out of the claim
  would leave the card although its evidence is only weaker, not absent.
- **Applied first** to the three principles the review named. The folding clause of `retrieval-prompts` is
  supported with caveat, inferred from the testing effect, and `signal-the-structure` now says to fold an answer
  that must stay hidden until asked for, which ends the contradiction between the two.

## Consequences

- A reader sees, on the card, which part of a principle is measured and which is practice.
- The grade column grows longer, and a card read in a narrow window wraps it.
- The other principles were re-read clause by clause in v1.18.0: nine gained grades by clause, and the rest kept
  one grade, since their clauses share their evidence.
- An extension that repeats one of these grades should repeat its clauses too, at its next pin.

## Considered options

- **Shrink each claim to its measured clause,** and move the rest to "What it asks". Every grade would be one word,
  but lists, tables and bold would leave the card, and the card is the part that is followed.

## See also

[Decisions](README.md); the grades, in [standard.md](../standard.md); the three principles,
[shallow nesting](../principles/sentence/shallow-nesting.md), [signal the
structure](../principles/page/signal-the-structure.md) and [retrieval prompts](../principles/document/retrieval-prompts.md).
