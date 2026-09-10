"""Actual small network run against prewritten shared-window timing oracle."""
import copy
import hashlib
import json
from pathlib import Path
from fractions import Fraction as F
from calculate import calculate

ROOT = Path(__file__).resolve().parent
app = copy.deepcopy(json.loads((ROOT.parent/'media-feedback-inputs/normalized-inputs.json').read_text())['hol-connection'])
app['id'] = 'root-shared-cwnd-three-streams'
for i,message in enumerate(app['messages']):
    message.update(id=f'm{i}',flow_id=f's{i}',bytes=1168,stream_offset=0,application_offset=0,deadline_seconds=None)
    message['packetization'].update(fragment_count=1,final_fragment_bytes=1168)
app['business_observers'] = [dict(id='all-three',kind='image',endpoint='server',completion_dependencies=[dict(id=f'm{i}',event='message_delivered',endpoint='server') for i in range(3)],version_changes=[])]
app['accounting'] = dict(application_bytes_by_direction={'client_to_server':3504},application_bytes=3504,message_count=3,task_count=0,fragment_count=3)
network = dict(links={'up':dict(rate_bps=9824,propagation=1),'down':dict(rate_bps=736,propagation=1)},until=20,initial_cwnd=2400,initial_max_data={'up':3504,'down':0},initial_max_stream_data={'up':{f's{i}':1168 for i in range(3)},'down':{}},receive_memory_bytes={'up':3504,'down':0},pad_in_flight=True,consume_delay=None,sender=dict(initial_rtt=4))
inputs = dict(application=app,network=network)
source_before = {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ('calculate.py','application.py','application_validation.py','sender.py')}
r = calculate(inputs)
data = [p for p in r['transmissions'] if p['kind']=='data']
acks = [p for p in r['transmissions'] if p['kind']=='ack']
checks = {
 'three shared-window starts': [F(p['send_start']) for p in data] == [F(0),F(1),F(4)],
 'three actual data arrivals': [F(p['received_at']) for p in data] == [F(2),F(3),F(6)],
 'actual ACK starts': [F(p['send_start']) for p in acks] == [F(2),F(3),F(6)],
 'actual ACK arrivals': [F(p['received_at']) for p in acks] == [F(4),F(5),F(8)],
 'wire conservation': r['summary']['wire_bytes'] == 3*1228+3*92,
 'unique application conservation': r['summary']['unique_received_application_bytes'] == 3504,
 'no losses': not any(r['losses'].values()),
 'completion at last actual delivery': r['businesses'][0]['complete'] and F(r['businesses'][0]['complete_at']) == 6,
}
source_after = {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in source_before}
report=dict(status='passed' if all(checks.values()) and source_before==source_after else 'failed',inputs=inputs,checks=checks,source_before=source_before,source_after=source_after,result=r)
(ROOT/'network-root-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['status'],checks)
assert report['status']=='passed'
