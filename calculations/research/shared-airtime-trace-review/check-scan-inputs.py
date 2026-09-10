"""Pre-result review of the nine inputs; no simulator, builder or output import."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import hashlib
import json

ROOT=Path(__file__).resolve().parent
CALC=ROOT.parent.parent
SCAN=ROOT.parent/'shared-airtime-scan-inputs'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
lock=json.loads((SCAN/'inputs.lock.json').read_text())
for name,digest in lock['files'].items():assert sha(CALC/name)==digest,name
for name,digest in lock['outputs'].items():assert sha(SCAN/name)==digest,name
before={str(p):sha(p) for p in (SCAN/'scenarios.json',SCAN/'hand-oracles.json',SCAN/'inputs.lock.json')}
inputs=json.loads((SCAN/'scenarios.json').read_text());oracles=json.loads((SCAN/'hand-oracles.json').read_text())['cases']
assert len(inputs)==len(oracles)==9
checks=[]
for size,service in ((320,178),(640,226),(960,274)):
    base=deepcopy(inputs[f'media-{size}B-ack1']);del base['network']['ack_policy']['every']
    for every,static_count in ((1,308),(2,155),(4,78)):
        name=f'media-{size}B-ack{every}';p=inputs[name];q=deepcopy(p)
        assert q['network']['ack_policy'].pop('every')==every and q==base
        app,net=p['application'],p['network'];messages={m['id']:m for m in app['messages']}
        assert net['pad_in_flight'] is False and net['sender']=={'initial_rtt':'1/10'}
        assert net.get('controller') is None and F(str(net['until']))==3
        assert net['links']=={'up':{'rate_bps':20000000,'propagation':'1/20'},'down':{'rate_bps':100000000,'propagation':'1/20'}}
        assert net['ack_policy']==dict(mode='count_or_timer',every=every,max_delay='1/100',delay_exponent=3,retain_packets=256,reorder_immediate=True,header_tag_bytes=24)
        assert len(messages)==10 and len(app['compute_tasks'])==1
        assert messages['image-upload']['bytes']==300000 and messages['image-response']['bytes']==50000
        task=app['compute_tasks'][0];assert task['id']=='image-compute' and task['endpoint']=='server' and F(task['duration_seconds'])==F('0.3')
        assert task['dependencies']==[{'id':'image-upload','event':'message_delivered','endpoint':'server'}]
        assert messages['image-response']['dependencies']==[{'id':'image-compute','event':'task_completed','endpoint':'server'}]
        audio=[messages[f'audio-{i}'] for i in range(8)]
        for i,m in enumerate(audio):
            assert m['bytes']==size and m['transport']=='datagram' and m['sender']=='server' and m['receiver']=='client'
            assert m['dependencies']==[] and F(m['ready_seconds'])==F(i,50) and m['priority']==100
            assert m['stream_offset'] is None
        observer=next(b for b in app['business_observers'] if b['id']=='audio')
        assert observer['playback']=='slots' and observer['endpoint']=='client'
        for i,b in enumerate(observer['blocks']):
            assert b['message_ids']==[f'audio-{i}'] and F(b['duration_seconds'])==F(1,50) and F(b['slot_start_seconds'])==F(1,10)+F(i,50)
        profile=net['wireless_access']['profile']
        assert profile==json.loads((ROOT.parent/'shared-airtime-inputs/profiles.json').read_text())['source_backed_reference_selection']
        assert net['wireless_access']['max_attempts']==1 and net['wireless_access']['failures']==[]
        phy=profile['phy'];assert phy['data_rate_bps']==54000000 and phy['mac_ack_rate_bps']==6000000
        # Derive symbols independently with exact rational ceiling, not builder helper.
        def air(payload):
            bits=16+8*(payload+32+28+8+24+4)+6
            data_symbols=(F(bits,216)).__ceil__()
            mac_symbols=(F(16+8*14+6,24)).__ceil__()
            return 34+20+4*data_symbols+16+20+4*mac_symbols
        image=298*air(1168)+air(992)+air(944)
        assert image==90544 and air(size)==service
        o=oracles[name]
        assert o['application_bytes_up']==300000 and o['application_bytes_down']==50000+8*size and o['application_total_bytes']==350000+8*size
        assert o['audio_bytes']==8*size and F(o['audio_duration_seconds'])==F(8,50)
        assert o['declared_audio_payload_bps']==F(size*8)/F(1,50)==400*size
        assert o['original_data_packets_up']==257 and o['original_data_packets_down']==51
        assert o['image_success_service_us']==image and o['individual_audio_success_service_us']==service
        assert o['audio_success_service_us']==8*service and o['original_DATA_success_service_floor_us']==image+8*service
        assert o['static_threshold_only_transport_ACK_count']==static_count==((257+every-1)//every+(51+every-1)//every)
        assert o['static_threshold_only_ACK_service_us']==134*static_count
        assert o['static_threshold_only_total_service_us']==image+8*service+134*static_count
        assert o['actual_transport_ACK_count'] is None and o['actual_media_playback_success'] is None
        checks.append(dict(case=name,only_ack_axis_changed=True,unit_and_service_arithmetic='passed',local_dependency_and_slot_checks='passed'))
assert before=={path:sha(Path(path)) for path in before}
(ROOT/'scan-input-review.json').write_text(json.dumps(dict(status='passed',scope='Nine sealed inputs and prewritten arithmetic only; no scan results read or simulator executed',checks=checks,source_input_lock_sha256=sha(SCAN/'inputs.lock.json'),input_hashes=before,checker_sha256=sha(Path(__file__)),limitations=['New 300KB/50KB unpadded and unpaced teaching workload, not original 30MB/5MB padded controller experiment','320/640/960 bytes are declared load variants, not equal-quality codec evidence','Static threshold-only ACK count is not the actual event count or its lower bound','All-data service floor is conditional on every offered original message actually sent successfully; horizon3s does not guarantee completion'],findings=[]),indent=2)+'\n')
print('nine input/policy/arithmetic/dependency checks passed; no scan output read')
