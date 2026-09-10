import hashlib,json,subprocess,sys
from pathlib import Path
r=Path(__file__).absolute().parent;m=json.loads((r/'manifest.json').read_text())
for n,h in m.items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h,n
for name in ['run','matrix-run']:
 s=json.loads((r/name/'supervisor.json').read_text());assert s['exit_code']==0 and s['reason'] is None and s['leftovers']=={}
subprocess.run([sys.executable,str(r/'analyze_matrix.py'),'--output',str(r/'matrix-results')],check=True)
s=json.loads((r/'capture-audit.json').read_text());assert s['total_calls']==196 and s['selected_rows']==3257 and all(c['outputs_and_routes_equal'] for c in s['cases']) and s['runtime_weight_matches_checkpoint_transpose']
print('PASS:',len(m),'files; complete successful executions; numerical quality failures retained')
