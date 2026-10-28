"""The sentence-embedding model the meaning checks share, loaded once, on CPU.

fastembed's ONNX build of all-MiniLM-L6-v2 (Apache-2.0, about 90 MB, no torch). Vectors come
back normalised, so a dot product is a cosine similarity. When fastembed is not installed, the
meaning tier is skipped, never failed. Time O(texts).
"""
from __future__ import annotations

import os

MODEL = "sentence-transformers/all-MiniLM-L6-v2"
_model = None


def available() -> bool:
    try:
        import fastembed  # noqa: F401
        return True
    except ImportError:
        return False


def embed(texts: list[str]):
    global _model
    import numpy
    from fastembed import TextEmbedding
    if _model is None:
        _model = TextEmbedding(MODEL, cache_dir=os.environ.get("FASTEMBED_CACHE_PATH"))
    vectors = numpy.array(list(_model.embed(texts))) if texts else numpy.zeros((0, 384))
    norms = numpy.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / numpy.where(norms == 0, 1, norms)
