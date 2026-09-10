"""C74: two sides tuned independently under one shared cap (9.6.2).

Comparing two fixed configurations answers a different question from comparing
two well-tuned sides. This module does both: it prices the pair of defaults, it
then lets each side choose its own storage width, tensor-parallel degree and
replica count under one shared power cap, and it reports where the two answers
disagree and what price ratio flips the ranking.

Device rates, capacity and power are published catalog figures; a precision a
vendor does not publish a rate for is refused rather than assumed. Model work
comes from the pinned official config. Prices are declared inputs, and a storage
width that changes numerics is ranked only where quality evidence is declared.
"""
from fractions import Fraction
from functools import lru_cache
import json

from .. import hardware
from ..models import forward as model_forward
from ..schema import Scenario
from ..sources import provenance
from ..units import positive_int
from . import ring_collective
from .weight_resident_traffic import geometry

PRECISIONS = {"BF16": 2, "FP8": 1}
TP_DEGREES = (1, 2, 4, 8)


def fraction(value: Fraction) -> dict:
    return {"numerator": value.numerator, "denominator": value.denominator}


def exact(value) -> Fraction:
    return Fraction(str(value))


@lru_cache(maxsize=None)
def step_work(model: str, batch: int, context: int) -> dict:
    """Matrix work and interface traffic for one decode step, from the config."""
    summary = model_forward(model, Scenario(history=context, tokens=1, batch=batch))["summary"]
    shape = geometry(model)
    return {"matrix_flops": summary["matrix_flops"],
            "weight_read_bytes": shape["active_decode_read_bytes"],
            "state_read_bytes": batch * shape["kv_bytes_per_token"] * context,
            "params_active": shape["params_active_decode"],
            "kv_bytes_per_token": shape["kv_bytes_per_token"],
            "kv_heads": shape["num_key_value_heads"]}


@lru_cache(maxsize=None)
def collective_seconds(model: str, batch: int, participants: int,
                       link_bytes_per_second: int) -> Fraction:
    """Serial tensor-parallel all-reduce time for one decode step."""
    ring = ring_collective.calculate(model=model, batch=batch, tokens=1,
                                     participants=participants,
                                     bandwidth_bytes_per_second=link_bytes_per_second)
    return exact(ring["summary"]["dense_tp_serial_collective_seconds"])


def published_peak(device: dict, precision: str):
    """Published dense tensor rate, or None when the vendor does not publish one."""
    try:
        row = hardware.select_peak(device, precision, "FP32", "tensor", "dense")
    except (ValueError, KeyError, StopIteration):
        return None
    rate = row.get("tera_ops_per_second")
    if not rate:
        return None
    return {"tera_ops_per_second": rate, "source_id": row.get("source_id"),
            "locator": row.get("locator"), "clock_basis": row.get("clock_basis")}


def configuration(model: str, device_id: str, precision: str, tensor_parallel: int,
                  batch: int, context: int, power_cap_watts: int,
                  link_bytes_per_second: int, price_per_device_hour: Fraction,
                  quality_evidence: dict) -> dict:
    """One side's candidate: a storage width, a split, and the replicas that fit."""
    device = hardware.select_device(device_id)
    row = {"device": device_id, "precision": precision, "tensor_parallel": tensor_parallel,
           "batch": batch, "context": context}
    peak = published_peak(device, precision)
    power = device.get("power_watts")
    if peak is None:
        return dict(row, admissible=False, reason=f"{device_id} publishes no dense {precision} tensor rate")
    if power is None:
        return dict(row, admissible=False, reason=f"{device_id} publishes no board power")

    work = step_work(model, batch, context)
    width = PRECISIONS[precision]
    weight_bytes = work["params_active"] * width
    # Session state stays at BF16 whatever the weight width. Tensor parallelism
    # splits it by key/value head, so it stops dividing past that head count.
    state_bytes = work["state_read_bytes"]
    state_shards = min(tensor_parallel, work["kv_heads"])
    if tensor_parallel % state_shards:
        return dict(row, admissible=False,
                    reason=f"tp{tensor_parallel} does not divide {work['kv_heads']} key/value heads")
    per_device_bytes = weight_bytes // tensor_parallel + state_bytes // state_shards
    memory = device["memory"]
    if memory["capacity_unit"] not in ("GB", "GiB"):
        return dict(row, admissible=False, reason="Unsupported memory capacity unit")
    scale = 10 ** 9 if memory["capacity_unit"] == "GB" else 2 ** 30
    capacity = memory["nominal_capacity"] * scale
    if per_device_bytes > capacity:
        return dict(row, admissible=False, per_device_bytes=per_device_bytes,
                    reason=f"needs {per_device_bytes} B per device against {capacity} B")

    replicas = power_cap_watts // (tensor_parallel * power)
    if replicas < 1:
        return dict(row, admissible=False,
                    reason=f"one replica needs {tensor_parallel * power} W against a {power_cap_watts} W cap")

    flops_rate = Fraction(int(peak["tera_ops_per_second"] * 10), 10) * 10 ** 12
    compute = Fraction(work["matrix_flops"], tensor_parallel) / flops_rate
    bandwidth = Fraction(str(memory["bandwidth_bytes_per_second"]))
    memory_seconds = (Fraction(weight_bytes, tensor_parallel)
                      + Fraction(state_bytes, state_shards)) / bandwidth
    collective = (collective_seconds(model, batch, tensor_parallel, link_bytes_per_second)
                  if tensor_parallel > 1 else Fraction(0))
    latency = max(compute, memory_seconds) + collective
    devices = tensor_parallel * replicas
    throughput = Fraction(replicas * batch) / latency
    cost = Fraction(devices) * price_per_device_hour / 3600 / throughput
    evidence = bool(quality_evidence.get(precision))
    return dict(row, admissible=True, reason="within capacity, power and published rates",
                peak=peak, power_watts=power, replicas=replicas, devices=devices,
                per_device_bytes=per_device_bytes, device_capacity_bytes=capacity,
                state_shards=state_shards,
                compute_seconds=fraction(compute), memory_seconds=fraction(memory_seconds),
                collective_seconds=fraction(collective),
                limiting_resource="compute" if compute >= memory_seconds else "memory",
                latency_seconds=fraction(latency),
                throughput_tokens_per_second=fraction(throughput),
                cost_per_token=fraction(cost),
                changes_numerics=width != PRECISIONS["BF16"],
                quality_evidence_declared=evidence,
                rankable_at_fixed_quality=(width == PRECISIONS["BF16"]) or evidence)


def side(model: str, device_id: str, batch: int, context: int, power_cap_watts: int,
         link_bytes_per_second: int, price_per_device_hour: Fraction,
         quality_evidence: dict, slo_seconds: Fraction) -> dict:
    """Every candidate one side can build, and its best under each objective."""
    rows = [configuration(model, device_id, precision, tp, batch, context, power_cap_watts,
                          link_bytes_per_second, price_per_device_hour, quality_evidence)
            for precision in PRECISIONS for tp in TP_DEGREES]
    usable = [row for row in rows if row["admissible"] and row["rankable_at_fixed_quality"]]
    within = [row for row in usable if Fraction(**row["latency_seconds"]) <= slo_seconds]

    def label(row):
        return f"{row['precision']}/tp{row['tensor_parallel']}"

    return {
        "device": device_id, "candidates": rows,
        "admissible": [label(row) for row in rows if row["admissible"]],
        "refused": [{"candidate": label(row), "reason": row["reason"]}
                    for row in rows if not row["admissible"]],
        "excluded_for_quality": [label(row) for row in rows
                                 if row["admissible"] and not row["rankable_at_fixed_quality"]],
        "lowest_latency": (min(usable, key=lambda row: Fraction(**row["latency_seconds"]))
                           if usable else None),
        "highest_throughput_within_slo": (max(within, key=lambda row: Fraction(**row["throughput_tokens_per_second"]))
                                          if within else None),
        "lowest_cost_per_token": (min(usable, key=lambda row: Fraction(**row["cost_per_token"]))
                                  if usable else None),
        "meets_slo": bool(within),
    }


def head_to_head(left: dict, right: dict) -> list:
    """Which tuned side wins each objective, and by how much."""
    objectives = (("lowest_latency", "latency_seconds", False),
                  ("highest_throughput_within_slo", "throughput_tokens_per_second", True),
                  ("lowest_cost_per_token", "cost_per_token", False))
    rows = []
    for name, key, largest in objectives:
        a, b = left[name], right[name]
        if a is None or b is None:
            rows.append({"objective": name, "winner": None,
                         "reason": "at least one side has no admissible configuration here"})
            continue
        first, second = Fraction(**a[key]), Fraction(**b[key])
        winner = left if (first > second) == largest else right
        loser = right if winner is left else left
        ratio = (max(first, second) / min(first, second)) if min(first, second) else None
        rows.append({"objective": name, "winner": winner["device"], "loser": loser["device"],
                     "winning_configuration": f"{winner[name]['precision']}/tp{winner[name]['tensor_parallel']}",
                     "losing_configuration": f"{loser[name]['precision']}/tp{loser[name]['tensor_parallel']}",
                     "winner_value": winner[name][key], "loser_value": loser[name][key],
                     "ratio": None if ratio is None else fraction(ratio)})
    return rows


def price_flip(left: dict, right: dict) -> dict:
    """Price ratio at which the cheaper side stops being the cheaper side.

    Cost per token is linear in the price, so scaling one side's price scales
    its cost directly and the crossing is one division.
    """
    a, b = left["lowest_cost_per_token"], right["lowest_cost_per_token"]
    if a is None or b is None:
        return {"ratio": None, "reason": "one side has no admissible configuration to price"}
    first, second = Fraction(**a["cost_per_token"]), Fraction(**b["cost_per_token"])
    if first == second:
        return {"ratio": None, "reason": "the two sides already cost the same per token"}
    cheaper, dearer = ((left, right) if first < second else (right, left))
    ratio = max(first, second) / min(first, second)
    return {"cheaper_side": cheaper["device"], "dearer_side": dearer["device"],
            "ratio": fraction(ratio),
            "reason": (f"Multiplying {cheaper['device']}'s declared price by more than this "
                       f"ratio, with everything else held, makes {dearer['device']} the cheaper "
                       "side per token")}


def evidence_sensitivity(model: str, left_device: str, right_device: str, batch: int,
                         context: int, power_cap_watts: int, link_bytes_per_second: int,
                         prices: dict, slo: Fraction, evidence: dict) -> dict:
    """Which objectives change winner when a narrower width gains quality evidence.

    Granting evidence never changes a device, a price or a byte count. Anything
    that moves here moved because a width became rankable, which is a statement
    about the evidence and not about the hardware.
    """
    rows = {}
    for name in PRECISIONS:
        if name == "BF16" or evidence.get(name):
            continue
        granted = dict(evidence, **{name: True})
        left = side(model, left_device, batch, context, power_cap_watts,
                    link_bytes_per_second, prices[left_device], granted, slo)
        right = side(model, right_device, batch, context, power_cap_watts,
                     link_bytes_per_second, prices[right_device], granted, slo)
        rows[name] = head_to_head(left, right)
    return rows


def calculate(model: str = "qwen3-8b", left_device: str = "h100-sxm",
              right_device: str = "a100-80gb-sxm",
              batch: int = 32, context: int = 8192,
              power_cap_watts: int = 5600,
              link_bytes_per_second: int = 50_000_000_000,
              left_price_per_device_hour: str = "3.0",
              right_price_per_device_hour: str = "1.5",
              slo_seconds: str = "0.05",
              quality_evidence: dict | None = None,
              fixed_precision: str = "BF16", fixed_tensor_parallel: int = 1) -> dict:
    """Price two fixed configurations, then two independently tuned sides."""
    for name, value in (("batch", batch), ("context", context),
                        ("power_cap_watts", power_cap_watts),
                        ("link_bytes_per_second", link_bytes_per_second),
                        ("fixed_tensor_parallel", fixed_tensor_parallel)):
        positive_int(value, name)
    if fixed_precision not in PRECISIONS:
        raise ValueError("Unknown fixed precision")
    if fixed_tensor_parallel not in TP_DEGREES:
        raise ValueError("Unknown fixed tensor-parallel degree")
    slo = exact(slo_seconds)
    if slo <= 0:
        raise ValueError("slo_seconds must be positive")
    prices = {left_device: exact(left_price_per_device_hour),
              right_device: exact(right_price_per_device_hour)}
    for price in prices.values():
        if price < 0:
            raise ValueError("A declared price cannot be negative")
    evidence = {"BF16": True} if quality_evidence is None else dict(quality_evidence)
    if not evidence.get("BF16"):
        raise ValueError("The baseline storage width needs declared quality evidence")

    fixed = [configuration(model, name, fixed_precision, fixed_tensor_parallel, batch, context,
                           power_cap_watts, link_bytes_per_second, prices[name], evidence)
             for name in (left_device, right_device)]
    fixed_winner = None
    usable_fixed = [row for row in fixed if row["admissible"]]
    if len(usable_fixed) == 2:
        fixed_winner = min(usable_fixed, key=lambda row: Fraction(**row["cost_per_token"]))["device"]

    left = side(model, left_device, batch, context, power_cap_watts, link_bytes_per_second,
                prices[left_device], evidence, slo)
    right = side(model, right_device, batch, context, power_cap_watts, link_bytes_per_second,
                 prices[right_device], evidence, slo)
    comparison = head_to_head(left, right)
    tuned_cost = next(row for row in comparison if row["objective"] == "lowest_cost_per_token")
    sensitivity = evidence_sensitivity(model, left_device, right_device, batch, context,
                                       power_cap_watts, link_bytes_per_second, prices,
                                       slo, evidence)
    baseline_winners = {row["objective"]: row["winner"] for row in comparison}
    flips = []
    for precision, rows in sensitivity.items():
        for row in rows:
            if row["winner"] is not None and row["winner"] != baseline_winners.get(row["objective"]):
                flips.append({"precision_granted_evidence": precision,
                              "objective": row["objective"],
                              "winner_without_evidence": baseline_winners.get(row["objective"]),
                              "winner_with_evidence": row["winner"],
                              "winning_configuration": row["winning_configuration"]})

    return {
        "calculation": "iso-resource-two-sided-comparison",
        "inputs": {"model": model, "left_device": left_device, "right_device": right_device,
                   "batch": batch, "context": context, "power_cap_watts": power_cap_watts,
                   "link_bytes_per_second": link_bytes_per_second,
                   "left_price_per_device_hour": left_price_per_device_hour,
                   "right_price_per_device_hour": right_price_per_device_hour,
                   "slo_seconds": slo_seconds,
                   "quality_evidence": evidence,
                   "fixed_precision": fixed_precision,
                   "fixed_tensor_parallel": fixed_tensor_parallel},
        "sources": provenance(model),
        "shared_cap": {"power_cap_watts": power_cap_watts,
                       "note": ("One cap, spent as each side likes. It does not require every "
                                "device to sit in one synchronous domain, so replicas are allowed.")},
        "fixed_configuration_comparison": {
            "configuration": f"{fixed_precision}/tp{fixed_tensor_parallel}",
            "rows": fixed, "cheaper_side": fixed_winner},
        "left": left, "right": right,
        "head_to_head": comparison,
        "price_flip": price_flip(left, right),
        "quality_evidence_sensitivity": sensitivity,
        "objectives_that_flip_on_quality_evidence": flips,
        "fixed_and_tuned_disagree": (fixed_winner is not None
                                     and tuned_cost["winner"] is not None
                                     and fixed_winner != tuned_cost["winner"]),
        "assumptions": [
            "Device capacity, bandwidth, board power and tensor rates are published catalog figures with locators.",
            "A precision the vendor publishes no dense rate for is refused, never assumed to run at the next width's rate.",
            "Model work comes from the pinned official config; the step is one decode position behind the stated context.",
            "Latency is max(compute, memory) plus the serial collective, an ideal-overlap lower bound rather than a measured latency.",
            "Tensor-parallel compute and capacity are assumed to divide evenly, which no implementation achieves exactly.",
            "Session state stays at BF16 whatever the weight width, so a narrower weight never shrinks the state term.",
            "A width that changes numerics is ranked only where quality evidence is declared; otherwise it is listed and set aside.",
            "Prices are declared teaching inputs, and the flip is reported as a ratio rather than as a market claim.",
        ],
    }


def markdown(result: dict) -> str:
    def number(entry, places=6):
        return "—" if entry is None else f"{float(Fraction(**entry)):.{places}f}"

    def label(row):
        return "—" if row is None else f"{row['precision']}/tp{row['tensor_parallel']}"

    fixed = result["fixed_configuration_comparison"]
    lines = ["# 同上限下的两侧独立选择", "",
             f"共享上限：{result['shared_cap']['power_cap_watts']} W。{result['shared_cap']['note']}", "",
             f"## 先比较两套固定配置（{fixed['configuration']}）", "",
             "| 设备 | 可用 | 副本 | 设备数 | 下界延迟 s | 吞吐 tok/s | 每 token 成本 | 限制资源 |",
             "|---|---|---:|---:|---:|---:|---:|---|"]
    for row in fixed["rows"]:
        if not row["admissible"]:
            lines.append(f"| {row['device']} | 否 | — | — | — | — | — | {row['reason']} |")
            continue
        lines.append("| " + " | ".join([
            row["device"], "是", str(row["replicas"]), str(row["devices"]),
            number(row["latency_seconds"]), f"{float(Fraction(**row['throughput_tokens_per_second'])):.1f}",
            number(row["cost_per_token"], 9), row["limiting_resource"]]) + " |")
    lines.append("")
    lines.append(f"固定配置下更便宜的一侧：{fixed['cheaper_side'] or '无法判定'}。")

    lines += ["", "## 再让两侧各自调优", ""]
    for key in ("left", "right"):
        entry = result[key]
        lines += [f"### {entry['device']}", "",
                  f"- 可用候选：{'、'.join(entry['admissible']) or '无'}",
                  f"- 因质量证据搁置：{'、'.join(entry['excluded_for_quality']) or '无'}",
                  f"- 最低延迟：{label(entry['lowest_latency'])}"
                  f"（{number(entry['lowest_latency']['latency_seconds']) if entry['lowest_latency'] else '—'} s）",
                  f"- SLO 内最高吞吐：{label(entry['highest_throughput_within_slo'])}",
                  f"- 最低每 token 成本：{label(entry['lowest_cost_per_token'])}"
                  f"（{number(entry['lowest_cost_per_token']['cost_per_token'], 9) if entry['lowest_cost_per_token'] else '—'}）", ""]
        if entry["refused"]:
            lines.append("被拒绝的候选：")
            for row in entry["refused"]:
                lines.append(f"- {row['candidate']}：{row['reason']}")
            lines.append("")

    lines += ["## 逐目标对比", "",
              "| 目标 | 胜方 | 胜方配置 | 负方 | 负方配置 | 比值 |", "|---|---|---|---|---|---:|"]
    for row in result["head_to_head"]:
        if row["winner"] is None:
            lines.append(f"| {row['objective']} | — | — | — | — | — |")
            continue
        lines.append("| " + " | ".join([
            row["objective"], row["winner"], row["winning_configuration"],
            row["loser"], row["losing_configuration"],
            f"{float(Fraction(**row['ratio'])):.3f}" if row["ratio"] else "—"]) + " |")

    flip = result["price_flip"]
    lines += ["", "## 翻转条件", "",
              "- 价格比：" + (f"×{float(Fraction(**flip['ratio'])):.3f}" if flip.get("ratio") else "不适用")
              + f"。{flip['reason']}。",
              f"- 固定配置与调优后结论是否不同：{'是' if result['fixed_and_tuned_disagree'] else '否'}。"
              "两套固定配置的比较回答的不是同一个问题。", ""]
    flips = result["objectives_that_flip_on_quality_evidence"]
    lines += ["### 仅因质量证据而翻转的目标", ""]
    if flips:
        lines += ["| 获得证据的位宽 | 目标 | 无证据时胜方 | 有证据时胜方 | 胜方配置 |",
                  "|---|---|---|---|---|"]
        for row in flips:
            lines.append("| " + " | ".join([
                row["precision_granted_evidence"], row["objective"],
                row["winner_without_evidence"] or "—", row["winner_with_evidence"],
                row["winning_configuration"]]) + " |")
        lines += ["", "硬件、价格与字节数都没有变；变的只是某个位宽是否可以参与排名。"]
    else:
        lines += ["本组输入下没有目标因质量证据而改变胜方。"]
    lines += ["",
              "## 口径与限制", ""]
    lines += ["- " + item for item in result["assumptions"]]
    lines += ["", "## 完整输入、来源与结果", "", "```json",
              json.dumps(result, ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lines)
