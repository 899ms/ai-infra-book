#!/bin/bash
# Build the English edition as a single PDF (ElegantBook, cyan theme).
#
# Requirements: pandoc, and either xelatex (TeX Live / MacTeX) or tectonic.
# The ElegantBook class and layout filter are reused from ../book/.
# Run assemble.py first if the chapters or images are out of date.
#
# Usage: cd book-en && bash build_pdf.sh

set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
ROOT="$(cd .. && pwd)"

# The book is large enough to exhaust XeTeX's default main memory during page
# output. main_memory is fixed when the format is dumped, but extra_mem_top and
# extra_mem_bot extend an existing format at runtime.
export extra_mem_top=8000000
export extra_mem_bot=8000000
# The mac-only monospace font is probed with \IfFontExistsTF in preamble.tex.
# Without this, kpathsea spawns METAFONT to build a Menlo.tfm (slow, noisy and
# always unsuccessful) before the DejaVu Sans Mono fallback engages.
export MKTEXTFM=0
# elegantbook.cls, layout.lua and the imported series template live in ../book/.
export TEXINPUTS="$ROOT/book:$ROOT/book/template:"

NAME="AI-Infra-Book-EN"
CHAPTERS=(introduction.md)
for n in 01 02 03 04 05 06 07 08 09 10 11 12; do
    [ -f "chapter$n.md" ] && CHAPTERS+=("chapter$n.md")
done
if [ ${#CHAPTERS[@]} -le 1 ]; then
    echo "No chapters found. Run: python3 assemble.py" >&2
    exit 1
fi
echo "Building from ${#CHAPTERS[@]} files..."

pandoc "${CHAPTERS[@]}" \
    -o "$NAME.tex" \
    --from markdown+lists_without_preceding_blankline \
    --to=latex --standalone \
    --top-level-division=chapter \
    --toc --toc-depth=2 --number-sections \
    --lua-filter="$ROOT/book/layout.lua" \
    -V documentclass=elegantbook \
    -V classoption=lang=en \
    -V classoption=nofont \
    -V classoption=cyan \
    -V classoption=device=normal \
    -V author="Bojie Li" \
    --metadata title-meta="Understanding AI Infra: Quantitative Analysis and System Design" \
    --metadata author-meta="Bojie Li (English translation)" \
    -H preamble.tex \
    --highlight-style=kate \
    --columns=100

if command -v xelatex >/dev/null 2>&1; then
    # Canonical path. Three passes settle the table of contents and references.
    for _ in 1 2 3; do
        xelatex -interaction=nonstopmode -halt-on-error -file-line-error "$NAME.tex"
    done
elif command -v tectonic >/dev/null 2>&1; then
    # Local fallback. The class loads biblatex unconditionally, so a biber
    # control file is written and tectonic shells out to biber; that fails
    # unless the system biber matches the biblatex tectonic bundles. This
    # edition cites nothing, so biblatex is marked as already loaded and its
    # entry points are stubbed, after which no control file is written and the
    # bibliography tool is never invoked. xurl reads two penalty counters that
    # biblatex would normally define, so those are supplied here too.
    python3 - "$NAME.tex" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1]); s = p.read_text()
stub = r"""\makeatletter
\@namedef{ver@biblatex.sty}{9999/01/01 stubbed: this edition cites nothing}
\makeatother
% xurl reads these as LaTeX counters, which biblatex would normally declare.
\newcounter{biburllcpenalty}\newcounter{biburlucpenalty}\newcounter{biburlnumpenalty}
\providecommand{\addbibresource}[2][]{}
\providecommand{\printbibliography}[1][]{}
\providecommand{\defbibheading}[3][]{}
\providecommand{\ExecuteBibliographyOptions}[2][]{}
"""
i = s.index("\\documentclass")
p.write_text(s[:i] + stub + s[i:])
PY
    mkdir -p build
    # One "Option clash for package biblatex" is expected here and is
    # harmless: the class asks for options on a package the stub has already
    # marked as loaded. Nothing in this edition cites anything.
    tectonic -X compile "$NAME.tex" --outdir build -Z continue-on-errors
    mv "build/$NAME.pdf" "$NAME.pdf"
else
    echo "Neither xelatex nor tectonic found." >&2
    exit 1
fi

echo "Wrote $HERE/$NAME.pdf"
