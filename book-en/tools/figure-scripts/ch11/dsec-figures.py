#!/usr/bin/env python3
"""Render the English DSec figures using the same geometry as the Chinese ones."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT/'manuscripts'), str(ROOT/'manuscripts/ch11')]

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from figure_style import Exporter
from figure_style.typography import configure_font
from dsec_figures import draw

if __name__ == '__main__':
    _, family = configure_font()
    plt.rcParams.update({'font.family': [family, 'DejaVu Sans'], 'svg.fonttype': 'path', 'svg.hashsalt': 'chapter11-dsec-en'})
    out = Exporter(ROOT/'book-en/images')
    draw(out, english=True)
    for path in out.outputs:
        print(path.relative_to(ROOT))
