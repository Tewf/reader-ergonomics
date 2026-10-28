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
practitioner argues that a shared piece bent to fit callers that diverge costs more than the copy it replaced (Metz
2016, a blog post: argument, not evidence). In hypertext, each link costs the reader a decision and extra visual
processing (DeStefano 2007, a review); that the same holds for links between files is an inference.

For an agent, a link may go unread. In one vendor's evaluation, an index written into AGENTS.md (the instructions
file an agent loads) beat skills the agent had to open (Vercel 2026: its own claim, method partly stated, sample
size not, one domain). Yet instruction files changed agents' task success by no significant amount on average
(Gloaguen 2026, a preprint). So the rule stays: link, and remind where the reader needs it.
