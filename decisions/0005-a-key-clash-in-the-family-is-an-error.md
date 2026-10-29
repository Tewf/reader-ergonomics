# 0005: A key that names another work in the family is an error

**Decision:** a key that another repository of the family gives another work is an error, like a key held twice in
one file; one work under two keys stays a warning.

**Status:** accepted, 2026-10-29, in v1.14.0. **Shape:** [decision record](../shapes/decision-record.md).

## Context

- [0003](0003-one-key-one-work-across-the-family.md) reported every comparison with the family as a warning.
- CI passes with warnings. On 2026-10-29 `GitHub 2026e` named one work in topic and another in presentations for
  some hours, behind green runs, and a session found it by reading.
- A key held twice is the error a citation cannot recover from: the reader of either repository cannot tell which
  work the key means. Inside one file that was already an error.

## Decision

- **A key another repository gives another work is an error,** reported at the row in this repository's
  bibliography. Its message gives the fix: rename, or give the two rows one link when they are one work at two
  addresses.
- **One work under two keys stays a warning.** A reader who meets both keys finds the same work under each, so
  nothing is misread. The match also rests on links, which one work can carry at two addresses.
- **A family member not found stays a warning,** as in 0003.

## Consequences

- A clash fails the next push of every extension that holds the key, so it is fixed before it is read.
- Between two extensions, the one that keeps the key fails too, until the other renames: the check reads its
  siblings' files, not their history, so it cannot tell which use is older. A clash with this standard fails only
  the extension, since this standard reads no one.
- One work at two addresses under one key now fails. It is fixed in the data, by one link for one work, which
  [one place per fact](../principles/collection/one-place-per-fact.md) asks anyway.
- On the day it shipped the family held no clash, so no extension fails on taking it.

## Considered options

- **Keep the warning.** No failure, but the clash that prompted this sat behind green runs.
- **An error only for two different DOIs or arXiv ids.** It is free of the two-addresses case. But most of the
  family's organisation keys link pages, so the clash that prompted this would still have been a warning.

## See also

[Decisions](README.md); the check, [bibliography_keys.py](../checks/program/bibliography_keys.py); the rule it
changes, [0003](0003-one-key-one-work-across-the-family.md).
