"""Regenerate just this release's registered scenarios, without unrelated experiments."""
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from infra_calc.topics import v41_flash, kv_comparison
from infra_calc.sources import read_source


def main():
    scenarios=json.loads((ROOT/'scenarios/book.json').read_text())
    artifacts=[]
    for group,module in (('v41_flash',v41_flash),('kv_comparison',kv_comparison)):
        for row in scenarios[group]:
            result=module.calculate(**row['inputs'])
            for ext,data in (('json',json.dumps(result,ensure_ascii=False,indent=2)+'\n'),('md',module.markdown(result))):
                path=ROOT/'results'/f"{row['id']}.{ext}"
                path.write_text(data)
                artifacts.append(dict(file=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    report=dict(scenario_groups=['v41_flash','kv_comparison'],scenario_count=sum(len(scenarios[g]) for g in ('v41_flash','kv_comparison')),artifacts=artifacts,
                scope='Targeted regeneration only; global results/manifest.json is not refreshed. Both groups also run through calc.py reproduce.')
    (Path(__file__).parent/'reproduction.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(scenarios=report['scenario_count'],artifacts=len(artifacts))))

if __name__=='__main__':main()
