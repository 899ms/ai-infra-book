"""Six official scenarios, twelve real unified CLI calls, streamed byte comparison."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,tempfile,time
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent.parent
MANIFEST=PROJECT/'results/manifest.json'

def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  while chunk:=f.read(1048576):h.update(chunk)
 return h.hexdigest()

def source_hashes():
 paths=sorted((PROJECT/'src/infra_calc/transport').glob('*.py'))+[PROJECT/'src/infra_calc/topics/transport_closed_loop.py',PROJECT/'src/infra_calc/topics/transport_sender.py',PROJECT/'src/infra_calc/cli.py',PROJECT/'src/infra_calc/sources.py',PROJECT/'configs/sources.lock.json',PROJECT/'scenarios/book.json']
 return {str(p.relative_to(PROJECT)):digest(p) for p in paths}

def fingerprint(rows):return hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()

def readiness():
 cases=[r for r in json.loads((PROJECT/'scenarios/book.json').read_text())['transport_closed_loop'] if r['id'].startswith('controller-loop-')]
 assert len(cases)==6
 manifest=json.loads(MANIFEST.read_text());entries={r['file']:r['sha256'] for r in manifest['artifacts']}
 missing=[]
 for row in cases:
  for fmt in ('json','md'):
   name='results/'+row['id']+'.'+fmt
   if name not in entries or not (PROJECT/name).is_file():missing.append(name)
 return cases,entries,missing

def compare(expected,actual):
 eh=hashlib.sha256();ah=hashlib.sha256();equal=True;eb=ab=0
 with expected.open('rb') as a,actual.open('rb') as b:
  while True:
   x=a.read(1048576);y=b.read(1048576)
   if not x and not y:break
   eh.update(x);ah.update(y);eb+=len(x);ab+=len(y);equal&=x==y
 return dict(expected_sha256=eh.hexdigest(),actual_sha256=ah.hexdigest(),expected_bytes=eb,actual_bytes=ab,bytewise_equal=equal)

def run():
 cases,entries,missing=readiness()
 if missing:
  print(json.dumps(dict(status='waiting_for_existing_reproduce',missing=missing),indent=2));return None
 code_before=source_hashes();code_fingerprint=fingerprint(code_before);manifest_before=digest(MANIFEST);started=time.monotonic();checks=[]
 for case in cases:
  for fmt in ('json','md'):
   pre=source_hashes();assert pre==code_before,'public source changed before CLI call'
   before=time.monotonic()
   with tempfile.TemporaryDirectory(prefix='controller-cli-') as td:
    td=Path(td);inp=td/'input.json';out=td/('actual.'+fmt)
    inp.write_text(json.dumps(case['inputs'],indent=2)+'\n')
    cmd=[sys.executable,str(PROJECT/'calc.py'),'transport-closed-loop','--inputs',str(inp),'--format',fmt,'--output',str(out)]
    completed=subprocess.run(cmd,capture_output=True,text=True)
    assert completed.returncode==0,(case['id'],fmt,completed.stderr)
    relative='results/'+case['id']+'.'+fmt
    record=compare(PROJECT/relative,out)
    assert record['expected_sha256']==entries[relative],(relative,'official result differs from manifest')
    assert record['bytewise_equal'],(relative,'actual CLI differs from official result')
    post=source_hashes();assert pre==post,'public source changed during CLI call'
    checks.append(dict(id=case['id'],format=fmt,command='calc.py transport-closed-loop --inputs <exact temporary input> --format '+fmt+' --output <temporary output>',input=case['inputs'],input_sha256=digest(inp),expected_file=relative,manifest_expected_sha256=entries[relative],**record,source_fingerprint_before=fingerprint(pre),source_fingerprint_after=fingerprint(post),elapsed_seconds=round(time.monotonic()-before,3)))
   print(case['id'],fmt,'PASS; temporary input/output released',flush=True)
  # Retain progress evidence; a partial file never claims full completion.
  (ROOT/'cli-check-progress.json').write_text(json.dumps(dict(status='running',completed_calls=len(checks),checks=checks),indent=2)+'\n')
 code_after=source_hashes();assert code_before==code_after and digest(MANIFEST)==manifest_before
 return dict(status='passed',scenario_count=len(cases),cli_calls=len(checks),checks=checks,source_hashes_before=code_before,source_hashes_after=code_after,source_fingerprint=code_fingerprint,results_manifest_sha256=manifest_before,elapsed_seconds=round(time.monotonic()-started,3),scope='Twelve actual CLI calls and full streamed byte equality against official manifested artifacts; not a reproduction run')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--ready',action='store_true');args=ap.parse_args()
 if args.ready:
  cases,entries,missing=readiness();print(json.dumps(dict(ready=not missing,scenario_count=len(cases),missing=missing),indent=2))
 else:
  result=run()
  if result:
   (ROOT/'cli-check.json').write_text(json.dumps(result,indent=2)+'\n');(ROOT/'cli-check-progress.json').unlink(missing_ok=True);print('PASS all',result['cli_calls'],'CLI calls',flush=True)
