"""Compile fixed upstream minmax unchanged and compare whole sample state."""
from pathlib import Path
import hashlib
import json
import random
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import bbr_minmax as M
import bbr_reference as B
hashes={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ('bbr_minmax.py','bbr_reference.py')}
rows=json.loads((ROOT/'bbr-sources.lock.json').read_text())['sources']
for row in rows:
    b=(ROOT/row['file']).read_bytes()
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
h=(ROOT/'bbr-sources/win_minmax.h').read_text()
c=(ROOT/'bbr-sources/win_minmax.c').read_text()
# Only kernel include plumbing is removed; all selected algorithms remain unchanged.
def without_includes(s):return '\n'.join(l for l in s.splitlines() if not l.startswith('#include'))
program='''#include <stdint.h>
#include <stdio.h>
typedef uint32_t u32;
#define unlikely(x) (x)
#define EXPORT_SYMBOL(x)
'''+without_includes(h)+'\n'+without_includes(c)+'''
int main(void) {
 struct minmax m; char op; unsigned a,b,c;
 while (scanf(" %c %u %u %u", &op,&a,&b,&c)==4) {
  if(op=='R') minmax_reset(&m,a,b); else minmax_running_max(&m,a,b,c);
  printf("%u %u %u %u %u %u\\n",m.s[0].t,m.s[0].v,m.s[1].t,m.s[1].v,m.s[2].t,m.s[2].v);
 }
 return 0;
}
'''
commands=[];expected=[]
def append(op,a,b,c=0):
    global model
    if op=='R':model=M.RunningMax(a,b)
    else:model.update(a,b,c)
    commands.append(f'{op} {a} {b} {c}')
    expected.append(' '.join(str(v) for x in model.samples for v in (x.t,x.v)))
# Strict window, quarter/half-window, repeated timestamp, equality and wrap.
for start in (0,2**32-8):
    append('R',start,100)
    for dt,value in [(0,99),(2,98),(3,97),(5,96),(6,95),(10,94),(11,93),(12,100),(12,100),(23,1)]:
        append('U',10,(start+dt)&0xffffffff,value)
rng=random.Random(94389002)
for trial in range(12):
    t=0 if trial%2==0 else 2**32-20
    append('R',t,rng.randrange(100))
    for i in range(400):
        t=(t+rng.randrange(5))&0xffffffff
        append('U',10 if trial<6 else 17,t,rng.randrange(150))
with tempfile.TemporaryDirectory(prefix='minmax-oracle-') as td:
    source=Path(td)/'oracle.c';binary=Path(td)/'oracle';source.write_text(program)
    subprocess.run(['clang','-std=c11','-O2',str(source),'-o',str(binary)],check=True,capture_output=True,text=True)
    actual=subprocess.run([str(binary)],input='\n'.join(commands)+'\n',capture_output=True,text=True,check=True).stdout.splitlines()
assert actual==expected, next(((i,a,e) for i,(a,e) in enumerate(zip(actual,expected)) if a!=e), 'length mismatch')
invalid=[];failures=[]
def reject(name,fn):
    try:fn()
    except (ValueError,TypeError):invalid.append(name)
    else:failures.append(name)
for field,value in [('t',True),('t',-1),('t',2**32),('value','3'),('value',1.5)]:
    args={'t':0,'value':0};args[field]=value
    reject('reset_'+field+'_'+repr(value),lambda args=args:M.RunningMax(**args))
for args in [(True,1,1),(10,-1,1),(10,0,2**32),(10,0,False)]:
    reject('update_'+repr(args),lambda args=args:M.RunningMax().update(*args))
for kwargs in ({'rtt_cnt':True},{'full_bw':2**32},{'mode':'TYPO'}):
    reject('seed_'+repr(kwargs),lambda kwargs=kwargs:B.StartupDrain(**kwargs))
for sample in ({'valid':1,'prior_delivered':0,'is_app_limited':False},{'valid':True,'prior_delivered':0,'is_app_limited':'false'}):
    reject('sample_'+repr(sample),lambda sample=sample:B.StartupDrain().update(sample=sample,total_delivered=1,filtered_max_bw=1000,packets_in_net_at_edt=100,drain_target=10))
result=dict(status='PASS' if not failures else 'FAIL',source_math='unchanged fixed Linux minmax C functions; kernel include/macro plumbing only',state_comparisons=len(actual),passed_invalid_inputs=invalid,accepted_invalid_inputs=failures,candidate_hashes=hashes)
for n,sha in hashes.items():
    if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=sha:
        result['status']='FAIL';result.setdefault('concurrent_changes',[]).append(n)
(ROOT/'minmax-boundary-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(result['status']!='PASS')
