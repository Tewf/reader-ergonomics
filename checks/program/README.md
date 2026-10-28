# Program tier

Checks that need only the Python standard library. They run on every push. A finding is an **error** when it is
certain, a **warning** when it comes from a heuristic, and a **judgment** question when no program can decide.

<!-- checks:start -->
| Check | What it verifies |
|---|---|
| [citations.py](citations.py) | Citations: every work cited in the text has one entry in the bibliography, and every entry is cited |
| [co_change.py](co_change.py) | Co-change: files that keep changing together should sit together |
| [cross_file_terms.py](cross_file_terms.py) | Short reference distance across files: a term defined in one file is linked where another uses it |
| [defined_before_use.py](defined_before_use.py) | Define before use: a term is not used in a file before the line that defines it |
| [duplication.py](duplication.py) | Duplication: the same run of words held in two files means one fact kept in two places |
| [figure_captions.py](figure_captions.py) | Figure next to its text: every image says what it shows, and every drawn figure has words beside it |
| [figures_present.py](figures_present.py) | Figures present: a long document with no figure, table or diagram is asked whether a relation went undrawn |
| [links.py](links.py) | Links: every relative link in a markdown file resolves to a file or folder that exists |
| [logical_lines.py](logical_lines.py) | File size: a trigger on logical lines and a ceiling on physical lines, each asking a question |
| [long_sentences.py](long_sentences.py) | Long sentences: a sentence past `max_words` words is the cheap sign of packed information |
| [name_matches_title.py](name_matches_title.py) | Names predict content: the words of a file's name appear in its title or opening |
| [outline_depth.py](outline_depth.py) | Outline depth: a document's headings stay within three levels |
| [overview_first.py](overview_first.py) | Overview first: a long document opens with what it is and how it is organised, not with a heading |
| [paragraph_length.py](paragraph_length.py) | Signal the structure: no wall of prose, and no long run without a heading |
| [portable_paths.py](portable_paths.py) | Portable paths: every path must check out on filesystems other than the one it was made on |
| [principle_coverage.py](principle_coverage.py) | Principle coverage: every principle names at least one check that exists, so CI tests every rule |
| [provisional_tags.py](provisional_tags.py) | PROVISIONAL tags: a value marked as a guess is measured, or kept knowingly, before it ages |
| [readable_measure.py](readable_measure.py) | Readable measure: the site's stylesheet sets body text inside the measured ranges |
| [references.py](references.py) | References: every DOI, arXiv id, GitHub repository and web link cited resolves |
| [shape_conformance.py](shape_conformance.py) | Shape conformance: a document declared to be of a shape holds the parts that shape requires |
| [standard_card.py](standard_card.py) | The repository's generated indexes: the principle table in standard.md, llms.txt, and the check tables |
| [sufficient_contrast.py](sufficient_contrast.py) | Sufficient contrast: text and background colours declared together reach a WCAG ratio of 4.5:1 |
| [tree_shape.py](tree_shape.py) | Tree shape: folders stay browsable, and dependencies between folders never form a cycle |
| [type_buckets.py](type_buckets.py) | Type buckets: no folder is named for a kind of file instead of what its files serve |
<!-- checks:end -->
