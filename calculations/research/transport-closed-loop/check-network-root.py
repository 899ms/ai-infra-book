from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,hashlib
root=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('network',root/'calculate.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
hashes={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in ['calculate.py','sender.py']}
checks=[]
x=m.example();x.update(upload_bytes=3504,response_bytes=0,model_seconds=0,until=20,routers={'up':{'rate_bps':4912,'queue_bytes':0,'propagation':0}})
r=m.calculate(x)
data=[t for t in r['transmissions'] if t['direction']=='up']
assert [(t['pn'],t['send_start'],t.get('received_at')) for t in data]==[(0,'0','4'),(1,'1',None),(2,'6','10'),(3,'12','16')]
assert [(t['pn'],t['at']) for t in r['losses']['up']]==[(1,'12')]
assert r['business']['upload']=='16'
checks.append('zero waiting buffer drops PN1 at router; sender loss at12, complete16')
x=m.example();x['until']='1/2';r=m.calculate(x)
assert r['summary']['wire_bytes']==1228 and F(r['summary']['serialized_wire_bytes_by_horizon'])==614
assert r['business']['upload'] is None and not r['summary']['complete']
checks.append('half-serialized packet is 614 actual bytes, not1228 or completed business')
x=m.example();x.update(receive_window=0,until=10);r=m.calculate(x)
assert not r['transmissions'] and not r['summary']['complete']
checks.append('zero absolute credit produces no wire packets and no completion')
x=m.example();x['explicit_consumption']=[dict(direction='up',at=0,upto=1168)]
try:m.calculate(x)
except ValueError:pass
else:raise AssertionError('Consumption before receive accepted')
checks.append('cannot consume bytes before actual receive')
assert hashes=={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in hashes}
(root/'network-root-check.json').write_text(json.dumps(dict(status='passed',hashes=hashes,checks=checks,scope='Four independent finite network/receiver boundaries; large traffic separately audited'),indent=2)+'\n')
print('Passed four independent network boundaries')
