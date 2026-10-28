# Reader styles

The [standard](../standard.md) is the best current guess for a reader nobody knows. Once the
reader is known, the best choice moves: what helps a novice slows an expert down (**expertise
reversal**: an aid that helps beginners hurts readers who no longer need it; Kalyuga et al.
2003), and a model reads differently from a person. A reader style says what moves, for
whom, and on what evidence.

## Contents

| File | The reader |
|---|---|
| [template.md](template.md) | blank style to copy for a known reader |
| [novice.md](novice.md) | new to the domain; needs every term, worked steps, explicit links between ideas |
| [expert.md](expert.md) | knows the domain; reads for the new part, by search, often out of order |
| [visual-relational.md](visual-relational.md) | prefers relations as graphs, sets as regions, quantities as geometry |
| [llm-reader.md](llm-reader.md) | a language model reading the text as context |

## How a style overrides the standard

- A style only lists **overrides**: principles it strengthens, relaxes or replaces. Everything else in the standard holds.
- Each override names its principle, says what changes, and cites why.
- A style may also change a check's thresholds; it does so in the repository's `checks/config.toml`, never by editing the check.
- A style for one named person stays with that person. The ones here are archetypes.

## Example

A repository written for experts sets `trigger = 120` in `checks/config.toml` and keeps worked examples to the
first use of each method, as [expert.md](expert.md) says. Run `python3 checks/run.py .` and the logical-lines
questions now start at 120 statements.

## What a style cannot do

The meshing hypothesis, **matching the presentation to a preferred learning style**, does not improve learning in the
experiments that tested it properly (Pashler et al. 2008).

So a style states preferences and known expertise, and promises nothing from matching alone. See
[evidence/learning-science](../evidence/learning-science/).
