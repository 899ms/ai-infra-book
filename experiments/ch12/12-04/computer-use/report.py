import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent;a=json.loads((R/'agent-summary.json').read_text());n=json.loads((R/'network-summary.json').read_text())
s="""# Screenshot-driven Computer Use and controlled network records

Qwen3-VL-8B-Instruct BF16 on the RTX PRO GPU operated a fresh local Chrome browser on Mac using screenshots and mouse/keyboard actions. The target was to save 12 USB-C Adapters from East warehouse for project Vision Lab with Express delivery. This is an isolated test application with no real purchase. The model received no DOM, hidden state, selectors or precomputed coordinates.

![Verified final order](structured-agent-results/trial0/final.png)

The initial unconstrained batch completed 0/3 tasks: all three first responses omitted the JSON y key. Those unmodified failures remain in agent-results/server-results. A separately recorded intervention added vLLM JSON-schema-constrained decoding; its three fresh trials all succeeded, with eight actual model-driven browser actions per trial. The action validator did not repair outputs. Source, prompts, screenshots, token IDs/events, final states and full logs remain available. This measures one fixed fixture, not broad Computer Use competence.

| Batch | Successful tasks | Formal GPU calls | Task seconds by trial |
|---|---:|---:|---|
"""
for key,v in a.items():
 s+=f"| {key} | {v['successes']}/3 | {v['formal_model_calls']} | "+' / '.join(f"{t['elapsed_s']:.3f}" for t in v['trials'])+' |\n'
s+="""
Each batch has one extra one-token image warmup excluded from task times. Live task duration includes screenshots, SSH-tunneled requests, model service and browser actions, excluding model load/browser startup. Model service is timed on the RTX clock; task/actions are timed on the Mac clock. No cross-host timestamp subtraction is used. Structured trials have 2.68–3.16 seconds summed GPU service. Both own model engines shut down and the GPU was empty afterward.

## Controlled transport of the recorded rounds

The first constrained trial supplies eight actual JSON requests containing PNG screenshots plus instructions/history and their action responses. Each request replays its measured model-service wait after complete upload. This is actual byte transport with recorded service, not 98 new GPU calls or 12 new browser tasks. Three shuffled repetitions compare TLS HTTP/1.1 and HTTP/3 with connection reuse off/on, at container-loopback netem 80ms RTT,20Mbit/s,0.1% loss,2CPU/2GiB. 96 formal exchanges plus2 warmups all passed hashes/action decoding/TLS/ALPN/reuse/qlogs/service waits and drained-queue checks.

| Protocol | Reuse | Median validated round ms | Eight-round trace seconds, three trials |
|---|---|---:|---|
"""
for c in n['conditions']:
 s+=f"| {c['protocol']} | {c['reuse']} | {c['median_round_ms']:.3f} | "+' / '.join(f"{v:.3f}" for v in c['trace_s'])+' |\n'
s+="""
Reuse-on includes one fresh and seven reused requests per trace. Reuse-off connections are distinct and closed at group cleanup; cleanup is excluded from trace time. The round medians pool24 formal rounds with different screenshot/instruction sizes and service times; each condition uses exactly the same source sequence. Browser screenshot/action execution is excluded from transport replay, with original times retained in network-fixture.json. Configured rate is not measured application goodput; previous short calibration is in ../controlled-network. Random loss placement and scheduling differ. These results do not establish general HTTP/3 superiority. No default browser network stack, acoustic onset, window tuning or interrupted recovery is claimed.

Revalidate with `python analyze_agent.py` and `python analyze_network.py`. PROTOCOL.md defines the two model batches and transport scope; run_network.sh pins the existing Docker image and isolates netem. Docker image/container inspections, qlogs and cleanup records are retained. Browser sessions and both own model engines closed. This completes the actual Computer Use trace and its connection-reuse record comparison; parent12-4 still needs window, recovery and final cross-workload work.
"""
(R/'README.md').write_text(s)
files={str(p.relative_to(R)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in R.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
(R/'manifest.json').write_text(json.dumps(dict(scope='Actual screenshot-driven model/browser tasks plus fixed trace network replay; parent incomplete',files=files),indent=2)+'\n')
