# Baseline: what this repository's rules are compared against

## The conditions

| Name | Content | Role |
|---|---|---|
| **B0, plain prose** | the same facts as one unstructured text: no headings, lists or tables, arbitrary order, each fact once | the baseline |
| **B1, no instruction file** | the repository without its agent file | the null of Gloaguen 2026, for agent tasks |
| **B2, llms.txt index** | an llms.txt file (Howard 2024) linking the same documents | the existing convention |
| **T, treatment** | the same facts written to this repository's rules | what is tested |

B0 holds content fixed, so any difference measures structure alone.

## Reading: accuracy on a fixed question set

- A fixed set of closed questions about the documents, each answerable from exactly one fact.
- Answers graded by program: exact match or a normalised string, never a model judge.
- Each fact placed at the start, middle and end across variants, following Liu 2024.
- Half the questions paraphrase their fact with no shared content words, following Modarressi 2025, since overlap inflates scores.
- Each condition written in several meaning-preserving format variants; report the range of accuracy, not one number (Sclar 2024).
- At least three model families and two sizes, because format effects correlate weakly between models.
- Tokens per correct answer reported beside accuracy.

## Acting: agent task success

- Real tasks from the repository's history, each with gold tests, run under T and B1.
- Report success, steps and cost per task, following Gloaguen 2026.
- Report equivalence bounds for null results, following Khatri 2026.

## Writing: program check against self-review

- A fixed set of drafts, hand-labelled for violations of the rules a program can check.
- Three reviewers on the same drafts: the checking program; the model that wrote the draft; a different model.
- Report precision and recall of each against the hand labels.
- Track compliance by position in the session, since it decays as a session goes on (McMillan 2026).
- Expected from the literature: the program wins on checkable rules, and self-review favours its own text (Huang 2024; Panickssery 2024).

## Decision rule

- A rule stays as a model-facing rule only if T beats B0 by more than the format range, on accuracy or on tokens per correct answer.
- A rule that does not is kept only as a human-reader rule, or cut.
- Comparisons are paired on the same questions and tasks; the analysis plan is fixed before the runs.
