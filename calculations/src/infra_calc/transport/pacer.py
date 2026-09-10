"""Piecewise-rate byte debt; explicit local quantization, no idle burst credit."""

from fractions import Fraction as F


class Pacer:
    def __init__(
        self, rate, *, time_quantum="0.000000001", debt_quantum="0.000000000001"
    ):
        if any(isinstance(v, bool) for v in (rate, time_quantum, debt_quantum)):
            raise ValueError("boolean is not a pacing number")
        self.rate = F(str(rate))
        self.time_quantum = F(str(time_quantum))
        self.debt_quantum = F(str(debt_quantum))
        if min(self.rate, self.time_quantum, self.debt_quantum) <= 0:
            raise ValueError("positive pacing rate and quantums required")
        self.now = F(0)
        self.debt = F(0)
        self.errors = []

    def advance(self, now, rate=None):
        if isinstance(now, bool) or isinstance(rate, bool):
            raise ValueError("boolean is not a pacing number")
        now = F(str(now))
        rate = F(str(rate)) if rate is not None else None
        if rate is not None and rate <= 0:
            raise ValueError("positive pacing rate")
        if now < self.now:
            raise ValueError("pacer time reversal")
        exact = max(F(0), self.debt - (now - self.now) * self.rate)
        grid = exact / self.debt_quantum
        rounded = F(-(-grid.numerator // grid.denominator)) * self.debt_quantum
        if exact != rounded:
            self.errors.append(
                dict(
                    at=str(now),
                    kind="debt_round",
                    original=str(exact),
                    rounded=str(rounded),
                    local_error=str(rounded - exact),
                )
            )
        self.debt = rounded
        self.now = now
        if rate is not None:
            self.rate = rate

    def ready(self, now):
        self.advance(now)
        exact = self.now + self.debt / self.rate
        grid = exact / self.time_quantum
        rounded = F(-(-grid.numerator // grid.denominator)) * self.time_quantum
        if rounded != exact:
            self.errors.append(
                dict(
                    at=str(now),
                    kind="ready_time_ceil",
                    original=str(exact),
                    rounded=str(rounded),
                    local_error=str(rounded - exact),
                )
            )
        return rounded

    def sent(self, now, packet_bytes):
        if type(packet_bytes) is not int or packet_bytes <= 0 or isinstance(now, bool):
            raise ValueError("positive integer QUIC packet bytes required")
        now = F(str(now))
        if now < self.now:
            raise ValueError("pacer time reversal")
        if self.debt - (now - self.now) * self.rate > 0:
            raise ValueError("paced send before debt repaid")
        self.advance(now)
        self.debt += packet_bytes

    def snapshot(self):
        return dict(
            at=str(self.now),
            debt_quic_bytes=str(self.debt),
            rate_quic_bytes_per_second=str(self.rate),
        )
