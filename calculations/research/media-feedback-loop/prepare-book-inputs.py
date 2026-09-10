"""Prepare explicit four-cell inputs and byte algebra; never run the network."""
from pathlib import Path
import copy,hashlib,json,importlib.util
from collections import Counter
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'media-feedback-inputs/normalized-inputs.json'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def accounting(app):
    per={d:Counter() for d in ('up','down')};flows={d:{} for d in per}
    for m in app['messages']:
        d='up' if m['sender']=='client' else 'down';size=m['bytes'];n=(size+1167)//1168
        assert m['packetization']['payload_limit_bytes']==1168 and m['packetization']['fragment_count']==n and not m['packetization']['coalesce_across_messages']
        if m['transport']=='datagram':assert n==1
        per[d]['declared_application_bytes']+=size;per[d]['declared_packets']+=n
        per[d]['declared_'+m['transport']+'_bytes']+=size
        per[d]['declared_padding_bytes']+=n*1168-size;per[d]['declared_layout_bytes']+=n*32
        per[d]['declared_data_quic_bytes']+=n*1200;per[d]['declared_data_wire_bytes']+=n*1228
        if m['transport']=='stream':flows[d][m['flow_id']]=max(flows[d].get(m['flow_id'],0),m['stream_offset']+size)
    return dict(per_direction={d:dict(v) for d,v in per.items()},stream_highest_declared_ends=flows,total_declared_application_bytes=sum(v['declared_application_bytes'] for v in per.values()),total_declared_packets=sum(v['declared_packets'] for v in per.values()),total_declared_data_wire_bytes=sum(v['declared_data_wire_bytes'] for v in per.values()),scope='All declared messages once. Cancellation, expiry or incomplete dependency can reduce actual sends; not predicted delivery.')
def network(app,ack):
    return dict(links={'up':dict(rate_bps=20000000,propagation='0.05'),'down':dict(rate_bps=100000000,propagation='0.05')},until=60,initial_cwnd=12000,initial_max_data={'up':64000000,'down':16000000},initial_max_stream_data=accounting(app)['stream_highest_declared_ends'],receive_memory_bytes={'up':64000000,'down':16000000},consume_delay=None,sender={'numeric_quantum':'0.000000000001'},controller={'name':'newreno'},pad_in_flight=True,ack_bytes=64,ack_policy=ack,drop_packets=[],routers={})

def prepare():
    for row in json.loads((ROOT/'book-input-sources.lock.json').read_text()):
        path=ROOT/row['file'];assert path.stat().st_size==row['bytes'] and digest(path)==row['sha256']
    raw=json.loads(SOURCE.read_text());base=raw['mixed-fifo'];image=raw['image-30mb-5mb']
    immediate='immediate_each_packet';aggregate=dict(mode='count_or_timer',every=2,max_delay='0.01',delay_exponent=3,retain_packets=256,reorder_immediate=True,header_tag_bytes=24)
    cases={}
    for scheduler in ('fifo','priority'):
        for name,ack in (('immediate',immediate),('aggregate',aggregate)):
            app=copy.deepcopy(base);app['scheduling']['send']=scheduler
            cases[f'mixed-{scheduler}-{name}']=dict(application=app,network=network(app,copy.deepcopy(ack)))
    baseline=dict(application=copy.deepcopy(image),network=network(image,immediate))
    spec=importlib.util.spec_from_file_location('media_input_preflight',ROOT/'calculate.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    for case in [*cases.values(),baseline]:
        instance=module.Network(case) # Constructor validation only. Never advance/run.
        assert not instance.traces and not instance.feedback['up'] and not instance.feedback['down']
    normalized=[]
    for c in cases.values():
        q=copy.deepcopy(c);q['application']['scheduling']['send']='<policy>';q['network']['ack_policy']='<policy>';normalized.append(q)
    assert all(q==normalized[0] for q in normalized)
    counts=accounting(image);assert counts['total_declared_packets']==30800 and counts['total_declared_data_wire_bytes']==37822400
    counts.update(conditional_immediate_ack_count=30800,conditional_immediate_total_wire_bytes=40656000,conditional_aggregate_ack_bounds=[2,30800],conditional_aggregate_total_wire_bounds=[37822584,40656000],bound_conditions='All original image data arrive once; no loss/recovery/control/duplicate injection; ACKs finish within horizon. Generic safe bounds, not a forecast for every2.')
    (ROOT/'book-inputs.json').write_text(json.dumps(cases,indent=2)+'\n')
    (ROOT/'image-baseline-inputs.json').write_text(json.dumps(baseline,indent=2)+'\n')
    result=dict(status='PREPARED_AND_CONSTRUCTOR_VALIDATED_NOT_SIMULATED',source_file=str(SOURCE.relative_to(ROOT.parent.parent)),source_sha256=digest(SOURCE),mixed=accounting(base),image=counts,four_cell_only_changes=['application.scheduling.send','network.ack_policy'],files={f:digest(ROOT/f) for f in ('book-inputs.json','image-baseline-inputs.json')},constructor_sha256=digest(ROOT/'calculate.py'),application_validator_sha256=digest(ROOT/'application_validation.py'))
    (ROOT/'book-input-accounting.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('status','files')}))
if __name__=='__main__':prepare()
