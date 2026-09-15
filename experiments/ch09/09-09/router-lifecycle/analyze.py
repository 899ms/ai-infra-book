"""Validate request identity, routing, cache observations, and recovery ordering."""
import hashlib
import json
from pathlib import Path
import statistics

R = Path(__file__).resolve().parent
O = R/'results'
execution = json.loads((O/'execution.json').read_text())
for name, digest in execution['source_hashes'].items():
    assert hashlib.sha256((R/name).read_bytes()).hexdigest() == digest
rows = [json.loads(line) for line in (O/'requests.jsonl').read_text().splitlines()]
events = [json.loads(line) for line in (O/'restart-events.jsonl').read_text().splitlines()]
assert len(rows) == 54 and len(events) == 3
stages = ['cold', 'warm']+[f'pressure-w{i}-{j}' for i in range(2) for j in range(4)]+[
    'after_pressure', 'rewarm', 'failover', 'failover_warm', 'after_recovery', 'recovery_warm',
    'restarted_direct', 'restarted_direct_warm']
# There are 18 requests per trial: ten target and eight pressure requests.
assert len(stages) == 18
locations, finished = {}, set()
for directory in O.glob('*-requests'):
    worker = int(directory.name.split('-w')[1].split('-')[0])
    for path in directory.glob('*.log'):
        for line in path.read_text().splitlines():
            if '{' not in line:
                continue
            row = json.loads(line[line.index('{'):])
            rid = row.get('rid', '')
            if not rid.startswith('book909life-'):
                continue
            if row.get('event') == 'request.received':
                assert rid not in locations
                locations[rid] = worker
            if row.get('event') == 'request.finished':
                assert rid not in finished
                finished.add(rid)
observations, outputs = [], []
for trial in range(3):
    rr = [r for r in rows if r['trial'] == trial]
    assert [r['stage'] for r in rr] == stages
    by = {r['stage']: r for r in rr}
    event = events[trial]
    assert event['trial'] == trial and event['old_pid'] != event['new_pid']
    assert by['rewarm']['end'] < event['killed_at'] < event['unhealthy_observed_at'] < by['failover']['start']
    assert by['failover_warm']['end'] < event['healthy_observed_at'] < by['after_recovery']['start']
    assert by['rewarm']['worker_indices'] == [event['worker']]
    assert by['failover']['worker_indices'] == [1-event['worker']]
    for row in rr:
        rid = row['rid']
        assert row['worker_indices'] == [locations[rid]] and rid in finished
        meta = row['response']['meta_info']
        assert meta['id'] == rid and meta['completion_tokens'] == 16 and meta['num_retractions'] == 0
        pressure = row['stage'].startswith('pressure-')
        assert meta['prompt_tokens'] == (len(json.loads((O/'inputs.json').read_text())['fillers'][int(row['stage'].rsplit('-',1)[1])]) if pressure else 3136)
        if pressure:
            assert row['worker_indices'] == [int(row['stage'].split('-w')[1][0])]
        else:
            outputs.append(row['response'].get('output_ids', row['response'].get('text')))
        observations.append(dict(trial=trial, stage=row['stage'], worker=locations[rid],
            cached_tokens=meta['cached_tokens'], elapsed_s=row['end']-row['start']))
    for stage in ['cold', 'after_pressure']:
        assert by[stage]['response']['meta_info']['cached_tokens'] == 0
    for stage in ['warm', 'rewarm', 'failover_warm', 'recovery_warm', 'restarted_direct_warm']:
        assert by[stage]['response']['meta_info']['cached_tokens'] == 3135
assert len(outputs) == 30
summary = dict(status='observations_verified', requests=54, target_requests=30,
    target_outputs_equal=all(o == outputs[0] for o in outputs), rows=observations,
    stages=[dict(stage=s, cached_tokens=[r['cached_tokens'] for r in observations if r['stage'] == s],
        workers=[r['worker'] for r in observations if r['stage'] == s],
        median_s=statistics.median(r['elapsed_s'] for r in observations if r['stage'] == s))
        for s in stages if not s.startswith('pressure-')],
    restart_events=events,
    limits='Fixed chronological functional lifecycle; no remote KV retrieval or full Agent quality claim.')
(R/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
manifest = {str(p.relative_to(R)): hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted(R.rglob('*')) if p.is_file() and p.name != 'manifest.json' and '__pycache__' not in p.parts}
(R/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(json.dumps(summary, indent=2))
