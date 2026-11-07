"""1.27 (user: Claude in the clip editor – "Befehle in Worten"): what the editor sends to Claude and how Claude's
answer becomes edits. Pure, no Qt, no network.

``describe`` turns the editor's state into the numbers Claude sees: the finished clip's length, each clip's place
on the output time axis, its tempo and whether it is a still, the fades, the export mode, an own short title and
subtitles, the F8 marks. Never a path, a file name, a map or a killer (CLAUDE.md, harte Regel „Claude“).

Claude answers with ``ops`` of a fixed set (SCHEMA). ``apply`` checks and runs them one after the other on a copy
through the sequence functions the timeline uses; whatever does not fit is skipped with a reason, never guessed.
The editor shows the result and applies it as one undo step only when the user says so."""
from __future__ import annotations

from dataclasses import replace

from . import clipedit, sequence, shorts
from .i18n import N_

MAX_OPS = 12                     # operations taken from one answer at most
MAX_REQUEST = 400                # characters of the user's wish sent at most
MAX_TITLE = 80                   # characters of a short's title
MAX_SUB = 120                    # characters of one subtitle
EPS = 0.05                       # seconds: edges this close count as the same moment
KINDS = ("cut", "keep", "speed", "split", "hold", "fade", "mode", "short_title", "subtitle", "censor")
MAX_BOXES = 20                   # 1.35: censor boxes in one edit at most
MAX_ROUNDS = 3                   # 1.43.1: requests of one talk at most (Claude may ask back twice)
MAX_QUESTION = 200               # characters of Claude's question shown at most
MAX_WHY = 120                    # characters of the reason of one step shown at most

SYSTEM = ("You are the editing assistant of a clip editor for Dead by Daylight gameplay recordings. You get the "
          "current edit as JSON (all times are seconds of the finished clip, the 'output time') and the user's "
          "wish. Answer with the operations that carry it out, in the order they should run; times of later "
          "operations refer to the clip as it is after the earlier ones. Only use these operations: "
          "cut(from,to) removes a range; keep(from,to) keeps only a range; speed(from,to,factor) with factor one of "
          + ", ".join(f"{s:g}" for s in clipedit.SPEEDS) + "; split(at); hold(at,seconds) inserts a freeze frame; "
          "fade(in,out) seconds of fade-in/out, each one of " + ", ".join(f"{f:g}" for f in clipedit.FADES)
          + "; mode(value) export mode, one of " + ", ".join(clipedit.MODES) + " ('shorts' = vertical 9:16 for "
          "YouTube Shorts/TikTok); short_title(text) and subtitle(from,to,text) only for mode shorts. Use 'marks' "
          "(moments the player marked with F8) when the wish refers to marked moments. Only when a picture of the "
          "recording is attached: censor(x,y,w,h) hides an area of the whole recording (player names, chat, friend "
          "lists), as fractions 0–1 of that picture (x, y = top left corner) – make the box generously larger than "
          "the text. If the wish cannot be done "
          "with these operations, return no operations and say why. Write 'summary' as one short sentence in the "
          "language of the wish. Give each operation a short 'why' in that language. Only when the wish is unclear "
          "in a way that changes the result (e.g. which of several marked moments), you may return no operations "
          "and ask one short 'question' in that language instead; the user's answer follows. Otherwise leave "
          "'question' empty.")

_OP = {"type": "object", "additionalProperties": False, "required": ["op"],
       "properties": {"op": {"type": "string", "enum": list(KINDS)},
                      "from": {"type": "number"}, "to": {"type": "number"}, "at": {"type": "number"},
                      "factor": {"type": "number"}, "seconds": {"type": "number"},
                      "in": {"type": "number"}, "out": {"type": "number"},
                      "value": {"type": "string"}, "text": {"type": "string"}, "why": {"type": "string"},
                      "x": {"type": "number"}, "y": {"type": "number"},
                      "w": {"type": "number"}, "h": {"type": "number"}}}
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["summary", "ops"],
          "properties": {"summary": {"type": "string"}, "ops": {"type": "array", "items": _OP},
                         "question": {"type": "string"}}}


def plain(t, limit: int) -> str:
    """1.43.1: one line of plain text from Claude – control and format characters out, at most ``limit``."""
    import unicodedata
    text = "".join(c for c in str(t if isinstance(t, str) else "") if unicodedata.category(c)[0] != "C")
    return " ".join(text.split())[:limit].strip()


def question(data) -> str:
    """1.43.1: Claude's question back – only when it gave no operation (a proposal always wins), else ""."""
    if not isinstance(data, dict) or data.get("ops"):
        return ""
    return plain(data.get("question"), MAX_QUESTION)


def follow_up(answer: str, rounds: int) -> str:
    """1.43.1: the user's answer to Claude's question as the next user turn; the last allowed round says so, then
    Claude must decide (``rounds`` = requests sent so far in this talk)."""
    text = "Answer to your question: " + str(answer or "").strip()[:MAX_REQUEST]
    if rounds + 1 >= MAX_ROUNDS:
        text += "\n\nNo more questions now: answer with operations, or with none and say why."
    return text


def _r(t: float) -> float:
    return round(float(t), 2)


def describe(state: sequence.EditState, mode: str, marks=()) -> dict:
    """What Claude sees of the edit. ``marks`` = output times of the F8 marks (sequence.occurrences)."""
    parts = state.parts
    st = sequence.starts(parts)
    out = {"length": _r(st[-1]),
           "clips": [{"from": _r(st[i]), "to": _r(st[i + 1]), "speed": p.speed, "still": p.hold > 0}
                     for i, p in enumerate(parts)],
           "fade_in": state.fade_in, "fade_out": state.fade_out, "mode": mode,
           "marks": [_r(t) for t in sorted(marks)][:50]}
    if state.short is not None:
        out["short_title"] = state.short.title
        out["subtitles"] = [{"from": _r(s.t0), "to": _r(s.t1), "text": s.text} for s in state.short.subs][:50]
    return out


def content(wish: str, state: sequence.EditState, mode: str, marks=(), picture: bool = False) -> str:
    """1.35: ``picture`` = a still of the recording goes along (the user's switch) – said, so Claude may censor."""
    import json
    seen = ("\n\nAttached: a still of the recording at the play head (censored areas already hidden)."
            if picture else "\n\nNo picture is attached.")
    return ("Current edit:\n" + json.dumps(describe(state, mode, marks), ensure_ascii=False) + seen
            + "\n\nWish: " + str(wish or "").strip()[:MAX_REQUEST])


def _num(op: dict, key: str):
    v = op.get(key)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    v = float(v)
    return v if v == v and abs(v) != float("inf") else None


def _cut_at(parts, t: float):
    """``parts`` with a boundary at output ``t`` (unchanged when one is already there or the piece would be too
    short)."""
    st = sequence.starts(parts)
    if any(abs(t - s) <= EPS for s in st):
        return parts
    out, _j = sequence.split(parts, t)
    return out


def _inside(parts, a: float, b: float) -> list:
    """Indexes of the parts lying within output [a, b]."""
    st = sequence.starts(parts)
    return [i for i in range(len(parts)) if st[i] >= a - EPS and st[i + 1] <= b + EPS]


def _fmt(t: float) -> str:
    return clipedit.fmt_pos(max(0.0, t))


def _valid_fade(v) -> bool:
    return v is not None and any(abs(v - f) <= 1e-3 for f in clipedit.FADES)


def _box(op: dict):
    """1.35: a censor box (fractions) cut to the picture, None when it lies outside or is empty."""
    vals = [_num(op, k) for k in ("x", "y", "w", "h")]
    if None in vals:
        return None
    x, y, w, h = vals
    if w <= 0 or h <= 0 or x >= 1 or y >= 1 or x + w <= 0 or y + h <= 0:
        return None
    x0, y0 = max(0.0, x), max(0.0, y)
    w, h = min(1.0, x + w) - x0, min(1.0, y + h) - y0
    if w < 0.005 or h < 0.005:
        return None
    return [round(x0, 4), round(y0, 4), round(w, 4), round(h, 4)]


def apply(state: sequence.EditState, ops, mode: str, picture: bool = False):
    """(new state, new mode, done, skipped) – ``done``/``skipped`` are (op, (German key, values)) for the list in the
    editor. 1.28 (audit B1–B5): every invalid value is refused, never moved to a limit; an operation that would change
    nothing is "skipped: keine Änderung", never "done"; ``new mode`` is None unless a valid ``mode`` operation set it
    (the export type the user chose meanwhile stays); ``ops`` that are not a list raise ValueError (the editor says
    Claude answered something it cannot read). An answer that would leave no clip changes nothing."""
    if not isinstance(ops, list):
        raise ValueError("ops is not a list")
    new = state.copy()
    new_mode = None
    done, skipped = [], []
    for raw in ops[:MAX_OPS]:
        op = raw if isinstance(raw, dict) else {}
        kind = op.get("op")
        parts = new.parts
        total = sequence.duration(parts)
        mode_now = new_mode or mode
        if kind not in KINDS:
            skipped.append((op, (N_("unbekannte Aktion"), {})))
            continue
        if kind == "censor":                             # 1.35: only with a still – else Claude cannot see where
            box = _box(op) if picture else None
            if not picture:
                skipped.append((op, (N_("Zensur nur mit Standbild"), {})))
            elif box is None:
                skipped.append((op, (N_("Kasten ausserhalb des Bildes"), {})))
            elif len(new.boxes) >= MAX_BOXES:
                skipped.append((op, (N_("zu viele Kästen"), {})))
            else:
                new.boxes.append(box)
                new.censor_on = True
                done.append((op, (N_("Bereich unkenntlich machen ({x} %, {y} %)"),
                                  {"x": int(round(box[0] * 100)), "y": int(round(box[1] * 100))})))
            continue
        if kind in ("cut", "keep", "speed"):
            a, b = _num(op, "from"), _num(op, "to")
            if a is None or b is None:
                skipped.append((op, (N_("Zeiten fehlen"), {})))
                continue
            if a < 0 or a >= total:
                skipped.append((op, (N_("Bereich zu kurz oder ausserhalb"), {})))
                continue
            b = min(b, total)                            # "to the end" may name any later second
            if b - a < sequence.MIN_LEN:
                skipped.append((op, (N_("Bereich zu kurz oder ausserhalb"), {})))
                continue
            factor = None
            if kind == "speed":
                factor = _num(op, "factor")
                if factor is None or not any(abs(factor - s) < 1e-6 for s in clipedit.SPEEDS):
                    skipped.append((op, (N_("Tempo nicht erlaubt"), {})))
                    continue
            cut = _cut_at(_cut_at(parts, a), b)
            inside = _inside(cut, a, b)
            if kind == "speed":
                for i in inside:
                    cut = sequence.with_speed(cut, i, factor)
                words = (N_("{a}–{b} mit Tempo {f}×"), {"a": _fmt(a), "b": _fmt(b), "f": f"{factor:g}"})
            else:
                keep = [p for i, p in enumerate(cut) if (i in set(inside)) == (kind == "keep")]
                if not keep:
                    skipped.append((op, (N_("würde alles entfernen"), {})))
                    continue
                cut = keep
                words = (N_("{a}–{b} herausgeschnitten") if kind == "cut" else N_("nur {a}–{b} behalten"),
                         {"a": _fmt(a), "b": _fmt(b)})
            if abs(sequence.duration(cut) - total) < 1e-9:   # nothing removed / no tempo changed (only split)
                skipped.append((op, (N_("keine Änderung"), {})))      # e.g. a range too close to a clip's edge
                continue
            new.parts = cut
            done.append((op, words))
        elif kind == "split":
            t = _num(op, "at")
            if t is None or not EPS < t < total - EPS:
                skipped.append((op, (N_("Stelle ausserhalb"), {})))
                continue
            cut = _cut_at(parts, t)
            if cut == parts:
                skipped.append((op, (N_("keine Änderung"), {})))
                continue
            new.parts = cut
            done.append((op, (N_("Schnitt bei {a}"), {"a": _fmt(t)})))
        elif kind == "hold":
            t, sec = _num(op, "at"), _num(op, "seconds")
            if t is None or not 0 <= t <= total:
                skipped.append((op, (N_("Stelle ausserhalb"), {})))
                continue
            if sec is None or not 0.1 <= sec <= clipedit.HOLD_MAX_S:
                skipped.append((op, (N_("Standbild: Dauer ungültig"), {})))
                continue
            new.parts, _j = sequence.insert_hold(parts, min(t, max(0.0, total - EPS)), sec)
            done.append((op, (N_("Standbild bei {a} für {s} s"), {"a": _fmt(t), "s": f"{sec:g}"})))
        elif kind == "fade":
            fi, fo = _num(op, "in"), _num(op, "out")
            if "in" not in op and "out" not in op:
                skipped.append((op, (N_("Blende ohne Dauer"), {})))
                continue
            if ("in" in op and not _valid_fade(fi)) or ("out" in op and not _valid_fade(fo)):
                skipped.append((op, (N_("Blende ungültig"), {})))
                continue
            before = (new.fade_in, new.fade_out)
            if fi is not None:
                new.fade_in = min(clipedit.FADES, key=lambda f: abs(f - fi))
            if fo is not None:
                new.fade_out = min(clipedit.FADES, key=lambda f: abs(f - fo))
            if (new.fade_in, new.fade_out) == before:
                skipped.append((op, (N_("keine Änderung"), {})))
                continue
            done.append((op, (N_("Blenden: ein {i} s, aus {o} s"), {"i": f"{new.fade_in:g}", "o": f"{new.fade_out:g}"})))
        elif kind == "mode":
            value = str(op.get("value") or "")
            if value not in clipedit.MODES:
                skipped.append((op, (N_("Export-Art unbekannt"), {})))
                continue
            if value == mode_now:
                skipped.append((op, (N_("keine Änderung"), {})))
                continue
            new_mode = value
            done.append((op, (N_("Export-Art: {m}"), {"m": value})))
        elif kind in ("short_title", "subtitle"):
            if mode_now != "shorts":
                skipped.append((op, (N_("nur bei Export-Art Short"), {})))
                continue
            text = " ".join(str(op.get("text") or "").split())
            if not text:
                skipped.append((op, (N_("Text fehlt"), {})))
                continue
            spec = new.short.copy() if new.short is not None else shorts.ShortSpec()
            if kind == "short_title":
                spec = replace(spec, title=text[:MAX_TITLE])
                done.append((op, (N_("Short-Titel „{t}“"), {"t": text[:MAX_TITLE]})))
            else:
                a, b = _num(op, "from"), _num(op, "to")
                if a is None or b is None:
                    skipped.append((op, (N_("Untertitel: Zeiten fehlen"), {})))
                    continue
                if a < 0 or a >= total:
                    skipped.append((op, (N_("Stelle ausserhalb"), {})))
                    continue
                b = min(b, total)                         # first to the clip's end, then the shortest length
                if b - a < 0.2:
                    skipped.append((op, (N_("Untertitel zu kurz"), {})))
                    continue
                if len(spec.subs) >= shorts.MAX_SUBS:
                    skipped.append((op, (N_("zu viele Untertitel"), {})))
                    continue
                spec.subs.append(shorts.Sub(a, b, text[:MAX_SUB]))
                done.append((op, (N_("Untertitel {a}–{b}"), {"a": _fmt(a), "b": _fmt(b)})))
            new.short = spec
    if len(ops) > MAX_OPS:
        skipped.append((None, (N_("{n} weitere Schritte nicht ausgeführt (höchstens {max})"),
                               {"n": len(ops) - MAX_OPS, "max": MAX_OPS})))
    if not new.parts:
        return state.copy(), None, [], [(None, (N_("würde alles entfernen"), {}))]
    return new, new_mode, done, skipped
