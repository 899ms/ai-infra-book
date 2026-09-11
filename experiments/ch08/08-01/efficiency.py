#!/usr/bin/env python3
"""Derive decode-bandwidth and prefill-compute efficiency on the RTX PRO 6000 from the batch sweep.

Decode: per-iteration wall time of engine iterations that run only decode (no prompt tokens in this or
the previous iteration, every running request emits one token). Median within each run, then median of
the three formal runs. Bytes per round = shared matrix weights read once + every request's own KV.
Prefill: from the first request's submission (first iteration timestamp minus its TTFT) to the last
iteration that still computed prompt tokens; matrix FLOPs from the official Qwen3-8B operator count.
Peak values come from calculations/configs/hardware.json (rtx-pro6000-blackwell-ws).
"""
import collections,json,statistics,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.models import forward
from infra_calc.schema import Scenario
hw={d['id']:d for d in json.loads((ROOT/'calculations/configs/hardware.json').read_text())['devices']}['rtx-pro6000-blackwell-ws']
BW=hw['memory']['bandwidth_bytes_per_second']
PEAK=next(r['tera_ops_per_second'] for r in hw['peak_rates'] if r['input_precision']=='BF16' and r['accumulator_precision']=='FP32' and r['execution_unit']=='tensor' and r['sparsity']=='dense')*1e12
W=15136811008  # shared decode weight read (embedding rows excluded), as in calculations/results/batch-reuse-*.json
K=147456
stats=collections.defaultdict(list)
for line in (HERE/'results/engine-stats.jsonl').open():
    x=json.loads(line)
    if x.get('iteration'):stats[x['run_id']].append(x)
rows=[]
for kind,history,cached in [('short',2048,0),('prefix',8192,6144)]:
    per_request_flops=forward('qwen3-8b',Scenario(history=cached,tokens=history-cached,output_head='last'))['summary']['matrix_flops']
    for batch in [1,4,16,64]:
        decode=[];prefill=[]
        for run in '012':
            it=sorted(stats[f'{run}-{kind}-b{batch}'],key=lambda x:x['iteration']['iteration_timestamp'])
            gaps=[b['iteration']['iteration_timestamp']-a['iteration']['iteration_timestamp'] for a,b in zip(it,it[1:])
                  if a['iteration']['prompt_token_stats']['computed']==0 and b['iteration']['prompt_token_stats']['computed']==0
                  and b['iteration']['num_generation_tokens']==b['scheduler']['num_running_reqs']==a['scheduler']['num_running_reqs']==batch]
            decode.append(statistics.median(gaps))
            start=it[0]['iteration']['iteration_timestamp']-max(it[0]['iteration']['time_to_first_tokens_iter'])
            last=max(x['iteration']['iteration_timestamp'] for x in it if x['iteration']['prompt_token_stats']['computed']>0)
            assert sum(x['iteration']['prompt_token_stats']['computed'] for x in it)==batch*(history-cached)
            prefill.append(last-start)
        t_d=statistics.median(decode);t_p=statistics.median(prefill)
        read=W+batch*history*K;flops=batch*per_request_flops
        rows.append(dict(kind=kind,context=history,cached_prefix=cached,batch=batch,
            decode_round_ms=round(t_d*1e3,2),decode_round_ms_runs=[round(v*1e3,2) for v in decode],
            nominal_read_bytes=read,peak_read_ms=round(read/BW*1e3,2),
            decode_bandwidth_efficiency=round(read/BW/t_d,3),
            prefill_new_tokens=batch*(history-cached),prefill_matrix_flops=flops,
            prefill_phase_s=round(t_p,4),prefill_phase_s_runs=[round(v,4) for v in prefill],
            prefill_rate_new_tokens_per_s=round(batch*(history-cached)/t_p),
            prefill_compute_efficiency=round(flops/PEAK/t_p,3)))
b1=next(r for r in rows if r['kind']=='short' and r['batch']==1)
# Additive step model used by the chapter's scheduling example: fixed + per new token + per causal pair.
# The pair cost is fixed at 3 ns; the other two terms reproduce batch-1 2K decode and prefill exactly.
pair_ns=3;dec_pairs=2049;pre_pairs=2048*2049//2
t_ns=(b1['prefill_phase_s']*1e9-b1['decode_round_ms']*1e6-pair_ns*(pre_pairs-dec_pairs))/2047
base_ns=b1['decode_round_ms']*1e6-t_ns-pair_ns*dec_pairs
schedule_fit=dict(per_causal_pair_ns=pair_ns,per_new_token_ns=round(t_ns,1),step_base_ns=round(base_ns),
    reproduces=dict(decode_2k_b1_ms=b1['decode_round_ms'],prefill_2k_b1_s=b1['prefill_phase_s']))
out=dict(device=hw['name'],schedule_fit=schedule_fit,peak_bandwidth_bytes_per_second=BW,peak_bf16_fp32_dense_flops=PEAK,
    shared_weight_read_bytes=W,kv_bytes_per_token=K,rows=rows,
    notes=['decode_round_ms: median of pure-decode engine iterations per run, then median of three runs',
           'prefix rows count every request reading its own 8K KV; shared 6K prefix blocks may be served from L2, so their bandwidth efficiency is nominal and can exceed physical DRAM traffic',
           'prefill phase includes decode tokens of requests that already started; batch 1 prefill equals TTFT'])
(HERE/'efficiency.json').write_text(json.dumps(out,ensure_ascii=False,indent=1)+'\n')
for r in rows:print(r['kind'],r['batch'],r['decode_round_ms'],r['peak_read_ms'],r['decode_bandwidth_efficiency'],r['prefill_phase_s'],r['prefill_rate_new_tokens_per_s'],r['prefill_compute_efficiency'])
