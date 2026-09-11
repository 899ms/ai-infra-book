"""Expert capacity factor: padded rows and dropped tokens for an uneven dispatch.

Rule from references/text/switch-transformer.txt lines 376-381: "The expert capacity—the number of
tokens each expert computes—is set by evenly dividing the number of tokens in the batch across the
number of experts, and then further expanding by a capacity factor, expert capacity =
(tokens per batch / number of experts) x capacity factor."  With top-k routing the batch contributes
tokens x k assignments, so capacity = c x tokens x k / E.  Lines 344-352 describe the consequence:
experts that overflow drop the excess tokens for that layer, and under-full experts leave padded
slots that still cost compute and communication.  GShard (references/text/gshard.txt lines 283-287)
states the same rule without the term: expert capacity O(N/E) for N tokens and E experts with top-2
dispatch, per-group fractional capacity 2N/(G E), and overflowed tokens "passed on to the next layer via
residual connections".
"""
from fractions import Fraction
from math import floor

from ..declared import exact, input_sources as _sources
from ..sources import model_config, provenance
from ..units import positive_int


def _ledger(histogram, capacity):
    rows, dropped, padded = [], 0, 0
    for expert, count in enumerate(histogram):
        drop = max(0, count - capacity)
        pad = max(0, capacity - count)
        dropped += drop; padded += pad
        rows.append(dict(expert=expert, assignments=count, capacity=capacity, executed_rows=min(count, capacity),
                         dropped=drop, padded=pad))
    return rows, dropped, padded


def calculate(model='qwen3-235b-a22b', tokens=8192, capacity_factors=('1', '1.25', '1.5', '2'),
              chapter_histogram=(96, 32), declared_hot_fraction='1/2', declared_hot_multiplier='3/2',
              input_sources=None):
    inputs = {k: v for k, v in locals().items() if k != 'input_sources'}
    sources = _sources(inputs, input_sources)
    positive_int(tokens, 'tokens')
    config = model_config(model)
    experts, top_k = config['num_experts'], config['num_experts_per_tok']
    hot_fraction = exact(declared_hot_fraction, 'declared_hot_fraction')
    hot_multiplier = exact(declared_hot_multiplier, 'declared_hot_multiplier')
    if hot_fraction >= 1 or hot_multiplier * hot_fraction > 1:
        raise ValueError('hot experts cannot receive more than all assignments')
    factors = [exact(c, 'capacity_factor') for c in capacity_factors]
    if not isinstance(chapter_histogram, (list, tuple)) or not chapter_histogram:
        raise ValueError('chapter_histogram must be a nonempty list of assignment counts')
    for count in chapter_histogram:
        positive_int(count, 'assignment count', allow_zero=True)
    # Chapter 10 two-expert example: E = number of experts in the histogram, k = 1.
    chapter_total = sum(chapter_histogram)
    chapter_mean = Fraction(chapter_total, len(chapter_histogram))
    chapter = []
    for c in factors:
        capacity = floor(c * chapter_mean)
        rows, dropped, padded = _ledger(list(chapter_histogram), capacity)
        chapter.append(dict(capacity_factor_exact=str(c), capacity_per_expert=capacity, rows=rows,
                            dropped_total=dropped, dropped_fraction_exact=str(Fraction(dropped, chapter_total)),
                            padded_total=padded, executed_rows_total=len(chapter_histogram) * capacity,
                            padded_fraction_of_executed_exact=str(Fraction(padded, len(chapter_histogram) * capacity)),
                            busiest_expert_rows=max(r['executed_rows'] for r in rows)))
    # Locked-config example: E experts, top-k, tokens x k assignments with a declared hot/cold split.
    assignments = tokens * top_k
    hot = int(hot_fraction * experts)
    cold = experts - hot
    if hot < 1 or cold < 1:
        raise ValueError('hot fraction must leave at least one hot and one cold expert')
    mean = Fraction(assignments, experts)
    hot_each = hot_multiplier * mean
    cold_each = (assignments - hot * hot_each) / cold
    if hot_each.denominator != 1 or cold_each.denominator != 1:
        raise ValueError('declared skew must give whole assignment counts per expert')
    histogram = [int(hot_each)] * hot + [int(cold_each)] * cold
    if sum(histogram) != assignments:
        raise ValueError('skewed histogram does not conserve assignments')
    model_rows = []
    for c in factors:
        capacity = floor(c * mean)
        rows, dropped, padded = _ledger(histogram, capacity)
        model_rows.append(dict(capacity_factor_exact=str(c), capacity_per_expert=capacity,
                               hot_expert=rows[0], cold_expert=rows[-1],
                               dropped_total=dropped, dropped_fraction_exact=str(Fraction(dropped, assignments)),
                               dropped_fraction=float(Fraction(dropped, assignments)),
                               padded_total=padded, executed_rows_total=experts * capacity,
                               padded_fraction_of_executed_exact=str(Fraction(padded, experts * capacity)),
                               padded_fraction_of_executed=float(Fraction(padded, experts * capacity)),
                               executed_over_useful_exact=str(Fraction(experts * capacity, assignments)),
                               busiest_expert_rows=max(r['executed_rows'] for r in rows)))
    summary = dict(chapter_assignments=chapter_total, model_experts=experts, model_top_k=top_k, model_assignments=assignments)
    for row in chapter:
        summary[f"chapter_c{row['capacity_factor_exact']}_capacity"] = row['capacity_per_expert']
        summary[f"chapter_c{row['capacity_factor_exact']}_dropped"] = row['dropped_total']
        summary[f"chapter_c{row['capacity_factor_exact']}_padded"] = row['padded_total']
    for row in model_rows:
        summary[f"model_c{row['capacity_factor_exact']}_capacity"] = row['capacity_per_expert']
        summary[f"model_c{row['capacity_factor_exact']}_dropped_fraction"] = row['dropped_fraction']
        summary[f"model_c{row['capacity_factor_exact']}_padded_fraction_of_executed"] = row['padded_fraction_of_executed']
    return dict(schema_version=1, calculation='moe-capacity', scenario=inputs, declared_input_sources=sources, summary=summary,
                sources=provenance(model),
                rule='capacity per expert = floor(c x tokens x k / E); rows beyond capacity are dropped, rows below are padded',
                chapter_example=dict(experts=len(chapter_histogram), top_k=1, assignments=chapter_total,
                                     mean_per_expert_exact=str(chapter_mean), histogram=list(chapter_histogram), rows=chapter),
                model_example=dict(model=model, experts=experts, top_k=top_k, tokens=tokens, assignments=assignments,
                                   mean_per_expert_exact=str(mean), hot_experts=hot, cold_experts=cold,
                                   hot_assignments_each=int(hot_each), cold_assignments_each=int(cold_each), rows=model_rows),
                assumptions=[
                    '容量因子规则取自归档 Switch Transformer 文本：每专家容量 = (token 数×k/E)×c，向下取整；超出容量的分派被丢弃（该层不处理），不足的槽位填充，仍占用计算与通信。',
                    '第 10 章示例：两张卡上的专家分别收到 96、32 次分派，按 E=2、k=1 处理。锁定配置示例：Qwen3-235B 的 E 与 k 来自官方 config；不均衡形状（一半专家收到 1.5 倍均值）为声明输入，与 96/32 的 3:1 比例一致。',
                    '只统计行数：丢弃 token 对质量的影响、辅助损失、专家并行的通信量与实际内核分组方式都不在本账内。',
                ])
