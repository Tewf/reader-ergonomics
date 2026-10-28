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
