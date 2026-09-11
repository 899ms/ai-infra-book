"""Shared helpers for the 2026-09-11 gap-plan topic tests."""
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
BOOK = json.loads((ROOT / 'scenarios/book.json').read_text())


def scenario_rows(key):
    rows = BOOK[key]
    assert rows, key
    for row in rows:
        assert set(row['inputs']) <= set(row['input_sources']), (row['id'], set(row['inputs']) - set(row['input_sources']))
        for name, source in row['input_sources'].items():
            assert isinstance(source, str) and source, (row['id'], name)
            assert source == 'book' or source.startswith('book') or source.startswith('references/') or source.startswith('configs/') or source.startswith('research/') or source.startswith('results/'), (row['id'], name, source)
            if source.startswith('results/'):
                cited = source.split(' ')[0]
                assert (ROOT / cited).is_file(), (row['id'], name, cited)
    return rows
