# Meaning tier

Checks that compare meaning with sentence embeddings: fastembed's ONNX build of all-MiniLM-L6-v2, on CPU, with no torch.
Every finding is a judgment question, because a model's similarity is evidence, not proof.

They run on every push; the model is cached between runs. Install with `pip install -r checks/meaning/requirements.txt`; without it the tier is
skipped with a notice.

<!-- checks:start -->
| File | Role | Guarantee |
|---|---|---|
| [document_mode.py](document_mode.py) | Document mode: a long page leans clearly to one of the four modes of documentation | Semantic, so judgment. |
| [embeddings.py](embeddings.py) | The sentence-embedding model the meaning checks share, loaded once, on CPU |  |
| [name_content.py](name_content.py) | Name and content: what a file's name means is close to what its opening says | Semantic, so judgment. |
| [paraphrase.py](paraphrase.py) | Paraphrase: the same fact said twice in different words, which the word-run duplication check cannot see | Semantic, so judgment. |
| [section_cohesion.py](section_cohesion.py) | Section cohesion: no section of a file is far, in meaning, from all the others | Semantic, so judgment. |
<!-- checks:end -->
