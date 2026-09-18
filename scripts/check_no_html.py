#!/usr/bin/env python3
"""Reject checked-in HTML, including force-added files ignored by Git."""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
# Web pages that an experiment drives (e.g. a computer-use task fixture whose
# hash is recorded in its evidence) are inputs, not build output.
forbidden = [p for p in paths if Path(p).suffix.lower() in ('.html', '.htm') and (root / p).exists()
             and not p.startswith('experiments/')]
if forbidden:
    raise SystemExit('HTML must only be a build artifact:\n' + '\n'.join(forbidden))
print('PASS: no tracked HTML source files')
