# Frame: the problem and its names

This file states the problem in one sentence, defines the terms used in this folder, names what the field calls each part, and sets the scope.

## The problem in one sentence

Which structure of text and files lets a **large language model** (LLM, a neural network that reads and writes text as tokens) answer and act correctly from them at the least cost? And how is a model that writes into the repository held to the repository's rules?

## Terms used in every file of this folder

| Term | Definition |
|---|---|
| **token** | the unit a model reads and is billed for, roughly a word piece |
| **context** | all tokens a model receives in one call: instructions, documents, history |
| **causal attention** | each token can draw only on tokens before it; the design of decoder-only models |
| **coding agent** | an LLM that runs tools (shell, editor, tests) inside a repository |
| **instruction file** | a file in a repository written for agents to read at the start of a session |
| **retrieval-augmented generation** (RAG) | retrieved passages are pasted into the context before the model answers |

## What the field calls each part

| Our words | The field's names | Acronym | Entry point |
|---|---|---|---|
| where a fact sits in the input | positional bias; lost in the middle; primacy and recency bias; serial-position effect | LiM | Liu 2024 |
| how much input a model really uses | effective context length; long-context utilization; context rot | NIAH (needle in a haystack) | Hsieh 2024a; Hong 2025 |
| the same content, laid out differently | prompt formatting sensitivity; spurious features; prompt template; table serialization | FormatSpread | Sclar 2024 |
| the format asked of the answer | structured generation; format restrictions; format tax | | Tam 2024; Lee 2026 |
| text that does not serve the task | distractibility; irrelevant context; noise robustness; context bloat | GSM-IC | Shi 2023 |
| two sources that disagree | knowledge conflict (inter-context, context-memory) | | Xu 2024b |
| choosing what enters the context | context engineering; prompt compression | | Mei 2025; Jiang 2023 |
| files that tell agents how to work | repository context files; agent configuration files; AGENTS.md; cursor rules; llms.txt | | Gloaguen 2026 |
| many rules at once | instruction following; verifiable instructions; instruction density | IFEval; IFScale | Zhou 2023a; Jaroslawicz 2025 |
| telling model text from human text | machine-generated text detection; excess vocabulary; stylometry | | Wu 2025; Kobak 2025 |
| a model checking its own work | intrinsic self-correction; self-refinement; self-repair; self-preference bias | | Huang 2024; Kamoi 2024 |

## Scope

- In: how the input is structured, instruction files for agents, the model as a writer bound by rules.
- Out: training methods, except where a trained model changes a conclusion drawn from prompted ones.
- Out: retrieval system design, except where it shows what text in the context does to the answer.
