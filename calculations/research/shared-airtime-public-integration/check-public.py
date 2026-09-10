"""Actual public calculate, 24 new full-payload comparisons and 19 old regressions."""
import argparse
import ast
import gc
import hashlib
import json
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parent
CALC=ROOT.parent.parent
sys.path.insert(0,str(CALC/'src'))
from infra_calc.topics import transport_closed_loop
STRIP=('wireless_reference_sources','wireless_reference_root')
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
def canonical(value):
 h=hashlib.sha256()
 for s in json.JSONEncoder(sort_keys=True,separators=(',',':')).iterencode(value):h.update(s.encode())
 return h.hexdigest()
def read(path):return json.loads(path.read_text())
def identity():
 paths=set((CALC/'src/infra_calc').rglob('*.py'))|{CALC/'configs/sources.lock.json',CALC/'configs/shared-airtime-provenance.json',CALC/'scenarios/shared-airtime-profiles.json',CALC/'scenarios/shared-airtime-example.json',CALC/'scenarios/book.json'}
 tree=ast.parse((CALC/'src/infra_calc/transport/reference_sources.py').read_text())
 for node in tree.body:
  if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SOURCE_FILES' for t in node.targets):
   for files in ast.literal_eval(node.value).values():paths.update(CALC/f for f in files)
 return {str(p.relative_to(CALC)):sha(p) for p in sorted(paths)}
def plan():
 book={r['id']:r['inputs'] for r in read(CALC/'scenarios/book.json')['transport_closed_loop']}
 provenance=read(CALC/'configs/shared-airtime-provenance.json');out=[]
 for m in provenance['mapping']:
  c=m['research_key'];category=m['category']
  path=CALC/('research/shared-airtime-loop/result.json' if category=='small' else f'research/shared-airtime-book-inputs/runs/{c}-result.json' if category=='full' else f'research/shared-airtime-scan-inputs/runs/{c}-result.json')
  inputs=book[m['public_id']];assert canonical(inputs)==m['canonical_input_sha256']
  out.append(dict(id=m['public_id'],category='new-'+category,path=path,key=c if category=='small' else None,inputs=inputs))
 old=read(CALC/'research/media-feedback-loop/result.json')
 for c,r in old.items():
  identity='media-feedback-'+c;assert book[identity]==r['inputs']
  out.append(dict(id=identity,category='old-small',path=CALC/'research/media-feedback-loop/result.json',key=c,inputs=book[identity]))
 for c in ('image-baseline','mixed-fifo-immediate','mixed-fifo-aggregate','mixed-priority-immediate','mixed-priority-aggregate'):
  identity='media-feedback-'+c
  out.append(dict(id=identity,category='old-full',path=CALC/f'research/media-feedback-loop/runs/book-{c}-result.json',key=None,inputs=book[identity]))
 assert len(out)==43 and sum(x['category'].startswith('old') for x in out)==19
 return out
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run',action='store_true');args=parser.parse_args()
 cases=plan();before=identity();expected_hashes={str(c['path'].relative_to(CALC)):sha(c['path']) for c in cases}
 if not args.run:
  print(json.dumps(dict(status='READY_NO_CALCULATE',cases=len(cases),public_files=len(before),research_results=len(expected_hashes))));return
 report=dict(status='RUNNING',allowed_top_level_removals=list(STRIP),public_before=before,expected_result_files=expected_hashes,cases=[])
 def save(): (ROOT/'public-check.json').write_text(json.dumps(report,indent=2)+'\n')
 save();start=time.monotonic()
 try:
  for index,c in enumerate(cases,1):
   assert identity()==before,'public identity drift before case'
   began=time.monotonic();print(f"START {index}/43 {c['id']}",flush=True)
   actual=transport_closed_loop.calculate(c['inputs'])
   expected=read(c['path']);expected=expected[c['key']] if c['key'] else expected
   assert actual['inputs']==expected['inputs'],c['id']+' inputs changed'
   for field in STRIP:actual.pop(field,None);expected.pop(field,None)
   assert actual==expected,c['id']+' full mathematical payload mismatch'
   mathhash=canonical(actual)
   assert identity()==before,'public identity drift after case'
   assert sha(c['path'])==expected_hashes[str(c['path'].relative_to(CALC))],'research expected drift'
   report['cases'].append(dict(id=c['id'],category=c['category'],status='FULL_PAYLOAD_EQUAL',input_sha256=canonical(c['inputs']),expected_file=str(c['path'].relative_to(CALC)),expected_key=c['key'],mathematical_payload_sha256=mathhash,elapsed_seconds=round(time.monotonic()-began,6)))
   save();print(f"PASS {index}/43 {c['id']} {report['cases'][-1]['elapsed_seconds']}s",flush=True)
   del actual,expected;gc.collect()
  report.update(status='PASS_24_NEW_19_OLD_FULL_PUBLIC_CALCULATE',public_after=identity())
 except Exception as e:
  report.update(status='FAILED',error=type(e).__name__+': '+str(e),public_after=identity());raise
 finally:
  report['elapsed_seconds']=round(time.monotonic()-start,6);save()
if __name__=='__main__':main()
