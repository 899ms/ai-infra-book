"""Recompute unchanged immediate-ACK defaults against sealed full mathematical traces."""
from pathlib import Path
import argparse
import gc
import hashlib
import importlib.util
import json
import time

ROOT = Path(__file__).resolve().parent

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

candidate = load(ROOT / 'calculate.py', 'ack_candidate')
comparison = load(ROOT.parent / 'transport-controller-loop/integration/check-network-public.py', 'parity_helpers')

def hashes():
    paths = [ROOT / 'calculate.py', ROOT / 'receiver.py']
    paths += [ROOT / x['file'] for x in json.loads((ROOT / 'dependencies.lock.json').read_text())]
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--large', action='store_true')
    args = ap.parse_args()
    before = hashes()
    results = []
    old = ROOT.parent / 'transport-closed-loop/result.json'
    baseline_results = json.loads(old.read_text())
    def legacy(name, expected):
        if (name == 'book-30mb-5mb') != args.large:
            return
        started = time.monotonic()
        actual = candidate.calculate(expected['inputs'])
        for key in comparison.EXCLUDED:
            actual.pop(key, None)
            expected.pop(key, None)
        assert actual == expected, name
        assert before == hashes(), 'source changed during run'
        results.append(dict(scenario='legacy-'+name,status='passed',elapsed_seconds=time.monotonic()-started,transmissions=len(actual['transmissions'])))
        print(name + ': passed', flush=True)
    for name, expected in baseline_results.items():
        legacy(name, expected)
    del baseline_results
    del expected
    gc.collect()
    controller = ROOT.parent / 'transport-controller-loop'
    inputs = json.loads((controller/'controller-scenarios.json').read_text())
    for name, p in inputs.items():
        if name.startswith('book-') != args.large:
            continue
        started = time.monotonic()
        actual = candidate.calculate(p)
        manifest = json.loads((controller/(name+'-manifest.json')).read_text())
        path = controller/(name+'-result.json')
        assert comparison.filehash(path) == manifest['result_sha256']
        reader = comparison.Reader(path)
        count = dict(scalars=0,list_items=0)
        comparison.compare(reader,actual,(),count)
        reader.f.close()
        assert before == hashes(), 'source changed during run'
        results.append(dict(scenario=name,status='passed',elapsed_seconds=time.monotonic()-started,compared=count,transmissions=len(actual['transmissions'])))
        print(name+': passed',flush=True)
        del actual
        gc.collect()
    assert before == hashes()
    (ROOT/('default-large-regression.json' if args.large else 'default-small-regression.json')).write_text(json.dumps(dict(status='passed',hashes=before,checks=results,source_result_sha256=comparison.filehash(old)),indent=2)+'\n')

if __name__=='__main__':
    main()
