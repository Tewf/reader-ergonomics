# Short reference distance

**Claim:** each concept sits close to the places that use it, and the order of a document is chosen so that prerequisites come first and the total distance between definitions and uses is small.

- **Grade:** supported with caveat: locality is measured in sentences and applied to documents by analogy.
- **Evidence:** [psycholinguistics](../../evidence/psycholinguistics/state-of-the-art.md) (sections 3 and 6), [against](../../evidence/psycholinguistics/against.md).
- **Check:** `cross-file-terms` (heuristic): a term defined in another folder is linked where it is used; the order of a whole document is judgment.
- **Reader styles:** strengthened by [novice](../../reader-styles/novice.md).

## What it asks

- Define a concept in the part that first needs it ([define before use](define-before-use.md)), not in a glossary far away.
- When a definition is far from a use, give a one-line reminder at the use and link back.
- Order the parts by their prerequisites; among the orders that respect them, prefer the one with the shorter total distance.

## Why

Linking a word to a distant head costs more with each new discourse referent in between (Gibson 1998), and languages keep dependencies
shorter than random reorderings in all 37 languages tested (Futrell et al. 2015).

The order can be computed. Write the concepts as a graph, an edge u → v meaning v uses u, and an order π that puts u
before v. The total distance is

$$D(\pi) = \sum_{u \to v} \big(\pi(v) - \pi(u)\big) = \sum_x \pi(x)\,\big(\mathrm{in}(x) - \mathrm{out}(x)\big).$$

For example, with three prerequisite edges:

```text
 A ──▶ B ──▶ C     order     A→B  B→C  A→D   total
 └──▶ D            A B C D    1    1    3      5
                   A B D C    1    2    2      5
                   A D B C    2    1    1      4  ← shortest
```

In general it is a weighted sum of positions under precedence: single-machine scheduling, solvable in polynomial time when the
prerequisites form a forest (Lawler 1978, abstract only: it names series-parallel precedence, which includes forests). Without precedence it is Minimum Linear Arrangement, NP-complete
in general (Garey et al. 1976) and polynomial on trees (Chung 1984).

## Limits

In natural reading, distance costs weakly outside nouns (Demberg & Keller 2008). Whether the general precedence case
with these weights is NP-hard is not known to this review. A document is reread and searched, which no sentence
experiment measured.
