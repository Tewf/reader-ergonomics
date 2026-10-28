# State of the art

Upper and lower bounds are kept apart, as in every topic ([method](../README.md)).

## Upper bounds, by sub-question

| Sub-question | Best evidence | Method | Measure |
|---|---|---|---|
| Line length | Dyson 2004 | review of on-screen studies | 100 cpl fastest, 55 cpl best comprehension |
| Readable size | Legge 2011 | psychophysics | fluent range x-height 0.2 to 2 degrees |
| Size and comprehension | Rello 2016 | one study, n = 104 | 18 pt and 26 pt better |
| Letter spacing, dyslexia | Zorzi 2012 | randomised, n = 74 and 20 children | errors halved, speed +0.3 syllables a second (11% to 20%) |
| Light vs dark text | Piepenbrock 2013 | controlled experiments | light-on-dark loses in acuity |
| Scannable layout | Nielsen 1997 | usability study | +47% scannable, +124% combined |
| Words with their figure | Ginns 2006 | meta-analysis | d about 0.72 to 0.85 (secondary) |
| Visual cues | Richter 2016 | meta-analysis | r = 0.17 |
| Decoration | Sundararajan 2020 | meta-analysis, 58 studies (68 effects) | g = -0.33 (secondary) |
| Text contrast | WCAG 1.4.3 | standard | 4.5:1 |

## Lower bounds (limits)

- Serif vs sans on screen: no difference in speed (Bernard 2002).
- Dyslexia fonts: no benefit (Wery 2017, Kuster 2018).
- Mid-range line spacing: no difference in comprehension (Rello 2016).
- Syntax highlighting: no comprehension gain for novices (Hannebauer 2018).
- Light-on-dark: no daytime advantage (Dobres 2017).
- No study fixes a column count for code.

## Most adopted (practice record)

Kept apart from the best-evidence table above: a different record, with different holders.

| Sub-question | Most adopted | Adoption |
|---|---|---|
| Line length | 45 to 75, 66 ideal (USWDS 2026, GOVUK 2024, Baymard 2022) | no design system cites a study; Carbon states none |
| Body size and leading | at least 16px, line height at least 1.5 (USWDS 2026) | convention, untested |
| Text contrast | WCAG 4.5:1, checked by axe-core, pa11y and Lighthouse | 83.9% of 1,000,000 home pages fail it (WebAIM 2026) |
| Next contrast method | APCA Lc, advocated, not adopted by W3C | WCAG 3 method undecided (W3C 2026) |
| Scanning | F-pattern, then layer-cake (Nielsen 2006, Nielsen Norman 2019) | eye tracking, 232 users in the first |
