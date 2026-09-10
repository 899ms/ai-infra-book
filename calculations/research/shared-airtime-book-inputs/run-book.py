"""Validate by default; --run explicitly executes one full sealed wireless case."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import time
ROOT=Path(__file__).resolve().parent
CALC=ROOT.parent.parent
LOOP=ROOT.parent/'shared-airtime-loop'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while block:=f.read(1048576):h.update(block)
    return h.hexdigest()
def write(p,data):p.write_text(json.dumps(data,indent=2)+'\n')
def verify():
    identity={}
    for lock in ('inputs.lock.json','sources.lock.json','runtime.lock.json'):
        path=ROOT/lock;identity[lock]=sha(path)
        for row in json.loads(path.read_text()):
            p=ROOT/row['file'];actual=sha(p)
            if p.stat().st_size!=row['bytes'] or actual!=row['sha256']:raise ValueError('sealed identity changed: '+row['file'])
            identity[row['file']]=actual
    expected={str((ROOT/r['file']).resolve()) for r in json.loads((ROOT/'runtime.lock.json').read_text()) if r['file'].endswith('.py')}
    actual={str(p.resolve()) for p in (CALC/'src/infra_calc').rglob('*.py')}
    if not actual<=expected:raise ValueError('new public Python dependency requires explicit reseal')
    return identity
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--case');parser.add_argument('--run',action='store_true');parser.add_argument('--ready',action='store_true');args=parser.parse_args()
    before=verify();cases=json.loads((ROOT/'book-inputs.json').read_text())
    if not args.run:
        print(json.dumps(dict(status='READY_NOT_EXECUTED',cases=list(cases),locked_files=len(before))));return
    if args.case not in cases:parser.error('--run requires one valid --case: '+', '.join(cases))
    folder=ROOT/'runs';folder.mkdir(exist_ok=True);stem=args.case
    manifestpath=folder/(stem+'-manifest.json')
    if manifestpath.exists():raise ValueError('run already exists; archive explicitly before rerun')
    effective=folder/(stem+'-inputs.json');write(effective,cases[stem]);started=time.monotonic()
    manifest=dict(status='RUNNING',case=stem,full_workload=True,inputs_sha256=sha(effective),source_hashes_before=before)
    write(manifestpath,manifest)
    partial=folder/(stem+'-result.partial.json')
    try:
        spec=importlib.util.spec_from_file_location('shared_airtime_book_run',LOOP/'calculate.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        result=module.calculate(cases[stem])
        with partial.open('w') as f:json.dump(result,f,indent=2);f.write('\n')
        after=verify();manifest['source_hashes_after']=after
        if after!=before:raise ValueError('runtime/input hash drift')
        target=folder/(stem+'-result.json');partial.replace(target)
        summary={k:result.get(k) for k in ('summary','businesses','wireless_summary')}
        summary.update(case=stem,transmission_count=len(result.get('transmissions',[])),result_sha256=sha(target))
        summarypath=folder/(stem+'-summary.json');write(summarypath,summary)
        manifest.update(status='COMPLETE_STABLE_IDENTITY_NOT_INDEPENDENT_ACCEPTANCE',result_file=target.name,result_sha256=sha(target),result_bytes=target.stat().st_size,summary_file=summarypath.name,summary_sha256=sha(summarypath))
    except Exception as error:
        manifest.update(status='FAILED_NOT_ACCEPTED',error=type(error).__name__+': '+str(error))
        try:manifest['source_hashes_after']=verify()
        except Exception as drift:manifest['source_recheck_error']=str(drift)
        raise
    finally:
        manifest['elapsed_seconds']=round(time.monotonic()-started,6);write(manifestpath,manifest)
    print(json.dumps(dict(status=manifest['status'],case=stem,elapsed_seconds=manifest['elapsed_seconds'],manifest=str(manifestpath))))
if __name__=='__main__':main()
