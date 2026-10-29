# Program tier

Checks that need only the Python standard library. They run on every push. A finding is an **error** when it is
certain, a **warning** when it comes from a heuristic, and a **judgment** question when no program can decide.

<!-- checks:start -->
| Check | What it verifies | Guarantee |
|---|---|---|
| [citations.py](citations.py) | Citations: every work cited in the text has one entry in the bibliography, and every entry is cited | Heuristic: a capitalised word before a year can be a false citation ("Colon Classification 1933"); config lists words that never start one. |
| [co_change.py](co_change.py) | Co-change: files that keep changing together should sit together | Coupling in history is evidence, not proof, so every finding is judgment. |
| [cross_file_terms.py](cross_file_terms.py) | Short reference distance across files: a term defined in one file is linked where another uses it | Heuristic. |
| [defined_before_use.py](defined_before_use.py) | Define before use: a term is not used in a file before the line that defines it | Heuristic: bold is also used for emphasis, and a term can be defined in another file. |
| [duplication.py](duplication.py) | Duplication: the same run of words held in two files means one fact kept in two places | Exact for the copy; whether the copy is a fact or a quotation is judgment. |
| [figure_captions.py](figure_captions.py) | Figure next to its text: every image says what it shows, and every drawn figure has words beside it | Exact for alt text; heuristic for the words beside a figure. |
| [figures_present.py](figures_present.py) | Figures present: a long document with no figure, table or diagram is asked whether a relation went undrawn | The count is exact; whether a figure is needed is judgment. |
| [links.py](links.py) | Links: every relative link in a markdown file resolves to a file or folder that exists | Exact for file links. |
| [logical_lines.py](logical_lines.py) | File size: a trigger on logical lines and a ceiling on physical lines, each asking a question | The sentence count is a heuristic (abbreviations split badly). |
| [long_sentences.py](long_sentences.py) | Long sentences: a sentence past `max_words` words is the cheap sign of packed information | Heuristic. |
| [name_matches_title.py](name_matches_title.py) | Names predict content: the words of a file's name appear in its title or opening | Heuristic. |
| [outline_depth.py](outline_depth.py) | Outline depth: a document's headings stay within three levels | The count is exact; the limit of three is a convention, so a deeper heading warns. |
| [overview_first.py](overview_first.py) | Overview first: a long document opens with what it is and how it is organised, not with a heading | Heuristic (the opening may be there and still not be an overview). |
| [paragraph_length.py](paragraph_length.py) | Signal the structure: no wall of prose, and no long run without a heading | Heuristic. |
| [portable_paths.py](portable_paths.py) | Portable paths: every path must check out on filesystems other than the one it was made on | Exact. |
| [principle_coverage.py](principle_coverage.py) | Principle coverage: every principle names at least one check that exists, so CI tests every rule | Exact. |
| [provisional_tags.py](provisional_tags.py) | PROVISIONAL tags: a value marked as a guess is measured, or kept knowingly, before it ages | Exact for the date. |
| [readable_measure.py](readable_measure.py) | Readable measure: the site's stylesheet sets body text inside the measured ranges | Exact for the declared values; the rendered line still depends on the face. |
| [references.py](references.py) | References: every DOI, arXiv id, GitHub repository and web link cited resolves | Exact offline. Online depends on remote servers (a timeout is reported, never hidden). |
| [shape_conformance.py](shape_conformance.py) | Shape conformance: a document declared to be of a shape holds the parts that shape requires | Exact. |
| [standard_card.py](standard_card.py) | The repository's generated indexes: the principle table in standard.md, llms.txt, and the check tables | Exact. |
| [sufficient_contrast.py](sufficient_contrast.py) | Sufficient contrast: every text colour reaches a WCAG ratio of 4.5:1 on the background it sits on | Exact for colours declared in the same rule; heuristic for inherited backgrounds. A colour is read as hex, or as `white` or `black`; any other form is skipped. The rendered page is not measured. |
| [tree_shape.py](tree_shape.py) | Tree shape: folders stay browsable, and dependencies between folders never form a cycle | Exact for breadth, depth and static imports; dynamic imports are invisible. |
| [type_buckets.py](type_buckets.py) | Type buckets: no folder is named for a kind of file instead of what its files serve | Exact. |
<!-- checks:end -->
