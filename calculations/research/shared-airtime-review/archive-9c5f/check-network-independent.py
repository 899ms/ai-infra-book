#!/usr/bin/env python3
"""Execute bounded candidate cases against prewritten oracles and new counterexamples."""
import copy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE.parent/'shared-airtime-loop'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('independent_airtime_network',CANDIDATE/'calculate.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def hashes():
    paths={CANDIDATE/'calculate.py',CANDIDATE/'airtime.py',CANDIDATE/'scenarios.json',CANDIDATE/'network-hand-oracles.json'}
    paths.update(Path(x.__file__).resolve() for n,x in tuple(sys.modules.items()) if n.startswith('infra_calc') and getattr(x,'__file__',None) and str(x.__file__).endswith('.py'))
    return {str(p):sha(p) for p in sorted(paths)}

before=hashes()
inputs=json.loads((CANDIDATE/'scenarios.json').read_text())
expected=json.loads((CANDIDATE/'network-hand-oracles.json').read_text())['cases']
checks=[]
results={}

def norm(v):
    if isinstance(v,(bool,type(None))):return v
    if isinstance(v,list):return [norm(x) for x in v]
    if isinstance(v,(str,int,F)):return F(v)
    return v

def eq(name,key,actual):
    want=expected[name][key]
    assert norm(actual)==norm(want),(name,key,actual,want)
    checks.append({'case':name,'field':key,'actual':actual,'expected':want})

def invariant(label,condition):
    assert condition,label
    checks.append({'case':label,'passed':True})

def attempts(r,d=None,kind=None):
    return [x for x in r.get('wireless_attempts',[]) if (d is None or x['direction']==d) and (kind is None or x['kind']==kind)]

def tx(r,d=None,kind=None):
    return [x for x in r['transmissions'] if (d is None or x['direction']==d) and (kind is None or x['kind']==kind)]

def generic(name,r):
    horizon=F(str(r['inputs']['network']['until']))
    reservations=r.get('wireless_reservations',[])
    invariant(name+'.shared reservation nonoverlap',all(F(a['end'])<=F(b['start']) for a,b in zip(reservations,reservations[1:])))
    by_pn={(t['direction'],t['pn']):t for t in r['transmissions']}
    invariant(name+'.one sender transmission record per PN',len(by_pn)==len(r['transmissions']))
    for a in attempts(r):
        invariant(name+f'.attempt{a["index"]}.no future feedback',a['feedback_known']==(F(a['feedback_at'])<=horizon))
        invariant(name+f'.attempt{a["index"]}.no future receive',a['received']==(a['receive_at'] is not None and F(a['receive_at'])<=horizon))
        t=by_pn[a['direction'],a['pn']]
        invariant(name+f'.attempt{a["index"]}.actual transport send precedes radio',F(t['send_start'])<=F(a['data_start']))
        if a['attempt']>1:
            prior=next(x for x in attempts(r,a['direction']) if x['pn']==a['pn'] and x['attempt']==a['attempt']-1)
            invariant(name+f'.attempt{a["index"]}.retry waits actual feedback',F(a['data_start'])>=F(prior['feedback_at'])+F(str(r['inputs']['network']['wireless_access']['retry_wait'])))
    for t in r['transmissions']:
        if 'wan_start' in t:
            invariant(name+f'.up{t["pn"]}.WAN after AP receive',F(t['wan_start'])>=F(t['wireless_received_at']))
            invariant(name+f'.up{t["pn"]}.WAN serializer bytes',F(t['wan_end'])-F(t['wan_start'])==F(t['wire_bytes']*8)/F(str(r['inputs']['network']['links']['up']['rate_bps'])))
        if 'ap_ready_at' in t:
            invariant(name+f'.down{t["pn"]}.air after WAN',all(F(a['data_start'])>=F(t['ap_ready_at']) for a in attempts(r,'down') if a['pn']==t['pn']))
    for direction,events in r['sender_events'].items():
        for event in events:
            if event['type']=='ack':
                reverse='down' if direction=='up' else 'up'
                invariant(name+'.ACK feedback exists only at endpoint receipt',any(t['kind']=='ack' and t.get('received_at')==event['at'] for t in tx(r,reverse)))

for name,p in inputs.items():
    r=m.calculate(copy.deepcopy(p))
    results[name]=r
    generic(name,r)
    if name.startswith('bidirectional'):
        for d in ['up','down']:
            key=d+'_server_delivery' if d=='up' else 'down_client_delivery'
            eq(name,key,r['delivered']['u' if d=='up' else 'd'])
        eq(name,'first_down_WAN',[tx(r,'down','data')[0][x] for x in ['send_start','send_end']])
        if name.endswith('shared'):
            for d in ['up','down']:
                a=attempts(r,d,'data')[0]
                eq(name,'first_'+d+'_air_exchange',[a['reservation_start'],a['end']])
            eq(name,'first_down_AP_ready',tx(r,'down','data')[0]['ap_ready_at'])
        else:
            eq(name,'first_up_WAN',[tx(r,'up','data')[0][x] for x in ['send_start','send_end']])
    if name.startswith('two-data') or name.startswith('tail-'):
        eq(name,'transport_ACK_count',len(tx(r,kind='ack')))
        eq(name,'total_success_airtime',sum(F(a['end'])-F(a['reservation_start']) for a in attempts(r)))
        if name.startswith('two-data'):
            eq(name,'data_MAC_confirmation_count',len([a for a in attempts(r,kind='data') if a['feedback_known'] and a['outcome']=='success']))
    if name.startswith('busy-client'):
        events=r['ack_events']['down']
        start=next(e for e in events if e['event']=='start')
        deadline=next(e for e in events if e['event']=='trigger' and e['reason']=='deadline')
        eq(name,'first_client_ACK_deadline',deadline['at'])
        eq(name,'first_client_ACK_air_start',start['at'])
        eq(name,'first_client_ACK_ranges',start['ranges'])
        for k in ['largest_received_at','raw_delay','encoded_delay','exceeds_max_delay']:eq(name,k,start[k])
        if name.endswith('refresh'):
            for i,key in enumerate(['first_down_air_exchange','second_down_air_exchange']):
                a=attempts(r,'down','data')[i];eq(name,key,[a['reservation_start'],a['end']])
    if name=='same-PN-MAC-ACK-lost':
        a=attempts(r,'up','data')
        eq(name,'up_MAC_attempt_PNs',[x['pn'] for x in a])
        eq(name,'up_DATA_air_intervals',[[x['data_start'],x['data_end']] for x in a])
        eq(name,'first_AP_receive',a[0]['receive_at'])
        eq(name,'failure_known',a[0]['feedback_at'])
        eq(name,'retry_MAC_success',a[1]['feedback_at'])
        eq(name,'up_original_sender_sent_events',len([e for e in r['sender_events']['up'] if e['type']=='sent']))
        eq(name,'up_WAN_forward_count',len([t for t in tx(r,'up') if 'wan_start'in t]))
        eq(name,'server_unique_delivery',r['delivered']['d0'])
    if name=='MAC-data-loss-exhaustion-then-PTO':
        a=attempts(r,'up','data')
        eq(name,'original_MAC_attempt_PNs',[x['pn'] for x in a[:2]])
        eq(name,'failures_known',[x['feedback_at'] for x in a[:2]])
        eq(name,'end_to_end_PTO',r['timers']['up'][0]['at'])
        eq(name,'probe_new_PN',a[2]['pn'])
        eq(name,'probe_air_DATA_interval',[a[2]['data_start'],a[2]['data_end']])
        eq(name,'server_unique_delivery',r['delivered']['d0'])
    if name.startswith('tail-'):
        eq(name,'server_tail_delivery',r['delivered']['d2'])
        audio=next(b for b in r['businesses'] if b['kind']=='tts')
        eq(name,'tail_slot_usable',audio['complete'])
        if name.endswith('immediate'):
            eq(name,'initial_cwnd_bytes',p['network']['initial_cwnd'])
            eq(name,'tail_play_start',audio['blocks'][0]['play_start'])
            eq(name,'tail_play_end',audio['blocks'][0]['play_end'])
        else:
            eq(name,'first_two_server_arrivals',[r['delivered'][x] for x in ['d0','d1']])
            eq(name,'first_server_ACK_deadline',next(e['at'] for e in r['ack_events']['up'] if e['event']=='trigger'))
            first=tx(r,'down','ack')[0]
            eq(name,'first_ACK_AP_ready',first['ap_ready_at'])
            eq(name,'first_ACK_client_receive',first['received_at'])
            eq(name,'third_DATA_air_start',attempts(r,'up','data')[2]['data_start'])
            eq(name,'missing_audio_seconds',audio['missing_audio_seconds'])

# New counterexample: reverse original MAC-loss case. First DATA arrives client
# at 2s; ACK loss becomes known at 2.5s; same-PN retry must not call QUIC again.
p=copy.deepcopy(inputs['same-PN-MAC-ACK-lost'])
msg=p['application']['messages'][0]
msg.update(sender='server',receiver='client')
p['application']['business_observers'][0]['endpoint']='client'
p['application']['business_observers'][0]['completion_dependencies'][0]['endpoint']='client'
p['application']['accounting']['application_bytes_by_direction']={'client_to_server':0,'server_to_client':1}
p['network']['initial_max_stream_data']={'up':{},'down':{'d0':1}}
p['network']['wireless_access']['failures'][0]['direction']='down'
for policy in ['immediate_each_packet',{'mode':'count_or_timer','every':1,'max_delay':'1','delay_exponent':3,'retain_packets':256,'reorder_immediate':True,'header_tag_bytes':24}]:
    p['network']['ack_policy']=policy
    r=m.calculate(copy.deepcopy(p))
    name='down-MAC-duplicate-'+('immediate' if isinstance(policy,str) else 'count')
    generic(name,r)
    invariant(name+'.single application delivery',r['delivered']=={'d0':'2'})
    invariant(name+'.same PN two MAC attempts',[x['pn'] for x in attempts(r,'down','data')]==[0,0])
    invariant(name+'.no extra transport ACK',len(tx(r,'up','ack'))==1)
    if not isinstance(policy,str):
        invariant(name+'.one QUIC receive notification',len([e for e in r['ack_events']['down'] if e['event']=='receive'])==1)
    results[name]=r

# Source-profile ACK must freeze at actual DATA TXSTART, after access idle,
# not at air reservation. Down DATA received 1s+242us; radio frees +302us;
# client's next access idle adds 34us, so ACK starts +336us and raw delay=94us.
p['network']['wireless_access']['failures']=[]
p['network']['wireless_access']['profile']=json.loads((HERE.parent/'shared-airtime-inputs/profiles.json').read_text())['source_backed_reference_selection']
p['network']['until']=3
r=m.calculate(copy.deepcopy(p));generic('source-profile-ACK-snapshot',r)
start=next(e for e in r['ack_events']['down'] if e['event']=='start')
invariant('source-profile.actual source ACK start',F(start['at'])==1+F(336,1000000))
invariant('source-profile.raw94us includes waiting and access',F(start['raw_delay'])==F(94,1000000))
invariant('source-profile.encoded delay floors94us to88us',start['encoded_delay']==11 and F(start['decoded_delay'])==F(88,1000000))
invariant('source-profile.IP overhead single accounting',attempts(r,'down','data')[0]['service']['data_psdu_bytes']==1264 and attempts(r,'up','ack')[0]['service']['data_psdu_bytes']==128)
results['source-profile-ACK-snapshot']=r

# Horizon deliberately inside failed reservation: outcome is scenario input,
# but sender must not yet know the future failure or enqueue its retry.
p=copy.deepcopy(inputs['same-PN-MAC-ACK-lost']);p['network']['until']='11/10'
r=m.calculate(p);generic('horizon-before-failure',r)
invariant('horizon-before-failure.no feedback events',not r['wireless_events'][1:])
invariant('horizon-before-failure.one attempt',len(attempts(r))==1 and not attempts(r)[0]['feedback_known'])
invariant('horizon-before-failure.no endpoint delivery',not r['delivered'])
results['horizon-before-failure']=r

# The disabled path must be exactly the old public result, not merely totals.
regressions=json.loads((HERE.parent/'media-feedback-loop/result.json').read_text())
for name,r in regressions.items():
    actual=m.calculate(copy.deepcopy(r['inputs']))
    invariant('disabled-existing-full-result.'+name,actual==r)
    disabled=copy.deepcopy(r['inputs']);disabled['network']['wireless_access']={'enabled':False}
    invariant('explicit-disabled-existing-full-result.'+name,m.calculate(disabled)==r)

invariant('source hashes unchanged',hashes()==before)
report={'status':'PASS','source_hashes':before,'checker_sha256':sha(Path(__file__)),
        'scenarios_executed':list(results),'disabled_existing_cases':list(regressions),
        'checks':checks,'result_sha256':{n:hashlib.sha256(json.dumps(r,sort_keys=True).encode()).hexdigest() for n,r in results.items()}}
(HERE/'network-review-result.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
print(f'PASS {len(results)} actual small inputs; {len(regressions)} disabled regressions x 2; {len(checks)} checks')
