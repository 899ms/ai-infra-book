from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
r=json.loads((P/'formal-001/outcomes.json').read_text());f=r['fault']
assert r['source_sha256']==hashlib.sha256((P/'run.py').read_bytes()).hexdigest()
assert f['returncode']==-9 and f['recovered_cursor']==23 and f['redo_steps_to43']==20
expected=json.loads((P/'formal-001/fault/expected.json').read_text())['checkpoint-2']
assert f['recovered_hashes']==expected and len(expected)==11
es=[json.loads(l) for l in (P/'formal-001/fault/events.jsonl').read_text().splitlines()]
e={x['event']:x for x in es if x.get('checkpoint')=='checkpoint-2'}
assert e['api_call']['monotonic_s']<e['api_return']['monotonic_s']<e['training_complete']['monotonic_s']<f['sigkill_monotonic_s']
assert e['data_write_complete']['monotonic_s']<=e['metadata_commit_complete']['monotonic_s']<f['sigkill_monotonic_s']
assert (P/'formal-001/fault/checkpoint-2/.metadata').exists()
print('Verified SIGKILL after commit, 20 subsequent updates, and 11 restored state hashes at cursor23')
