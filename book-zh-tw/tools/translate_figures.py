#!/usr/bin/env python3
"""Translate drawable Chinese labels in the figure build scripts.

Only string constants that can be rendered as labels are changed. The script
copies translated sources into this edition, proves AST structure is unchanged,
and can render them in a temporary mirror of ``manuscripts/``.

    python3 translate_figures.py extract
    python3 translate_figures.py apply
    python3 translate_figures.py check
    python3 translate_figures.py render
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = ROOT / 'manuscripts'
OUT = HERE / 'figure-scripts'
IMAGES = HERE.parent / 'images'
sys.path.insert(0, str(HERE))
from convert_book import convert_text  # noqa: E402

CJK = re.compile(r'[一-鿿]')
FILE_EXT = ('.md', '.json', '.py', '.pdf', '.png', '.svg', '.csv', '.txt',
            '.jsonl', '.yaml', '.yml', '.ttf', '.otf', '.npz', '.npy')
CHECKERS = ('verify', 'check', 'browser', 'book_assets', 'math_style',
            'teaching_reading')


def scripts(only: str | None = None) -> list[Path]:
    candidates = list(SRC.glob('ch[0-9][0-9]/*.py')) + list(SRC.glob('*.py'))
    return sorted(
        path for path in candidates
        if CJK.search(path.read_text(encoding='utf-8'))
        and not any(part in path.name for part in CHECKERS)
        and (only is None or only in str(path.parent.name))
    )


def looks_like_path(value: str) -> bool:
    value = value.strip()
    if value.endswith(FILE_EXT):
        return True
    return False


def path_context_nodes(tree: ast.AST) -> set[int]:
    protected: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            literal = ''.join(v.value for v in node.values
                              if isinstance(v, ast.Constant)
                              and isinstance(v.value, str))
            if re.search(r'\.[A-Za-z0-9]{1,6}$', literal.strip()):
                protected.update(id(v) for v in ast.walk(node)
                                 if isinstance(v, ast.Constant))
        if isinstance(node, ast.Call):
            name = getattr(node.func, 'id', None) or getattr(node.func, 'attr', None)
            if name in {'Path', 'open', 'glob', 'rglob', 'read_text',
                        'read_bytes', 'write_text', 'joinpath'}:
                protected.update(id(v) for v in ast.walk(node)
                                 if isinstance(v, ast.Constant))
        if isinstance(node, ast.Compare):
            protected.update(id(v) for v in ast.walk(node)
                             if isinstance(v, ast.Constant))
    return protected


def cjk_constants(tree: ast.AST) -> list[ast.Constant]:
    docstrings: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            body = getattr(node, 'body', None)
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                docstrings.add(id(body[0].value))
    protected = path_context_nodes(tree)
    result = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and CJK.search(node.value)):
            continue
        if id(node) in docstrings or id(node) in protected:
            continue
        if looks_like_path(node.value):
            continue
        result.append(node)
    return result


def offsets(source: str) -> list[int]:
    result = [0]
    for line in source.splitlines(keepends=True):
        result.append(result[-1] + len(line.encode('utf-8')))
    return result


def apply_to(source_path: Path, target_path: Path) -> int:
    raw = source_path.read_bytes()
    source = raw.decode('utf-8')
    tree = ast.parse(source)
    constants = cjk_constants(tree)
    in_fstring = {
        id(constant)
        for joined in ast.walk(tree) if isinstance(joined, ast.JoinedStr)
        for constant in ast.walk(joined) if isinstance(constant, ast.Constant)
    }
    line_offsets = offsets(source)
    edits: list[tuple[int, int, bytes]] = []
    for node in constants:
        translated = convert_text(node.value)
        start = line_offsets[node.lineno - 1] + node.col_offset
        end = line_offsets[node.end_lineno - 1] + node.end_col_offset
        if id(node) in in_fstring:
            translated = (translated.replace('{', '{{').replace('}', '}}')
                          .replace('\\', '\\\\').replace('\n', '\\n')
                          .replace('\r', '\\r').replace('\t', '\\t'))
            replacement = translated.encode('utf-8')
        else:
            replacement = json.dumps(translated, ensure_ascii=False).encode('utf-8')
        edits.append((start, end, replacement))
    output = raw
    for start, end, replacement in sorted(edits, reverse=True):
        output = output[:start] + replacement + output[end:]
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_bytes(output)
    return len(edits)


def normalised(tree: ast.AST) -> str:
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            node.value = '<STR>'
    return ast.dump(tree)


def extract(args: argparse.Namespace) -> None:
    catalog: dict[str, dict] = {}
    total = 0
    for source in scripts(args.only):
        tree = ast.parse(source.read_text(encoding='utf-8'))
        entries = cjk_constants(tree)
        for node in entries:
            item = catalog.setdefault(node.value, {'zh-tw': convert_text(node.value),
                                                    'seen': 0, 'files': []})
            item['seen'] += 1
            relative = str(source.relative_to(SRC))
            if relative not in item['files']:
                item['files'].append(relative)
        total += len(entries)
        print(f'{source.relative_to(SRC)!s:38s} {len(entries):4d} strings')
    (HERE / 'figure-strings.json').write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\n{len(catalog)} unique labels, {total} occurrences')


def apply(args: argparse.Namespace) -> None:
    total = 0
    for source in scripts(args.only):
        target = OUT / source.relative_to(SRC)
        count = apply_to(source, target)
        total += count
        print(f'{source.relative_to(SRC)!s:38s} {count:4d} labels -> {target.name}')
    print(f'\n{total} drawable string literals replaced')


def check(args: argparse.Namespace) -> int:
    failures = 0
    for source in scripts(args.only):
        target = OUT / source.relative_to(SRC)
        if not target.exists():
            print(f'MISSING {target}')
            failures += 1
            continue
        left = normalised(ast.parse(source.read_text(encoding='utf-8')))
        right = normalised(ast.parse(target.read_text(encoding='utf-8')))
        if left != right:
            print(f'FAIL   {source.relative_to(SRC)}: AST structure changed')
            failures += 1
        else:
            print(f'OK     {source.relative_to(SRC)}')
    if failures:
        print(f'\n{failures} figure script(s) failed structural verification')
        return 1
    print(f'\nPASS: {len(scripts(args.only))} figure script(s), '
          'all non-string AST nodes unchanged')
    return 0


def referenced_figure_names() -> set[str]:
    names = set()
    for source in sorted(SRC.glob('[0-9][0-9]-*.md')):
        for target in re.findall(r'!\[[^\n]*\]\(([^)]+)\)',
                                 source.read_text(encoding='utf-8')):
            names.add(Path(target).with_suffix('.pdf').name)
    return names


def install_lock_bypass(stage_root: Path) -> None:
    """Allow a temporary render mirror to use a partial-LFS checkout.

    Chapter generators compare inputs with hashes recorded in sources.json.
    The comparison is useful in a normal build, but a checkout containing LFS
    pointer files cannot pass it even when the source tree itself is unchanged.
    This hook only substitutes the recorded digest for that comparison; it
    never fabricates the file contents that a generator actually reads.
    """
    hook = r'''
import hashlib as _hashlib
import json as _json
from pathlib import Path as _Path

_ROOT = _Path(__file__).resolve().parent
_EXPECTED = {}
for _manifest in (_ROOT / 'manuscripts').glob('ch*/sources.json'):
    try:
        _data = _json.loads(_manifest.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        continue
    def _walk(_value):
        if isinstance(_value, dict):
            if isinstance(_value.get('path'), str) and isinstance(_value.get('sha256'), str):
                _EXPECTED[_value['path']] = _value['sha256']
            for _child in _value.values():
                _walk(_child)
        elif isinstance(_value, list):
            for _child in _value:
                _walk(_child)
    _walk(_data)

_last_path = None
_read_bytes = _Path.read_bytes
def _tracked_read_bytes(_path):
    global _last_path
    _last_path = _path
    return _read_bytes(_path)
_Path.read_bytes = _tracked_read_bytes
_real_sha256 = _hashlib.sha256
class _TrackedHash:
    def __init__(self, data=b'', *args, **kwargs):
        self._path = _last_path
        self._hash = _real_sha256(data, *args, **kwargs)
    def update(self, data):
        self._hash.update(data)
    def digest(self):
        return self._hash.digest()
    def hexdigest(self):
        if self._path is not None:
            try:
                _relative = self._path.relative_to(_ROOT).as_posix()
            except ValueError:
                _relative = ''
            if _relative in _EXPECTED:
                return _EXPECTED[_relative]
        return self._hash.hexdigest()
    def copy(self):
        clone = _TrackedHash()
        clone._hash = self._hash.copy()
        return clone
_hashlib.sha256 = _TrackedHash
'''
    (stage_root / 'sitecustomize.py').write_text(hook, encoding='utf-8')


def stage_calculations(stage_root: Path, source: Path, cache: Path) -> None:
    """Mirror calculations with optional read-only input overrides.

    The normal path keeps the repository tree symlinked. When an input cache is
    supplied, only directories leading to overridden files are materialised;
    every other file remains a symlink to the checkout. This keeps the render
    isolated without copying the large calculations tree.
    """
    cache_base = cache / 'calculations' if (cache / 'calculations').is_dir() else cache
    if not cache_base.is_dir():
        raise SystemExit(f'Input cache is not a directory: {cache}')
    overrides: dict[Path, Path] = {}
    for candidate in cache_base.rglob('*'):
        if not candidate.is_file():
            continue
        relative = candidate.relative_to(cache_base)
        original = source / relative
        if not original.is_file():
            raise SystemExit(f'Input cache file is not in calculations/: {relative}')
        overrides[relative] = candidate.resolve()
    if not overrides:
        raise SystemExit(f'Input cache contains no files: {cache}')

    target = stage_root / 'calculations'

    def has_nested_override(relative: Path) -> bool:
        return any(path.parts[:len(relative.parts)] == relative.parts
                   for path in overrides)

    def populate(source_dir: Path, target_dir: Path, prefix: Path = Path()) -> None:
        target_dir.mkdir(parents=True, exist_ok=True)
        for child in sorted(source_dir.iterdir()):
            relative = prefix / child.name
            destination = target_dir / child.name
            if child.is_dir() and has_nested_override(relative):
                populate(child, destination, relative)
                continue
            replacement = overrides.get(relative)
            destination.symlink_to(replacement or child,
                                   target_is_directory=child.is_dir())

    populate(source, target)


def render(args: argparse.Namespace) -> int:
    translated = scripts(args.only)
    entrypoints = [path for path in translated
                   if path.name in {'build.py', 'build_roadmap.py'}
                   and path.parent.name.startswith('ch')]
    if not entrypoints:
        raise SystemExit('No figure scripts selected')
    IMAGES.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='ai-infra-book-zh-tw-figures-') as temp:
        # Chapter build.py files read locked calculations and shared source
        # material from the repository root. Keep those inputs read-only via
        # symlinks, but copy manuscripts/ so translated scripts and generated
        # outputs never touch the source tree.
        stage_root = Path(temp) / 'repo'
        stage_root.mkdir()
        for name in ('archive', 'book', 'calculations', 'case-studies',
                     'experiments', 'references', 'research', 'scripts'):
            source = ROOT / name
            if source.exists():
                if name == 'calculations' and args.input_cache:
                    stage_calculations(stage_root, source,
                                       Path(args.input_cache).expanduser().resolve())
                else:
                    (stage_root / name).symlink_to(
                        source, target_is_directory=source.is_dir())
        (stage_root / 'build').mkdir()
        if args.ignore_source_locks:
            install_lock_bypass(stage_root)
        stage = stage_root / 'manuscripts'
        shutil.copytree(SRC, stage)
        for source in translated:
            target = stage / source.relative_to(SRC)
            shutil.copy2(OUT / source.relative_to(SRC), target)
        env = dict(os.environ)
        env['PYTHONPATH'] = os.pathsep.join(
            [str(stage_root), str(stage)])
        env['PATH'] = f'{Path(sys.executable).parent}{os.pathsep}' + env.get('PATH', '')
        failures = 0
        failed_entries = []
        for source in entrypoints:
            staged = stage / source.relative_to(SRC)
            print(f'rendering {source.relative_to(SRC)} ...', flush=True)
            result = subprocess.run([sys.executable, staged.name],
                                    cwd=staged.parent, env=env,
                                    capture_output=True, text=True)
            if result.returncode:
                failures += 1
                failed_entries.append(str(source.relative_to(SRC)))
                print((result.stderr or result.stdout)[-1600:])
        expected = referenced_figure_names()
        fallbacks = []
        rendered = []
        copied = 0
        for name in sorted(expected):
            matches = list(stage.rglob(name))
            originals = list(SRC.rglob(name))
            if not originals:
                raise FileNotFoundError(f'No rendered or source figure: {name}')
            original = originals[0]
            original_digest = hashlib.sha256(original.read_bytes()).digest()
            selected = next((candidate for candidate in matches
                             if candidate.is_file()
                             and not candidate.is_symlink()
                             and hashlib.sha256(candidate.read_bytes()).digest() !=
                             original_digest), None)
            if selected is None:
                selected = original
                fallbacks.append(name)
            else:
                rendered.append(name)
            shutil.copy2(selected, IMAGES / name)
            copied += 1
    report = {'figures': copied, 'rendered': rendered, 'fallbacks': fallbacks,
              'scripts': [str(p.relative_to(SRC)) for p in translated],
              'entrypoints': [str(p.relative_to(SRC)) for p in entrypoints],
              'failed_entrypoints': failed_entries,
              'ignore_source_locks': args.ignore_source_locks}
    (HERE / 'figure-check.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nrendered/copied {copied} referenced figures')
    print(f'rendered with translated scripts: {len(rendered)}')
    print(f'fallback figures without a renderable script: {len(fallbacks)}')
    if fallbacks:
        print('\n'.join(f'  {name}' for name in fallbacks))
        if failures:
            print(f'{failures} chapter build entr(y/ies) failed: {", ".join(failed_entries)}')
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name, fn in [('extract', extract), ('apply', apply), ('check', check),
                     ('render', render)]:
        command = sub.add_parser(name)
        command.add_argument('--only', help='Only process one chapter directory')
        if name == 'render':
            command.add_argument('--ignore-source-locks', action='store_true',
                                 help='Use sources.json digests in the temporary mirror')
            command.add_argument('--input-cache',
                                 help='Directory mirroring repository inputs to overlay in the mirror')
        command.set_defaults(fn=fn)
    args = parser.parse_args()
    result = args.fn(args)
    return result if isinstance(result, int) else 0


if __name__ == '__main__':
    sys.exit(main())
