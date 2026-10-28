# Review

Surveys first, then the standards, then the empirical studies.

## 1. Surveys and empirical studies

- Rani 2023: systematic literature review of code comment quality assessment. Quality attributes cluster on **consistency** with the code, **completeness**, and **usefulness** beyond the code itself.
- Pascarella 2019: a taxonomy of comments from 40 thousand comment lines in Java (secondary).
- Wen 2019: a large-scale study of code-comment inconsistencies; code and comments drift apart, and inconsistency is the dominant decay mode.
- Prana 2019: 4,226 README sections from 393 repositories, annotated as What, Why, How, When, Who, References, Contribution. What and How are common; Why and project status are the two commonly missing.

## 2. Repository-level standards

- Diataxis (Procida 2020): four page forms from two axes (action versus cognition, study versus work): tutorial, how-to, reference, explanation. Its one hard rule: do not blur forms inside a page.
- JOSS review criteria: the acceptance bar for research software.
  - A statement of need.
  - Installation, with dependencies.
  - Example usage on a real problem.
  - API documentation "to a suitable level".
  - Automated tests.
  - Community guidelines: how to contribute, report a problem, get support.
- Lee 2018, ten simple rules for documenting scientific software:
  - Write comments as you code.
  - Include many examples.
  - Provide a quickstart.
  - Make the README the homepage.
  - Let the command-line help suffice.
  - Keep documentation under version control.
  - Document the full API.
  - Use automated documentation tools.
  - Write error messages that point at the fix.
  - Say how to cite.

## 3. Code-level standards

- PEP 257: a one-line summary, imperative mood, never restate the signature.
- Google C++ style guide: declaration comments describe use, definition comments describe operation, descriptive register.
- Ousterhout 2018: a comment earns its place only by carrying what the code cannot; a comment that repeats the code is the smell.
- The two registers differ (imperative in Python, descriptive in C++); each follows its language's guide.

## 4. Practice

Each row is the owner's own page. None states a method or tests an effect, so each is **convention, untested**. Adoption is a count the owner reports.

- Google 2026 headings: task headings start with a base-form verb, concept headings are noun phrases, one h1, no skipped level, sentence case.
- Google 2026 abbreviations: spell out on first mention when the audience may not know the term; API, HTML and URL "rarely need to be spelled out".
- Microsoft 2026: "Shorter is always better"; lead with what matters; sentence case. The page is dated 2026-07-02 and cites no study.
- GitLab 2026: topic types, sentence case, no skipped level, and "Avoid heading levels greater than H5". The pipeline lints these rules.
- Red Hat 2026a: procedure titles are imperative, concept titles are noun phrases, no "Understanding" or "About", short description of 50 to 300 characters.
- Red Hat 2026b: concept, procedure and reference modules; procedures take no subheadings; procedure titles are gerunds; one short intro paragraph each.
- Django 2026: the writing guide names four kinds, tutorials, topic guides, reference and how-to. The intro page lists more parts, among them deployment guides. Neither page names Diataxis.
- GitHub 2026a README docs: a README says what, why, how to start, where to get help, who maintains it. GitHub builds an outline from headings and truncates past 500 KiB.
- Guo 2026: one maintainer, Danny Guo; a list of twelve optional sections; "too long is better than too short".
- Litt 2026: a spec for README section order, 6.4k stars and 2.5k forks. Its linter is marked work in progress.
- Diataxis site (Procida 2020): "hundreds of documentation projects" and three testimonials, from Vonage, Gatsby and Cloudflare. No list of projects, no study.
- Canonical 2021: the framework's author announces an ongoing restructuring and names five products. No metrics. Written by Procida, so adoption is self-reported.
- Procida 2026: show the destination early, give each step a visible result, keep explanation out and link to it. The page cites no research and asks for tests with real users.
- Viktorin 2022: a proposal to adopt Diataxis for the Python docs. Support came from several core developers; no decision is recorded.
- Hacker News 2024: a 514-point thread on Diataxis. Its critics call strict use rigid, overkill for small projects, and say mixed pages can be fine.
