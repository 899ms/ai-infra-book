"""Decision requests: one shared forward over state and questions, no token generation.

A decision request carries a state and several typed questions; every answer is a
probability distribution read at one position of the same forward pass, so the whole
request is one prefill of ``input_tokens`` positions and zero decode steps. The same
input is priced three ways: as that single forward on Qwen3-8B and on DeepSeek V4.1
Flash (CED path), and as a conventional LLM request that prefills the same input and
then decodes ``output_tokens`` tokens on Qwen3-8B. Device peaks come from
hardware.json; list prices and the leasing rate come from the archived sources in
configs/decision-request.lock.json.
"""
from fractions import Fraction as F
import hashlib
import json
from .. import hardware
from ..models import forward
from ..paths import PROJECT
from ..schema import Scenario
from ..sources import provenance
from ..units import positive_int
from .pd_pool import exact_rate
from . import v41_forward

LOCK = PROJECT / 'configs/decision-request.lock.json'
DECISION_MODEL = 'qwen3-8b'
V41_MODEL = 'deepseek-v4.1-flash'


def evidence() -> dict:
    lock = json.loads(LOCK.read_text())
    for row in lock['files']:
        data = (PROJECT / row['file']).read_bytes()
        if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
            raise ValueError('Decision-request source changed: ' + row['file'])
    return lock


def _dec(value: F, places: int = 6) -> float:
    return round(float(value), places)


def _head_flops_per_position() -> int:
    with_head = forward(DECISION_MODEL, Scenario(tokens=1, output_head='last'))['summary']['matrix_flops']
    without = forward(DECISION_MODEL, Scenario(tokens=1, output_head='none'))['summary']['matrix_flops']
    return with_head - without


def calculate(input_tokens=None, questions=8, output_tokens=(64, 512), decode_batch=64,
              device='h100-sxm', compute_efficiency='0.4', bandwidth_efficiency='0.5',
              cny_per_usd='7'):
    """Price one decision request on named hardware and against published list prices.

    input_tokens defaults to the demo's input length derived from its published cost
    and list price. questions is the number of answer positions read from the shared
    forward. output_tokens lists the generation lengths priced for the LLM path.
    compute_efficiency is the H100 BF16 MFU the book uses (Llama 3, 38%-43%);
    bandwidth_efficiency is the decode MBU calibrated in chapter 8. cny_per_usd is a
    declared conversion for the DeepSeek list price only.
    """
    lock = evidence()
    declared = lock['declared']
    jev_price = exact_rate(declared['jev']['usd_per_million_input_tokens'], 'jev price') / 10**6
    demo_jev_usd = exact_rate(declared['demo']['jev_usd'], 'demo jev usd')
    derived_tokens = demo_jev_usd / jev_price
    if input_tokens is None:
        input_tokens = int(derived_tokens + F(1, 2))
    positive_int(input_tokens, 'input_tokens')
    positive_int(questions, 'questions')
    positive_int(decode_batch, 'decode_batch')
    if isinstance(output_tokens, int):
        output_tokens = (output_tokens,)
    output_tokens = tuple(output_tokens)
    if not output_tokens or len(output_tokens) > 8:
        raise ValueError('Provide 1 to 8 output lengths for the LLM path')
    for value in output_tokens:
        positive_int(value, 'output_tokens')
        if value < 2:
            raise ValueError('The LLM path needs at least one decode step')
    eta_c = exact_rate(compute_efficiency, 'compute_efficiency')
    eta_b = exact_rate(bandwidth_efficiency, 'bandwidth_efficiency')
    if eta_c > 1 or eta_b > 1:
        raise ValueError('Efficiency factors must not exceed 1')
    fx = exact_rate(cny_per_usd, 'cny_per_usd')
    dev = hardware.select_device(device)
    peak = hardware.select_peak(dev, 'BF16', 'FP32', 'tensor', 'dense')
    if dev['memory']['bandwidth_bytes_per_second'] is None:
        raise ValueError(f'No verified memory bandwidth for {device}')
    compute = F(str(peak['tera_ops_per_second'])) * 10**12 * eta_c
    bandwidth = F(str(dev['memory']['bandwidth_bytes_per_second'])) * eta_b
    usd_per_gpu_second = exact_rate(declared['gpu_leasing']['usd_per_gpu_hour'], 'gpu hour usd') / 3600

    def usd(gpu_seconds):
        return gpu_seconds * usd_per_gpu_second

    # Decision path on the dense model: one forward, one head position per question.
    pre = forward(DECISION_MODEL, Scenario(tokens=input_tokens, output_head='last'))['summary']
    head = _head_flops_per_position()
    decision_flops = pre['matrix_flops'] + (questions - 1) * head
    decision_compute = F(decision_flops) / compute
    decision_memory = F(pre['weight_read_once_per_operator_bytes']) / bandwidth
    decision_latency = max(decision_compute, decision_memory)
    decision = dict(
        model=DECISION_MODEL, matrix_flops=decision_flops, head_flops_per_position=head,
        weight_read_bytes=pre['weight_read_once_per_operator_bytes'],
        kv_written_bytes=pre['kv_new_write_bytes'], kv_retained_bytes=0,
        compute_seconds_exact=str(decision_compute), memory_seconds_exact=str(decision_memory),
        bound='compute' if decision_compute >= decision_memory else 'memory',
        latency_seconds=_dec(decision_latency), gpu_seconds_per_request=_dec(decision_compute),
        gpu_seconds_per_request_exact=str(decision_compute),
        input_tokens_per_gpu_second=_dec(F(input_tokens) / decision_compute, 1),
        usd_per_request=_dec(usd(decision_compute), 9),
        usd_per_million_input_tokens=_dec(usd(decision_compute) / input_tokens * 10**6, 4))

    # Decision path on V4.1 Flash: the CED forward and, for contrast, the full-layer path.
    v41 = {}
    for execution in ('ced', 'reference'):
        result = v41_forward.calculate(batch=1, tokens=input_tokens, history=0, execution=execution,
                                       index_algorithm='candidate' if execution == 'ced' else None)
        flops = result['summary']['matrix_flops']
        seconds = F(flops) / compute
        v41[execution] = dict(matrix_flops=flops, gpu_seconds_per_request=_dec(seconds),
                              gpu_seconds_per_request_exact=str(seconds),
                              usd_per_request=_dec(usd(seconds), 9),
                              usd_per_million_input_tokens=_dec(usd(seconds) / input_tokens * 10**6, 4),
                              checkpoint_file_bytes=result['checkpoint']['checkpoint_file_bytes'])
    v41_ratio = F(v41['ced']['matrix_flops'], decision_flops)

    # LLM path on the dense model: same prefill, then serial decode steps.
    llm = []
    for total in output_tokens:
        steps = total - 1
        history = input_tokens + steps // 2
        single = forward(DECISION_MODEL, Scenario(batch=1, history=history, tokens=1))['summary']
        batched = forward(DECISION_MODEL, Scenario(batch=decode_batch, history=history, tokens=1))['summary']

        def step_seconds(summary, batch):
            c = F(summary['matrix_flops']) / compute
            m = F(summary['weight_read_once_per_operator_bytes'] + summary['kv_attention_unique_payload_bytes']) / bandwidth
            return max(c, m), ('compute' if c >= m else 'memory')

        single_step, single_bound = step_seconds(single, 1)
        batched_step, batched_bound = step_seconds(batched, decode_batch)
        latency = decision_latency + steps * single_step
        gpu_seconds = decision_compute + steps * batched_step / decode_batch
        llm.append(dict(
            output_tokens=total, decode_steps=steps, average_history_tokens=history,
            step_seconds_batch_1=_dec(single_step), step_bound_batch_1=single_bound,
            step_seconds_batch=_dec(batched_step), step_bound_batch=batched_bound,
            step_read_bytes_batch=batched['weight_read_once_per_operator_bytes'] + batched['kv_attention_unique_payload_bytes'],
            latency_seconds=_dec(latency, 3), gpu_seconds_per_request=_dec(gpu_seconds),
            gpu_seconds_per_request_exact=str(gpu_seconds),
            gpu_seconds_ratio_to_decision=_dec(gpu_seconds / decision_compute, 2),
            latency_ratio_to_decision=_dec(latency / decision_latency, 1),
            usd_per_request=_dec(usd(gpu_seconds), 9)))

    # Published prices for the same token counts.
    jev_usd_per_request = jev_price * input_tokens
    ds = declared['deepseek_v41_flash_cny_per_million']
    list_prices = {}
    for period in ('off_peak', 'peak'):
        miss = exact_rate(ds[period]['input_cache_miss'], 'miss') / 10**6
        out = exact_rate(ds[period]['output'], 'out') / 10**6
        decision_cny = miss * input_tokens + out * questions
        list_prices[period] = dict(
            decision_request_cny=_dec(decision_cny, 7), decision_request_usd=_dec(decision_cny / fx, 7),
            decision_input_usd_per_million=_dec(miss / fx * 10**6, 4),
            llm_requests=[dict(output_tokens=t, cny=_dec(miss * input_tokens + out * t, 7),
                               usd=_dec((miss * input_tokens + out * t) / fx, 7)) for t in output_tokens])
    demo_llm_usd = exact_rate(declared['demo']['llm_usd'], 'demo llm usd')
    off_peak_llm = [F(str(row['usd'])) for row in list_prices['off_peak']['llm_requests']]

    prices = dict(
        jev_usd_per_million_input_tokens=str(jev_price * 10**6),
        jev_usd_per_request=_dec(jev_usd_per_request, 9),
        jev_price_over_dense_floor=_dec(jev_usd_per_request / usd(decision_compute), 2),
        jev_price_over_v41_ced_floor=_dec(jev_usd_per_request / usd(F(v41['ced']['gpu_seconds_per_request_exact'])), 2),
        demo=dict(jev_usd=str(demo_jev_usd), llm_usd=str(demo_llm_usd),
                  jev_seconds=declared['demo']['jev_seconds'], llm_seconds=declared['demo']['llm_seconds'],
                  cost_ratio=_dec(demo_llm_usd / demo_jev_usd, 1),
                  latency_ratio=_dec(F(declared['demo']['llm_seconds']) / F(declared['demo']['jev_seconds']), 1)),
        deepseek_v41_flash_list=list_prices,
        escalation_share_doubling_cost=dict(
            to_demo_llm=_dec(jev_usd_per_request / demo_llm_usd, 5),
            to_v41_flash_off_peak=[dict(output_tokens=t, share=_dec(jev_usd_per_request / c, 4))
                                   for t, c in zip(output_tokens, off_peak_llm)]))

    return dict(
        schema_version=1, calculation='decision-request',
        scenario=dict(input_tokens=input_tokens, questions=questions, output_tokens=list(output_tokens),
                      decode_batch=decode_batch, device=device, device_name=dev['name'],
                      compute_efficiency=str(eta_c), bandwidth_efficiency=str(eta_b), cny_per_usd=str(fx),
                      usd_per_gpu_hour=declared['gpu_leasing']['usd_per_gpu_hour'],
                      peak_tera_ops_per_second=peak['tera_ops_per_second'],
                      memory_bandwidth_bytes_per_second=dev['memory']['bandwidth_bytes_per_second'],
                      derived_input_tokens_exact=str(derived_tokens)),
        decision_path_dense=decision,
        decision_path_v41_flash=dict(model=V41_MODEL, ced=v41['ced'], reference=v41['reference'],
                                     ced_flops_over_dense=_dec(v41_ratio, 3)),
        llm_path_dense=llm,
        prices=prices,
        summary=dict(
            input_tokens=input_tokens,
            decision_gpu_seconds=decision['gpu_seconds_per_request'],
            decision_latency_seconds=decision['latency_seconds'],
            decision_usd_per_million_input_tokens=decision['usd_per_million_input_tokens'],
            v41_ced_usd_per_million_input_tokens=v41['ced']['usd_per_million_input_tokens'],
            jev_usd_per_request=prices['jev_usd_per_request'],
            jev_price_over_dense_floor=prices['jev_price_over_dense_floor'],
            jev_price_over_v41_ced_floor=prices['jev_price_over_v41_ced_floor'],
            llm_gpu_seconds=[row['gpu_seconds_per_request'] for row in llm],
            llm_latency_seconds=[row['latency_seconds'] for row in llm],
            escalation_share_doubling_cost_to_demo_llm=prices['escalation_share_doubling_cost']['to_demo_llm']),
        sources=[{k: r[k] for k in ('file', 'url', 'revision', 'sha256')} for r in lock['files']]
        + [{k: r[k] for k in ('file', 'url', 'revision', 'sha256')}
           for r in hardware.records() if r.get('id') in dev['source_ids']]
        + provenance(DECISION_MODEL) + provenance(V41_MODEL),
        declared=declared,
        assumptions=[
            '一次决策请求＝状态加全部问题的一次前向；每个问题的答案是该问题末位置的输出分布，不生成 token，也不保留 KV。输入 token 数由演示公布的费用除以定价得到。',
            'GPU 秒按算力下界分摊：prefill 受算力限制，同批多条请求不改变每条的算力份额；单请求延迟取算力与读取时间中的较大者。V4.1 Flash 只给出算力份额，其权重需要多卡专家并行放置，不给出单卡延迟。',
            'LLM 路径的 decode 每步时间取算力与读取时间中的较大者，历史长度取生成中点；单请求延迟按 batch 1，GPU 秒按 decode_batch 分摊。',
            '租赁价取 DeepSeek 推理系统报告的 H800 每 GPU 小时 2 美元；H800 与 H100 SXM 的 BF16 稠密峰值相同（第 3.6.2 节）。人民币价格按声明的汇率换算，仅用于与定价比较。',
            '算力效率取 Llama 3 在 H100 上报告的 BF16 MFU 区间的 40%（第 3.6.1 节），带宽效率取第 8.6.3 节校准的 50%；两者都是输入，不是对 Jev 服务的测量。',
        ])
