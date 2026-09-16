#!/usr/bin/env python3
"""Fetch specific Git LFS objects directly via the batch API.

git-lfs cannot enumerate objects in this blobless/shallow clone, so it fetches
nothing and exits 0. The batch endpoint works fine, so resolve and download the
pointers ourselves.  Usage: lfs_fetch.py <path> [path ...]
"""
import hashlib, json, re, sys, urllib.request
from pathlib import Path

ENDPOINT = "https://github.com/bojieli/ai-infra-book.git/info/lfs/objects/batch"
HDR = {"Accept": "application/vnd.git-lfs+json",
       "Content-Type": "application/vnd.git-lfs+json"}

def pointer(p: Path):
    if p.stat().st_size > 400: return None
    m = re.search(r"oid sha256:([0-9a-f]{64})\s+size (\d+)", p.read_text(errors="replace"))
    return (m[1], int(m[2])) if m else None

def main(paths):
    want = {}
    for s in paths:
        p = Path(s)
        if not p.exists(): print(f"missing: {s}"); continue
        ptr = pointer(p)
        if ptr is None: print(f"already real: {s}"); continue
        want[ptr[0]] = (p, ptr[1])
    if not want: return
    # The batch endpoint rejects very large request bodies (HTTP 413), so ask
    # for the objects in slices rather than all at once.
    items = list(want.items())
    objects = []
    for i in range(0, len(items), 20):
        part = items[i:i + 20]
        body = json.dumps({"operation": "download", "transfers": ["basic"],
                           "objects": [{"oid": o, "size": s} for o, (_, s) in part]}).encode()
        req = urllib.request.Request(ENDPOINT, data=body, headers=HDR)
        objects += json.loads(urllib.request.urlopen(req, timeout=60).read())["objects"]
    for obj in objects:
        path, size = want[obj["oid"]]
        act = obj.get("actions", {}).get("download")
        if not act:
            print(f"  NO URL {path}: {obj.get('error')}"); continue
        raw = urllib.request.urlopen(
            urllib.request.Request(act["href"], headers=act.get("header", {})), timeout=600).read()
        got = hashlib.sha256(raw).hexdigest()
        if got != obj["oid"]:
            print(f"  HASH MISMATCH {path}"); continue
        path.write_bytes(raw)
        print(f"  ok {path}  {len(raw)/1e6:.1f} MB  sha256 verified")

main(sys.argv[1:])
