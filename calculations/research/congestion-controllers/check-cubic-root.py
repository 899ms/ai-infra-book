"""Root numerical bounds and actual CLI checks for the frozen CUBIC candidate."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json
import random
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
SHA = "91be0851fb7a2e947e42578e8703bd098df98ba7432672440a2f81e677282836"
assert hashlib.sha256((ROOT / "cubic.py").read_bytes()).hexdigest() == SHA
spec = importlib.util.spec_from_file_location("cubic_candidate", ROOT / "cubic.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
rng = random.Random(9438)
values = [F(n, d) for n in range(-20, 21) for d in (1, 3, 17)]
values += [F(rng.randrange(-10**30, 10**30), rng.randrange(1, 10**20)) for _ in range(300)]
values += [F(1, 10**120), F(-1, 10**120), F(10**120), F(-10**120)]
for value in values:
    lo, hi = module.cube_root_bounds(value)
    assert lo**3 <= value <= hi**3, (value, lo, hi)
    assert 0 <= hi - lo <= F(1, 10**30)
perfect = [F(n, d) for n in range(-10, 11) for d in (1, 7, 100)]
for root in perfect:
    assert module.cube_root_bounds(root**3) == (root, root)

frozen = json.loads((ROOT / "cubic-result.json").read_text())
inputs = json.loads((ROOT / "cubic-scenarios.json").read_text())
assert inputs == module.scenarios()
with tempfile.TemporaryDirectory() as directory:
    path = Path(directory)
    subprocess.run([sys.executable, str(ROOT / "cubic.py"), "--output", str(path / "all.json")], check=True)
    assert json.loads((path / "all.json").read_text()) == frozen
    for name, data in inputs.items():
        (path / "input.json").write_text(json.dumps(data))
        subprocess.run([sys.executable, str(ROOT / "cubic.py"), "--inputs", str(path / "input.json"), "--output", str(path / "one.json")], check=True)
        assert json.loads((path / "one.json").read_text()) == frozen[name], name
assert hashlib.sha256((ROOT / "cubic.py").read_bytes()).hexdigest() == SHA
result = dict(status="passed", candidate_sha256=SHA, root_bound_cases=len(values),
              exact_rational_cube_cases=len(perfect), actual_cli_invocations=len(inputs)+1,
              full_payload_scenarios=len(inputs),
              scope="Exact cubing inequalities validate returned root brackets; CLI complete payload equality. Does not prove all accumulated controller errors or transport behavior.")
(ROOT / "cubic-root-check.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
