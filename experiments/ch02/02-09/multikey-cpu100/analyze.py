"""Offline verification of the four-case completed V4 run, without loading a model."""
import hashlib,json,re
from pathlib import Path
R=Path(__file__).resolve().parent
O=R/'runs/multikey-exclusive-100-001'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for n,h in read(O/'execution-package-hashes.json').items():assert sha(O/n)==h,n
cases=read(O/'cases.json');tasks=read(R/'tasks.json');assert sha(R/'tasks.json')==cases['task_sha256']
rows=read(O/'requests.json');assert [r['case_id'] for r in rows]==[r['id'] for r in tasks]
summary=[]
for c,t,r in zip(cases['cases'],tasks,rows):
    assert c['messages']==t['messages'] and c['input_ids']==r['input_ids']
    assert len(r['input_ids'])==c['prompt_tokens']==4148
    assert r['sampling_params']==cases['sampling'] and r['status']=='returned'
    lookup=dict(re.findall(r'^(k\d{4}) = (\d{6})$',c['messages'][1]['content'],re.M))
    assert len(lookup)==512 and {k:lookup[k] for k in c['expected']}==c['expected']
    response=r['response'];pairs=json.loads(response['text'],object_pairs_hook=list)
    assert len(pairs)==3 and len({k for k,v in pairs})==3 and dict(pairs)==c['expected']
    meta=response['meta_info'];assert meta['prompt_tokens']==4148 and meta['completion_tokens']==len(response['output_ids'])==28
    assert meta['finish_reason']['type']=='stop'
    assert 0<r['request_wall_s']<600
    summary.append(dict(case_id=c['id'],strict_success=True,request_wall_s=r['request_wall_s'],prompt_tokens=4148,completion_tokens=28))
assert read(O/'scores.json')['strict_success']==4
s=read(O/'supervisor.json');assert s['exit_code']==0 and s['reason'] is None and not s['leftovers']
samples=[json.loads(l) for l in (O/'watchdog.jsonl').read_text().splitlines()]
config=read(O/'candidate.json');assert config['cpu_offload_gb']==100 and config['context_length']==5120
report=dict(status='four_cases_independently_verified',cases=summary,
    full_model_load_and_pool_log=read(O/'pool-log-evidence.json'),
    telemetry=dict(samples=len(samples),minimum_available_GiB=min(r['available_bytes'] for r in samples)/1024**3,
        maximum_own_GPU_MiB=max(r['own_gpu_mib'] for r in samples),minimum_GPU_free_MiB=min(r['gpu_free_mib'] for r in samples)),
    cleanup=dict(exit_code=s['exit_code'],leftovers=s['leftovers']),
    strict_numerical_clearance=False,
    scope='Four previously selected known retrieval cases, full fixed quantized V4 checkpoint and native encoding. No general quality, BF16-only execution, performance ranking, or broad numerical clearance.',
    source_hashes={str(p.relative_to(R)):sha(p) for p in [R/'tasks.json',O/'cases.json',O/'requests.json',O/'scores.json',O/'supervisor.json',O/'watchdog.jsonl']})
(R/'analysis.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
