"""Keep optional legacy rendering artifacts outside authoritative source directories."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def preview_path(markdown):
    markdown = Path(markdown)
    target = ROOT / 'build/legacy' / markdown.relative_to(ROOT).with_suffix('.html')
    target.parent.mkdir(parents=True, exist_ok=True)
    # Legacy renderers may use relative figure paths instead of embedding images.
    for folder in (ROOT / 'manuscripts').glob('ch[0-9][0-9]'):
        link = target.parent / folder.name
        if not link.exists():
            link.symlink_to(folder, target_is_directory=True)
    return target
