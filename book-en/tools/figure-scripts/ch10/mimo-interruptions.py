#!/usr/bin/env python3
"""Render the English MiMo figure using the same data and geometry as Chinese."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[4]

if __name__ == '__main__':
    module = runpy.run_path(str(ROOT/'manuscripts/ch10/mimo-interruptions.py'))
    outputs, checks = module['draw'](language='en', output_dir=ROOT/'book-en/images')
    assert not checks['text_extent_warnings']
    for path in outputs:
        print(path.relative_to(ROOT))
