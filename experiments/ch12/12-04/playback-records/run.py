"""Explicit playback calculation from measured in-order TTS body arrival records."""
import hashlib,json,statistics,wave
from pathlib import Path
R=Path(__file__).resolve().parent;B=R.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audio=B/'tts-network/audio.wav'
with wave.open(str(audio),'rb') as w:
 assert (w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes())==(1,2,44100,591872)
 pcm=w.readframes(w.getnframes())
assert len(audio.read_bytes())==44+len(pcm)
paths=[*sorted((B/'tts-network/network-results').glob('*/requests.jsonl')),*sorted((B/'tts-chunking/results').glob('*/requests.jsonl')),*sorted((B/'receive-windows/results/tts').glob('*/requests.jsonl'))]
assert len(paths)==20
rows=[];sources={str(audio.relative_to(B)):sha(audio)}
for p in paths:
 sources[str(p.relative_to(B))]=sha(p)
 family='reuse' if 'tts-network' in p.parts else 'release' if 'tts-chunking' in p.parts else 'window'
 for index,r in enumerate(map(json.loads,p.read_text().splitlines())):
  assert r['valid'] and r['bytes']==len(audio.read_bytes()) and r['sha256']==sha(audio)
  arrivals=r['arrivals'];prev=r['start'];total=0
  for a in arrivals:
   total+=a['bytes'];assert a['total']==total and a['at']>=prev;prev=a['at']
  assert total==len(pcm)+44
  ready=[];j=0
  for off in range(0,len(pcm),1764):
   end=min(len(pcm),off+1764)+44
   while arrivals[j]['total']<end:j+=1
   ready.append(arrivals[j]['at']-r['start'])
  durations=[min(1764,len(pcm)-off)/88200 for off in range(0,len(pcm),1764)]
  assert len(ready)==672 and durations[-1]==100/88200
  # Three complete frames before starting, no device scheduling delay.
  start=ready[2];cursor=start;plays=[];stalls=[]
  for k,(at,duration) in enumerate(zip(ready,durations)):
   if at>cursor:stalls.append(dict(frame=k,start_s=cursor,end_s=at,seconds=at-cursor))
   cursor=max(cursor,at);plays.append(cursor);cursor+=duration
  # Independent closed-form max-plus recurrence, using media-time offsets.
  offsets=[min(k*1764,len(pcm))/88200 for k in range(len(ready))]
  bound=start
  for k in range(len(ready)):
   bound=max(bound,ready[k]-offsets[k]);assert abs(plays[k]-(offsets[k]+bound))<1e-8
  stall_s=sum(x['seconds'] for x in stalls)
  assert abs(cursor-start-len(pcm)/88200-stall_s)<1e-8
  assert all(t+1e-9>=a for t,a in zip(plays,ready))
  mode=p.parent.name if family=='reuse' else p.parent.name.split('-',1)[1]
  rows.append(dict(source=str(p.relative_to(B)),row=index,family=family,mode=mode,protocol=r['protocol'],reuse=r['reuse'],warmup=r['warmup'],first_play_s=start,finish_s=cursor,stall_s=stall_s,stall_count=len(stalls),stalls=stalls,frame_ready_s=ready,frame_play_s=plays,pcm_sha256=hashlib.sha256(pcm).hexdigest()))
assert len(rows)==196 and sum(not r['warmup'] for r in rows)==156
keys=sorted({(r['family'],r['mode'],r['protocol'],r['reuse']) for r in rows if not r['warmup']})
conditions=[]
for family,mode,proto,reuse in keys:
 selected=[r for r in rows if not r['warmup'] and (r['family'],r['mode'],r['protocol'],r['reuse'])==(family,mode,proto,reuse)]
 conditions.append(dict(family=family,mode=mode,protocol=proto,reuse=reuse,count=len(selected),first_play_ms=statistics.median(r['first_play_s']*1000 for r in selected),stall_ms=statistics.median(r['stall_s']*1000 for r in selected),max_stall_ms=max(r['stall_s']*1000 for r in selected),finish_s=statistics.median(r['finish_s'] for r in selected)))
(R/'results.json').write_text(json.dumps(dict(scope='Calculated playback from measured network arrivals; not acoustic measurement',records=196,formal=156,policy='3 complete20ms frames before start; wait on starvation; preserve all samples; no device latency',source_sha256=sources,conditions=conditions,rows=rows),indent=2)+'\n')
s='''# Playback calculated from measured TTS arrivals

All196 complete TTS network traces (156 formal,40 warmups) were replayed through an explicit playback calculation. The input is the measured arrival ledger for the exact mono44100Hz PCM16 WAV, covering reuse (both loss profiles), release/coalescing and matched receive-window matrices. No new network/model execution or speaker/microphone measurement is claimed.

Policy: collect three complete20ms frames, start immediately, consume frames in order at44100Hz, and wait when the next full frame is unavailable. Waiting preserves samples and adds stall time; no samples are dropped or silently replaced. The final100-byte partial frame keeps its exact duration. Header bytes are excluded. Device startup latency, scheduling jitter and acoustic latency are absent from this declared calculation.

| Matrix | Mode | Protocol | Reuse | Formal n | First play ms | Median stall ms | Max stall ms | Finish seconds |
|---|---|---|---|---:|---:|---:|---:|---:|
'''
for c in conditions:s+=f"| {c['family']} | {c['mode']} | {c['protocol']} | {c['reuse']} | {c['count']} | {c['first_play_ms']:.3f} | {c['stall_ms']:.3f} | {c['max_stall_ms']:.3f} | {c['finish_s']:.3f} |\n"
s+='''
Every trace retains all672 frame availability/start times and every stall interval. A sequential event calculation is checked against an independent max-plus expression; finish minus start equals exact audio duration plus stalls. No frame starts before its last source byte arrives. Full source/result SHA, arrival conservation and temporal order are checked before playback calculation.

These results satisfy the playback-analysis form allowed by the original calculation/network-record condition. They do not turn calculated first play into measured audible onset or prove that a particular real player has this buffering policy. The adjacent12-7 actual muted device measurements demonstrate why hardware feed starvation and driver flags need separate observation. Recovery playback is outside this uninterrupted-trace table: a full restart can repeat audio already played, even when the final stored WAV is byte-exact.

Run `python run.py` to regenerate this table and results from the bound source ledgers. Original transport verifiers and reports remain the authority for those experiments' protocol checks.
'''
(R/'README.md').write_text(s)
print({'records':len(rows),'formal':156,'max_stall_s':max(r['stall_s'] for r in rows)})
