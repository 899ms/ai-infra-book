"""Actual network-to-controller feedback ledger, independent of controller helpers."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import calculate as network
ROOT=Path(__file__).resolve().parent

def hashes():return {f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ('calculate.py','sender.py','bbr_adapter.py','cubic_adapter.py')}

def audit(r,controller):
    p=r['inputs'];ts=r['transmissions'];by={(t['direction'],t['pn']):t for t in ts}
    acked={d:{} for d in ('up','down')}
    lost={d:{e['pn']:F(e['at']) for e in r['losses'][d]} for d in ('up','down')}
    for d in acked:
        for e in r['sender_events'][d]:
            if e['type']!='ack':continue
            for a,b in e['ranges']:
                for pn in range(a,b+1):acked[d].setdefault(pn,F(e['at']))
        for t in [t for t in ts if t['direction']==d]:
            assert t['quic_bytes']==(64 if t['kind']=='ack' else 1200)
            assert t['wire_bytes']==t['quic_bytes']+28
        if controller!='bbr':continue
        total=0;seen=set()
        for e in r['controller_events'][d]:
            if e['event']!='ack':continue
            at=F(e['at']); inp=e['callback']['input']
            fresh=e['newly_counted_pns'];assert not seen.intersection(fresh);seen.update(fresh);total+=len(fresh)
            assert inp['total_delivered']==total
            assert all(acked[d][pn]==at and by[d,pn]['kind']!='ack' for pn in fresh)
            prior=sum(t['kind']!='ack' and F(t['send_start'])<at and acked[d].get(t['pn'],F(10**9))>=at and lost[d].get(t['pn'],F(10**9))>=at for t in ts if t['direction']==d)
            after=sum(t['kind']!='ack' and F(t['send_start'])<at and acked[d].get(t['pn'],F(10**9))>at and lost[d].get(t['pn'],F(10**9))>at for t in ts if t['direction']==d)
            assert inp['prior_inflight']==prior,(d,at,'prior',inp['prior_inflight'],prior)
            assert inp['inflight']==after,(d,at,'after',inp['inflight'],after)
            chosen=max(fresh,key=lambda pn:(int(F(by[d,pn]['send_start'])*1000000),pn))
            assert e['selected_pn']==chosen
            if all(lost[d].get(pn,F(10**9))<at for pn in fresh):assert inp['rtt_us']==-1
        assert seen=={pn for pn in acked[d] if by[d,pn]['kind']!='ack'}
    assert r['summary']['complete']
    assert r['received_intervals']==dict(up=[[0,p['upload_bytes']]],down=[[0,p['response_bytes']]])
    assert F(r['business']['model_end'])-F(r['business']['model_start'])==F('0.3')
    return dict(wire_bytes=r['summary']['wire_bytes'],transmissions=len(ts),business=r['business'])

def run():
    initial=hashes();checks=[]
    for c in ('newreno','cubic_hystart','bbr'):
        for variation in ('plain','two-losses','flow-control','short-tail'):
            p=dict(upload_bytes=11680,response_bytes=32,model_seconds='0.3',until=10,
                links={d:dict(rate_bps=1000000,propagation='0.05') for d in ('up','down')},
                controller=dict(name=c),pad_in_flight=True,
                sender=dict(initial_cwnd=12000,rtt_seed=dict(latest_rtt='.1',smoothed_rtt='.1',rttvar='.05',min_rtt='.1')))
            if variation=='two-losses':p['drop_packets']=[dict(direction='up',pn=0),dict(direction='up',pn=3)]
            if variation=='flow-control':p.update(receive_window=2336,consume_delay='0.02')
            if variation=='short-tail':p['upload_bytes']=1200
            r=network.calculate(p);checks.append(dict(controller=c,case=variation,**audit(r,c)))
    assert initial==hashes(),'source changed during audit'
    return dict(status='passed',checks=checks,hashes=initial,scope='twelve small actual network feedback cases; pacer independently owned by root; not 30MB performance or full TCP')
if __name__=='__main__':
    r=run();(ROOT/'network-feedback-independent.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
