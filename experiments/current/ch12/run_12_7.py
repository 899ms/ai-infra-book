"""Trace one PCM block across saved runs without inventing a shared clock."""
from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
base=ROOT/'experiments/ch12/12-07';run=base/'audio-device/runs/cancel-false/round-0-pool-true-queqiao'
def lines(p):return [json.loads(x) for x in p.read_text().splitlines()]
path=ROOT/'references/author-context/queqiao-168ff4b/PATH-CHARACTER-DC-20260826.md'
s=path.read_text();cold=re.search(r'\| new connection, p50 \| ([\d.]+)ms \| \*\*([\d.]+)ms\*\*',s);warm=re.search(r'\| held open and tuned, p50 \| ([\d.]+)ms \| \*\*([\d.]+)ms\*\*',s);assert cold and warm
ratios={name:float(m[1])/float(m[2]) for name,m in [('new_connection',cold),('warm_tuned',warm)]}
ev=lines(run/'events.jsonl');origin=next(e for e in ev if e['kind']=='origin_write' and e['frame']==0);client=next(e for e in ev if e['kind']=='client_frame' and e['frame']==0)
reads=lines(run/'device-reads.jsonl');callbacks=lines(run/'device-callbacks.jsonl');cb=callbacks[0]
assert origin['bytes']==client['bytes']==cb['consumed_bytes']==1764 and reads[0]['bytes']>=1764
received=(run/'received.pcm').read_bytes();consumed=(run/'device-consumed.pcm').read_bytes();assert received==consumed
wav=(base/'tts-stream/replay/audio.wav').read_bytes();assert wav[44:]==received
original=(base/'tts-stream/runs/3-stream-true/response.wav').read_bytes();assert original[44:]==received
tr=lines(base/'tts-stream/runs/3-stream-true/reads.jsonl');first=next(r for r in tr if r['offset']+r['bytes']>=44+1764)
device=json.loads((run/'device.json').read_text());assert device['output_muted'] and device['acoustic_onset_ns'] is None
out=dict(exercise='12-7',ratios_of_medians=ratios,ideal_355KB_s=.23+355000*8/333000000,ideal_exact_file_s=.23+354640*8/333000000,unexplained_vs1s_s=1-(.23+355000*8/333000000),unexplained_vs_cold_direct_s=float(cold[1])/1000-(.23+354640*8/333000000),block=dict(index=0,bytes=1764,audio_ms=20,sample_rate=44100,sha256=hashlib.sha256(received[:1764]).hexdigest(),tts_request_to_complete_block_available_ms=first['elapsed_ns']/1e6,replay_go_origin_write_ms=origin['ns']/1e6,replay_go_client_frame_ms=client['ns']/1e6,replay_origin_write_to_client_ms=(client['ns']-origin['ns'])/1e6,helper_first_read_to_callback_ms=(cb['ns']-reads[0]['ns'])/1e6,callback_to_api_scheduled_output_ms=(cb['api_output_dac_time']-cb['api_current_time'])*1000,model_generation_timestamp=None,go_to_python_clock_offset=None,acoustic_onset=None,muted=True))
files=[path,ROOT/'manuscripts/12-端边云协同.md',base/'tts-stream/runs/3-stream-true/reads.jsonl',base/'tts-stream/runs/3-stream-true/response.wav',base/'tts-stream/replay/audio.wav',base/'audio-device/source/cmd/queqiaobench/book_audio_test.go',base/'audio-device/sink.py']+[run/n for n in ['events.jsonl','device-reads.jsonl','device-callbacks.jsonl','device.json','received.pcm','device-consumed.pcm']]
out['source_sha256']={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(P/'12-7-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'},indent=2))
