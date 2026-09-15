import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent
io=json.loads((P/'agent-storage-io/summary.json').read_text());s=json.loads((R/'results.json').read_text())
t='''# Agent KV local direct-I/O measurement

197 actual native Agent KV pages (443.25MiB) were copied into a fresh RTX directory and checked against their original Mac SHA-256 values. The benchmark completed197 O_DIRECT writes with file+directory fsync and591 O_DIRECT reads across three shuffled passes. Every read returned the full page and passed SHA verification.

| Operation | Count | Median page time | Sample p95 page time | Sum of timed operations |
|---|---:|---:|---:|---:|
'''
for name,x in io['summary'].items():t+=f'| {name} | {x["operations"]} | {x["median_s"]*1000:.6f}ms | {x["sample_p95_s"]*1000:.6f}ms | {x["sum_s"]:.6f}s |\n'
t+='''
Each page is2359296bytes (2.25MiB). The measured filesystem is ext4 on /dev/md0p1; it is not labeled as a single NVMe drive. O_DIRECT bypasses kernel data page cache, not hardware/controller caches. Source read, aligned-buffer fill and checksum work are outside the timed write; checksums are outside read timing. File open/close are included. The write contract includes fsync and is stronger than the existing remote HTTP store's non-fsynced publication.

The remote source and written copies are retained under /home/ubuntu/ai-infra-book-experiments/ch09/09-08/agent-storage-io; original payloads already exist locally in the source cross-Mac store. Per-operation records and source hashes are local. No GPU engine, global cache drop, other files or model cache were modified. These are actual storage primitives, not complete model-recovery requests or a stable request p95 estimate.

Run `python3 experiments/ch09/09-08/agent-storage-io/analyze.py` to recheck original page identities, all788 operations, seeded ordering and summaries.
'''
(P/'agent-storage-io/README.md').write_text(t)
t='''# Same-Agent capacity/checkpoint record replay

Completed729 explicitly defined scenarios and8748 per-request records:0/64/256 retained pages independently in four tiers, full/periodic4/no-persistence policies, and normal/restart-before-turn7/invalidation-before-turn7 conditions. Input prefixes and197 page identities come from the verified12-turn Agent trace.

This is an inclusive page-LRU reference replay, not native SGLang tree eviction or a new live four-tier service. Retention budgets exclude a sufficient execution working set; zero retained HBM is not zero physical GPU memory. Search stops at the first missing prefix page, so surviving suffix pages are not counted as reusable context.

The example below uses no volatile retention, no remote storage and a worker restart before turn7. Local-only timing uses measured direct-I/O page primitives and the documented model timing proxies.

| Local retained pages | Policy | Token hit rate | Logical bytes written | Estimated trace seconds |
|---:|---|---:|---:|---:|
'''
for x in s['scenarios']:
 c=x['capacity_pages']
 if c['hbm']==c['dram']==c['remote']==0 and x['fault']=='restart7':t+=f'| {c["local"]} | {x["policy"]} | {x["token_hit_rate"]:.2%} | {x["write_bytes"]["local"]} | {x["estimated_trace_completion_s"]:.6f} |\n'
t+='''
A64-page LRU store can evict the root while streaming a larger full prefix. In this defined policy, the smaller periodic checkpoint can preserve a usable beginning and produce more hits than full saving. This illustrates why total resident bytes alone do not establish recoverability; it is not an observation about SGLang's native eviction algorithm.

All729 rows retain tier hit counts, recomputation-token counts, checkpoint writes, eviction counts, storage-read quantiles and estimated completion components. Page-local read/write times are measured. Remote timings come from actual SSH/HTTP page RPCs; unobserved page reads use a measured median and their fallback counts are explicit. Synchronous checkpoint costs are added without async overlap. Complete-prefix model service uses measured GPU-warm/host profiles; incomplete prefixes use measured full-cold request time, with no proportional partial-prefill speedup assumption. These are timing proxies, not observed full-task completion or guaranteed bounds.

Storage-read sample p95 is a quantile of repeated composed records, not independent production p95. Local writes include file/directory fsync; remote publication did not fsync. Storage persistence here means surviving a model-worker restart while the stores remain intact, not equal power-loss durability. Restart/invalidation events are simulated; prior native recovery/fault runs remain the actual execution evidence.

This completes the dense-page capacity/save-policy reference replay. Historical9-8 still needs the V4 compression/window-state accounting and final requirement integration. No compressed V4 tensors or V4 model execution are claimed by this Qwen-page replay.

Reproduce from repository root with `python3 experiments/ch09/09-08/agent-policy-replay/run.py` and `python3 experiments/ch09/09-08/agent-policy-replay/verify.py`. Verification checks all729 unique settings, input/source hashes, token conservation, fault reset invariants, checkpoint schedule and closed-form no-eviction write identities. It does not turn the stated reference policy into a measured native implementation.
'''
(R/'README.md').write_text(t)
for d in [P/'agent-storage-io',R]:
 files=[p for p in d.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts]
 (d/'manifest.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
