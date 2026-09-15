"""Logical forward-call and KV-position accounting, not a runtime benchmark."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
source=next((ROOT/'manuscripts').glob('09-*.md'))
rows=[]
for outputs in [1025,1]:
 L=8192;positions=list(range(L));returned=[]
 # Prefill consumes the entire input and predicts first output position.
 returned.append(L)
 for _ in range(outputs-1):
  positions.append(returned[-1]);returned.append(returned[-1]+1)
 assert len(positions)==L+outputs-1
 assert returned[-1]==len(positions) and returned[-1] not in positions
 assert positions==list(range(returned[-1]))
 rows.append(dict(input_tokens=L,output_tokens=outputs,prefill_calls=1,decode_calls=outputs-1,total_forward_calls=outputs,KV_tokens_after_prefill=L,KV_tokens_at_end=len(positions),KV_bytes_at_end=len(positions)*147456,last_returned_without_KV_zero_based_position=returned[-1],PD_handoffs_needed_for_current_generation=int(outputs>1),PD_payload_bytes_for_current_generation=1207959552 if outputs>1 else 0))
out=dict(exercise='9-1',cases=rows,scope='Single request, cold prompt, unchunked prefill, ordinary autoregressive decode. Shared cache adds storage operations, not model calls; hits require explicit valid prefix and last-token/logits boundary.',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'9-1-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
