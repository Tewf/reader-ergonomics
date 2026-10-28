# Syntax tier

Checks that measure sentences on a dependency parse: spaCy with its small English model, on CPU. They run weekly and on
demand, not on every push. Findings are warnings: exact given the parse, but the parse is a model. Install with
`pip install -r checks/syntax/requirements.txt`; without it the tier is skipped with a notice.

<!-- checks:start -->
| File | Role |
|---|---|
| [clause_nesting.py](clause_nesting.py) | Shallow nesting: no sentence centre-embeds a clause inside a centre-embedded clause |
| [dependency_length.py](dependency_length.py) | Short dependencies: no word sits more than `max_distance` words from the word it depends on |
| [parser.py](parser.py) | The dependency parser the syntax checks share: spaCy's small English model, loaded once, on CPU |
| [sentence_links.py](sentence_links.py) | Given before new: each sentence of a paragraph picks up something the one before it gave |
| [sentences_of.py](sentences_of.py) | The parsed paragraphs of the files in scope, shared by the syntax checks. Time O(words) |
<!-- checks:end -->
