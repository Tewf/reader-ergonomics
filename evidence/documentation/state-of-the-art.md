# State of the art, per sub-question

| Sub-question | Record holder | Measured how |
|---|---|---|
| How to separate page forms | Diataxis | adopted widely; no controlled study |
| What research software documentation must contain | JOSS review criteria | applied by reviewers to submissions |
| Operational details of scientific documentation | Lee 2018 | expert consensus |
| What README sections exist | Prana 2019 | 4,226 sections, 393 repositories, annotated |
| What comment quality means | Rani 2023 | systematic literature review |
| How comments decay | Wen 2019 | large-scale study of inconsistencies |
| What a comment should carry | Ousterhout 2018, PEP 257, Google style guide | expert judgment |

## Upper bounds (achieved)

- README content has been classified at scale (Prana 2019).
- Comment types have been classified at scale (Pascarella 2019).

## Lower bounds (not yet shown)

- No controlled study shows that Diataxis page separation improves reader success.
- No study ties the JOSS criteria to later reuse or fewer defects.

## Most adopted, kept apart from best evidence

The first record is practice. The second is research. They have different holders.

| Sub-question | Most adopted | Best evidence |
|---|---|---|
| Separate page forms | Diataxis (Procida reports hundreds of projects, below the quality bar); GitLab and Red Hat topic types; Django's four kinds | none controlled |
| README sections | standard-readme (6.4k stars); GitHub's what, why, how, help, who | Prana 2019 |
| Heading style | sentence case (Google, Microsoft, GitLab agree) | none read; a convention |
| Brevity | Microsoft "shorter is always better" | no comparison with "too long is better than too short" |
| Define terms | Google: spell out unfamiliar terms | none read for documentation pages |
