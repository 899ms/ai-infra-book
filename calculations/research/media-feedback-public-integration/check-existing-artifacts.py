"""Compare final manifested pre-existing result bytes after media integration."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent.parent
before=json.loads((ROOT/'manifest-before.json').read_text())
after=json.loads((PROJECT/'results/manifest.json').read_text())
old={r['file']:r['sha256'] for r in before['artifacts']}
new={r['file']:r['sha256'] for r in after['artifacts']}
changed=[]
for name,digest in old.items():
    assert name in new,('old result disappeared',name)
    if new[name]!=digest: changed.append(name)
assert changed==['results/README.md'],changed
added=sorted(set(new)-set(old))
assert len(added)==38 and all(name.startswith('results/media-feedback-') for name in added),added
result={'status':'passed','unchanged_existing_artifacts':len(old)-len(changed),'changed_index':changed,'added_media_artifacts':added,'before_manifest_sha256':hashlib.sha256((ROOT/'manifest-before.json').read_bytes()).hexdigest(),'after_manifest_sha256':hashlib.sha256((PROJECT/'results/manifest.json').read_bytes()).hexdigest(),'scope':'Manifest result bytes only; final verify-results separately checks files and input sources'}
(ROOT/'existing-artifacts-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['unchanged_existing_artifacts'],'existing artifacts unchanged; 38 media artifacts added')
