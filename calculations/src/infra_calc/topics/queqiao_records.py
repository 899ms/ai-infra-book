"""C70: same-condition statistics over the pinned Queqiao ASR/TTS records.

The two source documents mix measurement generations, connection states, kernel
settings and path conditions in one narrative. This module refuses to compare
rows whose recorded conditions differ, re-derives each row's arithmetic floor
from the path parameters, separates leg residuals from timestamp resolution,
and reports how many samples actually stand behind every quoted quantile.

Nothing here fabricates a quantile the documents do not print, and no measured
value is interpolated, smoothed or extrapolated. A statistic that the records
cannot support is returned as ``None`` with the reason attached.
"""
from fractions import Fraction
import hashlib
import json

from ..paths import PROJECT
from ..units import positive_int, positive_number

LOCK = "configs/queqiao-records.lock.json"

# 12.5.1 splits the interaction into these stages. A recorded leg covers a
# contiguous run of them; stages no leg covers stay uncovered on purpose.
STAGES = ("capture", "encode", "upload", "asr_model", "llm",
          "tts_model", "download", "playback_buffer", "playback")

LEG_STAGES = {
    "connect": (),
    "request_to_first_byte": ("upload", "asr_model", "llm", "tts_model"),
    "download": ("download",),
    "total": ("upload", "asr_model", "llm", "tts_model", "download"),
}

# A quantile quoted from too few samples is decided by a handful of points.
# Five samples beyond the quantile is this project's declared floor for
# reporting one; below it the number is printed but marked unsupported.
MIN_SAMPLES_BEYOND_QUANTILE = 5


def fraction(value: Fraction) -> dict:
    return {"numerator": value.numerator, "denominator": value.denominator}


def exact(value) -> Fraction:
    """Read a recorded decimal without introducing binary rounding."""
    return Fraction(str(value))


def load() -> dict:
    """Read the transcribed records after checking every locked input."""
    lock = json.loads((PROJECT / LOCK).read_text())
    verified = []
    for record in lock:
        data = (PROJECT / record["file"]).read_bytes()
        if len(data) != record["bytes"]:
            raise ValueError("Queqiao input length mismatch: " + record["file"])
        if hashlib.sha256(data).hexdigest() != record["sha256"]:
            raise ValueError("Queqiao input checksum mismatch: " + record["file"])
        verified.append(record)
    records = json.loads((PROJECT / "sources/queqiao-records/records.json").read_text())
    for document in records["origin_documents"]:
        if not any(row["file"] == document["file"] for row in verified):
            raise ValueError("Origin document is not locked: " + document["file"])
    return records, verified


def serialization_ms(payload_bytes: int, bits_per_second: int) -> Fraction:
    """Wire time for one payload at a declared rate, in milliseconds."""
    positive_int(payload_bytes, "payload_bytes", allow_zero=True)
    positive_int(bits_per_second, "bits_per_second")
    return Fraction(payload_bytes * 8 * 1000, bits_per_second)


def slow_start_rounds(payload_bytes: int, mss_bytes: int, initial_window: int) -> dict:
    """Round trips a doubling initial window needs to clear one payload.

    Segment k of the ramp carries ``initial_window * 2**k`` segments, so after
    ``r`` rounds the sender has delivered ``initial_window * (2**r - 1)``.
    """
    positive_int(payload_bytes, "payload_bytes")
    positive_int(mss_bytes, "mss_bytes")
    positive_int(initial_window, "initial_window")
    segments = -(-payload_bytes // mss_bytes)
    rounds, delivered = 0, 0
    schedule = []
    while delivered < segments:
        window = initial_window * 2 ** rounds
        delivered += window
        rounds += 1
        schedule.append({"round": rounds, "window_segments": window,
                         "cumulative_segments": min(delivered, segments)})
    return {"payload_bytes": payload_bytes, "segments": segments,
            "rounds": rounds, "schedule": schedule}


def floor_interval(payload_bytes: int, round_trip_ms, model_ms, knee_bits_per_second: int) -> dict:
    """One round trip plus wire time plus model service, as an interval.

    Both endpoints are recorded intervals, so the floor is an interval too. A
    measurement below the low endpoint is arithmetically impossible, not fast.
    """
    wire = serialization_ms(payload_bytes, knee_bits_per_second)
    low = exact(round_trip_ms[0]) + wire + exact(model_ms[0])
    high = exact(round_trip_ms[1]) + wire + exact(model_ms[1])
    return {"payload_bytes": payload_bytes, "wire_ms": fraction(wire),
            "low_ms": fraction(low), "high_ms": fraction(high)}


def largest_feasible_payload_bytes(observed_ms, round_trip_ms, model_ms, knee_bits_per_second: int):
    """Biggest payload whose floor still fits under an observed median.

    Returns ``None`` when even a zero-byte payload cannot fit, which means the
    observed value is below the floor for the whole size range rather than for
    one mislabelled size.
    """
    budget = exact(observed_ms) - exact(round_trip_ms) - exact(model_ms)
    if budget < 0:
        return None
    return int(budget * knee_bits_per_second / Fraction(8 * 1000))


def condition_key(record: dict) -> tuple:
    """Everything that must match before two rows may be compared."""
    return (record["generation"], record["workload"],
            record["connection"], record["kernel_ssai"])


def compare(left: dict, right: dict, leg: str = "total") -> dict:
    """Ratio between two rows, refused unless every recorded condition matches."""
    if condition_key(left) != condition_key(right):
        raise ValueError("Refusing to compare rows recorded under different conditions")
    if left["arm"] == right["arm"]:
        raise ValueError("A comparison needs two different arms")
    values = []
    for record in (left, right):
        entry = record["legs"].get(leg)
        if entry is None or entry.get("p50") is None:
            raise ValueError(f"Row {record['id']} does not report a {leg} median")
        values.append(exact(entry["p50"]))
    ratio = values[0] / values[1]
    return {"leg": leg, "condition": list(condition_key(left)),
            "numerator_id": left["id"], "denominator_id": right["id"],
            "numerator_ms": fraction(values[0]), "denominator_ms": fraction(values[1]),
            "ratio": fraction(ratio), "difference_ms": fraction(values[0] - values[1])}


def paired_statistic(comparison: dict, documented: dict | None) -> dict:
    """Set the ratio of medians beside the document's paired per-round ratio.

    They are different statistics. The per-round values are not in the records,
    so the paired one cannot be recomputed here and is carried, not derived.
    """
    if documented is None or documented["median_of_per_round_ratios"] is None:
        return {"documented_paired_ratio": None,
                "paired_vs_ratio_of_medians": None,
                "paired_note": ("The documents give no median of per-round ratios for this condition"
                                if documented is None else
                                "The documents give only a spread for this condition, not a paired median"),
                "documented_paired_spread": (None if documented is None else
                                             [documented["middle_80_low"], documented["middle_80_high"]])}
    stated = exact(documented["median_of_per_round_ratios"])
    return {"documented_paired_ratio": fraction(stated),
            "paired_vs_ratio_of_medians": fraction(stated - Fraction(**comparison["ratio"])),
            "paired_note": ("A median of per-round ratios is not the ratio of the two medians; "
                            "the per-round values are not in the records, so only the difference is shown"),
            "documented_paired_spread": [documented["middle_80_low"], documented["middle_80_high"]]}


def leg_account(record: dict, resolution_ms) -> dict:
    """Legs against the total, with rounding separated from median non-additivity.

    Per-leg medians come from different rounds, so their sum is not the median
    of the total. The residual is reported as evidence of that, never as an
    unmeasured stage.
    """
    legs = {name: entry["p50"] for name, entry in record["legs"].items()
            if name != "total" and entry.get("p50") is not None}
    total = record["legs"].get("total", {}).get("p50")
    if total is None or not legs:
        return {"id": record["id"], "decomposable": False,
                "reason": "The document reports no total, or no separate legs, for this row"}
    summed = sum((exact(value) for value in legs.values()), Fraction(0))
    residual = exact(total) - summed
    half_ulp = exact(resolution_ms) / 2
    bound = half_ulp * (len(legs) + 1)
    covered = sorted({stage for name in legs for stage in LEG_STAGES[name]})
    return {"id": record["id"], "decomposable": True,
            "legs_ms": {name: fraction(exact(value)) for name, value in legs.items()},
            "total_ms": fraction(exact(total)), "summed_legs_ms": fraction(summed),
            "residual_ms": fraction(residual),
            "resolution_bound_ms": fraction(bound),
            "within_resolution": abs(residual) <= bound,
            "explanation": ("Residual fits the reported resolution" if abs(residual) <= bound
                            else "Residual exceeds rounding, so these are per-leg medians of different rounds and do not add"),
            "stages_covered": covered,
            "stages_uncovered": [stage for stage in STAGES if stage not in covered]}


def quantile_support(offered, quantile: Fraction) -> dict:
    """How many samples stand beyond a quoted quantile.

    ``p999`` over 1200 frames is the second largest sample. Reporting that is
    the point of this function; inventing the missing samples is not.
    """
    if offered is None:
        return {"quantile": fraction(quantile), "sample_count": None, "supported": None,
                "reason": "The document does not state how many samples this run produced"}
    positive_int(offered, "offered")
    rank = -((-offered * quantile.numerator) // quantile.denominator)
    beyond = offered - rank
    return {"quantile": fraction(quantile), "sample_count": offered,
            "order_statistic_rank": rank, "samples_beyond": beyond,
            "supported": beyond >= MIN_SAMPLES_BEYOND_QUANTILE,
            "reason": None if beyond >= MIN_SAMPLES_BEYOND_QUANTILE
            else f"Only {beyond} sample(s) lie beyond this quantile; it is decided by that many points"}


QUANTILE_LEVELS = {"p50": Fraction(1, 2), "p90": Fraction(9, 10),
                   "p99": Fraction(99, 100), "p999": Fraction(999, 1000)}


def frame_account(record: dict) -> dict:
    """Delivered/lost conservation and per-quantile support for one frame run."""
    offered, lost = record["offered"], record["lost"]
    derived = None if offered is None or lost is None else offered - lost
    recorded = record["delivered_recorded"]
    if recorded is not None and derived is not None and recorded != derived:
        raise ValueError("Frame run does not conserve offered = delivered + lost: " + record["id"])
    loss = None if offered in (None, 0) or lost is None else Fraction(lost, offered)
    quantiles = {}
    for name, value in record["quantiles_ms"].items():
        if value is None:
            quantiles[name] = {"value_ms": None, "available": False,
                               "reason": "The document does not report this quantile for this run"}
            continue
        quantiles[name] = {"value_ms": fraction(exact(value)), "available": True,
                           "support": quantile_support(offered, QUANTILE_LEVELS[name])}
    pair = record["quantiles_ms"].get("p99"), record["quantiles_ms"].get("p50")
    return {"id": record["id"], "carrier": record["carrier"], "arm": record["arm"],
            "sessions": record["sessions"], "offered": offered, "lost": lost,
            "delivered_recorded": recorded, "delivered_derived": derived,
            "loss_fraction": None if loss is None else fraction(loss),
            "quantiles": quantiles,
            "tail_over_median": (fraction(exact(pair[0]) / exact(pair[1]))
                                 if None not in pair else None),
            "tail_over_median_reason": (None if None not in pair
                                        else "Needs both p99 and p50; this run reports only one of them"),
            "section": record["section"]}


def playback_supply(records: dict, prebuffer_ms: float) -> dict:
    """Sustained supply against playback consumption, and time to the first stall.

    A buffer only delays a stall when average supply is below consumption; the
    drain time is what says how long it delays it.
    """
    positive_number(prebuffer_ms, "prebuffer_ms")
    audio = records["audio_file"]
    consumption = audio["assumed_sample_rate_hz"] * audio["assumed_channels"] * audio["assumed_sample_bytes"]
    consumption_bits = consumption * 8
    rows = []
    for name, rate in sorted(records["path"]["sustained_bits_per_s"].items()):
        if name == "section":
            continue
        supply = Fraction(rate)
        sufficient = supply > consumption_bits
        drain_ms = (None if sufficient else
                    exact(prebuffer_ms) * Fraction(consumption_bits) / (Fraction(consumption_bits) - supply))
        rows.append({"measurement": name, "supply_bits_per_s": rate,
                     "headroom": fraction(supply / consumption_bits),
                     "sufficient_for_playback": sufficient,
                     "stall_onset_ms": None if drain_ms is None else fraction(drain_ms),
                     "note": None if sufficient else
                     "Average supply is under consumption, so the prebuffer only postpones the stall"})
    pcm_bytes = audio["bytes"] - audio["wav_header_bytes"]
    return {"assumed_format": {"sample_rate_hz": audio["assumed_sample_rate_hz"],
                               "channels": audio["assumed_channels"],
                               "sample_bytes": audio["assumed_sample_bytes"],
                               "declared_by_document": audio["declared_format"]},
            "consumption_bytes_per_s": consumption,
            "consumption_bits_per_s": consumption_bits,
            "file_bytes": audio["bytes"], "pcm_bytes": pcm_bytes,
            "implied_duration_s": fraction(Fraction(pcm_bytes, consumption)),
            "prebuffer_ms": fraction(exact(prebuffer_ms)),
            "rows": rows}


def calculate(prebuffer_ms: float = 60.0, comparison_leg: str = "total") -> dict:
    """Re-account the pinned Queqiao records under their own recorded conditions."""
    records, locked = load()
    path = records["path"]
    knee = path["downstream_knee_bits_per_s"]
    resolution = records["reported_resolution_ms"]
    model = (records["model_service_ms"]["asr_low"], records["model_service_ms"]["asr_high"])

    groups = {}
    for record in records["request_records"]:
        groups.setdefault(condition_key(record), []).append(record)

    paired = {tuple(row["condition"]): row for row in records["documented_paired_ratios"]}
    comparisons, ungrouped = [], []
    for key, rows in sorted(groups.items()):
        arms = {row["arm"]: row for row in rows}
        if set(arms) == {"direct", "queqiao"}:
            leg = comparison_leg if comparison_leg in arms["direct"]["legs"] else "download"
            if leg in arms["direct"]["legs"] and leg in arms["queqiao"]["legs"]:
                row = compare(arms["direct"], arms["queqiao"], leg)
                row.update(paired_statistic(row, paired.get(key)))
                comparisons.append(row)
                continue
        ungrouped.append({"condition": list(key), "ids": [row["id"] for row in rows],
                          "reason": "This condition does not hold both arms with a shared leg median"})

    feasibility = []
    for record in records["request_records"]:
        total = record["legs"].get("total", {}).get("p50")
        if total is None:
            continue
        generation = records["generations"][record["generation"]]
        rtt = (path["remeasurement_round_trip_ms"] if record["generation"] == "single-fixed-file"
               else path["round_trip_ms"])
        band = (rtt["low"], rtt["high"])
        low_floor = floor_interval(generation["payload_low_bytes"], band, model, knee)
        high_floor = floor_interval(generation["payload_high_bytes"], band, model, knee)
        stated = largest_feasible_payload_bytes(total, band[0], model[0], knee)
        has_minimum = "minimum" in rtt
        at_minimum = (largest_feasible_payload_bytes(total, rtt["minimum"], model[0], knee)
                      if has_minimum else None)
        observed = exact(total)
        if stated is not None:
            verdict = ("Consistent with the recorded payload range"
                       if stated >= generation["payload_high_bytes"] else
                       "Consistent only with payloads at the small end of the recorded range")
        elif not has_minimum:
            verdict = "Below the floor across the recorded round-trip band; this run records no minimum round trip to appeal to"
        elif at_minimum is None:
            verdict = "Below the floor at every recorded size, even at the fastest recorded round trip"
        else:
            verdict = "Below the floor across the recorded round-trip band; only the recorded minimum round trip admits it"
        feasibility.append({
            "id": record["id"], "generation": record["generation"],
            "observed_p50_ms": fraction(observed),
            "payload_interval_bytes": [generation["payload_low_bytes"], generation["payload_high_bytes"]],
            "label_supported": generation["label_supported"],
            "round_trip_band_ms": list(band),
            "floor_at_smallest_payload": low_floor,
            "floor_at_largest_payload": high_floor,
            "below_floor_at_smallest_payload": observed < Fraction(**low_floor["low_ms"]),
            "largest_feasible_payload_bytes": stated,
            "largest_feasible_payload_bytes_at_minimum_rtt": at_minimum,
            "exceeds_recorded_payload_range": stated is not None and stated >= generation["payload_high_bytes"],
            "verdict": verdict})

    accounts = [leg_account(record, resolution) for record in records["request_records"]]
    frames = [frame_account(record) for record in records["frame_records"]]

    ramp = slow_start_rounds(records["audio_file"]["bytes"],
                             path["tcp_mss_bytes"], path["initial_window_segments"])
    ramp_ms = Fraction(ramp["rounds"]) * exact(path["round_trip_ms"]["low"])
    measured_rtfb = next((exact(row["legs"]["request_to_first_byte"]["p50"])
                          for row in records["request_records"]
                          if row["id"] == "asr-rot-new-direct"), None)
    ramp_check = {"rounds": ramp["rounds"], "schedule": ramp["schedule"],
                  "predicted_ramp_ms": fraction(ramp_ms),
                  "measured_request_to_first_byte_ms": None if measured_rtfb is None else fraction(measured_rtfb),
                  "measured_minus_predicted_ms": None if measured_rtfb is None else fraction(measured_rtfb - ramp_ms),
                  "note": ("The ramp accounts for the request-to-first-byte leg to within one model service time; "
                           "it is an arithmetic bound on a doubling window, not a simulation of cubic")}

    return {
        "calculation": "queqiao-recorded-conditions",
        "inputs": {"prebuffer_ms": prebuffer_ms, "comparison_leg": comparison_leg},
        "sources": locked,
        "reported_resolution_ms": resolution,
        "half_ulp_ms": fraction(exact(resolution) / 2),
        "generations": records["generations"],
        "same_condition_comparisons": comparisons,
        "conditions_without_a_pair": ungrouped,
        "floor_feasibility": feasibility,
        "leg_accounts": accounts,
        "frame_runs": frames,
        "slow_start_check": ramp_check,
        "playback_supply": playback_supply(records, prebuffer_ms),
        "stages": list(STAGES),
        "assumptions": [
            "Every figure is transcribed from the two pinned documents; no run was repeated for this calculation.",
            "Rows are compared only when generation, workload, connection state and kernel setting all match.",
            "The rotating-eight-file generation carries a payload interval, not a size, so no per-size claim rests on it.",
            "Per-leg medians come from different rounds and are not additive; the residual measures that, not a missing stage.",
            "Audio sample rate, channel count and sample width are declared assumptions; the documents state only the byte count.",
            "Capture and playback are outside every recorded leg, so no recorded total is a user-perceived time.",
            "A quantile the documents do not print stays unavailable; none is interpolated from the ones they do print.",
            "Ratios here are ratios of medians; the documents' paired per-round ratios are carried for comparison and cannot be recomputed from these records.",
        ],
    }


def markdown(result: dict) -> str:
    def value(entry):
        return "—" if entry is None else f"{float(Fraction(**entry)):.2f}"

    lines = ["# Queqiao 原始记录的同条件统计", "",
             "全部数字取自两份固定文档，本节不重跑实验。只有代次、负载、连接状态与内核设置全部相同的行才允许比较。", "",
             "## 同条件比较", "",
             "| 条件 | 分子 | 分母 | 分子 ms | 分母 ms | 中位数之比 | 文档配对比 |",
             "|---|---|---|---:|---:|---:|---:|"]
    for row in result["same_condition_comparisons"]:
        lines.append("| " + " | ".join([
            "/".join(str(item) for item in row["condition"]), row["numerator_id"], row["denominator_id"],
            value(row["numerator_ms"]), value(row["denominator_ms"]),
            f"{float(Fraction(**row['ratio'])):.3f}",
            "—" if row["documented_paired_ratio"] is None
            else f"{float(Fraction(**row['documented_paired_ratio'])):.2f}"]) + " |")
    lines += ["", "配对比是逐轮比值的中位数，与两个中位数之比是不同的统计量；逐轮原值不在记录中，无法在此重算。"]

    lines += ["", "## 算术下界与可行载荷", "",
              "下界＝一个往返＋拐点速率下的串行时间＋模型服务；两端都是区间，所以下界也是区间。",
              "低于下界的中位数不是更快，而是不可能。", "",
              "| 记录 | 观测 p50 ms | 最小载荷下界 ms | 最大可行载荷 B | 判定 |", "|---|---:|---:|---:|---|"]
    for row in result["floor_feasibility"]:
        largest = row["largest_feasible_payload_bytes"]
        lines.append("| " + " | ".join([
            row["id"], value(row["observed_p50_ms"]), value(row["floor_at_smallest_payload"]["low_ms"]),
            "不可行" if largest is None else
            f"≥{row['payload_interval_bytes'][1]}" if row["exceeds_recorded_payload_range"] else str(largest),
            row["verdict"]]) + " |")

    lines += ["", "## 分段与时间戳误差", "",
              "各段是各自轮次的中位数，中位数不可相加；残差用来证明这一点，不代表未测量的阶段。", "",
              "| 记录 | 各段和 ms | 总计 ms | 残差 ms | 分辨率界 ms | 结论 |", "|---|---:|---:|---:|---:|---|"]
    for row in result["leg_accounts"]:
        if not row["decomposable"]:
            continue
        lines.append("| " + " | ".join([
            row["id"], value(row["summed_legs_ms"]), value(row["total_ms"]),
            value(row["residual_ms"]), value(row["resolution_bound_ms"]),
            row["explanation"]]) + " |")

    lines += ["", "## 帧分位数的样本支撑", "",
              "缺失的分位数保持缺失。已给出的分位数标注其背后实际有多少个样本。", "",
              "| 记录 | 提供 | 丢失 | 丢失率 | p50 | p99 | p99 之外样本 | 支撑 |",
              "|---|---:|---:|---:|---:|---:|---:|---|"]
    for row in result["frame_runs"]:
        p99 = row["quantiles"].get("p99", {})
        support = p99.get("support") or {}
        p50 = row["quantiles"].get("p50", {})
        lines.append("| " + " | ".join([
            row["id"], "—" if row["offered"] is None else str(row["offered"]),
            "—" if row["lost"] is None else str(row["lost"]),
            "—" if row["loss_fraction"] is None else f"{float(Fraction(**row['loss_fraction'])):.4f}",
            value(p50.get("value_ms")), value(p99.get("value_ms")),
            "—" if support.get("samples_beyond") is None else str(support["samples_beyond"]),
            "—" if support.get("supported") is None else ("是" if support["supported"] else "否")]) + " |")

    supply = result["playback_supply"]
    lines += ["", "## 持续供给与播放消费", "",
              f"按声明的 {supply['assumed_format']['sample_rate_hz']} Hz／"
              f"{supply['assumed_format']['channels']} 声道／"
              f"{supply['assumed_format']['sample_bytes']} 字节采样，播放消费为 "
              f"{supply['consumption_bits_per_s']} bit/s。文档只记录了字节数，格式是本计算的声明假设。", "",
              "| 测量 | 供给 bit/s | 相对消费 | 足够 | 首次卡顿 ms |", "|---|---:|---:|---|---:|"]
    for row in supply["rows"]:
        lines.append("| " + " | ".join([
            row["measurement"], str(row["supply_bits_per_s"]),
            f"{float(Fraction(**row['headroom'])):.3f}",
            "是" if row["sufficient_for_playback"] else "否",
            value(row["stall_onset_ms"])]) + " |")

    ramp = result["slow_start_check"]
    lines += ["", "## 慢启动轮次核对", "",
              f"初始窗口 {ramp['schedule'][0]['window_segments']} 段、每轮翻倍，"
              f"清空该载荷需 {ramp['rounds']} 轮，预测 {value(ramp['predicted_ramp_ms'])} ms；"
              f"实测 request-to-first-byte 为 {value(ramp['measured_request_to_first_byte_ms'])} ms，"
              f"差 {value(ramp['measured_minus_predicted_ms'])} ms。", "",
              "## 口径与限制", ""]
    lines += ["- " + item for item in result["assumptions"]]
    lines += ["", "## 完整输入、来源与结果", "", "```json",
              json.dumps(result, ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lines)
