# English edition

An English translation of the book, kept alongside the Chinese source rather
than replacing it. Nothing under `manuscripts/` or `book/` is modified — this
directory carries its own chapters, figures, preamble and build script.

Thirteen files are translated: the preface (`introduction.md`) and chapters 1
through 12.

## Layout

| Path | Contents |
| --- | --- |
| `introduction.md`, `chapter01.md` … `chapter12.md` | translated chapters |
| `images/` | figures re-rendered with English labels (Git LFS) |
| `preamble.tex` | loads the shared series preamble from `../book/` with the CJK font commands made inert |
| `cover.tex` | the series cover drawing with English title, author and edition stamp |
| `build_pdf.py`, `build_pdf.sh` | Pandoc + XeLaTeX build, mirroring `book/build_pdf.py` |
| `assemble.py` | rebuilds the chapters and copies figures from `tools/` |
| `tools/` | translation tooling, glossary, and the translated figure scripts |

## Building

```bash
git lfs pull --include="book-en/images/**" --exclude=""
bash book-en/build_pdf.sh                       # writes book-en/AI-Infra-Book-EN.pdf
bash book-en/build_pdf.sh --output-dir ../build/pdf-en --source-ref "$(git rev-parse HEAD)"
```

Requires `pandoc`, `xelatex`, and the ElegantBook class from `book/`; the
fonts are the same as for the Chinese edition (see `book/README.md`). Besides
the PDF, the build writes `AI-Infra-Book-EN-build.json` (sources, figure count,
layout and font warnings) and a cover PNG. `--source-ref` pins the repository
links inside the PDF to one commit.

GitHub Actions builds this edition next to the Chinese one on every push and
pull request (`.github/workflows/book-site.yml`, job `pdf (en)`), validates it
with `book/check_ci_pdf.py --edition en` (all twelve chapters, no missing
glyphs, expected fonts), and publishes it in each Release as
`AI-Infra-Book-EN.pdf`. Latest build:
<https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book-EN.pdf>.

## How the translation is checked

Each chapter is translated in sections and compared against the Chinese source
before it is accepted. Heading levels, table rows, inline and display maths,
and every link and image target must match, and the text must actually be
English — a section failing any of these is retried with the specific problem
quoted back to it.

Figure labels live in the chapter build scripts rather than in the manuscript,
so they are translated as string constants only. Each translated script is
re-parsed and compared with the original with all string values blanked, which
shows that no coordinate, number or control flow changed. The translated
scripts are kept in `tools/figure-scripts/`.

Full-width punctuation carried over from the Chinese source (ideographic
spaces after figure numbers, `／`, `〔〕`) has no glyph in the Latin text fonts
and would fail the CI font check, so `assemble.py` maps it to ASCII.

Some strings in those scripts are not labels and must stay Chinese: file paths,
filename stems, regular expressions that match the Chinese manuscript, and
values compared against data files on disk. These are recognised by how they
are used rather than by what they say.

English labels are wider than the Chinese they replace. Rather than abbreviate
them, the figure exporter saves with a tight bounding box, so a label that
reaches past the plot area grows the canvas instead of being clipped.

## Known gaps

- Two figures still contain Chinese. `figure-6-context-dependency` has no
  generating script in the repository, and `figure-7-ub-round-trip` draws its
  text from a data file rather than from a string literal.
- One label in the chapter 5 execution timeline is abbreviated: its cell is
  sized from a measured duration and cannot fit an English word.
