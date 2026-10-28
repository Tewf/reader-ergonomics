# State of the art: who holds each record, and how it was measured

**Upper bound**: the best result achieved so far. **Lower bound**: the worst failure shown so far. The two are separate claims; improving one says nothing about the other.

## Reading long inputs

| Sub-question | Upper bound | Lower bound | Measured how |
|---|---|---|---|
| literal fact in long input | most of 17 models near-perfect on plain NIAH (Hsieh 2024a) | only half of models claiming 32K tokens stay satisfactory at 32K on harder tasks (Hsieh 2024a) | synthetic tasks, accuracy against length |
| fact without word overlap | GPT-4o: 99.3% short, 69.7% at 32K, among the best (Modarressi 2025) | 11 of 13 models below half their short-input score at 32K (Modarressi 2025) | NoLiMa needles, 13 models |
| fact in the middle | question before and after the data: key-value retrieval near-perfect, from a 45.6% worst case (Liu 2024) | GPT-3.5-Turbo with the answer in the middle: 53.8% (20 docs), below its 56.1% closed-book; its 16K version 50.5% (30 docs), below 56.0% (Liu 2024) | multi-document QA and key-value retrieval, six models |
| fixing the middle | attention calibration: up to 15 points on RAG tasks (Hsieh 2024b) | | RAG benchmarks |
| length alone | focused inputs of about 300 tokens beat full ones of about 113k tokens, all model families (Hong 2025) | accuracy falls far below the technical limit with padding alone (Levy 2024) | 306 LongMemEval prompts; padded QA |

## Format and order

| Sub-question | Upper bound | Lower bound | Measured how |
|---|---|---|---|
| input format | GPT-4 more robust to template changes than GPT-3.5 (He 2024) | 76 accuracy points between formats, LLaMA-2-13B, few-shot (Sclar 2024); up to 40% for GPT-3.5-turbo on code translation (He 2024) | same content, meaning-preserving variants |
| answer format | most recent closed-weight models show little loss (Lee 2026) | stricter format constraints, larger reasoning loss (Tam 2024) | free-form against JSON, XML, YAML |
| premise order | premises in proof order: best accuracy (Chen 2024b) | permuting them: drops of over 30% (Chen 2024b) | deductive tasks and R-GSM |
| repetition | question read twice improves reasoning on most of 14 datasets, a few drops on vanilla ChatGPT (Xu 2024a) | | 112 experiments |

## Distraction

| Sub-question | Upper bound | Lower bound | Measured how |
|---|---|---|---|
| irrelevant sentences | self-consistency and an "ignore irrelevant information" instruction recover part of the loss (Shi 2023) | large drop on GSM-IC across the prompting methods tested (Shi 2023) | grade-school maths with one added sentence |
| irrelevant passages | 1,000 training examples make a model robust (Yoran 2024) | retrieval lowers accuracy on some questions (Yoran 2024) | five open-domain QA sets |
| redundancy | up to 20x prompt compression with little loss (Jiang 2023) | | GSM8K, BBH, ShareGPT, arXiv |

## Instruction files for agents

| Sub-question | Upper bound | Lower bound | Measured how |
|---|---|---|---|
| task success | developer-written files: +2.4%, not significant (Gloaguen 2026) | generated files: -0.5% (SWE-bench Lite, 300 tasks) and -2% (138 instances), not significant (Gloaguen 2026) | gold tests, several agents and models |
| cost | median runtime -28.64%, output tokens -16.58% (Lulla 2026) | cost +20% and +23% on average with generated files, about +19% on average with developer files (Gloaguen 2026) | 124 pull requests; agent traces |
| [effect size](../learning-science/frame.md) bound | correctness change bounded to at most 10-15 points (Khatri 2026) | | 288 runs, equivalence tests |
| file structure | size, rule position, layout, contradictions: no detectable effect (McMillan 2026) | pooled OR 0.944 per generated function (about 5.6% lower odds), non-monotonic, found post hoc (McMillan 2026) | 1,650 sessions, one trivial target rule |
| many rules | best model 68% at 500 instructions (Jaroslawicz 2025) | earlier instructions favoured over later ones (Jaroslawicz 2025) | 20 models, keyword-inclusion rules |
| where files rot | | checker flags stale code references in 23.0% of 356 repositories, 36% of inspected flags false or ambiguous (Treude 2026) | documentation consistency checker |

## The model as writer

| Sub-question | Upper bound | Lower bound | Measured how |
|---|---|---|---|
| self-correction | RL-trained: self-correction gain +15.6 points on MATH, +9.1 on HumanEval over the base model (Kumar 2025) | prompted, no feedback: accuracy fell for every model on every benchmark tested (Huang 2024) | reasoning benchmarks without oracle labels |
| with test feedback | up to +12% with unit tests (Chen 2024a) | often modest, sometimes absent, once the cost of repair is counted (Olausson 2024) | MBPP and TransCoder (Chen); HumanEval and APPS (Olausson) |
| prevalence of LLM text | | at least 13.5% of 2024 PubMed abstracts LLM-processed (Kobak 2025); 6.5-16.9% of AI-conference peer-review text substantially LLM-modified (Liang 2024) | excess vocabulary; corpus-level estimation |
| per-document detection | | defeated by recursive paraphrasing (Sadasivan 2023); false positives on non-native writing (Liang 2023) | stress tests of detectors |

## Most adopted: the practice record

This record is kept apart from the research record above. Holders differ, and none of these numbers comes with a method.

| Sub-question | Most adopted practice | Measured how | Same holder as the research record? |
|---|---|---|---|
| file length | under 200 lines (Anthropic 2026b); 32 KiB combined (OpenAI 2026a) | none stated | no: research tests rule count, not lines (Jaroslawicz 2025) |
| where instructions go | long data first, query last (Anthropic 2026a); both ends (OpenAI 2025) | vendor tests, no data shown | agrees in direction with Liu 2024 |
| delimiters | XML tags (Anthropic 2026a); XML good, JSON poor (OpenAI 2025) | vendor tests, no data shown | partly: Sclar 2024 finds model-specific results |
| llms.txt | 28% of 137,210 domains using Ahrefs Web Analytics publish it, an upper bound (Ahrefs 2026) | server logs, 2026-05 | no: 97% of files had zero requests |
| docs the model lacks | an 8 KB index in AGENTS.md: 100% against 53% (Vercel 2026) | vendor evaluation, one domain | no: Gloaguen 2026 finds no net gain from files |
