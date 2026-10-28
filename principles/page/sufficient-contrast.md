# Sufficient contrast

**Claim:** text has a contrast ratio of at least 4.5:1 against its background, dark text on a light ground by default, with a dark theme offered and never forced.

- **Grade:** measured for polarity; the 4.5:1 floor is a convention (a standard).
- **Evidence:** [typography and layout](../../evidence/typography-and-layout/review.md) (strand 4), [baseline](../../evidence/typography-and-layout/baseline.md), [terms](../../evidence/typography-and-layout/frame.md).
- **Check:** `sufficient-contrast` (exact, on the site's stylesheet): every text colour declared with its background reaches 4.5:1.
- **Reader styles:** none override it.

## What it asks

- 4.5:1 for body text, 3:1 for large text and for the borders of controls (WCAG 2.2, 1.4.3 and 1.4.11).
- Colour never the only cue (WCAG 2.2, 1.4.1).
- Light background by default; a switch for readers who want dark.

## Why

Light-on-dark text cost acuity and proofreading accuracy at every age (Piepenbrock 2013), and more as type
shrank (Piepenbrock 2014).

## Limits

By day the polarities did not differ for single words read at a glance, and at night white text on black was
clearly less legible (Dobres 2017, measured, 34 adults). The
claim that dark mode improves reading is **not supported**.

The 4.5:1 floor is a convention under revision. APCA makes the threshold depend on the size of the text, and on
its weight in principle (APCA 2026); WCAG 3 has not chosen a method (W3C 2026). It is also widely broken: on 83.9% of the million home
pages WebAIM scanned, an automated AA check found low-contrast text (WebAIM 2026, measured, descriptive). APCA is its
author's proposal; its page cites no independent test.
