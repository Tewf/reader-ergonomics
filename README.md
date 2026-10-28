# Reader ergonomics

How to write notes, documents and files so that they cost the reader as little as possible, according to
what cognitive science, psycholinguistics and software engineering have measured. For people who write,
and for language models that write.

[Lire en français](README.fr.md). The content is in English; only this page has a French version.

## Three doors

| You are | Start at |
|---|---|
| a writer, or a model about to write | [standard.md](standard.md): one page, every principle with its grade, and how to check your text |
| a reader who wants the reasons | [evidence/](evidence/): one literature review per topic, with the case against each principle |
| writing for a known reader | [reader-styles/](reader-styles/): what changes for a novice, an expert, a visual reader, a language model |

## What is here

| Folder | Role |
|---|---|
| [principles/](principles/) | the general optimum, one file per principle, grouped by scale: collection, document, sentence, page |
| [reader-styles/](reader-styles/) | the overrides for a known reader, because the true optimum depends on who reads |
| [shapes/](shapes/) | fixed skeletons for kinds of documents: note, folder README, report, commit message |
| [evidence/](evidence/) | the reviews behind the principles, and one shared [bibliography](evidence/bibliography.md) |
| [checks/](checks/) | programs that verify what a program can verify; questions for judgment otherwise |

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
written to `checks/out/needs-judgment.md`. See [checks/](checks/).

## Contributing

[AGENTS.md](AGENTS.md) holds the rules for changing this repository, for people and models alike.

## Licence and citation

Code under the [Apache License 2.0](LICENSE); prose under [CC BY 4.0](LICENSES/CC-BY-4.0.txt). Reuse it as you wish and
cite it: [CITATION.cff](CITATION.cff).
