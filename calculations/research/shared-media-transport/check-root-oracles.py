"""Execute prewritten integer hand calculations through the candidate interface."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('shared_media_candidate', ROOT / 'calculate.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def packet(name, stream, offset=0, size=1, ready=0, **extra):
    return dict(id=name, stream=stream, direction='c2s', offset=offset,
                payload_bytes=size, ready=ready, **extra)


def base(packets):
    inputs = module.example()
    inputs.update(packets=packets, businesses=[], tasks=[])
    return inputs


def deliveries(result):
    return {row['id']: row['delivered'] for row in result['packets']}


def main():
    source_hash = hashlib.sha256((ROOT / 'calculate.py').read_bytes()).hexdigest()
    checks = []
    result = module.calculate(module.example())
    assert result['delivery_only_replay']['connection']['A0'] == '7'
    assert result['delivery_only_replay']['per_stream']['A0'] == '3'
    assert result['summary']['data_wire_bytes'] == 4
    checks.append('fixed-wire HOL: A delivery 7 vs 3; four transmitted bytes')

    packets = [packet('B'+str(i), 'B', i) for i in range(4)]
    packets.append(packet('A', 'A', ready=1, priority=10))
    inputs = base(packets)
    fifo = module.calculate(inputs)
    priority = module.calculate(dict(inputs, scheduler='priority'))
    assert deliveries(fifo)['A'] == '6' and deliveries(fifo)['B3'] == '5'
    assert deliveries(priority)['A'] == '3' and deliveries(priority)['B3'] == '6'
    assert fifo['summary']['data_wire_bytes'] == priority['summary']['data_wire_bytes'] == 5
    checks.append('same packets: audio priority 3 vs 6, image 6 vs 5')

    inputs = base([packet('B', 'B', size=4), packet('A', 'A', ready=1, priority=10)])
    result = module.calculate(dict(inputs, scheduler='priority'))
    assert deliveries(result)['A'] == '6'
    checks.append('4-byte running image is nonpreemptive')

    for streams in [('B','B','B'), ('A','B','C')]:
        offsets = {}
        packets = []
        for i, stream in enumerate(streams):
            packets.append(packet(str(i), stream, offsets.get(stream, 0)))
            offsets[stream] = offsets.get(stream, 0) + 1
        result = module.calculate(dict(base(packets), shared_credit_bytes=2))
        starts = [t['start'] for t in result['transmissions'] if t['kind']=='data']
        assert starts == ['0','1','4'], starts
    checks.append('one or three streams share two credits: starts 0,1,4')

    packets = [packet('a0','A',ready=1), packet('a1','A',1,ready=4),
               packet('a2','A',2,ready=5)]
    inputs = base(packets)
    blocks = [dict(packets=['a'+str(i)], duration=2, slot_start=3+2*i) for i in range(3)]
    inputs['businesses'] = [dict(id='speech',kind='tts',playback='reliable',blocks=blocks)]
    reliable = module.calculate(inputs)['businesses'][0]
    assert reliable['first_play']=='3' and reliable['stall_seconds']=='1'
    assert reliable['playback_end']=='10'
    slots = copy.deepcopy(inputs)
    slots['businesses'][0]['playback']='slots'
    result = module.calculate(slots)['businesses'][0]
    assert [x['played'] for x in result['blocks']] == [True,False,True]
    assert result['missing_seconds']=='2' and result['playback_end']=='9'
    checks.append('playback: reliable 1s stall vs fixed-slot 2s missing sound')

    inputs = module.example()
    inputs['tasks'] = [dict(id='model',dependencies=['B0','B1'],duration=2)]
    inputs['packets'].append(dict(packet('response','R',size=2,dependencies=['model']),direction='s2c'))
    result = module.calculate(inputs)
    assert deliveries(result)['response']=='12'
    checks.append('image completes7, compute7-9, response9-11 arrives12')

    inputs = base([packet('upload','I'), packet('cancel','C',ready=2,cancel_targets=['job']),
                   dict(packet('response','R',dependencies=['model'],cancel_tag='job'),direction='s2c')])
    inputs['tasks']=[dict(id='model',dependencies=['upload'],duration=3,cancel_tag='job')]
    result=module.calculate(inputs)
    assert result['cancellations'][0]['at']=='4'
    assert result['work'][0]['start']=='2' and result['work'][0]['end']=='5'
    assert not any(t['kind']=='data' and t['packet']=='response' for t in result['transmissions'])
    checks.append('cancel propagates to4; running compute2-5 retained; unsent response suppressed')
    if hasattr(module, 'mixed_example'):
        mixed = module.mixed_example()
        by_direction = {direction: sum(x['payload_bytes'] for x in mixed['packets']
                                      if x['direction']==direction)
                        for direction in ('c2s','s2c')}
        # One screenshot, one 32-byte cancellation, and one 64-byte action;
        # differs explicitly from the three-screenshot workload proposal.
        assert by_direction == {'c2s': 30_008_595, 's2c': 5_007_808}, by_direction
        pair = module.scenarios()
        a = module.calculate(pair['mixed-fifo'])['inputs']
        b = module.calculate(pair['mixed-priority'])['inputs']
        assert [k for k in a if a[k] != b[k]] == ['scheduler']
        assert a['compute_scheduler'] == b['compute_scheduler'] == 'fifo'
        checks.append('mixed offered bytes hand-counted; network-only scheduler comparison')
    assert source_hash == hashlib.sha256((ROOT / 'calculate.py').read_bytes()).hexdigest()
    report=dict(status='passed',source_sha256=source_hash,checks=checks)
    (ROOT / 'root-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
