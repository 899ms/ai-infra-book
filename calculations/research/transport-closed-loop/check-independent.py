"""Independent physical invariants and predeclared hand examples; no sender helpers."""
import copy
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOADED_HASHES={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ('calculate.py','sender.py')}
spec = importlib.util.spec_from_file_location('network_candidate', ROOT/'calculate.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def intervals(rows):
    out=[]
    for a,b in sorted(rows):
        if out and a<=out[-1][1]: out[-1][1]=max(b,out[-1][1])
        else: out.append([a,b])
    return out


def audit(r):
    p=r['inputs']; ts=r['transmissions']; by={(t['direction'],t['pn']):t for t in ts}
    assert len(by)==len(ts)
    ack_arrivals={(t['direction'], F(t['arrival'])) for t in ts if t['kind']=='ack' and not t['dropped']}
    for d in ('up','down'):
        rows=[t for t in ts if t['direction']==d]
        assert [t['pn'] for t in rows]==list(range(len(rows)))
        end=F(0)
        for t in rows:
            start,stop,arr=map(F,(t['send_start'],t['send_end'],t['arrival']))
            assert start>=end
            assert stop-start==F(8*t['wire_bytes'])/F(str(p['links'][d]['rate_bps']))
            assert arr-stop==F(str(p['links'][d]['propagation']))
            assert t['wire_bytes']==t['quic_bytes']+28
            if t['kind']=='data': assert t['quic_bytes']==32+sum(f['length'] for f in t['frames'])
            end=stop
        expected=intervals([(f['offset'],f['offset']+f['length']) for t in rows if not t['dropped'] and F(t['arrival'])<=F(str(p['until'])) for f in t['frames']])
        assert r['received_intervals'][d]==expected
        for e in r['sender_events'][d]:
            if e['type']=='sent':
                t=by[d,e['pn']]; assert F(e['at'])==F(t['send_start'])
            if e['type']=='ack':
                assert ('down' if d=='up' else 'up',F(e['at'])) in ack_arrivals
                # Every acknowledged ID was really received first, not guessed from a drop schedule.
                for a,b in e['ranges']:
                    for pn in range(a,b+1):
                        t=by[d,pn]; assert not t['dropped'] and F(t['arrival'])<=F(e['at'])
        if r['summary']['complete']:
            assert r['final_states'][d]['max_data_consumed']==(p['upload_bytes'] if d=='up' else p.get('response_bytes',0))
    assert r['summary']['wire_bytes']==sum(t['wire_bytes'] for t in ts)
    return {d:sum(t['wire_bytes'] for t in ts if t['direction']==d) for d in ('up','down')}


def execute():
    for row in json.loads((ROOT/'sources.lock.json').read_text()):
        b=(ROOT/row['file']).read_bytes(); assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    oracle=json.loads((ROOT/'root-oracles.json').read_text())['cases']; checks=[]
    for name,o in oracle.items():
        p=m.example(); p.update(response_bytes=0,model_seconds=0,receive_window=10000)
        if name=='cwnd-three-packets': p['upload_bytes']=3504
        elif name=='model-response-before-last-upload-ack': p=m.example()
        elif name=='consumed-credit-arrives-later':
            p.update(upload_bytes=3504,receive_window=2336,explicit_consumption=[dict(at=4,direction='up',upto=2336)])
        else:
            p.update(upload_bytes=1168 if name=='tail-pto-actual-probe' else 2336,drop_packets=[dict(direction='up',pn=0)])
        r=m.calculate(p); wire=audit(r)
        assert wire==dict(up=o['wire_c2s'],down=o['wire_s2c'])
        data=[t for t in r['transmissions'] if t['direction']=='up' and t['kind']=='data']
        expected=o.get('data',o.get('request'))
        if expected is None: expected=[o['lost_original'],o.get('later',o.get('probe'))]+([o['recovery']] if 'recovery' in o else [])
        assert len(data)==len(expected)
        for t,e in zip(data,expected):
            for k,k2 in [('send_start','start'),('send_end','end'),('arrival','receive')]: assert F(t[k])==F(e[k2]),(name,k,t,e)
        if name=='model-response-before-last-upload-ack': assert r['business']==dict(upload='3',model_start='3',model_end='4',response='6')
        if 'loss_observed' in o: assert F(r['losses']['up'][0]['at'])==F(o['loss_observed'])
        if 'first_pto' in o:
            assert F(r['timers']['up'][0]['at'])==12
            assert min(F(x['at']) for x in r['losses']['up'])==16
        checks.append(dict(name=name,status='passed',wire=wire))
    for capacity in (0,1227,1228):
        p=m.example();p.update(upload_bytes=3504,response_bytes=0,model_seconds=0,until=6,
            receive_window=10000,routers=dict(up=dict(rate_bps=4912,propagation=1,queue_bytes=capacity)))
        p['sender']['initial_cwnd']=3600
        r=m.calculate(p);data=[t for t in r['transmissions'] if t['direction']=='up']
        assert len(data)==3 and [F(t['send_start']) for t in data]==[0,1,2]
        assert [F(t['router_admission']) for t in data]==[2,3,4]
        assert data[0]['router_start']=='2' and data[0]['router_end']=='4'
        if capacity<1228:
            assert data[1]['dropped'] and data[1]['drop_reason']=='router_waiting_queue_capacity'
            assert data[2]['router_start']=='4' and data[2]['router_end']=='6'
        else:
            assert not any(t['dropped'] for t in data)
            assert data[1]['router_start']=='4' and data[2]['router_start']=='6'
        assert r['final_states']['up']['bytes_in_flight']==3600
        assert not r['losses']['up'] and r['received_intervals']['up']==[[0,1168]]
        checks.append(dict(name='router-capacity-'+str(capacity),status='passed'))
    p=m.example();p.update(upload_bytes=30000000,response_bytes=5000000,until=60,model_seconds="0.3",
        links=dict(up=dict(rate_bps=20000000,propagation='0.05'),down=dict(rate_bps=100000000,propagation='0.05')),
        sender=dict(initial_cwnd=12000,numeric_quantum='0.000000000001',rtt_seed=dict(latest_rtt='0.1',smoothed_rtt='0.1',rttvar='0.05',min_rtt='0.1')))
    r=m.calculate(p);wire=audit(r)
    nu=(30000000+1167)//1168; nd=(5000000+1167)//1168
    assert wire==dict(up=30000000+60*nu+92*nd,down=5000000+60*nd+92*nu)
    assert len(r['transmissions'])==2*(nu+nd)
    quantum=F(p['sender']['numeric_quantum'])
    errors=[x for v in r['numeric_errors'].values() for x in v]
    assert errors
    for e in errors:
        old,new,err=map(F,(e['original'],e['rounded'],e['local_error']))
        assert new-old==err and abs(err)<=quantum
    assert all(s['bytes_in_flight']==0 and s['next_timer'] is None for s in r['final_states'].values())
    assert F(r['business']['model_end'])-F(r['business']['model_start'])==F('0.3')
    assert r['summary']['complete'] and r['received_intervals']==dict(up=[[0,30000000]],down=[[0,5000000]])
    for d,n in [('up',30000000),('down',5000000)]:
        data=[t for t in r['transmissions'] if t['direction']==d and t['kind']=='data']
        assert sum(f['length'] for t in data for f in t['frames'])==n
        assert len(data)==(n+1167)//1168
    checks.append(dict(name='30MB-5MB-no-loss-conservation',status='passed',wire=wire,business=r['business'],packets=len(r['transmissions']),numeric_quantum=str(quantum),local_rounding_entries=len(errors)))
    return dict(status='passed',scope='five physical hand traces, three router boundaries and one 30MB no-loss trace; not all C68',checks=checks,
       candidate_sha256=LOADED_HASHES['calculate.py'],sender_sha256=LOADED_HASHES['sender.py'])

if __name__=='__main__':
    result=execute();(ROOT/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
