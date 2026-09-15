import hashlib,json
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[3]
files=['training-qwen3-8b-t32768.json','training-qwen3-235b-balanced.json'];rows=[];sources={}
for name in files:
 p=ROOT/'calculations/results'/name;x=json.loads(p.read_text());sources[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();s=x['summary'];work=F(s['training_matrix_flops'],s['input_tokens'])*100_000_000_000
 assert sum(x['parameter_state_bytes'].values())==s['unsharded_parameter_state_bytes']==18*s['parameters']
 for cards in [16,32,64,128]:
  deadline=30*86400;budget_per_sequence=F(deadline*s['input_tokens'],100_000_000_000)
  for communication_gb in [0,1,10,100]:
   for bandwidth in [100,150]:
    # Declared EXPOSED per-device traffic, not inferred from a parallel layout.
    comm=F(communication_gb,bandwidth);remaining=budget_per_sequence-comm
    required=None if remaining<=0 else F(s['training_matrix_flops'],cards)/remaining
    if required is not None:assert F(s['training_matrix_flops'],cards)/required+comm==budget_per_sequence
    rows.append(dict(model=x['model'],sequence_tokens=s['input_tokens'],cards=cards,persistent_bytes_per_card_ideal=str(F(s['unsharded_parameter_state_bytes'],cards)),task_tokens=100_000_000_000,deadline_days=30,exposed_gb_per_card_per_sequence=communication_gb,assumed_effective_gb_s=bandwidth,communication_seconds=float(comm),sequence_time_budget_seconds=float(budget_per_sequence),required_effective_matrix_tflops_per_card=None if required is None else float(required/10**12),required_exact=None if required is None else str(required),task_matrix_flops_exact=str(work)))
(R/'results.json').write_text(json.dumps(dict(scope='Conditional lower-bound sensitivity; not candidate-layout or measured hardware completion',source_sha256=sources,rows=rows),indent=2)+'\n')
s='''# Conditional deadline thresholds — partial10-4 calculation

The original exercise permits assumed effective performance for H20. These calculations use existing model-specific matrix work, not inference throughput and not6ND for MoE. Both tasks declare100B tokens and30 days. Qwen8 uses the archived32768-token workload; Qwen235 uses8192 tokens with balanced routing. They are separate tasks, not a matched cross-model speed benchmark. Within each task all hardware cases hold work fixed.

Persistent state is18bytes/parameter: BF16 weights plus FP32 gradients, master weights and two Adam moments. Ideal even division is a lower bound only; it excludes tensor/replica placement, activations, buffers, communication workspace and imbalance. No candidate is called memory-feasible on this basis.

For a sequence, let W be its recorded matrix FLOPs, G cards, b the deadline's allowed sequence time, and c the exposed communication time. Required effective matrix progress per card is W/[G(b−c)], if b>c. Otherwise the communication budget alone makes the deadline impossible. The exact rational inverse is independently checked for every feasible row. Effective progress here excludes the separately added exposed communication; using an MFU measured over total step time would double-count communication.

The100/150GB/s rates are explicit illustrative effective per-device bandwidths, not measured A800/A100 throughput. They model the same2:3 ratio as the archived400/600GB/s NVLink aggregate specifications; directionality, topology and actual efficiency still require verification for a concrete layout. Exposed1/10/100GB per sequence is a sensitivity input, not derived collective traffic. H20 must be compared to the required effective rate using measured or explicitly assumed values, not an invented specification.

| Model | Cards | Ideal persistent GB/card | Required effective TFLOP/s/card, no exposed communication |
|---|---:|---:|---:|
'''
for r in rows:
 if r['exposed_gb_per_card_per_sequence']==0 and r['assumed_effective_gb_s']==100:s+=f"| {r['model']} | {r['cards']} | {float(F(r['persistent_bytes_per_card_ideal']))/1e9:.3f} | {r['required_effective_matrix_tflops_per_card']:.3f} |\n"
s+='''
results.json contains all64 conditions, including explicit communication-impossible cases. These are conditional thresholds and do not close10-4. Remaining work is to bind actual candidate layouts to per-card state/activation peaks and communication volume, compare matched-form A100/A800 with only the checked interconnect variable changed, and evaluate explicit H20 assumptions against those layouts. Source calculation files are read-only and unchanged.
'''
(R/'README.md').write_text(s)
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in R.iterdir() if p.is_file() and p.name!='manifest.json'};(R/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print({'conditions':len(rows),'communication_impossible':sum(r['required_exact'] is None for r in rows)})
