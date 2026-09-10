import argparse,hashlib,json,math,statistics
from pathlib import Path
import torch
p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();r=Path(__file__).absolute().parent;torch.set_num_threads(4)
raw=json.loads((r/'results/raw.json').read_text());assert raw['source_sha256']==hashlib.sha256((r/'run.py').read_bytes()).hexdigest()
guard=json.loads((r/'runs/measurement/supervisor.json').read_text());assert guard['exit_code']==0 and guard['reason'] is None and not guard['leftovers']
assert len(raw['cases'])==6 and len(raw['timing'])==216
rows=[];comparisons=[]
for n in [4096,65536]:
 inp=torch.load(r/f'results/input-n{n}.pt',weights_only=True,map_location='cpu');assert inp['x'].shape==(1024,n) and inp['w'].shape==(n,)
 assert inp['x'].dtype==inp['w'].dtype==torch.bfloat16
 baseline={}
 for m in [1,32,1024]:
  case=next(x for x in raw['cases'] if x['m']==m and x['n']==n);assert case['parts']==n//1024 and case['scratch_bytes']==4*m*(n//1024+1)
  xd=inp['x'][:m].double();ref=xd*torch.rsqrt(xd.square().mean(1,keepdim=True)+1e-6)*inp['w'].double();del xd
  outputs={}
  for method in ['row','split']:
   output=torch.load(r/f'results/output-n{n}-m{m}-{method}.pt',weights_only=True,map_location='cpu');assert output.shape==(m,n) and output.dtype==torch.bfloat16
   outputs[method]=output;err=output.double()-ref;rel=(err.norm()/ref.norm()).item();scaled=(err.abs()/(.01+.01*ref.abs())).max().item();check=case['checks'][method]
   assert math.isclose(rel,check['relative_l2'],rel_tol=1e-8,abs_tol=1e-12),(n,m,method,rel,check)
   assert math.isclose(scaled,check['scaled_max'],rel_tol=1e-8,abs_tol=1e-12)
   assert check['pass_quality']==(rel<.005 and scaled<=1)
   assert check['repeats_bitwise_equal']==[True]*5
   if m==1:baseline[method]=output.clone()
   comparisons.append(dict(n=n,m=m,method=method,compared_prefix_rows=baseline[method].shape[0],prefix_changed_elements=int(torch.count_nonzero(output[:baseline[method].shape[0]]!=baseline[method]))))
   baseline[method]=output.clone()
   for mode in ['eager','graph']:
    samples=[x['us_per_call'] for x in raw['timing'] if x['m']==m and x['n']==n and x['method']==method and x['mode']==mode];assert len(samples)==9 and min(samples)>0
    rows.append(dict(n=n,m=m,method=method,mode=mode,median_us=statistics.median(samples),min_us=min(samples),max_us=max(samples),relative_l2=check['relative_l2'],scaled_max=check['scaled_max'],scratch_bytes=0 if method=='row' else case['scratch_bytes']))
  comparisons.append(dict(n=n,m=m,method='between_methods',changed_elements=int(torch.count_nonzero(outputs['row']!=outputs['split']))))
  for trial in range(9):
   group=[x for x in raw['timing'] if x['m']==m and x['n']==n and x['trial']==trial];assert len(group)==4 and sorted(x['position'] for x in group)==[0,1,2,3] and all(x['repeats']==20 for x in group)
  trace=json.loads((r/f'results/trace-n{n}-m{m}.json').read_text());kernels=[x for x in trace['traceEvents'] if x.get('cat')=='kernel']
  assert len(kernels)==4,[x['name'] for x in kernels]
  assert [x['name'] for x in kernels]==['row_norm','partial','final_reduce','apply_norm']
  case['trace_kernels']=[dict(name=x['name'],duration_us=x['dur'],grid=x['args'].get('grid'),block=x['args'].get('block')) for x in kernels]
  assert [x['args']['grid'] for x in kernels]==[[m,1,1],[m,n//1024,1],[m,1,1],[m,n//1024,1]]
follow=json.loads((r/'streamed/raw.json').read_text())
assert follow['source_sha256']==hashlib.sha256((r/'streamed.py').read_bytes()).hexdigest()
assert follow['input_sha256']==hashlib.sha256((r/'results/input-n65536.pt').read_bytes()).hexdigest()
guard=json.loads((r/'runs/streamed/supervisor.json').read_text());assert guard['exit_code']==0 and guard['reason'] is None and not guard['leftovers']
assert len(follow['cases'])==3 and len(follow['timing'])==54
inp=torch.load(r/'results/input-n65536.pt',weights_only=True,map_location='cpu');previous=None
for case in follow['cases']:
 m=case['m'];output=torch.load(r/f'streamed/output-m{m}.pt',weights_only=True,map_location='cpu');assert output.shape==(m,65536) and output.dtype==torch.bfloat16
 xd=inp['x'][:m].double();ref=xd*torch.rsqrt(xd.square().mean(1,keepdim=True)+1e-6)*inp['w'].double();err=output.double()-ref
 rel=(err.norm()/ref.norm()).item();scaled=(err.abs()/(.01+.01*ref.abs())).max().item()
 assert math.isclose(rel,case['relative_l2'],rel_tol=1e-8,abs_tol=1e-12) and math.isclose(scaled,case['scaled_max'],rel_tol=1e-8,abs_tol=1e-12)
 assert case['pass_quality']==(rel<.005 and scaled<=1) and case['repeats_bitwise_equal']==[True]*5
 if previous is not None:assert torch.equal(output[:previous.shape[0]],previous)
 previous=output.clone()
 for method in ['row','split']:
  other=torch.load(r/f'results/output-n65536-m{m}-{method}.pt',weights_only=True,map_location='cpu')
  comparisons.append(dict(n=65536,m=m,method='streamed_vs_'+method,changed_elements=int(torch.count_nonzero(output!=other))))
 for trial in range(9):
  group=[x for x in follow['timing'] if x['m']==m and x['trial']==trial];assert sorted(x['mode'] for x in group)==['eager','graph'] and all(x['repeats']==20 for x in group)
 for mode in ['eager','graph']:
  samples=[x['us_per_call'] for x in follow['timing'] if x['m']==m and x['mode']==mode];assert len(samples)==9 and min(samples)>0
  rows.append(dict(n=65536,m=m,method='streamed',mode=mode,median_us=statistics.median(samples),min_us=min(samples),max_us=max(samples),relative_l2=case['relative_l2'],scaled_max=case['scaled_max'],scratch_bytes=0))
 trace=json.loads((r/f'streamed/trace-m{m}.json').read_text());kernels=[x for x in trace['traceEvents'] if x.get('cat')=='kernel'];assert len(kernels)==1 and kernels[0]['name']=='streamed_row' and kernels[0]['args']['grid']==[m,1,1]
 case['trace_kernel']=dict(name=kernels[0]['name'],duration_us=kernels[0]['dur'],grid=kernels[0]['args']['grid'],block=kernels[0]['args']['block'])
summary=dict(rows=rows,comparisons=comparisons,cases=raw['cases'],followup=follow['cases'],cpu_fp64_reconstruction=True)
if a.check:assert json.loads((r/'analysis.json').read_text())==summary;print('PASS: 15 full outputs, CPU FP64, 270 timings, nine actual traces')
else:(r/'analysis.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(dict(rows=rows,comparisons=comparisons),indent=2))
