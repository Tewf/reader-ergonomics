# Baseline

Terms are defined in `review.md`; works are listed in the [bibliography](../bibliography.md).

## The named baseline

- **Coh-Metrix** (Graesser et al. 2004; McNamara et al. 2014): a multilevel set of text indices aligned with comprehension theory.
- Its five major factors (Graesser et al. 2011): word concreteness, syntactic simplicity, referential cohesion, causal cohesion, narrativity.
- Index family names in the table below were read in a secondary overview of Coh-Metrix 3.0.
- Plus per-word surprisal from a language model, reported per sentence as mean, maximum and variance (operationalizations as in Meister et al. 2021).
- Floor: Flesch reading ease (Flesch 1948), which a useful rule must beat, and which can be beaten (Crossley et al. 2017).

## Scale to index

| Scale | Coh-Metrix family | Open alternative | Model-based |
|---|---|---|---|
| 1. Information rate | none direct | none | surprisal mean, maximum, variance |
| 2. Sentence locality | syntactic complexity | mean dependency distance (Hansen et al. 2023) | none needed |
| 3. Nesting | syntactic complexity | depth from a parse | none needed |
| 4. Text | referential cohesion, semantic overlap | TAACO local cohesion and givenness (Crossley et al. 2016) | none needed |
| 5. Text tree | situation model, connectives | TAACO global cohesion; sentence coherence (Hansen et al. 2023) | surprisal contour by section (Tsipidi et al. 2024) |

## Tools and their status

| Tool | What it computes | Access |
|---|---|---|
| Coh-Metrix (Graesser et al. 2004) | cohesion, syntax, word and readability indices | web tool; no official source repository found |
| TAACO 2.1 (Crossley et al. 2016) | local, global and text cohesion, givenness | Python and spaCy; source on GitHub; no license file found |
| TextDescriptives (Hansen et al. 2023) | dependency distance, readability formulas, sentence coherence | Python and spaCy; Apache-2.0 |
| minicons (Misra 2022) | word and sentence probabilities from transformer models | Python; MIT |
| Linear Arrangement Library (from the authors of Alemany-Puig et al. 2022) | sums of edge lengths and minimum arrangements | C++ with Python bindings; AGPL-3.0 |

- Model choice matters: larger, lower-perplexity models fit reading time worse (Oh & Schuler 2023); report the model.

## What a check can compute exactly, in polynomial time, without a language model

| Check | Scale | Cost | Exact? |
|---|---|---|---|
| Sentence length, words per sentence | 1, 2 | O(n) | yes, given a tokenizer |
| Flesch reading ease | floor | O(n) | up to the syllable-counting rule |
| Markdown nesting: heading level, list indentation | 3, 5 | O(n) | yes, from syntax alone |
| Definition-to-use distance for marked terms (bold first use) | ordering | O(n), one pass with a hash map | yes |
| Use before definition | ordering | O(n) | yes |
| Ordering cost D(π) of a note's concept graph, and the bound D ≥ number of edges | ordering | O(V + E) | yes |
| Given a dependency parse: D, maximum depth, center-embedding degree, Yngve depth | 2, 3 | O(n) per sentence | yes, given the parse |
| Tree minimum D_min, hence an optimality score | 2 | polynomial (Chung 1984); linear if projective (Alemany-Puig et al. 2022) | yes, given the parse |
| Argument overlap of adjacent sentences | 4 | O(n) | yes, given lemmas |
| Entity grid transitions | 5 | O(sentences × entities) | yes, given entity mentions |

- A parser or lemmatizer is itself a statistical model, but a small local one; parsing runs in polynomial time.
- Not a check: the optimal ordering of concepts, NP-hard in general by the sources in `state-of-the-art.md` §6.
- Not zero-cost: surprisal, which needs one language-model pass per text.

## How this repository's rules are compared

1. Take a text and its rewrite under one rule.
2. Compute the baseline indices and the exact checks for both.
3. Report the differences per scale, never a single score.
4. Claim a reader effect only from reader data: reading time plus questions split into text base and situation model (McNamara et al. 1996b).
5. Run each comparison for at least two reader levels, since cohesion effects reverse with knowledge (O'Reilly & McNamara 2007).

## Practice baseline

People compare against a grade score and a sentence cap, not Coh-Metrix.

| Practice | Number | Source |
|---|---|---|
| Sentence average | 20 words | EC 2011 |
| Sentence average and cap | 15 and 25 words | Style Manual AU 2026 (secondary) |
| Flesch floor in law | 40 to 50 | NAIC 2025 |
| Tool grade target | grade 9 default | Hemingway 2026 |

- Report the grade tools beside the indices above, never in place of them.
- A tool grade is a floor-type baseline, like Flesch; it was not shown to track comprehension.
