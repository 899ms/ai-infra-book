"""Recompute all ten exercises in the current chapter 11 using exact arithmetic.

Prices are the manuscript's fixed inputs, not current market quotations.
The historical experiment directories retain their separate measurement scope.
"""
from collections import defaultdict
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT/'manuscripts/11-资源调度与运行环境.md'
spec = importlib.util.spec_from_file_location('platform_design', ROOT/'manuscripts/ch11/platform_design.py')
platform = importlib.util.module_from_spec(spec)
spec.loader.exec_module(platform)


def schedule(arrivals, durations, workers):
    free = [F(0)]*workers
    result = []
    for arrival, duration in zip(arrivals, durations):
        worker = min(range(workers), key=lambda w: (free[w], w))
        start = max(F(arrival), free[worker])
        free[worker] = start+duration
        result.append(dict(arrival=arrival, worker=worker, start=start, end=free[worker]))
    return result


def design(burst, jit):
    events = defaultdict(lambda: [F(0)]*3)
    phases = []
    def interval(a, b, resource, amount):
        events[a][resource] += amount
        events[b][resource] -= amount
    for i in range(1500):
        a = F(i//15) if burst else F(i, 15)
        if not jit:
            interval(a, a+9, 1, 2)
        for r in range(3):
            start = a+3*r
            interval(start, start+2, 2, 1)
            interval(start+2, start+3, 0, 1)
            if jit:
                interval(start, start+2, 0, F(1, 20))
                interval(start, start+3, 1, 2)
            if i < 150:
                phases.append(dict(task=i, round=r, model=[start, start+2], tool=[start+2, start+3]))
    active = [F(0)]*3
    peak = active.copy()
    area = active.copy()
    previous = F(0)
    timeline = []
    for t, delta in sorted(events.items()):
        for j in range(3):
            area[j] += active[j]*(t-previous)
            active[j] += delta[j]
            peak[j] = max(peak[j], active[j])
        if t <= 15:
            timeline.append(dict(time=t, cpu=active[0], memory_gib=active[1], model_slots=active[2]))
        previous = t
    assert active == [0, 0, 0]
    per_task = [x/1500 for x in area]
    model_cost = 3*platform.gpu_seconds_per_call(2, 16)*platform.B200_USD_PER_HOUR/3600
    cost = model_cost+per_task[0]*platform.CPU_USD_PER_CORE_SECOND+per_task[1]*platform.MEM_USD_PER_GIB_SECOND
    return dict(burst=burst, jit=jit, peak_cpu_memory_slots=peak, per_task_cpu_memory_slots=per_task,
                replicas_needed=math.ceil(peak[2]/16), tool_hosts_needed=max(math.ceil(peak[0]/platform.HOST_CORES), math.ceil(peak[1]/platform.HOST_GIB)),
                submission_cost=cost, cost_per_on_time_success=cost/F('.95'), timeline=timeline, phases=phases)


def calculate():
    results = {}
    results['11-1'] = dict(mean_rounds=3, model_calls_per_second=24, concurrent_model_calls=144,
                          mean_cpu_cores=24, resident_memory_gib=336, rebuilt_memory_gib=144,
                          rebuilt_environments_per_second=24)
    results['11-2'] = dict(rebuild={'resident_intervals': [[F('6.3'), 10]], 'tool': [9, 10], 'gib_seconds': F('7.4')},
                          snapshot={'save': [0, 8], 'restore': [8, 9], 'tool': [9, 10], 'gib_seconds': 20})
    results['11-3'] = [dict(accuracy=p, lead_seconds=a, expected_wait_seconds=p*max(2-a, 0)+(1-p)*2,
                           wasted_prediction_gib_seconds=(1-p)*2*a) for p in [F('.6'), F('.9')] for a in [1, 2, 4]]
    results['11-4'] = dict(new_task_migration_better_when_m_less_than=12,
                          sum_of_wait_and_delay_better_when_m_less_than=5,
                          wait_completion_seconds=32, migration_completion_expression='m+20',
                          wait_objective=12, migration_objective_expression='2*m+2')
    results['11-5'] = [dict(lifetime=t, preparation=p, useful_tokens=(t-p)*100, useful_fraction=F(t-p, t))
                          for p in [8, 4] for t in [10, 20, 40]]
    results['11-6'] = [dict(workers=w, last_duration=d, tasks=schedule([0,6,12], [10,2,d], w),
                           completion=max(r['end'] for r in schedule([0,6,12], [10,2,d], w))) for w in [1,2] for d in [8,80]]
    results['11-7'] = dict(cost_per_success='(0.0430 - 0.0342*h)/(0.90 + 0.09*h)',
                          on_time_success_probability='0.99*h', minimum_hit_fraction=F(10,11),
                          independent_model_minimum_hit_fraction=F(45,49))
    n = F('19555.2')*F('.98')/(F('.90')*3*F('.0088'))
    results['11-8'] = dict(crossover_tasks=n, first_integer_self_host_cheaper=math.floor(n)+1,
                          capacity=500000, crossover_feasible=False,
                          self_host_cost_per_success_at_capacity=F('19555.2')/(F('.90')*500000),
                          api_cost_per_success=3*F('.0088')/F('.98'))
    branches = [(F('.8'),10,True), (F('.12')*F('.6'),14,True),
                (F('.08')*F('.98'),18,True), (F('.08')*F('.02'),18,False),
                (F('.12')*F('.4')*F('.98'),22,True), (F('.12')*F('.4')*F('.02'),22,False)]
    assert sum(p for p,_,_ in branches) == 1
    results['11-9'] = [dict(deadline=d, on_time_success=sum(p for p,t,ok in branches if ok and t<=d),
                           cost_without_stopping=F('.01456'),
                           cost_with_stopping=F('.010') + (F('.12')*F('.006') if d>=14 else 0)
                           + (F('.08')*F('.030') if d>=18 else 0)
                           + (F('.12')*F('.4')*F('.030') if d>=22 else 0)) for d in [14,18,22]]
    results['11-10'] = [design(burst,jit) for burst in [False,True] for jit in [False,True]]
    assert results['11-10'][0]['peak_cpu_memory_slots'] == [45,270,90]
    assert results['11-10'][1]['peak_cpu_memory_slots'] == [F('49.5'),270,90]
    assert results['11-10'][2]['peak_cpu_memory_slots'] == [45,270,90]
    assert results['11-10'][3]['peak_cpu_memory_slots'] == [F('49.5'),270,90]
    assert results['11-10'][0]['per_task_cpu_memory_slots'] == [3,18,6]
    return results


if __name__ == '__main__':
    output = dict(scope='Exact calculations for current manuscript exercises, not hardware or cloud measurements.',
                  source=str(SOURCE.relative_to(ROOT)), source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), results=calculate())
    (HERE/'results.json').write_text(json.dumps(output, ensure_ascii=False, indent=2, default=str)+'\n')
    print('Completed 10 chapter-11 exercise calculations; event sweep: 6,000 tasks, 18,000 tool intervals.')
