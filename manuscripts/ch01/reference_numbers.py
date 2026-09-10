"""Recompute chapter-one reference numbers from versioned model and GPU inputs."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics.stage_resource_bounds import workload

def reference_numbers():
    hardware=json.loads((ROOT/'calculations/configs/hardware.json').read_text())
    devices=[]
    for key in ['rtx4090','a100-80gb-sxm','h100-sxm']:
        d=next(d for d in hardware['devices'] if d['id']==key)
        peak=next(p for p in d['peak_rates'] if p['input_precision']=='BF16' and p['accumulator_precision']=='FP32' and p['execution_unit']=='tensor' and p['sparsity']=='dense')
        bandwidth=d['memory']['bandwidth_bytes_per_second']
        devices.append(dict(id=key,capacity_gb=d['memory']['nominal_capacity'],bandwidth_tb_s=bandwidth/1e12,
                            bf16_fp32_dense_tflop_s=peak['tera_ops_per_second'],read_1gb_ms=1e12/bandwidth))
    calls=[]
    for name,tokens,history in [('prefill',2048,0),('decode',1,2048)]:
        _,capacity,baseline,_=workload('qwen3-8b',1,tokens,history,'balanced')
        calls.append(dict(stage=name,tokens=tokens,history=history,matrix_flops=baseline['matrix_flops'],
                          h100_matrix_only_ms=baseline['matrix_flops']/989.4e9,
                          weights_plus_kv_bytes=capacity['comparison_bytes']))
    batch=json.loads((ROOT/'calculations/results/batch-reuse-h100-2k.json').read_text())['summary']
    return dict(devices=devices,model='Qwen3-8B',calls=calls,
                weight_bytes=batch['weight_resident_bytes'],
                decode_weight_read_bytes=batch['shared_decode_weight_read_bytes'],
                kv_bytes_per_token=batch['kv_bytes_per_request_token'],
                source_scope='BF16 model data; matrix operation counts and ideal interface traffic; GPU times are resource bounds')

if __name__=='__main__':
    print(json.dumps(reference_numbers(),ensure_ascii=False,indent=2))
