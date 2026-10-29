# 0003: A key names one work across the family, checked from each extension

**Decision:** each repository compares its bibliography with the bibliographies its config names in
`[bibliography_keys] family`; this standard names none, so the extensions read their siblings and it reads no one.

**Status:** accepted, 2026-10-29, in v1.5.0. **Shape:** [decision record](../shapes/decision-record.md).

## Context

- The extensions cite many of the same works, and their rules ask a new key to be checked against the family's
  bibliographies before it is added. Nothing checked it. On 2026-10-29 a comparison by script of the six
  bibliographies (2,356 rows) found 11 keys that named two works and 3 works that carried two keys.
- `citations` resolves each key inside one repository, so it could not see them, and a key held twice in one file
  passed silently: the first row won.
- This standard never reads an extension ([0001](0001-extensions-depend-one-way.md)).
- The closest tool, bibtex-tidy's `--duplicates`, finds a DOI or a key held twice within one BibTeX file.

## Decision

- **One check, `bibliography-keys`, in the program tier.** A key held twice in one file is an error. One work under
  two keys, a key another repository gives another work, and a work it gives another key are warnings, reported at
  the row in this repository's bibliography.
- **A work is named by its link:** the DOI, else the arXiv id without its version, else the address. A DOI or
  arXiv id the citation also names, a preprint beside its journal version, is the same work.
- **The family is named in config**, as folders beside the repository, read at the same bibliography path. Each
  extension lists the others and this standard; this standard lists none. A clash between the standard and an
  extension is reported by the extension.
- **An exception is written by the repositories it concerns**, in `shared_links`, with its reason: two editions on
  their author's page, a book beside its author's site.
- **In CI, an extension checks out the family's default branches beside its own**, by the names in its config.
  A member that is not found is a warning, so a comparison is never passed over unread.
- **This standard's key wins.** An extension that holds one of its keys for another work renames its own. Between
  extensions, the older use keeps the key: the first commit on the default branch that adds its row. The other work
  takes the next letter free in the family. This order is the one that can be checked looking down only: each
  extension against this standard and its siblings.
- **The year in a key is the year of the version read**; a page with no date takes the year it was read.

Who compares with whom, and whose key wins a clash:

```text
 reader-ergonomics        family = [], reads no one
        ▲
        │ compared against; its key wins
        │
 an extension ──compared against──▶ each sibling
                 the older use of a key wins
```

## Consequences

- A clash with this standard surfaces in an extension, at its next push, and the extension renames.
- Each push of an extension checks out its siblings: a few small, shallow copies.
- A new repository in the family is added to each extension's list, and lists them in turn.
- One work under a DOI in one repository and its preprint's arXiv id in another is not matched; one essay at two
  addresses reads as two works. Both are warnings to fix in the data or to explain.

## Considered options

- **The older use wins everywhere.** The rule first applied, on 2026-10-29: presentations had used Microsoft 2026 47
  minutes before this standard did. Checking it would need this standard to read its extensions, against 0001.
- **A local check in each extension.** No change here, but five copies of one check.
- **The list of the family in this standard's config.** One list for all, but this standard would read its
  extensions, against 0001.
- **Siblings fetched over the network by the check.** A request on every run, and none offline; a checkout in CI
  does it once, and a local run reads the checkouts already beside it.
- **A pattern over the parent folder, `reader-ergonomics*`.** One line for every repository, but a worktree or an
  extracted release beside them would join the family unasked.

## See also

[Decisions](README.md); the check, [bibliography_keys.py](../checks/program/bibliography_keys.py); the interface it
adds to, [extending](../extending.md).
