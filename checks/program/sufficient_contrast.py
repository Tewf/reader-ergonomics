"""Sufficient contrast: text and background colours declared together reach a WCAG ratio of 4.5:1.

In each stylesheet listed in config, a rule that declares a text colour (`color`, or a
`--…-color` property) and a background (`background`, `background-color`, or a `--…-bg`
property) is measured with the WCAG 2.2 formula. A colour given as `var(--name, #hex)` is read
from its fallback. Below 4.5:1 fails.

Exact for colours declared in the same rule. Time O(stylesheet).
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import Finding

NAME = "sufficient-contrast"
EXACT = True
RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")
DECLARATION = re.compile(r"([\w-]+)\s*:\s*([^;]+);")
HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")


def luminance(hex_colour: str) -> float:
    digits = hex_colour if len(hex_colour) == 6 else "".join(character * 2 for character in hex_colour)
    channels = [int(digits[index:index + 2], 16) / 255 for index in (0, 2, 4)]
    linear = [value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def ratio(first: str, second: str) -> float:
    lighter, darker = sorted((luminance(first), luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("sufficient_contrast", {})
    findings = []
    for name in settings.get("stylesheets", []):
        path = root / name
        if not path.is_file():
            continue
        css = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.S)
        for selector, body in RULE.findall(css):
            texts, backgrounds = [], []
            for prop, value in DECLARATION.findall(body):
                colour = HEX.search(value)
                if not colour:
                    continue
                if prop == "color" or (prop.startswith("--") and prop.endswith("-color")):
                    texts.append((prop, colour.group(1)))
                elif prop in ("background", "background-color") or (prop.startswith("--") and prop.endswith("-bg")):
                    backgrounds.append(colour.group(1))
            for prop, text in texts:
                for background in backgrounds:
                    measured = ratio(text, background)
                    if measured < settings.get("min_ratio", 4.5):
                        findings.append(Finding(NAME, name, 0, f"{selector.strip()}: {prop} #{text} on #{background} "
                                                f"is {measured:.2f}:1, under 4.5:1"))
    return findings
