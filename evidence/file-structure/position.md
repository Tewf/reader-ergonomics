# Position: what is known, what is not, what this repository adds

## Known

- Each file convention is a known result, sometimes fifty years old, restated for files.
- Modularity, clone detection, conformance checking and menu design each have a literature (review.md).
- A cost function over a hierarchy exists and is hard to optimize (Dasgupta 2016).

## Not known

- Nobody has applied a hierarchy objective to a file tree.
- No clustering paper merges or factors duplicated content; no clone paper says where the factored result goes; no conformance tool ranks trees.
- The documentation case is nearly absent: clustering and clone work is about code, while prose trees have only Diataxis and the menu studies.
- It is untested whether a low cost matches what maintainers would accept (the standing threat: Candela 2016).

## What this repository adds

- It reads the conventions as constraints plus measurements on one reference graph.
- It extends the same graph model unchanged from code to documentation.
- It tests agreement with a maintainer's choices before it tests a lower cost.

## The formal reading

The conventions can be read as one optimization problem, a cost of space plus a weight times reader time over units, tree and parameters. Exact minimization is NP-hard, so this repository checks constraints and never optimizes.

## Candidate additions that are general

| Addition | Source | Grade |
|---|---|---|
| No import cycles between folders | Murphy 2001, ArchUnit, Nx | convention, untested |
| Breadth ceiling: split a folder past about 16 entries | Miller 1981, Kiger 1984, Larson 1998 | measured, on menus |
| Enter a folder through its index | Nx public API rule, Bazel visibility | convention, untested |
| Scent test: a newcomer predicts content from the path | Lawrance 2013, Larson 1998 | supported with caveat |
| Co-change edges from version history | Gall 1998, Zimmermann 2005, Tornhill 2015 | supported with caveat |
| Hotspots: size times change frequency | Tornhill 2015 (4 % of code held 72 % of defects in one case) | supported with caveat |
| Duplication ratio | Bellon 2007, jscpd, PMD CPD | convention, untested |
| Propagation cost | MacCormack 2006 | supported with caveat |
