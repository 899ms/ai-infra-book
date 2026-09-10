#!/usr/bin/env python3
"""Exact teaching model, plus event sweep for 1,000 evenly spaced tasks.
Resident environments are reused from a warm pool; JIT environments are rebuilt.
Intervals are half-open. Preparation uses 0.05 CPU for two seconds.
"""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import json

def calculate():
    options = []
    for model, seconds, price in [('ordinary', 9, F('.010')), ('fast', 6, F('.012'))]:
        for jit in [False, True]:
            events = defaultdict(lambda: [F(0)] * 3)  # CPU, GiB, model slots
            def interval(start, end, resource, amount):
                events[start][resource] += amount
                events[end][resource] -= amount
            duration = 3 * (seconds + 1)
            phases = []
            for r in range(3):
                start = r * (seconds + 1)
                phases.append({'model': [start, start + seconds],
                               'prepare': [start + seconds - 2, start + seconds] if jit else None,
                               'tool': [start + seconds, start + seconds + 1]})
            for n in range(1000):
                arrival = F(n, 10)
                if not jit:
                    interval(arrival, arrival + duration, 1, 2)
                for phase in phases:
                    a, b = phase['model']; interval(arrival+a, arrival+b, 2, 1)
                    a, b = phase['tool']; interval(arrival+a, arrival+b, 0, 1)
                    if jit:
                        a, b = phase['prepare']
                        interval(arrival+a, arrival+b, 0, F(1,20))
                        interval(arrival+a, arrival+b+1, 1, 2)
            active = [F(0)] * 3; peaks = active.copy(); areas = active.copy(); previous = F(0)
            for t, delta in sorted(events.items()):
                for i in range(3):
                    areas[i] += active[i] * (t-previous)
                    active[i] += delta[i]
                    peaks[i] = max(peaks[i], active[i])
                previous = t
            assert active == [0,0,0]
            cpu, memory, slots = [x/1000 for x in areas]
            cost = 3*price + (cpu+memory)*F('.0001')
            joint = F('.95') if duration <=24 else F(0)
            options.append({'model': model, 'environment': 'jit' if jit else 'resident',
                'duration_seconds': duration, 'phases': phases,
                'cpu_core_seconds': str(cpu), 'memory_gib_seconds': str(memory),
                'model_slot_seconds': str(slots), 'submission_cost': str(cost),
                'on_time_quality_probability': str(joint),
                'cost_per_on_time_quality': str(cost/joint) if joint else None,
                'peak_cpu_memory_slots': [str(x) for x in peaks],
                'within_capacity': all(a<=b for a,b in zip(peaks,[40,640,300]))})
    return {'kind': 'deterministic teaching design, not a deployment measurement',
            'arrivals': {'count':1000, 'spacing_seconds':'1/10'},
            'preparation': {'seconds':2, 'core_seconds':'1/10', 'gib':2},
            'resident_pool': 'warm reusable environments; initialization is amortized over pool lifetime',
            'options': options, 'inter_call_gap_cost_crossover_seconds':str(F(41,20))}

def build_design(path):
    path.write_text(json.dumps(calculate(),ensure_ascii=False,indent=2)+'\n')

if __name__ == '__main__':
    build_design(Path(__file__).with_name('platform-design.json'))
