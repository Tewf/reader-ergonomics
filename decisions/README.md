# Decisions

Why this repository is built the way it is: one record per decision that shapes more than one file, so the reason
lives in one place rather than in commit messages. Each record follows the format of Nygard 2011: its context, the decision and its
consequences. It adds the options the decision rejected, as MADR 2024 does. Both are
conventions, widely used and untested.

| Record | Decision |
|---|---|
| [0001](0001-extensions-depend-one-way.md) | the extensions depend on the standard, never the reverse; one repository per genre |
| [0002](0002-checks-run-in-tiers-by-cost.md) | the checks run in tiers, each as often as its cost allows |

A record is not edited once accepted: a decision that changes gets a new record, which names the one it replaces.
