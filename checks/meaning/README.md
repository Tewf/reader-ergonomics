# Meaning tier

Checks that compare meaning with sentence embeddings: fastembed's ONNX build of all-MiniLM-L6-v2, on CPU, with no torch.
They run on every push; the model is cached between runs. Every finding is a judgment question, because a model's
similarity is evidence, not proof. Install with `pip install -r checks/meaning/requirements.txt`; without it the tier is
skipped with a notice.

<!-- checks:start -->
| File | Role |
|---|---|
| [document_mode.py](document_mode.py) | Document mode: a long page leans clearly to one of the four modes of documentation |
| [embeddings.py](embeddings.py) | The sentence-embedding model the meaning checks share, loaded once, on CPU |
| [name_content.py](name_content.py) | Name and content: what a file's name means is close to what its opening says |
| [paraphrase.py](paraphrase.py) | Paraphrase: the same fact said twice in different words, which the word-run duplication check cannot see |
| [section_cohesion.py](section_cohesion.py) | Section cohesion: no section of a file is far, in meaning, from all the others |
<!-- checks:end -->
