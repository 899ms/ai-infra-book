import hashlib,json,math
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[3];sources={}
def load(name):
 p=ROOT/name;sources[name]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
moe=load('calculations/results/v4-moe-training-balanced.json');cfg=load('calculations/configs/models/deepseek-v4-flash/config.json');print({k:v for k,v in cfg.items() if 'layer' in k or k in ['hidden_size','n_routed_experts']})
attention=load('calculations/results/v4-attention-training-window128.json');hc=load('calculations/results/v4-hc-training-128.json');dense=load('calculations/results/dense-training-scale-book.json')
assert cfg['num_hidden_layers']==43 and cfg['n_routed_experts']==256 and cfg['hidden_size']==moe['config_geometry']['hidden']
assert moe['coverage']['full_fixed_selection_moe_main_loss_vjp'] and not moe['coverage']['complete_v4_training']
assert not attention['coverage']['complete_attention_layer'] and not hc['coverage']['complete_v4_training']
# Exclude selection bias and all non-MoE parameters: conservative subset.
parameter_subset=43*sum(moe['parameters'][k] for k in ['router_weight','routed_expert_weights','shared_expert_weights'])
state=16*parameter_subset # declared BF16 weights/grads, FP32 master and two Adam moments
work_per_token=F(43*(moe['totals']['forward_matrix_flops']+moe['totals']['backward_matrix_flops']),128)
rows=[]
for device,capacity in [('a100-80gb-sxm',80*10**9),('h100-sxm',80*10**9),('b200-sxm',180*10**9)]:
 peak=F(str(next(r['peak_bf16_fp32_dense_tflops'] for r in dense['dense_scale_rows'] if r['device']==device)))*10**12
 for tokens in [100_000_000_000,1_000_000_000_000]:
  for days in [90,180]:
   for eff in [F(3,10),F(2,5),F(1,2)]:
    work=work_per_token*tokens;seconds=days*86400;compute=math.ceil(work/(peak*eff*seconds));memory=math.ceil(F(state,capacity));cards=max(compute,memory)
    assert compute*peak*eff*seconds>=work and (compute-1)*peak*eff*seconds<work
    assert memory*capacity>=state and (memory-1)*capacity<state
    rows.append(dict(device=device,tokens=tokens,deadline_days=days,assumed_efficiency=str(eff),compute_cards_lower_bound=compute,moe_state_cards_lower_bound=memory,combined_necessary_cards=cards,full_training_cards=None,full_training_seconds=None,quality_qualified_cost=None))
result=dict(scope='MoE-only necessary resource lower bounds; no complete V4 training or deadline result',model='deepseek-v4-flash',source_sha256=sources,moe_parameter_subset=parameter_subset,persistent_subset_bytes=state,state_bytes_per_parameter=16,moe_matrix_flops_per_token_exact=str(work_per_token),source_workload='fixed-selection real-arithmetic128-token balanced MoE repeated through43 main layers; MTP excluded',coverage={'moe_main_loss_vjp':True,'mhc_wrapper':True,'attention_core_only':True,'complete_attention_projections_compressor_backward':False,'complete_optimizer_work':False,'complete_activation_peak':False,'complete_training_calibration':False},rows=rows)
(R/'results.json').write_text(json.dumps(result,indent=2)+'\n')
s=f'''# V4-Flash resource lower bounds and missing training coverage

The archived MoE calculation covers a128-token fixed-selection main-loss forward/backward path with router scores, shared expert and routed experts. Repeating this architectural component across43 main layers gives a **subset**, not total V4 work. The3 hash layers still retain router scores under the recorded contract. Selection-boundary derivatives, quantized-training equivalence, MTP and full training quality are not established.

The mHC result covers86 outer wrappers and requires inner derivatives from the caller. The attention result covers a fixed-index tied-KV core; it explicitly excludes the complete attention layer/compressor backward. Adding these files as if they were disjoint complete layers would double-count some pieces and omit others. Their coverage flags are retained in results.json.

The MoE parameter subset is **{parameter_subset:,} parameters**. A declared16bytes/parameter mixed-precision Adam state implies **{state:,}bytes** before attention, embeddings/head, mHC, activations, optimizer/kernel workspace or communication buffers. This is a necessary aggregate capacity bound, not a feasible placement. It assumes this declared full-parameter optimizer; it is not inferred from the inference checkpoint's quantized size.

MoE matrix work alone is **{float(work_per_token):,.0f}FLOPs/token** under the source128-token fixed-selection contract. Rows evaluate declared100B/1T-token tasks at90/180days and30%/40%/50% matrix efficiency. These efficiencies are hypotheses, not measured V4 MFU. Larger context/compression and whole-model work remain uncounted. The source's one-layer real-arithmetic calculation is not promoted to an actual full-model training benchmark.

| Device | MoE-state-only card floor | Other memory included? |
|---|---:|---|
'''
for device in ['a100-80gb-sxm','h100-sxm','b200-sxm']:
 r=next(r for r in rows if r['device']==device);s+=f"| {device} | {r['moe_state_cards_lower_bound']} | No |\n"
s+='''
All36 compute/state boundary cases check both n and n−1 exactly. Combined necessary counts are saved, but full training cards, full duration and quality-qualified cost remain null. Since MoE persistent state alone exceeds the local96GB GPU by orders of magnitude, the full declared optimizer task cannot be validated there by relabeling an inference/offload run as training.

To complete10-10's V4 portion, the missing full attention/compressor derivative and work contract, activation lifetime/placement, optimizer update, task/quality objective and allocation/data/checkpoint/recovery assumptions must be supplied or implemented. A supported original training trace can calibrate those quantities. More GPUs alone do not fill the missing semantics. This artifact quantifies a resource floor and identifies the missing components; it does not close10-10 or claim these floor-sized fleets suffice.

Run `python run.py` to reproduce. Existing calculation files are read-only.
'''
(R/'README.md').write_text(s);(R/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in R.iterdir() if p.is_file() and p.name!='manifest.json'},indent=2)+'\n');print({'rows':len(rows),'state_subset_bytes':state,'parameter_subset':parameter_subset})
