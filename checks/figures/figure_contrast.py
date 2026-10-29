"""Figure contrast: the lines of an SVG figure have at least `min_ratio` contrast against what lies next to them.

Each stroke an SVG declares, as an attribute or in a CSS rule, is compared with the page behind it (`page`, or
`page_dark` for a rule inside a dark-scheme media query) and with the fill of the same element or rule. A colour
with an alpha channel (#rrggbbaa) is reported as such: some renderers drop it and the line vanishes. Text is left to
sufficient-contrast (WCAG 1.4.11; principle sufficient contrast).

Exact for the colours a file declares; a colour set by a class this module cannot resolve is not checked.
Time O(text).
"""
from __future__ import annotations

from pathlib import Path

from figures._svg import attribute_pairs, colour, css_pairs, figures
from framework.check_api import Finding

NAME = "figure-contrast"
EXACT = True


def luminance(hex_colour: str) -> float:
    channels = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def ratio(a: str, b: str) -> float:
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def problems(stroke_value: str, fill_value: str | None, page: str, minimum: float) -> list[str]:
    stroke = colour(stroke_value)
    if stroke is None:
        return []
    if len(stroke) == 9:
        return [f"stroke {stroke_value} has an alpha channel, which some renderers drop: write it solid"]
    found = []
    for name, against in (("the page", page), ("its fill", colour(fill_value or ""))):
        if against and len(against) == 7 and against != stroke and ratio(stroke, against) < minimum:  # same: a solid shape
            found.append(f"stroke {stroke_value} has {ratio(stroke, against):.2f}:1 against {name} ({against}), "
                         f"under {minimum}:1")
    return found


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("figure_contrast", {})
    minimum = settings.get("min_ratio", 3.0)
    pages = {"light": settings.get("page", "#ffffff"), "dark": settings.get("page_dark", "#1a1a20")}
    findings = []
    for path in figures(root, config, settings.get("exempt", [])):
        svg = (root / path).read_text(encoding="utf-8", errors="replace")
        for scheme, stroke, fill in css_pairs(svg):
            findings += [Finding(NAME, path, 1, f"{scheme} scheme: {message}")
                         for message in problems(stroke, fill, pages[scheme], minimum)]
        for line, stroke, fill in attribute_pairs(svg):
            findings += [Finding(NAME, path, line, message) for message in problems(stroke, fill, pages["light"], minimum)]
    return findings
