"""Capacity lower bounds under the chapter's rounded packed-weight model."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
source=next((ROOT/'manuscripts').glob('07-*.md'))
rows=[]
for name,parameters in [('DeepSeek V4-Pro',1600*10**9),('Kimi K3',2800*10**9)]:
 weights=parameters//2
 for reserve in (0,8*10**9):
  usable=80*10**9-reserve; per_server=8*usable
  servers=(weights+per_server-1)//per_server; cards=(weights+usable-1)//usable
  assert (servers-1)*per_server<weights<=servers*per_server
  assert (cards-1)*usable<weights<=cards*usable
  # Ideal balanced placement across every card in the reserved servers.
  weight_card=F(weights,servers*8); total=weight_card+reserve
  assert total<=80*10**9
  rows.append(dict(model=name,weight_bytes=weights,reserve_per_card_bytes=reserve,usable_per_server_bytes=per_server,minimum_cards=cards,minimum_eight_card_servers=servers,allocated_cards=servers*8,balanced_weight_per_card_GB=float(weight_card/10**9),balanced_total_per_card_GB=float(total/10**9),aggregate_free_GB=float(F(servers*8*80*10**9-weights-servers*8*reserve,10**9)),PP_stage_boundaries_per_forward=servers-1))
out=dict(exercise='7-1',capacity=rows,scope='Rounded manuscript parameter counts and 0.5 byte/parameter; ideal balanced capacity lower bounds, not measured deployment or tensor-divisibility proof',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'7-1-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
