#!/usr/bin/env python3
"""Exact design model, plus event sweep for 1,000 evenly spaced tasks.

Model service: DeepSeek V4-Flash on 4xB200 replicas (chapter 13 single-agent-serving
comparison, 200K history): 32 sessions/replica give 25.3 ms per output token, 16 give
16.9 ms; a 355-token call therefore takes 9.0 s or 6.0 s.  GPU time per call is
4 GPUs x call seconds / sessions, priced at the archived Runpod B200 pod rate.
Tool host: EC2 m5d.metal from the Firecracker paper (48 cores, 384 GB RAM).
Environment: 1 vCPU / 2 GiB microVM; CPU and memory priced at the archived E2B
per-second rates.  Resident environments are reused from a warm pool; JIT
environments are rebuilt each round (2 s hot path, 0.1 CPU-second).
Intervals are half-open.  Preparation uses 0.05 CPU for two seconds.
"""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import json, math

GPU_PER_REPLICA = 4
B200_USD_PER_HOUR = F('6.79')                 # Runpod B200 pod, 2026-09-09 snapshot
CPU_USD_PER_CORE_SECOND = F('0.000014')       # E2B, per vCPU-second
MEM_USD_PER_GIB_SECOND = F('0.0000045')       # E2B, per GiB-second
HOST_CORES = 48                               # m5d.metal: 2x Xeon Platinum 8175M, SMT off
HOST_GIB = F(384 * 10**9, 2**30)              # 384 GB RAM
REPLICAS_AVAILABLE = 10                       # 40 B200
SERVICES = [('ordinary', 9, 32), ('fast', 6, 16)]   # call seconds, sessions per replica
TOKENS_PER_CALL = 355
MS_PER_TOKEN = {'ordinary': 1000 / 39.499741066648745, 'fast': 1000 / 59.08403886945592}


def gpu_seconds_per_call(seconds, sessions):
    return F(GPU_PER_REPLICA * seconds, sessions)


def calculate():
    options = []
    for model, seconds, sessions in SERVICES:
        call_gpu_s = gpu_seconds_per_call(seconds, sessions)
        call_usd = call_gpu_s * B200_USD_PER_HOUR / 3600
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
            model_cost = 3 * call_usd
            cost = model_cost + cpu*CPU_USD_PER_CORE_SECOND + memory*MEM_USD_PER_GIB_SECOND
            joint = F('.95') if duration <= 24 else F(0)
            slots_available = REPLICAS_AVAILABLE * sessions
            replicas_needed = math.ceil(peaks[2] / sessions)
            tool_ok = peaks[0] <= HOST_CORES and peaks[1] <= HOST_GIB
            options.append({'model': model, 'environment': 'jit' if jit else 'resident',
                'duration_seconds': duration, 'phases': phases,
                'call_seconds': seconds, 'sessions_per_replica': sessions,
                'gpu_seconds_per_call': str(call_gpu_s), 'usd_per_call': str(call_usd),
                'cpu_core_seconds': str(cpu), 'memory_gib_seconds': str(memory),
                'model_slot_seconds': str(slots), 'model_usd': str(model_cost),
                'cpu_usd': str(cpu*CPU_USD_PER_CORE_SECOND), 'memory_usd': str(memory*MEM_USD_PER_GIB_SECOND),
                'submission_cost': str(cost),
                'on_time_quality_probability': str(joint),
                'cost_per_on_time_quality': str(cost/joint) if joint else None,
                'peak_cpu_memory_slots': [str(x) for x in peaks],
                'tool_host_within_capacity': tool_ok,
                'model_slots_with_available_replicas': slots_available,
                'model_replicas_needed': replicas_needed,
                'within_capacity': tool_ok and peaks[2] <= slots_available})
    crossover = (2*2*MEM_USD_PER_GIB_SECOND + F(1,10)*CPU_USD_PER_CORE_SECOND) / (2*MEM_USD_PER_GIB_SECOND)
    return {'kind': 'deterministic design on named deployments; model timing from the chapter 13 calculation, prices from archived list prices',
            'arrivals': {'count':1000, 'spacing_seconds':'1/10'},
            'model_service': {'model': 'DeepSeek V4-Flash', 'gpu': 'B200', 'gpus_per_replica': GPU_PER_REPLICA,
                              'replicas_available': REPLICAS_AVAILABLE, 'tokens_per_call': TOKENS_PER_CALL,
                              'ms_per_output_token': MS_PER_TOKEN,
                              'exact_call_seconds': {k: TOKENS_PER_CALL*v/1000 for k, v in MS_PER_TOKEN.items()},
                              'b200_usd_per_hour': str(B200_USD_PER_HOUR),
                              'sources': ['experiments/ch13/13-06/single-agent-serving/comparison.json',
                                          'experiments/ch13/13-06/single-agent-serving/comparison-sources/gpu-prices.md']},
            'tool_host': {'name': 'EC2 m5d.metal', 'cores': HOST_CORES, 'memory_bytes': 384*10**9,
                          'memory_gib': str(HOST_GIB), 'max_resident_2gib_environments': int(HOST_GIB // 2),
                          'source': 'references/text/firecracker.txt'},
            'environment': {'vcpu': 1, 'gib': 2, 'source': 'references/files/documents/e2b-pricing.md'},
            'prices': {'cpu_usd_per_core_second': str(CPU_USD_PER_CORE_SECOND),
                       'memory_usd_per_gib_second': str(MEM_USD_PER_GIB_SECOND)},
            'preparation': {'seconds':2, 'core_seconds':'1/10', 'gib':2,
                            'cold_extra_seconds_25gbe': 2**31 / (25e9/8)},
            'resident_pool': 'warm reusable environments; initialization is amortized over pool lifetime',
            'options': options, 'inter_call_gap_cost_crossover_seconds': str(crossover)}

def build_design(path):
    path.write_text(json.dumps(calculate(),ensure_ascii=False,indent=2)+'\n')

if __name__ == '__main__':
    build_design(Path(__file__).with_name('platform-design.json'))
