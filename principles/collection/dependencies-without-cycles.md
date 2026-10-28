# Dependencies without cycles

**Claim:** code dependencies between folders never form a cycle, so every folder sits on a level above everything it uses.

- **Grade:** convention, argued from design practice.
- **Evidence:** [file structure](../../evidence/file-structure/review.md), [against](../../evidence/file-structure/against.md) (dependencies).
- **Check:** `tree-shape` (exact for static Python imports): a cycle between folders fails.
- **Reader styles:** none override it.

## What it asks

- No two folders that import each other, directly or through others.
- Shared code goes into a folder of its own, declared as a lower level, that the others import.
- A link between documents is a reference, not a dependency, and may cycle: a note and the note it cites may point at each other.

## Why

Without cycles a system can be levelized: each component gets a level above all it uses, and can be understood, tested
and replaced from the bottom up (Lakos 1996; the acyclic dependencies principle, Martin 2017). A cycle is the one shape
that makes placing shared code at a common ancestor impossible.

## Limits

The support is argument, not a controlled study. A rule on path shapes (never import a sibling folder) contradicts
levelization, which puts shared code exactly in a sibling; check levels and cycles, not paths.
