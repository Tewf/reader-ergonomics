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
