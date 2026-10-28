# Reader style: expert

## Who

- **Reader:** someone who knows the domain and reads for what is new, often arriving from a search.
- **Expertise:** expert in the subject.
- **Reading mode:** by search and by section, out of order; rereads to check one fact.

## Overrides

| Principle | Change | Why |
|---|---|---|
| [worked examples with subgoals](../principles/document/worked-examples-with-subgoals.md) | relax: show the first use of a method only, then state results | expertise reversal: worked steps an expert does not need slow them down (Kalyuga et al. 2003) |
| [define before use](../principles/document/define-before-use.md) | relax: define what is new or used in a non-standard sense; cite the rest | some readers with high prior knowledge learn more from a less cohesive text that makes them infer (McNamara et al. 1996b), but strategic high-knowledge readers do better with the cohesive one (O'Reilly & McNamara 2007): relax only for high-knowledge readers who are less skilled at reading |
| [names predict content](../principles/collection/names-predict-content.md) | strengthen: headings and file names carry the field's exact terms | an expert navigates by search and by scent; the field's term is the query they type |
| [one place per fact](../principles/collection/one-place-per-fact.md) | unchanged, and the cheapest win | an expert follows a link without losing the thread |

## Thresholds

```toml
[logical_lines]
trigger = 120   # an expert reads a long reference file by search, not end to end
```

## Open questions

Where the boundary between intermediate and expert falls for a given text is an empirical question, measured with a short pretest of prior knowledge.
