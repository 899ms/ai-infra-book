"""Derive per-device prefill and decode service rates from locked hardware peaks.

One worker is one device running the full model. Prefill time is the Roofline
lower bound of the whole prompt forward; decode step time is the Roofline lower
bound of one batched step at the average history length. Both use declared
efficiency factors applied to the official peak rates recorded in hardware.json.
"""
from fractions import Fraction as F
from .. import hardware
from ..models import qwen3
from ..schema import Scenario
from ..sources import provenance
from ..units import positive_int, positive_number


def _exact(value, name):
    positive_number(value, name)
    return F(str(value))


def device_rates(model='qwen3-8b', device='a100-80gb-sxm', prompt_tokens=8192, output_tokens=1025,
                 cached_prefix_tokens=0, decode_batch=32, compute_efficiency=0.5,
                 bandwidth_efficiency=0.5, precision='BF16', accumulator='FP32'):
    for name, value in [('prompt_tokens', prompt_tokens), ('output_tokens', output_tokens),
                        ('decode_batch', decode_batch)]:
        positive_int(value, name)
    positive_int(cached_prefix_tokens, 'cached_prefix_tokens', allow_zero=True)
    if cached_prefix_tokens >= prompt_tokens:
        raise ValueError('At least one uncached prefill token is required')
    eta_c = _exact(compute_efficiency, 'compute_efficiency')
    eta_b = _exact(bandwidth_efficiency, 'bandwidth_efficiency')
    if eta_c > 1 or eta_b > 1:
        raise ValueError('Efficiency factors must not exceed 1')
    dev = hardware.select_device(device)
    peak = hardware.select_peak(dev, precision, accumulator, 'tensor', 'dense')
    if dev['memory']['bandwidth_bytes_per_second'] is None:
        raise ValueError(f'No verified memory bandwidth for {device}')
    compute = F(str(peak['tera_ops_per_second'])) * 10**12 * eta_c
    bandwidth = F(str(dev['memory']['bandwidth_bytes_per_second'])) * eta_b
    capacity = int(dev['memory']['nominal_capacity']) * 10**9
    new_tokens = prompt_tokens - cached_prefix_tokens
    decode_calls = output_tokens - 1
    # Prefill: one request, cached prefix already resident, new tokens processed in one forward.
    pre = qwen3.calculate(model, Scenario(batch=1, history=cached_prefix_tokens, tokens=new_tokens))['summary']
    prefill_compute = F(pre['matrix_flops']) / compute
    prefill_memory = F(pre['weight_read_once_per_operator_bytes'] + pre['kv_existing_history_unique_payload_bytes']) / bandwidth
    prefill_seconds = max(prefill_compute, prefill_memory)
    # Decode: one batched step at the average history over the generation.
    history = prompt_tokens + decode_calls // 2
    step = qwen3.calculate(model, Scenario(batch=decode_batch, history=history, tokens=1))['summary'] if decode_calls else None
    if step:
        step_compute = F(step['matrix_flops']) / compute
        step_memory = F(step['weight_read_once_per_operator_bytes'] + step['kv_attention_unique_payload_bytes']) / bandwidth
        step_seconds = max(step_compute, step_memory)
        decode_rate = F(decode_batch) / step_seconds
        decode_seconds = F(decode_calls) / decode_rate
        final_kv = decode_batch * (prompt_tokens + decode_calls) * step['kv_bytes_per_token_per_request']
        resident = step['weight_resident_bytes'] + final_kv
    else:
        step_compute = step_memory = step_seconds = decode_rate = decode_seconds = None
        resident = pre['weight_resident_bytes']
    return dict(
        device=device, device_name=dev['name'], model=model,
        peak_tera_ops_per_second=peak['tera_ops_per_second'],
        memory_bandwidth_bytes_per_second=dev['memory']['bandwidth_bytes_per_second'],
        nominal_capacity_bytes=capacity,
        effective_flops_per_second_exact=str(compute), effective_bytes_per_second_exact=str(bandwidth),
        prefill=dict(new_tokens=new_tokens, matrix_flops=pre['matrix_flops'],
                     weight_bytes=pre['weight_read_once_per_operator_bytes'],
                     compute_seconds_exact=str(prefill_compute), memory_seconds_exact=str(prefill_memory),
                     seconds_exact=str(prefill_seconds),
                     bound='compute' if prefill_compute >= prefill_memory else 'memory',
                     tokens_per_second_exact=str(F(new_tokens) / prefill_seconds)),
        decode=None if not step else dict(
            batch=decode_batch, average_history_tokens=history, calls_per_request=decode_calls,
            step_matrix_flops=step['matrix_flops'], step_weight_bytes=step['weight_read_once_per_operator_bytes'],
            step_kv_bytes=step['kv_attention_unique_payload_bytes'],
            step_compute_seconds_exact=str(step_compute), step_memory_seconds_exact=str(step_memory),
            step_seconds_exact=str(step_seconds),
            bound='compute' if step_compute >= step_memory else 'memory',
            calls_per_second_exact=str(decode_rate), seconds_per_request_exact=str(decode_seconds)),
        resident_bytes_at_full_batch=resident, fits_nominal_capacity=resident <= capacity,
        colocated_seconds_per_request_exact=str(prefill_seconds + (decode_seconds or 0)),
        sources=[{k: r[k] for k in ('file', 'url', 'revision', 'sha256')}
                 for r in hardware.records() if r.get('id') in dev['source_ids']] + provenance(model))


def worker_from_device(spec: dict, model, prompt_tokens, output_tokens, cached_prefix_tokens):
    """Turn a device-form worker into the exact stage-rate form pd_pool consumes."""
    keys = {'name', 'count', 'device', 'decode_batch', 'compute_efficiency', 'bandwidth_efficiency'}
    if set(spec) != keys:
        raise ValueError(f'Device worker requires exactly {sorted(keys)}')
    rates = device_rates(model=model, device=spec['device'], prompt_tokens=prompt_tokens,
                         output_tokens=output_tokens, cached_prefix_tokens=cached_prefix_tokens,
                         decode_batch=spec['decode_batch'], compute_efficiency=spec['compute_efficiency'],
                         bandwidth_efficiency=spec['bandwidth_efficiency'])
    worker = dict(name=spec['name'], count=spec['count'],
                  prefill_tokens_per_second=rates['prefill']['tokens_per_second_exact'],
                  decode_tokens_per_second=rates['decode']['calls_per_second_exact'] if rates['decode'] else '1')
    return worker, rates
