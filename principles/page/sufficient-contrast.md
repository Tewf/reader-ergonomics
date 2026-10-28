# Sufficient contrast

**Claim:** text has a contrast ratio of at least 4.5:1 against its background, dark text on a light ground by default, with a dark theme offered and never forced.

- **Grade:** measured for polarity; the 4.5:1 floor is a convention (a standard).
- **Evidence:** [typography and layout](../../evidence/typography-and-layout/review.md) (strand 4), [baseline](../../evidence/typography-and-layout/baseline.md).
- **Check:** none in `checks/`; any WCAG contrast checker computes it exactly.
- **Reader styles:** none override it.

## What it asks

- 4.5:1 for body text, 3:1 for large text and for the borders of controls (WCAG 2.2, 1.4.3 and 1.4.11).
- Colour never the only cue (WCAG 2.2, 1.4.1).
- Light background by default; a switch for readers who want dark.

## Why

Light-on-dark text cost acuity and proofreading accuracy at every age, more as type shrank (Piepenbrock 2013).

## Limits

By day the polarities do not differ measurably for some tasks, and light-on-dark may win at night (Dobres 2017). The
claim that dark mode improves reading is **not supported**.
