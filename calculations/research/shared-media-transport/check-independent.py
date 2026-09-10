"""Independent prewritten scalar oracles and packet/credit conservation audit.

Does not import scheduling helpers or derive hand expectations from candidate output.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import copy
import hashlib
import importlib.util
import json

ROOT = Path(__file__).resolve().parent
START_SHA = hashlib.sha256((ROOT / 'calculate.py').read_bytes()).hexdigest()
scenario_evidence = {}
spec = importlib.util.spec_from_file_location('candidate_media', ROOT / 'calculate.py')
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
checks = []
failures = []

def eq(actual, expected, label):
    if actual != expected:
        raise AssertionError(f'{label}: {actual!r} != {expected!r}')

def run(name, fn):
    try:
        fn()
        checks.append(name)
    except Exception as exc:
        failures.append({'name': name, 'error': repr(exc)})

def packet(pid, stream=None, size=1, offset=0, direction='c2s', **kw):
    return dict(id=pid, stream=stream or pid, direction=direction,
                offset=offset, payload_bytes=size, **kw)

def base(packets):
    p = M.example()
    p['packets'] = packets
    p['businesses'] = []
    p['tasks'] = []
    return p

def records(r):
    return {x['id']: x for x in r['packets']}

def delivered(r, key):
    v = records(r)[key]['delivered']
    return None if v is None else F(v)

def business(r, key):
    return next(x for x in r['businesses'] if x['id'] == key)

def audit(r):
    p = r['inputs']
    nodes = {x['id']: x for x in p['packets']}
    out = records(r)
    stream_end = {}
    for x in p['packets']:
        key=(x['direction'],x['stream'])
        eq(x['offset'],stream_end.get(key,0),'disjoint contiguous input intervals')
        stream_end[key]=x['offset']+x['payload_bytes']
    tx = r['transmissions']
    bydirection = defaultdict(list)
    bypacket = defaultdict(list)
    credits = []
    arrival_first = {}
    for t in tx:
        d = t['direction']
        start, end, arrival = map(F, (t['start'], t['end'], t['arrival']))
        eq(end-start, F(8*t['wire_bytes'])/F(str(p[d+'_bits_per_second'])), 'serialization')
        eq(arrival-end, F(str(p[d+'_propagation_seconds'])), 'propagation')
        assert start >= F(str(p.get('connection_ready', 0)))
        bydirection[d].append((start, end))
        x = nodes[t['packet']]
        if t['kind'] == 'data':
            eq(d, x['direction'], 'data direction')
            eq((t['offset'], t['end_offset']), (x['offset'], x['offset']+x['payload_bytes']), 'interval identity')
            eq(t['wire_bytes'], x['payload_bytes']+p['header_bytes'], 'wire accounting')
            bypacket[x['id']].append(t)
            if not t['lost']:
                arrival_first[x['id']] = min(arrival, arrival_first.get(x['id'], arrival))
            if t['attempt'] == 1:
                credits.append((start, 1, x['id']))
        else:
            eq(d, 's2c' if x['direction']=='c2s' else 'c2s', 'ACK reverse direction')
            eq(t['wire_bytes'], p['ack_bytes'], 'ACK accounting')
            credits.append((arrival, 0, x['id']))
    for intervals in bydirection.values():
        intervals.sort()
        assert all(a[1] <= b[0] for a,b in zip(intervals, intervals[1:])), 'shared serializer overlap'
    for pid, sends in bypacket.items():
        eq([t['attempt'] for t in sends], list(range(1,len(sends)+1)), 'attempt sequence')
        assert len(sends) <= 2
        if len(sends)==2:
            assert sends[0]['lost'] and not sends[1]['lost']
            assert F(sends[1]['start']) >= F(str(nodes[pid]['recovery_ready']))
        eq(out[pid]['attempts'], len(sends), 'attempt output')
    # Independent unique coverage: input intervals are disjoint, retransmissions remain
    # separate wire entries but each first arrival contributes its interval exactly once.
    for pid,x in nodes.items():
        expected = arrival_first.get(pid)
        eq(None if out[pid]['received'] is None else F(out[pid]['received']), expected, 'first receipt')
    sums = r['summary']
    eq(sums['data_wire_bytes'], sum(t['wire_bytes'] for t in tx if t['kind']=='data'), 'data sum')
    eq(sums['ack_wire_bytes'], sum(t['wire_bytes'] for t in tx if t['kind']=='ack'), 'ACK sum')
    eq(sums['unique_received_payload_bytes'],sum(nodes[k]['payload_bytes'] for k in arrival_first),'unique received')
    eq(sums['unique_delivered_payload_bytes'],sum(nodes[k]['payload_bytes'] for k,v in out.items() if v['delivered'] is not None),'unique delivered')
    # Replay sender knowledge from actual ACK arrival, never from receiver state.
    outstanding=defaultdict(int); reliable=defaultdict(int); streams=defaultdict(int)
    sent=set(); acked=set()
    for at, typ, pid in sorted(credits):
        x=nodes[pid]; d=x['direction']; key=(d,x['stream']); n=x['payload_bytes']
        if typ==1:
            assert pid not in sent
            sent.add(pid); outstanding[d]+=n
            if x['reliable']:
                reliable[d]+=n; streams[key]+=n
        else:
            assert pid in sent
            assert arrival_first[pid] <= at
            if pid not in acked:
                acked.add(pid); outstanding[d]-=n
                if x['reliable']:
                    reliable[d]-=n; streams[key]-=n
        assert 0 <= outstanding[d] <= p['shared_credit_bytes']
        assert 0 <= reliable[d] <= p['reliable_receive_credit_bytes']
        assert 0 <= streams[key] <= p['stream_credit_bytes']
    eq(dict(sums['shared_outstanding_bytes']),{d:outstanding[d] for d in ('c2s','s2c')},'final credit')
    ack_counts=defaultdict(int)
    for t in tx:
        if t['kind']=='ack':
            ack_counts[t['packet']]+=1
            assert F(t['start']) >= arrival_first[t['packet']]
    for pid,sends in bypacket.items():
        eq(ack_counts[pid],sum(not t['lost'] for t in sends),'one ACK per received transmission')
    # Replay delivery dependencies over immutable arrivals, independent of scheduler.
    expected={}
    for i,x in enumerate(p['packets']):
        pid=x['id']
        if pid not in arrival_first:
            continue
        predecessors=[y['id'] for y in p['packets'][:i]
                      if x['reliable'] and y['reliable'] and y['direction']==x['direction']
                      and (p['delivery_mode']=='connection' or y['stream']==x['stream'])]
        if any(k not in expected for k in predecessors):
            continue
        at=max([arrival_first[pid]]+[expected[k] for k in predecessors])
        if x['allow_expire'] and at > F(str(x['deadline'])):
            continue
        expected[pid]=at
    for pid in nodes:
        eq(delivered(r,pid),expected.get(pid),'delivery dependency')
    # Verify work and dependent sends use application delivery, not mere receipt.
    done=dict(expected)
    done.update({w['id']: F(w['end']) for w in r['work']})
    worknodes={x['id']:x for x in p.get('tasks',[])}
    workresources=defaultdict(list)
    for w in r['work']:
        x=worknodes[w['id']]; start,end=F(w['start']),F(w['end'])
        eq(end-start,F(str(x['duration'])),'work duration')
        assert start >= F(str(x['ready']))
        assert all(start>=done[k] for k in x['dependencies'])
        workresources[(x.get('endpoint','server'),w['resource'])].append((start,end))
    for intervals in workresources.values():
        intervals.sort()
        assert all(a[1]<=b[0] for a,b in zip(intervals,intervals[1:]))
    for t in tx:
        if t['kind']=='data':
            x=nodes[t['packet']]
            assert F(t['start'])>=F(str(x['ready']))
            assert all(F(t['start'])>=done[k] for k in x['dependencies'])
    for b in p.get('businesses',[]):
        row=business(r,b['id'])
        if b['kind']!='tts':
            values=[expected.get(k) for k in b['required']]
            at=max(values) if all(v is not None for v in values) else None
            eq(None if row['complete'] is None else F(row['complete']),at,'business complete')
            usable=at is not None
            if usable and b['kind']=='screenshot':
                changes=[c for c in b.get('version_changes',[]) if F(str(c['at']))<=at]
                usable=not changes or changes[-1]['version']==b['version']
            eq(row['usable'],usable,'business usability')
            if b.get('preview_required'):
                vs=[expected.get(k) for k in b['preview_required']]
                at=max(vs) if all(v is not None for v in vs) else None
                eq(None if row['preview_complete'] is None else F(row['preview_complete']),at,'preview separate delivery')
        else:
            deliveries=[max(expected[k] for k in block['packets']) if all(k in expected for k in block['packets']) else None for block in b['blocks']]
            if b['playback']=='slots':
                mask=[a is not None and a<=F(str(block['slot_start'])) for a,block in zip(deliveries,b['blocks'])]
                eq([v['played'] for v in row['blocks']],mask,'slot admission')
                first=next((F(str(block['slot_start'])) for block,ok in zip(b['blocks'],mask) if ok),None)
                eq(None if row['first_play'] is None else F(row['first_play']),first,'first useful slot')
                eq(F(row['playback_end']),F(str(b['blocks'][-1]['slot_start']))+F(str(b['blocks'][-1]['duration'])),'fixed timeline end')
                eq(row['complete_playback'],all(mask),'slot full playback flag')
                eq(F(row['missing_seconds']),sum((F(str(block['duration'])) for block,ok in zip(b['blocks'],mask) if not ok),F(0)),'slot missing accounting')
            else:
                intervals=[];end=None;stall=F(0)
                for a,block in zip(deliveries,b['blocks']):
                    if a is None:break
                    start=a if end is None else max(a,end)
                    if end is not None:stall+=start-end
                    end=start+F(str(block['duration']));intervals.append((start,end))
                eq([(F(v['start']),F(v['end'])) for v in row['blocks']],intervals,'reliable playback recurrence')
                eq(F(row['stall_seconds']),stall,'stall accounting')
                eq(None if row['first_play'] is None else F(row['first_play']),intervals[0][0] if intervals else None,'first reliable playback')
                eq(row['complete_playback'],len(intervals)==len(b['blocks']),'reliable full playback flag')
    return r

def calc(p):
    return audit(M.calculate(copy.deepcopy(p)))

def hol():
    p=M.example(); a=calc(p)
    eq((delivered(a,'A0'),delivered(a,'B1')),(F(3),F(7)),'HOL independent')
    p['delivery_mode']='connection'; b=calc(p)
    eq((delivered(b,'A0'),delivered(b,'B1')),(F(7),F(7)),'HOL global')
    eq(a['transmissions'],b['transmissions'],'same wire')
    eq(a['summary']['data_wire_bytes'],4,'HOL wire')
    eq(a['summary']['unique_received_payload_bytes'],3,'HOL unique')

def priority():
    p=base([packet(f'B{i}','B',offset=i) for i in range(4)]+[packet('A',ready=1,priority=10)])
    a=calc(p); eq((delivered(a,'B3'),delivered(a,'A')),(F(5),F(6)),'FIFO')
    p['scheduler']='priority'; b=calc(p)
    eq((delivered(b,'B3'),delivered(b,'A')),(F(6),F(3)),'priority')
    p=base([packet('B',size=4),packet('A',ready=1,priority=10)]);p['scheduler']='priority'
    c=calc(p);eq(delivered(c,'A'),F(6),'nonpreemption')

def credit():
    for split in (False,True):
        p=base([packet(str(i),str(i) if split else 'shared',offset=0 if split else i) for i in range(3)])
        p['shared_credit_bytes']=2;r=calc(p)
        eq([F(t['start']) for t in r['transmissions'] if t['kind']=='data'],list(map(F,[0,1,4])),'shared start')
        eq([F(t['arrival']) for t in r['transmissions'] if t['kind']=='ack'][:2],[F(4),F(5)],'ACK visibility')

def playback():
    p=base([packet(str(i),'voice',offset=i,ready=t) for i,t in enumerate([1,4,5])])
    p['businesses']=[dict(id='voice',kind='tts',playback='reliable',blocks=[dict(packets=[str(i)],duration=2,slot_start=3+2*i) for i in range(3)])]
    r=calc(p);v=business(r,'voice')
    eq([(F(x['start']),F(x['end'])) for x in v['blocks']],[(F(3),F(5)),(F(6),F(8)),(F(8),F(10))],'reliable playback')
    eq(F(v['stall_seconds']),F(1),'stall')
    p['businesses'][0]['playback']='slots';r=calc(p);v=business(r,'voice')
    eq([x['played'] for x in v['blocks']],[True,False,True],'slot equality')
    eq((F(v['missing_seconds']),F(v['playback_end'])),(F(2),F(9)),'missing duration')

def image():
    p=M.example();p['tasks']=[dict(id='model',dependencies=['B0','B1'],duration=2)]
    p['packets'].append(packet('final',size=2,direction='s2c',dependencies=['model']))
    p['businesses']=[dict(id='final',kind='image',required=['final'])]
    r=calc(p);eq(delivered(r,'final'),F(12),'full image')
    eq((F(r['work'][0]['start']),F(r['work'][0]['end'])),(F(7),F(9)),'full image barrier')

def cancellation():
    p=base([packet('up'),packet('cancel',ready=2,cancel_targets=['request']),packet('response',direction='s2c',dependencies=['model'],cancel_tag='request')])
    p['tasks']=[dict(id='model',duration=3,dependencies=['up'],cancel_tag='request')]
    r=calc(p)
    eq(F(r['cancellations'][0]['at']),F(4),'cancel propagation')
    eq((F(r['work'][0]['start']),F(r['work'][0]['end'])),(F(2),F(5)),'running work remains')
    eq(records(r)['response']['attempts'],0,'unsent output cancelled')

def datagram_credit():
    p=base([packet('unreliable',size=2,reliable=False),packet('reliable',size=1)])
    p['shared_credit_bytes']=2;p['reliable_receive_credit_bytes']=1;p['stream_credit_bytes']=1
    r=calc(p);eq(delivered(r,'unreliable'),F(3),'datagram bypass receive credit')
    starts={t['packet']:F(t['start']) for t in r['transmissions'] if t['kind']=='data'}
    eq(starts['reliable'],F(5),'datagram shares send credit')
    p['packets'][0]['drop_first']=True;r=calc(p)
    eq(records(r)['reliable']['attempts'],0,'lost datagram retains sender credit')
    eq(r['summary']['shared_outstanding_bytes']['c2s'],2,'no omniscient release')

def deadline():
    for deadline_at,expected in [(2,F(2)),('199/100',None)]:
        p=base([packet('a',reliable=False,allow_expire=True,deadline=deadline_at)])
        r=calc(p);eq(delivered(r,'a'),expected,'arrival/deadline tie')
        eq(r['summary']['data_wire_bytes'],1,'late wire not refunded')
    p=base([packet('a',ready=3,reliable=False,allow_expire=True,deadline=2)])
    r=calc(p);eq(r['summary']['data_wire_bytes'],0,'unsent expiry')

def unreliable_hol():
    p=base([packet('lost',reliable=False,drop_first=True),packet('reliable')]);p['delivery_mode']='connection'
    r=calc(p);eq(delivered(r,'reliable'),F(3),'datagram does not HOL reliable')
    eq(F(r['delivery_only_replay']['connection']['reliable']),F(3),'replay semantics')

def invalid():
    mutations=[
        lambda p:p.update(c2s_bits_per_second=0),
        lambda p:p.update(shared_credit_bytes=True),
        lambda p:p['packets'][0].update(offset=1),
        lambda p:p['packets'][0].update(allow_expire=True,deadline=2),
        lambda p:p['packets'][0].update(dependencies=['missing']),
        lambda p:p['packets'][0].update(dependencies=['a']),
        lambda p:p['packets'][0].update(reliable=False,recovery_ready=5,drop_first=True),
    ]
    for mutate in mutations:
        p=base([packet('a')]);mutate(p)
        try:M.calculate(p)
        except ValueError:continue
        raise AssertionError('invalid input accepted')

def business_receivers():
    cases=[]
    p=base([packet('up'),packet('down',direction='s2c')]);p['businesses']=[dict(id='both',kind='asr',required=['up','down'])];cases.append(p)
    p=base([packet('up'),packet('down',direction='s2c')]);p['businesses']=[dict(id='both',kind='tts',playback='reliable',blocks=[dict(packets=['up'],duration=1),dict(packets=['down'],duration=1)])];cases.append(p)
    p=base([packet('unreliable',reliable=False,allow_expire=True,deadline=5)]);p['businesses']=[dict(id='image',kind='image',required=['unreliable'])];cases.append(p)
    for p in cases:
        try:M.calculate(p)
        except ValueError:continue
        raise AssertionError('invalid mixed receiver/reliable-image business accepted')

def scenario_check(name,p):
    r=calc(p)
    directions={}
    for d in ('c2s','s2c'):
        ts=[t for t in r['transmissions'] if t['direction']==d]
        directions[d]=dict(data_payload=sum(t['payload_bytes'] for t in ts if t['kind']=='data'),data_wire=sum(t['wire_bytes'] for t in ts if t['kind']=='data'),ack_wire=sum(t['wire_bytes'] for t in ts if t['kind']=='ack'),recovery_payload=sum(t['payload_bytes'] for t in ts if t['kind']=='data' and t['attempt']>1))
    if name=='image-30mb-5mb':
        eq(directions['c2s']['data_payload'],30000000,'actual full upload')
        eq(directions['s2c']['data_payload'],5000000,'actual full response')
        eq(directions['c2s']['recovery_payload']+directions['s2c']['recovery_payload'],0,'lossless image baseline')
        eq(r['summary']['unique_delivered_payload_bytes'],35000000,'full unique image bytes')
    scenario_evidence[name]=dict(directions=directions,businesses=r['businesses'],unfinished=r['unfinished'])

def scheduling_isolation():
    p=base([packet('a')]);p['scheduler']='priority'
    p['tasks']=[dict(id='first',duration=1,priority=0),dict(id='second',duration=1,priority=10)]
    r=calc(p);eq([x['id'] for x in r['work']],['first','second'],'network policy does not alter CPU')
    p['compute_scheduler']='priority';r=calc(p)
    eq([x['id'] for x in r['work']],['second','first'],'explicit CPU priority')
    scenarios=M.scenarios()
    a=copy.deepcopy(scenarios['mixed-fifo']);b=copy.deepcopy(scenarios['mixed-priority'])
    a.pop('scheduler');b.pop('scheduler');eq(a,b,'mixed pair changes network policy only')

def cancel_requires_delivery():
    for mode,at in [('connection',7),('per_stream',3)]:
        p=M.example();p['delivery_mode']=mode;p['packets'][1]['cancel_targets']=['job']
        p['tasks']=[dict(id='job',duration=2,ready=4,cancel_tag='job')]
        r=calc(p);eq(F(r['cancellations'][0]['at']),F(at),'cancel follows application delivery')
        eq(len(r['work']),1 if mode=='connection' else 0,'HOL changes remote knowledge')

def unfinished_business():
    p=base([packet('a'),packet('b','a',offset=1,drop_first=True)])
    p['businesses']=[dict(id='voice',kind='tts',playback='reliable',blocks=[dict(packets=['a'],duration=1),dict(packets=['b'],duration=1)])]
    r=calc(p);v=business(r,'voice')
    eq(v['complete_playback'],False,'partial prefix is not complete')
    eq(v['unresolved_blocks'],1,'unresolved media')
    eq(r['summary']['all_businesses_usable'],False,'partial business')
    p=base([packet('a',ready=1,reliable=False,allow_expire=True,deadline=0)])
    p['businesses']=[dict(id='voice',kind='tts',playback='slots',blocks=[dict(packets=['a'],duration=1,slot_start=0)])]
    r=calc(p);eq(r['unfinished'],[],'expired network quiescent')
    eq(r['summary']['all_businesses_usable'],False,'quiescent is not usable')
    eq(business(r,'voice')['complete_playback'],False,'missing slot not complete')

def sources():
    lock=json.loads((ROOT/'sources.lock.json').read_text())
    eq(len(lock),6,'source count')
    for s in lock:
        raw=(ROOT/s['file']).read_bytes()
        eq(len(raw),s['bytes'],'source bytes');eq(hashlib.sha256(raw).hexdigest(),s['sha256'],'source hash')

def cancellation_endpoints():
    p=base([packet('cancel',cancel_targets=['tag']),packet('client_future',ready=2,cancel_tag='tag'),packet('server_future',direction='s2c',ready=2,cancel_tag='tag')])
    p['tasks']=[dict(id='client_work',endpoint='client',ready=2,duration=1,cancel_tag='tag'),dict(id='server_work',endpoint='server',ready=2,duration=1,cancel_tag='tag')]
    r=calc(p)
    eq(records(r)['client_future']['attempts'],1,'client does not know remote cancellation')
    eq(records(r)['server_future']['attempts'],0,'cancel arrival before same-time send')
    eq([x['id'] for x in r['work']],['client_work'],'cancel endpoint/task tie')
    p=base([packet('cancel',cancel_targets=['tag']),packet('running',size=4,direction='s2c',cancel_tag='tag')])
    r=calc(p);eq(delivered(r,'running'),F(5),'inflight remains after cancel')

def screenshot_version():
    for at, usable in [(2,False),('201/100',True)]:
        p=base([packet('shot',direction='s2c')]);p['businesses']=[dict(id='s',kind='screenshot',required=['shot'],version='v1',version_changes=[dict(at=at,version='v2')])]
        r=calc(p);eq(business(r,'s')['usable'],usable,'version at completion')

def invalid_business():
    cases=[]
    p=base([packet('up'),packet('wrong_dep',dependencies=['up'])]);cases.append(p)
    p=base([packet('a')]);p['businesses']=[dict(id='b',kind='tts',playback='typo',blocks=[dict(packets=['a'],duration=1)])];cases.append(p)
    p=base([packet('a')]);p['businesses']=[dict(id='b',kind='tts',playback='reliable',blocks=[dict(packets=['a'],duration=-1)])];cases.append(p)
    p=base([packet('a')]);p['businesses']=[dict(id='b',kind='image',required=[])];cases.append(p)
    p=base([packet('a')]);p['businesses']=[dict(id='b',kind='screenshot',required=['a'],version='v1',version_changes=[dict(at=2,version='v2'),dict(at=1,version='v3')])];cases.append(p)
    for p in cases:
        try:M.calculate(p)
        except ValueError:continue
        raise AssertionError('invalid business/dependency accepted')

for name,fn in [('sources',sources),('A_HOL',hol),('B_priority',priority),('C_credit',credit),('D_playback',playback),('E_image',image),('E_cancel',cancellation),('datagram_credit',datagram_credit),('deadline_ties',deadline),('unreliable_HOL',unreliable_hol),('invalid_inputs',invalid),('cancel_endpoints',cancellation_endpoints),('screenshot_version',screenshot_version),('invalid_business',invalid_business),('business_receivers',business_receivers),('scheduling_isolation',scheduling_isolation),('cancel_requires_delivery',cancel_requires_delivery),('unfinished_business',unfinished_business)]:
    run(name,fn)
if hasattr(M,'scenarios'):
    scenarios=M.scenarios()
    if isinstance(scenarios,dict):
        for name,p in scenarios.items():
            run('scenario_'+name,lambda p=p,name=name:scenario_check(name,p))
END_SHA=hashlib.sha256((ROOT/'calculate.py').read_bytes()).hexdigest()
if END_SHA!=START_SHA:failures.append(dict(name='source_stable',error='candidate changed while checker ran'))
result=dict(scenario_evidence=scenario_evidence,status='PASS' if not failures else 'FAIL',candidate_sha256=START_SHA,passed=checks,failures=failures)
(ROOT/'check-independent.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='scenario_evidence'},indent=2))
raise SystemExit(bool(failures))
