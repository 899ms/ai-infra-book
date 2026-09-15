import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent
ROOT=R.parents[3]
S=ROOT/'experiments/ch12/12-07/tts-stream'
source=S/'runs/3-stream-true'
request=(source/'request.json').read_bytes()
response=(S/'replay/audio.wav').read_bytes()
original=(source/'response.wav').read_bytes()
assert len(response)==len(original) and response[44:]==original[44:]
reads=[json.loads(x) for x in (source/'reads.jsonl').read_text().splitlines()]
offset=0;plan=[]
for read in reads:
    assert read['offset']==offset
    if read['bytes']:
        plan.append(dict(offset=offset,bytes=read['bytes'],ready_s=read['elapsed_ns']/1e9))
        offset+=read['bytes']
assert offset==len(response)
assert all(a['ready_s']<=b['ready_s'] for a,b in zip(plan,plan[1:]))
(R/'request.json').write_bytes(request)
(R/'audio.wav').write_bytes(response)
fixture=dict(upload_file='request.json',response_file='audio.wav',
    upload_sha256=hashlib.sha256(request).hexdigest(),response_sha256=hashlib.sha256(response).hexdigest(),
    release_plan=plan,service_s=plan[-1]['ready_s'],
    source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source/'request.json',source/'response.wav',source/'reads.jsonl',source/'execution.json',S/'replay/audio.wav']},
    scope='Actual TTS PCM with source client-read availability schedule replayed after complete request receipt; not a new model run or native model chunk timing')
(R/'tts-fixture.json').write_text(json.dumps(fixture,indent=2)+'\n')
print(json.dumps(dict(response_bytes=len(response),release_segments=len(plan),first_audio_ready_s=plan[1]['ready_s'],last_ready_s=plan[-1]['ready_s'])))
