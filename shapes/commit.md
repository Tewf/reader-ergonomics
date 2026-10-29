# Shape: commit message

A commit message says **why** a change was made. The diff already says what changed. A reader
opens the history months later, when the code is still readable and the reason has gone, unless
someone wrote it down.

## Skeleton

The parts, in order:

```text
What changed, in the imperative; at most 72 characters

Why it changed: the state of things that made the change
necessary.

What it buys, what it does not, and anything that will
surprise the next reader: a measured number, a trap avoided,
something deliberately left undone.
```

## Worked example

A commit from this repository's history:

```gitcommit
Shrink a text figure to fit a phone instead of cutting it off

At 60 columns a figure fits the desktop column, but a phone shows
about 32 at the body's size: on a 375 px screen the card's flow
needed 606 px and had 324, so half the relation sat behind a
scrollbar. Under 600 px, a figure's type now scales to show its 60
columns, down to 9 px, where the same flow needs 328 px. Body text
keeps its size. Measured in a browser at 375 by 812.
```

The subject says what changed, in 61 characters. The body gives the state that made it necessary (the measured
overflow), what it buys (the whole figure), what it does not change (body text), and how it was verified.

## Rules

- The subject is capitalised and has no full stop.
- **One commit, one subject:** the change can be titled without an "and". If reverting it would bring back something unrelated, it is two commits.
- A blank line after the subject; a body whenever the change is more than a few lines.
- Filler subjects ("update", "fix", "wip", "misc") say nothing and are refused.
- Size is a symptom, not the rule: forty files can be one change (a rename), four lines can be two.

## Evidence

A study of what makes a good commit message found that developers judge messages by whether they say what changed
and why, and that many open-source messages say neither (Tian et al. 2022). The 72-character subject comes from how
`git log --oneline` and terminals display history (graded **convention**).

## Checks

The subject length, the blank line and the filler words can be checked by a `commit-msg` hook. Whether the body
gives the real reason is judgment.
