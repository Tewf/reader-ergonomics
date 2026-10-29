# 0001: The extensions depend on the standard, never the reverse

**Decision:** an extension depends on the standard and the standard on no extension; each genre has a repository
of its own, by convention.

**Status:** accepted, 2026-10-29, in v1.1.0. **Shape:** [decision record](../shapes/decision-record.md).

## Context

The standard is general; three extensions apply it to one genre each: academic writing, presentations and writing
about software ([extending.md](../extending.md)). Each extension reads the standard's principles, runs its checks and
extends its config. Two questions about these extensions had no written answer: which way the dependencies may run,
and when a genre deserves a repository of its own. Version 1.0.1 even listed the extensions on the contract page,
which said the standard never links to them.

## Decision

- **An extension depends on the standard; the standard depends on no extension.** It never reads, runs, imports or
  copies what an extension holds. It may list the extensions, as the contract does: a link is a reference, not a
  dependency ([dependencies without cycles](../principles/collection/dependencies-without-cycles.md)).
- **An extension pins a release by its commit**, and moves to a new one on purpose.
- **A rule moves up when it stops being particular.** A principle or check that two extensions need is promoted to
  the standard in a minor release. Both extensions then link to it instead of holding it.
- **A boundary that keeps moving is in the wrong place.** Suppose three releases in a row each force a change in the
  same extension, beyond moving its pin. Then the shared part moves into the standard, or the two repositories merge.
- **One repository per genre is a convention.** It follows the maintainer's rule that a project attacks one problem.
  Over 142 studies, organisation and structure mirrored each other in most firm studies but not in open
  collaborative projects (Colfer 2016, abstract read). No measured result says that splitting by genre helps here.

## Consequences

- An extension changes without asking the standard, and the standard changes only by release.
- A fix in the standard reaches an extension only when the extension moves its pin, so an extension can lag behind.
- A principle can be held in two extensions until it is promoted; the promotion rule bounds how long.

## Considered options

- **One repository with a folder per genre.** One history and one CI. But every change to a genre would be a change
  to the standard, and a genre could not be released, or parked, on its own.
- **Genres on branches of this repository.** Tried until 2026-10-28, when the branches moved to repositories of their
  own so that the standard could be declared done. A branch cannot be released or pinned apart from the rest.
- **The standard gathering the extensions' principles into its card.** Readers would see everything in one place,
  but the standard would depend on every extension, and a cycle would join the two levels.

## See also

[Decisions](README.md); the contract the extensions rely on, [extending.md](../extending.md).
