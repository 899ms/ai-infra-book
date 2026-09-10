"""Compare the five completed wireless workloads only after trace review.

All business metrics come from generated, hash-bound outputs. Pairing checks
ensure wireless is the only change from the original WAN workload and that the
mixed grid varies only source scheduling and transport ACK policy.
"""
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
RUNS = RESEARCH / "shared-airtime-book-inputs/runs"
CASES = ("image-baseline", "mixed-fifo-immediate", "mixed-fifo-aggregate",
         "mixed-priority-immediate", "mixed-priority-aggregate")


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1048576):
            digest.update(block)
    return digest.hexdigest()


def main():
    evidence = {}

    def read(path):
        evidence[str(path)] = sha(path)
        return json.loads(path.read_text())

    rows = []
    common_grid = None
    for case in CASES:
        manifest_path = RUNS / f"{case}-manifest.json"
        manifest = read(manifest_path)
        assert manifest["status"] == "COMPLETE_STABLE_IDENTITY_NOT_INDEPENDENT_ACCEPTANCE", case
        assert manifest["source_hashes_before"] == manifest["source_hashes_after"], case
        result_path = RUNS / manifest["result_file"]
        evidence[str(result_path)] = sha(result_path)
        assert evidence[str(result_path)] == manifest["result_sha256"], case
        summary_path = RUNS / manifest["summary_file"]
        summary = read(summary_path)
        assert evidence[str(summary_path)] == manifest["summary_sha256"], case
        review = read(RESEARCH / f"shared-airtime-trace-review/{case}-check.json")
        assert review["status"] == "passed" and review["full_saved_trace_checked"], case
        assert review["result_sha256"] == manifest["result_sha256"], case
        assert review["generation_manifest_sha256"] == evidence[str(manifest_path)], case
        current = read(RUNS / f"{case}-inputs.json")
        assert evidence[str(RUNS / f"{case}-inputs.json")] == manifest["inputs_sha256"], case
        old_root = RESEARCH / "media-feedback-loop"
        old_manifest = read(old_root / f"runs/book-{case}-manifest.json")
        assert old_manifest["status"] == "COMPLETE_STABLE_IDENTITY_NOT_INDEPENDENT_ACCEPTANCE", case
        assert old_manifest["case"] == case and old_manifest["pilot"] is False, case
        assert old_manifest["source_hashes_before"] == old_manifest["source_hashes_after"], case
        original_path = old_root / old_manifest["effective_input_file"]
        original = read(original_path)
        assert evidence[str(original_path)] == old_manifest["effective_input_sha256"], case
        old_result_path = old_root / old_manifest["result_file"]
        evidence[str(old_result_path)] = sha(old_result_path)
        assert evidence[str(old_result_path)] == old_manifest["result_sha256"], case
        stripped = deepcopy(current)
        stripped["network"].pop("wireless_access")
        assert stripped == original, (case, "only wireless_access may change")
        if case != "image-baseline":
            invariant = deepcopy(current)
            invariant["network"].pop("ack_policy")
            invariant["application"]["scheduling"].pop("send")
            if common_grid is None:
                common_grid = invariant
            assert invariant == common_grid, (case, "mixed grid changed other fields")
        businesses = {item["id"]: item for item in summary["businesses"]}
        tts = businesses.get("tts")
        old_summary_path = old_root / old_manifest["summary_file"]
        old_summary = read(old_summary_path)
        assert evidence[str(old_summary_path)] == old_manifest["summary_sha256"], case
        assert old_summary["effective_input_sha256"] == old_manifest["effective_input_sha256"], case
        assert old_summary["result_sha256"] == old_manifest["result_sha256"], case
        old_image = next(item for item in old_summary["businesses"] if item["id"] == "image")
        image_time = F(businesses["image"]["complete_at"])
        rows.append({
            "case": case,
            "image_complete_seconds": str(image_time),
            "same_input_wan_only_image_seconds": old_image["complete_at"],
            "additional_image_seconds": str(image_time - F(old_image["complete_at"])),
            "wan_ip_bytes": str(F(summary["summary"]["wan_serialized_ip_bytes_by_horizon"])),
            "wireless_reserved_seconds": summary["wireless_summary"]["observed_reserved_seconds"],
            "wireless_attempts": summary["wireless_summary"]["attempts_started"],
            "same_pn_mac_retries": summary["wireless_summary"]["same_pn_retry_attempts"],
            "unique_received_application_bytes": summary["summary"]["unique_received_application_bytes"],
            "played_blocks": None if tts is None else sum(block["play_end"] is not None for block in tts["blocks"]),
            "missing_audio_seconds": None if tts is None else tts["missing_audio_seconds"],
            "screenshot_usable": businesses.get("computer-use", {}).get("usable"),
            "all_business_complete": summary["summary"]["complete"],
        })
    report = {"status": "passed_five_trace_review_bindings_and_input_pairing",
              "scope": "Fixed legacy OFDM reference, no MAC failures; not measured Wi-Fi, TCP/TACK or complete C69 acceptance.",
              "rows": rows, "evidence_hashes": evidence, "script_sha256": sha(Path(__file__))}
    for name, digest in evidence.items():
        assert sha(Path(name)) == digest, (name, "changed during comparison")
    (HERE / "comparison.json").write_text(json.dumps(report, indent=2) + "\n")
    lines = ["# 完整共享空口对照", "", report["scope"], "",
             "| 场景 | 完整图片 s | 无线预约服务 s | WAN IP B | 已播块 | 缺音 s | 截图可用 |",
             "| --- | ---: | ---: | ---: | ---: | ---: | --- |"]
    for row in rows:
        played = "—" if row["played_blocks"] is None else str(row["played_blocks"])
        missing = "—" if row["missing_audio_seconds"] is None else f'{float(F(row["missing_audio_seconds"])):.2f}'
        usable = "—" if row["screenshot_usable"] is None else str(row["screenshot_usable"])
        lines.append(f'| {row["case"]} | {float(F(row["image_complete_seconds"])):.9f} | {float(F(row["wireless_reserved_seconds"])):.6f} | {row["wan_ip_bytes"]} | {played} | {missing} | {usable} |')
    lines += ["", "精确分数、各自无无线基线、输入配对与逐轨迹审查身份见 comparison.json。",
              "WAN和无线可以流水重叠，累计无线服务不能直接加到基线完成时刻；业务完成后可能仍有确认服务。",
              "五例仅新增 wireless_access；四格之间只改变 source send scheduling 与 transport ACK policy。",
              "队列排空不证明音频按时播放或截图动作有效。结果不外推为生产无线吞吐或等质量编解码性能。", ""]
    (HERE / "COMPARISON.md").write_text("\n".join(lines))
    print("passed five paired full results and their complete trace reviews")


if __name__ == "__main__":
    main()
