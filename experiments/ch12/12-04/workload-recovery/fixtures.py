import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent

def load(workload):
 if workload in ['asr','tts']:
  S=R.parent/('speech-records' if workload=='asr' else 'tts-network');f=json.loads((S/('asr-fixture.json' if workload=='asr' else 'tts-fixture.json')).read_text());request=(S/f['upload_file']).read_bytes();response=(S/f['response_file']).read_bytes()
  assert hashlib.sha256(request).hexdigest()==f['upload_sha256'] and hashlib.sha256(response).hexdigest()==f['response_sha256']
  plan=f['release_plan'] if workload=='tts' else [dict(offset=0,bytes=len(response),ready_s=f['service_s'])]
  return [dict(step=0,request=request,response=response,release_plan=plan,source=f)]
 S=R.parent/'computer-use';f=json.loads((S/'network-fixture.json').read_text());out=[]
 for r in f['steps']:
  request=(S/r['upload_file']).read_bytes();response=(S/r['response_file']).read_bytes();assert hashlib.sha256(request).hexdigest()==r['upload_sha256'] and hashlib.sha256(response).hexdigest()==r['response_sha256']
  out.append(dict(step=r['step'],request=request,response=response,release_plan=[dict(offset=0,bytes=len(response),ready_s=r['service_s'])],source=r))
 return out
