# Position: what is known, what is not, what this repository adds

This file holds what is known, what is not known, and what this repository adds, under one heading each, plus the formal reading and candidate additions.

## Known

- Each file convention is a known result, sometimes fifty years old, restated for files.
- Modularity, clone detection, conformance checking and menu design each have a literature (review.md).
- A cost function over a hierarchy exists and is hard to optimize (Dasgupta 2016).

## Not known

- This review found no application of a hierarchy objective to a file tree, which is weaker than saying none exists.
- In the papers reviewed here, clustering never merges or factors duplicated content, clone detection never says where the factored result goes, and conformance tools never rank trees.
- The documentation case is nearly absent: clustering and clone work is about code, while prose trees have only Diataxis and the menu studies.
- It is untested whether a low cost matches what maintainers would accept (the standing threat: Candela 2016).

## What this repository adds

- It collects the evidence behind the file conventions in one place and grades each one.
- It applies the same graph model to documentation as to code, by analogy, untested.

## The formal reading

The conventions can be read as one optimization problem, a cost of space plus a weight times reader time over units, tree and parameters. Exact minimization is NP-hard, so this repository checks constraints and never optimizes.

## Candidate additions that are general

| Addition | Source | Grade |
|---|---|---|
| No import cycles between folders | Murphy 2001, ArchUnit, Nx | convention, untested |
| Breadth ceiling: split a folder past about 32 entries | Larson 1998 alone; Kiger 1984 supports fewer levels and menus of about 8, not this figure | supported with caveat, by analogy from menus (see against.md) |
| Enter a folder through its index | Nx public API rule, Bazel visibility | convention, untested |
| Scent test: a newcomer predicts content from the path | Lawrance 2013, Larson 1998 | supported with caveat |
| Co-change edges from version history | Gall 1998, Zimmermann 2005, Tornhill 2015 | supported with caveat |
| Hotspots: size times change frequency | Tornhill 2015 (4 % of code held 72 % of defects in one case, secondary: reported from a 2015 talk) | supported with caveat |
| Duplication ratio | Bellon 2007, jscpd, PMD CPD | convention, untested |
| Propagation cost | MacCormack 2006 | supported with caveat |

## Practice against the evidence

Practice runs ahead of the evidence:

- Layout by tool convention is shipped to every user of Maven, Cargo and Rails with no comparison against an alternative. The one stated reason is familiarity across projects (Maven 2026).
- The Rule of Three is a numeric threshold whose source is a book attribution (Fowler 1999, secondary). Dodds 2020 and Metz 2016 argue against abstracting too early, still without a study.
- Language and build tools turn folders into checked units: Go internal/ and Bazel visibility fail the build, CODEOWNERS routes review by path. No study measures their effect on readers.

Practice ignores the evidence:

- Linter defaults differ by a factor of about 7 (300 against 2000 lines), so none can be the optimum for all repositories. Syer 2015 and El Emam 2002 found no size threshold that held.
