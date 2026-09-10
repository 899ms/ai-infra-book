"""Application-byte and causal hand checks, independent of sending simulation."""

from pathlib import Path
import hashlib
import json
from fractions import Fraction as F
from normalize import load_sealed, normalize, packet_view

ROOT = Path(__file__).resolve().parent
source = load_sealed()
normalized = {name: normalize(name, value) for name, value in source.items()}
assert normalized == json.loads((ROOT / "normalized-inputs.json").read_text())
checks = []
for name, value in normalized.items():
    original = source[name]
    assert len(value["messages"]) == len(original["packets"])
    for before, after in zip(original["packets"], value["messages"]):
        assert after["id"] == before["id"] and after["bytes"] == before["payload_bytes"]
        assert F(after["ready_seconds"]) == F(str(before.get("ready", 0)))
        assert after["application_offset"] == before["offset"]
        assert [d["id"] for d in after["dependencies"]] == before.get(
            "dependencies", []
        )
        slices = list(packet_view(after))
        assert sum(p["bytes"] for p in slices) == before["payload_bytes"]
        assert all(1 <= p["bytes"] <= 1168 for p in slices)
        cursor = 0
        for fragment in slices:
            assert fragment["message_offset"] == cursor
            cursor += fragment["bytes"]
        assert all("pn" not in p and "send_time" not in p for p in slices)
    for before, after in zip(original.get("tasks", []), value["compute_tasks"]):
        assert F(after["duration_seconds"]) == F(str(before["duration"]))
        assert [d["id"] for d in after["dependencies"]] == before.get(
            "dependencies", []
        )
    checks.append(dict(scenario=name, status="passed", accounting=value["accounting"]))
image = normalized["image-30mb-5mb"]
assert image["accounting"]["application_bytes_by_direction"] == dict(
    client_to_server=30000000, server_to_client=5000000
)
assert image["accounting"]["fragment_count"] == 30800  # (1200+200) blocks *22.
assert image["messages"][0]["packetization"]["final_fragment_bytes"] == 472
mixed = normalized["mixed-priority"]
messages = {m["id"]: m for m in mixed["messages"]}
assert sum(messages[f"asr-{i}"]["bytes"] for i in range(8)) == 5120
assert sum(messages[f"tts-{i}"]["bytes"] for i in range(8)) == 7680
assert [F(messages[f"asr-{i}"]["ready_seconds"]) for i in range(8)] == [
    F(i + 1, 50) for i in range(8)
]
assert messages["screenshot-v1"]["bytes"] == 3443
assert mixed["accounting"]["application_bytes_by_direction"] == dict(
    client_to_server=30008595, server_to_client=5007808
)
assert mixed["accounting"]["application_bytes"] == 35016403
assert (
    messages["tts-0"]["transport"] == "datagram"
    and messages["tts-0"]["stream_offset"] is None
)
assert messages["screen-cancel"]["on_delivery_cancel_tags"] == ["screen-v1"]
tasks = {t["id"]: t for t in mixed["compute_tasks"]}
assert tasks["tts-produce-0"]["dependencies"] == [
    dict(id="asr-model", event="task_completed", endpoint="server")
]
assert sum(F(tasks[f"tts-produce-{i}"]["duration_seconds"]) for i in range(8)) == F(
    12, 125
)
preview = normalized["mixed-preview-priority"]
assert (
    preview["accounting"]["application_bytes"]
    - mixed["accounting"]["application_bytes"]
    == 500000
)
assert (
    sum(m["bytes"] for m in preview["messages"] if m["flow_id"] == "preview") == 500000
)
assert (
    next(t for t in preview["compute_tasks"] if t["id"] == "preview-model")[
        "duration_seconds"
    ]
    == "1/20"
)
assert normalized["screenshot-stale"]["business_observers"][0]["version_changes"] == [
    dict(endpoint="client", at_seconds="2/25", version="v2")
]
# Atomic datagrams cannot quietly turn into independently useful fragments.
try:
    list(packet_view(dict(messages["tts-0"], bytes=2000)))
except ValueError:
    pass
else:
    raise AssertionError("invented DATAGRAM fragmentation")
result = dict(
    status="passed",
    scenarios=checks,
    hand_oracles=dict(
        image_upload_bytes=30000000,
        image_final_bytes=5000000,
        asr_bytes=5120,
        tts_bytes=7680,
        mixed_bytes=35016403,
        preview_extra_bytes=500000,
        preview_extra_service_seconds="1/20",
        image_fragments_preserving_blocks=30800,
    ),
    hashes={
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in (
            "normalize.py",
            "check.py",
            "inputs.lock.json",
            "normalized-inputs.json",
        )
    },
)
(ROOT / "check-result.json").write_text(json.dumps(result, indent=2) + "\n")
print(
    json.dumps(
        dict(
            status="passed", scenarios=len(checks), hand_oracles=result["hand_oracles"]
        )
    )
)
