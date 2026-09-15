import hashlib,json,itertools
from pathlib import Path
import torch
R=Path(__file__).resolve().parent;rows=[]
for task in ['extract','sequence']:
 files=sorted((R/'results').glob(task+'-*.pt'));loaded={p.name:torch.load(p,map_location='cpu',weights_only=True)['adapter'] for p in files}
 for a,b in itertools.combinations(loaded,2):
  for name in ['A','B']:
   x,y=loaded[a][name],loaded[b][name];d=x-y
   rows.append(dict(a=a,b=b,tensor=name,equal=torch.equal(x,y),differing_values=int(torch.count_nonzero(d)),max_abs=float(d.abs().max()),relative_l2=float(d.norm()/x.norm()) if x.norm() else None))
(R/'checkpoint-comparison.json').write_text(json.dumps(dict(rows=rows,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n');print('max_abs',max(x['max_abs'] for x in rows),'max_relative_l2',max(x['relative_l2'] or 0 for x in rows))
