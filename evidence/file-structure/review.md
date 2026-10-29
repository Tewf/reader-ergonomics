# Review: file structure

This page lists each source on cutting files and arranging folders, with what it found. Its eight strands run from modularity to practice.

Surveys first, then the seminal work, then forward citations.

## 1. Modularity: the reasons behind the conventions

- Parnas 1972: decompose by the design decisions likely to change, one hidden per module. Basis of "one role per file" and of "tunables live in config".
- Stevens 1974: the terms **coupling** and **cohesion**. Every clustering objective below is a ratio of the two.
- Chidamber 1994: LCOM, the first measurable cohesion.
- Hunt 1999: DRY, one authoritative representation of each piece of knowledge. Applies to files and notes, not only code.
- Martin 2003: single responsibility, one reason to change.
- Baldwin 2000: the **Design Structure Matrix** (DSM) as the representation of a modular design.
- MacCormack 2006: **propagation cost** from the DSM, the share of files a change can reach.
- Sangal 2005: the DSM as a tool that extracts dependencies, arranges them in a hierarchy and checks design rules.

## 2. Software clustering: choosing the tree

- Wiggerts 1997: the theoretical introduction (which entities, which similarity, which algorithm).
- Mancoridis 1998, Mitchell 2006: **Bunch**. Hill-climbing or a genetic algorithm on **modularization quality** (MQ), intra-edges over inter-edges summed over clusters.
- Kohler 2012: the same problem as a mixed-integer program.
- Tzerpos 1999: **MoJo**, the move-or-join distance between two clusterings. MoJoFM is its normalized form and the standard accuracy measure.
- Shtern 2012: the survey, with quality-assessment methods.
- Garcia 2013: six recovery techniques against eight expert-verified architectures. MoJoFM averages 31 to 59 % (Table II; the text says 38 to 59 %); ARC and ACDC best.
- Harman 2012: the search-based software engineering survey.
- Praditwong 2011: clustering as multi-objective search on 17 systems.
- Mkaouer 2015: NSGA-III with semantics and change history added.
- Bavota 2014: structural plus lexical measures.
- Candela 2016: on 100 open-source systems and a survey of 29 developers, the cohesion and coupling balance that recommenders optimize is not the one developers report. A cost nobody checked against people produces trees nobody wants.

## 3. Hierarchical clustering objectives: scoring the tree

- Dasgupta 2016: the first global cost for a hierarchy over pairwise similarities; each edge pays the number of leaves under its lowest common ancestor. NP-hard; recursive sparsest cut gives O(alpha log n).
- Roy 2017: spreading-metric LP, O(log n); SDP with an O(sqrt(log n)) gap.
- Charikar 2017: sparsest cut is O(alpha) tight; no constant factor under the Small-Set Expansion hypothesis.
- Moseley 2017: the dual maximization; average linkage is a 1/3-approximation.
- Cohen-Addad 2019: the dissimilarity version (average linkage 2/3) and a survey of the line.
- Hogemo 2021: relates Dasgupta's cost to vertex and edge ranking; the family is intractable; a 2-approximation on trees.
- Pan 2021: k-level trees under an information-theoretic cost; a heuristic without guarantee.
- Szyfelbein 2026: clustering into trees with a relaxed halting condition; inherits the SSE hardness.
- This strand never mentions software. It is the clean mathematics the clustering strand lacks.

## 4. Sharing and compression: the merge and factor moves

- Downey 1980: the minimal DAG of a tree in linear time. The result behind "identical subtrees collapse".
- Filliatre 2006: typed **hash-consing** with a parameterized equality.
- Lohrey 2013a, 2013b: how much a real document tree shrinks by sharing alone, and by grammar compression (RePair).
- Lohrey 2015: survey of grammar-based tree compression.
- Bille 2015: **top trees**, sharing patterns with holes.
- A tree grammar with parameters is a near-duplicate factored into a template plus arguments.
- Baxter 1998: clone detection by hashing subtrees into buckets, near-linear.
- Kamiya 2002: CCFinder, token-based.
- Jiang 2007: Deckard, characteristic vectors over the syntax tree.
- Bellon 2007: the benchmark; sets the minimum clone at six lines.
- Roy 2009, Rattan 2013: surveys. Type 1 is identical, type 2 identical up to identifiers and literals, type 3 with statements added or removed, type 4 same behaviour with different text.
- Svajlenko 2015: BigCloneBench.
- Rissanen 1978: minimum description length. Makes "total size after sharing" a legitimate objective.

## 5. Conformance checking: the constraint half as tools

- Murphy 2001: **reflexion models** map code onto a drawn architecture and report convergences, divergences and absences; applied at 1.2 million lines.
- Passos 2010: an illustrative overview of static conformance checking.
- ArchUnit (Java, rules as unit tests), import-linter (Python import contracts), dependency-cruiser (JavaScript rules).
- These check "a must not import b" and cycles. None carries an objective: they say whether a tree is legal, never which legal tree is better.

## 6. The human constants

- Kiger 1984: on 64 targets, the three two-level trees (8x8, 4x16, 16x4) were equally fast and faster than three and six levels; 8x8 was ranked easiest and most preferred. Miller 1981 alone supplies the flatter-menu comparison. Larson 1998, with web sites of 512 items: two levels of 16 by 32 were fastest and three levels of 8 slowest (see [against](against.md)).
- Pirolli 1999: **information foraging theory**.
- Lawrance 2013: programmers navigate code by scent, and a scent model predicts their paths better than a hypothesis model.
- Lawrie 2006, 2007: full words beat abbreviations and single letters for comprehension.
- Binkley 2009: very long names overload short-term memory.
- Hofmeister 2017: shorter names take longer to comprehend.
- Schankin 2018: descriptive compound names are read faster.
- El Emam 2001: once size is controlled, classic object-oriented metrics stop predicting faults; size is the confounder. This says size predicts faults, not that splitting helps: splitting a file keeps the total size. A length bound is defended on reading grounds, not on defect grounds (see [against](against.md)).
- Wiggins 2011: configuration in the environment, separate from code.

## 7. Evolution: what imports cannot see

- Gall 1998: logical coupling from release history.
- Zimmermann 2005: mining version histories for files that change together.
- Tornhill 2015: **hotspots**, size times change frequency; 4 % of code held 72 % of defects in the cited case (secondary: reported from a 2015 talk).
- jscpd and PMD CPD: duplication detectors; jscpd also reads markdown.

## 8. Practice

Every source here is a tool default, a company guide or a practitioner text. All grade as convention, untested: none compared its layout with an alternative. The owner of each page speaks about its own tool.

- Maven 2026: fixed paths such as src/main/java and src/test/java; the stated reason is that users of one project feel at home in another. Tool default.
- Cargo 2026: src/, tests/, examples/ and benches/ by convention, kebab-case target names. Tool default.
- Rails 2026: app/ holds the controllers, models, views, helpers, mailers, jobs and assets together. Framework default.
- Go 2026: start with one flat package; put commands in cmd/ and code to keep private in internal/. It uses placeholder names. Company guide.
- Cox 2021: an issue opened by rsc says the golang-standards layout misdescribes Go, since most packages do not use pkg/. closed on 2023-08-19. Community critique.
- Go 2014: a package under internal/ is importable only from the tree rooted at the parent of internal/. The go command enforced it for the main Go repository in Go 1.4, and the page extends it to any repository from Go 1.5. Language rule.
- Bazel 2026: a target is private to its package unless default_visibility says otherwise, and breaking a dependency's visibility fails the build at analysis. Build tool rule.
- GitHub 2026b: CODEOWNERS maps path patterns to reviewers, the last matching pattern wins, the file must stay under 3 MB. Platform feature.
- Wiggins 2011: configuration lives in environment variables. Litmus test: could the code be open source now without leaking credentials. It calls config files outside version control a huge improvement on constants, yet scattered. Practitioner guide.
- ESLint 2026a: default 300 lines per file; recommendations usually range from 100 to 500. Linter default.
- ESLint 2026b: default 50 lines per function. Linter default.
- Checkstyle 2026: default 2000 lines per file. Linter default.
- Fowler 1999: the Rule of Three, tolerate a second copy and extract at the third, credited to Don Roberts (secondary: read on a Wikipedia page, not in the book).
- Dodds 2020: AHA, avoid hasty abstractions, credited to Cher Scarlett; it calls Write Everything Twice dogmatic. Blog post.
- Microsoft 2024: reserved device names include COM and LPT followed by the superscript digits 1 to 3, with or without an extension. Platform specification.
- Nielsen Norman 2017: mega menus show every option at once and give no numeric limit. Company article.
- Nielsen Norman 2024: a review of 98 tree tests found median task success of 62%, quartiles 37% and 83%. It benchmarks findability and does not test breadth. Company article.
