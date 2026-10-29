"""Readable measure: the site's stylesheet sets body text inside the measured ranges.

In each stylesheet listed in config, a `max-width` in `ch` must lie between 45 and 75
characters, a `font-size` must be at least 16 px (a rem counts 16 px), and a unitless
`line-height` at least 1.5. Rules for code, tables and captions are not body text, and a
repository with no stylesheet has nothing to check.

Exact for the declared values; the rendered line still depends on the face. Time O(stylesheet).
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import Finding

NAME = "readable-measure"
EXACT = True
RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("readable_measure", {})
    low, high = settings.get("measure_ch", [45, 75])
    findings = []
    for name in settings.get("stylesheets", []):
        path = root / name
        if not path.is_file():
            findings.append(Finding(NAME, name, 0, "a stylesheet listed in config does not exist, so it was not measured",
                                    "warning"))
            continue
        css = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.S)
        for selector, body in RULE.findall(css):
            if re.search(r"\b(code|pre|table|caption|figcaption)\b", selector):
                continue
            for value in re.findall(r"max-width:\s*([\d.]+)ch", body):
                if not low <= float(value) <= high:
                    findings.append(Finding(NAME, name, 0, f"{selector.strip()}: a measure of {value}ch, outside {low} to {high}"))
            for value, unit in re.findall(r"font-size:\s*([\d.]+)(px|rem)", body):
                pixels = float(value) * (16 if unit == "rem" else 1)
                if pixels < settings.get("min_font_px", 16):
                    findings.append(Finding(NAME, name, 0, f"{selector.strip()}: body text of {pixels:g} px, under 16"))
            for value in re.findall(r"line-height:\s*([\d.]+)\s*;", body):
                if float(value) < settings.get("min_line_height", 1.5):
                    findings.append(Finding(NAME, name, 0, f"{selector.strip()}: line height {value}, under 1.5"))
    return findings
