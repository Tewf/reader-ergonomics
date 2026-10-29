# Reader ergonomics

What cognitive science, psycholinguistics and software engineering have measured about how to write notes, documents
and files so that they cost the reader as little as possible. For people who write, and for language models that
write.

> **Status:** a work in progress, shared as it is, in the hope that it helps whoever needs it. It is an informal
> reading of published research: not an official standard, not a peer-reviewed study, not a new result, and not a
> claim to the state of the art. Each principle says how strong its evidence is, and many are conventions nobody
> has tested.
>
> **How it was made:** with Claude, an AI assistant by Anthropic, under the maintainer's direction. AI agents
> drafted the literature reviews; every reference was resolved by script and claims were spot-checked, but not
> every source was read in full, and a number read only in a summary is marked "(secondary)". Corrections are
> welcome as issues.

[Lire en français](README.fr.md). The content is in English; only this page has a French version.

## Three doors

| You are | Start at |
|---|---|
| a writer, or a model about to write | [standard.md](standard.md): one page, every principle with its grade, and how to check your text |
| a reader who wants the reasons | [evidence/](evidence/): one literature review per topic, with the case against each principle |
| writing for a known reader | [reader-styles/](reader-styles/): what changes for a novice, an expert, a visual reader, a language model |
| building an extension for one genre | [extending.md](extending.md): the layout to mirror, and the parts of this repository it can rely on |

## What is here

| Folder | Role |
|---|---|
| [principles/](principles/) | the best current guess for any reader, one file per principle, grouped by scale: collection, document, sentence, page |
| [reader-styles/](reader-styles/) | the overrides for a known reader, because what works best depends on who reads |
| [shapes/](shapes/) | fixed skeletons for kinds of documents: note, folder README, report, commit message |
| [evidence/](evidence/) | the reviews behind the principles, and one shared [bibliography](evidence/bibliography.md) |
| [checks/](checks/) | programs that verify what a program can verify; questions for judgment otherwise |
| [decisions/](decisions/) | why the repository is built as it is: one record per decision, with the options it rejected |

## Why grades

A principle is only as strong as its evidence. Each one says whether it was **measured**, is **supported with caveat**,
is a **convention** nobody has tested, or was tested and is **not supported**. Some well-known rules land in the last
two groups, and the standard says so.

## Check a repository

```sh
git clone https://github.com/Tewf/reader-ergonomics
python3 reader-ergonomics/checks/run.py path/to/your/repo
```

Only the Python standard library is needed. Exact findings fail the run; questions a program cannot answer are
written to `checks/out/needs-judgment.md`, and their answers are kept in `checks/judgments.toml`. See
[checks/](checks/).

## Contributing

[AGENTS.md](AGENTS.md) holds the rules for changing this repository, for people and models alike.

## Licence

Code under the [Apache License 2.0](LICENSE); prose under [CC BY 4.0](LICENSES/CC-BY-4.0.txt). Reuse it as you wish, with
credit to this repository; [CITATION.cff](CITATION.cff) gives a citation if you need one.
