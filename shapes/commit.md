# Shape: commit message

A commit message says **why** a change was made. The diff already says what changed. A reader
opens the history months later, when the code is still readable and the reason has gone, unless
someone wrote it down.

## Skeleton

```text
One line saying what changed, imperative, capitalised, no full stop, at most 72 characters

Why it changed: the state of things that made the change necessary.

What it buys, what it does not, and anything that will surprise the next reader:
a measured number, a trap avoided, something deliberately left undone.
```

## Rules

- **One commit, one subject:** the change can be titled without an "and". If reverting it would bring back something unrelated, it is two commits.
- A blank line after the subject; a body whenever the change is more than a few lines.
- Filler subjects ("update", "fix", "wip", "misc") say nothing and are refused.
- Size is a symptom, not the rule: forty files can be one change (a rename), four lines can be two.

## Evidence

A study of what makes a good commit message found that developers judge messages by whether they say what changed
*and* why, and that many open-source messages say neither (Tian et al. 2022). The 72-character subject comes from how
`git log --oneline` and terminals display history (graded **convention**).

## Checks

The subject length, the blank line and the filler words can be checked by a `commit-msg` hook. Whether the body
gives the real reason is judgment.
