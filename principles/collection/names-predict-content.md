# Names predict content

**Claim:** a reader can predict what a file, folder or heading holds from its name before opening it, and each thing has one name throughout.

- **Grade:** supported with caveat for names that predict content; one name per thing argued from
  theory for people and supported with caveat for language models.
- **Evidence:** [file structure](../../evidence/file-structure/review.md), [against](../../evidence/file-structure/against.md) (names), [LLM readers](../../evidence/llm-readers/).
- **Check:** `name-matches-title` (heuristic): the name's words appear in the title or opening; `name-content` (meaning): name and opening close in meaning; `bibliography-keys` (exact in one file, heuristic across repositories): one key, one work.
- **Reader styles:** strengthened by [expert](../../reader-styles/expert.md) and [LLM reader](../../reader-styles/llm-reader.md).

## What it asks

- Full words for anything seen from far away: files, folders, headings, public names.
- Short names are fine in a small scope, and so are abbreviations the reader already knows (URL, HTML, README): a name's length follows its scope.
- One name per thing. A synonym used for variety reads as a second thing.
- The field's own term, which is what a reader types into search.

## Why

Readers navigate by **information scent**, the cues a label gives about what lies behind it (Pirolli 1999). Full words
gave the best comprehension of code (Lawrie 2006). Long-context retrieval in language models leans on literal word
overlap between question and text (see [LLM readers](../../evidence/llm-readers/)), so a thing with two names is
found under one of them only. For people, one name per thing is argued from a model of comprehension, in which each
sentence links to the last by a shared word (Kintsch 1978); no study tests it for names.

## Limits

Full words were often not significantly better than well-known abbreviations (Lawrie 2007), and longer names took
longer to process and lowered recall (Binkley 2009): good naming also limits length.
