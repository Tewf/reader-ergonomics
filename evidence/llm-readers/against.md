# Against: what does not transfer, what changed, what is an artefact

This file lists what does not transfer from human readers, results that changed with newer models, contradictions, benchmark artefacts and weak sources, one section each.

## What does not transfer from human readers

- Working-memory limits: a human holds a few chunks at once; a model attends to its whole context. Its limits take other shapes: length, rule count, position (Levy 2024; Jaroslawicz 2025; Liu 2024).
- The analogy is not empty: one model showed an n-back capacity limit resembling the human one (Gong 2024). The mechanism and the remedy still differ.
- Visual cues: bold, colour, alignment, white space and line length act on the eye. To a model they are tokens or nothing, and their effect is a model-specific format effect, not visual hierarchy (Sclar 2024).
- Skimming: a human skips what is irrelevant at no cost. A model pays for every token, and every token can distract (Shi 2023; Hong 2025).
- Restating for emphasis: repeating the question helps a model (Xu 2024a), but restating a fact in a second file creates a copy that goes stale (Treude 2026).
- Coherent flow: in Hong 2025 a needle was found more often in shuffled text than in coherent text, across all 18 models. This measures a needle's salience against its background, not comprehension.
- Orientation maps: an overview helps a human navigate; codebase overviews in instruction files did not shorten agents' paths to the files they edited (Gloaguen 2026).

## Results that changed with newer models

- Format sensitivity fell from GPT-3.5 to GPT-4 (He 2024), and recent closed-weight models pay little format tax (Lee 2026).
- Sclar 2024's largest spreads come from 2023 open models in few-shot prompts; their size in current models is not established here.
- Lost in the middle has not replicated consistently in later long-context studies (Veseli 2025), and did not appear for one NIAH task in 18 models (Hong 2025).
- Plain NIAH is nearly solved (Hsieh 2024a), so a high NIAH score no longer says a model reads long documents well.
- Self-correction failed for prompted models (Huang 2024), but models trained for it do self-correct (Kumar 2025; Kamoi 2024).
- Prompt repetition is reported for non-reasoning use only (Leviathan 2025); the effect with reasoning enabled is not claimed.

## Contradictions

- Instruction files cut runtime and output tokens in Lulla 2026, but raised cost by about a fifth in Gloaguen 2026.
- Khatri 2026 proposes a reason: each agent has its own band of borderline tasks, and studies sample different bands.
- Random passages raised RAG accuracy in Cuconasu 2024; that is one study with an unclear mechanism, not advice to add noise.

## Benchmark artefacts

- Plain NIAH rewards literal word matching between question and needle (Modarressi 2025).
- A single prompt format makes model rankings arbitrary, because format effects correlate weakly between models (Sclar 2024).
- Earlier self-correction gains used oracle labels to decide when to stop (Huang 2024; Kamoi 2024).
- In Zarzycki 2026, annotating models agreed with each other more than with the human reviewer: an LLM-labelled corpus can share its labellers' bias.
- McMillan 2026 measured compliance with one trivial annotation rule, a narrow outcome for conclusions about whole files.

## Weak sources

- The instruction-file studies (Gloaguen 2026; Lulla 2026; Khatri 2026; McMillan 2026; Zarzycki 2026) are preprints.
- Hong 2025 is a company technical report; its page gives no per-condition accuracies.
- Corpus-level prevalence estimates (Kobak 2025; Liang 2024) cannot classify a single document, and per-document detectors are unreliable (Sadasivan 2023; Liang 2023).

## Practice that contradicts a principle

- Vendors cap file size (Anthropic 2026b; OpenAI 2026a); the standard says size alone never decides a split. A file under a cap can still fail the one-role test.
- Vercel 2026 found a copied index beat a link, against the principle that every other place links. The link was often never followed: the skill went uninvoked in 56% of cases.
- OpenAI 2025 reports JSON delimiters did particularly poorly for long document sets. This is a vendor test with no data shown, and a model-specific result is expected (Sclar 2024).
- Vendor pages are owners' claims about themselves: Anthropic 2026a, Anthropic 2026b, OpenAI 2025, OpenAI 2026a, Vercel 2026.
