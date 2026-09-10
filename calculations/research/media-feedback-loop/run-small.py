"""Small real-feedback cases; old teaching recovery times are not imported."""

from pathlib import Path
import copy
import hashlib
import json
import calculate

ROOT = Path(__file__).resolve().parent


def network(app):
    limits = {"up": {}, "down": {}}
    for m in app["messages"]:
        if m["transport"] == "stream":
            d = "up" if m["sender"] == "client" else "down"
            flow = m["flow_id"]
            limits[d][flow] = max(
                limits[d].get(flow, 0), m["stream_offset"] + m["bytes"]
            )
    return dict(
        links={d: dict(rate_bps=9824, propagation=1) for d in ("up", "down")},
        until=60,
        initial_cwnd=2400,
        initial_max_data={d: sum(limits[d].values()) for d in limits},
        initial_max_stream_data=limits,
        receive_memory_bytes={d: 100000 for d in limits},
        pad_in_flight=True,
        consume_delay=None,
        sender=dict(rtt_seed=dict(latest_rtt=4, smoothed_rtt=4, rttvar=2, min_rtt=4)),
    )


def inputs():
    normalized = json.loads(
        (ROOT.parent / "media-feedback-inputs/normalized-inputs.json").read_text()
    )
    names = (
        "credit-3-streams",
        "schedule-fifo",
        "schedule-priority",
        "playback-reliable",
        "playback-slots",
        "cancel-running-work",
        "screenshot-complete",
        "screenshot-stale",
        "unreliable-loss-credit",
    )
    out = {
        name: dict(
            application=copy.deepcopy(normalized[name]),
            network=network(normalized[name]),
        )
        for name in names
    }
    # Explicit actual PN selectors replace all prescribed legacy recovery_ready inputs.
    out["unreliable-loss-credit"]["network"]["drop_packets"] = [
        dict(direction="up", pn=0)
    ]
    blocked = copy.deepcopy(out["credit-3-streams"])
    blocked["network"]["initial_max_stream_data"]["up"]["s0"] = 0
    out["one-stream-blocked-other-progress"] = blocked
    loss = copy.deepcopy(out["credit-3-streams"])
    loss["network"]["drop_packets"] = [dict(direction="up", pn=0)]
    out["reliable-loss-recovery"] = loss
    consume = copy.deepcopy(out["credit-3-streams"])
    consume["network"].update(
        initial_max_data={"up": 1, "down": 0},
        receive_memory_bytes={"up": 1, "down": 100000},
        consume_delay="1/2",
    )
    out["shared-credit-consumption"] = consume
    ack = copy.deepcopy(out["credit-3-streams"])
    ack["network"]["ack_policy"] = dict(
        mode="count_or_timer", every=2, max_delay="0.01", delay_exponent=3
    )
    out["shared-credit-aggregate-ack"] = ack
    tail = copy.deepcopy(out["unreliable-loss-credit"])
    tail["application"]["messages"] = tail["application"]["messages"][:1]
    keep = tail["application"]["messages"][0]["id"]
    for observer in tail["application"]["business_observers"]:
        observer["completion_dependencies"] = [
            x for x in observer["completion_dependencies"] if x["id"] == keep
        ]
    tail["application"]["accounting"].update(
        application_bytes=1,
        message_count=1,
        fragment_count=1,
        application_bytes_by_direction={"client_to_server": 1, "server_to_client": 0},
    )
    out["datagram-tail-pto-ping"] = tail
    return out


if __name__ == "__main__":
    scenarios = inputs()
    (ROOT / "scenarios.json").write_text(json.dumps(scenarios, indent=2) + "\n")
    hashes = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in ROOT.glob("*.py")
        if not p.name.startswith("check")
    }
    results = {}
    for name, p in scenarios.items():
        results[name] = calculate.calculate(p)
        print(name, results[name]["summary"], flush=True)
    assert hashes == {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in ROOT.glob("*.py")
        if not p.name.startswith("check")
    }
    (ROOT / "result.json").write_text(json.dumps(results, indent=2) + "\n")
    (ROOT / "result-manifest.json").write_text(
        json.dumps(
            dict(
                status="initial-small-candidate-not-final",
                code_hashes=hashes,
                scenario_count=len(results),
                result_sha256=hashlib.sha256(
                    (ROOT / "result.json").read_bytes()
                ).hexdigest(),
            ),
            indent=2,
        )
        + "\n"
    )
