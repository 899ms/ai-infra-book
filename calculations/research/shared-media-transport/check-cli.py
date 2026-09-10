"""Run real CLI calls and compare complete frozen research results."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    root=Path(__file__).resolve().parent
    before=hashlib.sha256((root/'calculate.py').read_bytes()).hexdigest()
    frozen=json.loads((root/'result.json').read_text())
    scenarios=json.loads((root/'scenarios.json').read_text())
    assert set(scenarios)==set(frozen)
    with tempfile.TemporaryDirectory() as directory:
        output=Path(directory)/'result.json'
        inputs=Path(directory)/'inputs.json'
        subprocess.run([sys.executable,str(root/'calculate.py'),'--output',str(output)],check=True)
        assert json.loads(output.read_text())==frozen
        checked=[]
        for name in ('hol-per_stream','mixed-priority','screenshot-complete'):
            inputs.write_text(json.dumps(scenarios[name]))
            subprocess.run([sys.executable,str(root/'calculate.py'),'--inputs',str(inputs),
                            '--output',str(output)],check=True)
            assert json.loads(output.read_text())==frozen[name]
            checked.append(name)
    assert before==hashlib.sha256((root/'calculate.py').read_bytes()).hexdigest()
    result=dict(status='passed',candidate_sha256=before,default_cli_full_results=len(frozen),
                editable_input_cli_matches=checked,result_sha256=hashlib.sha256((root/'result.json').read_bytes()).hexdigest())
    (root/'cli-check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':
    main()
