"""Sufficient contrast: every text colour reaches a WCAG ratio of 4.5:1 on the background it sits on.

In each stylesheet listed in config, a text colour (`color`, or a `--…-color` property) is
measured with the WCAG 2.2 formula against a background (`background`, `background-color`, or a
`--…-bg` property). A `var(--name)` takes the value its theme gives the variable, and its
fallback only when no theme declares it. A theme is the variables of `:root` or `html`, alone
or with the variables a block redefines over them: a dark scheme, a `[data-theme]` selector.

- A text colour and a background declared in the same rule are measured in every theme; a
  pair under the ratio is an error.
- A text colour declared alone inherits its background from a parent the stylesheet cannot
  name. It is measured against the page (the background of `html`, `body` or `:root`) and
  against each surface named in config (`surfaces`: the selectors that paint a slide, a card, a
  panel). A pair under the ratio is a warning, one per colour pair with the rules that use it:
  the text may never sit on that surface. Only the repository knows its surfaces, so none is
  assumed.

Exact for colours declared in the same rule; heuristic for inherited backgrounds. A colour is
read as hex, or as `white` or `black`; any other form is skipped. The rendered page is not
measured. Time O(rules x themes x surfaces).
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import Finding

NAME = "sufficient-contrast"
EXACT = True
DECLARATION = re.compile(r"([\w-]+)\s*:\s*([^;]+);")
HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
NAMED = {"white": "ffffff", "black": "000000"}
WORD = re.compile(r"\b(white|black)\b", re.IGNORECASE)
VAR = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*))?\)")
ROOT = re.compile(r"^(?::root|html)(?:\[[^\]]*\]|:not\([^)]*\))*$")
PAGE = {"html", "body", ":root"}
SKIPPED_BLOCKS = ("@keyframes", "@-webkit-keyframes", "@font-face")


def luminance(hex_colour: str) -> float:
    digits = hex_colour if len(hex_colour) == 6 else "".join(character * 2 for character in hex_colour)
    channels = [int(digits[index:index + 2], 16) / 255 for index in (0, 2, 4)]
    linear = [value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def ratio(first: str, second: str) -> float:
    lighter, darker = sorted((luminance(first), luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def rules(css: str) -> list[tuple[tuple[str, ...], str, list[tuple[str, str]]]]:
    """(enclosing at-rules, selector, declarations) of every rule; keyframes and font faces are skipped."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    found, stack, start = [], [], 0
    for index, character in enumerate(css):
        if character == "{":
            stack.append((css[start:index].rsplit(";", 1)[-1].strip(), index + 1))
            start = index + 1
        elif character == "}" and stack:
            prelude, opened = stack.pop()
            body = css[opened:index]
            context = tuple(outer for outer, _ in stack)
            if not prelude.startswith("@") and "{" not in body and not any(outer.startswith(SKIPPED_BLOCKS) for outer in context):
                found.append((context, " ".join(prelude.split()), DECLARATION.findall(body + ";")))
            start = index + 1
    return found


def themes(parsed) -> list[tuple[str, tuple[str, ...], dict[str, str]]]:
    """(label, at-rules it applies under, variables) of the base theme and of every block that redefines it."""
    base, overrides = {}, {}
    for context, selector, declarations in parsed:
        variables = {prop: value.strip() for prop, value in declarations if prop.startswith("--")}
        for part in (part.strip() for part in selector.split(",")):
            if not variables or not ROOT.match(part):
                continue
            if not context and part in (":root", "html"):
                base.update(variables)
            else:
                overrides.setdefault((context, part), {}).update(variables)
    return [("", (), base)] + [(" ".join(context + (part,)), context, {**base, **variables})
                               for (context, part), variables in overrides.items()]


def colour(value: str, variables: dict[str, str]) -> str | None:
    """The hex digits a value resolves to in a theme, or None when it is not a colour this check reads."""
    for _ in range(10):  # variables refer to variables; ten levels is far past any real stylesheet
        resolved = VAR.sub(lambda match: variables.get(match.group(1), match.group(2) or ""), value)
        if resolved == value:
            break
        value = resolved
    found = HEX.search(value)
    if found:
        return found.group(1)
    named = WORD.search(value)
    return NAMED[named.group(1).lower()] if named else None


def is_text(prop: str) -> bool:
    return prop == "color" or (prop.startswith("--") and prop.endswith("-color"))


def is_background(prop: str) -> bool:
    return prop in ("background", "background-color") or (prop.startswith("--") and prop.endswith("-bg"))


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("sufficient_contrast", {})
    minimum, surfaces, findings, seen = settings.get("min_ratio", 4.5), set(settings.get("surfaces", [])), [], set()

    def report(name: str, message: str, kind: str) -> None:
        if message not in seen:
            seen.add(message)
            findings.append(Finding(NAME, name, 0, message, kind))

    for name in settings.get("stylesheets", []):
        path = root / name
        if not path.is_file():
            continue
        parsed = rules(path.read_text(encoding="utf-8"))
        for label, theme_context, variables in themes(parsed):
            where = f" (theme {label})" if label else ""
            alone, grounds = [], []
            for context, selector, declarations in parsed:
                if context and context != theme_context:
                    continue
                texts = [(prop, found) for prop, value in declarations if is_text(prop) and (found := colour(value, variables))]
                backgrounds = [found for prop, value in declarations if is_background(prop) and (found := colour(value, variables))]
                for prop, text in texts:
                    for background in backgrounds:
                        measured = ratio(text, background)
                        if measured < minimum:
                            report(name, f"{selector}: {prop} #{text} on #{background} is {measured:.2f}:1, under "
                                         f"{minimum}:1{where}", "error")
                if backgrounds and any(part.strip() in PAGE | surfaces for part in selector.split(",")):
                    grounds.append((selector, backgrounds[0]))
                elif texts and not backgrounds:
                    alone += [(selector, prop, text) for prop, text in texts]
            pairs: dict[tuple[str, str], tuple[list[str], list[str]]] = {}
            for selector, prop, text in alone:
                for ground, background in grounds:
                    if ratio(text, background) < minimum:
                        users, places = pairs.setdefault((text.lower(), background.lower()), ([], []))
                        users += [selector] if selector not in users else []
                        places += [ground] if ground not in places else []
            for (text, background), (users, places) in pairs.items():
                named = ", ".join(users[:4]) + (f" and {len(users) - 4} more" if len(users) > 4 else "")
                report(name, f"#{text} ({named}) on {' or '.join(places)} (#{background}) is "
                             f"{ratio(text, background):.2f}:1, under {minimum}:1, if it sits there{where}", "warning")
    return findings
