# Evidence

One folder per topic, each a literature review in five steps, so that every principle of the
[standard](../standard.md) can be traced to what was measured, by whom, and what speaks against it.

## The steps, the same in every topic

```text
 frame             the field's name for the problem
   ▼
 review            surveys, seminal work, forward citations
   ▼   └─▶ against null results, disputes, failed replications
 state of the art  who holds the record, measured how
   ▼
 position          known, unknown, what this repository adds
   ▼
 baseline          what the principles are compared against
```

| File | Step |
|---|---|
| `frame.md` | 1. the problem in one sentence, and what the field calls it: names, acronyms, synonyms |
| `review.md` | 2. surveys first, then the seminal work, then forward citations, grouped by strand |
| `state-of-the-art.md` | 3. who holds the record on each sub-question, by what method, measured how |
| `position.md` | 4. what is known, what is not, and what this repository adds |
| `against.md` | the evidence against: null results, controversies, failed replications |
| `baseline.md` | 5. the named baseline the principles are compared against, and how |

Every work cited is listed once, in the [bibliography](bibliography.md).

## Topics

| Topic | The question |
|---|---|
| [file-structure](file-structure/) | how to cut content into files and arrange files in folders |
| [documentation](documentation/) | what a repository's pages and code comments must carry |
| [learning-science](learning-science/) | how text is structured so a reader learns and retains more |
| [reading-order](reading-order/) | in what order, and to what depth, a reader should take linked material |
| [psycholinguistics](psycholinguistics/) | how density, locality and nesting in text cost the reader, from the word to the text tree |
| [typography-and-layout](typography-and-layout/) | how text is set and laid out on screen |
| [llm-readers](llm-readers/) | what changes when the reader, or the writer, is a language model |

## Grades

Each topic's README lists its claims with a grade, as defined in the [standard](../standard.md).

## Audit

On 2026-10-28, the 26 claims the principles lean on most were checked against their primary sources:

| Verdict | Claims |
|---|---|
| correct | 15 |
| wrong (misattributed, a wrong value, a wrong link) | 4 |
| imprecise (right direction, narrower scope or other conditions) | 5 |
| unverifiable (the primary source could not be read) | 2 |

All eleven were corrected, or narrowed to what the source supports. The rest of the evidence has not been audited
this way, so a claim is only as good as the review that cites it; a number read only in a summary says "(secondary)".

## Method

The steps follow a thesis literature review:

- frame the problem in the field's words before searching;
- read surveys first;
- keep upper bounds (what has been achieved) apart from lower bounds (what is impossible);
- stop only when the baseline can be named.
