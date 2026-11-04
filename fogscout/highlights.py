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


def still_times(length: float, marks=()) -> list:
    """The output seconds to take stills at: EVEN_STILLS in the middle of equal stretches, the marks (at most
    MAX_MARK_STILLS) replacing an even still closer than MERGE_S. Sorted, inside [0, length)."""
    if length <= 0:
        return []
    even = [length * (i + 0.5) / EVEN_STILLS for i in range(EVEN_STILLS)]
    inside = sorted({_r(m) for m in marks if 0 <= m < length})[:MAX_MARK_STILLS]
    kept = [t for t in even if all(abs(t - m) > MERGE_S for m in inside)]
    return sorted(_r(t) for t in kept + inside)


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
