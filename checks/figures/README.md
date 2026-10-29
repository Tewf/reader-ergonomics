# Figure checks

The program-tier checks that read figures: whether a page has one, how it is drawn and described, and whether its
SVG still matches its Graphviz source. They change together, with the family's figure rule, and share one reading of
SVG files.

**Shape:** [folder and its README](../../shapes/readme-and-folder.md).

## Contents

<!-- checks:start -->
| File | Role | Guarantee |
|---|---|---|
| [_svg.py](_svg.py) | Shared reading of SVG figures for the figure checks: which files, and the colours they declare |  |
| [figure_alt.py](figure_alt.py) | Figure alt: an image's alt text says what it shows, never its file name or a word for its kind | Exact. |
| [figure_captions.py](figure_captions.py) | Figure next to its text: every image says what it shows, and every drawn figure has words beside it | Exact for alt text; heuristic for the words beside a figure. |
| [figure_contrast.py](figure_contrast.py) | Figure contrast: the lines of an SVG figure have at least `min_ratio` contrast against what lies next to them | Exact for the colours a file declares; a colour set by a class this module cannot resolve is not checked. |
| [figure_source.py](figure_source.py) | Figure source: an SVG drawn from a `.dot` file was rendered from the source that sits beside it now | Exact. |
| [figure_source_inline.py](figure_source_inline.py) | Figure source inline: a drawn figure carries its Graphviz source under it, folded, and the copy equals its file | Exact for the comparison; whether a figure needs its source shown is the rule's, not the reader's. |
| [figure_width.py](figure_width.py) | Figure width: a figure drawn in characters stays within `max_columns`, so it fits the column its text fits | Exact for the width; the limit is a convention, PROVISIONAL in config, set at the narrow end of the readable measure (45 to 75 characters), so a warning. |
| [figures_present.py](figures_present.py) | Figures present: a long document with no figure, table or diagram is asked whether a relation went undrawn | The count is exact; whether a figure is needed is judgment. |
| [render_figure.py](render_figure.py) | Render a Graphviz source to the SVG beside it, stamped with the hash of the source, and refresh its folded copies |  |
| [typed_figure.py](typed_figure.py) | Typed figure: a figure in a page people read is drawn from a source file, not typed in characters | Exact for what counts as a typed figure; the rule is a convention, so a warning. |
<!-- checks:end -->

## Example

Render a figure from its source, with the stamp `figure-source` reads:

```sh
python3 checks/figures/render_figure.py standard-how-to-use.dot
```
```console
standard-how-to-use.svg
```

## See also

The other tiers, in [checks](../README.md); the figure rule, in [draw relations](../../principles/page/draw-relations.md).
