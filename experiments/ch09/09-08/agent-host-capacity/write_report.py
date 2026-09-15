import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent
for d,title in [(R,'Agent GPU/host capacity scan'),(R.parent/'agent-dram-capacity','Agent independent host-capacity scan')]:
 if not (d/'summary.json').exists():continue
 s=json.loads((d/'summary.json').read_text())
 t=f'# {title}\n\nCompleted {s["requests"]} actual model calls: {s["target_requests"]} Agent target calls and {s["pressure_requests"]} unrelated pressure calls. All target output IDs agree across before/after pressure and scanned settings: **{s["all_target_outputs_equal_across_capacities"]}**. This is a fixed one-token replay of the same12 original Agent inputs, not a task-quality run.\n\n'
 t+='| GPU token pool | Host ratio | Target phase | Device hit tokens | Host hit tokens | Request hit rate | Token hit rate | Target time sum (s) |\n|---:|---:|---|---:|---:|---:|---:|---:|\n'
 for g in s['groups']:
  t+=f'| {g["capacity"]} | {g.get("host_ratio",2)} | {g["phase"]} | {g["levels"]["device"]} | {g["levels"]["host"]} | {g["request_hit_rate"]:.2%} | {g["token_hit_rate"]:.2%} | {g["sum_request_s"]:.6f} |\n'
 t+='\nStorage hits are zero throughout; no storage backend is configured. The native SGLang counters establish actual host reuse, rather than an inferred hit based on file existence. The analyzer checks effective GPU capacity from server_info, exact seeded3584-token pressure inputs,36 calls per fresh engine,16-token-page counters, input/source hashes and terminal engine/GPU cleanup.\n\n'
 if d==R:t+='At4096 GPU tokens, the12 post-pressure targets reuse2224 device tokens and17232 host tokens. At8192 and16384, all19456 reusable target tokens stay on device. This sweep holds host ratio2, so absolute host capacity grows too; the separate agent-dram-capacity run fixes GPU4096 and varies host capacity alone.\n\n'
 else:t+='These two fresh engines hold GPU capacity4096 and vary only host ratio1.01/1.25. The separately preserved4096/ratio2 run is the comparison point. Installed source rounds host slots to the next16-token page: the configured ratios correspond to4144/5136 slots, and ratio2 to8208 slots. These are logical pool slots, not complete process RSS. The source hash and formula are retained in host-pool-source.json.\n\n'
 t+='Per-turn complete-request times and descriptive nearest-rank sample p95 are in summary.json. They include model work, so they are not isolated host-copy latency or physical memory bandwidth. Each capacity has one pass in fixed order; first requests may include startup/JIT effects. Equal one-token outputs do not prove bitwise-equal KV tensors. All prior file/remote/failure records remain separate.\n\nHistorical9-8 remains open for the remaining storage-capacity/save-policy/V4-state comparison. Recheck from repository root with `python3 '+str(d.relative_to(Path.cwd()))+'/analyze.py`.\n'
 t+='\n![Native capacity hit levels](../agent-host-capacity/capacity.svg)\n\nThe ratio2 comparison point is reused from the first sweep, not an additional independent repetition. SVG/PNG were visually checked.\n'
 (d/'README.md').write_text(t)
 files=[p for p in d.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts]
 (d/'manifest.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
