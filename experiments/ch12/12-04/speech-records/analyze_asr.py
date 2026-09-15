import hashlib,json,re,statistics
from pathlib import Path
R=Path(__file__).resolve().parent
ROOT=R.parents[3]
env=json.loads((R/'asr-results/environment.json').read_text())
assert hashlib.sha256((R/'run_asr.py').read_bytes()).hexdigest()==env['source_sha256']
assert hashlib.sha256((R/'audio.wav').read_bytes()).hexdigest()==env['audio_sha256']
source=ROOT/'experiments/ch12/12-07/tts-stream/runs/3-stream-true/request.json'
reference=json.loads(source.read_text())['text']
rows=json.loads((R/'asr-results/requests.json').read_text())
assert len(rows)==4 and [r['warmup'] for r in rows]==[True,False,False,False]
assert all(r['start_ns']<=r['first_segment_ns']<=r['end_ns'] for r in rows)
def tokens(s):return re.findall(r"[a-z0-9]+",s.lower())
def distance(a,b):
    prior=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        current=[i]
        for j,y in enumerate(b,1):current.append(min(prior[j]+1,current[j-1]+1,prior[j-1]+(x!=y)))
        prior=current
    return prior[-1]
records=[]
for row in rows:
    a,b=tokens(reference),tokens(row['text'])
    records.append(dict(trial=row['trial'],warmup=row['warmup'],text=row['text'],
        service_s=(row['end_ns']-row['start_ns'])/1e9,reference_words=len(a),recognized_words=len(b),
        word_edit_distance=distance(a,b),normalized_wer=distance(a,b)/len(a)))
formal=records[1:]
assert len({r['text'] for r in formal})==1
assert json.loads((R/'cleanup.json').read_text())['process_absent']
response=(formal[0]['text']+'\n').encode()
(R/'transcript.txt').write_bytes(response)
fixture=dict(upload_file='audio.wav',response_file='transcript.txt',
    upload_sha256=env['audio_sha256'],response_sha256=hashlib.sha256(response).hexdigest(),
    service_s=statistics.median(r['service_s'] for r in formal),
    source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,R/'asr-results/requests.json',R/'asr-results/environment.json']},
    scope='Actual ASR input/result with median GPU service-time replay; no per-protocol model execution')
(R/'asr-fixture.json').write_text(json.dumps(fixture,indent=2)+'\n')
(R/'asr-summary.json').write_text(json.dumps(dict(reference=reference,normalization='lowercase ASCII alphanumeric word sequences; punctuation ignored; standard unit-cost word Levenshtein',records=records,fixture=fixture),indent=2)+'\n')
print(json.dumps(records,indent=2))
