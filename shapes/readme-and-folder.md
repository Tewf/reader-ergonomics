# Shape: folder and its README

A reader lands in a folder from a search result or a file listing, not from the front page. A signpost that sends them
elsewhere makes them search again. Listing what is here and showing one real use in a README lets them act from where
they stand.

## Skeleton

````markdown
# <What the folder is for, in the field's words>

One or two sentences: the role of this folder, and who uses it.

## Contents

| File or group | What it is |
|---|---|
| [name](name) | one line, plain words, grouped by role, not exhaustive |

## Example

```sh
the command a reader would actually run
```
```text
the output it actually produced, pasted, never invented
```

## See also
The parent folder, and where the depth lives.
````

## Rules for the folder itself

- Between 3 and about 32 entries; past that, group by purpose; under 3, fold into the parent, unless the folder is one record of a collection ([browsable folders](../principles/collection/browsable-folders.md)).
- Folders group what changes together, not files of the same type: no `docs/`, `assets/` or `misc/` buckets ([group by what changes together](../principles/collection/group-by-what-changes-together.md)).
- The parent points at the child, and the child explains itself. The README states what a thing is in one fresh line and links to the depth, never copies it ([one place per fact](../principles/collection/one-place-per-fact.md)).
- Register: name the concept, not a metaphor for it ("exact decision procedure", not "the tool that knows").

## Evidence

Documentation studies list what readers of a repository look for first: what it is, how to install it, a real
example, and where to go next ([documentation](../evidence/documentation/)).
