# Position

What is measured, what is not, and where practice runs ahead of the evidence.

## Known (measured)

- Line length affects speed and comprehension in opposite directions; both ranges are documented.
- Type below the fluent range slows reading; larger than the minimum helps comprehension.
- Common serif and sans faces read equally fast on screen.
- Dyslexia-specific fonts do not help; wider letter spacing helps dyslexic children.
- Light text on a dark ground is no better by day and worse at small sizes.
- Readers scan; layout that supports scanning raises usability.
- Words belong with the figure they explain; decoration does not help learning.

## Known with caveat

- 45-75 cpl as a safe band: practitioner consensus around one review.
- Off-white paper, left alignment, no italics: guidance with weak direct evidence.
- Collapsed content is missed: one study and design practice.

## Not known

- No study fixes the best line length for mixed text and code.
- No study tests heading density or paragraph length thresholds.
- No study tests a logical-line limit for a file or note.
- Evidence on dark mode comes from older displays.

## What this repo adds

- It states each rule with its grade, so a convention is not mistaken for a result.
- It measures the rendered line (characters, pixels) instead of trusting a CSS unit.
- It separates the standard (WCAG, pass or fail) from the research (ranges, trade-offs).

## Practice against evidence

Practice runs ahead of the evidence:
- Line length ranges in USWDS 2026, GOVUK 2024 and Baymard 2022 come from craft tradition. Baymard's own text credits Ruder and reports no numeric line-length test results.
- APCA thresholds are published by their authors with no experimental data on the page.
- The 4.5:1 floor has a stated derivation, a loss factor, but the page cites no reading experiment.

Practice ignores the evidence:
- 83.9% of home pages fail 4.5:1 (WebAIM 2026): a known rule, widely broken.
- Speed and comprehension peak at different lengths (Dyson 2004). None of the three design systems read names the trade-off; each gives one range.

Pending change:
- WCAG 3 has not chosen a contrast method (W3C 2026), so 4.5:1 stays the floor until it does.
- No rendered-page contrast checker is in this repository's checks; axe-core, pa11y and Lighthouse fill that role in practice.
