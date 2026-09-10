"""Source-derived rational oracles and sequence/sample boundary checks."""
from pathlib import Path
from fractions import Fraction as F
import copy,hashlib,importlib.util,json
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('hystart_candidate',ROOT/'calculate.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def flow(rounds=6,low='0.010',high='0.014'):
    events=[]
    for r in range(rounds):
        if r: events.append(dict(type='sent',at=r*10,snd_nxt=(r+1)*8000))
        for j in range(1,9):
            n=r*8+j;events.append(dict(type='ack',at=r*10+j,ack_seq=n*1000,newly_acked_bytes=1000,rtt=low if r==0 else high,rtt_sample_id=str(n)))
    return dict(smss=1000,initial_cwnd=10000,initial_snd_nxt=8000,events=events)

def run():
    tests=[]
    def calc(name,p):
        r=m.calculate(p);tests.append(name);return r
    r=calc('two-round-entry',flow(2));a=[e for e in r['events'] if e['event']['type']=='ack']
    assert a[7]['after']['cwnd']=='18000' and a[14]['after']['phase']=='slow_start'
    assert r['final']['cwnd']=='26000' and r['final']['phase']=='css' and r['final']['completed_css_rounds']==1
    assert a[-1]['details']['increment']=='1000'
    r=calc('five-css-round-limit',flow());assert r['final']['cwnd']==r['final']['ssthresh']=='34000'
    assert r['final']['phase']=='congestion_avoidance_handoff'
    p=flow(3)
    for e in p['events']:
        if e['type']=='ack' and e['ack_seq']>16000:e['rtt']='0.013'
    r=calc('css-eight-sample-jitter',p);a=[e for e in r['events'] if e['event']['type']=='ack']
    assert a[-2]['after']['phase']=='css' and a[-1]['after']['phase']=='slow_start' and a[-1]['after']['cwnd']=='28000'
    assert a[-1]['after']['css_baseline_min_rtt'] is None
    r=calc('css-baseline-equality',flow(3));assert r['final']['phase']=='css'
    for low,high,threshold in [('0.01','0.014','0.004'),('0.08','0.09','0.01'),('0.2','0.216','0.016')]:
        r=calc('threshold-'+low,flow(2,low,high));assert F(r['events'][-1]['details']['rtt_threshold'])==F(threshold) and r['final']['phase']=='css'
    for paced,expected in [(False,18000),(True,30000)]:
        r=calc('growth-'+str(paced),dict(initial_snd_nxt=20000,paced=paced,events=[dict(type='ack',at=1,ack_seq=20000,newly_acked_bytes=20000)]));assert F(r['final']['cwnd'])==expected
    p=flow(2)
    for e in p['events']:
        e.pop('rtt',None);e.pop('rtt_sample_id',None)
    r=calc('missing-samples',p);assert r['final']['phase']=='slow_start' and r['final']['cwnd']=='26000'
    assert all(e['after']['rtt_sample_count']==0 for e in r['events'])
    p=flow(2)
    p['events'] += [dict(type='ack',at=30+i,ack_seq=16000,newly_acked_bytes=0) for i in range(3)]
    p['events'] += [dict(type='sent',at=40,snd_nxt=24000),dict(type='ack',at=41,ack_seq=17000,newly_acked_bytes=1000)]
    r=calc('no-empty-rounds',p)
    assert all(e['after']['completed_css_rounds']==1 for e in r['events'][-5:])
    assert r['events'][-1]['after']['window_end']==24000
    p=dict(initial_snd_nxt=8000,events=[dict(type='sent',at=0,snd_nxt=20000),dict(type='ack',at=1,ack_seq=9000,newly_acked_bytes=9000)])
    r=calc('cross-marker-once',p);assert r['final']['round']==2 and r['final']['window_end']==20000 and r['final']['cwnd']=='18000'
    for signal in ('loss','ecn'):
        p=flow(2);p['events'].append(dict(type='congestion',at=30,signal=signal));r=calc(signal,p)
        assert r['final']['cwnd']==r['final']['ssthresh']=='26000' and not r['final']['handoff']['congestion_reduction_applied']
    for paced,end in [(False,28000),(True,31000)]:
        p=flow(2);p['paced']=paced
        p['events'] += [dict(type='sent',at=30,snd_nxt=36000),dict(type='ack',at=31,ack_seq=36000,newly_acked_bytes=20000)]
        r=calc('css-growth-'+str(paced),p);assert F(r['final']['cwnd'])==end
    p=flow(2)
    for i in range(4):
        end=24000+8000*i
        p['events'] += [dict(type='sent',at=30+2*i,snd_nxt=end),dict(type='ack',at=31+2*i,ack_seq=end,newly_acked_bytes=8000)]
    r=calc('css-round-limit-without-new-rtt',p)
    assert r['final']['phase']=='congestion_avoidance_handoff' and r['final']['cwnd']=='34000'
    st=m.Startup(flow(1)); first=flow(1)['events'][0];st.step(first)
    before=copy.deepcopy(st.state()); now=st.now
    bad=dict(first,at=2,ack_seq=2000)
    try:st.step(bad)
    except ValueError:pass
    else:raise AssertionError('duplicate sample accepted')
    assert st.state()==before and st.now==now
    tests.append('failed-incremental-step-atomic')
    invalid=[]
    p=flow(1);p['events'][1]['rtt_sample_id']=p['events'][0]['rtt_sample_id'];invalid.append(p)
    p=flow(1);p['events'][0]['ack_seq']=9000;invalid.append(p)
    p=flow(1);p['events'][0]['newly_acked_bytes']=True;invalid.append(p)
    p=flow(1);p['events'][0]['rtt']=0;invalid.append(p)
    p=flow(1);p['paced']=1;invalid.append(p)
    p=flow(1);p['constants']={'css_growth_divisor':1};invalid.append(p)
    p=flow(1);p['events'][0]['unknown']=1;invalid.append(p)
    p=flow();p['events'].append(dict(type='ack',at=100,ack_seq=48000,newly_acked_bytes=0));invalid.append(p)
    p=flow(1);p['events'].insert(0,dict(type='sent',at=0,snd_nxt=7999));invalid.append(p)
    for p in invalid:
        try:m.calculate(p)
        except ValueError:pass
        else:raise AssertionError('invalid accepted')
    return dict(status='passed',groups=tests,invalid_inputs=len(invalid),candidate_sha256=hashlib.sha256((ROOT/'calculate.py').read_bytes()).hexdigest(),scope='independent RFC9406 rational/round/sample cases; upstream RTT eligibility and ACK range validation remain caller duties')
if __name__=='__main__':
    r=run();(ROOT/'independent-check.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
