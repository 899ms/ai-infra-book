"""Run modules with optional numerical oracles using existing Mac environments.

From repository root:
PYTHONPATH="$PWD/experiments/tools/jax-cpu-venv/lib/python3.14/site-packages" \
  OMP_NUM_THREADS=1 experiments/tools/collective-cpu-venv/bin/python \
  experiments/audit-2026-09-14/run_optional_tests.py
"""
import json
from pathlib import Path
import sys
import unittest

import numpy
import scipy
import torch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
torch.set_num_threads(1)
print('versions', torch.__version__, scipy.__version__, numpy.__version__, flush=True)
paths = [p for p in (ROOT/'calculations/tests').glob('test_*.py')
         if any(s in p.read_text() for s in ['skipIf', 'skipTest', 'skipUnless'])]
suite = unittest.TestSuite()
for p in paths:
    suite.addTests(unittest.defaultTestLoader.discover(str(ROOT/'calculations/tests'), pattern=p.name))
result = unittest.TextTestRunner(verbosity=2).run(suite)
(HERE/'optional-numerical-tests.json').write_text(json.dumps(dict(
    tests=result.testsRun, skipped=result.skipped,
    errors=[x[0].id() for x in result.errors], failures=[x[0].id() for x in result.failures],
    versions=dict(torch=torch.__version__, scipy=scipy.__version__, numpy=numpy.__version__)), indent=2)+'\n')
sys.exit(not result.wasSuccessful())
