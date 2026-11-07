"""1.37 (user: "Weiter" – the highlight search proposed after 1.36): Claude looks at stills of the clip being edited
and names up to three ranges worth a short. Pure, no Qt, no network.

What goes out (only on the click „Highlights finden“, only with the switch „Standbilder aus Aufnahmen im Clip-Editor
an Claude schicken“): small stills at ``still_times`` – spread evenly over the edit plus one at each F8 mark –, each
labelled with its output second, the edit's length and the marks. The editor hides the censor boxes in every still
before it is sent (editorclaude). Never a path, a file name, a map or a killer.

What comes back counts only as ranges that ``parse`` accepts: inside the clip, at least ``MIN_S`` and at most
``MAX_S`` long, no overlap, at most ``MAX_HIGHLIGHTS``. A picked range becomes the operation keep(from, to), which
editcommands.apply checks again; the editor applies it only on „Übernehmen“ (one undo step)."""
from __future__ import annotations

MAX_HIGHLIGHTS = 3
MIN_S = 5.0                 # a highlight shorter than this is no clip
MAX_S = 60.0                # … longer is no short (YouTube Shorts allow up to 3 min, a highlight is shorter)
EVEN_STILLS = 16            # stills spread over the edit
MAX_MARK_STILLS = 8         # stills at F8 marks at most
MAX_PEAK_STILLS = 8         # 1.39.2: stills at the local moments (moments.find) at most
MERGE_S = 2.0               # a mark this close to an even still replaces it (no two pictures of the same moment)
STILL_H = 360               # height of a still as ffmpeg decodes it …
STILL_SIDE = 640            # … and its long side as sent (askclaude.image_block)
MAX_WHY = 120               # characters of a reason shown

SYSTEM = ("You find the highlights of a Dead by Daylight gameplay recording for its player. You get stills of the "
          "clip, each labelled with its time in seconds, the clip's length and the moments the player marked with "
          "F8 (marked moments are likely worth a look). Name up to three ranges that would make the best short "
          "clips: a chase, a save, a hook, a down, an escape, a funny moment. Each range must lie inside the clip, "
          f"be {MIN_S:g} to {MAX_S:g} seconds long and not overlap another; best first. 'why' is a few words in "
          "the language given. If nothing stands out, return no ranges and say so in 'summary'.")

SCHEMA = {"type": "object", "additionalProperties": False, "required": ["summary", "highlights"],
          "properties": {"summary": {"type": "string"},
                         "highlights": {"type": "array", "items": {
                             "type": "object", "additionalProperties": False, "required": ["from", "to", "why"],
                             "properties": {"from": {"type": "number"}, "to": {"type": "number"},
                                            "why": {"type": "string"}}}}}}


def _r(t: float) -> float:
    return round(float(t), 1)


def still_times(length: float, marks=(), peaks=()) -> list:
    """The output seconds to take stills at: EVEN_STILLS in the middle of equal stretches, the marks (at most
    MAX_MARK_STILLS) and – 1.39.2 – the local moments' peaks (at most MAX_PEAK_STILLS) replacing an even still closer
    than MERGE_S. Sorted, inside [0, length), no two closer than MERGE_S."""
    if length <= 0:
        return []
    even = [length * (i + 0.5) / EVEN_STILLS for i in range(EVEN_STILLS)]
    inside = sorted({_r(m) for m in marks if 0 <= m < length})[:MAX_MARK_STILLS]
    for p in [_r(p) for p in peaks if 0 <= p < length][:MAX_PEAK_STILLS]:
        if all(abs(p - m) > MERGE_S for m in inside):
            inside.append(p)
    kept = [t for t in even if all(abs(t - m) > MERGE_S for m in inside)]
    return sorted(_r(t) for t in kept + inside)


SHORT_WISH = ("Make one vertical short (mode shorts) of at most {limit} seconds from the best of this clip: keep the "
              "best range (a busy moment or a mark), cut the rest, slow the key second down to 0.5 for 1 to 2 "
              "seconds if it helps, add a short_title of at most six words and two to four subtitles at the key "
              "moments. Titles and subtitles in {language}, no player names.")


def blocks(length: float, marks, stills, language: str) -> list:
    """The user content: the facts, then each still as a label and its image block. ``stills``: [(second, block)]."""
    facts = (f"Clip length: {_r(length)} s. F8 marks at: "
             + (", ".join(f"{_r(m)} s" for m in sorted(marks)) if marks else "none")
             + f". Answer 'why' and 'summary' in {language}.")
    out = [{"type": "text", "text": facts}]
    for t, block in stills:
        out += [{"type": "text", "text": f"Still at {_r(t)} s:"}, block]
    return out


def _num(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    v = float(v)
    return v if v == v and abs(v) != float("inf") else None


def parse(data: dict, length: float) -> tuple[str, list]:
    """(summary, [(from, to, why)]) – only ranges inside the clip, MIN_S to MAX_S long, not overlapping one taken
    before (Claude's order: best first), at most MAX_HIGHLIGHTS. ValueError when 'highlights' is not a list."""
    items = data.get("highlights") if isinstance(data, dict) else None
    if not isinstance(items, list):
        raise ValueError("highlights")
    out = []
    for h in items:
        if not isinstance(h, dict):
            continue
        a, b = _num(h.get("from")), _num(h.get("to"))
        if a is None or b is None:
            continue
        a, b = max(0.0, a), min(float(length), b)
        if not MIN_S - 1e-6 <= b - a <= MAX_S + 1e-6:
            continue
        if any(a < y and x < b for x, y, _w in out):
            continue
        out.append((_r(a), _r(b), " ".join(str(h.get("why") or "").split())[:MAX_WHY]))
        if len(out) >= MAX_HIGHLIGHTS:
            break
    return " ".join(str(data.get("summary") or "").split())[:300], out


# ---- 1.42: „Export prüfen“ – stills of the finished cut, Claude names what should not be shared like this
CHECK_STILLS = 8            # stills spread over the cut
CHECK_H = 540               # bigger than a highlight still: a name must stay readable …
CHECK_SIDE = 960            # … long side as sent
MAX_FINDINGS = 6
CHECK_KINDS = ("name", "chat", "other")
CHECK_WINDOW_S = 2.0        # a box set from a finding hides this long before and after its moment (recording time)

CHECK_SYSTEM = ("You check a Dead by Daylight clip before its player shares it. You get stills of the finished cut, "
                "each labelled with its time in seconds; areas already hidden are blurred or black. Report what "
                "should not be shared like this: a readable player name (kind 'name') or chat text (kind 'chat') – "
                "with 'box' = [x, y, w, h] around it as fractions (0–1) of that still – and anything else clearly "
                "wrong, e.g. a loading screen or menu left in (kind 'other', 'box' empty). Game labels, perk or item "
                "names and timers are fine. At most six findings, 'why' a few words and 'summary' one sentence in the "
                "language given. Nothing to report: an empty list.")

CHECK_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["summary", "findings"],
                "properties": {"summary": {"type": "string"},
                               "findings": {"type": "array", "items": {
                                   "type": "object", "additionalProperties": False,
                                   "required": ["at", "kind", "why", "box"],
                                   "properties": {"at": {"type": "number"},
                                                  "kind": {"type": "string", "enum": list(CHECK_KINDS)},
                                                  "why": {"type": "string"},
                                                  "box": {"type": "array", "items": {"type": "number"}}}}}}}


def check_times(length: float) -> list:
    """The output seconds of the stills: the middles of CHECK_STILLS equal stretches (none for an empty cut)."""
    if length <= 0:
        return []
    step = float(length) / CHECK_STILLS
    return [_r(step * (k + 0.5)) for k in range(CHECK_STILLS)]


def check_blocks(length: float, stills, language: str) -> list:
    """The user content: the length and the language, then each still as a label and its image block."""
    out = [{"type": "text", "text": f"Clip length: {_r(length)} s. Answer 'why' and 'summary' in {language}."}]
    for t, block in stills:
        out += [{"type": "text", "text": f"Still at {_r(t)} s:"}, block]
    return out


def _box(v):
    """[x, y, w, h] inside the still (fractions), None for anything else (an empty list = no box)."""
    if not isinstance(v, list) or len(v) != 4 or any(_num(x) is None for x in v):
        return None
    x, y, w, h = (float(a) for a in v)
    x0, y0 = max(0.0, x), max(0.0, y)
    x1, y1 = min(1.0, x + w), min(1.0, y + h)
    if x1 - x0 < 0.005 or y1 - y0 < 0.005:
        return None
    return [round(x0, 4), round(y0, 4), round(x1 - x0, 4), round(y1 - y0, 4)]


def check_parse(data, length: float) -> tuple[str, list]:
    """(summary, [(at, kind, why, box or None)]) sorted by time – only times inside the cut, known kinds, a box only
    for names and chat; at most MAX_FINDINGS. ValueError when 'findings' is not a list."""
    items = data.get("findings") if isinstance(data, dict) else None
    if not isinstance(items, list):
        raise ValueError("findings")
    out = []
    for f in items[:MAX_FINDINGS * 2]:
        if not isinstance(f, dict) or f.get("kind") not in CHECK_KINDS:
            continue
        at = _num(f.get("at"))
        if at is None or not 0 <= at <= float(length):
            continue
        box = _box(f.get("box")) if f["kind"] in ("name", "chat") else None
        out.append((_r(at), f["kind"], " ".join(str(f.get("why") or "").split())[:MAX_WHY], box))
        if len(out) >= MAX_FINDINGS:
            break
    return " ".join(str(data.get("summary") or "").split())[:300], sorted(out, key=lambda f: f[0])


def uncrop(box, crop):
    """A box on a still cut to ``crop`` (fractions of the recording) → fractions of the whole recording."""
    if not crop:
        return list(box)
    cx, cy, cw, ch = crop[:4]
    return [round(cx + box[0] * cw, 4), round(cy + box[1] * ch, 4), round(box[2] * cw, 4), round(box[3] * ch, 4)]
