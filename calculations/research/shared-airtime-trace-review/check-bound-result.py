"""Verify generation identity, then independently inspect one full saved result."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse
import copy
import importlib.util
import json
import time

ROOT=Path(__file__).resolve().parent
BOOK=ROOT.parent/'shared-airtime-book-inputs'
spec=importlib.util.spec_from_file_location('trace_review',ROOT/'check-trace.py')
review=importlib.util.module_from_spec(spec);spec.loader.exec_module(review)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--case',default='image-baseline');args=parser.parse_args()
    started=time.monotonic();case=args.case
    manifestpath=BOOK/f'runs/{case}-manifest.json';manifesthash=review.sha(manifestpath)
    manifest=json.loads(manifestpath.read_text())
    assert manifest['status']=='COMPLETE_STABLE_IDENTITY_NOT_INDEPENDENT_ACCEPTANCE'
    assert manifest['source_hashes_before']==manifest['source_hashes_after']
    assert manifest['full_workload'] is True
    for filename,digest in manifest['source_hashes_before'].items():assert review.sha(BOOK/filename)==digest,filename
    inputpath=BOOK/f'runs/{case}-inputs.json';inputhash=review.sha(inputpath)
    assert inputhash==manifest['inputs_sha256']
    resultpath=manifestpath.parent/manifest['result_file'];resulthash=review.sha(resultpath)
    assert resulthash==manifest['result_sha256'] and resultpath.stat().st_size==manifest['result_bytes']
    if case=='image-baseline':assert resulthash=='44955a7478d5da294273e49ac530b884953beb5a9111e828d020b6898680c5c1'
    sources=review.identities()
    result=json.loads(resultpath.read_text())
    inputs=json.loads(inputpath.read_text())
    assert result['inputs']==inputs
    checked=review.check(result)
    analysis={}
    if case=='image-baseline':
        attempts=result['wireless_attempts'];tx=result['transmissions']
        kinds=Counter(a['kind'] for a in attempts)
        assert kinds=={'data':30800,'ack':30800}
        assert all(a['outcome']=='success' and a['attempt']==1 for a in attempts)
        assert all(F(a['end'])-F(a['reservation_start'])==F(302 if a['kind']=='data' else 134,1000000) for a in attempts)
        total=F(302*30800+134*30800,1000000)
        psdu_bytes=30800*(1264+128)+61600*14
        rf=F(30800*(208+40)+61600*44,1000000)
        access=F(61600*34,1000000);sifs=F(61600*16,1000000)
        assert psdu_bytes==43736000 and rf==F('10.3488') and access==F('2.0944') and sifs==F('0.9856')
        assert rf+access+sifs==total
        assert sum(a['service']['data_psdu_bytes']+a['service']['mac_ack_psdu_bytes'] for a in attempts)==psdu_bytes
        assert sum(F(a['service']['radio_transmit_seconds']) for a in attempts)==rf
        assert sum(F(a['service']['access_idle_seconds']) for a in attempts)==access
        assert total==F('13.4288')==F(result['wireless_summary']['observed_reserved_seconds'])
        assert result['summary']['unique_received_application_bytes']==35000000
        assert result['summary']['wire_bytes']==40656000
        complete=F(result['businesses'][0]['complete_at'])
        upload=max(F(t['received_at']) for t in tx if t['direction']=='up' and t['kind']=='data')
        download_first=min(F(t['send_start']) for t in tx if t['direction']=='down' and t['kind']=='data')
        model=result['work'];assert len(model)==1
        assert download_first-upload==F('0.3')
        old=ROOT.parent/'media-feedback-loop/runs/book-image-baseline-summary.json'
        old_manifest=ROOT.parent/'media-feedback-loop/runs/book-image-baseline-manifest.json'
        om=json.loads(old_manifest.read_text());assert review.sha(old)==om['summary_sha256']
        baseline=json.loads(old.read_text());old_complete=F(baseline['businesses'][0]['complete_at'])
        oldinputs=json.loads((ROOT.parent/'media-feedback-loop/image-baseline-inputs.json').read_text())
        clean=copy.deepcopy(inputs);del clean['network']['wireless_access'];assert clean==oldinputs
        busy_before_complete=sum(max(F(0),min(complete,F(a['end']))-F(a['reservation_start'])) for a in attempts if F(a['reservation_start'])<complete)
        radio_last=max(F(a['end']) for a in attempts)
        counts=Counter((t['direction'],t['kind']) for t in tx)
        analysis=dict(data_attempts=30800,transport_ack_attempts=30800,data_exchange_seconds='151/500000',ack_exchange_seconds='67/500000',
            aggregate_radio_service_seconds=str(total),aggregate_radio_service_decimal=float(total),
            total_mac_psdu_bytes=psdu_bytes,radio_transmit_seconds=str(rf),access_idle_seconds=str(access),sifs_seconds=str(sifs),
            complete_seconds=str(complete),complete_decimal=float(complete),
            upload_complete_seconds=str(upload),model_seconds='3/10',download_first_source_send=str(download_first),
            no_wireless_same_input_complete_seconds=str(old_complete),additional_complete_seconds=str(complete-old_complete),additional_complete_decimal=float(complete-old_complete),
            radio_service_before_complete=str(busy_before_complete),radio_service_after_complete=str(total-busy_before_complete),
            radio_nonreserved_time_before_complete=str(complete-busy_before_complete),last_radio_exchange_end=str(radio_last),
            direction_kind_counts={d+'_'+k:v for (d,k),v in counts.items()},
            no_wireless_summary_sha256=review.sha(old),
            interpretation='13.4288s is accumulated one-radio service across data and transport ACKs, not additive request latency. WAN serialization/propagation and radio overlap; late ACK service can continue after the image is complete. The delta uses identical message boundaries and all original network/application inputs with only wireless_access added; no attribution to individual controller or queue mechanism is inferred.')
    assert review.sha(resultpath)==resulthash and review.sha(inputpath)==inputhash and review.sha(manifestpath)==manifesthash
    assert review.identities()==sources
    for filename,digest in manifest['source_hashes_before'].items():assert review.sha(BOOK/filename)==digest,filename
    out=dict(status='passed',case=case,full_saved_trace_checked=True,checked=checked,analysis=analysis,
        generation_manifest_file=str(manifestpath),generation_manifest_sha256=manifesthash,
        generation_source_hashes=manifest['source_hashes_before'],input_sha256=inputhash,result_sha256=resulthash,
        review_source_hashes=sources,review_seconds=time.monotonic()-started,checker_sha256=review.sha(ROOT/'check-trace.py'),binding_checker_sha256=review.sha(Path(__file__)),
        scope='Full saved trace independent service/WAN/PN/coverage check and sealed generation identity; not a network rerun, full scheduler proof, measured WLAN or whole C69 acceptance')
    (ROOT/f'{case}-check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(case,'full saved trace passed',out['review_seconds'],flush=True)
    print(json.dumps(analysis,indent=2),flush=True)
if __name__=='__main__':main()
