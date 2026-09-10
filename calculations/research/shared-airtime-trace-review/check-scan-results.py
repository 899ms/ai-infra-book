"""Read nine executed scans; independently verify trace and fixed playback slots."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import importlib.util
import json

ROOT=Path(__file__).resolve().parent
CALC=ROOT.parent.parent
SCAN=ROOT.parent/'shared-airtime-scan-inputs'
spec=importlib.util.spec_from_file_location('trace_review',ROOT/'check-trace.py')
review=importlib.util.module_from_spec(spec);spec.loader.exec_module(review)
manifestpath=SCAN/'runs/manifest.json';manifesthash=review.sha(manifestpath)
manifest=json.loads(manifestpath.read_text())
assert manifest['status']=='PASS_EXECUTED_NINE_SCANS'
assert manifest['source_hashes_before']==manifest['source_hashes_after']
for name,digest in manifest['source_hashes_before'].items():assert review.sha(CALC/name)==digest,name
inputs=json.loads((SCAN/'scenarios.json').read_text());input_hash=review.sha(SCAN/'scenarios.json')
precheck=json.loads((ROOT/'scan-input-review.json').read_text())
assert precheck['status']=='passed' and precheck['input_hashes'][str(SCAN/'scenarios.json')]==input_hash
checks=[]
for case,p in inputs.items():
    name=f'runs/{case}-result.json';path=SCAN/name
    assert review.sha(path)==manifest['outputs'][name]
    result=json.loads(path.read_text());assert result['inputs']==p
    trace=review.check(result)
    observer=next(b for b in p['application']['business_observers'] if b['id']=='audio')
    actual=next(b for b in result['businesses'] if b['id']=='audio')
    until=F(str(p['network']['until']))
    arrivals={};on_time=[];missing=F(0);play_starts=[];play_ends=[]
    for block,index in zip(observer['blocks'],range(8)):
        identities=block['message_ids'];assert identities==[f'audio-{index}']
        message=identities[0]
        rx=[r for r in result['transmissions'] if r['message_id']==message and r['received_at'] is not None]
        # This input uses one atomic datagram per media block, no endpoint retry.
        assert len(rx)==1 and rx[0]['frames'][0]['type']=='datagram'
        arrival=F(rx[0]['received_at']);arrivals[message]=arrival
        assert F(result['delivered'][message])==arrival
        slot=F(block['slot_start_seconds']);duration=F(block['duration_seconds'])
        assert slot==F(1,10)+F(index,50) and duration==F(1,50)
        assert until>=slot+duration
        usable=arrival<=slot;on_time.append(usable)
        observed_block=actual['blocks'][index]
        assert observed_block['message_ids']==identities and F(observed_block['arrival'])==arrival
        if usable:
            assert F(observed_block['play_start'])==slot and F(observed_block['play_end'])==slot+duration
            assert F(observed_block['scheduled_play_end'])==slot+duration
            play_starts.append(slot);play_ends.append(slot+duration)
        else:
            assert observed_block.get('play_start') is None
            missing+=duration
    assert len(actual['blocks'])==8 and F(actual['missing_audio_seconds'])==missing
    assert F(actual['stall_seconds'])==0
    assert actual['all_required_delivered'] is True and F(actual['complete_at'])==max(arrivals.values())
    assert actual['complete']==all(on_time)
    assert actual['first_play']==(str(min(play_starts)) if play_starts else None)
    assert actual['playback_end']==(str(max(play_ends)) if play_ends else None)
    ack_count=sum(r['kind']=='ack' for r in result['transmissions'])
    checks.append(dict(case=case,trace=trace,on_time_media_blocks=sum(on_time),offered_media_blocks=8,
        missing_audio_seconds=str(missing),first_play=actual['first_play'],playback_end=actual['playback_end'],
        actual_transport_ACK_count=ack_count,received_media_at={k:str(v) for k,v in arrivals.items()},
        image_complete_at=next(b for b in result['businesses'] if b['id']=='image')['complete_at'],
        result_sha256=manifest['outputs'][name]))
    assert review.sha(path)==manifest['outputs'][name]
# Prove pairing uses exactly the ACK threshold as the within-size change.
for size in (320,640,960):
    paired=[]
    for every in (1,2,4):
        p=deepcopy(inputs[f'media-{size}B-ack{every}']);assert p['network']['ack_policy'].pop('every')==every;paired.append(p)
    assert paired[0]==paired[1]==paired[2]
assert review.sha(manifestpath)==manifesthash and review.sha(SCAN/'scenarios.json')==input_hash
for name,digest in manifest['source_hashes_before'].items():assert review.sha(CALC/name)==digest,name
(ROOT/'scan-check.json').write_text(json.dumps(dict(status='passed',scope='Nine complete saved traces and 72 atomic media delivery/slot comparisons; input-only pre-review completed before result reading; no simulation rerun',generation_manifest_sha256=manifesthash,generation_source_hashes=manifest['source_hashes_before'],inputs_sha256=input_hash,pre_result_input_review_sha256=review.sha(ROOT/'scan-input-review.json'),checks=checks,checker_sha256=review.sha(Path(__file__)),trace_checker_sha256=review.sha(ROOT/'check-trace.py'),comparison_limits='Within each media size only count_or_timer.every changes; across sizes declared byte load/quality differs. All nine are the new 300KB/50KB unpadded, no-controller-pacer teaching workload, not original full book inputs.'),indent=2)+'\n')
print('nine saved scans and72 fixed media slots PASS')
print([(c['case'],c['actual_transport_ACK_count'],c['on_time_media_blocks']) for c in checks])
