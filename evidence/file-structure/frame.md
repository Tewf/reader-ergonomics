# Frame: the problem and its names

The problem in one sentence, the names research and practice give it, and the terms searched.

## The problem in one sentence

Given a set of files and the references between them, choose how content is cut into files and how files are arranged in folders. The aim is that nothing is held twice, each file does one thing, and a reader or an import reaches what it needs in few steps.

## What the field calls it

The field has no single name. It is the meeting point of five strands, plus a human one.

| Strand | Field names | Acronyms and key authors |
|---|---|---|
| Why modules at all | **modularity**, **information hiding**, **coupling and cohesion** | DSM (Baldwin, Clark), Parnas |
| Choosing the folder tree from the dependency graph | **software clustering**, **remodularization**, **architecture recovery** | MQ, Bunch (Mancoridis), MoJo (Tzerpos, Holt), SBSE |
| Scoring a hierarchy | **hierarchical clustering objectives** | Dasgupta cost, SSE hardness |
| Holding nothing twice | **hash-consing**, **minimal DAG**, **tree compression**, **clone detection** | MDL, Type 1 to 4 clones, CCFinder, Deckard |
| Checking rules | **architecture conformance checking** | reflexion models, ArchUnit |
| The human constants | **menu depth versus breadth**, **information foraging**, **identifier studies** | scent, Miller, Pirolli |

## Search terms tried, three ways

- Academic: software module clustering, remodularization, hierarchical clustering cost function.
- Acronym: MQ, MoJoFM, DSM, SBSE, SSE.
- Author: Mancoridis, Dasgupta, Candela, Garcia, Murphy.

## What practitioners call it

Practice uses other words for the same questions. Each row pairs a practitioner term with the field name already used above.

| Practitioners say | The field says |
|---|---|
| project layout, repo structure, "where do files go" | architecture recovery, remodularization |
| package by feature, package by layer | dominant decomposition (Tarr 1999), common closure (Martin 2017) |
| screaming architecture | information hiding, purpose as first facet |
| monorepo, workspace | modularity at repository scale |
| DRY, WET, Rule of Three, AHA, wrong abstraction | clones, one place per fact |
| max-lines, "file too long" | size is a prompt |
| internal packages, visibility, code owners | conformance checking, folder boundaries |
| reserved names, MAX_PATH | portable paths |
