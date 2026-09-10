#!/usr/bin/env python3
"""Reconstruct chapter 4 teaching boundaries and finite-slot schedules."""
from pathlib import Path
from fractions import Fraction
import json, math
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def pipeline(slots, compute=128, extra_latency=128):
    rows=[]; port_free=0; matrix_free=0; released=[0]*slots
    for i in range(4):
        slot=i%slots
        issue=max(port_free,released[slot]); transfer_end=issue+64
        ready=transfer_end+extra_latency; start=max(ready,matrix_free); end=start+compute
        rows.append(dict(chunk=i,slot=slot,issue_start=issue,transfer_end=transfer_end,
                         data_ready=ready,compute_start=start,compute_end=end,slot_released=end))
        port_free=transfer_end;matrix_free=end;released[slot]=end
    return dict(input_slots=slots,compute_ticks=compute,extra_latency_ticks=extra_latency,
                input_buffer_bytes=slots*16384,finish_tick=matrix_free,chunks=rows)

def derive():
    base=json.loads((ROOT/'calculations/results/attention-input-base.json').read_text())
    schedules=[pipeline(n) for n in range(1,5)]
    # Check overlapping source cases without modifying their original enumeration.
    keys=list(schedules[0]['chunks'][0])
    for n in [1,2,4]:
        source=next(r for r in base['rows'] if r['mode']=='asynchronous-direct-to-buffer' and r['input_slots']==n)
        expected=schedules[n-1]
        assert source['timing']['finish_tick']==expected['finish_tick']
        assert [{k:r[k] for k in keys} for r in source['timing']['chunks']]==expected['chunks']
    intensity=Fraction(165200000000000,1008000000000)
    crossing=intensity*4096/(4096-2*intensity)
    return dict(source='calculations/results/attention-input-base.json',baseline=schedules,
                matrix_double=[pipeline(n,64) for n in range(1,5)],
                longer_latency=[pipeline(n,128,256) for n in range(1,5)],
                boundaries=dict(roofline_crossing_rows=float(crossing),first_compute_bound_row=math.floor(crossing)+1,
                    asymptotic_intensity=2048,host_reuse_count=math.ceil(Fraction(10**12,32*10**9)),
                    message_crossing_bytes=200000,first_transfer_dominated_row=25,
                    minimum_baseline_slots=3,minimum_double_matrix_slots=4),
                provenance='Teaching derivations; tick schedules are not GPU measurements.')

if __name__=='__main__':
    result=derive()
    (HERE/'teaching-data.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Derived finite-slot schedules and resource boundaries.')
