"""Shared reading of SVG figures for the figure checks: which files, and the colours they declare.

Not a check: it defines no NAME. Colours are read from attributes and from CSS rules in a <style> element; a rule
inside @media (prefers-color-scheme: dark) belongs to the dark scheme. Time O(text).
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import files_in_scope, matches_any

HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
NAMED = {"black": "#000000", "white": "#ffffff", "gray": "#808080", "grey": "#808080", "red": "#ff0000",
         "green": "#008000", "blue": "#0000ff", "lightgray": "#d3d3d3", "lightgrey": "#d3d3d3"}
NONE = {"none", "transparent", "currentcolor", "inherit", ""}
STYLE = re.compile(r"<style[^>]*>(.*?)</style>", re.DOTALL)
DARK = re.compile(r"@media[^{]*prefers-color-scheme:\s*dark[^{]*\{((?:[^{}]*\{[^{}]*\})*)[^{}]*\}", re.DOTALL)
RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")
ELEMENT = re.compile(r"<(?!text\b|tspan\b|/)(\w+)\b([^>]*)>")
ATTRIBUTE = re.compile(r'\b(stroke|fill)="([^"]*)"')


def figures(root: Path, config: dict, exempt: list[str]) -> list[str]:
    """Every SVG file in scope that is not exempt."""
    return [path for path in files_in_scope(root, config, {".svg"}) if not matches_any(path, exempt)]


def colour(value: str) -> str | None:
    """A colour as #rrggbb, #rrggbbaa kept as is; None for no colour or one this module cannot read."""
    value = value.strip().lower()
    if value in NONE or value.startswith("url("):
        return None
    if value in NAMED:
        return NAMED[value]
    match = HEX.match(value)
    if not match:
        return None
    digits = match.group(1)
    return "#" + "".join(c * 2 for c in digits) if len(digits) == 3 else "#" + digits


def declarations(body: str) -> dict:
    return {key.strip(): val.strip() for key, _, val in (part.partition(":") for part in body.split(";")) if key.strip()}


def css_pairs(svg: str) -> list[tuple[str, str | None, str | None]]:
    """(scheme, stroke, fill) for each CSS rule that sets a stroke; scheme is 'light' or 'dark'."""
    pairs = []
    for style in STYLE.findall(svg):
        dark_blocks = DARK.findall(style)
        light = DARK.sub("", style)
        for scheme, text in [("light", light)] + [("dark", block) for block in dark_blocks]:
            for _, body in RULE.findall(text):
                rule = declarations(body)
                if "stroke" in rule:
                    pairs.append((scheme, rule["stroke"], rule.get("fill")))
    return pairs


def attribute_pairs(svg: str) -> list[tuple[int, str, str | None]]:
    """(line, stroke, fill) for each element outside text that sets a stroke attribute."""
    pairs = []
    for element in ELEMENT.finditer(svg):
        found = dict(ATTRIBUTE.findall(element.group(2)))
        if "stroke" in found:
            pairs.append((svg.count("\n", 0, element.start()) + 1, found["stroke"], found.get("fill")))
    return pairs
