"""Rebuild a basic request-reading exercise from sealed successful evidence."""
import hashlib,json,re
from pathlib import Path
r=Path(__file__).absolute().parent
for x in json.loads((r/'provenance.json').read_text()):assert hashlib.sha256((r/x['file']).read_bytes()).hexdigest()==x['sha256']
cases=json.loads((r/'evidence/cases.json').read_text());requests=list(map(json.loads,(r/'evidence/requests.jsonl').read_text().splitlines()))
c=next(x for x in cases if x['id']=='n512-r0');q=next(x for x in requests if x['id']==c['id']);env=json.loads((r/'evidence/environment.json').read_text());supervisor=json.loads((r/'evidence/supervisor.json').read_text())
assert supervisor['exit_code']==0 and supervisor['leftovers']=={} and supervisor['reason'] is None
assert q['prompt_ids']==c['input_ids'] and q['finish_reason']=='stop' and json.loads(q['text'])==c['expected']
records=dict(re.findall(r'^(k\d{4}) = (\d{6})$',c['messages'][1]['content'],re.MULTILINE))
assert len(records)==512 and all(records[k]==v for k,v in c['expected'].items())
assert len(c['input_ids'])==7235 and len(q['output_ids'])==46
assert q['events'] and q['events'][-1][1]==len(q['output_ids'])
assert all(a[0]<=b[0] and a[1]<=b[1] for a,b in zip(q['events'],q['events'][1:]))
steps=[
 dict(id='A',label='Task and messages',layer=[1,2],role='Define the requested answer and prepare model input',evidence='cases.json: n512-r0 messages and expected'),
 dict(id='B',label='Tokenize and submit',layer=[2,3],role='Translate messages to token IDs and submit the request',evidence='driver.py: apply_chat_template and engine.generate; request prompt IDs match'),
 dict(id='C',label='Organize execution',layer=[3],role='Inference engine organizes request execution and cache capacity',evidence='environment.json: max_num_seqs=1, chunked prefill, KV config; not a scheduler trace'),
 dict(id='D',label='Execute model operations',layer=[4],role='Runtime dispatches model operations',evidence='driver.py uses vLLM; TRITON_ATTN configured; individual kernel timing is not supplied'),
 dict(id='E',label='Compute and resident data',layer=[5],role='CPU prepares/control; GPU executes; device memory holds model data and KV',evidence='successful RTX source run and its configuration; per-stage residency/traffic is not measured here'),
 dict(id='F',label='Decode and check answer',layer=[2,1],role='Decode returned tokens; application checks the requested result',evidence='driver.py checks decode; requests.jsonl contains final text; run.py validates exact JSON')]
summary=dict(request_id=c['id'],prompt_tokens=len(c['input_ids']),output_tokens=len(q['output_ids']),finish_reason=q['finish_reason'],answer=q['text'],expected=c['expected'],strict_answer_correct=True,steps=steps,layer6='Interconnect/data-center layer: no cross-host transfer or bandwidth measurement in this evidence; do not invent one.',scope='Existing single-host native request, reused for reading exercise. No new inference; no per-stage time attribution.')
(r/'result.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print('PASS: frozen successful request, exact prompt IDs, 46 returned tokens and exact JSON answer; six path labels generated')
