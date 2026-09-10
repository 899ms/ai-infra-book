"""Independent prewritten timing and causal oracles against real media feedback."""

from pathlib import Path
from fractions import Fraction as F
import copy
import hashlib
import importlib.util
import json

ROOT = Path(__file__).resolve().parent
CANDIDATE = ROOT.parent / "media-feedback-loop"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


engine = load(CANDIDATE / "calculate.py", "review_network")
normalizer = load(
    ROOT.parent / "media-feedback-inputs/normalize.py", "review_normalizer"
)
oracles = json.loads((ROOT / "oracles.json").read_text())
checks = []


def message(identity, flow=None, direction="c2s", size=1168, offset=0, **kw):
    return dict(
        id=identity,
        stream=flow or identity,
        direction=direction,
        payload_bytes=size,
        offset=offset,
        **kw
    )


def scenario(packets, tasks=None, businesses=None, **overrides):
    source = dict(
        packets=packets,
        tasks=tasks or [],
        businesses=businesses or [],
        scheduler="fifo",
        c2s_bits_per_second=9824,
        s2c_bits_per_second=736,
        c2s_propagation_seconds=1,
        s2c_propagation_seconds=1,
    )
    app = normalizer.normalize("independent", source)
    limits = {"up": {}, "down": {}}
    for m in app["messages"]:
        if m["transport"] == "stream":
            d = "up" if m["sender"] == "client" else "down"
            limits[d][m["flow_id"]] = max(
                limits[d].get(m["flow_id"], 0), m["stream_offset"] + m["bytes"]
            )
    net = dict(
        links={
            "up": dict(rate_bps=9824, propagation=1),
            "down": dict(rate_bps=736, propagation=1),
        },
        until=100,
        initial_cwnd=2400,
        initial_max_data={d: sum(v.values()) for d, v in limits.items()},
        initial_max_stream_data=limits,
        receive_memory_bytes={"up": 100000, "down": 100000},
        consume_delay=None,
        pad_in_flight=True,
        sender=dict(rtt_seed=dict(latest_rtt=4, smoothed_rtt=4, rttvar=20, min_rtt=4)),
    )
    net.update(overrides)
    return dict(application=app, network=net)


def trace(r, d, kind=None):
    return [
        t
        for t in r["transmissions"]
        if t["direction"] == d and (kind is None or t["kind"] == kind)
    ]


def run(name, p, check):
    before = {
        f: hashlib.sha256((CANDIDATE / f).read_bytes()).hexdigest()
        for f in (
            "calculate.py",
            "application.py",
            "sender.py",
            "application_validation.py",
            "network_validation.py",
        )
    }
    result = None
    try:
        result = engine.calculate(p)
        check(result)
    except Exception as error:
        checks.append(
            dict(
                case=name,
                status="FAIL",
                error=repr(error),
                inputs=p,
                actual_transmissions=(
                    None if result is None else result["transmissions"]
                ),
            )
        )
    else:
        checks.append(
            dict(
                case=name,
                status="PASS",
                summary=result["summary"],
                transmissions=len(result["transmissions"]),
            )
        )
    checks[-1]["candidate_hashes"] = before
    after = {
        f: hashlib.sha256((CANDIDATE / f).read_bytes()).hexdigest() for f in before
    }
    assert before == after, "candidate changed during case"
    return before


def shared(r):
    data = [t for t in trace(r, "up") if t["message_id"]]
    assert [F(t["send_start"]) for t in data] == [F(0), F(1), F(4)]
    assert [F(t["arrival"]) for t in data] == [F(2), F(3), F(6)]
    assert r["summary"]["wire_bytes"] == 3960
    assert r["summary"]["all_messages_delivered"]


run(
    "shared-cwnd-three-streams", scenario([message(x) for x in ("A", "B", "C")]), shared
)

p = scenario([message("A"), message("B")], until=10)
p["network"]["initial_max_stream_data"]["up"]["A"] = 0
p["network"]["initial_max_data"]["up"] = 1168


def flow(r):
    assert set(r["delivered"]) == {"B"}
    assert r["final_states"]["up"]["max_data_consumed"] == 1168
    assert r["final_states"]["up"]["max_stream_data"]["A"] == 0
    assert r["final_states"]["up"]["bytes_in_flight"] == 0


run("independent-stream-limit-not-opened-by-other-ACK", p, flow)

# Explicit MAX packet carries both absolute limits; its actual arrival enables
# the second range. At t2 ACK takes down serializer2..3, then padded MAX takes
# 307/23s and propagates1s, so credit arrives399/23. Its pure ACK occupies the up serializer for
# 23/307s before second data starts; MAX authorization itself needs no ACK.
p = scenario(
    [message("first", "A", size=100), message("second", "A", size=100, offset=100)],
    consume_delay=0,
    until=60,
)
p["network"]["initial_max_stream_data"]["up"]["A"] = 100
p["network"]["initial_max_data"]["up"] = 100


def actual_max(r):
    update = next(t for t in trace(r, "down") if t["kind"] == "max")
    second = next(t for t in trace(r, "up") if t["message_id"] == "second")
    assert F(update["send_start"]) == 3
    assert F(update["arrival"]) == F(399, 23)
    assert F(second["send_start"]) == F(399, 23) + F(23, 307)
    assert r["final_states"]["up"]["max_data_consumed"] == 200
    assert "second" in r["delivered"]


run("actual-MAX-arrival-opens-both-absolute-limits", p, actual_max)


p = scenario(
    [
        message("voice-0", size=960, reliable=False),
        message("voice-1", size=960, reliable=False),
    ],
    until=100,
    drop_packets=[dict(direction="up", pn=0)],
)


def datagram(r):
    units = [t for t in r["transmissions"] if t["message_id"] == "voice-0"]
    assert len(units) == 1 and units[0]["dropped"]
    assert "voice-0" not in r["delivered"] and "voice-1" in r["delivered"]
    assert r["final_states"]["up"]["max_data_consumed"] == 0
    assert r["summary"]["unique_received_application_bytes"] == 960
    assert all(
        f.get("id") != "voice-0"
        for t in r["transmissions"]
        if t is not units[0]
        for f in t["frames"]
    )


run("datagram-dropped-once-never-retransmitted", p, datagram)

p = scenario(
    [message("voice-only", size=960, reliable=False)],
    until=100,
    drop_packets=[dict(direction="up", pn=0)],
)


def datagram_pto(r):
    units = [t for t in r["transmissions"] if t["message_id"] == "voice-only"]
    assert len(units) == 1 and units[0]["dropped"]
    assert "voice-only" not in r["delivered"]
    probes = [t for t in trace(r, "up") if t["probe"]]
    assert probes and all(not t["frames"] for t in probes)
    assert r["final_states"]["up"]["max_data_consumed"] == 0
    assert r["summary"]["unique_received_application_bytes"] == 0


run("datagram-only-PTO-real-PING-without-retransmitted-unit", p, datagram_pto)


# Missing cancel prefix is recovered only by real sender PTO/loss/ACK processing.
p = scenario(
    [
        message("prefix", "ctl", size=1),
        message("cancel", "ctl", size=1, offset=1, cancel_targets=["v1"]),
    ],
    tasks=[
        dict(id="running", dependencies=[], duration=20, cancel_tag="v1"),
        dict(id="waiting", dependencies=[], ready=1, duration=1, cancel_tag="v1"),
        dict(
            id="client",
            endpoint="client",
            resource="cpu",
            dependencies=[],
            duration=1,
            cancel_tag="v1",
        ),
    ],
    drop_packets=[dict(direction="up", pn=0)],
)


def cancel(r):
    first_cancel = next(t for t in r["transmissions"] if t["message_id"] == "cancel")
    assert F(r["delivered"]["cancel"]) > F(first_cancel["arrival"])
    assert F(r["delivered"]["cancel"]) == F(r["delivered"]["prefix"])
    assert r["message_status"]["waiting"] == "cancelled"
    assert F(r["delivered"]["running"]) == 20 and F(r["delivered"]["client"]) == 1
    assert any(
        t["recovery_of"] is not None or t["probe_of"] is not None
        for t in r["transmissions"]
    )


run("cancel-held-by-real-recovered-prefix-and-local-scope", p, cancel)

p = scenario(
    [
        message("first", "result", size=100),
        message("middle", "result", size=100, offset=100, ready=5, cancel_tag="v1"),
        message("last", "result", size=100, offset=200, ready=6),
        message("cancel", direction="s2c", size=1, cancel_targets=["v1"]),
    ],
    links={
        "up": dict(rate_bps=9824, propagation=1),
        "down": dict(rate_bps=9824, propagation=1),
    },
    until=20,
)


def hole(r):
    assert r["message_status"]["middle"] == "cancelled"
    assert "last" not in r["delivered"] and "first" in r["delivered"]
    assert r["final_states"]["up"]["max_data_consumed"] == 300
    assert not any(t["message_id"] == "middle" for t in r["transmissions"])
    assert any(t["message_id"] == "last" for t in r["transmissions"])


run("cancelled-unsent-gap-preserved", p, hole)

for policy, order, voice_at in [
    ("fifo", ["bulk-0", "bulk-1", "voice"], 4),
    ("priority", ["bulk-0", "voice", "bulk-1"], 3),
]:
    p = scenario(
        [
            message("bulk-0"),
            message("bulk-1"),
            message("voice", ready="1/2", priority=100),
        ],
        initial_cwnd=3600,
    )
    p["application"]["scheduling"]["send"] = policy

    def scheduling(r, order=order, voice_at=voice_at):
        rows = [t for t in trace(r, "up") if t["message_id"]]
        assert [t["message_id"] for t in rows] == order
        assert [F(t["send_start"]) for t in rows] == [F(0), F(1), F(2)]
        assert F(r["delivered"]["voice"]) == voice_at

    run("nonpreemptive-" + policy, p, scheduling)

p = scenario(
    [message("up"), message("down", direction="s2c")],
    ack_policy=dict(mode="count_or_timer", every=1, max_delay=0),
)


def reverse(r):
    ack = next(t for t in trace(r, "down") if t["kind"] == "ack")
    assert F(ack["send_start"]) == F(307, 23)
    assert F(ack["arrival"]) == F(353, 23)
    assert F(ack["ack_snapshot"]["raw_delay"]) == F(261, 23)
    assert ack["ack_snapshot"]["encoded_delay"] == 1418478


run("reverse-data-blocks-ACK", p, reverse)

# Full source screenshot workload; only local version observation changes.
apps = json.loads(
    (ROOT.parent / "media-feedback-inputs/normalized-inputs.json").read_text()
)
for stale in (False, True):
    app = copy.deepcopy(apps["screenshot-complete"])
    if stale:
        app["business_observers"][0]["version_changes"] = [
            dict(endpoint="client", at_seconds="2/25", version="v2")
        ]
    p = scenario([])
    p["application"] = app
    p["network"].update(
        links={
            "up": dict(rate_bps=20000000, propagation="1/20"),
            "down": dict(rate_bps=100000000, propagation="1/20"),
        },
        initial_max_data={"up": 3443, "down": 64},
        initial_max_stream_data={
            "up": {"screen-up": 3443},
            "down": {"screen-result": 64},
        },
    )

    def screenshot(r, stale=stale):
        observer = r["businesses"][0]
        assert observer["all_required_delivered"] and observer["usable"] == (not stale)
        assert (
            len([t for t in trace(r, "up") if t["message_id"] == "screenshot-v1"]) == 3
        )
        assert len(r["work"]) == 1 and r["work"][0]["finished"]

    hashes = run("screenshot-" + ("stale" if stale else "current"), p, screenshot)
report = dict(
    status="PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL",
    checks=checks,
    candidate_hashes=hashes,
    oracle_sha256=hashlib.sha256((ROOT / "oracles.json").read_bytes()).hexdigest(),
    checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    scope="Small actual network scenarios; no injected recovery timestamps. MAX growth arrival algebra separately covered by sender review; no large-workload claim.",
)
(ROOT / "network-independent.json").write_text(json.dumps(report, indent=2) + "\n")
print(
    json.dumps(
        dict(
            status=report["status"],
            checks=[{k: v for k, v in c.items() if k != "inputs"} for c in checks],
        )
    )
)
