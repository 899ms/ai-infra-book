import hashlib,json,os,platform,subprocess,time
from pathlib import Path
B=Path(__file__).absolute().parent;out=B/'runs';client=out/'client';client.mkdir(exist_ok=False)
env=os.environ.copy();env.update(BOOK_WAN_PRIVATE=str(B/'private'),BOOK_AUDIO_OUT=str(client),BOOK_AUDIO_WAV=str(B/'fixture/audio.wav'),BOOK_AUDIO_SINK=str(B/'sink.py'))
cmd=[str(out/'client.test'),'-test.run=^TestBookAudioReplay$','-test.v','-test.timeout=10m'];start=time.time()
with (out/'client.log').open('w') as f:p=subprocess.run(cmd,cwd=B/'source',env=env,stdout=f,stderr=subprocess.STDOUT,timeout=660)
x=dict(command=cmd,start_unix_s=start,end_unix_s=time.time(),exit_code=p.returncode,platform=platform.platform(),binary_sha256=hashlib.sha256((out/'client.test').read_bytes()).hexdigest(),device_driver_sha256=hashlib.sha256((B/'sink.py').read_bytes()).hexdigest())
(out/'execution.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x));raise SystemExit(p.returncode)
