"""RFC9438 pure controller event replay; explicitly selected Reno startup."""

from .reference_sources import reference_sources

import copy
import json
from fractions import Fraction as F

SCALE = 10**30


def number(value):
    if isinstance(value, bool):
        raise ValueError("boolean is not a number")
    try:
        result = F(str(value))
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("invalid rational") from exc
    if max(result.numerator.bit_length(), result.denominator.bit_length()) > 8192:
        raise ValueError("input rational exceeds budget")
    return result


def positive(value, zero=False):
    result = number(value)
    if result < 0 or (result == 0 and not zero):
        raise ValueError("expected positive/nonnegative rational")
    return result


def integer_root(n):
    lo, hi = 0, 1 << ((n.bit_length() + 2) // 3)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**3 <= n:
            lo = mid
        else:
            hi = mid
    return hi if hi**3 == n else lo


def cube_root_bounds(x):
    if x < 0:
        lo, hi = cube_root_bounds(-x)
        return -hi, -lo
    a, b = integer_root(x.numerator), integer_root(x.denominator)
    if a**3 == x.numerator and b**3 == x.denominator:
        return F(a, b), F(a, b)
    lo = F(integer_root(x.numerator * SCALE**3 // x.denominator), SCALE)
    return lo, lo + F(1, SCALE)


def serialize(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serialize(v) for v in obj]
    return obj


def sources():
    return reference_sources("cubic")


class Controller:
    def __init__(self, inputs):
        self.c = positive(inputs.get("C", "2/5"))
        self.beta = positive(inputs.get("beta", "7/10"))
        if self.beta >= 1:
            raise ValueError("beta must be < 1")
        self.base_alpha = 3 * (1 - self.beta) / (1 + self.beta)
        self.fast = inputs.get("fast_convergence", False)
        if type(self.fast) is not bool:
            raise ValueError("fast_convergence must be bool")
        if inputs.get("startup_policy", "reno_reference") != "reno_reference":
            raise ValueError("only explicit Reno reference startup supported")
        initial = inputs.get("initial", {})
        self.cwnd = positive(initial.get("cwnd", 10))
        self.iw = positive(inputs.get("initial_window", self.cwnd))
        self.threshold = positive(initial.get("ssthresh", 100))
        self.prior = positive(initial.get("cwnd_prior", self.cwnd))
        self.maximum = positive(initial["w_max"]) if "w_max" in initial else None
        self.phase = initial.get("phase", "slow_start")
        if self.phase not in ("slow_start", "avoidance"):
            raise ValueError("invalid initial phase")
        self.epoch = positive(initial.get("cwnd_epoch", self.cwnd))
        self.estimate = positive(initial.get("w_est", self.epoch))
        self.alpha = self.base_alpha if self.estimate < self.prior else F(1)
        self.elapsed = positive(initial.get("epoch_elapsed", 0), True)
        self.now = F(0)
        self.limited = None
        self.limited_since = None
        self.force_zero = self.maximum is None
        self.seen = set()
        self.quantizations = []
        if self.maximum is None:
            self.maximum = self.epoch
        self.k = cube_root_bounds((self.maximum - self.epoch) / self.c)

    def new_epoch(self):
        self.epoch = self.estimate = self.cwnd
        self.elapsed = F(0)
        if self.force_zero:
            self.maximum = self.cwnd
            self.force_zero = False
        self.k = cube_root_bounds((self.maximum - self.epoch) / self.c)
        self.alpha = self.base_alpha if self.estimate < self.prior else F(1)

    def curve(self, at):
        lo, hi = self.k
        return [
            self.c * (at - hi) ** 3 + self.maximum,
            self.c * (at - lo) ** 3 + self.maximum,
        ]

    def quantize(self):
        for name in ("cwnd", "estimate"):
            x = getattr(self, name)
            if max(x.numerator.bit_length(), x.denominator.bit_length()) > 4096:
                rounded = F(round(x * SCALE), SCALE)
                self.quantizations.append(
                    dict(
                        at=self.now,
                        field=name,
                        original=x,
                        rounded=rounded,
                        local_error=rounded - x,
                    )
                )
                setattr(self, name, rounded)

    def snapshot(self):
        return dict(
            cwnd=self.cwnd,
            ssthresh=self.threshold,
            cwnd_prior=self.prior,
            w_max=self.maximum,
            cwnd_epoch=self.epoch,
            w_est=self.estimate,
            alpha=self.alpha,
            k_bounds=list(self.k),
            epoch_elapsed=self.elapsed,
            phase=self.phase,
            limited=self.limited,
            curve_bounds=self.curve(self.elapsed),
        )

    def step(self, event):
        at = positive(event["at"], True)
        if at < self.now:
            raise ValueError("events must be chronological")
        if self.phase == "avoidance" and self.limited is None:
            self.elapsed += at - self.now
        self.now = at
        kind = event["type"]
        detail = {}
        if kind == "ack":
            count = positive(event["segments_acked"], True)
            rtt = positive(event["smoothed_rtt"])
            if not count or self.limited is not None or self.phase == "recovery":
                detail["region"] = "no-growth"
            elif self.phase == "slow_start":
                self.cwnd += min(count, F(1))
                detail["region"] = "slow-start"
                if self.cwnd > self.threshold:
                    self.phase = "avoidance"
                    self.new_epoch()
            else:
                self.estimate += self.alpha * count / self.cwnd
                if self.estimate >= self.prior:
                    self.alpha = F(1)
                bounds = self.curve(self.elapsed)
                if bounds[0] < self.estimate <= bounds[1] and bounds[0] != bounds[1]:
                    raise ValueError("Reno branch unresolved by numerical root bounds")
                if self.estimate > bounds[1]:
                    if self.estimate < self.cwnd:
                        raise ValueError(
                            "inconsistent seed: Reno branch would decrease cwnd"
                        )
                    self.cwnd = self.estimate
                    detail["region"] = "reno-friendly"
                else:
                    target_bounds = [
                        max(self.cwnd, min(F(3, 2) * self.cwnd, x))
                        for x in self.curve(self.elapsed + rtt)
                    ]
                    midpoint = sum(self.k) / 2
                    raw = self.c * (self.elapsed + rtt - midpoint) ** 3 + self.maximum
                    target = max(self.cwnd, min(F(3, 2) * self.cwnd, raw))
                    detail.update(
                        region="cubic",
                        target=target,
                        target_bounds=target_bounds,
                        increment=(target - self.cwnd) / self.cwnd,
                    )
                    self.cwnd += detail["increment"]
        elif kind in ("congestion", "timeout"):
            event_id = event.get("event_id")
            if not isinstance(event_id, str) or not event_id:
                raise ValueError("congestion requires unique event_id")
            flight = positive(event["flight_size"], True)
            if event.get("signal", "loss") != "loss":
                raise ValueError("ECE/ECN not implemented")
            if event_id in self.seen or (
                kind == "congestion" and self.phase == "recovery"
            ):
                detail["ignored_recovery_event"] = True
                self.seen.add(event_id)
            else:
                self.seen.add(event_id)
                old = self.cwnd
                self.prior = old
                self.maximum = (
                    old * (1 + self.beta) / 2
                    if self.fast and old < self.maximum
                    else old
                )
                self.threshold = max(flight * self.beta, F(2))
                self.cwnd = F(1) if kind == "timeout" else self.threshold
                self.phase = "slow_start" if kind == "timeout" else "recovery"
                self.force_zero = kind == "timeout"
        elif kind == "recovery_exit":
            if self.phase != "recovery":
                raise ValueError("not in recovery")
            self.phase = "slow_start" if self.cwnd <= self.threshold else "avoidance"
            if self.phase == "avoidance":
                self.new_epoch()
        elif kind == "limited_start":
            reason = event.get("reason")
            if self.limited is not None or reason not in (
                "application",
                "receiver_window",
            ):
                raise ValueError("invalid limited interval")
            self.limited = reason
            self.limited_since = at
        elif kind == "limited_end":
            if self.limited is None:
                raise ValueError("no limited interval")
            self.limited = None
            self.limited_since = None
        elif kind == "idle_restart":
            idle, rto = positive(event["idle_duration"], True), positive(event["rto"])
            if self.limited is None:
                raise ValueError("idle restart requires observed limited interval")
            if idle > at - self.limited_since:
                raise ValueError("idle duration exceeds observed limited interval")
            if idle > rto:
                self.cwnd = min(self.iw, self.cwnd)
                self.phase = (
                    "slow_start" if self.cwnd <= self.threshold else "avoidance"
                )
                self.new_epoch()
                detail["restart_applied"] = True
        elif kind != "observe":
            raise ValueError("unsupported event type")
        self.quantize()
        return dict(event=copy.deepcopy(event), detail=detail, state=self.snapshot())


def validate_inputs(inputs):
    if not isinstance(inputs, dict):
        raise ValueError("inputs must be object")
    allowed = {
        "C",
        "beta",
        "fast_convergence",
        "startup_policy",
        "initial_window",
        "initial",
        "events",
    }
    if set(inputs) - allowed:
        raise ValueError("unknown input field")
    initial = inputs.get("initial", {})
    if not isinstance(initial, dict) or set(initial) - {
        "phase",
        "cwnd",
        "ssthresh",
        "cwnd_prior",
        "w_max",
        "cwnd_epoch",
        "w_est",
        "epoch_elapsed",
    }:
        raise ValueError("unknown initial field")
    schemas = {
        "ack": ({"segments_acked", "smoothed_rtt"}, set()),
        "congestion": ({"event_id", "flight_size"}, {"signal"}),
        "timeout": ({"event_id", "flight_size"}, {"signal"}),
        "recovery_exit": (set(), set()),
        "limited_start": ({"reason"}, set()),
        "limited_end": (set(), set()),
        "idle_restart": ({"idle_duration", "rto"}, set()),
        "observe": (set(), set()),
    }
    events = inputs.get("events", [])
    if not isinstance(events, list) or len(events) > 1000:
        raise ValueError("event budget exceeded")
    for event in events:
        if not isinstance(event, dict) or event.get("type") not in schemas:
            raise ValueError("unknown event")
        required, optional = schemas[event["type"]]
        required = required | {"type", "at"}
        if required - set(event) or set(event) - required - optional:
            raise ValueError("missing or unknown event field")


def calculate(inputs=None):
    inputs = copy.deepcopy(example() if inputs is None else inputs)
    lock = sources()
    validate_inputs(inputs)
    events = inputs.get("events", [])
    if not isinstance(events, list) or len(events) > 1000:
        raise ValueError("event budget exceeded")
    state = Controller(inputs)
    initial = state.snapshot()
    trace = [state.step(event) for event in events]
    return serialize(
        dict(
            inputs=inputs,
            initial=initial,
            events=trace,
            final=state.snapshot(),
            quantizations=state.quantizations,
            reference_sources=lock,
            numerical_contract="rational states; root bracket <=1e-30 s; local quantization errors only",
            scope="pure CUBIC state replay; explicit Reno startup; no feedback detector or network",
        )
    )


def example():
    return dict(
        initial=dict(
            phase="avoidance",
            cwnd="100",
            ssthresh="70",
            w_max="100",
            cwnd_epoch="484/5",
            w_est="484/5",
            cwnd_prior="100",
        ),
        events=[dict(at="2", type="ack", segments_acked="1", smoothed_rtt="1")],
    )


def scenarios():
    result = {"one-ack": example()}
    for name, events in {
        "curve": [dict(at=t, type="observe") for t in ("0", "2", "3")],
        "reno-friendly": [
            dict(at="0", type="ack", segments_acked="1", smoothed_rtt="1")
        ],
        "target-clamp": [
            dict(at="100", type="ack", segments_acked="8", smoothed_rtt="1")
        ],
        "loss-recovery": [
            dict(at="1", type="congestion", event_id="a", flight_size="50"),
            dict(at="2", type="congestion", event_id="b", flight_size="40"),
            dict(at="3", type="recovery_exit"),
            dict(at="4", type="ack", segments_acked="2", smoothed_rtt="1"),
        ],
        "limited": [
            dict(at="1", type="limited_start", reason="application"),
            dict(at="20", type="ack", segments_acked="1", smoothed_rtt="1"),
            dict(at="30", type="limited_end"),
            dict(at="31", type="observe"),
        ],
        "timeout": [dict(at="1", type="timeout", event_id="rto", flight_size="4")]
        + [
            dict(at=str(t), type="ack", segments_acked="1", smoothed_rtt="1")
            for t in range(2, 6)
        ],
        "idle-restart": [
            dict(at="1", type="limited_start", reason="application"),
            dict(at="10", type="idle_restart", idle_duration="9", rto="1"),
        ],
    }.items():
        inp = example()
        inp["events"] = events
        result[name] = inp
    result["reno-friendly"]["initial"]["cwnd"] = "484/5"
    result["idle-restart"]["initial_window"] = "10"
    result["slow-start"] = dict(
        initial=dict(cwnd="2", ssthresh="3"),
        events=[
            dict(at=str(t), type="ack", segments_acked="2", smoothed_rtt="1")
            for t in range(4)
        ],
    )
    result["fast-convergence"] = copy.deepcopy(result["loss-recovery"])
    result["fast-convergence"]["fast_convergence"] = True
    result["fast-convergence"]["initial"]["cwnd"] = "80"
    result["fractional-ack"] = example()
    result["fractional-ack"]["events"][0]["segments_acked"] = "1/2"
    result["duplicate-ack"] = example()
    result["duplicate-ack"]["events"][0]["segments_acked"] = "0"
    result["alpha-threshold"] = example()
    result["alpha-threshold"]["initial"]["w_est"] = "1691/17"
    result["alpha-threshold"]["events"][0]["segments_acked"] = "100"
    result["irrational-root"] = example()
    result["irrational-root"]["initial"]["cwnd_epoch"] = "97"
    result["irrational-root"]["initial"]["w_est"] = "97"
    result["receiver-limited"] = copy.deepcopy(result["limited"])
    result["receiver-limited"]["events"][0]["reason"] = "receiver_window"
    result["loss-floor"] = example()
    result["loss-floor"]["events"] = [
        dict(at="1", type="congestion", event_id="small", flight_size="1")
    ]
    return result
