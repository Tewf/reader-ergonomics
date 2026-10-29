# Shape: note

One topic per note. A note is written to be read again: on the day it is written, before it is used, and, long after,
by search.

## Skeleton

```markdown
# <The topic, named as the field names it>

> One line: what this is and why it matters.

## In three points          the overview, before any detail
1. ...
2. ...
3. ...

## Terms                    each term bold where it is defined, with its definition
- **term**: definition, one line.

## The idea                 figure first when the content is a relation, a set or a process;
                            then the text, one idea per line, no block past three lines

## Check yourself           two or three questions answered from memory; each answer folded
                            in <details><summary>Answer</summary> ... </details>, or listed
                            under a last heading, Answers

## Open                     what is still unclear, as questions

## Links                    the notes this one leans on and the notes that lean on it;
                            omit the section while there are none
```

## Worked example

A note written to this shape, from the evidence behind [worked examples with
subgoals](../principles/document/worked-examples-with-subgoals.md):

```markdown
# Expertise reversal

> A help that teaches a novice slows down a reader who no longer needs it.

## In three points
1. Worked examples and full explanations help novices learn a method.
2. The same help costs an experienced reader, who must process what they already know.
3. So the help is set by the reader's level, and faded as the level rises.

## Terms
- **expertise reversal**: a help that benefits low-knowledge learners loses its benefit, or turns harmful, for
  high-knowledge ones.

## The idea
In a meta-analysis, novices gained from more assistance (d = +0.51) and advanced learners from less (d = -0.43)
(Tetzlaff 2025). An earlier review named the effect (Kalyuga 2003).

## Check yourself
1. Why does a full worked example slow an expert down?
<details><summary>Answer</summary>The expert must read and hold steps they already know.</details>

## Open
- How to tell a reader's level before they start reading.

## Links
- Worked examples with subgoals; the reader styles for a novice and an expert.
```

## The principles it applies

| Part | Principle |
|---|---|
| In three points | [overview first](../principles/document/overview-first.md) |
| Terms | [define before use](../principles/document/define-before-use.md) |
| The idea | [draw relations](../principles/page/draw-relations.md), [signal the structure](../principles/page/signal-the-structure.md) |
| Check yourself | [retrieval prompts](../principles/document/retrieval-prompts.md) |
| Links | [one place per fact](../principles/collection/one-place-per-fact.md): link to the note that holds a fact, never copy it |

## Variants

A lecture note may add `## Outline of the lecture` after the terms, in the order the lecture taught. A shared concept
used by several courses lives in one note that each course links to.
