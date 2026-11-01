"""Editor projects (1.16, user: "Projektname, Projekt speichern" in the editor's top bar): the whole edit plan of a
recording – clips, crop, drawings, fades, censoring, sound mix and export choices – as one JSON file below the
clips folder (``Clips/Projekte/<recording>.fogscout-project.json``), so a cut can be picked up again later. Pure:
dict in, dict out; the editor turns its state into the dict and back. Nothing but these own files is read."""
from __future__ import annotations

import json
import os
import time

from . import annotate
from .clipedit import Part, SPEEDS
from .sequence import EditState

FORMAT = "fogscout-project"
VERSION = 1
PROJECT_DIR = "Projekte"
EXT = ".fogscout-project.json"
MAX_PARTS = 500
MAX_SHAPES = 500
MAX_BOXES = 50


def project_path(clips_dir: str, source: str) -> str:
    """Where the project of recording ``source`` lives (by the recording's file name, without its extension)."""
    stem = os.path.splitext(os.path.basename(source))[0]
    return os.path.join(clips_dir, PROJECT_DIR, stem + EXT)


def exists(clips_dir: str, source: str) -> bool:
    try:
        return os.path.isfile(project_path(clips_dir, source))
    except (OSError, ValueError):
        return False


def to_dict(state: EditState, source: str, name: str, extra: dict | None = None) -> dict:
    """The project as JSON data: the state (sequence.EditState) plus ``extra`` (name of the clip, export format,
    encoding, sound mix – whatever the editor hands over, JSON-able)."""
    try:
        size = os.path.getsize(source)
    except OSError:
        size = 0
    return {"format": FORMAT, "version": VERSION, "saved": time.time(),
            "source": {"file": os.path.basename(source), "size": size},
            "name": str(name or ""),
            "parts": [[round(float(p.start), 3), round(float(p.end), 3), float(p.speed)] for p in state.parts],
            "crop": [round(float(v), 5) for v in state.crop] if state.crop else None,
            "crop_key": str(state.crop_key or "none"),
            "shapes": [annotate.to_dict(s) for s in state.shapes],
            "fade_in": float(state.fade_in), "fade_out": float(state.fade_out),
            "censor": {"on": bool(state.censor_on), "style": str(state.censor_style or "pixel"),
                       "boxes": [[round(float(v), 5) for v in b] for b in state.boxes]},
            "extra": dict(extra or {})}


def _box(v) -> list | None:
    try:
        x, y, w, h = (float(a) for a in v)
    except (TypeError, ValueError):
        return None
    if not (0 <= x <= 1 and 0 <= y <= 1 and 0 < w <= 1 and 0 < h <= 1):
        return None
    return [x, y, min(w, 1 - x), min(h, 1 - y)]


def from_dict(d, duration: float = 0.0) -> tuple[EditState, dict] | None:
    """(state, extra) from project data, or None when it is no project of ours or holds no usable clip. Parts are
    held inside ``duration`` (0 = unknown), tempos inside SPEEDS, broken shapes and boxes dropped."""
    if not isinstance(d, dict) or d.get("format") != FORMAT:
        return None
    try:
        parts = []
        for raw in list(d.get("parts") or [])[:MAX_PARTS]:
            s, e, sp = float(raw[0]), float(raw[1]), float(raw[2]) if len(raw) > 2 else 1.0
            s, e = max(0.0, s), (min(e, duration) if duration > 0 else e)
            if e - s >= 0.1:
                parts.append(Part(s, e, max(SPEEDS[0], min(SPEEDS[-1], sp))))
        if not parts:
            return None
        crop = _box(d.get("crop")) if d.get("crop") else None
        shapes = [s for s in (annotate.from_dict(x) for x in list(d.get("shapes") or [])[:MAX_SHAPES]) if s is not None]
        censor = d.get("censor") if isinstance(d.get("censor"), dict) else {}
        boxes = [b for b in (_box(x) for x in list(censor.get("boxes") or [])[:MAX_BOXES]) if b is not None]
        style = str(censor.get("style") or "pixel")
        state = EditState(parts, tuple(crop) if crop else None, str(d.get("crop_key") or ("free" if crop else "none")),
                          shapes, max(0.0, float(d.get("fade_in") or 0)), max(0.0, float(d.get("fade_out") or 0)),
                          boxes, bool(censor.get("on")), style if style in ("pixel", "blur", "black", "retouch") else "pixel")
        extra = d.get("extra") if isinstance(d.get("extra"), dict) else {}
        extra = dict(extra)
        extra.setdefault("name", str(d.get("name") or ""))
        return state, extra
    except (TypeError, ValueError, IndexError, AttributeError):
        return None


def save(path: str, data: dict) -> bool:
    """Write ``data`` (tmp + replace); False when the folder cannot be written."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1, ensure_ascii=False)
        os.replace(tmp, path)
        return True
    except (OSError, TypeError, ValueError):
        return False


def load(path: str) -> dict | None:
    try:
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
    except (OSError, ValueError):
        return None
    return d if isinstance(d, dict) and d.get("format") == FORMAT else None
