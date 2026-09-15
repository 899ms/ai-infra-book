import hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[3];sources={};rows=[]
def load(n):
 p=ROOT/'calculations/results'/n;sources[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
keep=['a100-80gb-sxm','h100-sxm','b200-sxm']
for n in ['training-deadline-book.json','training-deadline-qwen235.json']:
 x=load(n)
 for r in x['training_deadline_rows']:
  if r['device'] not in keep:continue
  cards=r['combined_necessary_count'];hours=F(r['conditional_training_seconds_exact'])*cards/3600
  expected=F(x['summary']['task_training_matrix_flops'])/(F(r['matrix_work_efficiency_exact'])*F(r['bf16_fp32_dense_peak_flops_exact'])*3600);assert hours==expected
  rows.append(dict(task=x['model'],tokens=x['scenario']['task_tokens'],efficiency=r['matrix_work_efficiency_exact'],deadline_days=x['scenario']['deadline_days'],device=r['device'],necessary_cards=cards,compute_gpu_hours_exact=str(hours),deadline_reserved_gpu_hours=cards*x['scenario']['deadline_days']*24,quality_acceptance=None,full_layout_feasibility=None))
x=load('dense-training-scale-book.json')
for r in x['dense_scale_rows']:
 if r['device'] not in keep:continue
 for deadline in r['deadline_requirements']:
  hours=F(r['algorithm_flops'])/(F(r['efficiency_exact'])*F(str(r['peak_bf16_fp32_dense_tflops']))*10**12*3600);cards=deadline['necessary_card_count'];d=deadline['deadline_days'];assert hours<=cards*d*24
  rows.append(dict(task=f"dense-{r['parameters']//10**12}T",tokens=r['task_tokens'],efficiency=r['efficiency_exact'],deadline_days=d,device=r['device'],necessary_cards=cards,compute_gpu_hours_exact=str(hours),deadline_reserved_gpu_hours=cards*d*24,quality_acceptance=None,full_layout_feasibility=None))
assert len(rows)==72
pairs=[]
for task,eff,deadline in sorted({(r['task'],r['efficiency'],r['deadline_days']) for r in rows}):
 group=[r for r in rows if (r['task'],r['efficiency'],r['deadline_days'])==(task,eff,deadline)];assert len(group)==3
 for a,b in itertools.combinations(sorted(group,key=lambda r:keep.index(r['device'])),2):
  ratio=F(a['compute_gpu_hours_exact'])/F(b['compute_gpu_hours_exact']);reserved=F(a['deadline_reserved_gpu_hours'],b['deadline_reserved_gpu_hours'])
  # p_A=1,p_B=ratio makes modeled costs identical, exact rational arithmetic.
  assert F(a['compute_gpu_hours_exact'])==ratio*F(b['compute_gpu_hours_exact'])
  assert a['deadline_reserved_gpu_hours']==reserved*b['deadline_reserved_gpu_hours']
  pairs.append(dict(task=task,efficiency=eff,deadline_days=deadline,device_a=a['device'],device_b=b['device'],b_over_a_price_break_even_compute=str(ratio),b_over_a_price_break_even_reserved=str(reserved),b_cheaper_condition='p_B/p_A below the corresponding boundary; same currency, task and quality, all modeled conditions met'))
assert len(pairs)==72
(R/'results.json').write_text(json.dumps(dict(scope='Conditional rental-price boundaries, not invoices or quality-qualified rankings',source_sha256=sources,rows=rows,pairs=pairs),indent=2)+'\n')
s='''# Conditional cost boundaries for historical10-10

72 A100/H100/B200 cases and72 pairwise price boundaries were calculated from the archived Qwen8/Qwen235 and1T/5T/10T Dense cases. The exact rational checks establish equal modeled cost at every boundary. Original calculation files are only read; no rental price, invoice or quality result is invented.

Let H be modeled compute GPU-hours, G the necessary card count and d the deadline days. Immediate release after modeled computation costs `p*H`; reserving all G cards through the deadline costs `p*G*d*24`. For two devices A/B, B costs less iff `p_B/p_A < H_A/H_B` in the first convention, or below the reserved-hour ratio in the second. Currency, task, precision, quality and included charges must agree. These are conditions, not a recommendation that the aggregate lower-bound card counts form a feasible cluster.

| Task | MFU/effectiveness | Deadline days | Pair A→B | Break-even B/A price, compute-only | Same, full-deadline reservation |
|---|---|---:|---|---:|---:|
'''
for p in pairs:
 if p['efficiency']=='2/5':s+=f"| {p['task']} | {p['efficiency']} | {p['deadline_days']} | {p['device_a']} → {p['device_b']} | {float(F(p['b_over_a_price_break_even_compute'])):.6f} | {float(F(p['b_over_a_price_break_even_reserved'])):.6f} |\n"
s+='''
All30%/40%/50% cases remain in results.json; this table shows40%. The fixed task's ideal compute GPU-hours are independent of card count in this linear model. Capacity floors and integer card rounding can change the reservation ratio considerably, especially for Qwen235: a faster device may sit idle within a fixed reservation. A real scheduler's release behavior determines which accounting applies.

Preparation, data stalls, checkpoint pauses, restart and lost work are not silently set to zero in an actual bill. If not already included in the efficiency denominator, their allocated GPU-hours and other costs must be added using allocation intervals; after recovery, only newly completed work is credited. Existing public-training records demonstrate why cumulative tokens cannot be divided by one resumed run's duration. Actual resource intervals, prices and non-GPU costs remain unknown here.

Quality acceptance and complete per-card layout feasibility remain null in every row. A finite arithmetic price boundary is not a quality-qualified cost frontier. No V4 row is substituted with V3 or dense6ND: the matching full V4 training task/work and quality/calibration evidence still need explicit treatment. This artifact completes the conditional price algebra for the available tasks; it does not close historical10-10.
'''
(R/'README.md').write_text(s);(R/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in R.iterdir() if p.is_file() and p.name!='manifest.json'},indent=2)+'\n');print({'cases':len(rows),'price_boundaries':len(pairs)})
