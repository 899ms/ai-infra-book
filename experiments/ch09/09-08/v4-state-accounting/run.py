"""Logical checkpoint payload and recovery ledger; no V4 hardware timing."""
import hashlib
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'calculations/src'))
from infra_calc.topics.state import v4_state

config_path = ROOT / 'calculations/configs/models/deepseek-v4-flash/inference/config.json'
trace_path = ROOT / 'experiments/ch09/09-09/remote-kv/cross-mac-traces-001/results/agent-producer/requests.jsonl'
config = json.loads(config_path.read_text())
trace = [json.loads(line) for line in trace_path.read_text().splitlines()]
endpoints = []
for request in trace:
    n = len(request['expected_reusable_keys']) * 16
    state = v4_state(config, n, 1, 2)
    layers = []
    for row in state['layers']:
        ratio = row['ratio']
        layers.append(dict(layer=row['layer'], ratio=ratio,
                           unfinished_positions=n % ratio if ratio else 0,
                           overlap_positions=min(4, n // 4 * 4) if ratio == 4 else 0))
    endpoints.append(dict(turn=request['turn'], endpoint=n,
                          input_tokens=request['input_tokens'], components=state['components'],
                          summary=state['summary'], compressor_positions=layers))

scenarios = []
for budget_mib, policy, fault in itertools.product([0, 16, 32, 64], ['full', 'periodic4', 'recompute'], ['none', 'invalidate7']):
    budget = budget_mib * 2**20
    retained = []
    records = []
    for i, (request, endpoint) in enumerate(zip(trace, endpoints)):
        if i == 6 and fault == 'invalidate7':
            retained.clear()
        keys = request['expected_reusable_keys']
        compatible = [j for j in retained if keys[:len(trace[j]['expected_reusable_keys'])] == trace[j]['expected_reusable_keys']]
        restored = max(compatible, key=lambda j: endpoints[j]['endpoint']) if compatible else None
        prefix = endpoints[restored]['endpoint'] if restored is not None else 0
        read_bytes = endpoints[restored]['summary']['resident_bytes'] if restored is not None else 0
        scheduled = policy == 'full' or (policy == 'periodic4' and (i+1) % 4 == 0)
        size = endpoint['summary']['resident_bytes']
        evicted = []
        saved = scheduled and size <= budget
        if saved:
            while sum(endpoints[j]['summary']['resident_bytes'] for j in retained) + size > budget:
                evicted.append(retained.pop(0))
            retained.append(i)
        records.append(dict(turn=i, restored_snapshot_turn=restored, restored_tokens=prefix,
                            recompute_tokens=request['input_tokens'] - prefix,
                            history_only_fallback_recompute_tokens=request['input_tokens'],
                            read_bytes=read_bytes, write_bytes=size if saved else 0,
                            checkpoint_scheduled=scheduled, checkpoint_saved=saved,
                            evicted_snapshot_turns=evicted, retained_snapshot_turns=list(retained),
                            retained_bytes=sum(endpoints[j]['summary']['resident_bytes'] for j in retained),
                            save_s=None, restore_s=None, task_completion_s=None))
    scenarios.append(dict(budget_mib=budget_mib, policy=policy, fault=fault, requests=records,
                          write_bytes=sum(r['write_bytes'] for r in records),
                          read_bytes=sum(r['read_bytes'] for r in records),
                          recompute_tokens=sum(r['recompute_tokens'] for r in records)))

sources = [config_path, trace_path, ROOT / 'calculations/src/infra_calc/topics/state.py',
           ROOT / 'calculations/sources/deepseek-v4-flash/inference/model.py', HERE/'run.py', HERE/'PROTOCOL.md']
result = dict(status='analytical_state_and_recovery_accounting_complete',
              scope='Qwen Agent token-count/prefix fixture with pinned V4-Flash backbone state shapes; no V4 inference or tokenizer claim',
              source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
              endpoints=endpoints, scenarios=scenarios, scenario_count=len(scenarios),
              request_records=sum(len(s['requests']) for s in scenarios))
(HERE/'results.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(dict(scenarios=len(scenarios), records=result['request_records'],
                     first_snapshot_bytes=endpoints[0]['summary']['resident_bytes'],
                     last_snapshot_bytes=endpoints[-1]['summary']['resident_bytes'])))
