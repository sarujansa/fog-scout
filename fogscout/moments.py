"""Where something happens in a recording (1.39.2, user's pick "Short vorschlagen" – local first, Claude on click):
moments from the input changes (inputs companion file), the game sound (clipedit.waveform of track 1) and the F8
marks; idle stretches (nothing held, nothing changed); dark stretches at the start/end (loading screen). Pure – no
Qt, no ffmpeg, no network: the editor computes these locally; for „Short vorschlagen“ only the numbers (seconds,
changes per second) go to Claude, never which keys.

Times here are seconds of the recording (source time); ``*_ops`` turn them into editcommands operations in the
cut's output time (sequence.occurrences), latest first so the earlier times stay right while they are applied."""
from __future__ import annotations

from . import sequence

WINDOW_S = 5                  # seconds summed around each second for the score
MIN_GAP_S = 15.0              # two moments at least this far apart (peak to peak)
BEFORE_S, AFTER_S = 8.0, 6.0  # a moment is this long around its peak
MAX_MOMENTS = 8
MIN_SHARE = 0.35              # a peak needs this share of the best score
INPUT_WEIGHT, SOUND_WEIGHT = 0.65, 0.35
MARK_BONUS = 1.0              # an F8 mark adds this much at its second
IDLE_MIN_S = 8.0              # nothing held and nothing changed this long counts as idle …
IDLE_KEEP_S = 1.0             # … and keeps this much at each edge (no hard jump)
DARK_MIN_S = 1.0              # a dark run at the start/end this long is cut (loading screen)


def _changes_per_s(events, length: float) -> list:
    n = max(1, int(length) + 1)
    out = [0] * n
    for t, _c in events:
        k = int(t)
        if 0 <= k < n:
            out[k] += 1
    return out


def _sound_per_s(wave, per_s: int, length: float) -> list:
    n = max(1, int(length) + 1)
    if not wave or per_s <= 0:
        return [0.0] * n
    out = []
    for k in range(n):
        chunk = wave[k * per_s:(k + 1) * per_s]
        out.append(sum(chunk) / len(chunk) if chunk else 0.0)
    return out


def _norm(xs) -> list:
    top = max(xs, default=0) or 1
    return [x / top for x in xs]


def _window(xs, w: int) -> list:
    half = w // 2
    return [sum(xs[max(0, i - half):i + half + 1]) for i in range(len(xs))]


def scores(events, wave, wave_per_s: int, marks, length: float) -> list:
    """How much happens each second (0…, not normalised to 1 once marks add their bonus)."""
    inp = _norm(_window(_changes_per_s(events, length), WINDOW_S))
    snd = _norm(_window(_sound_per_s(wave, wave_per_s, length), WINDOW_S))
    out = [INPUT_WEIGHT * a + SOUND_WEIGHT * b for a, b in zip(inp, snd)]
    for m in marks:
        k = int(m)
        if 0 <= k < len(out):
            out[k] += MARK_BONUS
    return out


def find(events, wave, wave_per_s: int, marks, length: float) -> list:
    """The moments of one recording: [(t0, t1, peak second, score, kind)], sorted by time. ``kind`` = "mark" (an F8
    mark near the peak), "keys" (busy keys) or "sound" (loud game sound)."""
    if length <= 0 or not (events or wave or marks):
        return []
    sc = scores(events, wave, wave_per_s, marks, length)
    best = max(scores(events, wave, wave_per_s, (), length), default=0)   # the marks' bonus never raises the bar
    if max(sc, default=0) <= 0:
        return []
    best = best or max(sc)
    inp = _norm(_window(_changes_per_s(events, length), WINDOW_S))
    taken = []
    for k in sorted(range(len(sc)), key=lambda i: -sc[i]):
        if sc[k] < MIN_SHARE * best or len(taken) >= MAX_MOMENTS:
            break
        if any(abs(k - p) < MIN_GAP_S for p, *_r in taken):
            continue
        near_mark = any(abs(m - k) <= BEFORE_S for m in marks)
        kind = "mark" if near_mark else ("keys" if inp[k] >= 0.5 else "sound")
        taken.append((k, round(sc[k], 3), kind))
    out = [(max(0.0, p - BEFORE_S), min(float(length), p + AFTER_S), float(p), s, kind) for p, s, kind in taken]
    return sorted(out, key=lambda m: m[0])


def idle(events, length: float, min_s: float = IDLE_MIN_S) -> list:
    """Stretches where nothing is held and nothing changes for at least ``min_s`` (standing, waiting) – [(t0, t1)]
    with IDLE_KEEP_S left at each edge. Holding W to run is not idle (a key is held). Needs the inputs; [] without."""
    if not events:
        return []
    out = []
    points = list(events) + [(float(length), -1)]
    for (t, code), (t_next, _c) in zip(points, points[1:]):
        if code == 0 and t_next - t >= min_s:
            a, b = t + IDLE_KEEP_S, t_next - IDLE_KEEP_S
            if b - a > 0.5:
                out.append((round(a, 2), round(b, 2)))
    first = events[0][0]
    if first >= min_s:                                   # nothing at all before the first change
        out.insert(0, (round(IDLE_KEEP_S, 2), round(first - IDLE_KEEP_S, 2)))
    return out


def dark_edges(dark_start, dark_end, step: float, length: float) -> list:
    """Loading screen at the start / end: ``dark_start`` = is_dark of the pictures at 0, step, 2·step …;
    ``dark_end`` = of the pictures at length − step, length − 2·step … (backwards). [(t0, t1)] of output time to
    cut – a run counts from DARK_MIN_S."""
    out = []
    lead = 0
    for d in dark_start:
        if not d:
            break
        lead += 1
    if lead * step >= DARK_MIN_S:
        out.append((0.0, round(min(length, lead * step), 2)))
    trail = 0
    for d in dark_end:
        if not d:
            break
        trail += 1
    if trail * step >= DARK_MIN_S and length - trail * step > (out[0][1] if out else 0.0):
        out.append((round(max(0.0, length - trail * step), 2), round(length, 2)))
    return out


def to_output(parts, ranges, src: int = 0) -> list:
    """Source ranges of recording ``src`` → the output ranges they play at in the cut (each part they touch;
    stills skipped), sorted."""
    out = []
    for i, p in enumerate(parts):
        if p.hold > 0 or getattr(p, "src", 0) != src:
            continue
        for a, b in ranges:
            lo, hi = max(a, p.start), min(b, p.end)
            if hi - lo <= 0.05:
                continue
            x, y = sequence.output_at(parts, i, lo), sequence.output_at(parts, i, hi)
            out.append((round(min(x, y), 2), round(max(x, y), 2)))
    return sorted(out)


def cut_ops(out_ranges) -> list:
    """Output ranges → editcommands cut operations, latest first (the earlier ones keep their times)."""
    return [{"op": "cut", "from": a, "to": b} for a, b in sorted(out_ranges, reverse=True)]


def facts(moments_out, length: float, marks_out) -> str:
    """What Claude gets of the moments for „Short vorschlagen“: numbers only."""
    def r(t):
        return f"{round(float(t), 1):g}"
    lines = [f"Clip length: {r(length)} s.",
             "F8 marks at: " + (", ".join(f"{r(m)} s" for m in sorted(marks_out)) or "none") + "."]
    if moments_out:
        lines.append("Busy moments found locally (key changes and game sound, strongest first): "
                     + "; ".join(f"{r(a)}–{r(b)} s ({kind}, score {s:.2f})"
                                 for a, b, s, kind in sorted(moments_out, key=lambda m: -m[2])) + ".")
    else:
        lines.append("No busy moments found locally.")
    return " ".join(lines)
