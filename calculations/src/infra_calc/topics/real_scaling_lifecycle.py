"""Conditional lifecycle proxy from the live public real C4 fit, not hardware cost."""

from . import real_scaling_fit
from .scaling_law import lifecycle, _finite_api
from ..units import positive_int, positive_number
from .. import hardware


@_finite_api
def calculate(
    target_loss=2.9,
    candidate_sizes=(1e8, 5e8, 1e9, 2.81e9),
    calls=(0, 1000, 1000000, 1000000000),
    input_tokens=512,
    returned_tokens=128,
    cost_per_proxy_flop=1e-18,
    cost_device=None,
    cost_mfu=None,
):
    positive_number(target_loss, "target_loss")
    positive_int(input_tokens, "input_tokens", allow_zero=True)
    positive_int(returned_tokens, "returned_tokens")
    positive_number(cost_per_proxy_flop, "cost_per_proxy_flop")
    device_basis = None
    if cost_device is not None or cost_mfu is not None:
        # Price every proxy FLOP as time on one named device at a declared MFU.
        if cost_device is None or cost_mfu is None:
            raise ValueError("cost_device and cost_mfu must be given together")
        positive_number(cost_mfu, "cost_mfu")
        if cost_mfu > 1:
            raise ValueError("cost_mfu must not exceed 1")
        profile = hardware.select_device(cost_device)
        peak = hardware.select_peak(profile, "BF16", "FP32", "tensor", "dense")
        cost_per_proxy_flop = 1 / (float(peak["tera_ops_per_second"]) * 1e12 * cost_mfu)
        device_basis = dict(
            device=cost_device,
            name=profile["name"],
            bf16_dense_tera_flops_per_second=peak["tera_ops_per_second"],
            mfu=cost_mfu,
            unit="GPU-seconds",
        )
    if not isinstance(candidate_sizes, (list, tuple)) or not candidate_sizes:
        raise ValueError("candidate_sizes must be a nonempty sequence")
    for size in candidate_sizes:
        positive_number(size, "candidate size")
    if len(set(candidate_sizes)) != len(candidate_sizes):
        raise ValueError("candidate sizes must be unique")
    if not isinstance(calls, (list, tuple)) or not calls:
        raise ValueError("calls must be a nonempty sequence")
    for count in calls:
        positive_int(count, "calls", allow_zero=True)
    scenario = dict(
        target_loss=target_loss,
        candidate_sizes=list(candidate_sizes),
        calls=list(calls),
        input_tokens=input_tokens,
        returned_tokens=returned_tokens,
        cost_per_proxy_flop=cost_per_proxy_flop,
    )
    if device_basis is not None:
        scenario.update(cost_device=cost_device, cost_mfu=cost_mfu)
    fitted = real_scaling_fit.calculate()
    if scenario["returned_tokens"] < 1:
        raise ValueError("At least one returned token required")
    rate = scenario["cost_per_proxy_flop"]
    costs = dict(
        train_per_flop=rate,
        prefill_per_flop=rate,
        decode_per_flop=rate,
        setup_cost=0,
        prefill_flops_per_parameter_token=2,
        decode_flops_per_parameter_token=2,
    )
    demand = dict(
        calls_per_day=0,
        lifetime_days=1,
        input_tokens=scenario["input_tokens"],
        output_tokens=scenario["returned_tokens"] - 1,
    )
    fits = dict(primary=fitted["primary"], **fitted["sensitivity"])
    results = []
    for name, fit in fits.items():
        if fit["status"] != "fit":
            results.append(dict(variant=name, status=fit["status"], result=None))
            continue
        law = fit["result"]["law"]
        bounds = fit["result"]["fit_bounds"]
        result = lifecycle(
            law, scenario["candidate_sizes"], scenario["target_loss"], demand, costs
        )
        for row in result["rows"]:
            if row["feasible"]:
                row["outside_fit_box"] = any(
                    not bounds[key][0] <= row[key] <= bounds[key][1]
                    for key in ("N", "D")
                )
                row["extrapolation_factors"] = {
                    key: max(1, bounds[key][0] / row[key], row[key] / bounds[key][1])
                    for key in ("N", "D")
                }
        curves = []
        for calls in scenario["calls"]:
            feasible = [row for row in result["rows"] if row["feasible"]]
            values = [
                dict(
                    N=row["N"],
                    total_cost_units=row["upfront_cost"] + calls * row["cost_per_call"],
                )
                for row in feasible
            ]
            curves.append(
                dict(
                    calls=calls,
                    values=values,
                    minimizing_candidate_N=(
                        min(values, key=lambda x: x["total_cost_units"])["N"]
                        if values
                        else None
                    ),
                )
            )
        # Equality is independently checked from the two affine cost lines.
        crossing_checks = []
        for cross in result["crossovers"]:
            if cross["calls"] is None:
                continue
            left = next(row for row in result["rows"] if row["N"] == cross["left_N"])
            right = next(row for row in result["rows"] if row["N"] == cross["right_N"])
            lcost = left["upfront_cost"] + cross["calls"] * left["cost_per_call"]
            rcost = right["upfront_cost"] + cross["calls"] * right["cost_per_call"]
            relative_error = abs(lcost - rcost) / max(1, abs(lcost), abs(rcost))
            if relative_error > 1e-12:
                raise ValueError("Crossover equality failed")
            crossing_checks.append(
                dict(cross, relative_cost_equality_error=relative_error)
            )
        results.append(
            dict(
                variant=name,
                status="conditional_proxy",
                law=law,
                fit_bounds=bounds,
                lifecycle=result,
                curves=curves,
                crossing_checks=crossing_checks,
            )
        )
    if device_basis is None:
        cost_scope = f"All costs use the same declared {rate:g} abstract cost units per proxy FLOP, not currency, official hardware price, or measured efficiency."
    else:
        cost_scope = (
            f"All costs are {device_basis['name']} GPU-seconds: {rate:.9g} GPU-s per proxy FLOP = "
            f"1/({device_basis['bf16_dense_tera_flops_per_second']} TFLOP/s BF16 dense peak x MFU {cost_mfu:g}); "
            "the same MFU is applied to training and serving, and MFU is a declared input rather than measured here."
        )
    extra = dict(cost_basis=device_basis) if device_basis is not None else {}
    return dict(
        calculation="real-scaling-lifetime-proxy",
        scenario=scenario,
        **extra,
        fit_source=dict(calculation=fitted["calculation"], sources=fitted["sources"]),
        sources=fitted["sources"],
        work_convention=dict(
            input_phase_tokens=input_tokens,
            returned_tokens=returned_tokens,
            additional_decode_steps=returned_tokens - 1,
        ),
        variants=results,
        scope=[
            "The fitted real C4 loss is a proxy target, not demonstrated equal task quality or a trained candidate architecture.",
            cost_scope,
            "Training is 6ND. Input work is 2NP; additional decode is 2N(G-1), because the first output comes from the input phase. Attention, KV, sampling, actual heads and communication are not modeled.",
            "Every candidate reports its N/D fit-box extrapolation. Formula feasibility does not establish a realizable data budget or reliable prediction.",
            "Primary and four prespecified sensitivities are shown separately; held-out error does not select a cheaper law.",
            "Setup is explicitly zero for this scenario; changing assumptions requires rerunning inputs. No deployment recommendation or universal optimum follows.",
        ],
    )


def markdown(result):
    scenario = result["scenario"]
    basis = result.get("cost_basis")
    if basis is None:
        unit_text = f"使用 {scenario['cost_per_proxy_flop']:g} 抽象 cost-unit/FLOP"
    else:
        unit_text = (
            f"按 {basis['name']} GPU 秒计价：每 FLOP {scenario['cost_per_proxy_flop']:.9g} GPU 秒，"
            f"即 1/({basis['bf16_dense_tera_flops_per_second']} TFLOP/s BF16 dense 峰值 × MFU {basis['mfu']:g})，"
            "费用列单位均为 GPU 秒"
        )
    lines = [
        "# 真实 C4 拟合的条件生命周期代理",
        "",
        f"目标 loss {scenario['target_loss']}；输入 {scenario['input_tokens']} token，返回 {scenario['returned_tokens']} token，额外 decode {scenario['returned_tokens']-1} 步。训练、prefill、decode 均{unit_text}，setup=0。",
        "",
        "费用直线为 T(C)=6ND·r+C·2N[P+(G−1)]·r。它是声明的运算量代理，不是完整硬件费用、吞吐实测或等任务质量证明。",
        "",
    ]
    for variant in result["variants"]:
        lines += [f"## {variant['variant']}", ""]
        if variant["status"] != "conditional_proxy":
            lines.append(variant["status"])
            continue
        law = variant["law"]
        lines += [
            f"拟合 E={law['E']:.10g}, A={law['A']:.10g}, B={law['B']:.10g}, α={law['alpha']}, β={law['beta']}。",
            "",
            "| N | 可行 | 目标 D | 训练代理 FLOPs | 每调用代理费用 | 超出 N/D 拟合框 |",
            "|---:|---|---:|---:|---:|---|",
        ]
        for row in variant["lifecycle"]["rows"]:
            if not row["feasible"]:
                lines.append(
                    f"| {row['N']:g} | False | unavailable | unavailable | unavailable | unavailable |"
                )
                continue
            lines.append(
                f"| {row['N']:g} | True | {row['D']:.9g} | {row['training_proxy_flops']:.9g} | {row['cost_per_call']:.9g} | {row['outside_fit_box']} (N×{row['extrapolation_factors']['N']:.4g}, D×{row['extrapolation_factors']['D']:.4g}) |"
            )
        lines += [
            "",
            "| 两个 N | 交叉调用数 | 状态 | 代回相对误差 |",
            "|---|---:|---|---:|",
        ]
        errors = {
            (x["left_N"], x["right_N"]): x["relative_cost_equality_error"]
            for x in variant["crossing_checks"]
        }
        for cross in variant["lifecycle"]["crossovers"]:
            lines.append(
                f"| {cross['left_N']:g} / {cross['right_N']:g} | {cross['calls'] if cross['calls'] is not None else 'none'} | {cross['status']} | {errors.get((cross['left_N'],cross['right_N']),'not applicable')} |"
            )
        lines += [
            "",
            "| 调用数 | N | 总代理费用 | 该有限候选集合最小 N |",
            "|---:|---:|---:|---:|",
        ]
        for curve in variant["curves"]:
            for row in curve["values"]:
                lines.append(
                    f"| {curve['calls']} | {row['N']:g} | {row['total_cost_units']:.9g} | {curve['minimizing_candidate_N']:g} |"
                )
        lines.append("")
    lines += ["## 范围与来源", ""] + ["- " + x for x in result["scope"]]
    lines += [
        "",
        "训练点与来源随公共 real_scaling_fit.calculate() 实时校验和复算；下列 SHA 绑定所用数据原件。",
        "",
        "| 文件 | SHA256 |",
        "|---|---|",
    ]
    for source in result["sources"]:
        lines.append(f"| {source['file']} | {source['sha256']} |")
    return "\n".join(lines) + "\n"
