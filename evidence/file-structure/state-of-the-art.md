# State of the art, per sub-problem

Upper bounds (what has been achieved) are kept apart from lower bounds (what is impossible).

| Sub-problem | Record holder | Measured how |
|---|---|---|
| Recover a tree from a dependency graph | ARC and ACDC (Garcia 2013); Bunch as the search baseline | MoJoFM against expert architectures: 31 to 59 % on average (Garcia 2013, Table II) |
| Approximate Dasgupta's cost | recursive sparsest cut, O(sqrt(log n)); average linkage, constant factor on the dual objective | approximation ratio |
| Find duplicated structure | subtree hashing (Baxter 1998), Deckard vectors, CCFinder tokens | precision and recall on Bellon 2007 and BigCloneBench |
| Compress a tree by sharing | minimal DAG (Downey 1980); grammar and top-tree compression beyond it | size of the compressed representation |
| Check architecture rules | ArchUnit, Lattix, import-linter, dependency-cruiser | violations found; no quality score |
| Pick depth and breadth | two levels rather than three; up to 32 items on one level (Miller 1981, Kiger 1984, Larson 1998) | search time and errors on menus of 64 targets and sites of 512 items |

## Upper bounds

- Automated recovery averages 31 to 59 % MoJoFM (Table II), far from what architects draw (Garcia 2013).
- Cohesion and coupling alone do not match developer judgment (Candela 2016).

## Lower bounds

- Minimizing Dasgupta's cost is NP-hard (Dasgupta 2016).
- No constant-factor approximation exists under the Small-Set Expansion hypothesis (Charikar 2017).
- Exhaustive search for modularization quality works only on small systems (Mitchell 2006).

## Most adopted, kept apart from best evidence

The first column is a practice record. The second is a research record. They name different holders.

| Sub-question | Most adopted | Best evidence |
|---|---|---|
| Folders by purpose or by type | by type at the top: Maven, Cargo, Rails (review.md 8) | no controlled study found; Silva 2014 shows declared and actual change diverge |
| Breadth and findability | no figure from practice; Nielsen Norman 2024 gives a tree-test median of 62% | Larson 1998: 16 by 32 fastest, 8 by 8 by 8 slowest |
| Folder boundaries | enforced by tools: Go internal/, Bazel visibility | argued, not measured |
| File length | ESLint 300 lines, Checkstyle 2,000 lines (ESLint 2026a; Checkstyle 2026) | Syer 2015, El Emam 2002: no threshold held |
| Duplication | Rule of Three (Fowler 1999, secondary) | Juergens 2009, Kapser 2008 |
| Configuration source | environment variables (Wiggins 2011) | Xu 2015, Yin 2011; neither compares file with environment |
| Reserved names | Microsoft 2024 list | a platform specification, not a study |
