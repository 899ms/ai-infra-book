#!/usr/bin/env python3
"""Actually recompute five full workloads through explicit wireless-disabled entry."""
from pathlib import Path
import copy
import gc
import hashlib
import importlib.util
import json
import sys
import time

HERE=Path(__file__).resolve().parent
CALCULATIONS=HERE.parent.parent
CANDIDATE=HERE.parent/'shared-airtime-loop'
RUNS=HERE.parent/'media-feedback-loop/runs'
NAMES=['book-image-baseline','book-mixed-fifo-immediate','book-mixed-fifo-aggregate',
       'book-mixed-priority-immediate','book-mixed-priority-aggregate']

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda:source.read(1048576),b''):h.update(chunk)
    return h.hexdigest()

spec=importlib.util.spec_from_file_location('disabled_book_review_candidate',CANDIDATE/'calculate.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def hashes():
    paths={CANDIDATE/'calculate.py',CANDIDATE/'airtime.py',Path(__file__),CALCULATIONS/'configs/sources.lock.json'}
    paths.update(Path(m.__file__).resolve() for name,m in tuple(sys.modules.items()) if name.startswith('infra_calc') and getattr(m,'__file__',None) and str(m.__file__).endswith('.py'))
    return {str(p.relative_to(CALCULATIONS)):digest(p) for p in sorted(paths)}

def canonical_hash(value):
    h=hashlib.sha256()
    for chunk in json.JSONEncoder(sort_keys=True,separators=(',',':')).iterencode(value):
        h.update(chunk.encode())
    return h.hexdigest()


def main():
    before=hashes()
    locked={name:digest(RUNS/(name+'-result.json')) for name in NAMES}
    began=time.monotonic()
    report={'status':'running','entry':'calculate(inputs with network.wireless_access={enabled:false})',
            'comparison':'entire parsed JSON equality, plus independent canonical SHA256 of actual and expected; no metadata exclusions',
            'source_hashes_before':before,'baseline_file_hashes':locked,'cases':[]}
    output=HERE/'disabled-book-result.json'
    progress=HERE/'disabled-book-progress.json'
    for name in NAMES:
        started=time.monotonic()
        progress.write_text(json.dumps({'status':'running','case':name,'completed':len(report['cases'])},indent=2)+'\n')
        expected=json.loads((RUNS/(name+'-result.json')).read_text())
        inputs=copy.deepcopy(expected['inputs'])
        assert 'wireless_access' not in inputs['network']
        inputs['network']['wireless_access']={'enabled':False}
        compute_start=time.monotonic()
        actual=module.calculate(inputs)
        compute_elapsed=time.monotonic()-compute_start
        assert actual==expected,name+' full JSON differs'
        actual_sha=canonical_hash(actual)
        expected_sha=canonical_hash(expected)
        assert actual_sha==expected_sha
        assert hashes()==before,'source changed during '+name
        assert digest(RUNS/(name+'-result.json'))==locked[name],'baseline changed during '+name
        row={'name':name,'status':'PASS','calculate_elapsed_seconds':compute_elapsed,
             'total_case_elapsed_seconds':time.monotonic()-started,
             'full_json_equal':True,'actual_canonical_sha256':actual_sha,
             'expected_canonical_sha256':expected_sha,'baseline_file_sha256':locked[name],
             'transmission_count':len(actual['transmissions']), 'summary':actual['summary']}
        report['cases'].append(row)
        output.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({'case':name,'status':'PASS','calculate_seconds':round(compute_elapsed,3),'transmissions':row['transmission_count']}),flush=True)
        del expected,actual,inputs
        gc.collect()
    report['source_hashes_after']=hashes()
    assert report['source_hashes_after']==before
    assert {name:digest(RUNS/(name+'-result.json')) for name in NAMES}==locked
    report['elapsed_seconds']=time.monotonic()-began
    report['status']='PASS'
    output.write_text(json.dumps(report,indent=2)+'\n')
    progress.unlink()
    print(f'PASS five actual full disabled recomputations; {report["elapsed_seconds"]:.3f}s',flush=True)

if __name__=='__main__':main()
