"""Bounded public API/CLI mapping audit; never invokes full reproduce."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent.parent
sys.path.insert(0,str(PROJECT/'src'))
from infra_calc.sources import records,read_source,provenance
from infra_calc.topics import transport_closed_loop as public
spec=importlib.util.spec_from_file_location('frozen_network',ROOT.parent/'transport-closed-loop/calculate.py')
candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)


def math_only(r):
    return {k:v for k,v in r.items() if k not in {'reference_sources','reference_source_root'}}


def run():
    wanted={'RFC9000','RFC9002','RFC9002 Verified Errata7539'}
    allrows=records()
    for revision in wanted|{'RFC9221'}:
        found=[r for r in allrows if r.get('revision')==revision]
        assert len(found)==1,(revision,len(found))
        read_source(found[0]['file'])
    assert len(provenance('protocol-rfc'))==7
    tests=[]
    scenarios=candidate.scenarios()
    for name,p in scenarios.items():
        if p['upload_bytes']>=1000000: continue
        got=public.calculate(p); expected=candidate.calculate(p)
        assert math_only(got)==math_only(expected),name
        assert {r['revision'] for r in got['reference_sources']}==wanted
        for row in got['reference_sources']: read_source(row['file'])
        tests.append(name)
    default=public.calculate()
    assert math_only(default)==math_only(candidate.calculate(candidate.example()))
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); inp=td/'input.json';out=td/'result.json';md=td/'result.md'
        p=candidate.example();p.update(receive_window=2336,upload_bytes=3504,response_bytes=0,model_seconds=0,
            explicit_consumption=[dict(at=4,direction='up',upto=2336)])
        inp.write_text(json.dumps(p))
        for fmt,path in [('json',out),('md',md)]:
            completed=subprocess.run([sys.executable,str(PROJECT/'calc.py'),'transport-closed-loop','--inputs',str(inp),'--format',fmt,'--output',str(path)],capture_output=True,text=True,check=True)
            assert path.exists() and path.stat().st_size>0
        assert json.loads(out.read_text())==public.calculate(p)
        assert 'transport' in md.read_text().lower() or '闭环' in md.read_text()
    return dict(status='passed',small_scenarios=tests,default_api=True,cli_json_exact_public_match=True,cli_markdown=True,
        scope='source mapping and bounded public API/CLI equivalence; original independent physics review remains separate',
        files={str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [PROJECT/'src/infra_calc/topics/transport_closed_loop.py',PROJECT/'src/infra_calc/topics/transport_sender.py',PROJECT/'src/infra_calc/cli.py']})

if __name__=='__main__':
    result=run();(ROOT/'public-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
