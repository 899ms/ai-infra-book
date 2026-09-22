#!/usr/bin/env python3
"""Audit archived event timestamps; all durations are wall seconds, not GPU-hours.

Run from any directory. Outputs JSON to stdout; does not modify source snapshots.
"""
import json
from math import isclose, sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / name).read_text())


def event_key(event):
    return tuple(event.get(k) for k in ('t', 'kind', 'step', 'redo'))


def calculate(run):
    status = read(f'status_{run}.json')
    series = read(f'series_{run}.json')
    events = read(f'events_{run}.json')
    snapshots = [read(f'status_{run}_2026-09-18.json'), status]
    merged = {event_key(e): e for s in snapshots for e in s['events']}
    assert events == sorted(merged.values(), key=lambda e: e['t'])
    start, end = status['run']['start'], status['run']['end']
    steps = series['series']['timing_s/step']
    assert series['steps'] == list(range(1, 31)) and len(steps) == 30
    assert series['run_start'] == start
    last_by_step = {e['step']: e for e in events if e['kind'] == 'step'}
    assert [last_by_step[i]['t'] for i in series['steps']] == series['walls']
    restarts = sum(e['kind'] == 'restart' for e in events)
    assert restarts == status['totals']['restarts']
    previous = start
    gaps, superseded, redone, segments = [], [], [], []
    for e in events:
        elapsed = e['t'] - previous
        assert elapsed >= 0
        interval = dict(start=previous, end=e['t'], seconds=elapsed)
        if e['kind'] == 'restart':
            gaps.append(interval)
        elif e['kind'] == 'step':
            if e != last_by_step[e['step']]:
                superseded.append(dict(step=e['step'], **interval))
            if e.get('redo'):
                redone.append(dict(step=e['step'], **interval))
        category = ('interruption' if e['kind'] == 'restart' else
                    'rollback' if e['kind'] == 'step' and e != last_by_step[e['step']] else
                    'step' if e['kind'] == 'step' else 'tail')
        segments.append(dict(kind=category, step=e.get('step'), **interval))
        previous = e['t']
    total, retained = end - start, sum(steps)
    before_restart = sum(e['seconds'] for e in gaps)
    old_steps = sum(e['seconds'] for e in superseded)
    redo_steps = sum(e['seconds'] for e in redone)
    remainder = total - retained - before_restart - old_steps
    assert isclose(total, retained + before_restart + old_steps + remainder)
    rate = status['cost']['rate_per_s']
    assert isclose(status['cost']['so_far'], total*rate, rel_tol=1e-8)
    assert isclose(sum(e['seconds'] for e in segments), total)
    costs = dict(
        rate_usd_per_second=rate, rate_usd_per_hour=rate*3600,
        total_usd=total*rate, interruption_window_usd=before_restart*rate,
        rollback_window_usd=old_steps*rate,
        combined_estimated_usd=(before_restart+old_steps)*rate,
        mean_interruption_window_usd=before_restart*rate/restarts,
        interruption_events=[dict(number=i+1, seconds=e['seconds'], usd=e['seconds']*rate)
                             for i,e in enumerate(gaps)],
        pro_half_interruption_time_savings_usd=before_restart*rate/2 if run == 'pro' else None,
        assumption='Event-window opportunity-cost estimate at the official fixed rate, not separately measured discarded compute or an invoice. Savings assume avoided time shortens the run with other work unchanged.',
    )
    return dict(
        run_start=start, segments=segments, costs=costs,
        wall_seconds=total, retained_step_metric_seconds=retained,
        unallocated_wall_seconds=total-retained,
        unallocated_fraction_of_wall=(total-retained)/total,
        unallocated_relative_to_step_metric=(total-retained)/retained,
        mean_step_seconds=retained/30, restarts=restarts,
        wall_seconds_per_restart=total/restarts,
        pre_restart_intervals=gaps, pre_restart_seconds=before_restart,
        pre_restart_fraction_of_wall=before_restart/total,
        superseded_step_intervals=superseded, superseded_step_seconds=old_steps,
        redo_step_intervals=redone, redo_step_seconds=redo_steps,
        old_memo_fraction=(before_restart+redo_steps)/total,
        remainder_seconds=remainder, after_last_step_seconds=end-series['walls'][-1],
        start_to_last_step_seconds=series['walls'][-1]-start,
        first_five_mean_seconds=sum(steps[:5])/5,
        last_five_mean_seconds=sum(steps[-5:])/5,
        step_growth_ratio=sum(steps[-5:])/sum(steps[:5]),
        first_context_mean=series['series']['ctx_total_length/mean'][0],
        last_context_mean=series['series']['ctx_total_length/mean'][-1],
    )


def design_case():
    # Same payload and MTBF as calculations/results/checkpoint-interval-book.md.
    save = 114670295040 / 7000000000
    return {str(n): dict(
        overhead_fraction=save/1800 + n/29122560*(1800/2+120),
        optimal_interval_seconds=sqrt(2*save/(n/29122560)),
    ) for n in (32, 48, 1024)}


if __name__ == '__main__':
    print(json.dumps(dict(
        units='seconds unless fraction, count, ratio or context length',
        limitation='Unallocated wall time and pre-restart intervals are not measurements of discarded computation or pure recovery time.',
        runs={run: calculate(run) for run in ('pro', 'flash')},
        design_case=design_case(),
    ), ensure_ascii=False, indent=2))
