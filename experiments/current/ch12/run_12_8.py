"""Deployment budgets using the displayed teaching table's rounded inputs."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
cfg={'local':(F(0),F('2.9'),F(0),F(0),None),'near':(F('.27'),F('.137'),F('.02'),F('.08'),600),'cloud':(F('.14'),F('.073'),F('.2'),F(1),700)}
def budget(name,n,redo=0,disconnect=False):
 prep,model,rtt,upload,power=cfg[name];step=F('.3')+model+rtt+upload
 replay=redo if name!='local' else 0;repair=F(2) if disconnect and name!='local' else F(0)
 total=prep+(n+replay)*step+repair
 energy=[F('.576')*45*n,F('.756')*45*n] if power is None else [power*(prep+(n+replay)*model)]*2
 return dict(name=name,round_s=float(step),total_s=float(total),energy_J=[float(e) for e in energy],redo_rounds=replay,after_round8_remaining_s=float(repair+(n-8+replay)*step) if disconnect else None)
rows20=[budget(k,20) for k in cfg];rows10=[budget(k,10) for k in cfg]
def choose(rows,deadline):
 feasible=[r for r in rows if r['total_s']<=deadline];return min(feasible,key=lambda r:r['energy_J'][1])['name']
faults=[]
for redo in [1,8]:
 rows=[budget(k,10,redo,True) for k in cfg]
 faults.append(dict(redo_remote_rounds=redo,rows=rows,selected_deadline23=choose(rows,23)))
base=F('.14')+20*(F('.3')+F('.073')+F('.2'));threshold=F(128)/(45-base)
assert base+128/threshold==45 and base>F('.27')+20*F('.537')
variable=base+10*F('6.4')/6+10*F('6.4')/10;constant=base+128/F(8)
assert variable>constant
src=ROOT/'manuscripts/12-端边云协同.md'
out=dict(exercise='12-8',kind='analytical_displayed_table_inputs',source_sha256={str(src.relative_to(ROOT)):hashlib.sha256(src.read_bytes()).hexdigest()},rounds20=rows20,rounds10=rows10,choice10_deadline23=choose(rows10,23),choice10_deadline15=choose(rows10,15),cloud_without_upload_s=float(base),cloud_deadline45_min_uplink_Mbps=float(threshold),variable_uplink_s=float(variable),constant8_uplink_s=float(constant),variable_extra_s=float(variable-constant),faults=faults)
(P/'12-8-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
