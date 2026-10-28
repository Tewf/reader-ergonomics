# Baseline: what the file conventions are compared against

The review is finished because the baselines can be named. All three run on the same reference graph of a repository (files as nodes, imports and links as edges).

| Baseline | What it is | Compared on |
|---|---|---|
| A, a hand-made tree | the folder layout a maintainer built by judgment, as it stands | cost of the tree, and the share of proposed moves a maintainer would accept (top ten) |
| B, Bunch | MQ hill-climbing on the graph, flat (Mancoridis 1998, Mitchell 2006) | MoJoFM distance to A, and cost |
| C, average linkage | agglomerative clustering, a constant-factor approximation of the hierarchy objective (Moseley 2017, Cohen-Addad 2019) | MoJoFM distance to A, and cost |

## Reading the result

- If A beats B and C on cost while its top proposed moves are accepted, the conventions are calibrated.
- If B or C beat A and their moves are refused, the Candela 2016 finding has reproduced: the cost needs a term the literature lacks.
- Constraint checks (no cycles, breadth ceiling, entry through an index) need no baseline: they pass or fail.
