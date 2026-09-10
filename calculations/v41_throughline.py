#!/usr/bin/env python3
"""Recompute the fixed V4/V4.1 conversation case; timings are teaching assumptions."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics import kv_comparison

def calculate():
    rows=[]
    for length in (8192,131072):
        result=kv_comparison.calculate(length)
        selected=[r for r in result['rows'] if r['model'] in ('deepseek-v4-flash','deepseek-v4.1-flash') and r['layout']!='BF16 reference']
        rows.append(dict(length=length,models=selected))
    v4,v41=rows[1]['models']
    bandwidth=25e9
    transfers={r['model']:r['global_history_bytes']/bandwidth*1000 for r in (v4,v41)}
    replay=8.0
    r=dict(schema_version=1,cache_cases=rows,
        ced=dict(input_tokens=8192,encoder_layers=20,decoder_layers=20,replay_tokens=128,full_token_layers=40*8192,ced_token_layers=20*8192+20*128,ratio=(20*8192+20*128)/(40*8192)),
        transfer=dict(length=131072,bandwidth_bytes_per_second=bandwidth,global_only_ms=transfers,saved_ms=transfers['deepseek-v4-flash']-transfers['deepseek-v4.1-flash']),
        routing=dict(local_queue_ms=[10,20],remote_replay_ms=replay,remote_transfer_ms=transfers['deepseek-v4.1-flash'],remote_ready_ms=transfers['deepseek-v4.1-flash']+replay),
        assumptions=['B=1, visible snapshot includes current query; 8K=8192,128K=131072.',
          'Use published production cache layouts; per-layer logical operand payload is not measured HBM traffic.',
          'Resident cache excludes weights, compressor/allocator/candidate buffers, workspaces and parallel replication.',
          'CED counts expert-matrix token-layers for cold input; global KV projection and other components excluded.',
          '25 GB/s is a teaching effective bandwidth, global cache only; transfer is serialized for the routing example.',
          '8 ms encoder SWA replay and 10/20 ms queue times are teaching assumptions, not V4.1 measurements.',
          'Routing holds subsequent input processing, mandatory decoder replay and generation cost equal and compares only preparation time.'],sources=[])
    paths=['calculations/src/infra_calc/topics/kv_comparison.py','calculations/configs/models/deepseek-v4-flash/config.json','calculations/configs/models/deepseek-v4.1-flash/config.json','calculations/sources/deepseek-v4.1-flash/FlashMLA-README.md','calculations/sources/deepseek-v4.1-flash/DeepSeek_V41_Tech_Report.pdf','calculations/v41_throughline.py']
    for name in paths:r['sources'].append(dict(path=name,sha256=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()))
    assert rows[0]['models'][1]['global_history_bytes']==7290880
    assert r['ced']['ced_token_layers']==166400 and r['routing']['local_queue_ms'][0]<r['routing']['remote_ready_ms']<r['routing']['local_queue_ms'][1]
    return r
if __name__=='__main__':
    r=calculate();p=ROOT/'calculations/results/v41-throughline.json';p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(dict(ced=r['ced'],transfer=r['transfer'],routing=r['routing']),ensure_ascii=False))
