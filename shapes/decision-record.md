# Shape: decision record

One choice that shapes more than one file, and why it was made. Its reader comes later, a maintainer or a model,
and asks why the work is as it is; the record answers in about a page. An extension may add parts for its genre,
such as a table of the options that lost; it keeps these.

## Skeleton

```markdown
# <NNNN>: <the choice, as a short phrase>

**Decision:** <the choice in one sentence; a reader who stops here knows what holds>

**Status:** <proposed, accepted, superseded by NNNN, or withdrawn>, <date>. **Shape:** [decision record](<path to this file>).

## Context              the situation that made a choice necessary, and the facts it rests on

## Decision             what was chosen, in full sentences

## Consequences         what follows, good and bad, and what must stay true

## See also             the folder that lists the records, and the work the choice concerns
```

MADR 2024 adds the options a decision rejected; a record may add such a section after Decision.

## Where each part comes from

| Part | Evidence | Grade |
|---|---|---|
| Number, title, Context, Decision, Consequences | Nygard 2011 | convention, widely adopted |
| Status, with a link to the record that supersedes it | Nygard 2011 | convention, widely adopted |
| The decision in one sentence, first | [overview first](../principles/document/overview-first.md), applied to a record | convention, untested for records |
| The Shape line | names what the record follows, so a reader, or a check, knows its parts | convention, untested |
| See also | [one place per fact](../principles/collection/one-place-per-fact.md): the debate and the work are linked, not copied | convention |

- **Why keep the rationale at all:** in one laboratory experiment, recorded rationale made later decisions more
  effective when the requirements changed, with no gain in speed (Falessi 2010, measured: 50 master students, one
  system).
- **Why keep it to a page:** a lack of time or budget is the reason practitioners give most for not documenting
  rationale. In a survey of 81, 60.5% gave it, before a lack of standards (42%) and of tools (29.6%) (Tang 2006,
  measured). Lee 1997 argued that rationale systems failed on the cost of capture (an argument, read in a summary).
- **What is not known:** whether a record helps a later maintainer find out why has not been tested on maintainers.

## The rules

1. One decision per record, numbered in order, in a `decisions/` folder whose README lists them.
2. The decision comes first, in one sentence.
3. Consequences include the bad ones, and what must be done to keep the decision true.
4. An accepted decision is not changed in place: a new record supersedes it, and the old one's status links forward.
   Its wording may be corrected.

## The principles it applies

| Part | Principle |
|---|---|
| The decision first | [overview first](../principles/document/overview-first.md) |
| Number and title | [names predict content](../principles/collection/names-predict-content.md) |
| See also | [one place per fact](../principles/collection/one-place-per-fact.md) |

## Checked by

`shape-conformance`, declared in `checks/config.toml`: a record holds the headings Context, Decision, Consequences
and See also. The standard's own [decisions](../decisions/README.md) follow this shape.
