"""Render a Graphviz source to the SVG beside it, stamped with the hash of the source, and refresh its folded copies.

Usage: python3 checks/figures/render_figure.py FIGURE.dot [...]

Writes FIGURE.svg next to FIGURE.dot, with `<!-- source-sha256: H -->` after the XML prolog, H being the SHA-256 of
the .dot file's bytes; the check figure-source compares the two. Written in the presentations extension. Then every Markdown page of the repository that
embeds FIGURE.svg on a line of its own gets the source folded under the image, in a <details> block, replacing the
copy already there; figure-source-inline compares that copy with the file. Needs Graphviz's `dot`
on the PATH, and runs from inside the repository.
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

IMAGE = re.compile(r"^!\[[^\]]*\]\(([^)\s#]+\.svg)\)[ \t]*$", re.MULTILINE)
FOLDED = re.compile(r"\s*<details>\s*<summary>[^<]*</summary>\s*```dot[ \t]*\n(.*?)\n```\s*</details>", re.DOTALL)


def render(source: Path) -> Path:
    svg = subprocess.run(["dot", "-Tsvg", str(source)], capture_output=True, text=True, check=True).stdout
    stamp = f"<!-- source-sha256: {hashlib.sha256(source.read_bytes()).hexdigest()} -->\n"
    head, _, rest = svg.partition("?>\n") if svg.startswith("<?xml") else ("", "", svg)
    target = source.with_suffix(".svg")
    target.write_text((head + "?>\n" if head else "") + stamp + rest, encoding="utf-8")
    return target


def fold(source: Path) -> list[Path]:
    """Put the source under every image of its SVG, in the pages of the repository; return the pages changed."""
    top = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip())
    listed = subprocess.run(["git", "-C", str(top), "ls-files", "*.md", "*.qmd"], capture_output=True, text=True).stdout.split()
    changed = []
    for name in listed:
        page = top / name
        text = page.read_text(encoding="utf-8")
        out, last = [], 0
        for image in IMAGE.finditer(text):
            if (page.parent / image.group(1)).resolve() != source.with_suffix(".svg").resolve():
                continue
            summary = "Source Graphviz" if name.endswith(".fr.md") else "Graphviz source"
            folded = FOLDED.match(text, image.end())
            out += [text[last:image.end()],
                    f"\n\n<details>\n<summary>{summary}</summary>\n\n```dot\n{source.read_text(encoding='utf-8').strip()}\n```\n\n</details>"]
            last = folded.end() if folded else image.end()
        if out:
            new = "".join(out) + text[last:]
            if new != text:
                page.write_text(new, encoding="utf-8")
                changed.append(page)
    return changed


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for name in sys.argv[1:]:
        print(render(Path(name)))
        for page in fold(Path(name)):
            print(f"  folded into {page}")
