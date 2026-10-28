# Even information density

**Claim:** a text says no more than the reader needs, and spreads what it says: no sentence packs several new ideas, and a dense term arrives after its context.

- **Grade:** supported with caveat for judged quality; **not supported** as a way to read faster.
- **Evidence:** [psycholinguistics](../../evidence/psycholinguistics/state-of-the-art.md) (sections 1 and 2), [against](../../evidence/psycholinguistics/against.md).
- **Check:** `long-sentences` (heuristic): a sentence past 35 words; word probabilities from a language model would measure density itself, and are not in `checks/`.
- **Reader styles:** none override it.

## What it asks

- Cut first: what the reader does not need costs reading time whatever its shape.
- Then spread: one new idea per sentence, the context of a surprising word before the word.

## Why

**Surprisal** is how unexpected a word is, $s = -\log_2 P(\text{word} \mid \text{context})$. A text of $n$ words with
surprisals $s_i$, summing to $S$, costs the reader $C = \sum_i f(s_i)$.

- If $f$ is convex, Jensen's inequality makes the uniform spread the cheapest.
- If $f$ is linear, $C = an + bS$, and only $n$ and $S$ matter.
- Reading time is linear in surprisal, across 6 datasets and 11 languages (Shain et al. 2024; Wilcox et al. 2023).
- Uneven surprisal lowers how acceptable a sentence is judged (Meister et al. 2021, who also find reading times
  consistent with a weakly super-linear effect).

So evenness buys judged quality; cutting buys time.

## Limits

The shape of $f$ is still contested, by measure and by the language model used to estimate surprisal (Brothers &
Kuperberg 2021; Xu et al. 2023). Speakers spreading information (Jaeger 2010) is evidence about writers, not readers.
