# One role per file

**Claim:** a file holds one role: what it does fits one sentence, and its parts change for the same reasons.

- **Grade:** convention, untested.
- **Evidence:** [file structure](../../evidence/file-structure/review.md), [against](../../evidence/file-structure/against.md) (one role per file).
- **Check:** `logical-lines` asks past the trigger; `co-change` raises files that keep changing together across folders; `section-cohesion` (meaning) asks about a section far from all the others.
- **Reader styles:** none override it.

## What it asks

- The cheap first test: state the file's role in one sentence. If the sentence needs "and", the file may hold two roles.
- The real test: parts of a file that never change in the same commit are separate roles; parts that always change together belong together.
- Split by component, not by language or file type: the markup, style and behaviour of one component change together.

## Why

A module should hide one design decision likely to change (Parnas 1972). Its author later restated the single
responsibility principle as responsibility to one actor, a group who request changes (Martin 2017). Files that change
together can be read from version history. In the 82% of queries where it suggested
anything, co-change named a file changed in the same commit among its top three suggestions 72% of the time (Zimmermann 2005).

## Limits

The sentence test fails both ways: anything can be named in one sentence, and two closely related steps belong
together even when the sentence needs "and" (Ousterhout 2025). Co-change is sparse in a young repository.
