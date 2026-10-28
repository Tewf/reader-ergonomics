# Review

Order inside each strand: definitions, seminal work, forward citations.

## Surveys read first

- Gibson et al. 2019: efficiency as one explanation for lexicon, syntax and processing; vocabulary for strands 1 and 2.
- Temperley & Gildea 2018: corpus, simulation and comprehension evidence for shorter dependencies.
- McNamara & Magliano 2009: comparison of text comprehension models, construction-integration among them.
- Díaz et al. 2002: graph layout problems, with complexity, bounds and heuristics.

## 1. Information rate

- **Surprisal** of word w_i: s_i = -log2 P(w_i | w_1 ... w_(i-1)); Hale 2001 proposed it as processing cost.
- Levy 2008 derived the same cost as the size of the belief update over interpretations.
- **Linking function** f: the map from s_i to processing cost.
- **Uniform information density (UID)**: speakers prefer to spread information evenly (Levy & Jaeger 2007; Jaeger 2010).
- **Entropy rate constancy (ERC)**: information per sentence, given its context, stays constant through a text (Genzel & Charniak 2002).
- Jaeger 2010: in speech corpora, the optional complementizer "that" is kept more often where the clause onset is less predictable.
- Genzel & Charniak 2002: out-of-context sentence entropy rises with sentence position, as a constant in-context rate predicts (n-gram models).
- Smith & Levy 2013: reading time is linear in surprisal over six orders of magnitude of predictability.
- Meister et al. 2021: reading times fit a weakly super-linear f; acceptability shows a clearer penalty for non-uniform surprisal.
- Hoover et al. 2023: with better language models, reading time grows super-linearly in surprisal, and so does its variance.
- Brothers & Kuperberg 2021: self-paced reading (N = 216), picture naming (N = 36) and an eye-tracking meta-analysis (N = 218) show cost linear in probability.
- Wilcox et al. 2023: in 11 languages from 5 families, surprisal predicts reading time in all of them and contextual entropy adds to it in most (significant when pooled), with a linear link.
- Xu et al. 2023: in eye-tracking corpora of 7 languages, super-linearity appears in some, and depends strongly on the language model.
- Shain et al. 2024: 6 reading datasets, many language models, nonlinear regression: f is linear in surprisal.
- Buggy et al. 2026 (preprint): the materials of Brothers & Kuperberg 2021, read with eye-tracking, give a logarithmic effect of probability.
- Verma et al. 2023: neural language models do not reproduce clear entropy rate constancy.
- Tsipidi et al. 2024: surprisal contours of long discourses follow position in a hierarchical discourse structure.

## 2. Sentence locality

- **Dependency length**: distance in words between a head and its dependent; D is the sum over a sentence.
- **Dependency locality theory (DLT)**: linking a word to a distant head costs in proportion to the new discourse referents in between (Gibson 1998; Gibson 2000).
- **Yngve depth**: constituents a left-to-right producer has promised but not yet built; Yngve 1960 proposed a limit near seven.
- Grodner & Gibson 2005: two self-paced reading studies: integration difficulty grows with intervening material.
- Demberg & Keller 2008: in an eye-tracking corpus, DLT cost does not predict reading time for words in general, only for nouns.
- Lewis & Vasishth 2005: cue-based retrieval with decay and interference, an alternative to counting distance.
- Futrell et al. 2015: in 37 languages, D is shorter than random projective reorderings and longer than the projective optimum.
- Ferrer-i-Cancho et al. 2022: an optimality score over 93 languages: half reach 70% or more of the possible reduction.
- Futrell et al. 2020: locality follows from surprisal computed over a lossy memory of the context.
- Sampson 1997: an English corpus shows a bias against left-branching, but no sharp depth limit.

## 3. Nesting depth

- **Center-embedding**: a clause inside another, with outer material on both sides; its **degree** counts nested clauses.
- Miller & Chomsky 1963: center-embedded sentences are grammatical; their difficulty is a limit of finite memory.
- Miller & Isard 1964: self-embedded sentences are harder to learn in free recall (secondary).
- Karlsson 2007: 119 multiple center-embeddings in 7 European languages: degree at most 3 in writing, practically none in speech.
- Gibson & Thomas 1999: doubly nested relative clauses missing the middle verb phrase are rated as acceptable as complete ones.
- Vasishth et al. 2010: in seven experiments, dropping the middle verb eases English reading and hurts German reading.
- Hahn et al. 2022: a model trading memory precision against prediction fits nesting difficulty in English, Spanish and German data.

## 4. Text

- **Proposition**: a predicate with its arguments; the **text base** is the network of a text's propositions.
- **Situation model**: what the reader builds about the topic, from text base plus knowledge.
- **Argument overlap**: two propositions share an argument; **reinstatement search**: retrieval from memory when nothing in the buffer overlaps.
- Kintsch & Keenan 1973: reading time followed the number of propositions more than the number of words (secondary).
- Kintsch & van Dijk 1978: cycles through a limited buffer, coherence by argument overlap, macro-operators that reduce to gist.
- Miller & Kintsch 1980: the model applied to readability of short passages. Abstract only: 20 texts and 600 undergraduates, with readability as reading time per proposition recalled. Predictions of readability, reading time and recall reached r = .8 to .9.
- Kintsch 1988; Kintsch 1998: construction-integration: bottom-up activation, then integration by spreading activation.
- Haviland & Clark 1974: the **given-new contract**: a sentence is read faster when its given part has a direct antecedent (secondary).
- Britton & Gülgöz 1991: the model located inference calls in a 1000-word text; each was repaired into a principled revision.
- Gülgöz et al. 1999: revisions that add missing links help learning, most of all for readers short of inference skill, knowledge or motivation (secondary).
- Gopen & Swan 1990: old information in the topic position first, new information in the stress position last, subject near its verb.

## 5. Text tree

- **Content structure**: the hierarchy of idea units; the **levels effect**: units high in it are recalled better.
- Meyer & McConkie 1973; Meyer 1975: higher idea units recalled more often (two passages, 69 undergraduates; secondary).
- Meyer et al. 1980: good ninth-grade comprehenders follow top-level structure; signaling helps underachievers.
- Hyönä et al. 2002: adult readers who attend to headings have the largest working memory and write the best summaries.
- Wu et al. 2016: in eye-tracking, a changed word slowed reading at the top of a three-sentence hierarchy, not at the bottom.
- **Rhetorical structure theory (RST)**: a text is a tree of relations between nucleus and satellite spans (Mann & Thompson 1988).
- **Centering**: each utterance has one backward-looking center linking it to the previous one (Grosz et al. 1995).
- Gordon et al. 1993: in five reading-time experiments, that center is best realized as a pronoun, usually the subject.
- Poesio et al. 2004: in corpora, the pronoun rule holds under most settings; the uniqueness constraint depends on settings.
- **Entity grid**: a sentence-by-entity table of grammatical roles; it ranks orderings and summaries by coherence (Barzilay & Lapata 2008).

## 6. Reader dependence

- **Reverse cohesion effect**: high-knowledge readers learn more from a low-cohesion text (McNamara et al. 1996b).
- McNamara & Kintsch 1996a: high coherence helped recall; high-knowledge readers did better on open questions after low coherence.
- O'Reilly & McNamara 2007: with 143 students, the low-cohesion benefit held only for less skilled high-knowledge readers.
- **Expertise reversal effect**: support that helps novices can hurt more experienced learners (Kalyuga et al. 2003).
- A 1998 study reviewed in Kalyuga 2003: explanatory notes in a text helped readers with low language competence and slowed more knowledgeable readers.
- Davison & Kantor 1982: splitting sentences removes connectives, which shifts the inference load to the reader; some of the best adaptations made sentences longer.

## 7. Ordering and measurement

- **Minimum linear arrangement (MinLA)**: vertices on a line, minimizing the sum of edge lengths; results in `state-of-the-art.md`.
- Flesch 1948: reading ease from sentence length and syllables per word.
- Coh-Metrix: Graesser et al. 2004; McNamara et al. 2014; Graesser et al. 2011; open tools in `baseline.md`.

## 8. Practice

Kinds: G government guide, L law, T tool, P paper. Practice is **convention, untested** unless a study is named; adoption figures are **measured, descriptive**.

- EC 2011 (G): average of 20 words per sentence, with a few short ones; keep link words when splitting; the guide calls its advice "hints, not rules".
- Style Manual AU 2024 (G): "an average of 15 words and no more than 25 words"; read on the archived page (updated 2024-12-19), which cites no study.
- GSA 2026 (G): gives no word count and cites no study; it grounds the advice in the Plain Writing Act of 2010.
- NAIC 2025 (L): a chart of US state insurance rules; minimum Flesch score 40 in WV, NH, MT and NV, 45 in FL and NY, 50 in ME and NC.
- Vale 2026 (T): averages the listed metrics (Gunning Fog, Coleman-Liau, Flesch-Kincaid, SMOG, ARI); a `grade` parameter sets the highest acceptable level; owner documentation.
- Hemingway 2026 (T): grade score; the Editor Plus default target is grade 9; the page names no formula; owner documentation.
- textstat 2026 (T): MIT-licensed readability library, 1.4k GitHub stars on 2026-10-28; its README calls SMOG on texts under 30 sentences statistically invalid.
- Redish 2000 (P, commentary, read in full): formulas were built for children's school books and ignore reader differences, layout and retrieval aids.
- Redish 2000 reports that about half of 36 studies improved comprehension by improving scores. Revised jury instructions were understood better yet scored worse. A very poor score remains a red flag.
- Schriver 2017 (P, secondary): a review of 1940 to 2015 finds formulas often unreliable and invalid; usability testing is the best benchmark; read on an advocacy page.
- ISO 2023 (standard, preview read): plain language focuses on how well readers can use a document, not on mechanical measures such as readability formulas (p. v).
- Martinez et al. 2022 (P): in about 10 million words, contracts carry more rare words, center-embedding (0.729 vs 0.272 per sentence, OR = 2.56), passives (0.758 vs 0.160, OR = 4.35) and non-standard capitalisation than nine other genres.
- Martinez et al. 2022: two experiments pooled to N = 184 (108 retained in the first). Legalese lowered recall (42.4% vs 35.3%) and comprehension (beta = -0.179), also for readers with high reading experience, and the comprehension result replicated with the text in view and a bonus. Center-embedding showed the strongest register effect in an exploratory model with insufficient power per structure. Excerpts were written by a lawyer-author and read by laypeople online, and recall was delayed. The authors link the cost to working memory for long-distance dependencies.
