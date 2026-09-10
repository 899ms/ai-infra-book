"""Independent exact arithmetic checks of the declared byte-debt pacer.

This checks local pacing arithmetic, not network ordering or BBR correctness.
Run directly with Python; no optional dependencies are needed.
"""

from copy import deepcopy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("reviewed_pacer", ROOT / "pacer.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Pacer = module.Pacer
checks = []


def equal(label, actual, expected):
    assert actual == expected, (label, actual, expected)
    checks.append({"case": label, "actual": str(actual), "expected": str(expected)})


# 1200 B / 1200 B/s is one second. At 1/4 s, 900 B remains.
# Doubling the rate at that instant serves only the future 900 B.
p = Pacer(1200)
p.sent(0, 1200)
equal("initial packet debt deadline", p.ready(0), F(1))
p.advance(F(1, 4), 2400)
equal("old rate settles elapsed time", p.debt, F(900))
equal("increase affects future service only", p.ready(F(1, 4)), F(5, 8))
p.advance(F(3, 8), 600)
equal("second rate change remaining debt", p.debt, F(600))
equal("decrease extends future deadline", p.ready(F(3, 8)), F(11, 8))
p.sent(F(11, 8), 1200)
equal("exact deadline permits next packet", p.debt, F(1200))
p.advance(10)
equal("idle has no negative debt or burst credit", p.debt, F(0))
p.sent(10, 1200)
equal("one packet after idle restores full debt", p.ready(10), F(12))

# 1 B at 3 B/s: ceil(1/3 s to 0.1 s) = 0.4 s.
grid = Pacer(3, time_quantum="0.1", debt_quantum="0.01")
grid.sent(0, 1)
equal("event deadline rounds upward", grid.ready(0), F(2, 5))
equal("event rounding records added wait", F(grid.errors[-1]["local_error"]), F(1, 15))
grid.advance(F(1, 9))
equal("remaining two thirds byte rounds upward", grid.debt, F(67, 100))
equal("debt rounding records conservative error", F(grid.errors[-1]["local_error"]), F(1, 300))
equal("repeated observation has no extra debt", grid.ready(F(1, 9)), F(2, 5))
equal("observation preserves settled debt", grid.debt, F(67, 100))

# Failure must leave all state and audit rows untouched.
p = Pacer(1200)
p.sent(0, 1200)
invalid_calls = [
    ("zero rate", lambda: p.advance(F(1, 4), 0)),
    ("negative rate", lambda: p.advance(F(1, 4), -1)),
    ("boolean rate", lambda: p.advance(F(1, 4), True)),
    ("early packet", lambda: p.sent(F(1, 4), 1200)),
    ("zero packet", lambda: p.sent(1, 0)),
    ("negative packet", lambda: p.sent(1, -1)),
    ("fractional packet", lambda: p.sent(1, F(1, 2))),
    ("boolean packet", lambda: p.sent(1, True)),
    ("time reversal", lambda: p.advance(-1)),
    ("boolean time", lambda: p.ready(True)),
]
for label, call in invalid_calls:
    before = deepcopy(vars(p))
    try:
        call()
    except (ValueError, TypeError):
        pass
    else:
        raise AssertionError("accepted invalid input: " + label)
    equal("atomic rejection: " + label, vars(p), before)

result = {
    "scope": "local byte-debt arithmetic and failure atomicity; network ACK bypass and serializer order require separate checks",
    "pacer_sha256": hashlib.sha256((ROOT / "pacer.py").read_bytes()).hexdigest(),
    "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "passed": len(checks),
    "checks": checks,
}
(ROOT / "pacer-root-check.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"passed": len(checks), "pacer_sha256": result["pacer_sha256"]}))
