# 0007: A shape may be declared for a set of files

**Decision:** a repository may declare in its configuration the shape a set of files follows; the duplication
check then skips a line that holds the same words as a line of that shape's skeleton.

**Status:** accepted, 2026-11-09, in v1.23.0. **Shape:** [decision record](../shapes/decision-record.md).

## Context

- Since v1.19.0 the duplication check skips the lines a file's shape prescribes, when the file names its shape on a
  `Shape:` line and the line appears verbatim in the shape's skeleton.
- Two collections showed what that leaves out, on 2026-11-09:
  - a repository of coursework holds about 130 READMEs, one per practical, with the same closing lines: where the
    record is, where the concept note is, how the book is rendered. They drew 218 findings. None carries a Shape
    line, and their lines differ from one another only by a file name or a link.
  - a vault of notes follows shapes written in one rules file; no note names its shape.
- Shortening such a line does not end the finding. The lines of a skeleton follow one another, the check reads
  across lines, and it removes code and addresses, which is where the files differ: the run moves to the next line.
- The check already holds that a prescribed line "is not a fact held many times". What was missing is a way to say
  which files a shape prescribes for, and a way to match a line whose file name is its own.

## Decision

- **A shape is declared for a set of files in config.** `[[duplication.shapes]]` takes `files`, a list of
  patterns, and `shape`, a path from the root to a file with a Skeleton block. A file's own `Shape:` line is read
  as before when no entry covers it.
- **A skeleton line is matched as the check reads prose.** Both lines are reduced to their words, lower case, code
  and link addresses removed, and compared whole. The skeleton writes its variable part as code or as a link, and
  every file's own name matches it. A verbatim match still counts.
- **Only whole lines match.** A sentence that shares words with a skeleton line and adds its own is prose, and a
  copy of it is still reported.

## Consequences

- A repository writes down the skeleton its files share, once, where a reader and a check can find it; it no
  longer exempts whole files, which also hid the real copies inside them.
- The skeleton has to be kept true: a line that changes in the files and not in the shape is reported again.
- A fact repeated in every file can be passed off as skeleton by writing it into the shape. The shape file is
  read by people, and a line that states a fact about the world, not about the layout, does not belong there.
- A line wrapped differently in two files matches the skeleton in one of them only: the match is by line.

## Considered options

- **A `Shape:` line in each of the files.** It is what the standard already reads. It adds a line to 130 public
  READMEs for the benefit of a check, and it does not match a line whose file name differs.
- **Exempt the files by path.** It is what the configuration allowed. It hides every copy in those files, the
  accidental ones too.
- **Count a code span as a word.** Two lines that differ by a file name would stop matching everywhere. It would
  also stop reporting a paragraph copied with one identifier changed, which is the copy the check exists for.

## See also

[Decisions](README.md); the check, [duplication.py](../checks/program/duplication.py); the principle it serves,
[one place per fact](../principles/collection/one-place-per-fact.md).
