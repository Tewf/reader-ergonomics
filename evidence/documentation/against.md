# Evidence against and open controversies

## Against page-form separation

- Diataxis is a framework, not a result: no controlled study compares readers on separated and mixed pages.
- Small repositories may be served better by one README holding several forms.

## Against checklists as quality

- The JOSS criteria test presence, not usefulness: a page can satisfy all six and still fail a reader.
- Prana 2019 describes what READMEs contain, not which contents help.

## Against strict comment rules

- Comment quality is a cluster of attributes (Rani 2023), not one measurable quantity; weights between them are a judgment.
- The register differs by language (imperative in PEP 257, descriptive in the Google guide), so no single rule holds.
- Generated documentation sites (rule 8 of Lee 2018) trade zero redundancy for tooling; rejecting them is defensible, and so is adopting them.
- Ousterhout's test relies on judgment about what the code "cannot" say, which two reviewers can read differently.

## Practice against the principles

- **One mode per document:** Diataxis critics argue the cost of strict separation.
  - Viktorin 2022: one participant asks for guidance on pages that mix forms, another warns a heavy method may be ignored or half followed.
  - Hacker News 2024: critics call strict use rigid and overkill for small projects, and say some explanation inside a guide is helpful.
  - The same critics report poor links between split pages and duplicated content that goes stale.
- **A README mixes modes by design:** GitHub, Make a README and standard-readme each place several modes in one file. Read as an index, it does not break the principle.
- **Define before use:** Google leaves well-known terms undefined. The exemption turns on the audience, so it is a reader-style choice, not a contradiction.
- **Diataxis tutorials:** minimal explanation can put a term before its definition unless the step links to it.
- **Adoption is self-reported:** the Diataxis site and Canonical 2021, written by its author, give no metrics, so adoption does not show the separation helps readers.
- **Length:** "too long is better than too short" (Make a README) opposes "shorter is always better" (Microsoft); neither is measured.
