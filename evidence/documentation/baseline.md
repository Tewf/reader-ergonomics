# Baseline: what the documentation rules are compared against

| Level | Baseline |
|---|---|
| Repository | Diataxis, the JOSS review criteria and Lee 2018 together |
| Code | PEP 257 and the Google style guide, filtered by Ousterhout's test |

The academic anchor for the code level is Rani 2023 (consistency, completeness, usefulness).

## Repository checklist (per page, then per repo)

Per page, from Diataxis (Procida 2020) and from Prana 2019:

1. One Diataxis form per page; a folder README may hold two clearly separated blocks, anything more is a split finding.
2. Say the form's thing: tutorial, the reader does something and it works; how-to, a goal, the commands and the output quoted; reference, facts without persuasion; explanation, why, with the alternatives that lost.
3. Every example is real: commands were run, output is quoted as printed, numbers name their source.
4. The entry fits the reader it names: a term of art is defined, linked at first use, or deferred to a page that defines it.

Per repo, from the JOSS review criteria and from Lee 2018:

5. Statement of need: problem, audience, relation to other work.
6. Installation: dependencies named, exact commands, verified.
7. Example usage on a real problem, near the front door.
8. API or functionality documentation at a suitable level.
9. Automated tests, and the README says how to run them.
10. Community guidelines: how to contribute, report a problem, get support. Research repositories most often miss this one.
11. How to cite, and the licence scope.
12. Command-line help suffices to use each tool; error messages point at the fix.

A repository may reject a rule deliberately; the rejection is written where a reviewer will look for the missing thing.

## Code checklist (per file, in order)

1. The file header states the role: what the file owns and the one invariant the names do not give. A role sentence needing "and" is a structure finding.
2. Declaration comments describe use, not operation: what the caller gets, must guarantee, and what happens on failure.
3. Never restate the signature; name a parameter in prose only when its meaning or unit is not in its name.
4. Consistency beats completeness: a comment that contradicts the code is the worst state (Wen 2019), so it moves with the code or is deleted.
5. Constraints, units and provenance: anything measured, cited or bounded says where from; a magic number gets its reason or a pointer to its config.
6. No narration: a comment saying what the next line does is noise.
7. Error paths are documented where thrown: what the user sees, which exit code, and that it is deliberate (Lee 2018).
