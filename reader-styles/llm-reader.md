# Reader style: language model

## Who

- **Reader:** a language model given the text as context, to answer questions about it or to write more in the same repository.
- **Expertise:** broad and shallow. It knows the field's vocabulary and nothing about this repository.
- **Medium:** a context window. Every token costs time and money, and where a fact sits in the window can matter.
- **Reading mode:** everything at once, attending unevenly.

## Overrides

| Principle | Change | Why |
|---|---|---|
| [one place per fact](../principles/collection/one-place-per-fact.md) | strengthen: load only what the task needs, with nothing repeated | longer input lowers accuracy even when the added text is irrelevant; distracting passages lower it more (measured) |
| [names predict content](../principles/collection/names-predict-content.md) | strengthen: one name per thing, the same word in the question, the rule and the text; no synonyms for variety | long-context retrieval leans on literal word overlap (measured) |
| [define before use](../principles/document/define-before-use.md) | strengthen: give premises in the order they are used | ordered premises give better reasoning than shuffled ones (measured) |
| [overview first](../principles/document/overview-first.md) | strengthen: the task and the rules at the start, restated at the end of a long context | facts in the middle are used less well, by an amount that depends on model and length (supported with caveat) |
| [signal the structure](../principles/page/signal-the-structure.md) | change: one consistent format, without expecting any format to be best | layout changes move accuracy, differently for each model (measured) |
| [draw relations](../principles/page/draw-relations.md) | replace: give the relation as text (an edge list or a table), with the figure optional | a model without vision reads only the text |
| [shallow nesting](../principles/sentence/shallow-nesting.md) | relax | human working-memory limits do not carry over as such (supported with caveat) |

All of these are in [evidence/llm-readers](../evidence/llm-readers/).

## When the model writes

- **Keep the instructions short.** Agents follow instruction files, but in the one measured comparison the files did not raise task success, and adherence fell as rules multiplied and as a session went on (supported with caveat, preprints). So the instructions are a one-page card, [standard.md](../standard.md), and enforcement does not rest on them.
- **Check with programs, not with the model.** A model reviewing its own output without outside feedback does not reliably correct it, while tests and tools do (measured). So the model writes, runs `python3 checks/run.py .`, fixes every error, and answers the questions in `checks/out/needs-judgment.md`.
- **Do not detect, check.** Detecting model-written text in a single document is unreliable (measured). A rule is enforced by what the text does, never by guessing who wrote it.

## Thresholds

None changed.
