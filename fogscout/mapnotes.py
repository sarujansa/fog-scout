"""Own notes per map (1.8.54, user: "Notizen für die Map"): written on the maps page, shown in the game with the
map's lines (timer, record, server). Pure – settings key ``map_notes`` = {map_id: text}.
"""
from __future__ import annotations

from .media import wrap

KEY = "map_notes"
KILLER_KEY = "killer_notes"   # 1.38.30 (project review F5): {killer: text}, shown once the round's killer is known
MAX_CHARS = 300          # what the maps page keeps of a note
LINE_CHARS = 34          # characters per line in the game (the card stays about as wide as the record chip)
MAX_LINES = 4            # lines in the game; more ends with "…"


def clean(text) -> str:
    """The note as stored: lines without trailing blanks, no empty lines at the ends, at most MAX_CHARS."""
    lines = [line.rstrip() for line in str(text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    return "\n".join(lines).strip("\n ")[:MAX_CHARS].rstrip()


def get(notes, map_id) -> str:
    return clean((notes or {}).get(str(map_id), "")) if isinstance(notes, dict) else ""


def put(notes, map_id, text) -> dict:
    """A new dict with the note of ``map_id`` set ("" removes it)."""
    out = {str(k): str(v) for k, v in (notes or {}).items() if isinstance(notes, dict)}
    text = clean(text)
    if text:
        out[str(map_id)] = text
    else:
        out.pop(str(map_id), None)
    return out


def lines(text) -> tuple:
    """The note as lines for the overlay: each written line wrapped at LINE_CHARS, at most MAX_LINES."""
    out = []
    for part in clean(text).split("\n"):
        out += wrap(part, LINE_CHARS, MAX_LINES + 1) if part.strip() else []
    if len(out) > MAX_LINES:
        last = out[MAX_LINES - 1]
        out = out[:MAX_LINES - 1] + [(last[:LINE_CHARS - 1].rstrip() if len(last) >= LINE_CHARS else last) + "…"]
    return tuple(out)


def memo_lines(map_note, killer_note, killer: str = "") -> tuple:
    """1.38.30: the overlay's note block – the map's note, then the killer's ("Nurse: …"); together at most
    MAX_LINES (the map's note first, the killer's gets what is left – at least one line when there is one)."""
    first = lines(map_note)
    k = clean(killer_note)
    if not k:
        return first
    head = f"{killer}: " if killer else ""
    second = lines(head + k.replace("\n", " · "))
    room = max(1, MAX_LINES - len(first))
    first = first[:MAX_LINES - room] if len(first) + room > MAX_LINES else first
    if len(second) > room:
        last = second[room - 1]
        second = second[:room - 1] + ((last[:LINE_CHARS - 1].rstrip() if len(last) >= LINE_CHARS else last) + "…",)
    return tuple(first) + tuple(second)
