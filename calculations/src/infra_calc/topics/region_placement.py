"""C71: cross-region placement for one measured Agent session (12.6).

Three placements carry the same task: run it in a remote region that keeps no
prefix cache, run it in a remote region that holds the session warm, or run it
beside the user. All three replay one pinned trace -- same model revision, same
token sequence, same rounds -- so quality is fixed by construction rather than
by a claimed per-placement evaluation.

Every byte is real. Request payloads are the trace's own message bodies, replies
are its output text, and session state is the official config's K/V geometry
times the tokens actually held. Round-trip delay and link capacity come from the
pinned Queqiao path. Prices, power caps and lead times are declared teaching
inputs, and each conclusion is stated as a break-even condition over them rather
than as a claim about what any operator charges.
"""
from fractions import Fraction
from functools import lru_cache
import json

from ..models import forward as model_forward
from ..schema import Scenario
from ..sources import model_config, provenance
from ..units import positive_int, positive_number
from . import agent_trace, queqiao_records

GB = 10 ** 9
HOUR_SECONDS = 3600

PLACEMENTS = ("remote_stateless", "remote_warm", "local")

# Declared teaching inputs. The far site is genuinely cheaper per unit and
# genuinely slower to deliver, which is the trade 12.6.1 asks the reader to price.
DEFAULT_REGIONS = {
    "near": {
        "role": "beside the user",
        "compute_price_per_gpu_hour": "3.0",
        "egress_price_per_gb": "0",
        "state_price_per_gb_hour": "0.12",
        "electricity_price_per_kwh": "0.11",
        "cooling_overhead": "1.25",
        "power_cap_kw": 400,
        "lead_time_weeks": 4,
    },
    "far": {
        "role": "cheaper site across the region boundary",
        "compute_price_per_gpu_hour": "1.2",
        "egress_price_per_gb": "0.08",
        "state_price_per_gb_hour": "0.05",
        "electricity_price_per_kwh": "0.04",
        "cooling_overhead": "1.35",
        "power_cap_kw": 400,
        "lead_time_weeks": 30,
    },
}

PLACEMENT_REGION = {"local": "near", "remote_stateless": "far", "remote_warm": "far"}


def fraction(value: Fraction) -> dict:
    return {"numerator": value.numerator, "denominator": value.denominator}


def exact(value) -> Fraction:
    """Read a declared decimal without introducing binary rounding."""
    return Fraction(str(value))


def region_inputs(regions: dict | None) -> dict:
    """Normalise declared region attributes and reject unusable ones."""
    source = DEFAULT_REGIONS if regions is None else regions
    if not isinstance(source, dict) or not source:
        raise ValueError("Regions must be a nonempty mapping")
    if set(source) != set(DEFAULT_REGIONS):
        raise ValueError("Regions must name exactly the near and far sites this placement compares")
    normalised = {}
    for name, row in source.items():
        entry = {}
        for key in ("compute_price_per_gpu_hour", "egress_price_per_gb",
                    "state_price_per_gb_hour", "electricity_price_per_kwh",
                    "cooling_overhead"):
            if key not in row:
                raise ValueError(f"Region {name} is missing {key}")
            value = exact(row[key])
            if value < 0:
                raise ValueError(f"Region {name} has a negative {key}")
            entry[key] = value
        if entry["cooling_overhead"] < 1:
            raise ValueError(f"Region {name} cannot have cooling overhead below 1")
        entry["power_cap_kw"] = positive_int(row["power_cap_kw"], f"{name} power_cap_kw")
        entry["lead_time_weeks"] = positive_int(row["lead_time_weeks"],
                                                f"{name} lead_time_weeks", allow_zero=True)
        entry["role"] = row.get("role", "")
        normalised[name] = entry
    return normalised


def feasibility(regions: dict, required_kw: int, deadline_weeks: int) -> list:
    """A site that cannot be powered or delivered in time is not a candidate.

    This gate runs before any price comparison, so a lower unit price never
    ranks a site that cannot carry the demand.
    """
    positive_int(required_kw, "required_kw")
    positive_int(deadline_weeks, "deadline_weeks", allow_zero=True)
    rows = []
    for name, region in sorted(regions.items()):
        reasons = []
        if required_kw > region["power_cap_kw"]:
            reasons.append(f"needs {required_kw} kW against a {region['power_cap_kw']} kW cap")
        if region["lead_time_weeks"] > deadline_weeks:
            reasons.append(f"delivers in {region['lead_time_weeks']} weeks "
                           f"against a {deadline_weeks} week deadline")
        rows.append({"region": name, "role": region["role"],
                     "required_kw": required_kw, "power_cap_kw": region["power_cap_kw"],
                     "lead_time_weeks": region["lead_time_weeks"],
                     "deadline_weeks": deadline_weeks,
                     "feasible": not reasons,
                     "reasons": reasons or ["within the declared power cap and lead time"]})
    return rows


def kv_bytes_per_token(model: str, state_bits: int) -> int:
    """K and V for one position, from the official config's attention geometry."""
    if state_bits not in (16, 8):
        raise ValueError("Session state must be held at 16 or 8 bits")
    config = model_config(model)
    if config.get("num_key_value_heads") is None or config.get("head_dim") is None:
        raise ValueError("This adapter needs an explicit grouped-query geometry")
    return 2 * (state_bits // 8) * config["num_hidden_layers"] * \
        config["num_key_value_heads"] * config["head_dim"]


@lru_cache(maxsize=None)
def prefill_flops(model: str, history: int, tokens: int) -> int:
    """Matrix work to prefill `tokens` new positions behind `history` cached ones."""
    positive_int(history, "history", allow_zero=True)
    positive_int(tokens, "tokens")
    return model_forward(model, Scenario(history=history, tokens=tokens))["summary"]["matrix_flops"]


def round_bytes(files: dict, rounds: list, unit_bytes: int) -> list:
    """Bytes each placement pushes across the region boundary, per round.

    A stateless service receives the whole conversation prefix every round; a
    warm one receives only what grew since the last round. Both figures are the
    trace's own message bodies, not a token count multiplied by a guess.
    """
    raw = files["rounds.jsonl"]
    if len(raw) != len(rounds):
        raise ValueError("Accounted rounds and raw trace rounds disagree")
    ledger, previous = [], 0
    for record, row in zip(raw, rounds):
        if record["turn"] != row["turn"]:
            raise ValueError("Raw and accounted rounds are not aligned")
        prefix = len(json.dumps(record["messages"], ensure_ascii=False).encode())
        if prefix < previous:
            raise ValueError("A conversation prefix cannot shrink between rounds")
        delta, previous = prefix - previous, prefix
        reply = len(record["output_text"].encode())
        held = row["prompt_tokens"] + row["output_tokens"]
        ledger.append({
            "turn": row["turn"],
            "prompt_tokens": row["prompt_tokens"], "cached_tokens": row["cached_tokens"],
            "uncached_tokens": row["uncached_tokens"], "output_tokens": row["output_tokens"],
            "prefix_bytes": prefix, "delta_bytes": delta, "reply_bytes": reply,
            "inbound_bytes": {"remote_stateless": prefix, "remote_warm": delta, "local": 0},
            "outbound_bytes": {"remote_stateless": reply, "remote_warm": reply, "local": 0},
            "held_state_tokens": held, "held_state_bytes": held * unit_bytes,
            "prefill_matrix_flops": {
                "remote_stateless": row["cold_prefill_matrix_flops"],
                "remote_warm": row["cached_prefill_matrix_flops"],
                "local": row["cached_prefill_matrix_flops"]},
            "decode_matrix_flops": row["decode_matrix_flops"],
            "measured_model_seconds": row["measured_model_seconds"]})
    return ledger


def transfer_seconds(byte_count: int, bits_per_second: int) -> Fraction:
    positive_int(byte_count, "byte_count", allow_zero=True)
    positive_int(bits_per_second, "bits_per_second")
    return Fraction(byte_count * 8, bits_per_second)


def wait_per_round(entry: dict, placement: str, round_trip_ms, bits_per_second: int,
                   device_flops_per_second: int) -> dict:
    """One round's wait: a round trip, the bytes it carries, and the compute.

    Compute here is work divided by a declared rate, which bounds service from
    below; it is not a measured latency and does not replace one.
    """
    crossing = placement != "local"
    inbound = entry["inbound_bytes"][placement]
    outbound = entry["outbound_bytes"][placement]
    trip = exact(round_trip_ms) / 1000 if crossing else Fraction(0)
    move = transfer_seconds(inbound + outbound, bits_per_second) if crossing else Fraction(0)
    flops = entry["prefill_matrix_flops"][placement] + entry["decode_matrix_flops"]
    compute = Fraction(flops, device_flops_per_second)
    return {"turn": entry["turn"], "placement": placement,
            "round_trip_seconds": fraction(trip), "transfer_seconds": fraction(move),
            "compute_lower_bound_seconds": fraction(compute),
            "wait_seconds": fraction(trip + move + compute), "matrix_flops": flops}


def session_cost(ledger: list, placement: str, region: dict, device_flops_per_second: int,
                 state_hold_hours: Fraction, ingress_price_per_gb: Fraction) -> dict:
    """Compute, transfer and resident-state cost for one placement in one region."""
    inbound = sum(entry["inbound_bytes"][placement] for entry in ledger)
    outbound = sum(entry["outbound_bytes"][placement] for entry in ledger)
    flops = sum(entry["prefill_matrix_flops"][placement] + entry["decode_matrix_flops"]
                for entry in ledger)
    seconds = Fraction(flops, device_flops_per_second)
    compute_cost = seconds * region["compute_price_per_gpu_hour"] / HOUR_SECONDS
    egress_cost = Fraction(outbound, GB) * region["egress_price_per_gb"]
    ingress_cost = Fraction(inbound, GB) * ingress_price_per_gb
    peak_state = max((entry["held_state_bytes"] for entry in ledger), default=0)
    holds_state = placement == "remote_warm"
    state_cost = (Fraction(peak_state, GB) * region["state_price_per_gb_hour"] * state_hold_hours
                  if holds_state else Fraction(0))
    total = compute_cost + egress_cost + ingress_cost + state_cost
    return {"placement": placement, "inbound_bytes": inbound, "outbound_bytes": outbound,
            "matrix_flops": flops, "compute_seconds_lower_bound": fraction(seconds),
            "compute_cost": fraction(compute_cost), "egress_cost": fraction(egress_cost),
            "ingress_cost": fraction(ingress_cost),
            "resident_state_bytes": peak_state if holds_state else 0,
            "state_hold_hours": fraction(state_hold_hours if holds_state else Fraction(0)),
            "state_cost": fraction(state_cost), "total_cost": fraction(total)}


def break_even_hold_hours(ledger: list, region: dict, device_flops_per_second: int,
                          ingress_price_per_gb: Fraction) -> dict:
    """How long a warm session can be held before re-sending it is cheaper.

    Warm cost rises linearly with the hold; stateless cost does not depend on it.
    One division gives the crossing exactly.
    """
    warm = session_cost(ledger, "remote_warm", region, device_flops_per_second,
                        Fraction(0), ingress_price_per_gb)
    stateless = session_cost(ledger, "remote_stateless", region, device_flops_per_second,
                             Fraction(0), ingress_price_per_gb)
    saving = Fraction(**stateless["total_cost"]) - Fraction(**warm["total_cost"])
    peak = warm["resident_state_bytes"]
    rate = Fraction(peak, GB) * region["state_price_per_gb_hour"]
    if saving <= 0:
        return {"hold_hours": None,
                "reason": "Holding the session saves nothing even before residency is charged"}
    if rate == 0:
        return {"hold_hours": None,
                "reason": "Residency is declared free here, so the warm placement never loses"}
    hours = saving / rate
    return {"hold_hours": fraction(hours), "hold_seconds": fraction(hours * HOUR_SECONDS),
            "saving_at_zero_hold": fraction(saving),
            "residency_cost_per_hour": fraction(rate),
            "resident_state_bytes": peak,
            "reason": ("Below this hold the warm placement is cheaper; above it the prefill "
                       "it avoids no longer pays for the memory it occupies")}


def break_even_egress_price(local: dict, remote: dict, region: dict) -> dict:
    """Egress price at which the cheaper remote region stops paying for itself."""
    outbound = remote["outbound_bytes"]
    if outbound == 0:
        return {"price_per_gb": None, "reason": "This placement moves no billable bytes"}
    slack = Fraction(**local["total_cost"]) - (Fraction(**remote["total_cost"])
                                               - Fraction(**remote["egress_cost"]))
    if slack <= 0:
        return {"price_per_gb": None,
                "reason": "The remote region is not cheaper even before any egress is charged"}
    boundary = slack / Fraction(outbound, GB)
    return {"price_per_gb": fraction(boundary),
            "declared_price_per_gb": fraction(region["egress_price_per_gb"]),
            "headroom_per_gb": fraction(boundary - region["egress_price_per_gb"]),
            "reason": ("Above this egress price the local placement is cheaper; "
                       "below it the remote one is")}


def deadline_scan(regions: dict, required_kw: int, weeks: tuple) -> list:
    """Where the delivery deadline alone decides which sites remain candidates."""
    rows = []
    for deadline in weeks:
        gate = feasibility(regions, required_kw, deadline)
        rows.append({"deadline_weeks": deadline,
                     "feasible_regions": [row["region"] for row in gate if row["feasible"]]})
    return rows


def reuse_scan(ledger: list, region: dict, device_flops_per_second: int,
               state_hold_hours: Fraction, ingress_price_per_gb: Fraction,
               model: str) -> dict:
    """Sweep the cache hit fraction and report where the ordering changes.

    A hit changes both what crosses the boundary and what the accelerator has
    to prefill, and the second is the larger term. The prefill work at each hit
    level is recomputed through the model adapter rather than scaled, so the
    scan stays an accounting of the official geometry.
    """
    prompt = sum(entry["prompt_tokens"] for entry in ledger)
    cached = sum(entry["cached_tokens"] for entry in ledger)
    measured = Fraction(cached, prompt) if prompt else Fraction(0)
    rows = []
    for numerator in range(11):
        share = Fraction(numerator, 10)
        scaled = []
        for entry in ledger:
            tokens = entry["prompt_tokens"]
            # One query position always stays uncached, as the trace itself requires.
            hit = min(int(tokens * share), tokens - 1)
            copy = dict(entry)
            copy["inbound_bytes"] = dict(entry["inbound_bytes"])
            copy["prefill_matrix_flops"] = dict(entry["prefill_matrix_flops"])
            copy["inbound_bytes"]["remote_warm"] = (
                int(Fraction(entry["prefix_bytes"]) * (tokens - hit) / tokens) if tokens else 0)
            copy["prefill_matrix_flops"]["remote_warm"] = prefill_flops(model, hit, tokens - hit)
            scaled.append(copy)
        warm = session_cost(scaled, "remote_warm", region, device_flops_per_second,
                            state_hold_hours, ingress_price_per_gb)
        stateless = session_cost(scaled, "remote_stateless", region, device_flops_per_second,
                                 state_hold_hours, ingress_price_per_gb)
        rows.append({"cache_hit_fraction": fraction(share),
                     "warm_total_cost": warm["total_cost"],
                     "stateless_total_cost": stateless["total_cost"],
                     "warm_is_cheaper": Fraction(**warm["total_cost"])
                     < Fraction(**stateless["total_cost"])})
    flips = [rows[index] for index in range(1, len(rows))
             if rows[index]["warm_is_cheaper"] != rows[index - 1]["warm_is_cheaper"]]
    return {"measured_cache_hit_fraction": fraction(measured), "scan": rows,
            "ordering_changes_between": flips or None,
            "note": ("Only the prefill a warm cache avoids pays for holding the state, so the "
                     "scan says how much reuse the hold needs; the prefix payload is scaled "
                     "from the trace's real bytes, not re-measured")}


def calculate(trace: str = "thinking-off", model: str = "qwen3-8b",
              regions: dict | None = None,
              device_flops_per_second: int = 100 * 10 ** 12,
              link_bits_per_second: int | None = None,
              state_bits: int = 16,
              state_hold_hours: float | None = None,
              ingress_price_per_gb: float = 0.0,
              required_kw: int = 250, deadline_weeks: int = 36) -> dict:
    """Place one measured Agent session across regions at fixed quality."""
    positive_int(device_flops_per_second, "device_flops_per_second")
    if ingress_price_per_gb < 0:
        raise ValueError("ingress_price_per_gb must be nonnegative")
    if state_hold_hours is not None:
        positive_number(state_hold_hours, "state_hold_hours")

    measured = agent_trace.calculate(trace=trace)
    files, _ = agent_trace.read_trace(trace)
    records, _ = queqiao_records.load()
    knee = records["path"]["downstream_knee_bits_per_s"]
    link = knee if link_bits_per_second is None else positive_int(link_bits_per_second,
                                                                 "link_bits_per_second")
    band = (records["path"]["round_trip_ms"]["low"], records["path"]["round_trip_ms"]["high"])

    unit = kv_bytes_per_token(model, state_bits)
    ledger = round_bytes(files, measured["agent_rounds"], unit)
    normalised = region_inputs(regions)

    elapsed = Fraction(str(measured["summary"]["measured_elapsed_seconds"]))
    hold = (Fraction(elapsed, HOUR_SECONDS) if state_hold_hours is None
            else exact(state_hold_hours))
    ingress = exact(ingress_price_per_gb)

    gate = feasibility(normalised, required_kw, deadline_weeks)
    feasible = {row["region"] for row in gate if row["feasible"]}

    costs, waits = [], []
    for placement in PLACEMENTS:
        name = PLACEMENT_REGION[placement]
        region = normalised[name]
        row = session_cost(ledger, placement, region, device_flops_per_second, hold, ingress)
        row.update(region=name, feasible=name in feasible)
        costs.append(row)
        for bound, trip in (("low", band[0]), ("high", band[1])):
            total = sum((Fraction(**wait_per_round(entry, placement, trip, link,
                                                   device_flops_per_second)["wait_seconds"])
                         for entry in ledger), Fraction(0))
            waits.append({"region": name, "placement": placement, "round_trip_bound": bound,
                          "round_trip_ms": trip, "session_wait_seconds": fraction(total)})

    by_placement = {row["placement"]: row for row in costs}
    ranked = sorted((row for row in costs if row["feasible"]),
                    key=lambda row: Fraction(**row["total_cost"]))

    return {
        "calculation": "cross-region-placement",
        "inputs": {"trace": trace, "model": model,
                   "device_flops_per_second": device_flops_per_second,
                   "link_bits_per_second": link, "state_bits": state_bits,
                   "state_hold_hours": None if state_hold_hours is None else state_hold_hours,
                   "ingress_price_per_gb": ingress_price_per_gb,
                   "required_kw": required_kw, "deadline_weeks": deadline_weeks},
        "sources": provenance(model) + measured["sources"],
        "quality_contract": (
            "All three placements replay one pinned trace: same model revision, same token "
            "sequence, same rounds. Quality is fixed by construction, and no placement here "
            "is claimed to have been evaluated on its own."),
        "path": {"round_trip_ms_band": list(band), "link_bits_per_second": link,
                 "provenance": "pinned Queqiao path records"},
        "kv_bytes_per_token": unit,
        "state_hold_hours_used": fraction(hold),
        "measured_summary": measured["summary"],
        "regions": {name: {key: (fraction(value) if isinstance(value, Fraction) else value)
                           for key, value in region.items()}
                    for name, region in normalised.items()},
        "feasibility": gate,
        "deadline_scan": deadline_scan(normalised, required_kw, (4, 12, 26, 30, 36, 52)),
        "round_ledger": ledger,
        "session_costs": costs,
        "session_waits": waits,
        "ranked_feasible": [row["region"] + "/" + row["placement"] for row in ranked],
        "excluded_by_hard_constraints": [row["region"] + "/" + row["placement"]
                                         for row in costs if not row["feasible"]],
        "hold_boundary": break_even_hold_hours(ledger, normalised["far"],
                                               device_flops_per_second, ingress),
        "egress_price_boundary": break_even_egress_price(by_placement["local"],
                                                         by_placement["remote_warm"],
                                                         normalised["far"]),
        "reuse_scan": reuse_scan(ledger, normalised["far"], device_flops_per_second,
                                 hold, ingress, model),
        "assumptions": [
            "Request and reply bytes are the trace's own message bodies and output text, not token counts times a guess.",
            "Session state is the official config's K/V geometry times the tokens actually held.",
            "Prices, power caps and lead times are declared teaching inputs; no operator tariff is claimed.",
            "Compute time is work divided by a declared rate, a lower bound on service rather than a latency.",
            "Round-trip delay and link capacity come from the pinned Queqiao path, which is one measured path.",
            "The power and lead-time gate runs before any price ranking, so a cheap site that cannot carry the demand never ranks.",
            "Quality is fixed by replaying one identical trace, not by evaluating each placement separately.",
        ],
    }


def markdown(result: dict) -> str:
    def money(entry):
        return "—" if entry is None else f"{float(Fraction(**entry)):.6f}"

    def number(entry, places=3):
        return "—" if entry is None else f"{float(Fraction(**entry)):.{places}f}"

    lines = ["# 跨地域放置：同一任务、同一质量", "",
             result["quality_contract"], "",
             f"会话状态按官方配置的 K/V 几何计为每 token {result['kv_bytes_per_token']} 字节；"
             f"请求与回复字节取自轨迹自身的消息体。价格、功率上限与交付期是声明输入。", "",
             "## 硬约束先于价格", "",
             "| 地域 | 需求 kW | 功率上限 kW | 交付期 周 | 期限 周 | 可用 | 原因 |",
             "|---|---:|---:|---:|---:|---|---|"]
    for row in result["feasibility"]:
        lines.append("| " + " | ".join([
            row["region"], str(row["required_kw"]), str(row["power_cap_kw"]),
            str(row["lead_time_weeks"]), str(row["deadline_weeks"]),
            "是" if row["feasible"] else "否", "；".join(row["reasons"])]) + " |")

    lines += ["", "| 交付期限 周 | 仍是候选的地域 |", "|---:|---|"]
    for row in result["deadline_scan"]:
        lines.append(f"| {row['deadline_weeks']} | {'、'.join(row['feasible_regions']) or '无'} |")

    lines += ["", "## 三种放置的字节与费用", "",
              "| 放置 | 地域 | 入向 B | 出向 B | 矩阵 FLOPs | 计算费 | 出网费 | 驻留费 | 合计 | 可用 |",
              "|---|---|---:|---:|---:|---:|---:|---:|---:|---|"]
    for row in result["session_costs"]:
        lines.append("| " + " | ".join([
            row["placement"], row["region"], str(row["inbound_bytes"]), str(row["outbound_bytes"]),
            str(row["matrix_flops"]), money(row["compute_cost"]), money(row["egress_cost"]),
            money(row["state_cost"]), money(row["total_cost"]),
            "是" if row["feasible"] else "否"]) + " |")
    lines += ["", f"可用放置按费用排序：{' < '.join(result['ranked_feasible']) or '无'}。"]
    if result["excluded_by_hard_constraints"]:
        lines.append(f"因硬约束排除：{'、'.join(result['excluded_by_hard_constraints'])}。")

    lines += ["", "## 每会话等待（往返区间两端）", "",
              "等待中的计算项是矩阵工作量除以声明速率，是服务时间下界而非时延。"
              f"同一轨迹的实测模型时间为 {result['measured_summary']['measured_model_seconds']:.3f} s、"
              f"实测总耗时 {result['measured_summary']['measured_elapsed_seconds']:.3f} s，"
              "两者不可互相替代。", "",
              "| 放置 | 往返 ms | 会话等待 s |", "|---|---:|---:|"]
    for row in result["session_waits"]:
        lines.append(f"| {row['placement']} | {row['round_trip_ms']} | "
                     f"{number(row['session_wait_seconds'])} |")

    hold = result["hold_boundary"]
    egress = result["egress_price_boundary"]
    lines += ["", "## 盈亏平衡", "",
              f"- 保温时长：{('可保温 ' + number(hold['hold_seconds'], 1) + ' s（' + number(hold['hold_hours'], 5) + ' h）') if hold['hold_hours'] else '不适用'}；{hold['reason']}。",
              f"- 出网价格：{('边界 ' + money(egress['price_per_gb']) + ' /GB，声明价 ' + money(egress['declared_price_per_gb']) + ' /GB') if egress['price_per_gb'] else '不适用'}；{egress['reason']}。",
              "", "## 复用比例扫描", "",
              f"实测缓存命中比例 {number(result['reuse_scan']['measured_cache_hit_fraction'], 4)}。", "",
              "| 命中比例 | 保温合计 | 无状态合计 | 保温更便宜 |", "|---:|---:|---:|---|"]
    for row in result["reuse_scan"]["scan"]:
        lines.append("| " + " | ".join([
            number(row["cache_hit_fraction"], 1), money(row["warm_total_cost"]),
            money(row["stateless_total_cost"]), "是" if row["warm_is_cheaper"] else "否"]) + " |")

    lines += ["", "## 口径与限制", ""]
    lines += ["- " + item for item in result["assumptions"]]
    lines += ["", "## 完整输入、来源与结果", "", "```json",
              json.dumps(result, ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lines)
