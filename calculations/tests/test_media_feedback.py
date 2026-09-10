"""Media DAG through the public feedback entry point, from independent hand cases."""

import copy
from fractions import Fraction as F
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from infra_calc.topics import transport_closed_loop


def message(
    identity,
    flow=None,
    sender="client",
    size=1168,
    offset=0,
    ready="0",
    priority=0,
    transport="stream",
    dependencies=None,
    cancel_tag=None,
    cancel_targets=None,
):
    return dict(
        id=identity,
        sender=sender,
        receiver="server" if sender == "client" else "client",
        flow_id=flow or identity,
        transport=transport,
        bytes=size,
        stream_offset=offset if transport == "stream" else None,
        application_offset=offset,
        ready_seconds=ready,
        dependencies=dependencies or [],
        priority=priority,
        source_order=0,
        deadline_seconds=None,
        allow_expire=False,
        cancel_tag=cancel_tag,
        on_delivery_cancel_tags=cancel_targets or [],
        packetization=dict(
            payload_limit_bytes=1168,
            fragment_count=(size + 1167) // 1168,
            final_fragment_bytes=(size - 1) % 1168 + 1,
            coalesce_across_messages=False,
        ),
    )


def task(identity, endpoint="server", duration="1", ready="0", cancel_tag=None):
    return dict(
        id=identity,
        endpoint=endpoint,
        resource="cpu",
        duration_seconds=duration,
        ready_seconds=ready,
        source_order=0,
        priority=0,
        dependencies=[],
        cancel_tag=cancel_tag,
    )


def dependency(identity, endpoint, event="message_delivered"):
    return dict(id=identity, endpoint=endpoint, event=event)


def inputs(messages, tasks=None, observers=None, **network_overrides):
    messages = copy.deepcopy(messages)
    for order, m in enumerate(messages):
        m["source_order"] = order
    tasks = copy.deepcopy(tasks or [])
    for order, t in enumerate(tasks):
        t["source_order"] = order
    app = dict(
        schema_version=1,
        id="public-hand-case",
        messages=messages,
        compute_tasks=tasks,
        business_observers=observers or [],
        scheduling=dict(
            send="fifo",
            compute="fifo",
            compute_nonpreemptive=True,
            resource_capacity_tasks=1,
        ),
        connection_ready_seconds="0",
    )
    limits = {"up": {}, "down": {}}
    for m in messages:
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
        pad_in_flight=True,
        consume_delay=None,
        sender=dict(rtt_seed=dict(latest_rtt=4, smoothed_rtt=4, rttvar=20, min_rtt=4)),
    )
    net.update(network_overrides)
    return dict(application=app, network=net)


def data(result, direction="up"):
    return [
        t
        for t in result["transmissions"]
        if t["direction"] == direction and t["message_id"]
    ]


class MediaFeedbackTests(unittest.TestCase):
    def calculate(self, value):
        original = copy.deepcopy(value)
        result = transport_closed_loop.calculate(value)
        self.assertEqual(value, original)
        return result

    def test_three_streams_share_initial_window(self):
        r = self.calculate(inputs([message(x) for x in ("A", "B", "C")]))
        # 1228 wire bytes at9824bps=1s; ACK92B at736bps=1s, each prop1s.
        self.assertEqual([F(t["send_start"]) for t in data(r)], [0, 1, 4])
        self.assertEqual([F(t["arrival"]) for t in data(r)], [2, 3, 6])
        self.assertEqual(r["summary"]["wire_bytes"], 3 * 1228 + 3 * 92)
        self.assertEqual(r["summary"]["delivered_application_bytes"], 3504)

    def test_other_stream_ACK_does_not_grant_flow_credit(self):
        p = inputs([message("A"), message("B")], until=10)
        p["network"]["initial_max_stream_data"]["up"]["A"] = 0
        p["network"]["initial_max_data"]["up"] = 1168
        r = self.calculate(p)
        self.assertEqual(set(r["delivered"]), {"B"})
        self.assertEqual(r["final_states"]["up"]["bytes_in_flight"], 0)
        self.assertEqual(r["final_states"]["up"]["max_stream_data"]["A"], 0)
        self.assertEqual(r["final_states"]["up"]["max_data_consumed"], 1168)

    def test_actual_MAX_arrival_and_its_ACK_serialization(self):
        p = inputs(
            [
                message("first", "A", size=100),
                message("second", "A", size=100, offset=100),
            ],
            consume_delay=0,
            until=60,
        )
        p["network"]["initial_max_stream_data"]["up"]["A"] = 100
        p["network"]["initial_max_data"]["up"] = 100
        r = self.calculate(p)
        update = next(
            t
            for t in r["transmissions"]
            if t["direction"] == "down" and t["kind"] == "max"
        )
        second = next(t for t in data(r) if t["message_id"] == "second")
        # MAX after reverse ACK: starts3, duration307/23, prop1 =>399/23.
        # The resulting pure ACK occupies up serializer23/307 before data.
        self.assertEqual(F(update["send_start"]), 3)
        self.assertEqual(F(update["arrival"]), F(399, 23))
        self.assertEqual(F(second["send_start"]), F(399, 23) + F(23, 307))
        self.assertEqual(r["final_states"]["up"]["max_data_consumed"], 200)

    def test_DATAGRAM_only_loss_PTO_sends_PING_not_duplicate_unit(self):
        p = inputs(
            [message("voice", size=960, transport="datagram")],
            drop_packets=[dict(direction="up", pn=0)],
        )
        r = self.calculate(p)
        units = [t for t in data(r) if t["message_id"] == "voice"]
        self.assertEqual(len(units), 1)
        self.assertTrue(units[0]["dropped"])
        probes = [
            t for t in r["transmissions"] if t["direction"] == "up" and t["probe"]
        ]
        self.assertTrue(probes)
        self.assertTrue(all(not t["frames"] for t in probes))
        self.assertEqual(r["final_states"]["up"]["max_data_consumed"], 0)
        self.assertNotIn("voice", r["delivered"])
        self.assertFalse(r["summary"]["complete"])

    def test_priority_selects_high_number_without_preemption(self):
        for policy, order, arrival in [
            ("fifo", ["bulk-0", "bulk-1", "voice"], 4),
            ("priority", ["bulk-0", "voice", "bulk-1"], 3),
        ]:
            with self.subTest(policy=policy):
                p = inputs(
                    [
                        message("bulk-0"),
                        message("bulk-1"),
                        message("voice", ready="1/2", priority=100),
                    ],
                    initial_cwnd=3600,
                )
                p["application"]["scheduling"]["send"] = policy
                r = self.calculate(p)
                self.assertEqual([t["message_id"] for t in data(r)], order)
                self.assertEqual([F(t["send_start"]) for t in data(r)], [0, 1, 2])
                self.assertEqual(F(r["delivered"]["voice"]), arrival)

    def test_cancel_waits_for_real_recovered_prefix_and_is_local(self):
        p = inputs(
            [
                message("prefix", "ctl", size=1),
                message("cancel", "ctl", size=1, offset=1, cancel_targets=["v1"]),
            ],
            tasks=[
                task("running", duration="20", cancel_tag="v1"),
                task("waiting", ready="1", cancel_tag="v1"),
                task("client", endpoint="client", cancel_tag="v1"),
            ],
            drop_packets=[dict(direction="up", pn=0)],
        )
        r = self.calculate(p)
        receipt = next(t for t in data(r) if t["message_id"] == "cancel")["arrival"]
        self.assertGreater(F(r["delivered"]["cancel"]), F(receipt))
        self.assertEqual(r["delivered"]["cancel"], r["delivered"]["prefix"])
        self.assertEqual(r["message_status"]["waiting"], "cancelled")
        self.assertEqual(F(r["delivered"]["running"]), 20)
        self.assertEqual(F(r["delivered"]["client"]), 1)

    def test_cancelled_unsent_hole_is_not_silently_delivered(self):
        p = inputs(
            [
                message("first", "A", size=100),
                message(
                    "middle", "A", size=100, offset=100, ready="5", cancel_tag="v1"
                ),
                message("last", "A", size=100, offset=200, ready="6"),
                message("cancel", sender="server", size=1, cancel_targets=["v1"]),
            ],
            links={d: dict(rate_bps=9824, propagation=1) for d in ("up", "down")},
            until=20,
        )
        r = self.calculate(p)
        self.assertEqual(r["message_status"]["middle"], "cancelled")
        self.assertNotIn("last", r["delivered"])
        self.assertIn("first", r["delivered"])
        self.assertEqual(r["final_states"]["up"]["max_data_consumed"], 300)
        self.assertEqual([t["message_id"] for t in data(r)], ["first", "last"])

    def test_local_version_can_invalidate_successful_delivery(self):
        for change, usable in [("1", False), ("20", True)]:
            with self.subTest(change=change):
                obs = dict(
                    id="screen",
                    kind="screenshot",
                    endpoint="client",
                    version="v1",
                    version_changes=[
                        dict(endpoint="client", at_seconds=change, version="v2")
                    ],
                    completion_dependencies=[dependency("action", "client")],
                )
                r = self.calculate(
                    inputs(
                        [message("action", sender="server", size=64)], observers=[obs]
                    )
                )
                self.assertTrue(r["businesses"][0]["all_required_delivered"])
                self.assertEqual(r["businesses"][0]["usable"], usable)

    def test_future_playback_is_not_reported_as_already_played(self):
        obs = dict(
            id="tts",
            kind="tts",
            endpoint="client",
            playback="slots",
            version_changes=[],
            completion_dependencies=[dependency("audio", "client")],
            blocks=[
                dict(
                    message_ids=["audio"], duration_seconds="1", slot_start_seconds="20"
                )
            ],
        )
        r = self.calculate(
            inputs(
                [message("audio", sender="server", size=960, transport="datagram")],
                observers=[obs],
                until=15,
            )
        )
        self.assertIn("audio", r["delivered"])
        self.assertIsNone(r["businesses"][0]["first_play"])
        self.assertIsNone(r["businesses"][0]["blocks"][0]["play_end"])
        self.assertFalse(r["businesses"][0]["complete"])

    def test_outer_shape_and_endpoint_bypass_rejected_without_mutation(self):
        base = inputs([message("A")])
        bad = [
            dict(base, unexpected=True),
            {"application": base["application"]},
            {"network": base["network"]},
        ]
        forged = copy.deepcopy(base)
        forged["application"]["messages"] = []
        forged["application"]["compute_tasks"] = [
            task("client", endpoint="client"),
            task("server"),
        ]
        forged["application"]["compute_tasks"][1].update(
            sender="client",
            dependencies=[dependency("client", "client", "task_completed")],
        )
        bad.append(forged)
        for value in bad:
            with self.subTest(keys=list(value)):
                before = copy.deepcopy(value)
                with self.assertRaises(ValueError):
                    transport_closed_loop.calculate(value)
                self.assertEqual(value, before)


if __name__ == "__main__":
    unittest.main()
