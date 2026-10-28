# Size is a prompt

**Claim:** past a length, a file is asked to state its role; size alone never decides a split.

- **Grade:** convention, untested. The belief that smaller files have fewer defects is **not supported**.
- **Evidence:** [against](../../evidence/file-structure/against.md) (file length).
- **Check:** `logical-lines`: past 80 statements, a judgment question; past 500 lines, a review.
- **Reader styles:** [novice](../../reader-styles/novice.md) lowers the trigger; [expert](../../reader-styles/expert.md) raises it.

## What it asks

- Count statements, not layout: a sentence, a list item, a table row or a code block each count one; headings, blank lines and wrapping count zero. Re-cutting a paragraph into bullets changes nothing.
- Past about 80 statements, state the file's role in one sentence ([one role per file](one-role-per-file.md)). If it holds, the file stays.
- Past about 500 lines, review the file: split it only into pieces that change separately and that each stay whole.

## Why

The trigger costs one sentence and catches files that grew a second role. The thresholds are conventions, tagged
PROVISIONAL in `checks/config.toml`.

## Limits

No size threshold has held up for defects: defect-proneness grows more slowly than size, so smaller modules carry
proportionally more defects (Koru 2008; Koru 2010a); the shape of the curve is contested (Syer 2015). Splitting keeps
total size, and smaller modules are proportionally more coupled (Koru 2010b). Over-split code becomes entangled: one
piece cannot be read without the other (Ousterhout 2025). All these studies measure code, not prose.
