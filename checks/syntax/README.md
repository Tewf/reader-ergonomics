# Syntax tier

Checks that measure sentences on a dependency parse: spaCy with its small English model, on CPU. Their findings are
warnings: exact given the parse, but the parse is a model.

They run weekly and on demand, not on every push. Install spaCy and its
model with `pip install -r checks/syntax/requirements.txt`; without it the tier is skipped with a notice.

<!-- checks:start -->
| File | Role | Guarantee |
|---|---|---|
| [clause_nesting.py](clause_nesting.py) | Shallow nesting: no sentence centre-embeds a clause inside a centre-embedded clause | Exact given the parse; the parse itself is a model. |
| [dependency_length.py](dependency_length.py) | Short dependencies: no word sits more than `max_distance` words from the word it depends on | Exact given the parse; the parse itself is a model. |
| [parser.py](parser.py) | The dependency parser the syntax checks share: spaCy's small English model, loaded once, on CPU |  |
| [sentence_links.py](sentence_links.py) | Given before new: each sentence of a paragraph picks up something the one before it gave | Heuristic, on top of a parse. |
| [sentences_of.py](sentences_of.py) | The parsed paragraphs of the files in scope, shared by the syntax checks. Time O(words) |  |
<!-- checks:end -->
