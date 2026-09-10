"""Verify sealed artifacts and completed experiment scope; no GPU required."""
import hashlib,json
from pathlib import Path
r=Path(__file__).absolute().parent;m=json.loads((r/'manifest.json').read_text())
for name,sha in m.items():assert hashlib.sha256((r/name).read_bytes()).hexdigest()==sha,name
s=json.loads((r/'run/supervisor.json').read_text());assert s['exit_code']==0 and s['reason'] is None and s['leftovers']=={}
a=json.loads((r/'analysis.json').read_text());assert a['intervention_calls']==392 and a['selected_rows']==6514
assert len(a['cases'])==8 and all(x['calls']==49 and x['changed_output_calls']>0 and x['layer0_routes_identical'] for x in a['cases'])
assert a['max_cpu_audit_relative_l2']<.004
rows=list(map(json.loads,(r/'results/requests.jsonl').read_text().splitlines()));tasks={x['id']:x for x in json.loads((r/'tasks.json').read_text())}
for row,check in zip(rows,a['cases']):
 assert row['id']==check['id']
 try:correct=json.loads(row['text'])==tasks[row['id'].split('-',1)[1]]['expected']
 except json.JSONDecodeError:correct=False
 assert correct==check['correct']
print('PASS:',len(m),'sealed files; eight complete requests; targeted replacement and CPU audit verified')
