"""Actually recompute six public networks and stream-compare every mathematical field."""
from pathlib import Path
import gc
import hashlib
import importlib.util
import json
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
PROJECT = ROOT.parents[2]
sys.path.insert(0, str(PROJECT / 'calculations/src'))
from infra_calc.topics.transport_closed_loop import calculate

spec = importlib.util.spec_from_file_location('large_reader', ROOT / 'check-large-independent.py')
reader_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader_module)
Reader = reader_module.Reader
filehash = reader_module.filehash
EXCLUDED = {'reference_sources', 'reference_source_root'}


def hashes():
    files = list((PROJECT / 'calculations/src/infra_calc/transport').glob('*.py'))
    files += [PROJECT / 'calculations/src/infra_calc/topics' / f for f in ('transport_closed_loop.py', 'transport_sender.py')]
    manifest = json.loads((ROOT / 'book-bbr-manifest.json').read_text())
    files += [ROOT / f for f in manifest['code_hashes']]
    for folder in ('congestion-controllers', 'hystart-plus-plus'):
        files += list((ROOT.parent / folder).glob('*.py'))
    return {str(p.relative_to(PROJECT)): filehash(p) for p in sorted(set(files))}


def compare(reader, actual, path, count):
    if isinstance(actual, dict):
        found = set()
        def child(key):
            assert key not in found, ('duplicate key', path, key)
            found.add(key)
            assert key in actual, ('missing public field', path, key)
            if not path and key in EXCLUDED:
                reader.value()
            else:
                compare(reader, actual[key], path + (key,), count)
        reader.object(child)
        assert found == set(actual), ('different object keys', path, found ^ set(actual))
    elif isinstance(actual, list):
        index = 0
        def item(value):
            nonlocal index
            assert index < len(actual), ('long expected list', path)
            assert value == actual[index], ('list item mismatch', path, index)
            # Dict/list values must also retain scalar types (bool != integer).
            assert json.dumps(value, sort_keys=True, separators=(',', ':')) == json.dumps(actual[index], sort_keys=True, separators=(',', ':')), ('typed item mismatch', path, index)
            index += 1
        reader.array(item)
        assert index == len(actual), ('short expected list', path, index, len(actual))
        count['list_items'] += index
    else:
        value = reader.value()
        assert type(value) is type(actual) and value == actual, ('scalar mismatch', path, value, actual)
        count['scalars'] += 1


def main():
    inputs = json.loads((ROOT / 'controller-scenarios.json').read_text())
    before = hashes()
    checks = []
    output = ROOT / 'integration/network-public-check.json'
    for name, p in inputs.items():
        start = time.monotonic()
        result_file = ROOT / (name + '-result.json')
        manifest = json.loads((ROOT / (name + '-manifest.json')).read_text())
        assert filehash(result_file) == manifest['result_sha256']
        for f, digest in manifest['code_hashes'].items():
            assert filehash(ROOT / f) == digest
        actual = calculate(p)
        count = {'scalars': 0, 'list_items': 0}
        reader = Reader(result_file)
        compare(reader, actual, (), count)
        reader.white()
        assert reader.eof, 'unparsed trailing data'
        reader.f.close()
        assert before == hashes(), 'code changed during calculation/comparison'
        assert filehash(result_file) == manifest['result_sha256'], 'research result changed'
        checks.append(dict(scenario=name, status='passed', elapsed_seconds=time.monotonic()-start, compared=count, result_sha256=manifest['result_sha256'], transmissions=len(actual['transmissions']), business=actual['business'], summary=actual['summary']))
        print(name + ': full mathematical payload passed', flush=True)
        del actual
        gc.collect()
        output.write_text(json.dumps(dict(status='running', excluded_top_level_fields=sorted(EXCLUDED), checks=checks, code_hashes=before), indent=2)+'\n')
    assert hashes() == before
    output.write_text(json.dumps(dict(status='passed', excluded_top_level_fields=sorted(EXCLUDED), checks=checks, code_hashes=before, checker_sha256=filehash(Path(__file__))), indent=2)+'\n')


if __name__ == '__main__':
    main()
