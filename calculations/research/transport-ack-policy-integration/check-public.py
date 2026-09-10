"""Actual public ACK-policy recomputation and complete mathematical migration parity."""
from pathlib import Path
import importlib.util
import gc
import json
import sys
import time

ROOT = Path(__file__).resolve().parent
RESEARCH = ROOT.parent / 'transport-ack-policy'
CONTROLLERS = ROOT.parent / 'transport-controller-loop'
PROJECT = ROOT.parents[2]
sys.path.insert(0, str(PROJECT/'calculations/src'))
from infra_calc.topics.transport_closed_loop import calculate
spec = importlib.util.spec_from_file_location('migration_compare',CONTROLLERS/'integration/check-network-public.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def hashes():
    files = list((PROJECT/'calculations/src/infra_calc/transport').glob('*.py'))
    files += [PROJECT/'calculations/src/infra_calc/topics'/name for name in ('transport_closed_loop.py','transport_sender.py')]
    files += [RESEARCH/name for name in ('calculate.py','receiver.py')]
    for name in ('congestion-controllers','hystart-plus-plus','transport-controller-loop'):
        files += [f for f in (ROOT.parent/name).glob('*.py') if not f.name.startswith(('check','plot','run','root'))]
    return {str(p.relative_to(PROJECT)):helper.filehash(p) for p in sorted(set(files))}


def main():
    before=hashes()
    checks=[]
    def record(name, actual, elapsed, count, expected_file):
        assert before==hashes(), 'source changed during execution'
        checks.append(dict(scenario=name,status='passed',elapsed_seconds=elapsed,compared=count,transmissions=len(actual['transmissions']),business=actual['business'],reference_result_file=str(expected_file.relative_to(PROJECT)),reference_result_sha256=helper.filehash(expected_file)))
        print(name+': complete payload passed',flush=True)
    small_file=RESEARCH/'result.json'
    manifest=json.loads((RESEARCH/'result-manifest.json').read_text())
    assert helper.filehash(small_file)==manifest['result_sha256']
    for filename,digest in manifest['code_hashes'].items():assert helper.filehash(RESEARCH/filename)==digest
    small=json.loads(small_file.read_text())
    for name,expected in small.items():
        started=time.monotonic()
        actual=calculate(expected['inputs'])
        for key in helper.EXCLUDED:
            actual.pop(key)
            expected.pop(key)
        assert actual==expected,name
        assert json.dumps(actual,sort_keys=True)==json.dumps(expected,sort_keys=True),('scalar-type mismatch',name)
        record('ack-'+name,actual,time.monotonic()-started,dict(mode='full typed object equality'),small_file)
        del actual
    del small
    gc.collect()
    for name in ('newreno','cubic_hystart','bbr'):
        manifest=json.loads((RESEARCH/f'book-aggregate-{name}-manifest.json').read_text())
        path=RESEARCH/manifest['result_file']
        assert helper.filehash(path)==manifest['result_sha256']
        for filename,digest in manifest['code_hashes'].items():assert helper.filehash(Path(filename))==digest
        started=time.monotonic()
        actual=calculate(manifest['inputs'])
        reader=helper.Reader(path);count=dict(scalars=0,list_items=0)
        helper.compare(reader,actual,(),count);reader.white();assert reader.eof;reader.f.close()
        assert helper.filehash(path)==manifest['result_sha256']
        record('ack-book-'+name,actual,time.monotonic()-started,count,path)
        del actual
        gc.collect()
    # Default small compatibility: actual public execution, separate from new ACK cases.
    path=ROOT.parent/'transport-closed-loop/result.json'
    baseline=json.loads(path.read_text())
    for name,expected in baseline.items():
        if name=='book-30mb-5mb':continue
        started=time.monotonic();actual=calculate(expected['inputs'])
        for key in helper.EXCLUDED:actual.pop(key);expected.pop(key)
        assert actual==expected,name
        record('default-'+name,actual,time.monotonic()-started,dict(mode='full object equality'),path)
    del baseline,expected,actual
    gc.collect()
    for name in ('newreno','cubic_hystart','bbr'):
        path=CONTROLLERS/f'router-{name}-result.json'
        expected=json.loads(path.read_text());started=time.monotonic();actual=calculate(expected['inputs'])
        for key in helper.EXCLUDED:actual.pop(key);expected.pop(key)
        assert actual==expected,name
        record('default-router-'+name,actual,time.monotonic()-started,dict(mode='full object equality'),path)
        del actual,expected
        gc.collect()
    assert before==hashes()
    (ROOT/'public-check.json').write_text(json.dumps(dict(status='passed',new_ack_cases=10,default_public_small_cases=12,excluded_fields=sorted(helper.EXCLUDED),checks=checks,code_hashes=before,checker_sha256=helper.filehash(Path(__file__))),indent=2)+'\n')


if __name__=='__main__':main()
