"""Bind pre-caption CLI evidence to byte-identical final outputs, transparently."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        while chunk:=stream.read(1048576):h.update(chunk)
    return h.hexdigest()

before=json.loads((ROOT/'before-caption-fix/results-manifest.json').read_text())
final=json.loads((PROJECT/'results/manifest.json').read_text())
a={r['file']:r['sha256'] for r in before['artifacts']}
b={r['file']:r['sha256'] for r in final['artifacts']}
assert a==b,'caption edit changed result artifacts'
cli=json.loads((ROOT/'cli-check.json').read_text())
assert cli['status']=='passed' and cli['cli_calls']==38
for check in cli['checks']:
    path=check['expected_file']
    assert b[path]==check['expected_sha256']==check['actual_sha256']
    assert digest(PROJECT/path)==b[path]
for path,h in cli['source_hashes_after'].items():
    assert digest(PROJECT/path)==h,('CLI source drift',path)
plot=PROJECT/'src/infra_calc/media_feedback_plot.py'
assert any(r['file']==str(plot.relative_to(PROJECT)) and r['sha256']==digest(plot) for r in final['inputs'])
report={'status':'passed','identical_result_artifacts':len(b),'actual_cli_outputs_preserved':38,'cli_execution_manifest_sha256':cli['results_manifest_sha256'],'final_manifest_sha256':digest(PROJECT/'results/manifest.json'),'cli_sources_still_identical':len(cli['source_hashes_after']),'scope':'CLI was executed against the first manifest. Final reproduction has byte-identical result artifacts and unchanged CLI mathematical/report sources; corrected plot source is included in the final input manifest.'}
(ROOT/'final-binding-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
