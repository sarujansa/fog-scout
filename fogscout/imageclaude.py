"""1.35 (user's release of 3.11.2026: "Bilder aus Aufnahmen/Screenshots auf Klick, je Funktion eigenes Häkchen"):
the screenshot editor's „Mit Claude bearbeiten“. Pure, no Qt, no network.

The editor sends the picture as the user sees it in the editor – turned, coloured, already censored boxes and
drawings applied, not cropped (``picture``) – and the wish. Coordinates in the answer are fractions (0–1) of exactly
that picture, which are the editor's own coordinates (imageedit: fractions of the turned picture).

Claude answers with ``ops`` of a fixed set (SCHEMA). ``apply`` checks them on a copy of the edit; whatever does not
fit is skipped with a reason, never guessed. Boxes, crop and colour run first in the given order, turning and
mirroring last (imageedit.turned/flipped carry the boxes along), so every box of one answer refers to the picture
Claude saw. The window shows the result and applies it as one undo step only on „Übernehmen“."""
from __future__ import annotations

from . import imageedit
from .i18n import N_

MAX_OPS = 16
MAX_REQUEST = 400
MAX_BOXES = 20                   # censor boxes in one edit at most
KINDS = ("crop", "censor", "censor_style", "adjust", "rotate", "flip")
ASPECT_KEYS = tuple(k for k, _r in imageedit.ASPECTS)

SYSTEM = ("You are the editing assistant of a screenshot editor for Dead by Daylight screenshots. You see the "
          "picture as it is now and get the user's wish. Answer with operations that carry it out. Coordinates are "
          "fractions of the picture you see: x and y of the top left corner, w and h the size, each 0 to 1. "
          "Only use these operations: crop(x,y,w,h, optional aspect one of " + ", ".join(ASPECT_KEYS) + ") keeps "
          "only that area; censor(x,y,w,h) makes an area unreadable (player names, chat, friend lists – make the "
          "box generously larger than the text); censor_style(value) one of "
          + ", ".join(imageedit.CENSOR_STYLES) + "; adjust(brightness, contrast, saturation) factors between "
          f"{imageedit.ADJUST_RANGE[0]:g} and {imageedit.ADJUST_RANGE[1]:g}, 1 = unchanged, only the ones to "
          "change; rotate(quarters) 1 = 90° clockwise, 2, 3; flip(value) 'horizontal' or 'vertical'. If the wish "
          "cannot be done with these operations, return no operations and say why. Write 'summary' as one short "
          "sentence in the language of the wish.")

_OP = {"type": "object", "additionalProperties": False, "required": ["op"],
       "properties": {"op": {"type": "string", "enum": list(KINDS)},
                      "x": {"type": "number"}, "y": {"type": "number"},
                      "w": {"type": "number"}, "h": {"type": "number"},
                      "aspect": {"type": "string"}, "value": {"type": "string"},
                      "brightness": {"type": "number"}, "contrast": {"type": "number"},
                      "saturation": {"type": "number"}, "quarters": {"type": "integer"}}}
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["summary", "ops"],
          "properties": {"summary": {"type": "string"}, "ops": {"type": "array", "items": _OP}}}


def picture(original, edit: imageedit.ImageEdit):
    """What Claude sees: the editor's picture without the crop – censored boxes stay censored (never sent clear)."""
    return imageedit.render(original, edit, crop=False)


def content(wish: str) -> str:
    return "Wish: " + str(wish or "").strip()[:MAX_REQUEST]


def _num(op: dict, key: str):
    v = op.get(key)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    v = float(v)
    return v if v == v and abs(v) != float("inf") else None


def _box(op: dict):
    vals = [_num(op, k) for k in ("x", "y", "w", "h")]
    if None in vals:
        return None
    x, y, w, h = vals
    if w <= 0 or h <= 0 or x >= 1 or y >= 1 or x + w <= 0 or y + h <= 0:
        return None
    x0, y0 = max(0.0, x), max(0.0, y)
    return imageedit.clamp_box((x0, y0, min(1.0, x + w) - x0, min(1.0, y + h) - y0))


def _pct(v: float) -> int:
    return int(round(v * 100))


def apply(edit: imageedit.ImageEdit, ops, size: tuple):
    """(new edit, done, skipped) – ``done``/``skipped``: [(op, (text, kwargs))] for the window to translate.
    ``size``: the turned picture's size in pixels (for an aspect). ValueError when ``ops`` is not a list."""
    if not isinstance(ops, list):
        raise ValueError("ops")
    new = edit.copy()
    done, skipped = [], []
    turns = []
    for op in ops[:MAX_OPS]:
        kind = op.get("op") if isinstance(op, dict) else None
        if kind not in KINDS:
            skipped.append((op, (N_("unbekannter Schritt"), {})))
            continue
        if kind in ("rotate", "flip"):
            turns.append(op)
            continue
        if kind == "crop":
            box = _box(op)
            if box is None:
                skipped.append((op, (N_("Ausschnitt ausserhalb des Bildes"), {})))
                continue
            aspect = op.get("aspect")
            ratio = dict(imageedit.ASPECTS).get(aspect) if aspect in ASPECT_KEYS else None
            new.crop = imageedit.aspect_box(box, ratio, size)
            done.append((op, (N_("Zuschneiden auf {w} × {h} %"), {"w": _pct(new.crop[2]), "h": _pct(new.crop[3])})))
        elif kind == "censor":
            box = _box(op)
            if box is None:
                skipped.append((op, (N_("Kasten ausserhalb des Bildes"), {})))
                continue
            if len(new.censor) >= MAX_BOXES:
                skipped.append((op, (N_("zu viele Kästen"), {})))
                continue
            new.censor.append(box)
            done.append((op, (N_("Bereich unkenntlich machen ({x} %, {y} %)"), {"x": _pct(box[0]), "y": _pct(box[1])})))
        elif kind == "censor_style":
            v = op.get("value")
            if v not in imageedit.CENSOR_STYLES:
                skipped.append((op, (N_("unbekannte Art der Zensur"), {})))
                continue
            new.censor_style = v
            done.append((op, (N_("Zensur: {style}"), {"style": v})))
        elif kind == "adjust":
            lo, hi = imageedit.ADJUST_RANGE
            changed = False
            for key in ("brightness", "contrast", "saturation"):
                v = _num(op, key)
                if v is None:
                    continue
                setattr(new, key, max(lo, min(hi, v)))
                changed = True
            if not changed:
                skipped.append((op, (N_("Farbe ohne Werte"), {})))
                continue
            done.append((op, (N_("Farbe: Helligkeit {b} %, Kontrast {c} %, Sättigung {s} %"),
                              {"b": _pct(new.brightness), "c": _pct(new.contrast), "s": _pct(new.saturation)})))
    for op in turns:                     # last: every box above refers to the picture Claude saw
        if op["op"] == "rotate":
            q = op.get("quarters")
            if isinstance(q, bool) or not isinstance(q, int) or q % 4 == 0:
                skipped.append((op, (N_("Drehung ohne Winkel"), {})))
                continue
            w, h = size if new.rotate % 2 == edit.rotate % 2 else (size[1], size[0])
            new = imageedit.turned(new, q % 4, (w, h))
            done.append((op, (N_("Um {deg}° drehen"), {"deg": (q % 4) * 90})))
        else:
            v = op.get("value")
            if v not in ("horizontal", "vertical"):
                skipped.append((op, (N_("Spiegeln ohne Richtung"), {})))
                continue
            w, h = size if new.rotate % 2 == edit.rotate % 2 else (size[1], size[0])
            new = imageedit.flipped(new, v == "horizontal", (w, h))
            done.append((op, (N_("Spiegeln") if v == "horizontal" else N_("Kippen"), {})))
    return new, done, skipped
