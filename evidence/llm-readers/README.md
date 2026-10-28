# LLM readers

How text and files should be structured when the reader is a large language model, and how a model that writes for the repository is held to its rules.

Steps: [frame](frame.md) · [review](review.md) · [state of the art](state-of-the-art.md) · [position](position.md) · [against](against.md) · [baseline](baseline.md) · [bibliography](../bibliography.md)

## Claims

| Claim | Grade | Where |
|---|---|---|
| Longer input lowers accuracy even when the task is unchanged and the added text is irrelevant. | measured | `state-of-the-art.md`, reading long inputs |
| Irrelevant sentences and passages lower accuracy. | measured | `state-of-the-art.md`, distraction |
| A fact in the middle of a long input is used less well than at the ends; the size of the effect depends on model and length. | supported with caveat | `state-of-the-art.md`; `against.md` |
| Long-context retrieval leans on literal word overlap between question and answer. | measured | `state-of-the-art.md` |
| Meaning-preserving layout changes move accuracy; the effect is model-specific, smaller in some newer models, and no layout is best for every model. | measured | `state-of-the-art.md`, format and order |
| Premises ordered as they are used give better reasoning than shuffled ones. | measured | `state-of-the-art.md` |
| Repeating the question, or the whole prompt, improves accuracy. | supported with caveat | `review.md`, strand 3 |
| Agents follow instruction files, but the files do not raise task success on average and cost about a fifth more. | supported with caveat | `state-of-the-art.md`, instruction files |
| Codebase overviews in instruction files do not help agents find the code to change. | supported with caveat | `against.md` |
| Adherence falls as rules multiply and as a session lengthens. | supported with caveat | `state-of-the-art.md` |
| llms.txt and AGENTS.md improve model accuracy. | convention, untested | `position.md` |
| LLM text carries stylistic markers measurable across a corpus. | measured | `review.md`, strand 5 |
| Detecting LLM text in a single document is unreliable: paraphrase evades detectors, and non-native writing triggers false positives. | measured | `state-of-the-art.md`, model as writer |
| A model reviewing its own output without external feedback does not reliably correct it; tests and tools do. | measured | `state-of-the-art.md`; `baseline.md` |
| Define before use, one name per thing, one place per fact and cutting what does not serve transfer to models. | supported with caveat | `position.md` |
| Human working-memory limits and visual layout cues do not transfer to models as such. | supported with caveat | `against.md` |
