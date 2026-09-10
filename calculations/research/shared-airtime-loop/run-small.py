"""Execute current small wireless inputs and exact disabled public regressions."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('airtime_network',ROOT/'calculate.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def hashes():
    paths={ROOT/'calculate.py',ROOT/'airtime.py'}
    paths.update(Path(m.__file__).resolve() for name,m in tuple(sys.modules.items()) if name.startswith('infra_calc') and getattr(m,'__file__',None) and str(m.__file__).endswith('.py'))
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}

def main():
    before=hashes()
    inputs=json.loads((ROOT/'scenarios.json').read_text())
    results={name:module.calculate(p) for name,p in inputs.items()}
    baseline=json.loads((ROOT.parent/'media-feedback-loop/result.json').read_text())
    default_checks=[]
    for name,expected in baseline.items():
        actual=module.calculate(expected['inputs'])
        assert json.dumps(actual,sort_keys=True)==json.dumps(expected,sort_keys=True),name
        default_checks.append(name)
    assert hashes()==before,'runtime sources changed'
    result_text=json.dumps(results,indent=2)+'\n'
    (ROOT/'result.json').write_text(result_text)
    (ROOT/'result-manifest.json').write_text(json.dumps(dict(status='small_candidate_not_full_acceptance',scenarios=len(results),default_complete_regressions=default_checks,code_hashes=before,result_sha256=hashlib.sha256(result_text.encode()).hexdigest(),scenarios_sha256=hashlib.sha256((ROOT/'scenarios.json').read_bytes()).hexdigest()),indent=2)+'\n')
    print('executed',len(results),'wireless/disabled scenarios;',len(default_checks),'complete default regressions')
if __name__=='__main__':main()
