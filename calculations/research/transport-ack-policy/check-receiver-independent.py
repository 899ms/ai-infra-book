"""Independent fixed arithmetic and boundary checks; does not derive expectations from snapshots."""
from pathlib import Path
import importlib.util
import hashlib
import json
from fractions import Fraction as F

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('ack_receiver_review', ROOT / 'receiver.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
checks = []
source_before = hashlib.sha256((ROOT/'receiver.py').read_bytes()).hexdigest()
def new(**kw):
    return m.Receiver(dict(mode='count_or_timer', **kw))
def check(name, fn):
    fn()
    checks.append(name)
def snap(r, at, capacity=1200):
    return r.snapshot(F(at), capacity)
def eq(actual, expected):
    assert actual == expected, (actual, expected)

def pair():
    r=new(max_delay='0.025'); eq(r.receive(0,0,True),False); eq(r.receive(1,'0.005',True),True)
    s=snap(r,'0.005'); eq(s['ranges'],[[0,1]]); eq(F(s['raw_delay']),0)
check('pair-count-fixed-arithmetic',pair)
def tail():
    r=new(max_delay='0.025');r.receive(0,0,True);eq(r.expire(F(1,40),r.generation),True)
    s=snap(r,'0.025');eq(s['encoded_delay'],3125);eq(F(s['decoded_delay']),F(1,40))
check('tail-25ms-3125ticks',tail)
def queued():
    r=new(max_delay='0.025');r.receive(0,0,True);r.expire(F(1,40),r.generation);r.receive(1,'0.029',True)
    s=snap(r,'0.030');eq(s['ranges'],[[0,1]]);eq(s['encoded_delay'],125);eq(F(s['raw_delay']),F(1,1000))
check('queued-snapshot-refresh',queued)
def largest():
    r=new(every=1);r.receive(2,'0.020',True);r.receive(0,'0.029',True)
    s=snap(r,'0.030');eq(s['ranges'],[[0,0],[2,2]]);eq(s['encoded_delay'],1250)
check('largest-PN-not-latest-arrival',largest)
def duplicate():
    r=new(every=1);r.receive(7,'0.010',True);snap(r,'0.010');r.receive(7,'0.020',True)
    s=snap(r,'0.021');eq(F(s['raw_delay']),F(11,1000));eq(r.state()['received_count'],1)
check('duplicate-preserves-first-time',duplicate)
def floor():
    r=new(every=1);r.receive(0,0,True);s=snap(r,'0.001003');eq(s['encoded_delay'],125);eq(F(s['encoding_error']),F(-3,1000000))
check('floor-residual-three-us',floor)
def capacity():
    r=new(every=1)
    for pn in range(0,512,2):r.receive(pn,0,True)
    before=r.state()
    try:snap(r,0,64)
    except ValueError:pass
    else:raise AssertionError('64B accepted 256 ranges')
    eq(r.state(),before)
    s=snap(r,0,541);eq(s['frame_bytes'],517);eq(len(s['ranges']),256)
check('256-singletons-517B-frame-atomic-rejection',capacity)
def pure():
    r=new();eq(r.receive(0,0,False),False);eq(r.deadline,None);eq(r.queued,False)
    r.receive(1,'0.001',True);r.receive(2,'0.002',False);r.expire(F(11,1000),r.generation)
    s=snap(r,'0.011');eq(s['ranges'],[[0,2]]);eq(F(s['raw_delay']),F(9,1000))
check('pure-ACK-no-trigger-but-included',pure)
def tied():
    r=new(max_delay='0.025');r.receive(0,0,True);g=r.generation;r.receive(1,'0.025',True)
    eq(r.expire(F(1,40),g),False);s=snap(r,'0.025');eq(s['encoded_delay'],0)
    eq(r.expire(F(1,40),g),False);eq(len([e for e in r.events if e['event']=='start']),1)
check('arrival-timer-tie-single-ACK',tied)
def immutable():
    r=new(every=1);r.receive(0,0,True);s=snap(r,1);r.receive(1,2,True)
    eq(s['ranges'],[[0,0]]);eq(r.state()['pending'],[1])
check('started-snapshot-not-rewritten',immutable)
def retention():
    r=new(every=1,retain_packets=2)
    for pn in range(3):r.receive(pn,pn,True);snap(r,pn)
    eq(r.state()['retained'],[1,2]);eq(r.state()['received_count'],3)
    r.receive(0,4,True);s=snap(r,4);eq(s['ranges'],[[0,2]]);eq(r.state()['received_count'],3)
check('omitted-old-range-remains-duplicate-safe',retention)
for key,value in [('delay_exponent',21),('delay_exponent',True),('every',0),('every',True),('max_delay','0.0001'),('max_delay','16.384'),('retain_packets',0),('reorder_immediate',1)]:
    try:new(**{key:value})
    except (ValueError,TypeError):checks.append('reject-'+key+'-'+str(value))
    else:raise AssertionError((key,value))
source_after=hashlib.sha256((ROOT/'receiver.py').read_bytes()).hexdigest();eq(source_before,source_after)
result=dict(status='PASS',scope='Independent receiver arithmetic and input checks only; no network or sender correctness claim',source_sha256=source_after,checks=checks,count=len(checks))
(ROOT/'receiver-independent.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
