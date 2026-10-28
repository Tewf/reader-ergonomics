# Position: what is known, what is not, what this repository adds

## Known

- Extra input costs accuracy as well as money: length, irrelevant text and distractors each lower it (Levy 2024; Shi 2023; Hong 2025).
- Where a fact sits can matter, but how much depends on the model and on input length relative to its window (Liu 2024; Veseli 2025).
- Word overlap between a question and its answer carries much of long-context retrieval (Modarressi 2025).
- Order that follows use helps: premises in proof order beat shuffled ones (Chen 2024b).
- Layout effects are real and model-specific; they persisted with scale in 2023 open models (Sclar 2024) and are smaller in some newer closed models (He 2024; Lee 2026).
- Agents follow instruction files, yet on average the files do not raise task success and do raise cost (Gloaguen 2026; Khatri 2026).
- Models do not reliably fix their own output from introspection; external feedback from tools and tests does (Huang 2024; Kamoi 2024).

## Not found in this review

These are gaps in what this review found, not claims that nobody has studied them.

- A controlled test of document conventions (overview first, define before use, one place per fact) on a model's answers about a repository's own documentation.
- Any measurement of llms.txt on answer accuracy; Volpini 2026 bundled llms.txt-style instructions with breadcrumbs and search, so the file's own effect cannot be separated.
- A head-to-head of a rule-checking program against model self-review on prose style rules, as opposed to code or maths.
- Headings against no headings on document QA with recent models; He 2024 varied templates for tasks, not reference documents.

## Which human-reader principles transfer

| Principle | Evidence with models | Grade | Verdict |
|---|---|---|---|
| state the purpose first | question before and after the data helps retrieval (Liu 2024); repository overviews do not shorten an agent's search (Gloaguen 2026) | supported with caveat | state the task at the top and again at the end; skip the codebase tour |
| define before use | causal attention cannot look ahead; premise order matters (Chen 2024b); re-reading compensates (Xu 2024a) | measured for reasoning order; untested for documents | keep: definitions above first use |
| short reference distance | recency bias near window limits (Veseli 2025); non-literal links get harder with length (Modarressi 2025) | supported with caveat | keep related facts close and name them with the same words |
| one name per thing | retrieval leans on literal overlap (Modarressi 2025) | supported with caveat | keep: a synonym breaks the match |
| one place per fact | stale copies (Treude 2026) and conflicts (Xu 2024b; dos Santos 2026) hurt; files duplicating existing docs add cost without gain (Gloaguen 2026) | supported with caveat | keep for facts |
| repetition aids memory | repeating the question or prompt helps (Xu 2024a; Leviathan 2025) | supported with caveat | a separate exception: repeat the task, never the facts |
| cut what does not serve | irrelevant text and length lower accuracy (Shi 2023; Levy 2024; Hong 2025) | measured | keep, and it also saves tokens |
| tables for structured data | format changes results; no format is best everywhere (Sui 2024; Ahsan 2026) | supported with caveat | use tables, test the format per model |
| few rules at once | adherence falls with rule count and session length (Jaroslawicz 2025; McMillan 2026) | supported with caveat | keep the instruction file short; check by program |
| working-memory limits, visual layout | see `against.md` | | do not transfer as such |

## What this repository adds

- A split of every rule into what a program can check exactly and what needs judgment, since program feedback is the reliable kind (Kamoi 2024).
- An instruction file limited to rules an agent would not infer, which is where Gloaguen 2026 found the files earn their cost.
- The comparison in `baseline.md`, which would fill the first gap above for this repository's own documents.
