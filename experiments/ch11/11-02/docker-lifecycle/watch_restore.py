"""Preserve transient runtime logs for one newly created experiment container."""
import json
import os
from pathlib import Path
import sys
import time
cid,out=sys.argv[1:]
assert len(cid)==64 and all(c in '0123456789abcdef' for c in cid)
r=Path('/run/containerd/io.containerd.runtime.v2.task/moby')/cid
latest={};deadline=time.monotonic()+12
while time.monotonic()<deadline:
    if r.exists():
        for p in r.rglob('*.log'):
            try:latest[str(p)]=p.read_text(errors='replace')
            except OSError:pass
    time.sleep(.01)
Path(out).write_text(json.dumps(latest,indent=2)+'\n')
os.chmod(out,0o644)
