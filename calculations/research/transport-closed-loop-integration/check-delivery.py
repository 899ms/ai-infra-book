"""All ten frozen payloads and twenty actual CLI invocations; no reproduction run."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import gc
import hashlib
import json
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent.parent
FILES=[PROJECT/'src/infra_calc/topics/transport_closed_loop.py',PROJECT/'src/infra_calc/topics/transport_sender.py',PROJECT/'src/infra_calc/cli.py',PROJECT/'configs/sources.lock.json',PROJECT/'scenarios/book.json']

def hashes():
    return {str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}

def math_only(r):
    return {k:v for k,v in r.items() if k not in {'reference_sources','reference_source_root'}}

def run():
    initial=hashes();started=time.monotonic()
    cases=json.loads((PROJECT/'scenarios/book.json').read_text())['transport_closed_loop']
    candidate=json.loads((ROOT.parent/'transport-closed-loop/result.json').read_text())
    assert len(cases)==len(candidate)==10
    payload_checks=[]
    for row in cases:
        name=row['id']; frozen=candidate[name.removeprefix('closed-loop-')]
        got=json.loads((PROJECT/'results'/f'{name}.json').read_text())
        assert row['inputs']==frozen['inputs']==got['inputs'],name
        assert math_only(got)==math_only(frozen),name
        payload_checks.append(name)
        del got
    del frozen,candidate
    gc.collect()
    outputs=[]
    with tempfile.TemporaryDirectory(prefix='closed-loop-cli-') as td:
        td=Path(td)
        jobs=[]
        for row in cases:
            name=row['id'];inp=td/f'{name}.input.json';inp.write_text(json.dumps(row['inputs']))
            jobs.extend((name,fmt,inp,td/f'{name}.{fmt}') for fmt in ('json','md'))
        def check(job):
            name,fmt,inp,out=job;begin=time.monotonic()
            cp=subprocess.run([sys.executable,str(PROJECT/'calc.py'),'transport-closed-loop','--inputs',str(inp),'--format',fmt,'--output',str(out)],capture_output=True,text=True)
            assert cp.returncode==0,(name,fmt,cp.stderr)
            expected=PROJECT/'results'/f'{name}.{fmt}'
            # Serialization is part of fixed deliverables: compare every byte, stronger than totals.
            actual_bytes=out.read_bytes(); expected_bytes=expected.read_bytes()
            assert actual_bytes==expected_bytes,(name,fmt,'fixed output differs')
            return dict(id=name,format=fmt,bytes=len(actual_bytes),sha256=hashlib.sha256(actual_bytes).hexdigest(),elapsed_seconds=round(time.monotonic()-begin,3))
        with ThreadPoolExecutor(max_workers=2) as pool:
            for result in pool.map(check,jobs):
                outputs.append(result)
                print(result['id'],result['format'],'PASS',flush=True)
    final=hashes();assert initial==final,'public source/config changed during delivery audit'
    return dict(status='passed',frozen_mathematical_payloads=payload_checks,cli_invocations=outputs,
        source_hashes_before=initial,source_hashes_after=final,elapsed_seconds=round(time.monotonic()-started,3),
        scope='all ten candidate/fixed payloads and all twenty actual CLI outputs; excludes general reproduce')

if __name__=='__main__':
    result=run();(ROOT/'delivery-check.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',len(result['cli_invocations']),'CLI invocations')
