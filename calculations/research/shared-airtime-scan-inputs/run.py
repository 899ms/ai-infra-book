#!/usr/bin/env python3
"""Run all nine sealed scans; preserve full results separately from summaries."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
CANDIDATE=HERE.parent/'shared-airtime-loop'
EXPECTED='37c442824b5b127407658a75b21638882ee5a75ff08156cfc716b141d1b75f6b'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(CANDIDATE/'calculate.py')==EXPECTED,'candidate revision changed'
spec=importlib.util.spec_from_file_location('airtime_scan_candidate',CANDIDATE/'calculate.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def hashes():
    paths={Path(__file__),CANDIDATE/'calculate.py',CANDIDATE/'airtime.py',ROOT/'configs/sources.lock.json'}
    paths.update(HERE/n for n in ['build.py','scenarios.json','hand-oracles.json','inputs.lock.json'])
    source_root=HERE.parent/'shared-airtime-inputs'
    paths.add(source_root/'sources.lock.json')
    paths.update(source_root/row['file'] for row in json.loads((source_root/'sources.lock.json').read_text()))
    paths.update(Path(x.__file__).resolve() for n,x in tuple(sys.modules.items()) if n.startswith('infra_calc') and getattr(x,'__file__',None) and str(x.__file__).endswith('.py'))
    # Public official originals are listed by the public source lock; capture
    # all existing locked local files, independent of metadata returned later.
    lock=json.loads((ROOT/'configs/sources.lock.json').read_text())
    for row in lock['sources']:
        for key in ['local_path','path','file']:
            if key in row and isinstance(row[key],str) and (ROOT/row[key]).is_file():paths.add(ROOT/row[key])
    input_lock=json.loads((HERE/'inputs.lock.json').read_text())
    for name,expected in input_lock['files'].items():
        p=ROOT/name
        assert digest(p)==expected,'input source changed: '+name
        paths.add(p)
    for name,expected in input_lock['outputs'].items():assert digest(HERE/name)==expected
    return {str(p.relative_to(ROOT)):digest(p) for p in sorted(paths)}

def main():
    out=HERE/'runs';out.mkdir(exist_ok=True)
    before=hashes();began=time.monotonic()
    inputs=json.loads((HERE/'scenarios.json').read_text())
    hand=json.loads((HERE/'hand-oracles.json').read_text())['cases']
    summaries={};outputs={}
    for name,p in inputs.items():
        started=time.monotonic();r=m.calculate(p)
        assert hashes()==before,'source changed during '+name
        target=out/(name+'-result.json')
        target.write_text(json.dumps(r,indent=2)+'\n')
        attempts=r['wireless_attempts']
        data_service=sum(F(a['end'])-F(a['reservation_start']) for a in attempts if a['kind']=='data')
        summaries[name]=dict(elapsed_seconds=time.monotonic()-started,
            transmissions=len(r['transmissions']),actual_transport_ACK_packets=sum(t['kind']=='ack' for t in r['transmissions']),
            actual_started_DATA_attempts=sum(a['kind']=='data' for a in attempts),
            offered_application_bytes=p['application']['accounting']['application_bytes'],
            delivered_application_bytes=r['summary']['delivered_application_bytes'],
            unique_received_application_bytes=r['summary']['unique_received_application_bytes'],
            message_status=r['message_status'],businesses=r['businesses'],
            started_DATA_reserved_seconds=str(data_service),
            all_started_attempts_reserved_seconds=r['wireless_summary']['reserved_service_seconds'],
            observed_reserved_seconds=r['wireless_summary']['observed_reserved_seconds'],
            hand_all_offered_original_DATA_success_floor_seconds=str(F(hand[name]['original_DATA_success_service_floor_us'],1000000)),
            note='Offered DATA floor is conditional on all offered originals being sent successfully. Actual attempts/received/delivered/playable are separate; cancellation or expiry may reduce sent service, retries may increase it.')
        outputs[str(target.relative_to(HERE))]=digest(target)
        print(json.dumps({'case':name,'ACKs':summaries[name]['actual_transport_ACK_packets'],'airtime':r['wireless_summary']['observed_reserved_seconds'],'businesses':r['businesses']}),flush=True)
    summary=out/'summary.json';summary.write_text(json.dumps(summaries,indent=2)+'\n');outputs[str(summary.relative_to(HERE))]=digest(summary)
    after=hashes();assert before==after
    (out/'manifest.json').write_text(json.dumps(dict(status='PASS_EXECUTED_NINE_SCANS',elapsed_seconds=time.monotonic()-began,source_hashes_before=before,source_hashes_after=after,outputs=outputs),indent=2)+'\n')
    print('PASS actual nine scans, all source/input hashes stable',flush=True)

if __name__=='__main__':main()
