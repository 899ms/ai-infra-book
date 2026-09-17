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
| `images/` | figures re-rendered with English labels |
| `preamble.tex` | English preamble; loads no CJK typesetting stack |
| `build_pdf.sh` | Pandoc + XeLaTeX build |
| `assemble.py` | rebuilds the chapters and copies figures from `tools/` |
| `tools/` | translation tooling, glossary, and the translated figure scripts |

## Building

```bash
cd book-en && bash build_pdf.sh
```

Requires `pandoc`, `xelatex`, and the ElegantBook class from `book/`.

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
