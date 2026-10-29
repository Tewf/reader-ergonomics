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
| [0004](0004-an-organisation-key-may-carry-a-title-word.md) | an organisation's key may carry a title word after the year instead of a letter |
| [0005](0005-a-key-clash-in-the-family-is-an-error.md) | a key that names another work in the family is an error, not a warning |
| [0006](0006-a-claim-is-graded-clause-by-clause.md) | a claim whose clauses rest on evidence of different strength grades each clause |

An accepted decision is not changed in place: a decision that changes gets a new record, which names the one it
replaces. Its wording may be corrected; both records were put in the shape in v1.3.0, their decisions unchanged.
