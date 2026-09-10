"""Verify every figure data record against its actual public result input."""
import json
from pathlib import Path
import sys
from fractions import Fraction

CALC=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(CALC/'src'))
from infra_calc import shared_media_plot


def main():
    manifest_check=shared_media_plot.verify()
    folder=CALC/'figures/shared-media'
    data=json.loads((folder/'data.json').read_text())
    result=lambda name: json.loads((CALC/'results'/('shared-media-'+name+'.json')).read_text())
    hol=result('hol-connection')
    assert data['hol']['fixed_transmissions']==hol['transmissions']
    assert data['hol']['delivery']==hol['delivery_only_replay']
    assert hol['transmissions']==result('hol-per_stream')['transmissions']
    traces=len(hol['transmissions'])
    businesses=0
    for policy in ('fifo','priority'):
        actual=result('schedule-'+policy)
        assert data['scheduling'][policy]['transmissions']==actual['transmissions']
        assert data['scheduling'][policy]['businesses']==actual['businesses']
        traces+=len(actual['transmissions'])
        businesses+=len(actual['businesses'])
    for policy in ('reliable','slots'):
        assert data['playback'][policy]==result('playback-'+policy)['businesses']
        businesses+=len(data['playback'][policy])
    mixed=result('mixed-priority')
    assert data['mixed']['visible_until_seconds_exact']=='1'
    assert data['mixed']['transmissions']==[t for t in mixed['transmissions'] if Fraction(t['start'])<1]
    assert data['mixed']['work']==[w for w in mixed['work'] if Fraction(w['start'])<1]
    assert data['mixed']['businesses']==mixed['businesses']
    traces+=len(data['mixed']['transmissions'])
    businesses+=len(mixed['businesses'])
    evidence=dict(status='passed',figure_manifest=manifest_check,
                  exact_trace_records_checked=traces,business_records_checked=businesses,
                  work_records_checked=len(data['mixed']['work']),
                  scope='Four selected teaching panels; not full figure12-4 requirements')
    (Path(__file__).parent/'figure-check.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(evidence))


if __name__=='__main__':
    main()
