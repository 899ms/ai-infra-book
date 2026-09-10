"""Shared, repository-pinned Chinese typography for every chapter figure."""
from pathlib import Path
from matplotlib import font_manager

FONT_DIR = Path(__file__).resolve().parent / 'fonts'
FAMILY = 'Source Han Sans CN'


def configure_font(override=None):
    """Register real regular/medium/bold faces; retain explicit --font overrides."""
    for weight in ('Regular', 'Medium', 'Bold'):
        path = FONT_DIR / f'SourceHanSansCN-{weight}.ttf'
        if not path.exists():
            raise FileNotFoundError(f'Pinned figure font missing: {path}')
        font_manager.fontManager.addfont(str(path))
    path = Path(override).expanduser().resolve() if override else FONT_DIR/'SourceHanSansCN-Regular.ttf'
    if override:
        font_manager.fontManager.addfont(str(path))
    return path, font_manager.FontProperties(fname=str(path)).get_name()
