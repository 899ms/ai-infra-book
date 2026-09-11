"""End, nearby and cloud tiers for the chapter-12 screenshot Agent, bound to named devices.

Every tier runs the same Qwen3-8B q4_0 weights at an 8K context and generates the same
number of tokens per round, so task quality is fixed by construction and only the device
changes.  Device inputs come from configs/hardware.json (memory bandwidth, BF16-input
FP32-accumulate dense tensor peak, board power); the phone tier uses the four-channel
LPDDR5X bus of results/energy-ledger-book.json (chapter 12.1.5), which is also where the
per-round token count is fixed.  Per-step bytes are the chapter 2/4 decode ledger
(results/qwen3-8b-decode-b1-s8192.json) with the weights re-packed to q4_0 (18 bytes per
32 values instead of 64).

Model time per round is the decode read lower bound: tokens x step bytes / bandwidth,
the same convention as 12.1.5.  A second set of GPU rows scales that bound by the
batch-1 8K decode time measured on the RTX PRO 6000 Blackwell Workstation Edition in
experiments/ch08/08-01/efficiency.json (25.83 ms against a 9.12 ms read bound), which is
the book's only measured batch-1 decode on one of these devices.  The one-time
preparation is a prefill of the 8K context the earlier rounds left behind, divided by the
dense BF16 peak; the phone has no archived matrix peak, so its preparation is set to zero,
which only favours the phone.  Energy is board power x busy seconds for the GPUs (an upper
bound, since power_watts is a TDP/TGP ceiling) and the MELTing Point per-token range for
the phone.  Network rates, round-trip times, the terminal's 0.3 s and the reconnect times
are declared network/task conditions, not device claims.

The encoder block binds 12.2.2: Qwen3-VL-4B vision encoding FLOPs from
results/vision-encoding-single.json divided by the dense BF16 peaks of an RTX 4090 terminal
and an H100 SXM server, and the image/feature transfer at the declared uplink and at one
ConnectX-7 400 Gb/s port (references/files/specs/nvidia-connectx7-datasheet.pdf).
"""
from fractions import Fraction
import json

from .. import hardware
from ..declared import exact, input_sources as _sources
from ..paths import BOOK, PROJECT
from ..units import positive_int
from .region_placement import prefill_flops

DEFAULT_TIERS = (
    {"name": "end", "label": "phone, four LPDDR5X x16 channels", "device": None,
     "uplink_bits_per_second": None, "rtt_seconds": "0"},
    {"name": "near", "label": "nearby workstation", "device": "rtx-pro6000-blackwell-ws",
     "uplink_bits_per_second": 80000000, "rtt_seconds": "0.02"},
    {"name": "cloud", "label": "cloud region", "device": "h100-sxm",
     "uplink_bits_per_second": 6400000, "rtt_seconds": "0.2"},
)

DEFAULT_CASES = (
    {"id": "twenty-rounds", "rounds": 20, "deadline_seconds": 45},
    {"id": "ten-rounds", "rounds": 10, "deadline_seconds": 23},
    {"id": "ten-rounds-tight", "rounds": 10, "deadline_seconds": 15},
    {"id": "twenty-retain-nine", "rounds": 20, "deadline_seconds": 45, "reconnect_seconds": 1, "redo_rounds": 1},
    {"id": "twenty-lose-ten", "rounds": 20, "deadline_seconds": 45, "reconnect_seconds": 1, "redo_rounds": 10},
    {"id": "ten-retain-seven", "rounds": 10, "deadline_seconds": 23, "reconnect_seconds": 2, "redo_rounds": 1},
    {"id": "ten-lose-eight", "rounds": 10, "deadline_seconds": 23, "reconnect_seconds": 2, "redo_rounds": 8},
)


def _read(path):
    file = PROJECT / path
    if not file.is_file():
        file = BOOK / path
    return json.loads(file.read_text())


def _f(value):
    return float(value)


def _peak(device):
    return Fraction(str(hardware.select_peak(device, "BF16", "FP32", "tensor", "dense")["tera_ops_per_second"])) * 10**12


def calculate(decode_result="results/qwen3-8b-decode-b1-s8192.json",
              energy_ledger_result="results/energy-ledger-book.json",
              efficiency_record="experiments/ch08/08-01/efficiency.json",
              vision_result="results/vision-encoding-single.json",
              model="qwen3-8b", context_tokens=8192, q4_block_bytes=18, bf16_block_bytes=64,
              tokens_per_round=45, terminal_seconds="0.3", screenshot_bytes=800000,
              phone_joules_per_token=("0.576", "0.756"), tiers=DEFAULT_TIERS, cases=DEFAULT_CASES,
              variable_uplink=((10, 6000000), (10, 10000000)), constant_uplink_bits_per_second=8000000,
              uplink_scan_bits_per_second=(2000000, 20000000, 181),
              encoder_devices=("rtx4090", "h100-sxm"), encoder_uplink_bits_per_second=6400000,
              image_bytes=800000, fast_link_bits_per_second=400000000000, input_sources=None):
    inputs = {k: v for k, v in locals().items() if k != "input_sources"}
    sources = _sources(inputs, input_sources)
    for key in ("context_tokens", "q4_block_bytes", "bf16_block_bytes", "tokens_per_round", "screenshot_bytes", "image_bytes"):
        positive_int(inputs[key], key)
    terminal = exact(terminal_seconds, "terminal_seconds")
    decode = _read(decode_result)["summary"]
    weight_bf16 = decode["weight_read_once_per_operator_bytes"]
    kv = decode["kv_existing_history_unique_payload_bytes"]
    weight_q4 = weight_bf16 * q4_block_bytes // bf16_block_bytes
    step_bytes = weight_q4 + kv
    phone_bus = Fraction(str(_read(energy_ledger_result)["summary"]["phone_bus_gb_per_second"])) * 10**9
    j_low, j_high = (exact(v, "phone_joules_per_token") for v in phone_joules_per_token)
    record = _read(efficiency_record)
    measured = next(r for r in record["rows"] if r["context"] == context_tokens and r["batch"] == 1)
    measured_ratio = Fraction(str(measured["decode_round_ms"])) / Fraction(str(measured["peak_read_ms"]))
    prefill = prefill_flops(model, 0, context_tokens)

    rows = {}
    for tier in tiers:
        name = tier["name"]
        if tier["device"] is None:
            bandwidth, peak, power, device_name = phone_bus, None, None, "phone (4 x LPDDR5X x16)"
        else:
            device = hardware.select_device(tier["device"])
            bandwidth = Fraction(str(device["memory"]["bandwidth_bytes_per_second"]))
            peak, power, device_name = _peak(device), device["power_watts"], device["name"]
        step = Fraction(step_bytes) / bandwidth
        model_round = tokens_per_round * step
        prepare = Fraction(prefill) / peak if peak else Fraction(0)
        uplink = tier["uplink_bits_per_second"]
        upload = Fraction(screenshot_bytes * 8, uplink) if uplink else Fraction(0)
        rtt = exact(tier["rtt_seconds"], "rtt_seconds", allow_zero=True)
        round_seconds = terminal + model_round + rtt + upload
        scaled_model = model_round * measured_ratio if peak else None
        rows[name] = dict(
            tier=name, label=tier["label"], device=tier["device"], device_name=device_name,
            bandwidth_bytes_per_second=_f(bandwidth), bf16_dense_peak_flops=_f(peak) if peak else None,
            power_watts=power, step_bytes=step_bytes, step_seconds=_f(step), tokens_per_second=_f(1 / step),
            model_seconds_per_round=_f(model_round), prepare_seconds=_f(prepare),
            prepare_basis="8K-context prefill FLOPs / dense BF16 peak" if peak else "no archived matrix peak; set to 0",
            uplink_bits_per_second=uplink, upload_seconds_per_round=_f(upload), rtt_seconds=_f(rtt),
            terminal_seconds=_f(terminal), round_seconds=_f(round_seconds),
            measured_efficiency_model_seconds_per_round=_f(scaled_model) if scaled_model is not None else None,
            measured_efficiency_round_seconds=_f(round_seconds - model_round + scaled_model) if scaled_model is not None else None,
            _exact=dict(model=model_round, prepare=prepare, upload=upload, rtt=rtt, round=round_seconds,
                        scaled=scaled_model, power=power))

    def run(case):
        rounds = case["rounds"]
        deadline = exact(case["deadline_seconds"], "deadline_seconds")
        reconnect = exact(case.get("reconnect_seconds", 0), "reconnect_seconds", allow_zero=True)
        redo = case.get("redo_rounds", 0)
        out = []
        for name, row in rows.items():
            e = row["_exact"]
            remote = row["uplink_bits_per_second"] is not None
            extra_rounds = redo if remote else 0
            extra = (reconnect + redo * e["round"]) if remote and (reconnect or redo) else Fraction(0)
            total = e["prepare"] + rounds * e["round"] + extra
            executed = rounds + extra_rounds
            if e["power"] is None:
                energy = [executed * tokens_per_round * j_low, executed * tokens_per_round * j_high]
            else:
                busy = e["prepare"] + executed * e["model"]
                energy = [busy * e["power"]] * 2
            out.append(dict(tier=name, total_seconds=_f(total), meets_deadline=total <= deadline,
                            executed_rounds=executed, energy_joules=[_f(v) for v in energy],
                            extra_seconds=_f(extra)))
        feasible = [r for r in out if r["meets_deadline"]]
        choice = min(feasible, key=lambda r: r["energy_joules"][1])["tier"] if feasible else None
        return dict(case, rows=out, lowest_energy_feasible=choice)

    case_rows = [run(case) for case in cases]
    base = case_rows[0]
    rounds = base["rounds"]
    near, cloud = rows["near"]["_exact"], rows["cloud"]["_exact"]
    deadline = exact(base["deadline_seconds"], "deadline_seconds")
    cloud_fixed = cloud["prepare"] + rounds * (terminal + cloud["model"] + cloud["rtt"])
    upload_bits = rounds * screenshot_bytes * 8
    near_total = near["prepare"] + rounds * near["round"]
    deadline_uplink = Fraction(upload_bits) / (deadline - cloud_fixed)
    faster_slack = near_total - cloud_fixed
    faster_uplink = Fraction(upload_bits) / faster_slack if faster_slack > 0 else None
    # The same thresholds with both GPU model times scaled by the measured batch-1 ratio.
    cloud_fixed_m = cloud["prepare"] + rounds * (terminal + cloud["scaled"] + cloud["rtt"])
    near_total_m = near["prepare"] + rounds * (near["round"] - near["model"] + near["scaled"])
    faster_slack_m = near_total_m - cloud_fixed_m
    low, high, count = uplink_scan_bits_per_second
    scan = [low + (high - low) * i / (count - 1) for i in range(count)]
    variable = cloud_fixed + sum(n * Fraction(screenshot_bytes * 8, b) for n, b in variable_uplink)
    constant = cloud_fixed + Fraction(upload_bits, constant_uplink_bits_per_second)
    thresholds = dict(
        cloud_fixed_seconds=_f(cloud_fixed), upload_megabits=upload_bits / 10**6,
        near_total_seconds=_f(near_total),
        cloud_deadline_uplink_bits_per_second=_f(deadline_uplink),
        cloud_faster_than_near_uplink_bits_per_second=_f(faster_uplink) if faster_uplink else None,
        cloud_never_faster_reason=None if faster_uplink else "cloud time without upload already exceeds the nearby total",
        measured_ratio=_f(measured_ratio), measured_ratio_source=dict(file=efficiency_record, context=measured["context"],
                                                                       batch=1, decode_round_ms=measured["decode_round_ms"],
                                                                       peak_read_ms=measured["peak_read_ms"]),
        measured_cloud_fixed_seconds=_f(cloud_fixed_m), measured_near_total_seconds=_f(near_total_m),
        measured_cloud_faster_uplink_bits_per_second=_f(Fraction(upload_bits) / faster_slack_m) if faster_slack_m > 0 else None,
        variable_uplink=[list(x) for x in variable_uplink], variable_uplink_seconds=_f(variable),
        constant_uplink_bits_per_second=constant_uplink_bits_per_second, constant_uplink_seconds=_f(constant),
        scan_bits_per_second=scan, scan_cloud_seconds=[_f(cloud_fixed + Fraction(upload_bits) / Fraction(b)) for b in scan])

    vision = _read(vision_result)["summary"]
    flops = vision["matrix_flops_per_image"]
    feature = vision["complete_encoder_bytes_per_image"]
    encoders = []
    for identifier in encoder_devices:
        device = hardware.select_device(identifier)
        encoders.append(dict(device=identifier, device_name=device["name"], bf16_dense_peak_flops=_f(_peak(device)),
                             encode_seconds=_f(Fraction(flops) / _peak(device))))
    local, remote = (Fraction(flops) / _peak(hardware.select_device(i)) for i in encoder_devices)
    image_up = Fraction(image_bytes * 8, encoder_uplink_bits_per_second)
    feature_up = Fraction(feature * 8, encoder_uplink_bits_per_second)
    encoder = dict(matrix_flops_per_image=flops, feature_bytes=feature, image_bytes=image_bytes, devices=encoders,
                   local_device=encoder_devices[0], remote_device=encoder_devices[1],
                   uplink_bits_per_second=encoder_uplink_bits_per_second,
                   image_upload_seconds=_f(image_up), feature_upload_seconds=_f(feature_up),
                   local_path_seconds=_f(local + feature_up), remote_path_seconds=_f(image_up + remote),
                   encode_difference_seconds=_f(local - remote), transfer_difference_seconds=_f(feature_up - image_up),
                   fast_link_bits_per_second=fast_link_bits_per_second,
                   fast_link_transfer_difference_seconds=_f(Fraction((feature - image_bytes) * 8, fast_link_bits_per_second)))

    for row in rows.values():
        del row["_exact"]
    summary = dict(
        step_bytes=step_bytes, q4_weight_bytes=weight_q4, kv_bytes=kv, prefill_flops=prefill,
        end_model_seconds_per_round=rows["end"]["model_seconds_per_round"],
        near_model_seconds_per_round=rows["near"]["model_seconds_per_round"],
        cloud_model_seconds_per_round=rows["cloud"]["model_seconds_per_round"],
        near_prepare_seconds=rows["near"]["prepare_seconds"], cloud_prepare_seconds=rows["cloud"]["prepare_seconds"],
        totals_twenty_rounds_seconds=[r["total_seconds"] for r in base["rows"]],
        energy_twenty_rounds_joules=[r["energy_joules"] for r in base["rows"]],
        lowest_energy_feasible_twenty_rounds=base["lowest_energy_feasible"],
        cloud_deadline_uplink_mbit_per_second=thresholds["cloud_deadline_uplink_bits_per_second"] / 10**6,
        cloud_faster_than_near_uplink_mbit_per_second=(thresholds["cloud_faster_than_near_uplink_bits_per_second"] or 0) / 10**6 or None,
        measured_cloud_faster_uplink_mbit_per_second=(thresholds["measured_cloud_faster_uplink_bits_per_second"] or 0) / 10**6 or None,
        local_encode_seconds=encoders[0]["encode_seconds"], remote_encode_seconds=encoders[1]["encode_seconds"],
        fast_link_transfer_difference_ms=encoder["fast_link_transfer_difference_seconds"] * 1000)
    return dict(schema_version=1, calculation="edge-deployment-tiers", scenario=inputs, declared_input_sources=sources,
                summary=summary, tiers=list(rows.values()), cases=case_rows, uplink=thresholds, encoder=encoder,
                assumptions=[
                    "All tiers run one Qwen3-8B q4_0 checkpoint at 8K context and generate the same tokens per round; quality is fixed by construction.",
                    "Model time per round is tokens x (q4_0 weights + 8K KV) / memory bandwidth, the decode read lower bound used in 12.1.5.",
                    "Preparation is one 8K-context prefill at the dense BF16 peak; the phone has no archived matrix peak and is given zero, which only favours it.",
                    "GPU energy is TDP/TGP x busy seconds (an upper bound); phone energy is the MELTing Point measured 0.16-0.21 mWh per token.",
                    "Measured-efficiency rows scale both GPU model times by the RTX PRO 6000 batch-1 8K decode measurement of experiment 8-1.",
                    "Uplink, round-trip times, terminal time and reconnect times are declared network and task conditions.",
                    "A disconnection affects only remote tiers; redone rounds are executed again and counted again in energy.",
                ])
