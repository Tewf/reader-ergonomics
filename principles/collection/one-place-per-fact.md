# One place per fact

**Claim:** each piece of knowledge that must change together lives in one file; every other place links to it.

- **Grade:** supported with caveat.
- **Evidence:** [file structure](../../evidence/file-structure/review.md), [against](../../evidence/file-structure/against.md) (one place per fact).
- **Check:** `duplication` (exact, 20 identical words in two files), `links` (exact, a link that replaces a copy must resolve), `paraphrase` (meaning: the same fact in other words).
- **Reader styles:** strengthened by [LLM reader](../../reader-styles/llm-reader.md).

## What it asks

- State a fact once; elsewhere, one fresh line saying what it is, and a link to where it lives.
- When two files hold the same passage, ask whether the copies must change together. If they must, merge them. If they change for different reasons, a short copy may stay, naming its source.
- No summary copied into a second file "for convenience": a summary that must be loaded somewhere is a pointer, not a second version.

## Why

Copies drift. In five systems about half of the clone groups held inconsistencies, and developers confirmed 107 faults
caused by changing one copy and not the others (Juergens 2009). The rule is about knowledge, not text: the authors of
"don't repeat yourself" restated it that way (Thomas 2019, secondary).

## Limits

Not every copy is harmful: up to 71% of the clones studied in two systems helped maintenance (Kapser 2008). A
shared piece bent to fit callers that diverge costs more than the copy it replaced (Metz 2016). Each link costs
the reader a decision and a context switch (DeStefano 2007).

For an agent, a link may never be followed: in one vendor's evaluation, an index written into AGENTS.md beat skills
the agent had to open (Vercel 2026, its own claim). So what an agent must always know goes into the file it loads,
or is imported into it.
