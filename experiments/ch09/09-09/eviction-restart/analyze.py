"""Check native responses, lifecycle ordering and frozen inputs independently."""
import hashlib
import json
from pathlib import Path
from statistics import median

HERE = Path(__file__).resolve().parent
out = HERE/'results'
protocol = json.loads((out/'protocol.json').read_text())
for name, digest in protocol['source_sha256'].items():
    assert hashlib.sha256((HERE/name).read_bytes()).hexdigest() == digest, name
inputs = json.loads((out/'inputs.json').read_text())
source = json.loads((HERE/'agent-prompts.json').read_text())
assert inputs['target'] == source['requests'][-1]['prompt_token_ids']
rows = [json.loads(line) for line in (out/'requests.jsonl').read_text().splitlines()]
stages = ['cold', 'warm', 'pressure-0', 'pressure-1', 'pressure-2', 'pressure-3',
          'after_pressure', 'rewarm', 'after_restart', 'restart_warm']
assert len(rows) == 30
for trial in range(3):
    group = [r for r in rows if r['trial'] == trial]
    assert [r['stage'] for r in group] == stages
    assert len(set(r['pid'] for r in group[:8])) == 1
    assert group[8]['pid'] == group[9]['pid'] != group[0]['pid']
    for a,b in zip(group,group[1:]):
        assert a['start'] <= a['end'] <= b['start']
    for r in group:
        meta = r['response']['meta_info']
        n = len(inputs['fillers'][int(r['stage'][-1])]) if r['stage'].startswith('pressure-') else len(inputs['target'])
        assert meta['prompt_tokens'] == n
        assert meta['completion_tokens'] == 16
        assert 0 <= meta['cached_tokens'] < n
    for index in [0,6,8]:
        assert group[index]['response']['meta_info']['cached_tokens'] == 0
    for index in [1,7,9]:
        assert group[index]['response']['meta_info']['cached_tokens'] == len(inputs['target'])-1
cleanup = json.loads((out/'cleanup.json').read_text())
assert len(cleanup) == 6 and len(set(r['pid'] for r in cleanup)) == 6
assert {r['pid'] for r in rows} == {r['pid'] for r in cleanup}
target_rows = [r for r in rows if not r['stage'].startswith('pressure-')]
summary = dict(status='completed_subexperiment', requests=30, target_requests=18, pressure_requests=12,
               prompt_tokens=len(inputs['target']), all_target_text_equal=len(set(r['response']['text'] for r in target_rows))==1,
               timing_is='Client wall time on a shared GPU, fixed lifecycle ordering; not an isolated performance comparison.',
               quality_scope='Sixteen generated tokens from an archived failed Agent task; not a completed or newly correct task.',
               stages=[dict(stage=stage, cached_tokens=[r['response']['meta_info']['cached_tokens'] for r in rows if r['stage']==stage],
                            median_client_seconds=median(r['end']-r['start'] for r in rows if r['stage']==stage))
                       for stage in stages if not stage.startswith('pressure-')],
               remaining='No router, remote storage, multiple workers, or task-quality claim. Historical 9-9 remains partial.')
(HERE/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
files=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='manifest.json']
(HERE/'manifest.json').write_text(json.dumps({str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)},indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
