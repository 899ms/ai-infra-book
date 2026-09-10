import hashlib,json,os,subprocess
from pathlib import Path
B=Path(__file__).absolute().parent;out=B/'runs';out.mkdir(exist_ok=True)
for r in json.loads((B/'source-lock.json').read_text())['files']:
 data=(B/'source'/r['path']).read_bytes();assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256']
meta={}
for target in ['mac','linux']:
 env=os.environ.copy();env['GOTOOLCHAIN']='auto'
 if target=='linux':env.update(GOOS='linux',GOARCH='amd64',CGO_ENABLED='0')
 binary=out/('client.test' if target=='mac' else 'server.test')
 cmd=['go','test','-c','-buildvcs=false','-o',str(binary),'./cmd/queqiaobench']
 with (out/f'build-{target}.log').open('w') as f:subprocess.run(cmd,cwd=B/'source',env=env,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=300)
 meta[target]=dict(command=cmd,sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),build_info=subprocess.check_output(['go','version','-m',str(binary)],text=True))
meta['harness_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (B/'source/cmd/queqiaobench').glob('book*test.go')}
(out/'build.json').write_text(json.dumps(meta,indent=2)+'\n')
print('Both native binaries built')
