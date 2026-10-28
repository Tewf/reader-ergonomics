# Group by what changes together

**Claim:** a folder holds what serves one purpose and changes together, not files of one type; other ways of grouping are carried by links and indexes.

- **Grade:** supported with caveat.
- **Evidence:** [file structure](../../evidence/file-structure/review.md), [against](../../evidence/file-structure/against.md) (group folders by purpose).
- **Check:** `co-change` (judgment): files that keep changing together but sit in different folders; `type-buckets` (exact): no folder named for a kind of file.
- **Reader styles:** none override it.

## What it asks

- No buckets by type (`docs/`, `assets/`, `misc/`): a figure sits next to the text that uses it.
- A tree can make only one way of grouping primary. Choose the one along which files change together; reach the others through an index, tags or links.
- When two groupings compete (by product or by stage, say), count how often files change together inside each candidate folder in the version history. The grouping that keeps more co-change inside folders is primary.

## Why

Any single decomposition forces every other concern to cut across it, the tyranny of the dominant decomposition
(Tarr 1999). Library science met this first: a faceted classification combines independent aspects in a chosen
citation order, and the aspects cited later are scattered and reconnected by an index (Ranganathan 1937). The common
closure principle groups what changes for the same reasons at the same times (Martin 2017).

## Limits

No controlled comparison of grouping by feature against grouping by layer exists. Declared purpose and actual change
can diverge (Silva 2014).

Where a tool finds files by a folder's name, its convention wins. Cargo expects `src/` and `tests/`, Maven
`src/main` and `src/test` (it allows others), Rails `app/` and `test/`, and Go recommends `cmd/` (Cargo 2026;
Maven 2026; Rails 2026; Go 2026). Those names group by type, yet they predict the content of most repositories
that use the tool. Convention: the tools' own documentation, no study.
