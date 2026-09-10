"""Independent scalar expectations and sender-ledger conservation for stage one."""
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
import hashlib
import importlib.util
import json
import copy
ROOT=Path(__file__).resolve().parent
START=hashlib.sha256((ROOT/'calculate.py').read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('feedback_candidate',ROOT/'calculate.py')
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
passed=[];failures=[];evidence={}

def eq(a,b,label=''):
    if a!=b:raise AssertionError(f'{label}: {a!r} != {b!r}')

def run(name,fn):
    try:fn();passed.append(name)
    except Exception as e:failures.append(dict(name=name,error=repr(e)))

def base(events,until='0.4',**kw):
    return dict(max_datagram_size=1200,initial_max_data=1000000,
                initial_max_stream_data={'A':1000000,'B':1000000},events=events,until=until,**kw)

def sent(pn,at,offset=0,length=100,stream='A',**kw):
    return dict(type='sent',pn=pn,at=at,sent_bytes=1200,
                frames=[dict(type='stream',stream=stream,offset=offset,length=length)],**kw)

def ack(at,lo,hi=None,**kw):
    return dict(type='ack',at=at,ranges=[[lo,lo if hi is None else hi]],**kw)

def seed():
    return dict(latest_rtt='0.1',smoothed_rtt='0.1',rttvar='0.05',min_rtt='0.1',first_sample_at=-1)

def audit(r):
    history={};acknowledged=set();lost=set();coverage=defaultdict(set)
    # Reconstruct accounting from explicit transmissions and newly-lost facts.
    # Loss timing itself is checked by separate independent scalar oracles.
    for row in r['events']:
        e=row['input'];at=F(row['at'])
        if row['event']=='sent':
            assert e['pn'] not in history
            history[e['pn']]=e
            eq(list(history),list(range(len(history))),'monotone fresh PN')
        if row['event']=='ack':
            numbers={pn for lo,hi in e['ranges'] for pn in range(lo,hi+1)}
            assert numbers<=history.keys()
            for pn in numbers:
                assert F(str(history[pn]['at']))<=at
                acknowledged.add(pn)
                for frame in history[pn].get('frames',[]):
                    if frame['type']=='stream':
                        coverage[frame['stream']].update(range(frame['offset'],frame['offset']+frame['length']))
        lost.update(row['details'].get('newly_lost',[]))
        flight=sum(h['sent_bytes'] for pn,h in history.items()
                   if h.get('in_flight',True) and pn not in acknowledged and pn not in lost)
        eq(row['state']['bytes_in_flight'],flight,'flight once per transmission')
        maxima={}
        for h in history.values():
            for frame in h.get('frames',[]):
                if frame['type']=='stream':
                    maxima[frame['stream']]=max(maxima.get(frame['stream'],0),frame['offset']+frame['length'])
        eq(row['state']['max_data_consumed'],sum(maxima.values()),'absolute flow usage')
        eq(row['state']['stream_highest_sent_offsets'],maxima,'stream highest offset')
    eq(r['summary']['sent_udp_payload_bytes'],sum(h['sent_bytes'] for h in history.values()),'wire bytes')
    eq(r['summary']['stream_payload_transmission_bytes'],sum(f['length'] for h in history.values() for f in h.get('frames',[]) if f['type']=='stream'),'repeated stream wire')
    eq(r['sender_confirmed_business']['unique_stream_bytes'],sum(map(len,coverage.values())),'unique acknowledged data')
    for stream,intervals in r['sender_confirmed_business']['stream_intervals'].items():
        counted=defaultdict(int)
        for a,b in intervals:
            for i in range(a,b):counted[i]+=1
        eq(set(counted),coverage[stream],'coverage ranges')
        assert all(v==1 for v in counted.values()),'duplicate output coverage'
    return r

def calc(p):return audit(M.calculate(copy.deepcopy(p)))

def bdplower():
    eq(F(20000000)*F(1,10)/8,250000,'uplink BDP')
    eq(F(100000000)*F(1,10)/8,1250000,'downlink BDP')
    eq(F(30000000*8,20000000)+F(5000000*8,100000000)+F(3,10)+F(1,10),F(64,5),'ideal request lower bound only')

def rtt_errata():
    for latest,expected_srtt,expected_var in [('0.12',F(1,10),F(3,80)),('0.18',F(43,400),F(21,400))]:
        end=F(1,5)+F(latest)
        p=base([sent(0,0),ack('0.1',0),sent(1,'0.2',offset=100),ack(str(end),1,ack_delay='0.02'),ack(str(end+F(1,100)),1,ack_delay=100)],until=str(end+F(1,100)))
        r=calc(p);eq(len(r['rtt_samples']),2,'duplicate ACK no sample')
        eq(F(r['final_state']['smoothed_rtt']),expected_srtt,'corrected SRTT')
        eq(F(r['final_state']['rttvar']),expected_var,'Verified7539 old-SRTT variance')
        eq(F(r['final_state']['cwnd']),14400,'two new ACKs only')
    p=base([sent(0,0),ack('0.1',0,ack_delay='0.09')],until='0.1')
    r=calc(p);eq(F(r['final_state']['smoothed_rtt']),F(1,10),'first sample ignores delay')

def threshold_loss():
    p=base([sent(i,str(F(i,1000)),offset=100*i) for i in range(4)]+[ack('0.103',3)],until='0.12',rtt_seed=seed())
    r=calc(p)
    eq([(x['pn'],F(x['at'])) for x in r['loss_events']],[(0,F(103,1000)),(1,F(227,2000)),(2,F(229,2000))],'packet then time loss')
    eq(F(r['final_state']['cwnd']),6000,'one recovery reduction')
    eq(r['final_state']['bytes_in_flight'],0,'ACK and loss remove once')
    # ACK at the time threshold takes precedence over the timer.
    p['events'].append(ack('0.1135',1));r=calc(p)
    self_lost={x['pn'] for x in r['loss_events']};eq(self_lost,{0},'ACK precedes loss; new RTT postpones PN2')
    eq(F(r['final_state']['next_timer']['at']),F(2057,16000),'updated RTT moves remaining loss deadline')

def pto_boundary():
    s=seed();s['rttvar']='0.0375'
    for with_ack in (False,True):
        events=[sent(0,1)]
        if with_ack:events.append(ack('1.275',0))
        r=calc(base(events,until='1.275',rtt_seed=s))
        eq(len(r['timer_events']),0 if with_ack else 1,'ACK/PTO tie')
        if not with_ack:
            eq(r['timer_events'][0]['kind'],'pto')
            eq(F(r['timer_events'][0]['at']),F(51,40),'PTO time')
            eq(r['loss_events'],[],'PTO does not imply loss')
            eq(F(r['final_state']['cwnd']),12000,'PTO no cwnd cut')
            eq(r['final_state']['bytes_in_flight'],1200,'PTO no release')
            eq(r['final_state']['probe_allowance'],2,'probe opportunities only')
    r=calc(base([sent(0,1)],until='1.55',rtt_seed=s))
    eq([F(x['at']) for x in r['timer_events']],[F(51,40),F(31,20)],'PTO exponential backoff')

def absolute_limits():
    query=dict(type='can_send',sent_bytes=40,frames=[dict(type='stream',stream='A',offset=4,length=2)])
    e0=sent(0,0,length=4);e0['sent_bytes']=40
    e1=sent(1,'0.001',length=2,stream='B');e1['sent_bytes']=40
    old=sent(2,'0.2',length=4);old['sent_bytes']=40
    p=base([e0,e1,ack('0.1',0,1),dict(query,at='0.15'),old,ack('0.3',2),
            dict(type='max_data',at=5,value=8),dict(query,at=5),
            dict(type='max_stream_data',at=6,stream='A',value=6),dict(query,at=6),
            dict(type='max_data',at=6,value=1)],until=6)
    p.update(initial_max_data=6,initial_max_stream_data={'A':4,'B':2})
    r=calc(p);queries=[x['details'] for x in r['events'] if x['event']=='can_send']
    eq(queries[0]['blocked_by'],['MAX_DATA','MAX_STREAM_DATA:A'],'ACK not flow update')
    eq(queries[1]['blocked_by'],['MAX_STREAM_DATA:A'],'both absolute gates needed')
    eq(queries[2]['can_send'],True,'received both limits')
    eq(r['final_state']['max_data'],8,'lower limit ignored')
    eq(r['final_state']['max_data_consumed'],6,'old offset not new flow')
    eq(r['summary']['stream_payload_transmission_bytes'],10,'old offset still transmitted')
    eq(r['sender_confirmed_business']['unique_stream_bytes'],6,'old offset unique once')

def late_ack_and_recovery():
    events=[sent(i,str(F(i,1000)),offset=i*100) for i in range(4)]+[ack('0.103',3),sent(4,'0.104',offset=0),ack('0.105',0),ack('0.204',4)]
    r=calc(base(events,until='0.204',rtt_seed=seed()))
    late=next(x for x in r['events'] if x['event']=='ack' and x['input']['at']=='0.105')
    eq(late['details']['late_acked'],[0],'late ACK recognized')
    eq(late['state']['bytes_in_flight'],3600,'late old ACK no double release')
    eq(F(late['state']['cwnd']),6000,'late old ACK no growth')
    eq(F(r['final_state']['cwnd']),6240,'new post-recovery packet ACK CA')
    eq(r['sender_confirmed_business']['unique_stream_bytes'],200,'newPN oldoffset unique')

def limited_and_ackonly():
    for flag in ('app_limited','flow_limited'):
        r=calc(base([sent(0,0),ack('0.1',0,**{flag:True})],until='0.1'))
        eq(F(r['final_state']['cwnd']),12000,'limited suppresses ACK growth')
    for inflight in (False,True):
        p=base([dict(type='sent',at=0,pn=0,sent_bytes=100,ack_eliciting=False,in_flight=inflight,frames=[]),ack('0.1',0)],until='0.1')
        r=calc(p);eq(r['events'][0]['state']['bytes_in_flight'],100 if inflight else 0,'ACK-only versus padding')
        eq(r['rtt_samples'],[],'no ACK eliciting sample')

def datagram():
    e=dict(type='sent',at=0,pn=0,sent_bytes=1200,frames=[dict(type='datagram',id='d',length=100)])
    p=base([e,ack('0.1',0)],until='0.1');p.update(initial_max_data=0,initial_max_stream_data={})
    r=calc(p);eq(r['final_state']['max_data_consumed'],0,'datagram no flow credit')
    eq(r['sender_confirmed_business']['acked_datagram_bytes'],100,'transport-confirmed datagram')

def invalid():
    cases=[base([ack('0.1',0)]),base([sent(1,0)]),base([sent(0,0),sent(0,'0.1')]),base([sent(0,0),dict(type='ack',at='0.1',ranges=[[0,0],[0,0]])])]
    p=base([sent(0,0)]);p['initial_max_data']=0;cases.append(p)
    p=base([sent(0,0,probe=True)]);cases.append(p)
    p=base([sent(0,0),ack('0.1',0,flow_limited=1)]);cases.append(p)
    p=base([]);p['initial_max_data']=2**62;cases.append(p)
    p=base([]);p['initial_max_stream_data']['A']=2**62;cases.append(p)
    cases.append(base([dict(type='max_data',at=0,value=2**62)]))
    cases.append(base([dict(type='max_stream_data',at=0,stream='A',value=2**62)]))
    cases.append(base([sent(0,0),dict(type='ack',at='0.1',ranges=[[0,2**62]])]))
    for p in cases:
        try:M.calculate(p)
        except ValueError:continue
        raise AssertionError('invalid trace accepted')

def duplicate_ack_does_not_cancel_pto():
    # PN0 already ACKed; duplicate feedback cannot satisfy PN1's timer.
    s=seed();s['rttvar']='0.0375'
    p=base([sent(0,0),ack('0.1',0),sent(1,1,offset=100),ack('1.325',0)],until='1.325')
    r=calc(p)
    eq([F(x['at']) for x in r['timer_events']],[F(53,40)],'duplicate ACK cannot cancel PTO')
    eq(r['final_state']['pto_count'],1,'duplicate no PTO reset')

def probes_obey_flow():
    s=seed();s['rttvar']='0.0375'
    q=sent(1,'0.275',offset=100,probe=True);q['type']='can_send'
    p=base([sent(0,0),q],until='0.275',rtt_seed=s)
    p.update(initial_max_data=100,initial_max_stream_data={'A':100})
    r=calc(p);eq(r['events'][-1]['details']['can_send'],False,'probe cannot evade flow control')
    assert 'MAX_DATA' in r['events'][-1]['details']['blocked_by']
    old=sent(1,'0.275',offset=0,probe=True)
    p['events'][-1]=old;r=calc(p)
    eq(r['final_state']['max_data_consumed'],100,'probe old stream extent')
    eq(r['final_state']['bytes_in_flight'],2400,'probe is real new flight')
    eq(r['final_state']['probe_allowance'],1,'probe opportunity consumed')

def persistent_rejected():
    s=dict(latest_rtt='0.001',smoothed_rtt='0.001',rttvar=0,min_rtt='0.001',first_sample_at=-1)
    p=base([sent(i,t,offset=i*100) for i,t in enumerate((0,'0.1','0.101','0.102','0.103'))]+[ack('0.104',4)],until='0.104',rtt_seed=s)
    try:M.calculate(p)
    except ValueError as e:
        assert 'persistent congestion' in str(e)
        return
    raise AssertionError('persistent congestion scope not rejected')

def sources():
    rows=json.loads((ROOT/'sources.lock.json').read_text());eq(len(rows),4)
    for row in rows:
        b=(ROOT/row['file']).read_bytes();eq(len(b),row['bytes']);eq(hashlib.sha256(b).hexdigest(),row['sha256'])

for name,fn in [('sources',sources),('1_BDP_lower_only',bdplower),('2_RTT_verified_errata',rtt_errata),('3_packet_time_loss',threshold_loss),('4_PTO_ACK_ties',pto_boundary),('5_absolute_flow_limits',absolute_limits),('late_ACK_newPN_oldoffset',late_ack_and_recovery),('limited_and_ACK_only',limited_and_ackonly),('datagram',datagram),('invalid',invalid),('duplicate_ACK_PTO',duplicate_ack_does_not_cancel_pto),('probe_flow_constraints',probes_obey_flow),('persistent_scope_guard',persistent_rejected)]:run(name,fn)
if hasattr(M,'scenarios'):
    for name,p in M.scenarios().items():
        def check(p=p,name=name):
            r=calc(p);evidence[name]=dict(final_state=r['final_state'],summary=r['summary'],loss_events=r['loss_events'],timer_events=r['timer_events'])
        run('scenario_'+name,check)
END=hashlib.sha256((ROOT/'calculate.py').read_bytes()).hexdigest()
if START!=END:failures.append(dict(name='stable_source',error='candidate changed during execution'))
result=dict(status='PASS' if not failures else 'FAIL',candidate_sha256=START,passed=passed,failures=failures,scenario_evidence=evidence)
(ROOT/'check-independent.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='scenario_evidence'},indent=2))
raise SystemExit(bool(failures))
