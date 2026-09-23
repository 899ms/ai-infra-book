#!/usr/bin/env python3
"""Build the Traditional Chinese edition PDF with Pandoc and XeLaTeX."""

from pathlib import Path
from urllib.parse import quote
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BOOK = ROOT / 'book'
NAME = 'AI-Infra-Book-ZH-TW'
LFS_POINTER = b'version https://git-lfs.github.com/spec/v1'


def run(command, *, cwd=HERE, log=None):
    env = dict(os.environ)
    env['TEXINPUTS'] = f'.:{HERE}:{BOOK}:{BOOK / "template"}:'
    env.setdefault('extra_mem_top', '8000000')
    env.setdefault('extra_mem_bot', '8000000')
    env.setdefault('MKTEXTFM', '0')
    if log:
        with log.open('w') as stream:
            result = subprocess.run(command, cwd=cwd, env=env,
                                    stdout=stream, stderr=subprocess.STDOUT)
        if result.returncode:
            raise SystemExit(f'Build failed; see {log}\n' +
                             log.read_text(errors='replace')[-6000:])
    else:
        subprocess.run(command, cwd=cwd, env=env, check=True)


def prepare(source, dest, number, assets, source_ref=None):
    text = source.read_text(encoding='utf-8')
    if number == 0:
        text = re.sub(r'^# 前言\s*$', '# 前言 {.unnumbered}', text, flags=re.M)
        text = re.sub(r'^(## .+)$', r'\1 {.unnumbered}', text, flags=re.M)
    text = re.sub(r'^# 第\s*\d+\s*章\s*(.*)$',
                  rf'# \1 {{#chapter-{number}}}', text, flags=re.M)
    text = re.sub(r'<a id="([^"]+)"></a>\s*\n+(#{1,6} [^\n]+)',
                  lambda m: m[2] + ' {' + '#' + m[1] + '}', text)
    text = re.sub(r'!\[[^\n]*\]\(([^)]+)\)\s*\n\s*\*([^\n]+)\*',
                  lambda m: f'![{m[2]}]({m[1]})', text)

    def image(match):
        selected = (HERE / match[2]).resolve()
        if not selected.exists():
            raise FileNotFoundError(selected)
        if selected.read_bytes().startswith(LFS_POINTER):
            raise ValueError('Figure is an LFS pointer; run '
                             f'git lfs pull --include="book-zh-tw/images/**" '
                             f'--exclude="": {selected}')
        assets.append(selected)
        return f'![{match[1]}]({selected.as_posix()})'

    text = re.sub(r'!\[([^\n]*)\]\(([^)]+)\)', image, text)
    if source_ref:
        text = text.replace(
            'https://github.com/bojieli/ai-infra-book/blob/main/',
            f'https://github.com/bojieli/ai-infra-book/blob/{quote(source_ref, safe="")}/')
    dest.write_text(text, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, default=HERE,
                        help='Output directory relative to book-zh-tw/')
    parser.add_argument('--source-ref',
                        help='Git commit for portable GitHub links in the PDF')
    args = parser.parse_args()
    output_dir = (HERE / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    work = HERE / 'build' / NAME
    work.mkdir(parents=True, exist_ok=True)

    chapters = [HERE / f'chapter{n:02}.md' for n in range(1, 13)]
    missing = [p.name for p in chapters if not p.exists()]
    if missing:
        raise SystemExit('Missing chapters: ' + ', '.join(missing))

    assets, inputs = [], []
    for number, source in enumerate(chapters, start=1):
        target = work / source.name
        prepare(source, target, number, assets, args.source_ref)
        inputs.append(target)

    preface = HERE / 'introduction.md'
    prepared_preface = work / preface.name
    prepare(preface, prepared_preface, 0, assets, args.source_ref)
    preface_tex = work / 'preface.tex'
    run(['pandoc', str(prepared_preface), '--to=latex',
         '--lua-filter=' + str(BOOK / 'layout.lua'),
         '--top-level-division=chapter', '-o', str(preface_tex)],
        log=work / 'preface-pandoc.log')

    before = work / 'frontmatter.tex'
    before.write_text('\\renewcommand{\\BookEdition}{v1.0}\n'
                      '\\input{cover.tex}\n'
                      '\\pagenumbering{Roman}\n'
                      '\\input{' + str(preface_tex) + '}\n'
                      '\\clearpage\n', encoding='utf-8')
    first = inputs[0]
    first.write_text('```{=latex}\n\\clearpage\n\\pagenumbering{arabic}\n'
                     '\\setcounter{chapter}{0}\n```\n\n' +
                     first.read_text(encoding='utf-8'), encoding='utf-8')

    tex = work / 'book.tex'
    command = ['pandoc', *map(str, inputs), '--file-scope', '--standalone',
               '--from=markdown+lists_without_preceding_blankline', '--to=latex',
               '--top-level-division=chapter', '--toc', '--toc-depth=2',
               '--number-sections', '--lua-filter=' + str(BOOK / 'layout.lua'),
               '-V', 'documentclass=elegantbook', '-V', 'classoption=lang=cn',
               '-V', 'classoption=nofont', '-V', 'classoption=cyan',
               '-V', 'classoption=device=normal', '-V', 'author=李博杰',
               '--metadata', 'title-meta=深入理解 AI Infra：量化分析與系統設計',
               '--metadata', 'author-meta=李博杰（繁體中文版）',
               '-H', str(HERE / 'preamble.tex'),
               '--include-before-body=' + str(before),
               '--highlight-style=kate', '--columns=100', '-o', str(tex)]
    run(command, log=work / 'pandoc.log')

    for iteration in range(1, 4):
        run(['xelatex', '-interaction=nonstopmode', '-halt-on-error',
             '-file-line-error', '-output-directory=' + str(work), str(tex)],
            log=work / f'xelatex-{iteration}.log')

    output = output_dir / f'{NAME}.pdf'
    staged_output = output.with_suffix('.pdf.tmp')
    shutil.copy2(work / 'book.pdf', staged_output)
    staged_output.replace(output)

    log = (work / 'book.log').read_text(errors='replace')
    warnings = [line for line in log.splitlines()
                if any(x in line for x in
                       ['Overfull', 'Missing character:',
                        'undefined references', 'LaTeX Warning:'])]
    sources = [preface] + chapters
    report = {
        'output': str(output),
        'source_ref': args.source_ref,
        'edition': 'zh-tw',
        'chapters': list(range(1, 13)),
        'engine': 'Pandoc + XeLaTeX / ElegantBook (AI Infra Book series template)',
        'sources': [
            dict(path=str(path.relative_to(ROOT)),
                 sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            for path in sources
        ],
        'figure_count': len(assets),
        'warnings': warnings,
    }
    (output_dir / f'{NAME}-build.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if shutil.which('pdftoppm'):
        run(['pdftoppm', '-f', '1', '-l', '1', '-scale-to', '1600',
             '-png', '-singlefile', str(output),
             str(output_dir / f'{NAME}-Cover')])
    print(output)
    print(f'12 chapters, {len(assets)} figures; {len(warnings)} layout/font warnings; '
          f'details: {work}/book.log')


if __name__ == '__main__':
    main()
