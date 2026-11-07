"""The input card in the clip editor (1.39.1, user: input display "Overlay + Editor"): a recording's input changes
(inputs.load – seconds of the file, inputs.encode codes) shown as a track, drawn on the preview and burned into the
export. Pure – no Qt, no ffmpeg: the editor and clipedit.export call it.

``InputSpec`` is the editor's choice (on, device layout, corner, size, dark area), part of the edit (undo, project).
``segments`` maps the changes of every source through the cut (parts in play order, tempo, backwards, stills) into
the finished clip's seconds: [(t0, t1, code)] – one picture per distinct code, laid over the clip in output time.
"""
from __future__ import annotations

import bisect
from dataclasses import dataclass

from . import inputs, sequence

CORNERS = ("bottom_left", "bottom_right", "top_left", "top_right")
LAYOUTS = inputs.LAYOUTS                  # auto / keyboard / gamepad
SIZE_RANGE = (8, 25)                      # card height, percent of the finished picture's height
DEFAULT_SIZE = 14
MARGIN = 0.02                             # distance to the picture's edge, share of its height
DENSITY_PER_S = 4                         # bins per second of the timeline strip
MIN_SEGMENT_S = 0.02                      # shorter state changes are merged (below one frame at 60 fps)


@dataclass
class InputSpec:
    on: bool = False
    layout: str = "auto"
    corner: str = "bottom_right"
    size: int = DEFAULT_SIZE
    backdrop: bool = True

    def copy(self) -> "InputSpec":
        return InputSpec(self.on, self.layout, self.corner, self.size, self.backdrop)

    def to_dict(self) -> dict:
        return {"on": bool(self.on), "layout": self.layout, "corner": self.corner, "size": int(self.size),
                "backdrop": bool(self.backdrop)}


def from_dict(d) -> InputSpec | None:
    """A project's ``inputs`` field → InputSpec (each value checked, a wrong one takes its default); None for none."""
    if not isinstance(d, dict):
        return None
    s = InputSpec()
    if isinstance(d.get("on"), bool):
        s.on = d["on"]
    if d.get("layout") in LAYOUTS:
        s.layout = d["layout"]
    if d.get("corner") in CORNERS:
        s.corner = d["corner"]
    size = d.get("size")
    if isinstance(size, (int, float)) and not isinstance(size, bool):
        s.size = int(min(SIZE_RANGE[1], max(SIZE_RANGE[0], round(size))))
    if isinstance(d.get("backdrop"), bool):
        s.backdrop = d["backdrop"]
    return s


def _times(events) -> list:
    return [t for t, _c in events]


def state_at(events, t: float, times=None) -> int:
    """The code held at second ``t`` of the recording (0 = nothing held, also before the first change)."""
    if not events:
        return 0
    times = _times(events) if times is None else times
    i = bisect.bisect_right(times, t) - 1
    return events[i][1] if i >= 0 else 0


def state_before(events, t: float, times=None) -> int:
    """The code held just before second ``t`` (a change exactly at ``t`` not yet)."""
    if not events:
        return 0
    times = _times(events) if times is None else times
    i = bisect.bisect_left(times, t) - 1
    return events[i][1] if i >= 0 else 0


def density(events, length: float, per_s: int = DENSITY_PER_S) -> list:
    """Changes per bin over a recording ``length`` s long, scaled 0…1 (the busiest bin = 1) – the editor's strip."""
    n = max(1, int(length * per_s) + 1)
    bins = [0] * n
    for t, _c in events:
        k = int(t * per_s)
        if 0 <= k < n:
            bins[k] += 1
    top = max(bins) or 1
    return [b / top for b in bins]


def _merge(points, total: float) -> list:
    """[(output time, code)] change points (sorted) → [(t0, t1, code)] covering [0, total], equal neighbours and
    slivers merged."""
    out = []
    for i, (t0, code) in enumerate(points):
        t1 = points[i + 1][0] if i + 1 < len(points) else total
        if t1 - t0 <= 0:
            continue
        if out and (out[-1][2] == code or t1 - t0 < MIN_SEGMENT_S):
            out[-1] = (out[-1][0], t1, out[-1][2])
            continue
        out.append((t0, t1, code))
    return out


def segments(parts, events_by_src) -> list:
    """The cut's input card over time: [(t0, t1, code)] in seconds of the finished clip. ``events_by_src`` =
    {montage source: [(second of that recording, code)]} (a source without events shows nothing held). A still
    shows the moment it holds; a backwards part plays the changes backwards (a press becomes a release)."""
    starts = sequence.starts(parts)
    total = starts[-1] if starts else 0.0
    points = []
    for i, p in enumerate(parts):
        ev = events_by_src.get(getattr(p, "src", 0)) or []
        times = _times(ev)
        s0 = starts[i]
        if p.hold > 0:
            points.append((s0, state_at(ev, p.start, times)))
            continue
        speed = max(0.01, p.speed)
        lo = bisect.bisect_right(times, p.start)
        hi = bisect.bisect_left(times, p.end)
        inside = ev[lo:hi]
        if not p.reverse:
            points.append((s0, state_at(ev, p.start, times)))
            points += [(s0 + (t - p.start) / speed, c) for t, c in inside]
        else:
            points.append((s0, state_before(ev, p.end, times)))
            for t, _c in reversed(inside):
                points.append((s0 + (p.end - t) / speed, state_before(ev, t, times)))
    points.sort(key=lambda x: x[0])
    return _merge(points, total)


def layouts(segs, setting: str) -> list:
    """The device layout of each segment – "auto" follows the device used last (inputs.DeviceChoice) along the clip."""
    choice = inputs.DeviceChoice()
    return [choice.layout(setting, inputs.decode(code)) for _t0, _t1, code in segs]


def card_box(spec: InputSpec, width: int, height: int) -> tuple:
    """(x, y, card height) of the card in a finished picture ``width`` × ``height`` – its size share of the height,
    narrower pictures (9:16) make it smaller so it never leaves the picture."""
    from .overlay_render import INPUT_RATIO
    margin = max(2, round(height * MARGIN))
    h = max(24, round(height * spec.size / 100))
    if round(h * INPUT_RATIO) > width - 2 * margin:
        h = max(24, int((width - 2 * margin) / INPUT_RATIO))
    w = round(h * INPUT_RATIO)
    left = spec.corner in ("bottom_left", "top_left")
    top = spec.corner in ("top_left", "top_right")
    x = margin if left else max(0, width - margin - w)
    y = margin if top else max(0, height - margin - h)
    return int(x), int(y), int(h)


def concat_text(entries) -> str:
    """ffmpeg's concat demuxer list for [(png path, seconds)] – the last picture named twice (the demuxer drops the
    last duration otherwise); quotes as obsrec.merge_files."""
    def q(p):
        return "file '" + str(p).replace("'", "'\\''") + "'\n"
    lines = ["ffconcat version 1.0\n"]
    for path, secs in entries:
        lines.append(q(path))
        lines.append(f"duration {max(0.001, secs):.3f}\n")
    if entries:
        lines.append(q(entries[-1][0]))
    return "".join(lines)
