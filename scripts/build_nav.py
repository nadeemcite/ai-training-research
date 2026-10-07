"""Add prev/next navigation to every study reading. Safe to re-run.

Usage: uv run scripts/build_nav.py

Order: study/README.md -> ch01/README.md -> ch01/01-*.md ... -> ch02/README.md -> ...
Each chapter folder uses README.md as its overview, so GitHub renders it when the folder is opened.
Nav blocks live between <!-- nav:top --> / <!-- nav:bottom --> markers and are replaced on each run.
"""

import os
import re
from pathlib import Path

STUDY = Path(__file__).resolve().parent.parent / "study"
TOP = re.compile(r"<!-- nav:top -->.*?<!-- /nav:top -->\n\n", re.S)
BOTTOM = re.compile(r"\n*<!-- nav:bottom -->.*?<!-- /nav:bottom -->\n?", re.S)
SYLLABUS = re.compile(r"<!-- nav:start -->.*?<!-- /nav:start -->\n\n", re.S)


def title(path: Path) -> str:
    for line in path.read_text().splitlines():
        if line.startswith("# "):
            return line[2:].strip().replace("|", "\\|")
    return path.stem


def link(src: Path, dst: Path, text: str) -> str:
    return f"[{text}]({Path(os.path.relpath(dst, src.parent)).as_posix()})"


def linkify_overview(text: str) -> str:
    """`01-concept.md` -> [01-concept](01-concept.md) and `lab_x.py` -> [`lab_x.py`](lab_x.py) in tables."""
    text = re.sub(r"^\| `(\d\d-[\w-]+)\.md` \|", r"| [\1](\1.md) |", text, flags=re.M)
    return re.sub(r"(?<!\[)`(lab_\w+\.py)`", r"[`\1`](\1)", text)


def main() -> None:
    chapters = sorted(p for p in STUDY.iterdir() if p.is_dir() and re.match(r"\d\d-", p.name))
    for ch in chapters:  # one-time migration: 00-overview.md -> README.md
        if (ch / "00-overview.md").exists():
            (ch / "00-overview.md").rename(ch / "README.md")

    home = STUDY / "README.md"
    planned = len(re.findall(r"^\| \d\d \|", home.read_text(), flags=re.M))  # syllabus rows
    pages = [home]
    for ch in chapters:
        pages += [ch / "README.md", *sorted(ch.glob("[0-9][0-9]-*.md"))]

    for i, page in enumerate(pages[1:], start=1):
        ch = page.parent
        readings = sorted(ch.glob("[0-9][0-9]-*.md"))
        overview = ch / "README.md"
        num = int(ch.name[:2])  # folder prefix, so gaps in the syllabus are fine
        crumbs = [link(page, home, "🏠 Course")]
        if page == overview:
            crumbs.append(f"**Topic {num:02d} / {planned:02d}**")
            crumbs.append("▶️ " + link(page, readings[0], "Pehli reading shuru karo"))
        else:
            crumbs.append(link(page, overview, title(overview)))
            crumbs.append(f"Reading {readings.index(page) + 1} / {len(readings)}")
        top = f"<!-- nav:top -->\n{' › '.join(crumbs)}\n<!-- /nav:top -->\n\n"

        prev_page = pages[i - 1]
        nxt = pages[i + 1] if i + 1 < len(pages) else None
        prev_cell = "⬅️ " + link(page, prev_page, title(prev_page))
        mid_cell = "📚 " + link(page, overview, f"Topic {num:02d} overview")
        next_cell = (link(page, nxt, title(nxt)) + " ➡️") if nxt else (
            link(page, home, "Course home") + " 🏁 *(agle topics jald aa rahe hain)*")
        bottom = ("\n\n<!-- nav:bottom -->\n---\n\n| ⬅️ Pichla | 📚 Topic | Agla ➡️ |\n|:--|:-:|--:|\n"
                  f"| {prev_cell} | {mid_cell} | {next_cell} |\n<!-- /nav:bottom -->\n")

        text = BOTTOM.sub("", TOP.sub("", page.read_text())).rstrip()
        text = re.sub(r"\n+---\n+✅ \*\*Topics? [^\n]*complete![^\n]*$", "", text)  # old manual footers
        if page == overview:
            text = linkify_overview(text)
        page.write_text(top + text + bottom)

    # Course home: link finished chapters in the syllabus + a start button.
    text = SYLLABUS.sub("", home.read_text())
    for ch in chapters:
        num = int(ch.name[:2])
        text = re.sub(rf"^\| {num:02d} \| (?!\[)([^|]+?) \|",
                      lambda m, ch=ch: f"| {num:02d} | [{m.group(1)}]({ch.name}/) |", text, flags=re.M)
    start = (f"<!-- nav:start -->\n▶️ **Shuru karo:** {link(home, chapters[0] / 'README.md', title(chapters[0] / 'README.md'))}"
             "\n<!-- /nav:start -->\n\n")
    text = text.replace("## Is classroom ka rule", start + "## Is classroom ka rule", 1)
    home.write_text(text)
    print(f"nav updated: {len(pages) - 1} pages across {len(chapters)} chapters")


if __name__ == "__main__":
    main()
