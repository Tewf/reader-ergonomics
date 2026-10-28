# Protocol of the multivocal review

How the multivocal review of 2026-10-28 was run, and how its grey sources are scored. The method is the multivocal
literature review (Garousi 2019). It reads research and practice together and scores each practice source for quality.

## What was searched

Eight strands, one agent each: plain language, style guides, linters and tools, answer-first structure, interface and
type, repository layout, learning practice, agent instructions. Each stopped when new sources stopped adding claims,
after reading standards, company guides and practice, tools, practitioner books, communities and practitioner surveys.

## What was not recorded

The search strings and their hit counts were not logged, so the pool cannot be rerun exactly. That is one departure from Garousi 2019; the other is one scorer per topic.

## Quality of grey sources

Twenty criteria (Garousi 2019, Table 7), each scored 1, 0.5 or 0, in eight groups:

| Group | Criteria | Max |
|---|---|---|
| A authority of the producer | reputable publisher; author tied to a reputable organisation; author's other work; expertise | 4 |
| M methodology | clear aim; stated method; authoritative references; limits stated; specific question; particular case | 6 |
| O objectivity | balanced; objective; no vested interest; conclusions follow the data | 4 |
| D date | a clearly stated date | 1 |
| P position | related sources linked or discussed | 1 |
| N novelty | adds something; strengthens or refutes a position | 2 |
| I impact | citations, backlinks, adoption signals | 1 |
| T outlet type | tier 1 = 1 (books, standards, government reports, theses), tier 2 = 0.5 (company pages, talks, news), tier 3 = 0 (blogs, forums) | 1 |

- **Threshold: 10 of 20.** A source below it is kept only as an example of practice, never as support for a claim.
  It may still be quoted for what it says itself (a guide's own rule, a tool's own method); it may not support a
  claim about readers or about the world.
- **A low score sometimes means "not read":** a book or a paywalled page scores 0 on every part not seen, so a score can measure the scorer's access
  rather than the source. Of the 42 sources below 10, 11 carry such a note. Such a source is marked "(secondary)" or "(not read)".
- **A part of a source that was not seen scores 0** on its criteria.
- **Formal sources** (peer-reviewed papers) are not scored this way; they carry their evidence grade.
- **One scorer per topic**, an agent, with no second rater: the scores are a first pass, not an agreement.

Each topic's `sources.md` lists its sources with their kind, their quality and where they are used.
