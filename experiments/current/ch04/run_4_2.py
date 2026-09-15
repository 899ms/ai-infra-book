"""Reconcile actual quantized-path timings and allocator peaks for current4-2."""
import hashlib,json,statistics
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2];B=ROOT/'experiments/ch04/04-02'
raw=json.loads((B/'block-scales/results/raw.json').read_text());rows=[]
for q in raw:
 assert q['integer_exact'] and all(v['passed'] and v['relative_l2']<.02 for v in q['checks'].values())
 stages={}
 for stage in ['direct','dequant','activation_quant','weight_dequant']:
  samples=[r for r in q['samples'] if r['stage']==stage];assert sorted(r['trial'] for r in samples)==list(range(9))
  stages[stage]=statistics.median(r['device_ms'] for r in samples)
 rows.append(dict(label=q['label'],error=q['checks'],stage_median_ms=stages))
workspace=[];files=[B/'block-scales/results/raw.json',B/'workspace/analysis.json']
for name in ['decode-direct','decode-dequant','prefill-direct','prefill-dequant']:
 p=B/'workspace/results'/name/'measurement.json';files.append(p);q=json.loads(p.read_text());assert len(q['records'])==4
 peaks=[r['end']['peak_allocated']-q['baseline']['allocated'] for r in q['records']]
 assert len(set(peaks[1:]))==1
 for v in q['records']:assert v['peak_increment_bytes']==v['end']['peak_allocated']-v['start']['allocated']
 workspace.append(dict(condition=name,cold_total_peak_bytes=peaks[0],warm_total_peak_bytes=peaks[1],resident_bytes=q['resident_increment_bytes'],warm_increment_bytes=q['records'][1]['peak_increment_bytes']))
ops=[dict(R=r,expand_at_load=dict(weight_expansions=1,activation_preparations=r,bf16_gemm=r),expand_every_call=dict(weight_expansions=r,activation_preparations=r,bf16_gemm=r),group_direct=dict(activation_preparations=r,int8_partial_gemm=16*r,scaled_group_merges=16*r)) for r in [1,8,64,1024]]
x=dict(exercise='4-2',timing_records=rows,allocator_records=workspace,operation_counts=ops,
 symbolic_times=dict(load_once='Cw + R*L',per_call='R*(Cw + L)',group_direct='R*D'),
 scope='Symbolic execution accounting plus independent medians/peak reconciliation from actual routed-input records. No newly measured resident-BF16 complete path; no sum/subtraction of stage medians presented as measured latency.',
 source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
(R/'4-2-results.json').write_text(json.dumps(x,indent=2)+'\n');print('verified',len(rows),'timing conditions and',len(workspace),'allocator conditions')
