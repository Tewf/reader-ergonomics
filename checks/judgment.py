"""Judgment: the questions a program cannot answer exactly, sent to the backend chosen in config.

Backends, cheapest first:
- `none`: the questions are dropped.
- `flag` (default): the questions are written to `checks/out/needs-judgment.md`, for the
  person or the agent already running to answer. Costs nothing.
- `local`: each question goes to a model served on this machine through an OpenAI-compatible
  chat endpoint. Its address and model come from the environment only
  (READER_ERGONOMICS_LOCAL_URL, READER_ERGONOMICS_LOCAL_MODEL); there is no default.
- `api`: the same protocol to a paid provider (READER_ERGONOMICS_API_URL, _KEY, _MODEL).
  It refuses to run unless `[judgment.api] enabled = true` in config: a paid check exists,
  but stays off until the maintainer turns it on.

A model's answer is recorded next to its question as advice; it never fails the run.
"""
from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

from check_api import Finding

QUESTION_PROMPT = ("Answer the question about the file below in at most three sentences, then end with "
                   "a line 'VERDICT: pass' or 'VERDICT: fail'.\n\nQuestion: {question}\n\nFile {path}:\n{content}")


def ask(url: str, model: str, key: str | None, prompt: str, timeout: int) -> str:
    request = urllib.request.Request(
        url.rstrip("/") + "/chat/completions",
        data=json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0}).encode(),
        headers={"Content-Type": "application/json", **({"Authorization": f"Bearer {key}"} if key else {})})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read())["choices"][0]["message"]["content"].strip()


def endpoint(backend: str, settings: dict) -> tuple[str, str, str | None] | str:
    """The (url, model, key) of a model backend, or the reason it cannot be used."""
    prefix = "READER_ERGONOMICS_LOCAL" if backend == "local" else "READER_ERGONOMICS_API"
    if backend == "api" and not settings.get("api", {}).get("enabled", False):
        return "the api backend is paid and is off in config.toml ([judgment.api] enabled = false)"
    url, model = os.environ.get(f"{prefix}_URL"), os.environ.get(f"{prefix}_MODEL")
    if not url or not model:
        return f"{prefix}_URL and {prefix}_MODEL are not set"
    return url, model, os.environ.get(f"{prefix}_KEY") if backend == "api" else None


def dispatch(root: Path, findings: list[Finding], backend: str, settings: dict) -> str:
    """Send the judgment findings to the backend; return one line saying what happened."""
    questions = [finding for finding in findings if finding.kind == "judgment"]
    output = root / "checks" / "out" / "needs-judgment.md"
    if backend == "none" or not questions:
        if not questions and output.exists():
            output.unlink()  # a file left by an earlier run would ask questions that no longer apply
        return f"judgment: {len(questions)} question(s), backend {backend}"
    answers, note = {}, ""
    if backend in ("local", "api"):
        target = endpoint(backend, settings)
        if isinstance(target, str):
            note, backend = f" ({target}; fell back to flag)", "flag"
        else:
            url, model, key = target
            for finding in questions:
                content = (root / finding.path).read_text(encoding="utf-8", errors="replace") if (root / finding.path).is_file() else ""
                prompt = QUESTION_PROMPT.format(question=finding.message, path=finding.path, content=content[:20000])
                try:
                    answers[finding] = ask(url, model, key, prompt, settings.get("timeout_seconds", 120))
                except Exception as error:  # an unreachable model leaves the question open, it does not crash
                    answers[finding] = f"(no answer: {error.__class__.__name__})"
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Questions for judgment", "", f"Backend: {backend}. Answer each one; a model's answer is advice.", ""]
    for finding in questions:
        lines.append(f"- [ ] `{finding.path}` ({finding.check}): {finding.message}")
        if finding in answers:
            lines += ["", "  " + answers[finding].replace("\n", "\n  "), ""]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return f"judgment: {len(questions)} question(s) written to checks/out/needs-judgment.md{note}"
