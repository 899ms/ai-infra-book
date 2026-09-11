"""Independent arithmetic checks against stored tensor inventories and exact counts."""
from pathlib import Path
import json,math,hashlib,struct
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
r=json.loads((HERE/'result.json').read_text());checks=[]
def check(ok,label):
    checks.append({'check':label,'passed':bool(ok)})
    if not ok:raise AssertionError(label)
base=json.loads((ROOT/'calculations/results/storage-generation-qwen8-235.json').read_text())['workloads'][0]
# The independent tensor inventory carries names, shape, copies and parameters.
linear=sum(t['parameters'] for t in base['tensors'] if len(t['shape'])==2 and 'model.layers.' in t['name'])
head=next(t['parameters'] for t in base['tensors'] if t['name']=='lm_head.weight')
check(linear*2==r['qwen_work']['linear_flops_per_token'],'linear FLOPs match tensor inventory')
causal_pairs=sum(range(1,4097));attention=causal_pairs*32*128*4*36
check(4096*linear*2+attention+head*2==r['qwen_work']['prefill_4k_causal_matrix_flops'],'enumerated causal pairs and output-head policy')
check(linear*2+8192*32*128*4*36+head*2==r['qwen_work']['decode_8k_matrix_flops'],'8K decode matrix count')
check(struct.unpack('e',struct.pack('e',1e-8))[0]==0,'1e-8 rounds to FP16 zero')
check(r['numerics']['BF16']['min_normal']<1e-8,'1e-8 is in BF16 normal range')
check(56*56*9*64*2==r['conv']['expanded_bytes'],'explicit spatial-window count')
check(r['conv']['expanded_bytes']==r['conv']['input_bytes']*9,'ninefold img2col expansion')
check(r['conv']['explicit_expansion_roundtrip_bytes']==2*r['conv']['expanded_bytes'],'write/read counted separately')
a=r['ascend_attention']
check(a['two_handoffs_external_roundtrip_bytes']==256*1024,'two FP32 attention handoffs total 256 KiB externally')
check(math.isclose(a['required_cv_GBs_for_two_handoffs_in_1_024us'],128,rel_tol=1e-12),'direct CV design target 128 GB/s')
check(math.isclose(a['required_external_GBs_in_1_024us'],256,rel_tol=1e-12),'external exchange design target 256 GB/s')
check(a['exp_vector_groups']/a['cube_cycles_at_8192']==.25,'vector issue requirement, not assumed throughput')
profiles={p['id']:p for p in r['profiles']}
for row in r['decode']:
    p=profiles[row['device']]
    check(math.isclose(row['read_ms']*p['bandwidth_gbs'],row['payload_gb']*1000,rel_tol=1e-12),'byte conservation '+row['workload']+'/'+row['device'])
    check(row['fits_nominal']==(row['headroom_gb']>=0),'capacity sign '+row['workload']+'/'+row['device'])
work={w['id']:w for w in r['workloads']}
w=work['qwen3-235b-a22b-b1-h8191-w4-balanced']
check(w['resident_budget_bytes']+8e9>128e9 and w['resident_budget_bytes']+8e9<256e9,'Apple 128GB/256GB threshold with OS reserve')
w1=work['qwen3-235b-a22b-b8-h8191-w4-balanced'];w2=work['qwen3-235b-a22b-b8-h8191-w4-concentrated']
check(w1['resident_budget_bytes']==w2['resident_budget_bytes'] and w1['accounted_payload_bytes']>3*w2['accounted_payload_bytes'],'MoE route changes traffic, not residence')
for e in r['sources']:check(hashlib.sha256((ROOT/e['path']).read_bytes()).hexdigest()==e['sha256'],'source hash '+e['path'])
report={'passed':all(c['passed'] for c in checks),'checks':len(checks),'results':checks}
(HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS:',len(checks),'independent arithmetic and source checks')
