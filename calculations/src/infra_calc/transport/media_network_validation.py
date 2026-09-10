"""Finite declared layout and shared network resource contract."""

from fractions import Fraction as F


def integer(value, name, minimum=0, maximum=2**62 - 1):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(name)


def nonnegative(value, name, positive=False):
    if type(value) is bool:
        raise ValueError(name)
    try:
        number = F(str(value))
    except (ValueError, ZeroDivisionError):
        raise ValueError(name)
    if number < 0 or (positive and number == 0):
        raise ValueError(name)
    return number


def validate_network(p, app):
    required = {
        "links",
        "until",
        "initial_cwnd",
        "initial_max_data",
        "initial_max_stream_data",
        "receive_memory_bytes",
    }
    optional = {
        "sender",
        "controller",
        "pad_in_flight",
        "ack_policy",
        "ack_bytes",
        "routers",
        "drop_packets",
        "consume_delay",
    }
    if (
        not isinstance(p, dict)
        or not required <= set(p)
        or set(p) - required - optional
    ):
        raise ValueError("network keys")
    nonnegative(p["until"], "until", True)
    integer(p["initial_cwnd"], "initial_cwnd", 2400)
    if type(p.get("pad_in_flight", True)) is not bool:
        raise ValueError("padding flag")
    integer(p.get("ack_bytes", 64), "ACK packet layout", 32, 1200)
    if p.get("consume_delay") is not None:
        nonnegative(p["consume_delay"], "consume_delay")
    for key in (
        "links",
        "initial_max_data",
        "initial_max_stream_data",
        "receive_memory_bytes",
    ):
        if not isinstance(p[key], dict) or set(p[key]) != {"up", "down"}:
            raise ValueError("direction keys " + key)
    for d in ("up", "down"):
        if set(p["links"][d]) != {"rate_bps", "propagation"}:
            raise ValueError("link keys")
        nonnegative(p["links"][d]["rate_bps"], "link rate", True)
        nonnegative(p["links"][d]["propagation"], "propagation")
        integer(p["initial_max_data"][d], "MAX_DATA")
        integer(p["receive_memory_bytes"][d], "receive memory")
        if not isinstance(p["initial_max_stream_data"][d], dict):
            raise ValueError("stream limits")
        for flow, limit in p["initial_max_stream_data"][d].items():
            if not isinstance(flow, str) or not flow:
                raise ValueError("stream id")
            integer(limit, "MAX_STREAM_DATA")
        if p["initial_max_data"][d] > p["receive_memory_bytes"][d]:
            raise ValueError("credit exceeds memory")
    for m in app["messages"]:
        if m["packetization"]["payload_limit_bytes"] > 1168:
            raise ValueError("message exceeds declared packet layout")
        d = "up" if m["sender"] == "client" else "down"
        if (
            m["transport"] == "stream"
            and m["flow_id"] not in p["initial_max_stream_data"][d]
        ):
            raise ValueError("missing stream limit")
    options = p.get("sender", {})
    if not isinstance(options, dict) or set(options) - {
        "rtt_seed",
        "numeric_quantum",
        "initial_rtt",
        "granularity",
        "max_ack_delay",
        "max_datagram_size",
    }:
        raise ValueError("unsupported sender overrides")
    if "max_datagram_size" in options and options["max_datagram_size"] != 1200:
        raise ValueError("declared network packet layout requires MDS1200")
    policy = p.get("ack_policy", "immediate_each_packet")
    expected = (
        F(str(policy.get("max_delay", "0.01"))) if isinstance(policy, dict) else F(0)
    )
    if "max_ack_delay" in options and F(str(options["max_ack_delay"])) != expected:
        raise ValueError("sender max_ack_delay conflicts with receiver")
    if p.get("controller") is not None:
        cc = p["controller"]
        if (
            not isinstance(cc, dict)
            or cc.get("name") not in ("newreno", "cubic_hystart", "bbr")
            or set(cc)
            - {
                "name",
                "pacing_gain",
                "time_quantum",
                "debt_quantum",
                "controller_quantum",
                "fast_convergence",
                "bbr_random_draws",
            }
        ):
            raise ValueError("controller profile")
    routers = p.get("routers", {})
    if not isinstance(routers, dict) or set(routers) - {"up", "down"}:
        raise ValueError("router directions")
    for router in routers.values():
        if set(router) - {"rate_bps", "queue_bytes", "propagation"} or not {
            "rate_bps",
            "queue_bytes",
        } <= set(router):
            raise ValueError("router fields")
        nonnegative(router["rate_bps"], "router rate", True)
        integer(router["queue_bytes"], "router queue")
        nonnegative(router.get("propagation", 0), "router propagation")
    loss = p.get("drop_packets", [])
    if not isinstance(loss, list) or len(loss) > 10000:
        raise ValueError("loss selectors")
    seen = set()
    for item in loss:
        if (
            not isinstance(item, dict)
            or set(item) != {"direction", "pn"}
            or item["direction"] not in ("up", "down")
        ):
            raise ValueError("loss selector")
        integer(item["pn"], "loss PN")
        key = (item["direction"], item["pn"])
        if key in seen:
            raise ValueError("duplicate loss selector")
        seen.add(key)
