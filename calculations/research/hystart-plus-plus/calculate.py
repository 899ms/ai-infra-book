"""RFC9406 HyStart++ startup reference; explicit ACK/RTT/sequence callbacks."""

import argparse
import copy
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def rational(x, positive=True):
    if isinstance(x, bool):
        raise ValueError("boolean is not a rational")
    try:
        value = F(str(x))
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("invalid rational") from exc
    if value < 0 or (positive and not value):
        raise ValueError("invalid sign")
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > 4096:
        raise ValueError("rational budget")
    return value


def integer(x, minimum=0):
    if type(x) is not int or not minimum <= x <= 2**62 - 1:
        raise ValueError("invalid bounded integer")
    return x


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, list):
        return [encode(v) for v in value]
    return value


def verify_sources():
    rows = json.loads((ROOT / "sources.lock.json").read_text())
    for row in rows:
        data = (ROOT / row["file"]).read_bytes()
        if (
            len(data) != row["bytes"]
            or hashlib.sha256(data).hexdigest() != row["sha256"]
        ):
            raise ValueError("source hash mismatch")
    return rows


class Startup:
    def __init__(self, p):
        allowed = {
            "smss",
            "initial_cwnd",
            "initial_snd_nxt",
            "initial_acked_seq",
            "paced",
            "initial_slow_start",
            "constants",
            "events",
        }
        if not isinstance(p, dict) or set(p) - allowed:
            raise ValueError("unknown input")
        self.smss = integer(p.get("smss", 1000), 1)
        self.cwnd = rational(p.get("initial_cwnd", 10000))
        self.snd_nxt = integer(p.get("initial_snd_nxt", 8000), 1)
        self.acked_seq = integer(p.get("initial_acked_seq", 0))
        if self.acked_seq >= self.snd_nxt:
            raise ValueError("initial flight must contain unacknowledged bytes")
        self.confirmed_bytes = self.acked_seq
        self.paced = p.get("paced", False)
        initial = p.get("initial_slow_start", True)
        if type(self.paced) is not bool or type(initial) is not bool:
            raise ValueError("policy flags must be bool")
        constants = p.get("constants", {})
        if not isinstance(constants, dict) or set(constants) - {
            "min_rtt_thresh",
            "max_rtt_thresh",
            "min_rtt_divisor",
            "n_rtt_sample",
            "css_growth_divisor",
            "css_rounds",
        }:
            raise ValueError("unknown tuning constant")
        self.min_thresh = rational(constants.get("min_rtt_thresh", "0.004"))
        self.max_thresh = rational(constants.get("max_rtt_thresh", "0.016"))
        self.rtt_divisor = rational(constants.get("min_rtt_divisor", 8))
        self.samples_required = integer(constants.get("n_rtt_sample", 8), 1)
        self.css_divisor = integer(constants.get("css_growth_divisor", 4), 2)
        self.css_round_limit = integer(constants.get("css_rounds", 5), 1)
        if self.min_thresh > self.max_thresh:
            raise ValueError("threshold order")
        self.phase = "slow_start" if initial else "standard_slow_start_handoff"
        self.hystart_enabled = initial
        self.window_end = self.snd_nxt
        self.round = 1
        self.last_min = None
        self.current_min = None
        self.samples = 0
        self.sample_ids = set()
        self.css_baseline = None
        self.css_completed = 0
        self.ssthresh = None
        self.handoff = (
            None
            if initial
            else {"reason": "not_initial_slow_start", "policy": "standard_slow_start"}
        )
        self.now = F(0)

    def state(self):
        return dict(
            phase=self.phase,
            cwnd=self.cwnd,
            ssthresh=self.ssthresh,
            snd_nxt=self.snd_nxt,
            acked_seq=self.acked_seq,
            confirmed_bytes=self.confirmed_bytes,
            window_end=self.window_end,
            round=self.round,
            last_round_min_rtt=self.last_min,
            current_round_min_rtt=self.current_min,
            rtt_sample_count=self.samples,
            css_baseline_min_rtt=self.css_baseline,
            completed_css_rounds=self.css_completed,
            hystart_enabled=self.hystart_enabled,
            handoff=copy.deepcopy(self.handoff),
        )

    def finish(self, reason):
        self.phase = "congestion_avoidance_handoff"
        self.ssthresh = self.cwnd
        self.hystart_enabled = False
        self.handoff = dict(
            reason=reason,
            policy="congestion_avoidance",
            cwnd=self.cwnd,
            ssthresh=self.ssthresh,
            congestion_reduction_applied=False,
        )

    def sample(self, e):
        rtt = e.get("rtt")
        if rtt is None:
            if e.get("rtt_sample_id") is not None:
                raise ValueError("sample id without RTT")
            return False
        sample_id = e.get("rtt_sample_id")
        if (
            not isinstance(sample_id, str)
            or not sample_id
            or sample_id in self.sample_ids
        ):
            raise ValueError("RTT samples require distinct identities")
        rtt = rational(rtt)
        self.sample_ids.add(sample_id)
        self.current_min = (
            rtt if self.current_min is None else min(self.current_min, rtt)
        )
        self.samples += 1
        return True

    def acknowledge(self, e):
        if self.phase not in ("slow_start", "css"):
            raise ValueError("ACK growth belongs to handed-off controller")
        seq = integer(e["ack_seq"])
        n = integer(e["newly_acked_bytes"])
        if (
            not self.acked_seq <= seq <= self.snd_nxt
            or not seq <= self.confirmed_bytes + n <= self.snd_nxt
        ):
            raise ValueError("ACK exceeds locally sent sequence/unique byte budget")
        valid_sample = self.sample(e)
        self.acked_seq = seq
        self.confirmed_bytes += n
        before = self.phase
        increment = F(n if self.paced else min(n, 8 * self.smss))
        if before == "css":
            increment /= self.css_divisor
        self.cwnd += increment
        detail = dict(
            growth_phase=before, increment=increment, new_rtt_sample=valid_sample
        )
        if self.samples >= self.samples_required and self.current_min is not None:
            if before == "slow_start" and self.last_min is not None:
                threshold = max(
                    self.min_thresh,
                    min(self.last_min / self.rtt_divisor, self.max_thresh),
                )
                detail["rtt_threshold"] = threshold
                if self.current_min >= self.last_min + threshold:
                    self.phase = "css"
                    self.css_baseline = self.current_min
                    self.css_completed = 0
                    detail["transition"] = "enter_css"
            elif before == "css" and self.current_min < self.css_baseline:
                self.phase = "slow_start"
                self.css_baseline = None
                self.css_completed = 0
                detail["transition"] = "resume_slow_start"
        if self.window_end is not None and seq >= self.window_end:
            detail["completed_round"] = self.round
            if self.phase == "css":
                self.css_completed += 1
                if self.css_completed >= self.css_round_limit:
                    self.finish("css_round_limit")
                    detail["transition"] = "enter_congestion_avoidance"
            self.last_min = self.current_min
            self.current_min = None
            self.samples = 0
            self.round += 1
            self.window_end = self.snd_nxt if self.snd_nxt > seq else None
        return detail

    def step(self, e):
        schemas = {
            "sent": ({"snd_nxt"}, set()),
            "ack": ({"ack_seq", "newly_acked_bytes"}, {"rtt", "rtt_sample_id"}),
            "congestion": ({"signal"}, set()),
            "restart": (set(), set()),
            "observe": (set(), set()),
        }
        if not isinstance(e, dict) or e.get("type") not in schemas:
            raise ValueError("unknown event")
        required, optional = schemas[e["type"]]
        required = required | {"at", "type"}
        if required - set(e) or set(e) - required - optional:
            raise ValueError("missing/unknown event field")
        at = rational(e["at"], False)
        if at < self.now:
            raise ValueError("events must be chronological")
        before = self.state()
        detail = {}
        kind = e["type"]
        if kind == "sent":
            nxt = integer(e["snd_nxt"])
            if nxt < self.snd_nxt:
                raise ValueError("SND.NXT cannot retreat")
            self.snd_nxt = nxt
            if self.window_end is None and nxt > self.acked_seq:
                self.window_end = nxt
        elif kind == "ack":
            detail = self.acknowledge(e)
        elif kind == "congestion":
            if e["signal"] not in ("loss", "ecn") or self.phase not in (
                "slow_start",
                "css",
            ):
                raise ValueError("invalid startup congestion callback")
            self.finish(e["signal"])
        elif kind == "restart":
            if self.hystart_enabled:
                raise ValueError("exit initial startup before subsequent restart")
            self.phase = "standard_slow_start_handoff"
            self.handoff = dict(
                reason="subsequent_restart",
                policy="standard_slow_start",
                cwnd=self.cwnd,
                ssthresh=self.ssthresh,
            )
        self.now = at
        return dict(
            event=copy.deepcopy(e), before=before, details=detail, after=self.state()
        )


def calculate(inputs=None):
    p = copy.deepcopy(example() if inputs is None else inputs)
    sources = verify_sources()
    s = Startup(p)
    initial = s.state()
    events = p.get("events", [])
    if not isinstance(events, list) or len(events) > 10000:
        raise ValueError("finite event budget")
    trace = [s.step(e) for e in events]
    return encode(
        dict(
            inputs=p,
            initial=initial,
            events=trace,
            final=s.state(),
            reference_sources=sources,
            scope="RFC9406 initial startup reference with explicit round-boundary policy; controller/network handoff only",
        )
    )


def example():
    events = []
    for rnd in range(1, 7):
        for j in range(1, 9):
            count = (rnd - 1) * 8 + j
            if j == 8 and rnd < 6:
                events.append(
                    dict(
                        type="sent",
                        at=str(F(count) - F(1, 2)),
                        snd_nxt=(rnd + 1) * 8000,
                    )
                )
            events.append(
                dict(
                    type="ack",
                    at=count,
                    ack_seq=count * 1000,
                    newly_acked_bytes=1000,
                    rtt="0.01" if rnd == 1 else "0.014",
                    rtt_sample_id=f"rtt-{count}",
                )
            )
    return dict(smss=1000, initial_cwnd=10000, initial_snd_nxt=8000, events=events)


def scenarios():
    out = {"css-five-rounds": example()}
    for paced in (False, True):
        out["paced-growth" if paced else "unpaced-growth"] = dict(
            initial_snd_nxt=20000,
            paced=paced,
            events=[dict(type="ack", at=1, ack_seq=20000, newly_acked_bytes=20000)],
        )
    partial = example()
    partial["events"] = partial["events"][:17]
    out["seven-samples-no-css"] = partial
    jitter = example()
    for e in jitter["events"]:
        if e["type"] == "ack" and 17 <= e["at"] <= 24:
            e["rtt"] = "0.013"
    out["jitter-resume"] = jitter
    no_sample = example()
    for e in no_sample["events"]:
        if e["type"] == "ack":
            e.pop("rtt")
            e.pop("rtt_sample_id")
    out["no-rtt-samples"] = no_sample
    for signal in ("loss", "ecn"):
        out[signal + "-handoff"] = dict(
            initial_snd_nxt=8000,
            events=[
                dict(type="congestion", at=1, signal=signal),
                dict(type="restart", at=2),
            ],
        )
    for paced in (False, True):
        css = example()
        css["paced"] = paced
        css["events"] = [e for e in css["events"] if F(str(e["at"])) <= 16]
        css["events"] += [
            dict(type="sent", at="16.5", snd_nxt=40000),
            dict(type="ack", at=17, ack_seq=36000, newly_acked_bytes=20000),
        ]
        out["paced-css-growth" if paced else "unpaced-css-growth"] = css
    sparse = example()
    sparse["events"] = [e for e in sparse["events"] if F(str(e["at"])) <= 24]
    for e in sparse["events"]:
        if e["type"] == "ack" and 17 <= e["at"] <= 23:
            e["rtt"] = "0.013"
        elif e["type"] == "ack" and e["at"] == 24:
            e.pop("rtt")
            e.pop("rtt_sample_id")
    out["css-seven-valid-samples"] = sparse
    out["fractional-segment-ack"] = dict(
        initial_snd_nxt=8000,
        events=[dict(type="ack", at=1, ack_seq=500, newly_acked_bytes=500)],
    )
    out["empty-round-waits-for-send"] = dict(
        initial_snd_nxt=8000,
        events=[
            dict(type="ack", at=1, ack_seq=8000, newly_acked_bytes=8000),
            dict(type="ack", at=2, ack_seq=8000, newly_acked_bytes=0),
            dict(type="sent", at=3, snd_nxt=16000),
            dict(type="ack", at=4, ack_seq=16000, newly_acked_bytes=8000),
        ],
    )
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path)
    parser.add_argument("--output", type=Path)
    a = parser.parse_args()
    r = (
        calculate(json.loads(a.inputs.read_text()))
        if a.inputs
        else {k: calculate(v) for k, v in scenarios().items()}
    )
    text = json.dumps(r, ensure_ascii=False, indent=2) + "\n"
    if a.output:
        a.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
