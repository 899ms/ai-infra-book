"""Actual degeneration to established upload/model/response packet timings."""
import copy
import hashlib
import json
from pathlib import Path
from calculate import calculate
from infra_calc.topics.transport_closed_loop import calculate as established

ROOT = Path(__file__).resolve().parent
base = json.loads((ROOT/'example.json').read_text())
base['application']['messages'][0]['ready_seconds']='0'
for message in base['application']['messages']:
    message['flow_id']='business'
base['network']['initial_max_stream_data']={'up':{'business':3443},'down':{'business':64}}
checks=[]
fields=('direction','pn','kind','frames','send_start','send_end','arrival','quic_bytes','wire_bytes','dropped','probe','received_at','recovery_of','probe_of')
for name,extra in [('immediate',{}),('first-data-loss',{'drop_packets':[{'direction':'up','pn':0}]}),('first-ACK-loss',{'drop_packets':[{'direction':'down','pn':0}]}),('aggregate',{'ack_policy':{'mode':'count_or_timer','every':2,'max_delay':'0.01','delay_exponent':3,'retain_packets':256,'reorder_immediate':True,'header_tag_bytes':24}})]:
    current=copy.deepcopy(base);current['network'].update(extra)
    old=dict(upload_bytes=3443,response_bytes=64,model_seconds='0.05',links=current['network']['links'],until=10,pad_in_flight=True,receive_window=3443)
    old.update(extra)
    before={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ('calculate.py','application.py','network_validation.py','application_validation.py')}
    actual=calculate(current);expected=established(old)
    assert len(actual['transmissions'])==len(expected['transmissions']), name
    for a,b in zip(actual['transmissions'],expected['transmissions']):
        for field in fields:assert a.get(field)==b.get(field),(name,field,a.get(field),b.get(field))
    assert actual['summary']['wire_bytes']==expected['summary']['wire_bytes'],name
    assert actual['delivered']['screen-action']==expected['business']['response'],name
    assert actual['losses']==expected['losses'],name
    assert actual['timers']==expected['timers'],name
    after={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in before}
    assert before==after,'candidate changed during run'
    checks.append(dict(case=name,inputs=current,established_inputs=old,source_hashes=before,packets=len(actual['transmissions']),wire_bytes=actual['summary']['wire_bytes'],response_at=actual['delivered']['screen-action'],compared_fields=fields))
report=dict(status='passed',checks=checks,scope='Four actual one-message upload/compute/response degenerations; physical packet/feedback equality, not whole media acceptance')
(ROOT/'single-image-root-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(checks),'actual packet timing and recovery regressions')
