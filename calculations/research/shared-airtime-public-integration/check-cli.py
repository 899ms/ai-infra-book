"""Prepare/readiness by default; --run makes 48 real CLI computations after reproduce."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parent
CALC=ROOT.parent.parent
MANIFEST=CALC/'results/manifest.json'
sys.path.insert(0,str(CALC/'src'))


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
    return h.hexdigest()


def canonical(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def source_hashes():
    paths=list((CALC/'src/infra_calc').rglob('*.py'))
    paths += [CALC/'calc.py',CALC/'configs/sources.lock.json',CALC/'configs/shared-airtime-provenance.json',CALC/'scenarios/book.json']
    paths += list((CALC/'scenarios').glob('shared-airtime-*.json'))
    prefixes=('sources/shared-airtime/','sources/shared-media-rfc/','sources/protocol-rfc/','sources/congestion-controllers/','sources/connection-window/')
    rows=json.loads((CALC/'configs/sources.lock.json').read_text())['sources']
    paths += [CALC/r['file'] for r in rows if r['file'].startswith(prefixes)]
    return {str(p.relative_to(CALC)):digest(p) for p in sorted(set(paths))}


def readiness():
    # This calls only the source-inventory reader, never reproduce/run/calculate.
    from infra_calc.reproduce import input_hashes
    if not MANIFEST.exists():raise ValueError('official results manifest is missing; wait for reproduce')
    manifest=json.loads(MANIFEST.read_text())
    if manifest.get('inputs')!=input_hashes():
        raise ValueError('official result manifest is stale against current inputs; wait for a completed reproduce')
    cases=[r for r in json.loads((CALC/'scenarios/book.json').read_text())['transport_closed_loop'] if r['id'].startswith('shared-airtime-')]
    mapping=json.loads((CALC/'configs/shared-airtime-provenance.json').read_text())['mapping']
    assert len(cases)==24 and len({r['id'] for r in cases})==24
    assert {r['id'] for r in cases}=={r['public_id'] for r in mapping}
    # Map file uses the same canonical representation (UTF-8 ASCII JSON keys).
    for case in cases:
        expected=next(r for r in mapping if r['public_id']==case['id'])
        assert canonical(case['inputs'])==expected['canonical_input_sha256'],case['id']
    artifacts=manifest['artifacts'];entries={r['file']:r['sha256'] for r in artifacts}
    assert len(entries)==len(artifacts),'duplicate official artifact paths'
    required={f"results/{case['id']}.{fmt}" for case in cases for fmt in ('json','md')}
    assert {name for name in entries if name.startswith('results/shared-airtime-')}==required,'unexpected or missing wireless artifacts'
    for name in required:
        if not (CALC/name).is_file() or digest(CALC/name)!=entries[name]:
            raise ValueError('official artifact is missing or differs from manifest: '+name)
    return cases,entries,manifest


def compare(left,right):
    hashes=[hashlib.sha256(),hashlib.sha256()];counts=[0,0];equal=True
    with left.open('rb') as a,right.open('rb') as b:
        while True:
            chunks=(a.read(1048576),b.read(1048576))
            if not any(chunks):break
            for i,chunk in enumerate(chunks):hashes[i].update(chunk);counts[i]+=len(chunk)
            equal &= chunks[0]==chunks[1]
    return dict(expected_sha256=hashes[0].hexdigest(),actual_sha256=hashes[1].hexdigest(),expected_bytes=counts[0],actual_bytes=counts[1],bytewise_equal=equal)


def save(path,value):
    tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,indent=2)+'\n');tmp.replace(path)


def run():
    cases,entries,official=readiness()
    manifest_hash=digest(MANIFEST);before=source_hashes();checks=[];started=time.monotonic()
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    folder=ROOT/'cli-runs'/stamp;folder.mkdir(parents=True)
    state=dict(status='running',started_utc=stamp,expected_calls=48,completed_calls=0,checks=checks,
        results_manifest_sha256=manifest_hash,source_hashes_before=before,checker_sha256=digest(Path(__file__)))
    save(folder/'progress.json',state)
    try:
        for case in cases:
            for fmt in ('json','md'):
                assert source_hashes()==before and digest(MANIFEST)==manifest_hash,'source or formal manifest changed before call'
                relative=f"results/{case['id']}.{fmt}";expected=CALC/relative
                assert digest(expected)==entries[relative],'official artifact changed before call'
                tick=time.monotonic()
                with tempfile.TemporaryDirectory(prefix='shared-airtime-cli-') as td:
                    td=Path(td);inp=td/'exact-input.json';out=td/f'actual.{fmt}'
                    inp.write_text(json.dumps(case['inputs'],ensure_ascii=False,indent=2)+'\n')
                    assert json.loads(inp.read_text())==case['inputs']
                    command=[sys.executable,str(CALC/'calc.py'),'transport-closed-loop','--inputs',str(inp),'--format',fmt,'--output',str(out)]
                    executed=subprocess.run(command,capture_output=True,text=True)
                    if executed.returncode:
                        save(folder/'failed-command.json',dict(id=case['id'],format=fmt,returncode=executed.returncode,stderr=executed.stderr,stdout=executed.stdout))
                        raise RuntimeError(f"CLI failed: {case['id']} {fmt}")
                    compared=compare(expected,out)
                    record=dict(id=case['id'],format=fmt,canonical_input_sha256=canonical(case['inputs']),temporary_input_sha256=digest(inp),
                        command=['<python>','calc.py','transport-closed-loop','--inputs','<exact temporary input>','--format',fmt,'--output','<temporary output>'],
                        expected_file=relative,manifest_expected_sha256=entries[relative],**compared,elapsed_seconds=time.monotonic()-tick)
                    checks.append(record)
                    assert compared['expected_sha256']==entries[relative] and compared['bytewise_equal'],f"CLI bytes differ: {relative}"
                    assert source_hashes()==before and digest(MANIFEST)==manifest_hash,'source or formal manifest changed during call'
                state['completed_calls']=len(checks);state['elapsed_seconds']=time.monotonic()-started
                save(folder/'progress.json',state)
                print(case['id'],fmt,'PASS',flush=True)
        # Re-evaluate the entire formal input inventory and all48 artifacts, not
        # merely the relevant runtime subset, before claiming completion.
        after_cases,after_entries,after_manifest=readiness()
        assert after_cases==cases and after_entries==entries and after_manifest==official
        assert source_hashes()==before and digest(MANIFEST)==manifest_hash
        state.update(status='passed',completed_calls=48,source_hashes_after=before,elapsed_seconds=time.monotonic()-started,
            scope='48 actual subprocess recalculations and full byte comparisons; no copied output or reproduce invocation')
        save(folder/'check.json',state);save(ROOT/'cli-check.json',state)
        print('PASS48 actual calls; evidence',folder,flush=True)
    except BaseException as error:
        state.update(status='failed',completed_calls=sum(r.get('bytewise_equal',False) for r in checks),failure=repr(error),elapsed_seconds=time.monotonic()-started)
        save(folder/'failure.json',state)
        raise


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    choice=parser.add_mutually_exclusive_group();choice.add_argument('--run',action='store_true');choice.add_argument('--ready',action='store_true')
    args=parser.parse_args()
    if args.run:run()
    else:
        try:
            cases,_,_=readiness();print(json.dumps(dict(ready=True,cases=len(cases),actual_cli_calls_planned=48,execution='not started; explicit --run required'),indent=2))
        except (ValueError,AssertionError,FileNotFoundError) as error:
            print(json.dumps(dict(ready=False,reason=str(error),execution='not started'),indent=2))
            raise SystemExit(2)
if __name__=='__main__':main()
