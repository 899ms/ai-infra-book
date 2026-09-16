#!/usr/bin/env python3
"""Build a PDF from the ENGLISH manuscripts, mirroring build_pdf.py.

Two deliberate differences from the upstream script:
  * the preprocessing regexes match `# Chapter N ...` instead of `# 第 N 章 ...`
  * it drives `tectonic` instead of `xelatex`

Everything that determines the look -- elegantbook.cls, preamble.tex, cover.tex,
layout.lua and the pandoc flags -- is reused untouched.
"""
from pathlib import Path
import argparse
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EN = ROOT / 'manuscripts-en'
ZH = ROOT / 'manuscripts'


def run(command, *, cwd=HERE, log=None):
    if log:
        with log.open('w') as stream:
            r = subprocess.run(command, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT)
        if r.returncode:
            raise SystemExit(f'Build failed; see {log}\n' + log.read_text(errors='replace')[-5000:])
    else:
        subprocess.run(command, cwd=cwd, check=True)


def prepare(source, dest, assets):
    """Mirror of build_pdf.prepare with English heading patterns."""
    text = source.read_text()
    number = int(source.name[:2])
    # upstream: r'^# 第\s*\d+\s*章\s*(.*)$'
    text = re.sub(r'^# Chapter\s*\d+[:.\s]\s*(.*)$', rf'# \1 {{#chapter-{number}}}',
                  text, flags=re.M)
    text = re.sub(r'<a id="([^"]+)"></a>\s*\n+(#{1,6} [^\n]+)',
                  lambda m: m[2] + ' {#' + m[1] + '}', text)
    # alt text repeated as the following italic caption -> merge into one caption
    text = re.sub(r'!\[[^\n]*\]\(([^)]+)\)\s*\n\s*\*([^\n]+)\*',
                  lambda m: f'![{m[2]}]({m[1]})', text)

    def image(match):
        # figures live next to the Chinese sources
        original = (ZH / match[2]).resolve()
        selected = original.with_suffix('.pdf') if original.with_suffix('.pdf').exists() \
            else original.with_suffix('.png')
        if not selected.exists():
            raise FileNotFoundError(original)
        assets.append(selected)
        return f'![{match[1]}]({selected.as_posix()})'
    text = re.sub(r'!\[([^\n]*)\]\(([^)]+)\)', image, text)

    # relative links point into the repo; make them absolute GitHub URLs
    def link(match):
        target = match[2]
        if re.match(r'[a-z]+:|#', target):
            return match[0]
        return f'[{match[1]}](https://github.com/bojieli/ai-infra-book/blob/main/{target.lstrip("./")})'
    text = re.sub(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)', link, text)
    dest.write_text(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chapter', type=int, default=1)
    ap.add_argument('--lang', default='en', choices=('en', 'cn'),
                    help='elegantbook language: controls "Chapter"/"Contents" furniture')
    args = ap.parse_args()

    name = f'AI-Infra-Book-EN-Chapter-{args.chapter:02}'
    work = HERE / 'build' / name
    work.mkdir(parents=True, exist_ok=True)
    source = next(EN.glob(f'{args.chapter:02}-*.md'))
    prepared = work / source.name
    assets = []
    prepare(source, prepared, assets)

    before = work / 'frontmatter.tex'
    before.write_text('\\renewcommand{\\BookEdition}{Chapter '
                      f'{args.chapter} translation sample' + '}\n\\input{cover.tex}\n'
                      '\\pagenumbering{Roman}\n')
    prepared.write_text('```{=latex}\n\\clearpage\n\\pagenumbering{arabic}\n'
                        f'\\setcounter{{chapter}}{{{args.chapter - 1}}}\n```\n\n'
                        + prepared.read_text())

    # The .tex must sit in book/: preamble.tex reaches the pinned fonts via
    # ../manuscripts/..., and \input{template/...} is relative too. xelatex got
    # this from cwd=book/; tectonic instead uses the .tex file's own directory.
    tex = HERE / f'{name}.tex'
    run(['pandoc', str(prepared), '--file-scope', '--standalone',
         '--from=markdown+lists_without_preceding_blankline', '--to=latex',
         '--top-level-division=chapter', '--toc', '--toc-depth=2', '--number-sections',
         '--lua-filter=' + str(HERE / 'layout.lua'),
         '-V', 'documentclass=elegantbook', '-V', f'classoption=lang={args.lang}',
         '-V', 'classoption=nofont', '-V', 'classoption=cyan',
         '-V', 'classoption=device=normal',
         # elegantbook always loads biblatex; its default biber backend makes
         # tectonic shell out to biber, and Homebrew's biber 2.22 is too new for
         # the biblatex 3.17 in tectonic's bundle. The chapter cites nothing, so
         # switch the backend and skip the external tool entirely.
         '-V', 'classoption=bibtex',
         '-V', 'author=Li Bojie', '-H', str(HERE / 'preamble.tex'),
         '--include-before-body=' + str(before), '--highlight-style=kate',
         '--columns=100', '-o', str(tex)],
        log=work / 'pandoc.log')

    run(['tectonic', '-X', 'compile', str(tex), '--outdir', str(work),
         '--keep-logs', '--keep-intermediates', '-Z', 'continue-on-errors'],
        log=work / 'tectonic.log')

    out = HERE / f'{name}.pdf'
    shutil.copy2(work / f'{name}.pdf', out)
    print(out)
    print(f'{len(assets)} figures')


if __name__ == '__main__':
    main()
