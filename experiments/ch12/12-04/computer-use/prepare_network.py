import base64,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent;D=R/'structured-agent-results/trial0';O=R/'network-fixtures';O.mkdir(exist_ok=False)
result=json.loads((D/'result.json').read_text());assert result['passed']
rows=[]
for p in sorted(D.glob('step*.json')):
 r=json.loads(p.read_text());i=r['step'];png=(D/f'step{i:02d}.png').read_bytes();request=json.dumps(dict(id=f't0-s{i}',image=base64.b64encode(png).decode(),instruction=r['request_instruction'],max_tokens=160)).encode();response=r['response']['text'].encode()
 (O/f'request{i}.json').write_bytes(request);(O/f'response{i}.json').write_bytes(response)
 rows.append(dict(step=i,upload_file=f'network-fixtures/request{i}.json',response_file=f'network-fixtures/response{i}.json',upload_sha256=hashlib.sha256(request).hexdigest(),response_sha256=hashlib.sha256(response).hexdigest(),upload_bytes=len(request),response_bytes=len(response),service_s=r['response']['end_s']-r['response']['start_s'],action=r['action'],browser_action_s=r['action_end_s']-r['action_start_s'],screenshot_s=r['screenshot_end_s']-r['screenshot_start_s']))
(R/'network-fixture.json').write_text(json.dumps(dict(source_trial=0,scope='Fixed actual first constrained trial screenshot/instruction uploads and action outputs; measured GPU service waits replayed, no new inference or browser execution',steps=rows),indent=2)+'\n')
