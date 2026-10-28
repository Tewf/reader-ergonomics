# Position

Terms are defined in `review.md`; works are listed in the [bibliography](../bibliography.md).

## Known

| Finding | Grade |
|---|---|
| Per-word reading time is linear in surprisal | measured |
| So, for reading time, even spreading of information buys nothing at fixed length and total information | measured (argument in `state-of-the-art.md` §2) |
| Non-uniform surprisal lowers judged acceptability | supported with caveat |
| Languages keep dependencies short, between random and optimal | measured |
| Long dependencies cost reading time in controlled sentences | measured |
| In a corpus of 7 languages, written center-embedding never exceeded degree 3; in speech it was practically absent | measured (corpus) |
| Reading time tracks propositions more than words | supported with caveat |
| A missing antecedent costs a bridging inference | measured |
| Ideas high in the text hierarchy are remembered better | measured |
| Readers who use headings summarize best | measured |
| The best cohesion level depends on reader knowledge and skill | measured |
| Classic readability formulas are a weak baseline for adults | measured |

## Not known

Each item below is "not seen in this review", which is a claim about the search, not about the world.

- A controlled test of definition-to-use distance in reference notes.
- A test of heading or list nesting depth on retrieval from notes.
- A test of the surprisal linking function on reread or searched text.
- The complexity of ordering concepts when weights are in-degree minus out-degree.
- A test that RST tree depth predicts reading cost.
- Whether lab effects on single reading hold for texts that are skimmed and searched.

## What this repository adds

- One map from five scales to findings, grades and checks, so a rule can be traced to its evidence.
- The Jensen argument written out, with the verdict split by measure: reading time or acceptability.
- The note-ordering problem restated as scheduling with precedence, with what is and is not known of its complexity.
- Checks sorted by what they compute exactly without a language model (`baseline.md`).
- A reader condition on every density rule, because cohesion and support effects reverse with expertise.

## Practice and the evidence

- Practice runs ahead: sentence targets of 15, 20 and 25 words (EC 2011; Style Manual AU 2026) come with no test in the sources read.
- Practice ignores evidence: US state law still fixes a Flesch floor (NAIC 2025) after Redish 2000 and Crossley et al. 2017.
- Practice agrees: the legalese advice matches Martinez et al. 2022 on center-embedding.
- Critics and the standard meet: Redish 2000 and Schriver 2017 name usability testing as the benchmark.
- Consequence for checks: a readability or length number is a flag for a reader to judge, never an error.
- Not seen in this review: any government test of its own word cap.

## Correction to the brief

- The brief said Futrell et al. 2015 use MinLA as a baseline.
- They use the minimum over projective orders; unconstrained MinLA on trees is the baseline of Ferrer-i-Cancho et al. 2022.

## Language models as readers (lower priority)

- Long-context models use information best at the start or end of the input (Liu et al. 2023).
- That is a locality effect at document scale; whether human findings transfer to such readers is untested here.
