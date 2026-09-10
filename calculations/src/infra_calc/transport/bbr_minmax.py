"""Linux v6.6 three-sample running maximum, including u32 time subtraction.

This is the fixed constant-space approximation, not an exact deque maximum.
"""

from dataclasses import dataclass
from .bbr_reference import u32


@dataclass(frozen=True)
class Sample:
    t: int
    v: int


class RunningMax:
    def __init__(self, t=0, value=0):
        self.reset(t, value)

    @property
    def value(self):
        return self.samples[0].v

    def reset(self, t, value):
        u32(t, "t")
        u32(value, "value")
        self.samples = [Sample(t, value)] * 3
        return value

    def update(self, window, t, value):
        u32(window, "window")
        u32(t, "t")
        u32(value, "value")
        point = Sample(t, value)
        elapsed = lambda start: (t - start) & 0xFFFFFFFF
        if value >= self.samples[0].v or elapsed(self.samples[2].t) > window:
            return self.reset(t, value)
        if value >= self.samples[1].v:
            self.samples[1] = self.samples[2] = point
        elif value >= self.samples[2].v:
            self.samples[2] = point
        dt = elapsed(self.samples[0].t)
        if dt > window:
            self.samples = [self.samples[1], self.samples[2], point]
            if elapsed(self.samples[0].t) > window:
                self.samples = [self.samples[1], self.samples[2], point]
        elif self.samples[1].t == self.samples[0].t and dt > window // 4:
            self.samples[1] = self.samples[2] = point
        elif self.samples[2].t == self.samples[1].t and dt > window // 2:
            self.samples[2] = point
        return self.value
