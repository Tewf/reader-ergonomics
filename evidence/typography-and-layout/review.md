# Review

Grouped by strand. Surveys first, then primary studies and standards.

## 1. Line length (measure)

- Dyson 2004 (R): characters per line is the variable. Around 100 cpl is read fastest on screen. Around 55 cpl gives the best comprehension and is rated easiest.
- Dyson 2004 also notes that preference and performance "have not been in close agreement".
- Bringhurst (P): 45-75 cpl, 66 ideal for a single column.
- Baymard (P): 50-75 cpl.
- A CSS box of 70ch holds more than 70 letters: with a 17 px humanist sans at 6.9 px per character, 70ch measured 86 characters (Rutter, P).
- Width in px depends on face and size, so measure the rendered line, not the CSS value.

## 2. Size, face and line spacing

- Legge 2011 (R, S): a tenfold fluent range of print size (x-height 0.2 to 2 degrees) gives full reading speed; below it speed falls.
- Rello 2016 (S, n = 104): comprehension was higher at 18 pt and 26 pt than at smaller sizes; mid-range line spacing made no difference.
- Bernard 2002 (S): no reading-speed difference between common serif and sans faces on screen.
- Justified text: results are mixed (Akhmadeeva 2016, R).
- Rello 2013 (S, n = 48 dyslexic readers aged 11 to 50, 12 fonts): sans serif, monospaced and roman gave shorter fixations than serif, proportional and italic; reading time did not differ.

## 3. Dyslexia-related evidence

- Zorzi 2012 (RCT, n = 74 and 20 dyslexic children, two experiments): extra letter spacing halved errors and raised speed by about 0.3 syllables a second (11% to 20%); reading-level controls were unaffected.
- Rello 2013: the dyslexia font OpenDyslexic changed nothing; spacing was uncontrolled.
- Wery 2017 (S): dyslexia-specific fonts gave no benefit.
- Kuster 2018 (S, n = 170): no benefit of a dyslexia font.
- BDA style guide (P): sans serif, 12-14 pt (16-19 px), spacing 1.5, left-aligned, no italics or underline, off-white paper. Guidance, partly beyond the evidence.

## 4. Contrast and polarity

- WCAG 2.2 sets the numeric floors (see baseline.md).
- Piepenbrock 2013 (RCT, fixed 10 pt type): light-on-dark text lost on acuity and proofreading at every age.
- Piepenbrock 2014 (RCT): the loss grows as characters shrink.
- Dobres 2017 (S): no daytime difference between polarities; light wins at night.
- Nielsen Norman Group (P): default to light, offer a switch.

## 5. Scanning and chunking

- Nielsen 1997 (S): 79% of users scanned. Scannable layout raised usability +47%, concise text +58%, both plus objective language +124%.
- NN/g F-pattern (S): first lines and the left edge are read most, so front-load.
- Moran 2016 (P): short paragraphs, headings, lists and bold keywords; the evidence is Miller 1956 and anecdote.
- Horn 1969 (P): structured writing by chunking, relevance, labelling and consistency.
- NNg 2016 (S): phone comprehension matches desktop; reading is slower.

## 6. Layout, signalling and figures

- Gestalt (R): proximity is a strong grouping cue, and common region (a box) groups harder than whitespace.
- Ginns 2006 (MA): placing words in the picture or code they explain, d about 0.72 to 0.85 (secondary). Ayres 2014 (R) gives the split-attention account.
- Richter 2016 (MA): signalling r = 0.17, strongest for low prior knowledge.
- Schneider 2018 (MA, 103 studies): signalling helps retention.
- Sundararajan 2020 (MA, 58 studies, 68 effects): seductive details hurt learning, g = -0.33 (secondary).
- Bateman 2010 (S): embellished charts were no worse for accuracy and better for recall.
- Cleveland 1984 (S): position and length are judged more accurately than angle, area or colour.
- Vessey 1991 (R): tables fit symbolic look-up; graphs fit spatial tasks.
- Tufte 2006 (P): the data-ink rule is intuition, not tested.

## 7. Navigation

- Pirolli 1999 and Budiu 2020: link labels act as information scent.
- Krug (P): the clicked label should equal the page name; breadcrumbs show location.
- Conklin 1987 (R): disorientation and cognitive overhead limit hypertext.
- NN/g (P): deep hierarchies bury content, broad ones blur labels.
- Wang 2023 (S): collapsed content may be missed altogether; accordions fit independent sections.

## 8. Code and mathematics

- Hannebauer 2018 (RCT, n = 390): syntax highlighting did not improve novice comprehension.
- Beelders 2015 (S): fewer fixations with colour, not significant.
- No controlled study supports an 80-column limit.
- Knuth 1989 (P): separate symbols with words, never open a sentence with one.
- Math markup that emits only HTML hides the accessible layer screen readers use (Isaac Physics, P).

## 9. Practice (design systems, standards, practitioner surveys)

Each line gives what the source prescribes, its kind and its adoption. A company page is its owner's claim about itself.
Practice is graded convention, untested; an adoption count is measured, descriptive.

- USWDS 2026 (government design system): body at least 16px, lines 45 to 90 characters, 66 for long text, line height at least 1.5. It cites no study.
- GOVUK 2024 (government design system): lines usually no more than 75 characters, page container 1020px. No study cited.
- Carbon 2026 (vendor design system): a type scale on a 12px base; no line length, no numeric line height, no study.
- Baymard 2022 (research firm blog): 50 to 75 characters. The text credits Ruder, other web typography sources and WCAG 1.4.8, and reports no figures from its own tests.
- W3C 2023a (WCAG 2.2, a W3C Recommendation): 1.4.3 sets 4.5:1, and 3:1 for large text. Level AAA 1.4.8 limits width to 80 characters.
- W3C 2023b (Understanding WCAG 2.2, informative): 3:1 comes from ISO 9241-3 and ANSI/HFES 100-1988. 4.5:1 is 3 times 1.5, the contrast sensitivity loss at 20/40 acuity (an acuity study it cites), so it derives from a loss factor.
- W3C 2026 (WCAG 3, a Working Draft): the contrast algorithm is "yet to be determined", and a size and weight factor is assumed.
- APCA 2026 (advocate repository, a fork): Lc 75 is the minimum for body text over 18px, Lc 90 preferred. The page says W3C recommends neither method and shows no experimental data.
- WebAIM 2026 (automated scan, 1,000,000 home pages, data from the second month of 2026): 83.9% have low-contrast text, about 34 instances per page. The scan counts only what WAVE detects.
- Nielsen Norman 2008 (company, 25 users, 45,237 page views): users read about 20% of the words on an average page.
- Nielsen 2006 (company, eye tracking, 232 users): an F-shaped scan; start subheads and bullets with informative words. The page does not describe tasks or equipment.
- Nielsen Norman 2019 (company, eye tracking): descriptive headings give a layer-cake scan, called "by far the most effective way to scan pages". The page shows one heatmap from 9 participants and no measured effect.
- Nielsen Norman 2020 (company literature review): light mode for normal vision, offer a dark option. NN/g ran no study of its own.
- axe-core, pa11y and Lighthouse (tools; Deque 2026; Pa11y 2026; Lighthouse 2026): check contrast on the rendered page at 4.5:1 and 3:1. axe skips text over background images and reports 1:1 as needing review.
