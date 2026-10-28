# State of the art: who holds each record, and how it was measured

**Upper bound**: the best result achieved so far. **Lower bound**: the worst failure shown so far. The two are separate claims; improving one says nothing about the other.

## Reading long inputs

| Sub-question | Upper bound | Lower bound | Measured how |
|---|---|---|---|
| literal fact in long input | most of 17 models near-perfect on plain NIAH (Hsieh 2024a) | only half of models claiming 32K tokens stay satisfactory at 32K on harder tasks (Hsieh 2024a) | synthetic tasks, accuracy against length |
| fact without word overlap | GPT-4o: 99.3% short, 69.7% at 32K, among the best (Modarressi 2025) | 11 of 13 models below half their short-input score at 32K (Modarressi 2025) | NoLiMa needles, 13 models |
| fact in the middle | question before and after the data: key-value retrieval near-perfect, from a 45.6% worst case (Liu 2024) | GPT-3.5-Turbo with the answer in the middle: 53.8% (20 docs) and 50.5% (30 docs), below its 56.1% with no documents (Liu 2024) | multi-document QA, six models |
| fixing the middle | attention calibration: up to 15 points on RAG tasks (Hsieh 2024b) | | RAG benchmarks |
| length alone | focused inputs of about 300 tokens beat full ones of about 113k tokens, all model families (Hong 2025) | accuracy falls far below the technical limit with padding alone (Levy 2024) | 306 LongMemEval prompts; padded QA |

## Format and order

| Sub-question | Upper bound | Lower bound | Measured how |
|---|---|---|---|
| input format | GPT-4 robust to template changes (He 2024) | 76 accuracy points between formats, LLaMA-2-13B, few-shot (Sclar 2024); up to 40% for GPT-3.5-turbo on code translation (He 2024) | same content, meaning-preserving variants |
| answer format | most recent closed-weight models show little loss (Lee 2026) | stricter format constraints, larger reasoning loss (Tam 2024) | free-form against JSON, XML, YAML |
| premise order | premises in proof order: best accuracy (Chen 2024b) | permuting them: drops of over 30% (Chen 2024b) | deductive tasks and R-GSM |
| repetition | question read twice improves reasoning on 14 datasets (Xu 2024a) | | 112 experiments |

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
| cost | median runtime -28.64%, output tokens -16.58% (Lulla 2026) | cost +20% and +23% with generated files, up to +19% with developer files (Gloaguen 2026) | 124 pull requests; agent traces |
| effect size bound | correctness change bounded to at most 10-15 points (Khatri 2026) | | 288 runs, equivalence tests |
| file structure | size, rule position, layout, contradictions: no detectable effect (McMillan 2026) | odds of compliance fall about 5.6% per generated function, OR 0.944 (McMillan 2026) | 1,650 sessions, one trivial target rule |
| many rules | best model 68% at 500 instructions (Jaroslawicz 2025) | earlier instructions favoured over later ones (Jaroslawicz 2025) | 20 models, keyword-inclusion rules |
| where files rot | | stale code references in 23.0% of 356 repositories (Treude 2026) | documentation consistency checker |

## The model as writer

| Sub-question | Upper bound | Lower bound | Measured how |
|---|---|---|---|
| self-correction | RL-trained: +15.6% on MATH, +9.1% on HumanEval (Kumar 2025) | prompted, no feedback: no gain, sometimes worse (Huang 2024) | reasoning benchmarks without oracle labels |
| with test feedback | up to +12% with unit tests (Chen 2024a) | modest once the cost of repair is counted (Olausson 2024) | MBPP and TransCoder (Chen); HumanEval and APPS (Olausson) |
| prevalence of LLM text | | at least 13.5% of 2024 PubMed abstracts LLM-processed (Kobak 2025); 6.5-16.9% of AI peer reviews (Liang 2024) | excess vocabulary; corpus-level estimation |
| per-document detection | | defeated by recursive paraphrasing (Sadasivan 2023); false positives on non-native writing (Liang 2023) | stress tests of detectors |
