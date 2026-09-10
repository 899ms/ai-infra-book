#!/usr/bin/env python3
"""Build nine bounded scan inputs; validate schema, never run an event engine."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'src'))
from infra_calc.transport.media_application_validation import validate_application
spec=importlib.util.spec_from_file_location('scan_schema_helpers',HERE.parent/'shared-airtime-loop/scenario_helpers.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
profiles_path=HERE.parent/'shared-airtime-inputs/profiles.json'
profile=json.loads(profiles_path.read_text())['source_backed_reference_selection']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def service_us(payload):
    # STREAM/DATAGRAM layout budget32 + IPUDP28 + LLC8/MAC24/FCS4.
    psdu=payload+96
    symbols=(22+8*psdu+215)//216
    return 20+4*symbols+34+16+44

def fragments(size):
    n,tail=divmod(size,1168)
    return [1168]*n+([tail] if tail else [])

cases={};oracles={}
for size in [320,640,960]:
    messages=[h.message('image-upload',size=300000,flow='image-up')]
    messages.append(h.message('image-response',sender='server',size=50000,flow='image-down',dependencies=[h.dependency('image-compute','server','task_completed')]))
    for i in range(8):
        messages.append(h.message(f'audio-{i}',sender='server',size=size,transport='datagram',flow='audio',ready=F(i,50)))
    task=dict(source_order=0,priority=0,id='image-compute',endpoint='server',resource='server',ready_seconds='0',duration_seconds='3/10',dependencies=[h.dependency('image-upload','server')],cancel_tag=None)
    observers=[h.complete_observer('image',['image-response'],endpoint='client'),
               dict(id='audio',kind='tts',endpoint='client',completion_dependencies=[h.dependency(f'audio-{i}','client') for i in range(8)],version_changes=[],playback='slots',blocks=[dict(message_ids=[f'audio-{i}'],duration_seconds='1/50',slot_start_seconds=str(F(1,10)+F(i,50))) for i in range(8)])]
    app=h.application(f'media-size-{size}',messages,observers,[task])
    # Same priority policy for all nine: audio wins within the server queue;
    # global radio arbitration remains the fixed shared FIFO profile.
    app['scheduling']['send']='priority'
    for message in app['messages']:
        if message['id'].startswith('audio-'):message['priority']=100
    validate_application(app)
    for every in [1,2,4]:
        name=f'media-{size}B-ack{every}'
        network=h.teaching_network(app,until=3,cwnd=12000)
        network.update(links={'up':dict(rate_bps=20000000,propagation='1/20'),'down':dict(rate_bps=100000000,propagation='1/20')},
            pad_in_flight=False,sender={'initial_rtt':'1/10'},
            ack_policy=dict(mode='count_or_timer',every=every,max_delay='1/100',delay_exponent=3,retain_packets=256,reorder_immediate=True,header_tag_bytes=24),
            wireless_access=dict(enabled=True,profile=profile,max_attempts=1,retry_wait=0,failures=[]))
        cases[name]=dict(application=app,network=network)
        upload=fragments(300000);response=fragments(50000)
        image_service=sum(service_us(x) for x in upload+response)
        audio_service=8*service_us(size)
        # A static threshold-only accounting comparator, NOT a lower bound on
        # actual ACK count: timer, queue coalescing, retention and recovery differ.
        static_ack=(len(upload)+every-1)//every+(len(response)+8+every-1)//every
        oracles[name]=dict(application_bytes_up=300000,application_bytes_down=50000+8*size,
            application_total_bytes=350000+8*size,audio_bytes=8*size,audio_duration_seconds='4/25',
            declared_audio_payload_bps=400*size,original_data_packets_up=len(upload),original_data_packets_down=len(response)+8,
            image_success_service_us=image_service,audio_success_service_us=audio_service,
            original_DATA_success_service_floor_us=image_service+audio_service,
            individual_audio_success_service_us=service_us(size),
            static_threshold_only_transport_ACK_count=static_ack,
            static_threshold_only_ACK_service_us=134*static_ack,
            static_threshold_only_total_service_us=image_service+audio_service+134*static_ack,
            actual_transport_ACK_count=None,actual_media_playback_success=None,
            scope='Original DATA service floor assumes every offered message sent once successfully; no ACK/minimum count assertion, retries or horizon-completion claim.')
assert len(cases)==9
assert len(fragments(300000))==257 and fragments(300000)[-1]==992
assert len(fragments(50000))==43 and fragments(50000)[-1]==944
assert [service_us(x) for x in [320,640,960]]==[178,226,274]
assert all(v['image_success_service_us']==90544 for v in oracles.values())
(HERE/'scenarios.json').write_text(json.dumps(cases,indent=2)+'\n')
(HERE/'hand-oracles.json').write_text(json.dumps({'status':'PREWRITTEN_NO_NETWORK_EXECUTION','cases':oracles},indent=2)+'\n')
paths=[HERE.parent/'media-feedback-inputs/README.md',HERE.parent/'media-feedback-public-integration/NEXT-SCOPE.md',profiles_path,HERE.parent/'shared-airtime-inputs/sources.lock.json',HERE.parent/'shared-airtime-loop/scenario_helpers.py',Path(sys.modules[validate_application.__module__].__file__),Path(__file__)]
(HERE/'inputs.lock.json').write_text(json.dumps({'status':'NINE_APPLICATION_SCHEMAS_VALIDATED_NO_NETWORK_EXECUTION','files':{str(p.relative_to(ROOT)):sha(p) for p in paths},'outputs':{n:sha(HERE/n) for n in ['scenarios.json','hand-oracles.json']}},indent=2)+'\n')
print('9 input schemas validated; packet/byte/service arithmetic PASS; no network execution')
