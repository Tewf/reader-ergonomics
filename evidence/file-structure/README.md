# File structure: how to cut files and arrange folders for the reader

Question: how should content be cut into files, and files arranged in folders, so that nothing is held twice, each file does one thing, and a reader reaches what they need in few steps.

Steps: [frame](frame.md) · [review](review.md) · [state of the art](state-of-the-art.md) · [position](position.md) · [against](against.md) · [baseline](baseline.md) · [bibliography](../bibliography.md)

## Claims

| Claim | Grade | Where |
|---|---|---|
| Decompose by decisions likely to change; one role per module | supported with caveat | review.md 1 |
| Every clustering objective is a ratio of coupling to cohesion | supported with caveat | review.md 1, 2 |
| Developers do not balance cohesion and coupling the way recommenders do (100 systems, 29 developers) | measured | review.md 2 |
| Automated recovery reaches 38-59 % MoJoFM against expert architectures | measured | state-of-the-art.md |
| Exact minimization of a hierarchy cost is NP-hard | proved (Dasgupta 2016) | position.md |
| 8-16 items per menu level is the optimum for search | measured, on menus | review.md 6 |
| Navigation follows scent; descriptive names are read faster | supported with caveat | review.md 6 |
| Folders must not import each other in a cycle | convention, untested | review.md 5 |
| Co-change and hotspot measures add what imports cannot see | supported with caveat | review.md 7 |
| Size confounds class-level metrics | measured | review.md 6 |
| Smaller files have fewer defects, so files should be split by length | not supported: defects grow more slowly than size | against.md |
