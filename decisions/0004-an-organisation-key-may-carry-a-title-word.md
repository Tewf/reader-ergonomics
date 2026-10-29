# 0004: An organisation's key may carry a title word instead of a letter

**Decision:** an organisation's key may end in a title word instead of a letter, `Microsoft 2026 icons`, read as
part of the key only when the bibliography holds it.

**Status:** accepted, 2026-10-29, in v1.11.0. **Shape:** [decision record](../shapes/decision-record.md).

## Context

- [0003](0003-one-key-one-work-across-the-family.md) gives a second work of one author and year the next letter
  free in the family. For a person that stays short. For an organisation it runs long: on 2026-10-29 the family's
  bibliographies held ten keys from `GitHub 2026` to `GitHub 2026i`, and six for `W3C 2023`.
- A letter says nothing of the work, so a reader of `GitHub 2026g` must open the bibliography to know which page it
  is ([names predict content](../principles/collection/names-predict-content.md)).
- A word after the year is also how running text goes on: in "Microsoft 2026 recommends a plain style", the word
  after the year is the sentence's verb.

## Decision

- **The form:** the organisation's name, a space, the year, a space, one word of letters or digits taken from the
  work's title or subject (`Microsoft 2026 ADR`, `W3C 2023 contrast`). Hyphens may join it (`dark-mode`); it holds no
  space.
- **It is optional, and for organisations.** A person keeps the letter. A key already in use is not renamed for it.
- **The longer key wins only when it exists.** The check `citations` tries the word after the last year of a
  citation. If the bibliography holds that key, the citation cites it; otherwise it reads as before.
- **Uniqueness is unchanged.** `bibliography-keys` compares whole keys without case or punctuation, so
  `Microsoft 2026 icons` and `Microsoft 2026 ADR` are two keys, and `Microsoft 2026 Icons` beside the first is one
  key held twice.

## Consequences

- An organisation's works can be told apart in the text, where the reader is, and a new one is named without
  finding the next free letter in six bibliographies.
- A repository that holds both `Microsoft 2026` and `Microsoft 2026 icons` cannot cite the first just before the
  word "icons": the longer key wins. Such a sentence is reworded; the case should be rare, since the word is chosen
  from the work's title.
- A citation of the plain key, when only titled keys exist, is reported as having no entry, so a missing word is
  found.
- The interface in [extending](../extending.md) grows by one clause, compatible with every key already written.

## Considered options

- **Letters only, as before.** Nothing to change, but `GitHub 2026i` names nothing a reader can predict.
- **The word joined by a hyphen or in brackets, `Microsoft 2026-icons`.** Parsed without consulting the bibliography,
  but one more form for writers to learn; the longest match costs one lookup per citation.
- **Any word after the year read as part of the key.** Simpler, but "Microsoft 2026 recommends" would become a key
  with no entry.

## See also

[Decisions](README.md); the checks, [citations.py](../checks/program/citations.py) and
[bibliography_keys.py](../checks/program/bibliography_keys.py); the rule it extends,
[0003](0003-one-key-one-work-across-the-family.md).
