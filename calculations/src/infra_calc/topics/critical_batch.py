"""Gradient-noise-scale step/example trade-off applied to the chapter-10 continued-training design.

Relation used (references/text/scaling-laws.txt lines 782-792, Kaplan et al. quoting McCandlish et al.
[MKAT18]): "(S/S_min - 1)(E/E_min - 1) = 1 ... This relation defines the critical batch size
B_crit(L) = E_min/S_min".  Writing B_noise for B_crit and E = B*S gives S(B) = S_min (1 + B_noise/B)
and E(B) = E_min (1 + B/B_noise).  The underlying model is McCandlish et al., references/text/
large-batch-empirical.txt line 267 (optimal loss improvement "1 + Bnoise/B", eq. 2.7), line 268-271
(noise scale B_noise = tr(H Sigma)/(G^T H G), eq. 2.8) and line 288 ("the switch between the two
occurs at B ~ Bnoise").  The noise scale itself is a declared input; the archived text only
says (line 147) that for their models it "is roughly 1-2 million" tokens, so no measured value for the
chapter's model exists here.  The reference run (384 sequences x 8192 tokens per step, 100B tokens) is
chapter 10's own design and is taken as exactly sufficient for its target loss.
"""
from fractions import Fraction

from ..declared import exact, input_sources as _sources
from ..units import ceil_div, positive_int


def calculate(declared_noise_scale_tokens=2 * 10**6, reference_sequences_per_step=384, sequence_tokens=8192,
              total_tokens=100 * 10**9, reference_cards=48, microbatches_per_card=8,
              step_seconds_at_reference='56.7', compute_seconds_at_reference='52.2',
              overhead_seconds_per_step='4.5', card_counts=(32, 48, 96, 192, 384, 768, 1536), input_sources=None):
    inputs = {k: v for k, v in locals().items() if k != 'input_sources'}
    sources = _sources(inputs, input_sources)
    for name in ('declared_noise_scale_tokens', 'reference_sequences_per_step', 'sequence_tokens', 'total_tokens',
                 'reference_cards', 'microbatches_per_card'):
        positive_int(inputs[name], name)
    step = exact(step_seconds_at_reference, 'step_seconds_at_reference')
    compute = exact(compute_seconds_at_reference, 'compute_seconds_at_reference')
    overhead = exact(overhead_seconds_per_step, 'overhead_seconds_per_step', allow_zero=True)
    if compute + overhead != step:
        raise ValueError('step seconds must equal compute plus overhead seconds')
    if reference_cards * microbatches_per_card != reference_sequences_per_step:
        raise ValueError('reference cards x microbatches per card must give the reference batch')
    noise = Fraction(declared_noise_scale_tokens)
    b_ref = Fraction(reference_sequences_per_step * sequence_tokens)
    s_ref = ceil_div(total_tokens, int(b_ref))
    s_min = Fraction(s_ref) / (1 + noise / b_ref)
    e_min = s_min * noise
    e_ref = s_ref * b_ref

    def steps(batch):
        return s_min * (1 + noise / batch)

    rows = []
    for cards in card_counts:
        positive_int(cards, 'cards')
        batch = Fraction(cards * microbatches_per_card * sequence_tokens)
        s = steps(batch)
        e = e_min * (1 + batch / noise)
        weak_time = s * step
        strong_steps = Fraction(s_ref)
        strong_step_seconds = compute * reference_cards / cards + overhead
        strong_time = strong_steps * strong_step_seconds
        rows.append(dict(cards=cards, weak_batch_tokens=int(batch), weak_batch_sequences=cards * microbatches_per_card,
                         weak_steps_exact=str(s), weak_steps=float(s), weak_examples_tokens=float(e),
                         weak_examples_over_reference=float(e / e_ref),
                         weak_wall_seconds=float(weak_time), weak_wall_days=float(weak_time / 86400),
                         weak_speedup_over_reference=float(s_ref * step / weak_time),
                         strong_batch_tokens=int(b_ref), strong_steps=s_ref,
                         strong_step_seconds_exact=str(strong_step_seconds), strong_wall_seconds=float(strong_time),
                         strong_wall_days=float(strong_time / 86400),
                         strong_speedup_over_reference=float(s_ref * step / strong_time),
                         weak_batch_over_noise_scale=float(batch / noise)))
    ceiling = s_ref * step / (s_min * step)
    return dict(schema_version=1, calculation='critical-batch', scenario=inputs, declared_input_sources=sources,
                relation='S(B) = S_min (1 + B_noise/B); E(B) = E_min (1 + B/B_noise); B_noise = E_min/S_min',
                reference=dict(batch_tokens=int(b_ref), steps=s_ref, examples_tokens=int(e_ref),
                               noise_scale_tokens=declared_noise_scale_tokens,
                               batch_over_noise_scale_exact=str(b_ref / noise),
                               s_min_exact=str(s_min), s_min=float(s_min), e_min_exact=str(e_min), e_min=float(e_min),
                               step_seconds=float(step), wall_seconds=float(s_ref * step), wall_days=float(s_ref * step / 86400)),
                rows=rows,
                summary=dict(weak_scaling_speedup_ceiling_exact=str(ceiling), weak_scaling_speedup_ceiling=float(ceiling),
                             weak_scaling_step_floor=float(s_min),
                             cards_where_weak_batch_equals_noise_scale=float(noise / (microbatches_per_card * sequence_tokens)),
                             half_efficiency_batch_tokens=declared_noise_scale_tokens),
                assumptions=[
                    '关系式取自归档 scaling-laws 文本对 McCandlish 等人结果的转述：(S/S_min-1)(E/E_min-1)=1；B_noise 为声明输入，未对本章模型实测。',
                    '参考运行（每步 384×8192 token、共 100B token）视为恰好达到目标：由 S_ref 与 B_ref 反推 S_min 与 E_min，其他批量的步数与样本数按关系式换算。',
                    '弱扩展：每卡固定微批数，批量随卡数增长，每步时间不变（取本章 48 卡的 56.7 s）；强扩展：批量固定，计算时间按卡数反比缩放，通信与输入等待 4.5 s 不变。两者都不含并行效率变化。',
                    '弱扩展加速上限 = S_ref/S_min，是数据并行扩大批量的天花板；不代表学习率调度、warmup 或质量变化。',
                ])
