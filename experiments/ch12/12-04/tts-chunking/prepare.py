import hashlib,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parent
S=R.parent/'tts-network'
source=json.loads((S/'tts-fixture.json').read_text())
for name in ['audio.wav','request.json']:shutil.copyfile(S/name,R/name)
size=(R/'audio.wav').stat().st_size
original=source['release_plan']
def ready(end):return next(r['ready_s'] for r in original if r['offset']+r['bytes']>=end)
coalesced=[dict(offset=0,bytes=44,ready_s=ready(44))]
for offset in range(44,size,65536):
    end=min(size,offset+65536)
    coalesced.append(dict(offset=offset,bytes=end-offset,ready_s=ready(end)))
plans=dict(recorded=original,coalesce64k=coalesced,whole=[dict(offset=0,bytes=size,ready_s=ready(size))])
for mode,plan in plans.items():
    offset=0
    for row in plan:
        assert row['offset']==offset
        offset+=row['bytes']
        assert row['ready_s']==ready(offset)
    assert offset==size
    fixture=dict(source,release_plan=plan,chunk_mode=mode,
        baseline_fixture_sha256=hashlib.sha256((S/'tts-fixture.json').read_bytes()).hexdigest(),
        scope='Chunk policy applied to the same actual TTS byte-availability trace; no new synthesis')
    (R/(mode+'-fixture.json')).write_text(json.dumps(fixture,indent=2)+'\n')
print({mode:len(plan) for mode,plan in plans.items()})
