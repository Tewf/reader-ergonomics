# Evidence

One folder per topic, each a literature review in five steps. Every principle of the [standard](../standard.md) can be
traced through them to what was measured, by whom, and what speaks against it.

## The steps, the same in every topic

```text
 frame
 │   the field's name for the problem
 ▼
 review
 │   surveys, seminal work, forward citations
 ├─▶ against
 │     null results, disputes, failed replications
 ▼
 state of the art
 │   who holds the record, measured how
 ▼
 position
 │   known, unknown, what this repository adds
 ▼
 baseline
     what the principles are compared against
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

Three audits checked claims against their primary sources on 2026-10-28, each by agents that had not written the
lines they checked. The first took the 26 claims the principles lean on most. The second took every line of the
evidence files that carries a number: 109 lines, of which 17 repeated a claim the first had settled. The third took
the 411 lines the multivocal review added, in the evidence and in the principles.

| Verdict | First | Second | Third |
|---|---|---|---|
| correct | 15 | 34 | 87 |
| wrong (misattributed, a wrong value, a wrong link) | 4 | 10 | 2 |
| imprecise (right direction, narrower scope or other conditions) | 5 | 40 | 46 |
| unverifiable (the primary source could not be read) | 2 | 8 | 22 |
| research in the repository left uncited for a practice source | | | 2 |
| a change that broke the principle it changed | | | 3 |

The audits corrected every line they found wrong, imprecise or self-breaking, or narrowed it to what the source supports, here
and in the principles that repeat it. An unverifiable line was read again; if it still could not be read, it says
"(secondary)" or "(not verified)", or was removed. The audits also fixed DOIs, titles and links in the bibliography.
The audits did not cover claims without a number in the original reviews: such a claim is only as good as the review that cites it.

## Multivocal review

On 2026-10-28 every topic was read again for what exists outside the academic literature: standards, company guides
and practice, tools, practitioner books, communities and practitioner surveys. The method is the multivocal
literature review (Garousi 2019). Eight agents searched eight strands and found about 240 sources, some read only in a summary.

The agents that merged them were asked to re-read each claim on its page; the third audit then checked 162 claims from
the 411 lines added, and later passes read 26 works in full. A claim read only in a summary or an abstract says so.

The grey sources were then scored on the method's quality criteria ([protocol](multivocal-protocol.md)); each topic's
`sources.md` lists the scores. One scorer per topic, so the scores are a first pass, not an agreement.

| Result | Count |
|---|---|
| sources added to the bibliography | 76 |
| principles whose grade changed | 0 |
| principles given a new limit or caveat, each with its own grade | 9 |
| principles whose one-line claim changed | 0 (one widening, on practice alone, was reverted by the audit) |
| principles whose limits, numbers or evidence changed | 18 |
| grey sources scored on the protocol's 20 criteria | 125 |
| scored below 10, so examples only, never support | 40, of which 9 were not read at all and 8 only in part (an abstract, a record, a summary page) |

- **No practice source raised a grade.** Practice shows what is done; an outcome it reports is its owner's claim.
- **Overview first is not importance first.** Putting the main fact first, as news does, has no tested support: two
  theses disagree, and the plain-language standard advises it as a convention.
- **Practice sets numbers without studies:** sentence lengths, line lengths up to 90 characters, file-length limits.
- **11 of the 31 checks have no counterpart** among the tools searched, and 7 have one that does the same job; see
  [checks](../checks/README.md).

## Method

The steps follow a thesis literature review:

- frame the problem in the field's words before searching;
- read surveys first;
- keep upper bounds (what has been achieved) apart from lower bounds (what is impossible);
- stop only when the baseline can be named.
