#!/usr/bin/env python3
"""Reproduce 8K/200K single-token decode with the chapter's pinned model paths."""
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'calculations/src'))
from infra_calc.models import forward
from infra_calc.schema import Scenario
from infra_calc.topics import k3_forward, qwen36_forward, state, v4_forward


def calculate():
    rows = []
    sources = {}
    for history in (8192, 204800):
        q = forward('qwen3-8b', Scenario(batch=1, tokens=1, history=8192, output_head='last'))
        # Qwen3-8B's pinned unscaled context limit is below 200K.
        # Extrapolate only its operator formula; do not claim a runnable configuration.
        delta = history - 8192
        q['summary']['matrix_flops'] += 36*4*32*128*delta
        q['summary']['kv_resident_before_bytes'] += 147456*delta
        q36 = qwen36_forward.calculate(batch=1, tokens=1, history=history, output_head='last')
        v = v4_forward.calculate('deepseek-v4-flash', batch=1, tokens=1, history=history)
        k = k3_forward.calculate(batch=1, tokens=1, history=history, mla_path='compact', kda_algorithm='recurrent', output_head='last')
        va = v['components']['attention']['summary']
        interaction = [36*4*32*128*(history+1), 10*4*16*256*(history+1),
                       va['effective_qk_pv_matrix_flops'] + va['reference_index_matrix_flops'],
                       24*2*96*(576+512)*(history+1)]
        # Independent check of V4's window, selected CSA, HCA and index scan.
        n = history+1
        expected_v4 = 4*64*512*(43*128+21*min(n//4,512)+20*(n//128)) + 2*64*128*21*(n//4)
        assert interaction[2] == expected_v4
        sizes = [q['summary']['kv_resident_before_bytes'],
                 20*1024*history + int(61.875*2**20),
                 state.calculate('deepseek-v4-flash', history)['summary']['resident_bytes'],
                 state.calculate('kimi-k3', history, mla_path='compact')['summary']['resident_bytes']]
        for i, (name, result) in enumerate(zip(['Qwen3-8B','Qwen3.6','V4-Flash','K3（紧凑 MLA）'], [q,q36,v,k])):
            total = result['summary'].get('matrix_flops', result['summary'].get('matrix_flops_effective_attention'))
            rows.append(dict(model=name, history=history, matrix_flops=total,
                             history_interaction_flops=interaction[i], other_matrix_flops=total-interaction[i],
                             state_bytes=sizes[i]))
            sources[name] = result['sources']
    anchors = json.loads((HERE/'model-comparison.json').read_text())['models']
    for short, long, anchor in zip(rows[:4], rows[4:], anchors):
        assert short['matrix_flops'] == anchor['decode_matrix_flops']
        assert short['state_bytes'] == anchor['state_8192_bytes']
        assert short['other_matrix_flops'] == long['other_matrix_flops']
    code = sorted((ROOT/'calculations/src/infra_calc').rglob('*.py'))
    return dict(qwen3_200k_scope='Analytical extrapolation beyond pinned unscaled context limit; not a supported execution or quality claim', scope='B=1, P=1, S=8192 or 204800 (K=1024); last-position head; effective matrix FLOPs, not latency; no context-quality claim',
                models=rows, sources=sources,
                calculator_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in code},
                checks=['8K totals and states equal existing table', 'non-history matrix work unchanged', 'V4 window/CSA/HCA/index formula matches calculator'])


if __name__ == '__main__':
    data = calculate()
    (HERE/'long-context-comparison.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    for row in data['models']:
        print(row['model'], row['history'], round(row['matrix_flops']/1e9,2), round(row['history_interaction_flops']/1e9,2), round(row['state_bytes']/2**30,3))
