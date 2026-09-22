#!/usr/bin/env python3
"""Assemble the committed Traditional Chinese manuscripts into book inputs."""

from pathlib import Path
from urllib.parse import quote, unquote
import re
import shutil
import subprocess

try:
    from tools.convert_book import convert_text
except (ImportError, SystemExit):  # Optional for users only copying built inputs.
    convert_text = None

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ZH = ROOT / 'manuscripts'
TRANSLATED = HERE / 'tools' / 'manuscripts-zh-tw'
IMAGES = HERE / 'images'
LFS_POINTER = b'version https://git-lfs.github.com/spec/v1'
KNOWN_LANGUAGE_EXCEPTIONS = {
    'figure-6-context-dependency.pdf',
    'figure-7-ub-round-trip.pdf',
}


def chapter_files():
    return sorted(TRANSLATED.glob('[0-9][0-9]-*.md'))


def out_name(number: int) -> str:
    return 'introduction.md' if number == 0 else f'chapter{number:02d}.md'


def figure_for(target: str) -> Path:
    source = (ZH / unquote(target)).resolve()
    if not source.is_relative_to(ROOT):
        raise ValueError(f'Figure target escapes repository: {target}')
    name = source.with_suffix('.pdf').name
    selected = IMAGES / name
    if not selected.exists() or selected.read_bytes().startswith(LFS_POINTER):
        selected = source.with_suffix('.pdf')
        if not selected.exists():
            selected = source.with_suffix('.png')
        if not selected.exists():
            raise FileNotFoundError(source)
        IMAGES.mkdir(parents=True, exist_ok=True)
        shutil.copy2(selected, IMAGES / name)
        selected = IMAGES / name
    if selected.read_bytes().startswith(LFS_POINTER):
        raise ValueError(f'Figure is an LFS pointer; fetch it before assembling: {selected}')
    return selected


def rewrite_links(text: str) -> str:
    def link(match):
        label, target = match[1], match[2]
        if re.match(r'[a-z]+:|#', target):
            return match[0]
        path, _, fragment = target.partition('#')
        resolved = (ZH / unquote(path)).resolve()
        if not resolved.is_relative_to(ROOT):
            return match[0]
        relative = quote(resolved.relative_to(ROOT).as_posix(), safe='/')
        suffix = f'#{fragment}' if fragment else ''
        return (f'[{label}](https://github.com/bojieli/ai-infra-book/blob/main/'
                f'{relative}{suffix})')

    return re.sub(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)', link, text)


def check_figures() -> None:
    figures = sorted(IMAGES.glob('*.pdf'))
    pointers = [path.name for path in figures
                if path.read_bytes().startswith(LFS_POINTER)]
    if pointers:
        raise SystemExit('Figure files are still Git LFS pointers: ' +
                         ', '.join(pointers[:5]))

    pdftotext = shutil.which('pdftotext')
    if convert_text is None or pdftotext is None:
        print('figure language check skipped (requires OpenCC and pdftotext)')
        return

    untranslated = []
    for path in figures:
        text = subprocess.run([pdftotext, str(path), '-'],
                              capture_output=True, text=True,
                              check=False).stdout
        if convert_text(text) != text and path.name not in KNOWN_LANGUAGE_EXCEPTIONS:
            untranslated.append(path.name)
    if untranslated:
        raise SystemExit('Figures still contain convertible Simplified Chinese: ' +
                         ', '.join(untranslated[:8]))
    print(f'all figures check out ({len(KNOWN_LANGUAGE_EXCEPTIONS)} known exceptions allowed)')


def main() -> None:
    files = chapter_files()
    if len(files) != 13:
        raise SystemExit(f'Expected preface plus 12 chapters, found {len(files)}')
    written = []
    for source in files:
        text = source.read_text(encoding='utf-8')

        def image(match):
            selected = figure_for(match[2])
            return f'![{match[1]}](images/{selected.name})'

        text = re.sub(r'!\[([^\n]*)\]\(([^)]+)\)', image, text)
        text = rewrite_links(text)
        out = HERE / out_name(int(source.name[:2]))
        out.write_text(text, encoding='utf-8')
        written.append(out)

    print(f'assembled {len(written)} file(s): {", ".join(p.name for p in written)}')
    print(f'{len(list(IMAGES.glob("*.pdf")))} figure file(s) in images/')
    check_figures()


if __name__ == '__main__':
    main()
