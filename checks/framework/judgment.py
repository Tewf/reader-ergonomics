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

Answers are kept in the file named by `[judgment] answers` (by default `checks/judgments.toml`),
committed with the repository, so a question answered once is not asked on every run. Each
answer carries the fingerprint of its file when it was given; once the file changes, the question
is asked again. The open questions are also written as entries ready to fill in, in
`checks/out/judgments-to-answer.toml`.
"""
from __future__ import annotations

import hashlib
import json
import os
import tomllib
import urllib.request
from pathlib import Path

from framework.check_api import Finding

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


def fingerprint(root: Path, path: str) -> str:
    """The first 12 hex characters of the file's SHA-256, or "" when the path is not a file."""
    file = root / path
    return hashlib.sha256(file.read_bytes()).hexdigest()[:12] if file.is_file() else ""


def answered(root: Path, settings: dict) -> set[tuple[str, str, str, str]]:
    """(check, path, question, fingerprint) of every answer given and not left empty."""
    file = root / settings.get("answers", "checks/judgments.toml")
    if not file.is_file():
        return set()
    entries = tomllib.loads(file.read_text(encoding="utf-8")).get("answer", [])
    return {(entry["check"], entry["path"], entry["question"], entry["file"]) for entry in entries
            if str(entry.get("answer", "")).strip()}


def to_answer(root: Path, questions: list[Finding]) -> str:
    """The open questions as entries of the answers file, each with its fingerprint and an empty answer."""
    entries = []
    for finding in questions:
        entries += ["[[answer]]", f"check = {json.dumps(finding.check)}", f"path = {json.dumps(finding.path)}",
                    f"question = {json.dumps(finding.message, ensure_ascii=False)}",
                    f"file = {json.dumps(fingerprint(root, finding.path))}", 'answer = ""', ""]
    return "\n".join(entries)


def dispatch(root: Path, findings: list[Finding], backend: str, settings: dict) -> str:
    """Send the judgment findings to the backend; return one line saying what happened."""
    asked = [finding for finding in findings if finding.kind == "judgment"]
    known = answered(root, settings)
    questions = [finding for finding in asked
                 if (finding.check, finding.path, finding.message, fingerprint(root, finding.path)) not in known]
    done = f", {len(asked) - len(questions)} answered in {settings.get('answers', 'checks/judgments.toml')}" if known else ""
    output = root / "checks" / "out" / "needs-judgment.md"
    stub = output.with_name("judgments-to-answer.toml")
    if backend == "none" or not questions:
        for left in (output, stub):
            if not questions and left.exists():
                left.unlink()  # a file left by an earlier run would ask questions that no longer apply
        return f"judgment: {len(asked)} question(s){done}, backend {backend}"
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
    stub.write_text(to_answer(root, questions), encoding="utf-8")
    return f"judgment: {len(asked)} question(s){done}, {len(questions)} written to checks/out/needs-judgment.md{note}"
