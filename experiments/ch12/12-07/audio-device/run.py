import hashlib,json,os,platform,subprocess,time
from pathlib import Path
B=Path(__file__).absolute().parent
lock=json.loads((B/'source-lock.json').read_text())
for r in lock['files']:
 data=(B/'source'/r['path']).read_bytes();assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256']
out=B/'runs';out.mkdir(exist_ok=False)
env=os.environ.copy();env['GOTOOLCHAIN']='auto';env['BOOK_AUDIO_OUT']=str(out);env['BOOK_AUDIO_WAV']=str(B/'fixture/audio.wav');env['BOOK_AUDIO_SINK']=str(B/'sink.py')
binary=out/'audio-replay.test'
with (out/'build.log').open('w') as f:subprocess.run(['go','test','-c','-buildvcs=false','-o',str(binary),'./cmd/queqiaobench'],cwd=B/'source',env=env,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=600)
cmd=[str(binary),'-test.run=^TestBookAudioReplay$','-test.v','-test.timeout=10m'];start=time.time()
with (out/'native.log').open('w') as f:p=subprocess.run(cmd,cwd=B/'source',env=env,stdout=f,stderr=subprocess.STDOUT,timeout=660)
x=dict(command=cmd,start_unix_s=start,end_unix_s=time.time(),exit_code=p.returncode,platform=platform.platform(),revision=lock['revision'],harness_sha256=hashlib.sha256((B/'source/cmd/queqiaobench/book_audio_test.go').read_bytes()).hexdigest(),binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),build_info=subprocess.check_output(['go','version','-m',str(binary)],text=True))
(out/'execution.json').write_text(json.dumps(x,indent=2)+'\n');binary.unlink();print(json.dumps(x));raise SystemExit(p.returncode)
