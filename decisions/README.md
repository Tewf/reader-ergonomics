# Decisions

Why this repository is built the way it is: one record per decision that shapes more than one file, so the reason
lives in one place rather than in commit messages. Each record follows the [decision record](../shapes/decision-record.md) shape, and adds the options the decision
rejected. Both are
conventions, widely used and untested.

| Record | Decision |
|---|---|
| [0001](0001-extensions-depend-one-way.md) | the extensions depend on the standard, never the reverse; one repository per genre |
| [0002](0002-checks-run-in-tiers-by-cost.md) | the checks run in tiers, each as often as its cost allows |
| [0003](0003-one-key-one-work-across-the-family.md) | a key names one work across the family, checked by each extension against the others |

An accepted decision is not changed in place: a decision that changes gets a new record, which names the one it
replaces. Its wording may be corrected; both records were put in the shape in v1.3.0, their decisions unchanged.
