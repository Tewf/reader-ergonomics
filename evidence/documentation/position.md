# Position

What the evidence settles about documentation, what it leaves open, and where practice stands.

## Known

- Comment quality has a survey and three attributes (Rani 2023).
- Code and comments drift apart (Wen 2019).
- READMEs have a content taxonomy and known gaps (Prana 2019).
- Page-form and acceptance-bar standards exist and are used (Diataxis, JOSS, Lee 2018).

## Not known

- Whether the standards improve reader outcomes.
- How the two levels fit together: standards at one level rarely cite the other.
- The effect of a single page mixing forms.

## What this repository adds

- It joins both levels into two checklists (baseline.md), each traced to a named source.
- It reads the repository-level standards as a taxonomy: start page as tutorial, usage sections as how-to, option and index pages as reference, method and write-up pages as explanation.
- It treats a deliberate rejection of a rule, such as generated documentation sites, as a recorded decision, not a gap.
- Gaps are expected to cluster in two places: community guidelines and file-header role comments.

## Where practice meets the evidence

Practice runs ahead of the evidence:
- Procida reports that Diataxis spread through hundreds of projects (below the quality bar: an example, not evidence), with no controlled study and no list of projects.
- No style guide read cites a study for its length or depth limit.

Practice agrees across guides:
- Sentence-case headings (Google, Microsoft, GitLab); descriptive headings, one purpose per topic, a short lead before detail (not checked per guide).
- These support the principles on names, structure, overview and one mode. Adoption adds weight of use, never a grade.

Guides disagree where evidence is silent:

| Point | Google | Microsoft | Red Hat | GitLab | Make a README |
|---|---|---|---|---|---|
| Procedure title | base-form verb | not read | imperative (supplementary), gerund (modular) | not read | not applicable |
| Length | trim to a minimum | "shorter is always better" | short description 50 to 300 characters | not read | "too long is better than too short" |
| Heading depth | one h1, no skipped level | not read | none in procedures | to H5 | not applicable |

- The standard's three levels of headings is stricter than all of them; none cites a reason for its own limit.
- Choosing one title form and keeping it satisfies names predict content under every guide.
- The standard's size trigger sits between Microsoft and Make a README, since neither side is measured.

A README is an index of modes by convention. GitHub, Make a README and standard-readme all put what, install, usage
and contributing in one file. Each section serves one mode.

Google exempts well-known terms such as API from spelling out. The principle says every term, so the exemption is stated as depending on the reader.

Diataxis tutorial guidance keeps explanation out of the steps and links to it. This agrees with define before use only when the link points at the definition.
