# The reader-ergonomics standard

The principles below are the best current guess for a reader nobody knows, as far as the evidence goes. When the reader is known, their
[reader style](reader-styles/) overrides what it names, and everything else here still holds.

## How to use it

```text
 who reads?
  ├─ known ──▶ open their reader style
  │                 │
  └─ unknown ───────┤
                    ▼
              pick the shape
                    ▼
          write to the principles
                    ▼
          python3 checks/run.py .
                    ├─▶ error     certain: fix it
                    ├─▶ warning   fix it, or say why it is false
                    └─▶ judgment  answer it in checks/judgments.toml
```

1. **Name the reader.** If they are known, open their style in [reader-styles/](reader-styles/).
2. **Pick the shape** of the document from [shapes/](shapes/).
3. **Write to the principles** below; each file says what it asks, why, and where it stops.
4. **Check:** `python3 checks/run.py .` (or the path to this repository's `checks/run.py`, followed by the folder to check).
   - Fix every **error**: it is certain.
   - Fix every **warning**, or say in one line why it is a false match: warnings come from heuristics.
   - Answer the **judgment** questions in `checks/out/needs-judgment.md`, written only when there are questions, for whoever is at work; none is a normal result for a short text. An answer goes in `checks/judgments.toml`, committed with the text, and holds until its file changes. The open questions come ready to fill in, in `checks/out/judgments-to-answer.toml`.
   - A program verifies what a program can; judgment answers the rest; nobody reviews their own text in place of the checks.

## Grades

Every principle says how strong its evidence is, and never claims more.

- **measured:** controlled studies or meta-analyses found the effect.
- **supported with caveat:** evidence exists, with a limit the principle states.
- **convention:** agreed or standardised, not tested.
- **not supported:** tested, and the effect was not found.

## Principles

The principles act at four scales; the first three nest, the fourth is how all of them are shown.

```text
 ┌ collection: folders and files ─────────────────────────┐
 │ what the reader navigates                              │
 │ ┌ document: one file ──────────────────────────────┐   │
 │ │ the order and depth the reader follows           │   │
 │ │ ┌ sentence ──────────────────────────────────┐   │   │
 │ │ │ what the reader holds in memory            │   │   │
 │ │ └────────────────────────────────────────────┘   │   │
 │ └──────────────────────────────────────────────────┘   │
 └────────────────────────────────────────────────────────┘
   page: how all three are shown (figures, signals, type)
```

<!-- principles:start -->

### Collection: files and folders

| Principle | Claim | Grade |
|---|---|---|
| [Browsable folders](principles/collection/browsable-folders.md) | a collection is shallow and broad: two levels rather than three, folders of at least 3 entries and at most about 32 that a reader can scan. | supported with caveat; the evidence is from menus and web pages, applied to folders by analogy |
| [Dependencies without cycles](principles/collection/dependencies-without-cycles.md) | code dependencies between folders never form a cycle, so every folder sits on a level above everything it uses. | convention, argued from design practice |
| [Group by what changes together](principles/collection/group-by-what-changes-together.md) | a folder holds what serves one purpose and changes together, not files of one type; other ways of grouping are carried by links and indexes. | supported with caveat |
| [Names predict content](principles/collection/names-predict-content.md) | a reader can predict what a file, folder or heading holds from its name before opening it, and each thing has one name throughout. | supported with caveat |
| [One place per fact](principles/collection/one-place-per-fact.md) | each piece of knowledge that must change together lives in one file; every other place links to it. | supported with caveat |
| [One role per file](principles/collection/one-role-per-file.md) | a file holds one role: what it does fits one sentence, and its parts change for the same reasons. | convention, untested |
| [Portable paths](principles/collection/portable-paths.md) | every path in a repository can be checked out on any common filesystem. | convention (a platform specification) |
| [Size is a prompt](principles/collection/size-is-a-prompt.md) | past a length, a file is asked to state its role; size alone never decides a split. | convention, untested. The belief that smaller files have fewer defects is **not supported** |
| [Tunables in config](principles/collection/tunables-in-config.md) | a value someone will set (a quota, a threshold, a price) lives in a configuration file, read at run time, and a value nobody has measured yet is tagged PROVISIONAL. | convention, supported with caveat |

### Document: order and depth

| Principle | Claim | Grade |
|---|---|---|
| [Define before use](principles/document/define-before-use.md) | every term and symbol is defined at or before its first use, premises come in the order they are needed, and each thing keeps one name. | supported with caveat |
| [One mode per document](principles/document/one-mode-per-document.md) | each document serves one mode of reading (learning by doing, doing a task, looking something up, or understanding why) and says which. | convention, untested; widely adopted |
| [Overview first](principles/document/overview-first.md) | a document opens with what it is about and how it is organised (its parts, in a few lines or a simple map) before any detail. | measured |
| [Retrieval prompts](principles/document/retrieval-prompts.md) | a document meant to be learned ends each part with a few questions the reader answers from memory, with the answers folded, and is reread after a gap. | measured |
| [Shallow outline](principles/document/shallow-outline.md) | what matters most sits at the top of a document's hierarchy, and the outline stays shallow: at most three levels of headings. | measured for recall of top-level ideas; the three-level limit is a convention |
| [Short reference distance](principles/document/short-reference-distance.md) | each concept sits close to the places that use it, and the order of a document is chosen so that prerequisites come first and the total distance between definitions and uses is small. | supported with caveat: locality is measured in sentences and applied to documents by analogy |
| [Worked examples with subgoals](principles/document/worked-examples-with-subgoals.md) | a method is taught by a solved example whose steps are named by what they achieve, then faded: the next examples leave more steps to the reader. | measured, for novices; reversed for experts |

### Sentence: density, locality and nesting

| Principle | Claim | Grade |
|---|---|---|
| [Even information density](principles/sentence/even-information-density.md) | a text says no more than the reader needs, and spreads what it says: no sentence packs several new ideas, and a dense term arrives after its context. | supported with caveat for judged quality; **not supported** as a way to read faster |
| [Given before new](principles/sentence/given-before-new.md) | a sentence starts from what the reader already has (the topic, or what the previous sentence ended on) and ends on what is new. | supported with caveat |
| [Shallow nesting](principles/sentence/shallow-nesting.md) | a sentence puts at most one clause inside another; with two nested clauses, readers already misread. | measured |
| [Short dependencies](principles/sentence/short-dependencies.md) | words that depend on each other stay close: a subject near its verb, a modifier next to what it modifies, a pronoun near what it refers to. | measured in controlled sentences; supported with caveat in natural reading |

### Page: figures, layout and type

| Principle | Claim | Grade |
|---|---|---|
| [Draw relations](principles/page/draw-relations.md) | a relation, a set, a quantity or a process is shown as a figure placed with the words that explain it, not as words alone. | measured |
| [Figure next to its text](principles/page/figure-next-to-its-text.md) | the words that explain a figure, a formula or a block of code sit beside or inside it, not on another page or below the fold. | measured |
| [Readable measure](principles/page/readable-measure.md) | body text is set at a line length of about 45 to 75 characters, at a size in the fluent range, with line spacing of at least 1.5. | supported with caveat |
| [Signal the structure](principles/page/signal-the-structure.md) | the structure of a text is visible before it is read: headings that name their content, lists for parallel items, tables for comparisons, bold for the defined term. | measured |
| [Sufficient contrast](principles/page/sufficient-contrast.md) | text has a contrast ratio of at least 4.5:1 against its background, dark text on a light ground by default, with a dark theme offered and never forced. | measured for polarity; the 4.5:1 floor is a convention (a standard) |

<!-- principles:end -->

## When two principles pull apart

- **The stronger grade wins.** At equal grade, the reader style decides; with no style, the reader with less prior knowledge does.
- One place per fact makes the reader follow links, and every link is a hop. Link, and give a novice a one-line reminder at the distant use.
- Lifting shared files to a common ancestor crowds it. Put shared code in a folder of its own, declared as a lower level.
- A file past the size trigger that passes the one-role test stays whole.

## Where the evidence is

Every principle links to its review in [evidence/](evidence/), and every work cited is listed once in the
[bibliography](evidence/bibliography.md).
