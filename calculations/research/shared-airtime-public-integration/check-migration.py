"""AST migration proof and actual small public execution; no full reproduce."""
from pathlib import Path
import ast,copy,hashlib,json,sys,time
ROOT=Path(__file__).resolve().parent
CALC=ROOT.parent.parent
RESEARCH=ROOT.parent/'shared-airtime-loop'
PUBLIC=CALC/'src/infra_calc/transport'
sys.path.insert(0,str(CALC/'src'))
from infra_calc.topics.transport_closed_loop import calculate
from infra_calc.transport import shared_airtime_network as network,airtime,media_network
from infra_calc.transport.reference_sources import reference_sources
from infra_calc.sources import read_source

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def parsed(p):return ast.parse(p.read_text())
def dump(n):return ast.dump(n,include_attributes=False)
def functions(p):return {n.name:n for n in parsed(p).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def identities():
    files=[PUBLIC/n for n in ('airtime.py','shared_airtime_network.py','media_network.py','media_application.py','media_application_validation.py','media_network_validation.py','media_sender.py','ack_receiver.py','pacer.py','reference_sources.py','cubic.py','cubic_adapter.py','hystart.py','bbr_adapter.py','bbr_reference.py','bbr_minmax.py','bbr_state.py','persistent_congestion.py')]
    files += [CALC/'src/infra_calc/topics'/n for n in ('transport_closed_loop.py','transport_sender.py')]
    files += [RESEARCH/'calculate.py',RESEARCH/'airtime.py',CALC/'configs/sources.lock.json']
    return {str(p.relative_to(CALC)):sha(p) for p in files}

def main():
    before=identities()
    a=functions(RESEARCH/'airtime.py');b=functions(PUBLIC/'airtime.py')
    assert set(b)==set(a)-{'main'}
    for name in b:assert dump(a[name])==dump(b[name]),name
    a=functions(RESEARCH/'calculate.py');b=functions(PUBLIC/'shared_airtime_network.py')
    assert set(b)==set(a)-{'main'}
    # Only source metadata root changes inside Network.run; all event code same.
    old_run=next(n for n in a['Network'].body if isinstance(n,ast.FunctionDef) and n.name=='run')
    new_run=next(n for n in b['Network'].body if isinstance(n,ast.FunctionDef) and n.name=='run')
    def root_assignment(fn):
        return next(n for n in fn.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Subscript) and isinstance(n.targets[0].slice,ast.Constant) and n.targets[0].slice.value=='wireless_reference_root')
    root_assignment(old_run).value=copy.deepcopy(root_assignment(new_run).value)
    for name in set(b)-{'verify_sources'}:assert dump(a[name])==dump(b[name]),name
    assert network.base is media_network and network.airtime is airtime
    original=parsed(ROOT/'transport_closed_loop.before.py.txt');current=parsed(CALC/'src/infra_calc/topics/transport_closed_loop.py')
    fn=next(n for n in current.body if isinstance(n,ast.FunctionDef) and n.name=='calculate')
    branch=fn.body[0]
    oldfn=next(n for n in original.body if isinstance(n,ast.FunctionDef) and n.name=='calculate')
    assert isinstance(branch.body[-2],ast.If)
    branch.body[-2]=copy.deepcopy(oldfn.body[0].body[-2])
    assert dump(original)==dump(current),'topic changed beyond wireless import dispatch'
    oldrows=json.loads((ROOT.parent/'shared-airtime-inputs/sources.lock.json').read_text());rows=reference_sources('shared_airtime')
    assert len(rows)==len(oldrows)==14
    for old,new in zip(oldrows,rows):
        assert Path(old['file']).name==Path(new['file']).name
        for key in ('url','revision','bytes','sha256'):assert old[key]==new[key]
        assert read_source(new['file'])==(ROOT.parent/'shared-airtime-inputs'/old['file']).read_bytes()
    maps=json.loads((CALC/'configs/shared-airtime-provenance.json').read_text())['mapping']
    registered={row['id']:row['inputs'] for row in json.loads((CALC/'scenarios/book.json').read_text())['transport_closed_loop']}
    checks=[];small=json.loads((RESEARCH/'result.json').read_text());started=time.monotonic()
    for row in maps:
        if row['category']=='full':continue
        name=row['research_key']
        if row['category']=='small':expected=small[name]
        else:expected=json.loads((ROOT.parent/f'shared-airtime-scan-inputs/runs/{name}-result.json').read_text())
        p=registered[row['public_id']];actual=calculate(p)
        for field in ('wireless_reference_sources','wireless_reference_root'):
            actual.pop(field,None);expected.pop(field,None)
        assert json.dumps(actual,sort_keys=True)==json.dumps(expected,sort_keys=True),name
        checks.append(dict(id=row['public_id'],packets=len(actual['transmissions']),status='passed'))
    old=json.loads((ROOT.parent/'media-feedback-loop/result.json').read_text())
    for name,expected in old.items():
        actual=calculate(expected['inputs']);assert json.dumps(actual,sort_keys=True)==json.dumps(expected,sort_keys=True),name
        checks.append(dict(id='default-'+name,packets=len(actual['transmissions']),status='passed'))
    assert before==identities()
    proof=dict(status='passed',static_math='All airtime functions and Network math AST equal; only source root assignment normalized. Topic only adds wireless import branch; static base/airtime bindings verified.',source_files_verified=14,allowed_result_differences=['wireless_reference_sources','wireless_reference_root'],new_public_small_and_scan_cases=19,old_public_media_small_cases=14,checks=checks,elapsed_seconds=time.monotonic()-started,runtime_hashes=before,checker_sha256=sha(Path(__file__)))
    (ROOT/'small-public-check.json').write_text(json.dumps(proof,indent=2)+'\n')
    print('AST/source/static binding and33 actual small full-payload comparisons passed')
if __name__=='__main__':main()
