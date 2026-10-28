# Review: surveys, seminal work, forward citations

Terms are defined in `frame.md`; numbers live in `state-of-the-art.md`.

## How the search ran

| Strand | Academic name | Acronym | Author seed |
|---|---|---|---|
| position | "lost in the middle", positional bias | LiM, NIAH | Liu; Hsieh |
| format | prompt formatting sensitivity, table serialization | FormatSpread | Sclar |
| distraction | irrelevant context, distractibility | GSM-IC | Shi |
| instruction files | repository context files, cursor rules | AGENTS.md | Gloaguen; Treude |
| writer | self-correction, LLM-generated text detection | IFEval | Huang; Kamoi |

Each strand: arXiv search by title and abstract phrase, then by author, then a web search for non-arXiv sources.

## Surveys, read first

- Mei 2025 frames the context as an information payload to optimise, over about 1,400 papers.
- Liu 2025 surveys long-context models, including how they are evaluated and analysed.
- Kamoi 2024 audits self-correction research and gives a checklist for fair experiments.
- Wu 2025 surveys the detection of LLM-generated text and its open problems.
- Xu 2024b classifies knowledge conflicts: between context and memory, inside the context, inside memory.

## Strand 1: position in the context

- Seminal: Liu 2024 moved the answer document through 10, 20 and 30 documents, and keys through key-value lists, for six models.
- The result was a U-shape: best at the start or end, worst in the middle.
- Placing the question both before and after the data (**query-aware contextualization**) fixed key-value retrieval but barely moved document QA.
- Hsieh 2024b traced the U-shape to an attention bias toward the start and end, and calibrated it away.
- Hsieh 2024a (RULER) showed that plain NIAH is nearly solved, then added multi-hop and aggregation tasks that are not.
- Modarressi 2025 (NoLiMa) removed word overlap between question and needle, and long-context accuracy fell sharply.
- Veseli 2025 measured length relative to each model's window: LiM fades near the limit, and a recency bias remains.
- Hong 2025 tested 18 models: accuracy fell as input grew, and needle position did not matter in their task.
- Levy 2024 padded the same reasoning task to longer inputs and saw accuracy fall far below the advertised limit.

## Strand 2: format sensitivity

- Seminal: Sclar 2024 varied separators, casing and spacing that keep meaning, and measured large accuracy swings.
- Format rankings in Sclar 2024 correlated only weakly between models, so one model's best format is not another's.
- He 2024 wrote the same prompts as plain text, Markdown, JSON and YAML; the larger model was more robust.
- Sui 2024 found table understanding depends on table format, content order and partition marks.
- Ahsan 2026 (TABVERSE, preprint) held table content fixed across HTML, Markdown, LaTeX and images.
- Tam 2024 showed that asking for JSON or XML output lowers reasoning.
- Lee 2026 located that loss in the format instruction itself, and recovered it by reasoning first and formatting second.

## Strand 3: distraction, length, order, redundancy

- Seminal: Shi 2023 (GSM-IC) added one irrelevant sentence to grade-school maths problems.
- Yoran 2024 characterised when retrieval hurts and trained models to ignore irrelevant passages.
- Cuconasu 2024 found related-but-useless passages hurt more than random ones.
- Chen 2024b permuted premises away from the order a proof uses them.
- Xu 2024a (Re2) had the model read the question twice, citing causal attention as the reason it helps.
- Leviathan 2025 (preprint) repeated the whole prompt for non-reasoning models of four families.
- Jiang 2023 (LLMLingua) compressed prompts heavily with little loss, so much prompt text is redundant to the model.

## Strand 4: instruction files for agents

- Howard 2024 proposed llms.txt: one required H1, a summary blockquote, link lists, and an "Optional" section an agent may skip.
- The AGENTS.md site (Agentic AI Foundation 2026) defines a plain Markdown file for agents; the nearest file in the tree wins, and the chat prompt overrides it.
- Neither site cites an evaluation of accuracy.
- Jiang 2025 built a taxonomy of cursor rules from 401 repositories: conventions, guidelines, project information, directives, examples.
- Zarzycki 2026 censused 22,854 repositories and annotated 341,852 statements in their instruction files.
- dos Santos 2026 catalogued six smells in instruction files, including bloat and conflicting instructions.
- Treude 2026 named stale instruction files **context rot** and detected them with an existing documentation checker.
- Gloaguen 2026 ran agents with and without instruction files on SWE-bench Lite and on a new benchmark of repositories that ship one.
- Lulla 2026 ran agents on 124 pull requests with and without AGENTS.md, measuring time and tokens.
- Khatri 2026 ablated instruction files across two agents with equivalence tests.
- McMillan 2026 varied file size, rule position, file layout and contradictions in a factorial design.
- Zhou 2023a (IFEval) built instructions a program can verify, such as word counts and required keywords.
- Jaroslawicz 2025 (IFScale) raised the number of simultaneous instructions to 500.
- Zhou 2023b (DocPrompting) retrieved library documentation before code generation.

## Strand 5: the LLM as writer

- Kobak 2025 tracked excess style words across 15 million biomedical abstracts.
- Liang 2024 estimated the share of LLM-modified text in AI conference peer reviews.
- Reinhart 2025 compared human and LLM text on Biber's grammatical and rhetorical features.
- Sadasivan 2023 broke detectors, watermarks included, with recursive paraphrasing.
- Liang 2023 showed detectors flag non-native English writing as machine-made.
- Huang 2024 removed oracle stopping labels and found self-correction of reasoning fails without external feedback.
- Gou 2024 (CRITIC) and Chen 2024a (self-debugging) gave models tool and test feedback instead.
- Olausson 2024 counted the cost of self-repair and found feedback quality is the bottleneck.
- Panickssery 2024 showed evaluators recognise and favour their own outputs.
- Kumar 2025 (SCoRe) trained self-correction with reinforcement learning.

## Strand 6: Practice

Each page below is its owner's claim about its own product. None states a method for its numbers, except where noted.

- Anthropic 2026a (company guide): long documents at the top, the query at the end; it reports gains "up to 30 percent" with no method.
- Anthropic 2026b (product docs): target under 200 lines per CLAUDE.md; longer files reduce adherence; contradictory rules may be picked arbitrarily.
- Anthropic 2026b also says memory files are context, not enforcement, and points to a hook to block an action.
- OpenAI 2025 (company cookbook): instructions at both start and end beat one end only; XML delimiters did well and JSON did particularly poorly.
- OpenAI 2026a (product docs): AGENTS.md files are layered from root to current directory, with a combined cap of 32 KiB by default.
- AGENTS.md 2026 (de facto specification): the page claims use by over 60k open-source projects and lists logos of 23 tools (counted here); stewarded under the Linux Foundation.
- Howard 2024 (llms.txt): the proposal; its page says only that thousands of sites publish one.
- Ahrefs 2026 reports llms.txt on 28% of 137,210 domains using Ahrefs Web Analytics, an upper bound.
- Ahrefs 2026 (SEO company, stated method, server logs, 2026-05): 97% of llms.txt files received zero requests; AI retrieval bots made 1.1%. The page's heading says of total requests, but its body says of AI bot requests.
- Ahrefs 2026 states that a fetch is not a read, so these shares are ceilings on use.
- Vercel 2026 (vendor evaluation, one domain): baseline 53%; a skill by default 53%; a skill with explicit instructions 79%; an 8 KB docs index in AGENTS.md 100%.
- In Vercel 2026 the skill was never invoked in 56% of cases; the page gives no model name and no task count.
- Chatlatanagulchai 2026 (preprint) describes content only: in 2,303 files from 1,925 repositories, test procedures appear in 75.9%, security in 14.8%.
