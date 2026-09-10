"""Independent evidence-only RFC9002 7.6 predicates and old-span split example."""
from pathlib import Path
import hashlib,json
from persistent_congestion import evaluate
ROOT=Path(__file__).resolve().parent

def packet(pn,t,status='lost',eliciting=True,prior=True):
    return dict(pn=pn,sent_at=t,status=status,ack_eliciting=eliciting,rtt_known_at_send=prior)

def check():
    tests=[]
    def run(name,ps,expected,trigger='ack'):
        r=evaluate(ps,smoothed_rtt='0.1',rttvar='0.02',max_ack_delay='0.025',granularity='0.001',trigger=trigger)
        assert r['threshold_duration']=='123/200'
        assert r['established']==expected,(name,r)
        tests.append(name);return r
    run('strict-equal',[packet(0,0),packet(1,'0.615')],False)
    run('strict-above',[packet(0,0),packet(1,'0.616')],True)
    run('one-lost-endpoint',[packet(0,0),packet(1,1,'sent')],False)
    run('no-prior-rtt',[packet(0,0,prior=False),packet(1,1)],False)
    run('valid-prior-subspan',[packet(0,0,prior=False),packet(1,1),packet(2,2)],True)
    for status in ('acked','lost_then_acked'):
        run('barrier-'+status,[packet(0,0),packet(1,'0.5',status,False),packet(2,1)],False)
    run('noneliciting-not-endpoint',[packet(0,0,eliciting=False),packet(1,1)],False)
    run('unacked-middle',[packet(0,0),packet(1,'0.5','sent'),packet(2,1)],True)
    for t in ('pto','loss_timer'):
        r=run('no-establishment-'+t,[packet(0,0),packet(1,1)],False,t);assert r['required_cwnd_bytes'] is None
    old=[packet(i,t) for i,t in enumerate([0,'0.1','0.2','0.8',1])]
    a=run('old-episode',old,True)
    old[1]['status']='lost_then_acked';b=run('same-loss-episode-split-key',old,True)
    assert a['qualifying_spans'][0]['evidence_key']=='0:4' and b['qualifying_spans'][0]['evidence_key']=='2:4'
    assert {x['pn'] for x in old if x['status']=='lost'}=={0,2,3,4}
    return dict(status='passed',checks=tests,candidate_sha256=hashlib.sha256((ROOT/'persistent_congestion.py').read_bytes()).hexdigest(),scope='evidence only; changed span key does not establish a new controller episode')
if __name__=='__main__':
    r=check();(ROOT/'persistent-independent.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
