# Baseline

Rules are compared against the **WCAG 2.2 success criteria** (pass or fail) and the **measured ranges** below (inside or outside).

## WCAG 2.2 success criteria

| Criterion | Requirement |
|---|---|
| 1.4.3 Contrast (Minimum), AA | text 4.5:1; large text 3:1 |
| 1.4.6 Contrast (Enhanced), AAA | text 7:1 |
| 1.4.11 Non-text Contrast, AA | UI parts and graphics 3:1 |
| 1.4.12 Text Spacing, AA | no loss when line height is 1.5, paragraph spacing 2 times, letter spacing 0.12 em, word spacing 0.16 em |
| 1.4.10 Reflow, AA | no two-way scrolling at 320 CSS px |
| 1.4.4 Resize Text, AA | text scales to 200% without loss |
| 2.5.8 Target Size (Minimum), AA | pointer targets at least 24 by 24 CSS px |

## Measured ranges

| Variable | Baseline range | Source |
|---|---|---|
| Measure | 45-75 cpl; 55 for comprehension, up to 100 for speed | Dyson 2004, Bringhurst |
| Type size | 16-19 px body; x-height inside 0.2 to 2 degrees; 18 pt better in one study | Legge 2011, Rello 2016, BDA |
| Line height (leading) | 1.5 at least, no effect among mid values | WCAG 1.4.12, Rello 2016 |
| Face | common sans or serif; no dyslexia font needed | Bernard 2002, Kuster 2018 |
| Alignment | left, ragged right | BDA |
| Polarity | dark text on light ground by default; offer a switch | Piepenbrock 2013, NN/g |

## How to compare

- Compute contrast from the rendered colours, in each colour scheme.
- Measure the rendered line in characters and pixels at the narrowest and widest supported viewport.
- Test with the WCAG 1.4.12 overrides applied.
- Test at 320 px width and 200% zoom.
- Record each rule as inside or outside its range, and as pass or fail.

## Practice baseline

What people compare against in practice, apart from the measured ranges:

| Variable | Practice baseline | Source |
|---|---|---|
| Measure | 45 to 75 characters; upper bounds 80 (AAA) and 90 | GOVUK 2024, W3C 2023a, USWDS 2026 |
| Body size | at least 16px | USWDS 2026 |
| Line height | at least 1.5 | USWDS 2026 |
| Contrast check | rendered-page scan at 4.5:1 and 3:1 | axe-core, pa11y, Lighthouse |
