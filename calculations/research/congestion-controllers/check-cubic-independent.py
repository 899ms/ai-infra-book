"""Source-derived scalar oracles; does not call curve/root helpers for expected values."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import importlib.util
import json
ROOT=Path(__file__).resolve().parent
START=hashlib.sha256((ROOT/'cubic.py').read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('cubic_checked',ROOT/'cubic.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
passed=[];failures=[]
def eq(a,b):
    if a!=b:raise AssertionError(f'{a!r} != {b!r}')
def run(name,fn):
    try:fn();passed.append(name)
    except Exception as e:failures.append(dict(name=name,error=repr(e)))
def base():
    return dict(initial=dict(phase='avoidance',cwnd='484/5',ssthresh=70,w_max=100,cwnd_epoch='484/5',w_est='484/5',cwnd_prior=100),events=[])
def ack(t,n=1):return dict(type='ack',at=t,segments_acked=n,smoothed_rtt=1)
def calc(p):return M.calculate(p)
def curve():
    p=base();p['events']=[dict(type='observe',at=t) for t in (0,2,3)];r=calc(p)
    eq([list(map(F,x['state']['curve_bounds'])) for x in r['events']],[[F(484,5)]*2,[F(100)]*2,[F(502,5)]*2])
    eq(F(r['final']['cwnd']),F(484,5))
def concave():
    p=base();p['events']=[ack(2)];r=calc(p)
    eq(F(r['final']['cwnd']),F(117173,1210));eq(F(r['final']['w_est']),F(3982577,41140))
    eq(r['events'][0]['detail']['region'],'cubic')
def reno():
    p=base();p['events']=[ack(0)];r=calc(p)
    eq(F(r['final']['cwnd']),F(3982577,41140));eq(r['events'][0]['detail']['region'],'reno-friendly')
def delayed():
    p=base();p['initial'].update(cwnd=100,cwnd_epoch=100,w_max=100,w_est=100,cwnd_prior=200);p['events']=[ack(100,8)]
    r=calc(p);eq(F(r['final']['cwnd']),F(201,2));eq(F(r['events'][0]['detail']['target']),150)
def alpha():
    p=base();p['initial'].update(cwnd=100,w_est='1691/17');p['events']=[ack(0,100)];r=calc(p)
    eq(F(r['final']['w_est']),100);eq(F(r['final']['alpha']),1)
def loss():
    p=base();p.update(fast_convergence=True);p['initial'].update(cwnd=80,cwnd_epoch=80,w_est=80)
    p['events']=[dict(type='congestion',at=1,event_id='loss',flight_size=50)]
    r=calc(p);eq([F(r['final'][k]) for k in ('cwnd_prior','w_max','ssthresh','cwnd')],[80,68,35,35])
def idle():
    p=base();p['events']=[dict(type='limited_start',at=1,reason='application'),dict(type='limited_end',at=101),ack(102)];r=calc(p)
    eq(F(r['final']['epoch_elapsed']),2);eq(F(r['final']['cwnd']),F(117173,1210))
def startup():
    for count,want in ((0,10),('1/2',F(21,2)),(8,11)):
        r=calc(dict(initial=dict(cwnd=10,ssthresh=20),events=[ack(0,count)]));eq(F(r['final']['cwnd']),want)
def timeout():
    p=base();p['initial'].update(cwnd=80);p['events']=[dict(type='timeout',at=1,event_id='RTO',flight_size=50)];r=calc(p)
    eq(F(r['final']['cwnd']),1);eq(F(r['final']['ssthresh']),35)
def invalid():
    cases=[dict(initial=dict(cwnd=True)),dict(beta=1),dict(startup_policy='hystart++'),dict(initial=dict(phase='unknown'))]
    for e in (dict(type='ack',at=0,segments_acked=-1,smoothed_rtt=1),dict(type='ack',at=0,segments_acked=1,smoothed_rtt=0),dict(type='typo',at=0),dict(type='limited_end',at=0),dict(type='recovery_exit',at=0),dict(type='congestion',at=0,event_id='e',flight_size=10,signal='ECN')):
        p=base();p['events']=[e];cases.append(p)
    cases.extend([dict(unrecognized=True),dict(initial=dict(unrecognized=1))])
    p=base();p['events']=[dict(ack(0),unrecognized=True)];cases.append(p)
    p=base();p['events']=[dict(type='limited_start',at=1,reason='application'),dict(type='idle_restart',at=2,idle_duration=10,rto=1)];cases.append(p)
    for p in cases:
        try:calc(p)
        except ValueError:continue
        raise AssertionError('invalid accepted '+repr(p))
for n,f in [('curve',curve),('concave_ack',concave),('reno_friendly',reno),('delayed_ACK',delayed),('alpha_equality',alpha),('prior_vs_flight',loss),('idle_exclusion',idle),('Reno_startup',startup),('TCP_timeout',timeout),('invalid_inputs',invalid)]:run(n,f)
END=hashlib.sha256((ROOT/'cubic.py').read_bytes()).hexdigest()
if START!=END:failures.append(dict(name='stable_source',error='concurrent modification'))
r=dict(status='PASS' if not failures else 'FAIL',candidate_sha256=START,passed=passed,failures=failures)
(ROOT/'cubic-independent-check.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));raise SystemExit(bool(failures))
