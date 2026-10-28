# Frame

Terms named here are defined in `review.md`; works are listed in the [bibliography](../bibliography.md).

## The problem in one sentence

How much information should each unit of a text carry, how deeply may units nest, and how far apart may related units sit, so that a reader spends the least effort for the most understanding?

## One problem, five scales

| Scale | Unit | Density | Depth | Locality |
|---|---|---|---|---|
| 1. Information rate | word | surprisal per word | | |
| 2. Sentence locality | dependency | | | head-to-dependent distance |
| 3. Nesting | clause | | center-embedding degree | |
| 4. Text | proposition | propositions per word | | argument overlap across sentences |
| 5. Text tree | idea unit, section | | level in the hierarchy | link between distant sections |
| Ordering | concept | | | definition-to-use distance |

## What the field calls it

| Scale | Field name | Acronym | Seminal authors | Also called |
|---|---|---|---|---|
| 1 | surprisal theory; uniform information density; entropy rate constancy | UID, ERC | Hale; Levy; Jaeger; Genzel & Charniak | predictability effect, linking function, information density |
| 2 | dependency locality theory; dependency length minimization; depth hypothesis | DLT, SPLT, DLM, DDm | Gibson; Futrell; Temperley & Gildea; Ferrer-i-Cancho; Yngve | dependency distance, integration cost, Yngve depth |
| 3 | center-embedding; self-embedding; structural forgetting | none | Miller & Chomsky; Karlsson; Gibson & Thomas | missing-VP illusion, grammaticality illusion |
| 4 | propositional text base; construction-integration; given-new contract | CI | Kintsch; van Dijk; Haviland & Clark | idea density, argument overlap, referential cohesion, reinstatement search, bridging inference |
| 5 | levels effect; rhetorical structure theory; centering; entity grid | RST | Meyer; Mann & Thompson; Grosz, Joshi & Weinstein; Barzilay & Lapata | content structure, macrostructure, local coherence |
| Reader | reverse cohesion effect; expertise reversal effect | none | McNamara; Kalyuga | prior knowledge by text interaction |
| Ordering | minimum linear arrangement; optimal linear ordering; weighted completion-time scheduling | MinLA, MLA, `1\|prec\|ΣwC` | Garey, Johnson & Stockmeyer; Shiloach; Chung; Adolphson & Hu; Lawler | graph layout, linear layout |
| Measurement | automated text analysis; readability formulas | Coh-Metrix, TAACO, FRE | Graesser; McNamara; Crossley; Flesch | text difficulty, cohesion indices |

## What practitioners call it

| Practitioners say | Field says | Scale |
|---|---|---|
| plain language, plain English | text comprehensibility, readability | 4, 5 |
| short sentences, one idea per sentence | idea density, propositions per sentence | 1, 4 |
| reading age, grade level, Flesch score | readability formula (FRE, FKGL) | measurement |
| avoid legalese, passives, nominalisations | center-embedding, dependency length, rare words | 2, 3 |
| readability grade check (Vale, Hemingway, textstat) | automated readability formula | measurement |

- Martinez et al. 2022 joins the two vocabularies: legalese measured as center-embedding, rare words, passives and non-standard capitalisation.

## Search log: each term three ways

| Term | Academic name | Acronym | Author | Outcome |
|---|---|---|---|---|
| UID | "uniform information density" | UID | Jaeger, Meister | rich; led to Meister et al. 2021 and Tsipidi et al. 2024 |
| ERC | "entropy rate constancy" | ERC | Genzel | one arXiv hit, the failed replication Verma et al. 2023 |
| Linking function | "linear" vs "logarithmic" predictability | none | Smith, Levy, Brothers | led to the replication Buggy et al. 2026 |
| DLT | "dependency locality theory" | DLT | Gibson | seminal plus tests Grodner & Gibson 2005, Demberg & Keller 2008 |
| DLM | "dependency length minimization" | DLM, DDm | Futrell, Ferrer-i-Cancho | corpus studies and the baseline dispute |
| Center-embedding | "multiple center-embedding" | none | Karlsson | corpus count; processing studies found separately |
| CI | "construction-integration" | CI | Kintsch | model, revisions, reverse cohesion effect |
| RST, centering | "rhetorical structure theory", "centering" | RST | Mann, Grosz | theory plus corpus test Poesio et al. 2004 |
| MinLA | "minimum linear arrangement" | MinLA, MLA | Shiloach, Chung | complexity results and the graph layout survey |
| Ordered variant | "precedence-constrained linear arrangement" | none | none | zero exact hits: the query was wrong |
| Ordered variant, renamed | "optimal linear ordering"; "weighted completion time" with precedence | `1\|prec\|ΣwC` | Adolphson & Hu; Lawler | found, via the abstract of Shiloach 1979 |
| Readability | "readability formula" | FRE, FKGL | Flesch, Crossley | formula and critiques |

## Scope

- In: comprehension cost and memory for written text by adult readers; corpus regularities of writing; tools that measure them.
- Out: typography, layout and visual design.
- Lower priority: language models as readers (one entry in `position.md`).
