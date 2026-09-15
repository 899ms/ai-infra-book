import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent
s=json.loads((P/'additional-training/samples.json').read_text());formal=json.loads((P/'formal/summary.json').read_text());samples=[];mapping=[]
for item in s['samples']:
 ref=next(x for x in formal['results'] if x['task']==item['task'] and x['strategy']=='baseline')
 assert json.loads(item['expected_text'])==json.loads(ref['text'])
 # The already verified Mac baseline serialization is the fixed canonical form for this task.
 a={**item,'output_ids':ref['token_ids'],'expected_text':ref['text']};a['sample_sha256']=hashlib.sha256(json.dumps([a['prompt_ids'],a['output_ids']],separators=(',',':')).encode()).hexdigest();samples.append(a)
 mapping.append(dict(request_id=item['request_id'],raw_output_positions=len(item['output_ids']),canonical_output_positions=len(a['output_ids']),raw_sample_sha256=item['sample_sha256'],canonical_sample_sha256=a['sample_sha256'],semantic_content_equal=True,token_positions_identical=item['output_ids']==a['output_ids']))
sources={n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['additional-training/samples.json','formal/summary.json']}
(R/'samples.json').write_text(json.dumps(dict(samples=samples,source_sha256=sources),indent=2)+'\n');(R/'normalization.json').write_text(json.dumps(mapping,indent=2)+'\n')
