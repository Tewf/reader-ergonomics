# Against: the file and folder conventions

The evidence against nine file and folder conventions, theme by theme: the claim and its grade, the evidence against, then a verdict with a one-line amendment.

## One place per fact

- **Claim** (supported with caveat): every fact or snippet lives in one file; others link to it and never copy it.
- Thomas 2019 restates **DRY** (don't repeat yourself) as a rule about knowledge and intent, not about text, and concedes that the first edition explained it poorly (secondary: read in a summary quoting the book).
- Kapser 2008 judged up to 71% of the **clones** (copied code fragments) in Apache and Gnumeric to have a positive effect on maintainability. Boiler-plating and replicate-and-specialize were mostly beneficial, verbatim snippets and parameterized code mostly harmful.
- Juergens 2009 supports the rule where knowledge is shared: about half of the clones (52%) held inconsistencies. Developers confirmed 107 faults caused by changing one copy and not the others (five systems, 1,427 clone groups, about 1800 manual assessments).
- Metz 2016 names the opposite risk, "duplication is far cheaper than the wrong abstraction", once one shared piece is bent to fit callers that diverge.
- A link has a reading cost: DeStefano 2007 found in its review that the extra decisions and visual processing of hypertext impair reading, most for readers with low working memory or low prior knowledge.
- Madrid 2009 found that 3 versus 8 links per page did not change learning, while an incoherent reading order raised load (secondary: both abstracts read in index summaries).
- **Verdict: keep with an amendment.** Amendment: one place per piece of knowledge that must change together; a short copy is allowed when the copies change for different reasons, and it names its source.

## One role per file

- **Claim** (convention, untested): a file's role fits one sentence without "and"; structure, style and behaviour (HTML, CSS, JS) live in separate files.
- The test comes from Martin 2008, chapter 10: describe a class in about 25 words without "if", "and", "or" or "but" (secondary: wording read in a chapter summary).
- Martin 2017 restated the single responsibility principle as responsibility to one **actor** (a group of users or stakeholders who require a change). He wrote that the old name is misread as a rule that each module does one thing: the test moved from wording to change.
- A sentence test fails both ways, and Ousterhout 2025 makes both points against the related one-thing rule. Anything can be given a name (a false pass). Two closely related steps, such as taking a lock and then updating, belong together (a false fail).
- **Co-change** (files modified in the same commit) tests roles by behaviour. Gall 1998 recovered logical coupling from 20 releases of a telecom switching system. Zimmermann 2005 covered eight projects. In the 82% of queries where it suggested anything, it named a file changed in the same commit among its top three suggestions 72% of the time, including couplings program analysis cannot see.
- The HTML, CSS and JS clause is contested: Hunt 2013 argued that separating markup from display logic separates technologies rather than concerns, since the two change together (slides and summaries read, talk not watched).
- That clause also splits by file type, which the grouping convention forbids at folder level, so the two conventions disagree with each other.
- **Verdict: keep with an amendment.** Amendment: keep the sentence as the cheap first test, confirm it against co-change, and split by component rather than by language.

## File length

- **Claim** (supported with caveat): past about 80 statements a file restates its role and splits if the sentence needs "and"; about 500 lines is a ceiling.
- No size threshold has held up: El Emam 2002 found no threshold effect of class size in three systems with four size measures. He traced earlier U-curves to a mathematical artifact (dividing defects by size, then plotting the ratio against size).
- The shape of the curve is contested.
  - Basili 1984 found larger modules less error-prone even when more complex (370 Fortran modules, about 90,000 lines).
  - Hatton 1997 reported medium components most reliable.
  - Fenton 1999 judged this **Goldilocks conjecture** (an optimal module size) unsupported.
- Koru 2008, Koru 2009 and Koru 2010a found defect-proneness rising more slowly than size in ten open-source products, then Mozilla, Eclipse, JBoss and Cn3d, then ten closed-source products: smaller modules carry proportionally more defects.
- Syer 2015 replicated Koru 2008, extended it to Chrome, Eclipse, Firefox and Netbeans, and judged its conclusions not generalizable. With defects dated at their introduction and the survival model's assumptions checked, defect density formed an inverted U, highest in medium files.
- Splitting leaves total size unchanged, and size is the confounder behind most metric-defect links: in El Emam 2001 the studied object-oriented metrics lost their association with faults once class size was controlled.
- Koru 2010b found smaller modules proportionally more coupled, more so after refactoring, so a split can add dependencies per line.
- Ousterhout 2018 holds that length alone rarely justifies a split, prefers **deep modules** (a simple interface over much functionality) and names **classitis** (many shallow classes) as a failure (secondary: wording read in reader notes).
- Ousterhout 2025 adds that over-split methods become **entangled**: one cannot be understood without reading the other.
- Every study above measures code modules; none measures prose, so the statement count transfers to documents by analogy only.
- **Verdict: keep with an amendment.** Amendment: the trigger stands; the ceiling becomes a review, not an automatic split, and a split must yield pieces that change separately and stay deep.

## Group folders by purpose

- **Claim** (convention, untested): folders group by what they serve, not by file type; no `docs/`, `assets/` or `misc/` buckets.
- Tarr 1999 named the **tyranny of the dominant decomposition**: one decomposition, whichever it is, forces every other concern to cut across it.
- Library science met this first: Ranganathan 1933 composed class numbers from **facets** (independent aspects of a subject), theorized in Ranganathan 1937.
- The **citation order** (the order facets are combined, later written as the PMEST formula: personality, matter, energy, space, time; Satija 2017) decides which facet stays together on the shelf.
- Aspects cited later are scattered; Broughton 2015 calls them **distributed relatives**, reconnected by a relative index (secondary: definition read in a glossary).
- Martin 2017 groups by change, not by name: the **common closure principle** gathers classes that change for the same reasons at the same times.
- No controlled comparison of package-by-feature against package-by-layer was found. Silva 2014 projected co-change clusters onto the packages of three systems and found a different pattern in each, so declared purpose and actual change can diverge.
- **Verdict: keep with an amendment.** Amendment: purpose is the first facet because it should predict change; index the other facets, and check folder boundaries against co-change.

## Navigation

- **Claim** (supported with caveat): any file within two clicks; a browsed folder splits past about 16 entries, citing an optimum of 8-16 items per level; subfolders only from 3 items.
- Miller 1981 timed selection among 64 targets in menus shaped 2^6, 4^3, 8^2 and 64^1: two levels of eight was fastest and had fewest errors.
- Kiger 1984 tested five 64-target menus: 4x16 was fastest, not reliably faster than 16x4 or 8x8, and users preferred 8x8 (secondary: read in Larson 1998).
- Larson 1998 used three sites of 512 items each and 19 participants, with 24 searches per person and targets drawn from the 128 shared items. 16x32 was fastest (mean 36 s), 32x16 next (46 s), 8x8x8 slowest (58 s), and only the three-level tree was significantly slower.
- So the best measured layout had two levels with 32 items on one of them. Breadth 8 lost when it forced a third level: an optimum of 8-16 per level is not what these studies found.
- The direction of all three studies supports the 3-item floor: needless depth costs more than breadth.
- The transfer is untested. The studies timed search for a named target through category labels. Sadowski 2015 logged about five search sessions and 12 queries per developer per workday at Google, often aimed at a known location.
- Ko 2006 found developers spent about 35% of their time on the mechanics of navigating within and between files, and their searches often failed on misleading cues.
- **Verdict: weaken.** Amendment: prefer two levels to three, allow up to about 32 scannable entries, and cite the menu studies as analogy, not measurement.

## Dependencies

- **Claim** (convention, untested; argued from design practice): a file sits at the depth of its usage scope. Imports reach up to a common ancestor, never up-then-down into a sibling. Folders never import in a cycle.
- The sources support acyclicity by argument, not by controlled study: Lakos 1996 **levelization** (each component gets a level above everything it uses, possible only without cycles) and the **acyclic dependencies principle** of Martin 2017.
- Tension with breadth: a file shared by several subtrees lifts to their common ancestor, often the root, which then grows past the breadth ceiling.
- Tension with its own sources: levelization puts shared code in a separate lower-level component, which in a tree is a sibling folder, and importing a sibling is the up-then-down shape the rule forbids.
- Lakos 1996 also lists redundancy among its levelization techniques (secondary: section title read in the table of contents; its scope is unverified).
- **Verdict: keep with an amendment.** Amendment: keep the cycle ban; allow imports into a sibling folder declared as a lower level, and check levels and cycles rather than path shapes.

## Names

- **Claim** (supported with caveat): full descriptive names, no abbreviations; if a name needs explaining, rename it.
- The **scope rule** of Martin 2008, chapter 2: a name's length should match the size of its scope, and single letters suit local variables in short methods.
- Binkley 2008, journal version Binkley 2009: with 158 programmers, longer names from production code took longer to process and lowered recall correctness; the authors conclude that good naming limits length.
- Lawrie 2006 and Lawrie 2007: full words gave the best comprehension, but often not significantly better than abbreviations, and well-chosen abbreviations may be easier to remember.
- **Verdict: keep with an amendment.** Amendment: full words at wide scope; short names in small scopes and abbreviations the reader already knows (URL, HTML, README) are allowed.

## Configuration

- **Claim** (convention, untested): tunables live in a config file loaded at runtime; placeholder values carry a PROVISIONAL tag.
- Xu 2015: only 6.1-16.7% of parameters were set by most users and up to 54.1% were seldom set; its guidelines would remove 51.9% of a commercial storage system's parameters.
- Each knob costs. In Xu 2015, 17.3-48.5% of users' configuration issues were about finding or setting the right parameter. Of 620 user-reported issues, 17.5-53.3% of the configuration errors came from defaults wrongly left in place.
- Yin 2011: of 546 real misconfigurations, 70.0-85.5% were parameter mistakes, and 38.1-53.7% of those were illegal values.
- Potdar 2014 supports the tag and shows its limit: **self-admitted technical debt** (comments marking a known shortcut) appeared in 2.4-31% of files in four projects, but only 26.3-63.5% of it was later removed.
- **Verdict: keep with an amendment.** Amendment: a value moves to config only when someone will set it, otherwise it is a named constant; a check counts and ages PROVISIONAL tags.

## Portable paths

- **Claim** (supported with caveat: a platform specification, not a study): no `: * ? " < > | \` in a path component, no leading or trailing space, no names differing only by case, no versioned symlink.
- No source argues against the rule, but Microsoft 2024 shows it incomplete. It also reserves device names (CON, PRN, AUX, NUL, COM1-9, LPT1-9, even with an extension, as in NUL.txt). It forbids a trailing period and characters 1-31. It caps paths at 260 characters unless long paths are enabled.
- Accented names can be stored decomposed on macOS, and git recomposes them only when core.precomposeUnicode is on (Git 2023).
- **Verdict: keep with an amendment.** Amendment: add reserved device names, trailing periods, control characters and a path-length budget to the check.

## Practice against the principles

Each item is a practice that pulls against one principle. The pages are tool owners and a practitioner guide, so the claims are theirs.

- **Group folders by purpose:** Maven 2026, Cargo 2026 and Rails 2026 group by type at the top level (src/main, tests/, app/ with models, views, controllers). The folder name predicts content across projects, which is the same reader benefit. Amendment: where a tool finds files by folder name, the tool's convention wins.
- **Tunables in config:** Wiggins 2011 puts configuration in environment variables, not files, while granting that files outside version control beat constants. Both keep values out of code. Amendment: outside the code, in a file or the environment.
- **One place per fact:** the Rule of Three (Fowler 1999, secondary) adds a threshold, merge at the third copy. Dodds 2020 and Metz 2016 push the threshold later. Amendment: none; the change-together test stays primary.
- **File length:** ESLint 2026a defaults to 300 and Checkstyle 2026 to 2000, against the principle's 500 ceiling. ESLint says recommendations usually range from 100 to 500. Amendment: none; the defaults differ without a study.
- **Navigation:** Nielsen Norman 2017 favours options visible at once and gives no numeric limit. Nielsen Norman 2024 offers a tree-test benchmark (median 62%), which could serve as a baseline for a findability claim but not as a breadth limit.
- **Portable paths:** Microsoft 2024 also reserves COM and LPT followed by the superscript digits 1 to 3. Amendment: add those forms to the reserved-name check.
- **Dependencies:** Go internal/ and Bazel visibility enforce boundaries in the compiler or build, where the principle only asks that folders never form a cycle. Amendment: none; boundaries extend the rule.

## The common thread

- Most sources above define their unit by change:
  - Parnas 1972 hides in each module a design decision likely to change.
  - Martin 2017 groups by reasons and times of change.
  - Thomas 2019 locates duplication in knowledge.
  - Gall 1998 and Zimmermann 2005 read coupling from co-change.
- The conventions test text instead: copied text for duplication, a sentence for role, a folder name for purpose, a count for length and breadth.
- Text tests are cheap and work on day one; they fail where wording and change diverge, which is where the evidence above concentrates.
- Proposal: make co-change from version history the operational test, and keep the text tests as the fallback while history is short.

| Convention | Text test today | Co-change test proposed |
|---|---|---|
| One role per file | one sentence, no "and" | parts that never change in the same commit are separate roles |
| One place per fact | no copied text | copies that change together merge; copies that change apart may stay |
| Group by purpose | a folder named for a purpose | co-change clusters fall inside folders (Silva 2014) |
| File length | 80 statements, 500 lines | a split is valid when the pieces change separately |

- Co-change is sparser than structural dependencies: Beck 2011 reports earlier work where structural dependencies clustered better for that reason and combining both improved the result. In its own 16 projects co-change was among the couplings most congruent with real modules, no principle dominating.
- Mechanical commits (renames, reformatting) create false co-change and must be filtered; thresholds stay PROVISIONAL until measured on the repository's own history.

## Not verified

- Practice strand: Fowler 1999 is read on a Wikipedia page, not in the book. The Go 1.4 internal rule is read in its release notes; its later scope is not checked. Potvin's article of 2016, Turborepo and Nx were not re-read.

- Read in summaries, not in the books: the 25-word test (Martin 2008), the length and classitis passages (Ousterhout 2018), the DRY restatement (Thomas 2019), and the redundancy technique (Lakos 1996, table of contents only).
- Kiger 1984 is reported through Larson 1998; the paper itself was not read.
- Hunt 2013: slides and summaries read, talk not watched; DeStefano 2007 and Madrid 2009: abstracts read in index summaries; Broughton 2015: term from the contents, definition from a glossary.
- Syer 2015 appeared online in 2014; the key uses the issue year.
