#!/usr/bin/env python3
"""Populate the English edition from the translated manuscripts.

This edition is assembled, not transformed in place. The Chinese build under
book/ is left untouched: its preprocessing regexes match Chinese headings and
its helper scripts parse the Chinese manuscripts, so teaching that pipeline to
emit English means breaking it for its actual purpose. Instead the translated
prose and the re-rendered figures are copied here, and this directory carries
its own preamble and build script.

Usage: cd book-en && python3 assemble.py
"""
from pathlib import Path
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EN = HERE / "tools" / "manuscripts-en"
ZH = ROOT / "manuscripts"
IMAGES = HERE / "images"

# Two figures cannot be regenerated in English; see README.md.
KNOWN_CHINESE = {"figure-6-context-dependency.pdf", "figure-7-ub-round-trip.pdf"}


def chapter_files():
    # 00 is the preface; it is emitted as introduction.md, matching the layout
    # of the English edition of the companion AI Agent book.
    return sorted(EN.glob("[0-9][0-9]-*.md"))


def out_name(number: int) -> str:
    return "introduction.md" if number == 0 else f"chapter{number:02d}.md"


def convert(source: Path, number: int) -> str:
    text = source.read_text(encoding="utf-8")

    # Headings carry no manual numbering; the document class numbers them.
    text = re.sub(r"^#\s+Chapter\s*\d+[:.\s]\s*", "# ", text, count=1, flags=re.M)

    # The preface is front matter: mark its headings unnumbered so it does not
    # consume chapter 1 and shift every chapter that follows, matching what
    # book/build_pdf.py does for the Chinese edition.
    if number == 0:
        text = re.sub(r"^(#\s+.+)$", r"\1 {.unnumbered}", text, count=1, flags=re.M)
        text = re.sub(r"^(##\s+.+)$", r"\1 {.unnumbered}", text, flags=re.M)

    # An image whose alt text is repeated as the following italic line is a
    # figure caption; merge the two so pandoc emits one \caption.
    text = re.sub(r"!\[[^\n]*\]\(([^)]+)\)\s*\n\s*\*([^\n]+)\*",
                  lambda m: f"![{m[2]}]({m[1]})", text)

    # Point every figure at the copy in images/, preferring the vector PDF that
    # the chapter build emits alongside the SVG.
    def image(m):
        alt, target = m[1], m[2]
        src = (ZH / target).resolve()
        chosen = src.with_suffix(".pdf")
        if not chosen.exists():
            chosen = src.with_suffix(".png")
        if not chosen.exists():
            raise FileNotFoundError(src)
        IMAGES.mkdir(exist_ok=True)
        shutil.copy2(chosen, IMAGES / chosen.name)
        return f"![{alt}](images/{chosen.name})"
    text = re.sub(r"!\[([^\n]*)\]\(([^)]+)\)", image, text)

    # Relative links point into the repository; make them absolute so the
    # delivered PDF resolves them.
    def link(m):
        target = m[2]
        if re.match(r"[a-z]+:|#", target):
            return m[0]
        rel = target.lstrip("./")
        return f"[{m[1]}](https://github.com/bojieli/ai-infra-book/blob/main/{rel})"
    text = re.sub(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)", link, text)

    return text


def main() -> None:
    written = []
    for source in chapter_files():
        number = int(source.name[:2])
        out = HERE / out_name(number)
        out.write_text(convert(source, number), encoding="utf-8")
        written.append(out.name)
    figures = sorted(IMAGES.glob("*")) if IMAGES.exists() else []
    print(f"assembled {len(written)} chapter(s): {', '.join(written)}")
    print(f"{len(figures)} figure file(s) in images/")

    # Figures are copied out of manuscripts/, which holds the Chinese originals
    # unless the translated build scripts are swapped in. Running this script at
    # the wrong moment therefore produces a silently Chinese edition, which has
    # happened twice. Check what was actually copied and fail loudly instead.
    pointers, chinese = [], []
    for f in figures:
        head = f.open("rb").read(64)
        if head.startswith(b"version https://git-lfs"):
            pointers.append(f.name)
            continue
        out = subprocess.run(["pdftotext", str(f), "-"], capture_output=True, text=True).stdout
        if any("\u4e00" <= c <= "\u9fff" for c in out) and f.name not in KNOWN_CHINESE:
            chinese.append(f.name)
    if pointers or chinese:
        if pointers:
            print(f"\nERROR: {len(pointers)} figure(s) are Git LFS pointers, not files: "
                  f"{pointers[:4]}")
            print("  run tools/lfs_fetch.py on them, then re-run this script")
        if chinese:
            print(f"\nERROR: {len(chinese)} figure(s) still contain Chinese: {chinese[:4]}")
            print("  the translated figure scripts were not in place when these were")
            print("  rendered; re-render the chapters, then re-run this script")
        raise SystemExit(1)
    print(f"all figures check out ({len(KNOWN_CHINESE)} known exceptions allowed)")
    if not written:
        print("nothing to assemble — translate a chapter into manuscripts-en/ first")


if __name__ == "__main__":
    main()
