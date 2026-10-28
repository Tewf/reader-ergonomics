# Position

This file holds what is known, what is not known, what is not claimed, and a proposal for iterative deepening for reading.

## Known

- A map, outline or topic given before the text helps memory and comprehension (organizers small, maps larger).
- Telling the reader what matters raises learning of that part and lowers learning of the rest.
- Examples before problems, and alternating concept and procedure lessons, beat their reverses.
- Interleaving practice across units beats blocking.
- In hypertext, a related-next order helps readers with low knowledge.
- A self-test, not a feeling of understanding, is a sound signal to stop.

## Not known

- No trial compares breadth-first and depth-first reading of the same hierarchical material.
- Elaboration theory, zoom-lens and spiral sequencing have no positive controlled test.
- Stop thresholds (minutes, number of descents, number of recalls) come from word-pair laboratory tasks.
- Whether goal-bounded depth pays off when the later test asks outside the goal.
- Whether instruction first or problem first wins for a given course: the moderator is [element interactivity](../learning-science/frame.md), and no study of a specific course exists.
- Depth over breadth (Schwartz 2009) is correlational and about school science.

## What is not claimed

- "Nobody has done this" is not claimed; the review did not find a trial, which is weaker.
- The proposal below is built from neighbouring results, not from a test of itself.

## Proposal: iterative deepening for reading

Grade: **convention, untested**. Thresholds are PROVISIONAL.

Definitions:
- **Unit**: the chapter or section studied now.
- **Depth 1**: the one-line summary of each notion (hub row, glossary line).
- **Depth 2**: the notion's own page: definition and example.
- **Depth 3**: proofs, derivations, and every link that leaves the unit.
- **Task set** of a unit: notions the unit's exercises or goals require, plus notions marked as must-know, plus their ancestors on the unit's map.

```text
1 subject map, once                     no link opened
2 next unit whose prerequisites are done
3 depth 1 for all notions               no link opened
4 read exercise requirements, list the task set; try the first question 5 min (PROVISIONAL)
5 depth 2 for the task set only, in map order; after each, explain it in two lines from memory
6 check failed? depth 3 on that link only; then check again
7 worked example, then paired exercise; stalled 10 min (PROVISIONAL): unfold one step
8 unit done when a self-test passes unaided, and again a day later
```

Stop rule, per notion:
1. Depth 1 always.
2. Depth 2 if and only if the notion is in the task set.
3. Depth 3 only when a failed check traces to that link, or the proof is marked must-know.
4. Go back up when any holds: the check passes from memory, or two descents in a row changed no answer (PROVISIONAL). Also go back up when the link leaves the unit (log it as a black box: what it gives, not how).
5. The unit is done when the self-test passes, and again a day later.

Evidence per step:

| Step | Evidence | Grade |
|---|---|---|
| 1, 3 | context before; maps; prequestions | measured |
| 2 | prerequisite order | supported with caveat |
| 4 | relevance instructions; agenda; first-step test | measured |
| 5 | coherent order; explanation test | measured |
| 6 | self-explanation of proofs | measured |
| 7 | example then problem; instruction first for interacting elements | measured; supported with caveat |
| 8 | criterion level; overconfidence | measured |
| The combination | none | convention, untested |

Fit of the three common habits:

| Habit | Fits | Fails |
|---|---|---|
| Overview first | steps 1 and 3 | read as a list to remember, it is rereading |
| Depth-first through links | step 5 inside the task set | unbounded: no stop test, depth spent where nothing asks for it |
| Breadth-first only | steps 3 and 4 | as the whole method: skimming gives moderate comprehension and must hand over to steps 5 to 8 |

Changes to a corpus that would support the procedure:
1. A column showing which exercises need each notion (generated, not typed): makes the task set visible at step 3.
2. A section for links beyond the unit's level, one line each: what it gives, when it would matter.
3. One page on how to read a unit (the steps and the stop rule), linked from each unit.
4. A short folded plan above each must-know proof.
5. An interleaved review step after every two or three units (PROVISIONAL).

## Practice and the evidence

- Practice runs ahead of the evidence: BLUF and the Pyramid Principle have wide use, and no controlled comparison with narrative order for working readers was found.
- Practice ignores the evidence: the inverted pyramid survives while its direct tests favour narrative for Thai news readers (Nildam 1998) or show no difference (Sternadori 2008).
- Reader state limits the rule: front-loading fits readers who scan for a fact (Nielsen 2006), and explanation first fits readers who will resist the conclusion (Jansen 2010) (secondary).
- ISO 2023 extends the standard: it adds relevance and testing with readers, which reading order does not cover.
