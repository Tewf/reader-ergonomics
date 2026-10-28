# Reader style: novice

## Who

- **Reader:** someone meeting the domain for the first time, reading to understand, not to look up.
- **Expertise:** novice in the subject; may be expert elsewhere, which does not transfer.
- **Reading mode:** front to back, at least on the first pass.

## Overrides

| Principle | Change | Why |
|---|---|---|
| [define before use](../principles/document/define-before-use.md) | strengthen: define every term, including ones "everybody knows" in the field | a novice cannot infer the missing definition; readers with little prior knowledge learn more from explicit, cohesive text (McNamara et al. 1996b) |
| [worked examples with subgoals](../principles/document/worked-examples-with-subgoals.md) | strengthen: solve the first problem of each kind in full, then fade | the worked-example effect is largest for novices (Sweller 2019; Renkl et al. 2004) |
| [overview first](../principles/document/overview-first.md) | strengthen: open with an advance organizer that names the parts before any detail | organizers help most when the reader has no schema yet ([reading order](../evidence/reading-order/)) |
| [short reference distance](../principles/document/short-reference-distance.md) | strengthen: repeat a one-line reminder of a definition at a distant use, with a link | a novice reinstates a forgotten term slowly; a short reminder costs less than a search |
| [shallow nesting](../principles/sentence/shallow-nesting.md) | strengthen: one clause level per sentence | working memory is fully taken by new content |

## Thresholds

```toml
[logical_lines]
trigger = 60   # shorter files, so each one holds one new idea
```

## Open questions

The fading schedule, meaning how many worked steps to remove each time, is not settled for written notes as opposed to tutoring.
