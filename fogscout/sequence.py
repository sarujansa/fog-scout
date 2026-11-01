"""The clip editor's sequence (1.16, user: a timeline "wie DaVinci Resolve / CapCut" instead of the strip with
start and end): the clips of a recording in play order, each a stretch of the source (clipedit.Part: start, end,
speed), laid one after the other on the output time axis – no gaps, no overlaps, trimming one clip moves the
ones after it (ripple). Pure functions on lists of parts and a small undo history; no Qt, so the timeline's
arithmetic is tested without a window.

Two clocks: *source time* = seconds of the recording (what ffmpeg seeks, where the F8 marks and the drawings
live), *output time* = seconds of the finished clip (where the playhead of the timeline is). ``source_at`` and
``output_at`` translate between them.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace

from .clipedit import Part, SPEEDS

MIN_LEN = 0.1                    # seconds of source a clip keeps at least (clean_parts drops shorter ones)
HISTORY_KEPT = 100               # undo steps kept
RULER_STEPS = (0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 30.0, 60.0, 120.0, 300.0, 600.0, 1800.0, 3600.0)
LABEL_GAP_PX = 84                # at least this far between two labels of the ruler


def length(part: Part) -> float:
    """Output seconds of one part."""
    return max(0.0, part.end - part.start) / max(0.01, part.speed)


def duration(parts) -> float:
    return sum(length(p) for p in parts)


def starts(parts) -> list:
    """Output time at which each part begins (and, as the last value, the end of the sequence)."""
    out, t = [], 0.0
    for p in parts:
        out.append(t)
        t += length(p)
    out.append(t)
    return out


def index_at(parts, t: float) -> int | None:
    """The part under output time ``t`` (the last one at its very end), None without parts."""
    if not parts:
        return None
    acc = 0.0
    for i, p in enumerate(parts):
        acc += length(p)
        if t < acc - 1e-9:
            return i
    return len(parts) - 1


def source_at(parts, t: float) -> tuple[int | None, float]:
    """(part index, source second) for output time ``t``; without parts (None, t)."""
    i = index_at(parts, t)
    if i is None:
        return None, max(0.0, t)
    base = starts(parts)[i]
    p = parts[i]
    src = p.start + max(0.0, t - base) * p.speed
    return i, min(max(p.start, src), p.end)


def output_at(parts, i: int, src: float) -> float:
    """Output time of source second ``src`` inside part ``i``."""
    p = parts[i]
    return starts(parts)[i] + (min(max(p.start, src), p.end) - p.start) / max(0.01, p.speed)


def occurrences(parts, src: float) -> list:
    """Every output time at which source second ``src`` plays (a part used twice shows a mark twice)."""
    return [output_at(parts, i, src) for i, p in enumerate(parts) if p.start - 1e-9 <= src <= p.end + 1e-9]


def split(parts, t: float) -> tuple[list, int | None]:
    """The sequence with the part under output ``t`` cut in two at that moment; (parts, index of the second half)
    – unchanged (None) when the cut would fall on an edge or leave a piece shorter than MIN_LEN."""
    i, src = source_at(parts, t)
    if i is None:
        return list(parts), None
    p = parts[i]
    if src - p.start < MIN_LEN - 1e-9 or p.end - src < MIN_LEN - 1e-9:
        return list(parts), None
    out = list(parts)
    out[i:i + 1] = [Part(p.start, src, p.speed), Part(src, p.end, p.speed)]
    return out, i + 1


def trim(parts, i: int, edge: str, src: float, total: float) -> list:
    """Part ``i`` with its ``edge`` ("start" or "end") moved to source second ``src`` (inside the recording of
    ``total`` seconds, keeping MIN_LEN); the sequence re-flows."""
    out = list(parts)
    p = out[i]
    if edge == "start":
        out[i] = replace(p, start=min(max(0.0, src), p.end - MIN_LEN))
    else:
        out[i] = replace(p, end=max(min(total if total > 0 else src, src), p.start + MIN_LEN))
    return out


def move(parts, i: int, j: int) -> list:
    """Part ``i`` taken out and put back so that it is the ``j``-th one."""
    out = list(parts)
    if not 0 <= i < len(out):
        return out
    p = out.pop(i)
    out.insert(min(max(0, j), len(out)), p)
    return out


def remove(parts, i: int) -> list:
    out = list(parts)
    if 0 <= i < len(out):
        del out[i]
    return out


def with_speed(parts, i: int, speed: float) -> list:
    out = list(parts)
    if 0 <= i < len(out):
        lo, hi = SPEEDS[0], SPEEDS[-1]
        out[i] = replace(out[i], speed=max(lo, min(hi, float(speed))))
    return out


def drop_index(parts, i: int, t: float) -> int:
    """Where part ``i`` lands when dropped with its left edge at output ``t``: after every other part whose middle
    lies left of that edge (dropped at the very start it comes first, past the last one's middle it comes last)."""
    if not parts:
        return 0
    others = [(k, s + length(p) / 2) for k, (s, p) in enumerate(zip(starts(parts), parts)) if k != i]
    return sum(1 for _k, centre in others if t > centre)


def ruler_step(px_per_s: float, gap_px: float = LABEL_GAP_PX) -> tuple[float, int]:
    """(seconds between two labelled ticks, minor ticks per label) for a zoom of ``px_per_s``."""
    for step in RULER_STEPS:
        if step * px_per_s >= gap_px:
            minor = 5 if step in (0.5, 1.0, 5.0, 10.0, 30.0, 60.0, 300.0, 600.0, 3600.0) else 4 if step in (2.0, 120.0) else 3 if step in (15.0, 1800.0) else 2
            return step, minor
    return RULER_STEPS[-1], 6


def fmt_ruler(t: float, step: float) -> str:
    """m:ss (or m:ss.t below a one-second step) for a ruler label."""
    t = max(0.0, t)
    if step < 1.0:
        t = round(t * 10) / 10
        m = int(t // 60)
        return f"{m}:{t - m * 60:04.1f}"
    t = int(round(t))
    return f"{t // 60}:{t % 60:02d}"


@dataclass
class EditState:
    """Everything the undo history remembers of the editor: the clips, picture crop (and the choice it came
    from), drawings, fades, censor boxes with their switch and look."""
    parts: list = field(default_factory=list)
    crop: tuple | None = None
    crop_key: str = "none"
    shapes: list = field(default_factory=list)
    fade_in: float = 0.0
    fade_out: float = 0.0
    boxes: list = field(default_factory=list)
    censor_on: bool = False
    censor_style: str = "pixel"

    def copy(self) -> "EditState":
        return EditState([Part(p.start, p.end, p.speed) for p in self.parts], self.crop, self.crop_key,
                         [replace(s, pts=list(s.pts)) for s in self.shapes], self.fade_in, self.fade_out,
                         [list(b) for b in self.boxes], self.censor_on, self.censor_style)


class History:
    """Undo/redo over snapshots: ``push(state, key)`` after a change (a change with the same ``key`` as the one
    before replaces it – typing into a text is one step), ``undo()``/``redo()`` give the state to show."""

    def __init__(self, first: EditState, kept: int = HISTORY_KEPT):
        self._past = [first.copy()]
        self._future = []
        self._keys = [None]
        self.kept = kept

    @property
    def current(self) -> EditState:
        return self._past[-1]

    def push(self, state: EditState, key=None) -> bool:
        """Remember ``state``; False when it equals the current one (nothing happened)."""
        if state == self.current:
            return False
        if key is not None and self._keys[-1] == key and len(self._past) > 1:
            self._past[-1] = state.copy()
        else:
            self._past.append(state.copy())
            self._keys.append(key)
            del self._past[:-self.kept]
            del self._keys[:-self.kept]
        self._future.clear()
        return True

    def can_undo(self) -> bool:
        return len(self._past) > 1

    def can_redo(self) -> bool:
        return bool(self._future)

    def undo(self) -> EditState | None:
        if not self.can_undo():
            return None
        self._future.append((self._past.pop(), self._keys.pop()))
        self._keys[-1] = None                        # the step before is closed: a new change is a new step
        return self.current.copy()

    def redo(self) -> EditState | None:
        if not self._future:
            return None
        state, key = self._future.pop()
        self._past.append(state)
        self._keys.append(None if key is None else key)
        self._keys[-1] = None
        return self.current.copy()
