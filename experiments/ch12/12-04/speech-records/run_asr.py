import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import time
import wave
from faster_whisper import WhisperModel

R=Path(__file__).resolve().parent
OUT=R/'asr-results'
OUT.mkdir(exist_ok=False)
audio=R/'audio.wav'
model=Path('/home/ubuntu/.cache/huggingface/hub/models--Systran--faster-whisper-base.en/snapshots/3d3d5dee26484f91867d81cb899cfcf72b96be6c')
with wave.open(str(audio)) as f:
    audio_info=dict(rate=f.getframerate(),channels=f.getnchannels(),sample_width=f.getsampwidth(),frames=f.getnframes())
environment=dict(pid=os.getpid(),model=str(model),device='cuda',compute_type='float16',
    packages={x:importlib.metadata.version(x) for x in ['faster-whisper','ctranslate2','av']},
    source_sha256=hashlib.sha256((R/'run_asr.py').read_bytes()).hexdigest(),
    audio_sha256=hashlib.sha256(audio.read_bytes()).hexdigest(),audio=audio_info,
    checkpoint_sha256={str(p.relative_to(model)):hashlib.sha256(p.read_bytes()).hexdigest() for p in model.rglob('*') if p.is_file()})
(OUT/'environment.json').write_text(json.dumps(environment,indent=2)+'\n')
begin=time.perf_counter_ns()
recognizer=WhisperModel(str(model),device='cuda',compute_type='float16',local_files_only=True)
loaded=time.perf_counter_ns()
records=[]
for trial in range(4):
    start=time.perf_counter_ns()
    segments,info=recognizer.transcribe(str(audio),language='en',beam_size=5,temperature=0,
        vad_filter=False,condition_on_previous_text=False,word_timestamps=True)
    rows=[]
    first=None
    for segment in segments:
        now=time.perf_counter_ns()
        if first is None:first=now
        rows.append(dict(id=segment.id,start=segment.start,end=segment.end,text=segment.text,
                         words=[dict(word=w.word,start=w.start,end=w.end,probability=w.probability) for w in segment.words]))
    end=time.perf_counter_ns()
    records.append(dict(trial=trial,warmup=trial==0,start_ns=start,first_segment_ns=first,end_ns=end,
                        language=info.language,duration=info.duration,segments=rows,
                        text=''.join(s['text'] for s in rows).strip()))
    (OUT/'requests.json').write_text(json.dumps(records,indent=2)+'\n')
    print(trial,(end-start)/1e9,records[-1]['text'],flush=True)
(OUT/'completion.json').write_text(json.dumps(dict(requests=len(records),model_load_s=(loaded-begin)/1e9))+'\n')
