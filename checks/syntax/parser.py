"""The dependency parser the syntax checks share: spaCy's small English model, loaded once, on CPU.

spaCy and en_core_web_sm are MIT-licensed; the model is about 12 MB. When either is missing, the
syntax tier is skipped, never failed. Time O(words).
"""
from __future__ import annotations

_nlp = None


def available() -> bool:
    try:
        import spacy
        return spacy.util.is_package("en_core_web_sm")
    except ImportError:
        return False


def parse(texts: list[str]):
    global _nlp
    import spacy
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm", disable=["ner"])
    return list(_nlp.pipe(texts))
