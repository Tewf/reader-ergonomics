# State of the art

Terms are defined in `review.md`; works are listed in the [bibliography](../bibliography.md).

- **Upper bound**: the best that has been achieved or shown.
- **Lower bound**: what has been shown impossible, or ruled out.

## 1. The shape of the linking function f

| Measure | Holder | Method | Result | Grade |
|---|---|---|---|---|
| Reading time, English | Shain et al. 2024 | 6 datasets, many language models, nonlinear regression | f linear in surprisal | measured |
| Reading time, 11 languages | Wilcox et al. 2023 | monolingual and multilingual models | f linear in surprisal | measured |
| Reading time, super-linear claims | Meister et al. 2021; Hoover et al. 2023; Xu et al. 2023 | reading corpora | weak or model-dependent super-linearity | supported with caveat |
| Reading time, cloze-controlled items | Brothers & Kuperberg 2021 vs Buggy et al. 2026 | same items, self-paced reading vs eye-tracking | linear in probability vs logarithmic | contested |
| Acceptability | Meister et al. 2021 | acceptability judgments | non-uniform surprisal lowers acceptability | supported with caveat (one study) |

## 2. Does spreading information evenly lower cost?

A text of n words carries surprisals s_1 ... s_n, with total S = s_1 + ... + s_n.
Its total cost is C = f(s_1) + ... + f(s_n).

- f convex: by Jensen's inequality, C ≥ n·f(S/n), with equality when every s_i = S/n; uniform is the minimum.
- f linear, f(s) = a + b·s: C = a·n + b·S; the distribution does not matter, only n and S do.
- f concave: uniform is the maximum; clustering information is cheaper.
- Cost linear in probability (Brothers & Kuperberg 2021) means f(s) = a - b·2^(-s), which is concave in s.

| Measure | Best-supported f | Consequence at fixed n and S |
|---|---|---|
| Reading time | linear | spreading buys nothing measurable; lowering S or n does |
| Acceptability | convex | uniform surprisal is judged better |

- Grade: the argument is proved; the reading-time verdict is measured; the acceptability verdict is supported with caveat.
- Caveat: a rewrite changes n and S, so "fixed n and S" is an idealization.
- Caveat: cost spills over to the next words, so C is not exactly a sum of independent terms.

## 3. Dependency length

- Upper bound reached by languages: D between random and optimal in all 37 languages of Futrell et al. 2015.
- Degree reached: half of 93 languages at 70% or more of the possible reduction (Ferrer-i-Cancho et al. 2022).
- Not reached: the optimum; observed D stays above it, Indonesian coming closest (Futrell et al. 2015).
- Processing: the cleanest effect is in controlled sentences (Grodner & Gibson 2005); naturalistic reading bounds it (Demberg & Keller 2008).

## 4. Nesting

- Observed maximum of use: degree 3 in writing, practically absent in speech (Karlsson 2007); a corpus count, not a processing limit.
- Processing: degree 2 already yields an illusion in English (Gibson & Thomas 1999) but not in German (Vasishth et al. 2010).

## 5. Text and text tree

- Strongest applied evidence: model-guided revision (Britton & Gülgöz 1991), summarized by Gülgöz et al. 1999.
- Levels effect: recall (Meyer & McConkie 1973), eye-tracking (Wu et al. 2016), conditional on reader skill (Meyer et al. 1980).
- Coherence modelling: the entity grid is the classical baseline (Barzilay & Lapata 2008); neural successors not reviewed here.

## 6. Ordering complexity

| Problem | Bound | Source | Kind | Grade |
|---|---|---|---|---|
| MinLA, general graph | NP-complete | Garey et al. 1976 | lower | measured (theorem) |
| MinLA, tree | polynomial, O(n^2.2) (abstract only) | Shiloach 1979; Chung 1984 | upper | measured (theorem) |
| Projective or planar minimum, tree | linear time | Alemany-Puig et al. 2022 | upper | measured (theorem) |
| Arrangement of an acyclic directed graph | NP-complete | Even and Shiloach, as cited in Shiloach 1979 | lower | supported with caveat (secondary) |
| Linear ordering, rooted tree (root at the left end, each node after all its ancestors) | O(n log n) | Adolphson & Hu 1973, section 3 | upper | measured (theorem) |
| Unit-time scheduling with precedence, weighted completion time | NP-hard | Lawler 1978 (proved in its 1976 report, p. 4; weights arbitrary) | lower | supported with caveat |

- Caveat on the acyclic directed row, cited through Shiloach 1979 (abstract only): its definition of the directed version was not read, nor was Even and Shiloach.
- The rooted-tree row is the ordered version: Adolphson and Hu 1973 (section 2) place each node after its predecessors, so it is not MinLA on an undirected tree.
- Futrell et al. 2015 compare to the projective minimum, not to unconstrained MinLA.
- The unconstrained tree minimum (Chung 1984) is the baseline of Ferrer-i-Cancho et al. 2022.

### Ordering notes as scheduling (derivation in this file)

- Concepts form a directed graph: an edge u → v means v uses u; the order π must put u before v.
- Every edge then points forward, so D(π) = Σ over edges of (π(v) - π(u)) = Σ over x of π(x)·(in(x) - out(x)).
- That is a weighted sum of positions under precedence, with weight w(x) = in(x) - out(x).
- With units of equal length, adding a constant to every weight changes D by a constant, so negative weights are harmless.
- It is then unit-time single-machine scheduling with precedence, minimizing weighted completion time.
- Known: with series-parallel precedence, rooted forests included, that problem is solvable in O(n log n) time once
  the decomposition is given (Lawler 1978; its 1976 report read, the published chapter not). An undirected path need
  not be series-parallel.
- With sections of unequal length, positions become start offsets and the weights keep both signs; standard results assume non-negative weights, so none is claimed.
- Not found: whether weights of the form in(x) - out(x) keep the general case NP-hard; this file makes no such claim.

## 7. Measurement

- Readability: models built from NLP features beat Flesch-Kincaid for adult comprehension, processing and familiarity (Crossley et al. 2017).
- Surprisal source: larger transformer models with lower perplexity fit reading time worse (Oh & Schuler 2023).

## 8. Most adopted, kept apart from best evidence

| Sub-question | Most adopted (practice record) | Best evidence (research record) |
|---|---|---|
| Sentence length | average 20 words (EC 2011); average 15, cap 25 (Style Manual AU 2024) | dependency length, not word count (Futrell et al. 2015; corpus evidence, no comprehension test) |
| Readability number | Flesch floor of 40 to 50 in US state law (NAIC 2025); grade 9 default (Hemingway 2026) | NLP-feature models beat Flesch for adults (Crossley et al. 2017) |
| Nesting | advice to avoid legalese | register of legalese hurt recall, with center-embedding the strongest feature in an exploratory, underpowered model; N = 184 over two experiments (Martinez et al. 2022) |

- No source read here states a comprehension test of any word cap.
- The practice record is convention, untested; the adoption counts are measured, descriptive.
