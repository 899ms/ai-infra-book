"""Independent sender accounting and application preflight adversarial cases."""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json

ROOT=Path(__file__).resolve().parent
CANDIDATE=ROOT.parent/'media-feedback-loop'

def load(name):
    spec=importlib.util.spec_from_file_location('review_'+name,CANDIDATE/(name+'.py'))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

sender=load('sender')
validation=load('application_validation')
apps=json.loads((ROOT.parent/'media-feedback-inputs/normalized-inputs.json').read_text())
checks=[]

def emit(s,event):
    s['enqueue'](event)
    s['advance'](event['at'])

def packet(pn,at,frames,probe=False):
    return dict(type='sent',pn=pn,at=at,sent_bytes=1200,frames=frames,
                in_flight=True,ack_eliciting=True,probe=probe)

def stream(offset,length):
    return dict(type='stream',stream='A',offset=offset,length=length)

s=sender.create_sender(dict(initial_max_data=300,initial_max_stream_data={'A':300},
                           initial_cwnd=3600,until=20,events=[]))
emit(s,packet(0,0,[stream(0,100)]))
emit(s,packet(1,'.01',[stream(200,100)]))
assert s['state']()['max_data_consumed']==300
emit(s,packet(2,'.02',[stream(0,100)]))
assert s['state']()['max_data_consumed']==300
emit(s,dict(type='ack',at='.1',ranges=[[0,2]],ack_delay=0))
business=s['result']()['sender_confirmed_business']
assert business['unique_stream_bytes']==200
assert business['stream_intervals']=={'A':[[0,100],[200,300]]}
checks.append(dict(case='highest-offset300-actual200-retransmit-credit0',status='passed'))
# DATAGRAM loss does not create a retransmittable payload; the probe has no frames.
s=sender.create_sender(dict(initial_max_data=0,initial_max_stream_data={},initial_rtt='.1',
                           max_ack_delay=0,initial_cwnd=2400,until=1,events=[]))
emit(s,packet(0,0,[dict(type='datagram',id='unit',length=960)]))
s['advance']('.3')
assert s['state']()['bytes_in_flight']==1200
assert sender.retransmittable_frames(s['history'][0])==[]
assert s['state']()['max_data_consumed']==0
emit(s,packet(1,'.301',[],True))
emit(s,dict(type='ack',at='.4',ranges=[[1,1]],ack_delay=0))
assert s['history'][0]['status']=='lost'
assert s['state']()['bytes_in_flight']==0
assert s['result']()['summary']['datagram_payload_transmission_bytes']==960
before=deepcopy(s['state']())
try:s['validate_packet'](packet(2,'.41',[dict(type='datagram',id='unit',length=960)]))
except ValueError:pass
else:raise AssertionError('repeated datagram identity accepted')
assert s['state']()==before
checks.append(dict(case='PTO-no-premature-flight-release-PING-and-no-DATAGRAM-retry',status='passed'))
findings=[]

def expect_rejected(name,app):
    before=deepcopy(app)
    try:
        validation.validate_application(app)
    except ValueError as error:
        findings.append(dict(case=name,status='rejected',reason=str(error)))
    except Exception as error:
        findings.append(dict(case=name,status='wrong-exception',exception=type(error).__name__))
    else:
        findings.append(dict(case=name,status='accepted-invalid',input=app))
    assert app==before

base=deepcopy(apps['screenshot-complete'])
# A server task gains a fake sender field. The dependency event is legitimately
# client-local, but the actual task remains server-local and must be rejected.
base['messages']=[]
base['business_observers']=[]
base['compute_tasks']=[dict(id='client-work',endpoint='client',resource='cpu',duration_seconds='1',
                           ready_seconds='0',source_order=0,priority=0,dependencies=[]),
                      dict(id='server-work',endpoint='server',sender='client',resource='cpu',
                           duration_seconds='1',ready_seconds='0',source_order=1,priority=0,
                           dependencies=[dict(id='client-work',event='task_completed',endpoint='client')])]
expect_rejected('extra-sender-field-bypasses-task-endpoint-causality',base)
base=deepcopy(apps['screenshot-stale'])
base['business_observers'][0]['version_changes'][0]['endpoint']='server'
expect_rejected('remote-version-change-used-by-client-observer',base)
base=deepcopy(apps['mixed-priority'])
obs=next(o for o in base['business_observers'] if o['kind']=='tts')
obs['blocks'][0]['message_ids']=['does-not-exist']
expect_rejected('playback-block-unknown-message',base)
base=deepcopy(apps['screenshot-complete'])
base['messages'][0]['on_delivery_cancel_tags']='screen-v1'
expect_rejected('cancel-tag-string-becomes-character-targets',base)
base=deepcopy(apps['screenshot-complete'])
base['schema_version']=True
expect_rejected('boolean-schema-version',base)
report=dict(status='findings' if any(x['status']!='rejected' for x in findings) else 'passed',
            sender_checks=checks,validation_findings=findings,
            hashes={name:hashlib.sha256((CANDIDATE/name).read_bytes()).hexdigest() for name in
                    ('sender.py','sender-dependencies.lock.json','application_validation.py')},
            checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            scope='Independent sender accounting and adversarial application validation; no network acceptance')
(ROOT/'boundary-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],sender_checks=len(checks),findings=[{k:v for k,v in x.items() if k!='input'} for x in findings])))
