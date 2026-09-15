"""Concrete PP-only layout arithmetic, with explicit unresolved workspace bounds."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[3]
rows=[];sources={}
def load(path):
 p=ROOT/path;sources[path]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
for model,file,partitions in [('qwen3-8b','training-qwen3-8b-t32768.json',[4,8]),('qwen3-235b-a22b','training-qwen3-235b-balanced.json',[47,94])]:
 c=load(f'calculations/configs/models/{model}/config.json');x=load('calculations/results/'+file);h=c['hidden_size'];d=c['head_dim'];layers=c['num_hidden_layers'];v=c['vocab_size'];q=c['num_attention_heads']*d;kv=c['num_key_value_heads']*d
 attention=h*q+2*h*kv+q*h
 norm=2*h+2*d
 mlp=3*h*c['intermediate_size'] if model=='qwen3-8b' else 3*h*c['moe_intermediate_size']*c['num_experts']+h*c['num_experts']
 per_layer=attention+norm+mlp;embedding=v*h;assert c['tie_word_embeddings'] is False
 params=layers*per_layer+2*embedding+h;assert params==x['summary']['parameters']
 layer_f=sum(r['training_matrix_flops']//3 for r in x['training_matrix_rows'] if r['name']!='lm_head')//layers
 head_f=next(r['training_matrix_flops']//3 for r in x['training_matrix_rows'] if r['name']=='lm_head')
 assert 3*(layer_f*layers+head_f)==x['summary']['training_matrix_flops']
 tokens=x['summary']['input_tokens'];boundary=2*tokens*h
 for pp in partitions:
  for microbatches in [8,32]:
   stages=[];offset=0
   for rank in range(pp):
    count=layers//pp+(rank<layers%pp);weights=per_layer*count+(embedding if rank==0 else 0)+(embedding+h if rank==pp-1 else 0)
    # GPipe, one stored BF16 layer-input checkpoint per layer/microbatch.
    # Boundary recv buffers are additional conservative allocations, not aliases.
    checkpoints=microbatches*count*boundary;recv=2*boundary
    persistent=weights*18;forward=layer_f*count+(head_f if rank==pp-1 else 0)
    # Checkpointed transformer layers rerun forward once during backward.
    training=3*forward+layer_f*count
    stages.append(dict(rank=rank,layers=list(range(offset,offset+count)),parameters=weights,persistent_bytes=persistent,checkpoint_bytes=checkpoints,extra_boundary_buffers_bytes=recv,accounted_bytes=persistent+checkpoints+recv,forward_matrix_flops=forward,training_with_layer_recompute_matrix_flops=training,unaccounted_workspace_headroom_80GB=80_000_000_000-persistent-checkpoints-recv,unaccounted_workspace_headroom_96GB=96_000_000_000-persistent-checkpoints-recv));offset+=count
   assert offset==layers and sum(s['parameters'] for s in stages)==params
   assert sum(s['persistent_bytes'] for s in stages)==x['summary']['unsharded_parameter_state_bytes']
   assert sum(s['forward_matrix_flops'] for s in stages)==x['summary']['forward_matrix_flops']
   links=[dict(source=i,target=i+1,forward_bytes_per_microbatch=boundary,backward_bytes_per_microbatch=boundary,total_bytes_per_step=2*microbatches*boundary) for i in range(pp-1)]
   total=sum(l['total_bytes_per_step'] for l in links);assert total==2*microbatches*(pp-1)*boundary
   rows.append(dict(model=model,pp=pp,tp=1,dp=1,ep=1,schedule='GPipe full fill/drain; layer-input checkpointing',microbatches=microbatches,microbatch_size=1,sequence_tokens=tokens,effective_tokens_per_full_step=microbatches*tokens,stages=stages,links=links,total_link_payload_bytes_per_step=total,peak_accounted_bytes=max(s['accounted_bytes'] for s in stages),minimum_workspace_headroom_80GB=min(s['unaccounted_workspace_headroom_80GB'] for s in stages),minimum_workspace_headroom_96GB=min(s['unaccounted_workspace_headroom_96GB'] for s in stages),full_memory_feasibility='unproven: temporary activations, kernel and optimizer workspace not bounded'))
(R/'results.json').write_text(json.dumps(dict(scope='Concrete model PP candidate accounting; analytical, not a runtime',source_sha256=sources,candidates=rows),indent=2)+'\n')
s='''# Concrete PP candidate memory and transfers

Eight candidates place every parameter of the pinned Qwen3-8B and Qwen3-235B configurations. This is a conditional analytical comparison, not a claim that these high-PP layouts have run or are efficient. All ranks have TP=DP=EP=1. Qwen8 uses PP4/8; Qwen235 uses PP47/94. Keeping whole transformer layers and all experts on their owning stage avoids an invented perfectly even parameter split or unmodeled expert all-to-all. Contiguous layer counts differ by at most one. Embedding belongs to the first rank; separate LM head and final norm to the last.

The selected schedule is full fill/drain GPipe,8 or32 microbatches,one sequence per microbatch. Training state is18bytes/parameter. Retained layer-input checkpoints are BF16 and kept for every microbatch through forward fill. Each layer is recomputed during backward, so its forward matrix work is charged again. Two extra full BF16 boundary receive buffers per rank are conservatively counted without aliasing. This changes the earlier no-recompute matrix-work budget; it must not be priced as free memory savings.

| Model | PP | Microbatches | Peak accounted GB | Minimum unaccounted workspace headroom,80GB | Same,96GB |
|---|---:|---:|---:|---:|---:|
'''
for r in rows:s+=f"| {r['model']} | {r['pp']} | {r['microbatches']} | {r['peak_accounted_bytes']/1e9:.3f} | {r['minimum_workspace_headroom_80GB']/1e9:.3f} | {r['minimum_workspace_headroom_96GB']/1e9:.3f} |\n"
s+='''
A negative headroom rejects the candidate even before temporary workspace. A positive value is the maximum remaining allowance, not a proof of fit: recomputation intermediates, attention kernels, logits/loss, optimizer workspace, allocator fragmentation and framework allocations are unbounded here. Full memory feasibility therefore remains unproven.

Per link, each microbatch sends one BF16 `[tokens,4096]` forward activation and one same-shaped BF16 gradient backward. The rank list and every link's bytes are saved. For Qwen8's32768-token sequence each message is268435456bytes; for Qwen235's8192-token sequence it is67108864bytes. No DP collective is implied by DP1; no expert traffic crosses stages under EP1. Summing all links is network work, not elapsed time: stage dependencies, overlapping links and topology must be scheduled before bandwidth produces a completion time. Boundary gradient dtype is an explicit BF16 activation-gradient assumption, independent of FP32 parameter-gradient storage.

Exact parameter totals agree with the prior archived model calculations, and all stage work/state sums and forward/backward transfer identities are checked. Calculation sources are only read. Run `python run.py` to reproduce. Remaining10-4 work is the memory-workspace bound and a schedule/topology-based matched A100/A800 comparison with explicit H20 effective-performance assumptions; this partial result does not close the exercise.
'''
(R/'README.md').write_text(s)
(R/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in R.iterdir() if p.is_file() and p.name!='manifest.json'},indent=2)+'\n')
print([(r['model'],r['pp'],r['microbatches'],round(r['peak_accounted_bytes']/1e9,3)) for r in rows])
