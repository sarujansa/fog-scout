"""1.35 (user: "Erststart und Startzeit der .exe optimieren" – first measure, then change): how long Fog Scout takes
from the start of its process until the window is ready, in phases.

``process_age_s`` reads only the own process, like selfload: on Windows ``GetProcessTimes(GetCurrentProcess())`` –
the pseudo handle to itself, no ``OpenProcess``, no other process (CLAUDE.md) –, on Linux ``/proc/self/stat``. The
time before Python runs our code (the .exe's loader unpacking nothing but loading DLLs, the interpreter, the
package's imports up to ``__main__``) is only visible this way.

``StartClock`` takes the marks of ``__main__`` and the App; ``line()`` is the log line, ``diag()`` the diagnosis
line, ``as_dict()`` what the self-check writes. No timing changes any behaviour."""
from __future__ import annotations

import ctypes
import os
import sys
import time

PHASES = (("python", "bis Python"), ("splash", "Ladebildschirm"), ("loaded", "Laden"), ("built", "Aufbau"),
          ("ready", "Fenster"))


def process_age_s() -> float | None:
    """Seconds since this process was created, None when the system does not say."""
    try:
        if sys.platform == "win32":
            from ctypes import wintypes
            k32 = ctypes.WinDLL("kernel32", use_last_error=True)
            k32.GetCurrentProcess.restype = wintypes.HANDLE
            ft = ctypes.POINTER(wintypes.FILETIME)
            # the pseudo handle is -1 as a pointer-wide int: without argtypes ctypes passes a C int and overflows
            k32.GetProcessTimes.argtypes = (wintypes.HANDLE, ft, ft, ft, ft)
            k32.GetProcessTimes.restype = wintypes.BOOL
            k32.GetSystemTimeAsFileTime.argtypes = (ft,)
            k32.GetSystemTimeAsFileTime.restype = None
            created, exited, kernel, user = (wintypes.FILETIME() for _i in range(4))
            if not k32.GetProcessTimes(k32.GetCurrentProcess(), ctypes.byref(created), ctypes.byref(exited),
                                       ctypes.byref(kernel), ctypes.byref(user)):
                return None
            now = wintypes.FILETIME()
            k32.GetSystemTimeAsFileTime(ctypes.byref(now))

            def ticks(ft):
                return (ft.dwHighDateTime << 32) | ft.dwLowDateTime
            return max(0.0, (ticks(now) - ticks(created)) / 1e7)          # FILETIME: 100 ns steps
        with open("/proc/self/stat", encoding="ascii") as fh:
            fields = fh.read().rsplit(")", 1)[1].split()
        with open("/proc/uptime", encoding="ascii") as fh:
            uptime = float(fh.read().split()[0])
        return max(0.0, uptime - int(fields[19]) / os.sysconf("SC_CLK_TCK"))   # field 22: starttime
    except Exception:                 # a measurement never stops the start (ctypes.ArgumentError, OSError …)
        return None


class StartClock:
    """Marks in order; each phase is the time since the mark before. ``before`` = the process's age when the clock
    was made (the time before our code ran), None when unknown."""

    def __init__(self, before: float | None = None, now: float | None = None):
        self.t0 = time.perf_counter() if now is None else now
        self.before = process_age_s() if before is None else before
        self.marks: dict[str, float] = {}
        self.steps: list[tuple[str, float]] = []        # 1.38.15: finer steps inside the phases (label, time)

    def mark(self, name: str, now: float | None = None) -> None:
        if name not in self.marks:                       # the first time counts (a second window build does not)
            self.marks[name] = time.perf_counter() if now is None else now

    def step(self, label: str, now: float | None = None) -> None:
        """1.38.15 (user's diagnosis: "Ladebildschirm 1,18 · Aufbau 1,24" on Windows, 0,16 s on Linux – where?): a
        point inside a phase; its time is the span since the step or mark before it. The first time counts."""
        if all(name != label for name, _t in self.steps):
            self.steps.append((label, time.perf_counter() if now is None else now))

    def steps_ms(self) -> list:
        """[(label, ms since the step or mark before)] in order of time."""
        points = sorted([(t, None) for t in self.marks.values()] + [(t, label) for label, t in self.steps],
                        key=lambda p: p[0])
        out, last = [], self.t0
        for t, label in points:
            if label is not None:
                out.append((label, max(0.0, t - last) * 1000))
            last = t
        return out

    def phases_ms(self) -> dict:
        out = {}
        if self.before is not None:
            out["python"] = self.before * 1000
        last = self.t0
        for name, _label in PHASES[1:]:
            if name in self.marks:
                out[name] = max(0.0, self.marks[name] - last) * 1000
                last = self.marks[name]
        return out

    def total_ms(self) -> float | None:
        """From the process's start (or, unknown, from the clock) to the last mark."""
        if not self.marks:
            return None
        return (max(self.marks.values()) - self.t0) * 1000 + (self.before or 0.0) * 1000

    def as_dict(self) -> dict:
        d = {k: round(v) for k, v in self.phases_ms().items()}
        if self.steps:
            d["steps"] = {label: round(ms) for label, ms in self.steps_ms()}
        total = self.total_ms()
        if total is not None:
            d["total"] = round(total)
        return d

    def diag(self) -> str:
        """For the diagnosis (not translated): "Start: 2,41 s (bis Python 0,92 · Ladebildschirm 0,05 · …)"."""
        total = self.total_ms()
        if total is None:
            return "Start: nicht gemessen"
        parts = [f"{label} {self.phases_ms()[name] / 1000:.2f}".replace(".", ",")
                 for name, label in PHASES if name in self.phases_ms()]
        line = f"Start: {total / 1000:.2f} s".replace(".", ",") + (" (" + " · ".join(parts) + ")" if parts else "")
        if self.steps:                                    # 1.38.15: the steps, each since the point before it
            line += "\n  Schritte: " + " · ".join(f"{label} {ms / 1000:.2f}".replace(".", ",")
                                                   for label, ms in self.steps_ms())
        return line
