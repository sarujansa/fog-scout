"""Where the overlay's tick spends its time (1.8.31, user's pick: "Messung unter Windows in die Diagnose") – pure:
per tick the milliseconds of each step, kept for the last ``KEPT`` ticks (≈ 30 s at 4 ticks a second), shown as
one line of the diagnosis: average and maximum of the whole tick and of each step."""
from __future__ import annotations

import contextlib
import time
from collections import deque

KEPT = 120
STEPS = (("hud", "Systemwerte"), ("today", "Heute"), ("music", "Musik"), ("info", "Infos"),
         ("resolve", "Ausweichen"), ("guides", "Hilfslinien"))


class TickTimes:
    def __init__(self, kept: int = KEPT):
        self.ticks = deque(maxlen=kept)          # {step: ms, "total": ms}
        self._now = None

    def start(self):
        self._now = {}

    def add(self, step: str, ms: float):
        if self._now is not None:
            self._now[step] = self._now.get(step, 0.0) + ms

    def end(self, total_ms: float | None = None):
        """Close the running tick. ``total_ms`` None (1.38.22, the worker): the steps' sum – its ticks end in a
        sleep whose length says nothing about the work."""
        if self._now is None:
            return
        tick = dict(self._now)
        if total_ms is None:
            total_ms = sum(self._now.values())
        tick["total"] = total_ms
        tick["map"] = max(0.0, total_ms - sum(v for k, v in self._now.items()))   # the rest: map and placing
        self.ticks.append(tick)
        self._now = None

    @contextlib.contextmanager
    def measure(self, step: str):
        """``with times.measure("end"): …`` – the block's time counts for ``step`` of the running tick."""
        t0 = time.perf_counter()
        try:
            yield
        finally:
            self.add(step, (time.perf_counter() - t0) * 1000)

    def timed(self, step: str, fn):
        """``fn`` wrapped so that its time counts for ``step`` of the running tick."""
        def run(*a, **kw):
            t0 = time.perf_counter()
            try:
                return fn(*a, **kw)
            finally:
                self.add(step, (time.perf_counter() - t0) * 1000)
        run.__wrapped__ = fn
        return run

    def line(self) -> str:
        if not self.ticks:
            return "Overlay-Takt: noch keine Messung"
        n = len(self.ticks)

        def stat(key):
            vals = [t.get(key, 0.0) for t in self.ticks]
            return sum(vals) / n, max(vals)
        avg, top = stat("total")
        slow = sum(1 for t in self.ticks if t["total"] >= 30)
        parts = [f"{label} {a:.1f}/{m:.0f}" for key, label in (("map", "Karte"),) + STEPS
                 for a, m in (stat(key),) if m >= 0.05]
        return (f"Overlay-Takt ({n} Takte, Ø/max ms): gesamt {avg:.1f}/{top:.0f}, ≥ 30 ms: {slow}× · "
                + " · ".join(parts))


# 1.38.22 (project review, PERF-2): the detection worker timed the same way – before, nothing said what a tick of
# the detection cost (the full-screen grab, the OCR of the banner and the lobby corner, the round-end look).
LOOK_STEPS = (("grab", "Aufnahme"), ("mask", "Schwärzen"), ("banner", "Banner-OCR"), ("lobby", "Lobby-OCR"),
              ("end", "Rundenende"), ("vbars", "Balken"), ("window", "Fenstersuche"))


class LookTimes(TickTimes):
    """The worker's ticks ("looks"): steps are sparse – the lobby is read once a second, the banner strip up to
    five times – so each step is averaged over the ticks it ran in, with that count."""

    def line(self) -> str:
        if not self.ticks:
            return "Erkennungs-Takt: noch keine Messung"
        n = len(self.ticks)
        totals = [t["total"] for t in self.ticks]
        parts = []
        for key, label in LOOK_STEPS:
            vals = [t[key] for t in self.ticks if t.get(key, 0.0) >= 0.05]
            if vals:
                parts.append(f"{label} {sum(vals) / len(vals):.1f}/{max(vals):.0f} ({len(vals)}×)")
        return (f"Erkennungs-Takt ({n} Takte, Ø/max ms je Lauf): Arbeit je Takt {sum(totals) / n:.1f}/{max(totals):.0f}"
                + (" · " + " · ".join(parts) if parts else ""))


class CpuShare:
    """1.38.22: CPU share of one thread from its own ``time.thread_time()`` (GetThreadTimes on itself, no handle to
    any other thread or process) – ``note(wall, cpu)`` once per tick, ``percent`` = CPU seconds per wall second
    over the kept window, as a share of one core. Pure."""

    def __init__(self, kept: int = 600):
        self.samples = deque(maxlen=kept)      # (wall, cpu seconds)

    def note(self, wall: float, cpu: float):
        self.samples.append((wall, cpu))

    def percent(self, window_s: float = 60.0) -> float | None:
        if len(self.samples) < 2:
            return None
        last_wall, last_cpu = self.samples[-1]
        first = next((s for s in self.samples if s[0] >= last_wall - window_s), self.samples[0])
        if first is self.samples[-1]:
            first = self.samples[-2]
        dt = last_wall - first[0]
        return max(0.0, 100.0 * (last_cpu - first[1]) / dt) if dt > 0 else None

    def line(self, name: str = "Erkennung") -> str:
        p60, p600 = self.percent(60), self.percent(600)
        if p60 is None:
            return f"CPU {name}: noch keine Messung"
        return f"CPU {name} (ein Kern = 100 %): letzte Minute {p60:.1f} %, letzte 10 min {p600:.1f} %"
