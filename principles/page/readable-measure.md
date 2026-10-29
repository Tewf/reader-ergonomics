# Readable measure

**Claim:** body text has a line length of about 45 to 75 characters, a size in the fluent range, and line spacing of at least 1.5.

- **Grade:** supported with caveat.
- **Evidence:** [typography and layout](../../evidence/typography-and-layout/review.md) (strands 1 to 3), [baseline](../../evidence/typography-and-layout/baseline.md).
- **Check:** `readable-measure` (exact, on the site's stylesheet): a measure of 45 to 75 characters, body text of 16 px
  or more, line height of 1.5 or more. `figure-width` (a warning): a figure drawn in characters stays within 60
  columns, so it fits where its text fits.
- **Reader styles:** none override it; letter spacing may be raised for readers with dyslexia.

## What it asks

- 45 to 75 characters per line for a single column, measured on the rendered page.
- Body size large enough to sit well inside the fluent range on the reader's device; 18 px is a safe default on screen.
- Line height of 1.5 or more, and text that survives the WCAG 1.4.12 spacing overrides.
- Left-aligned text, no long runs of italics.

## Why

Reading speed holds across a tenfold range of print sizes and falls below it (Legge 2011). Comprehension was higher at
18 pt than at smaller sizes in a sample of 104 (Rello 2016). Common serif and sans faces read equally fast on screen
(Bernard 2002).

## Limits

Speed and preference disagree on line length: about 100 characters is read fastest on screen, about 55 is understood
best and preferred (Dyson 2004). Fonts designed for dyslexia do not help (Wery 2017; Kuster 2018); extra letter spacing
does help dyslexic children read accurately (Zorzi 2012).

The upper bound is contested in practice: WCAG's AAA criterion allows 80 characters, 40 in CJK (W3C 2023a), and the
US Web Design System 90, with 66 as its target (USWDS 2026). Neither page cites a study: both are convention, and
the data above split speed from understanding (Dyson 2004).
