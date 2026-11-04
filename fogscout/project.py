"""Editor projects (1.16, user: "Projektname, Projekt speichern" in the editor's top bar): the whole edit plan of a
recording – clips, crop, drawings, fades, censoring, sound mix and export choices – as one JSON file below the
clips folder (``Clips/Projekte/<recording>.fogscout-project.json``), so a cut can be picked up again later. Pure:
dict in, dict out; the editor turns its state into the dict and back. Nothing but these own files is read."""
from __future__ import annotations

import json
import os
import time
from dataclasses import replace

from . import annotate, clipedit, fsops
from .clipedit import Part, SPEEDS
from .sequence import EditState

FORMAT = "fogscout-project"
VERSION = 1
PROJECT_DIR = "Projekte"
EXT = ".fogscout-project.json"
MAX_PARTS = 500
MAX_SHAPES = 500
MAX_BOXES = 50
MAX_SOURCES = 50                  # 1.22: recordings of one montage
MONTAGE_DIR = "Montagen"          # 1.22: montage projects – Clips/Montagen, bound to no single recording


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
            "parts": [_part_row(p) for p in state.parts],
            "crop": [round(float(v), 5) for v in state.crop] if state.crop else None,
            "crop_key": str(state.crop_key or "none"),
            "shapes": [annotate.to_dict(s) for s in state.shapes],
            "fade_in": float(state.fade_in), "fade_out": float(state.fade_out),
            "censor": {"on": bool(state.censor_on), "style": str(state.censor_style or "pixel"),
                       "boxes": [[round(float(v), 5) for v in b] for b in state.boxes]},
            "extra": dict(extra or {}), **_short_field(state), **_music_field(state),
            **_sources_field(state)}


def _short_field(state) -> dict:
    """1.20: {"short": …} only when the state has one – a cut without it has the content (and hash) of 1.19."""
    from . import shorts
    d = shorts.to_dict(getattr(state, "short", None))
    return {"short": d} if d else {}


def _music_field(state) -> dict:
    """1.21: {"music": …} only when the state has a track A2 – without it the content (and hash) of 1.20."""
    from . import musictrack
    d = musictrack.to_dict(getattr(state, "music", None))
    return {"music": d} if d else {}


def _sources_field(state) -> dict:
    """1.22: {"sources": [paths]} only for a montage – the files Part.src / Shape.src point at (in the content: the
    clips mean nothing without them); a single recording keeps the content (and hash) of 1.21."""
    srcs = [str(s) for s in getattr(state, "sources", None) or []]
    return {"sources": srcs} if srcs else {}


def _part_row(p) -> list:
    """[start, end, speed] – 1.19: plus a dict of the clip's effects when it has any."""
    row = [round(float(p.start), 3), round(float(p.end), 3), float(p.speed)]
    fx = {}
    if getattr(p, "color", None):
        fx["color"] = [float(v) for v in p.color]
    if getattr(p, "zoom", None):
        fx["zoom"] = [[float(v) for v in b] for b in p.zoom]
    if getattr(p, "reverse", False):
        fx["reverse"] = True
    if getattr(p, "hold", 0.0) > 0:
        fx["hold"] = round(float(p.hold), 3)
    if getattr(p, "src", 0):
        fx["src"] = int(p.src)                     # 1.22: a montage clip from another recording
    return row + [fx] if fx else row


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
        text = json.dumps(data, indent=1, ensure_ascii=False)    # 1.34.2 (review W8): before any file is made –
        os.makedirs(os.path.dirname(path), exist_ok=True)         # an unwritable value left a .tmp behind
        fsops.write_atomic(path, text.encode("utf-8"))
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


# ---- 1.18.1: format 2 (Implementierungsplan Fassung 6, chapter 2 and 4.6) – added beside format 1; the editor keeps
# saving format 1 until projectsave is wired in. Nothing below writes a file: projectsave does, through fsops.
VERSION2 = 2
VERSION3 = 3                      # 1.19: clips carry effects (colour, zoom, backwards, stills) – 1.18.1 opens these
VERSION4 = 4                      # 1.20: the short (layout, title, subtitles) – 1.19 opens these read-only
VERSION5 = 5                      # 1.21: the own audio track A2 (music, ducking, fades) – 1.20 opens these read-only
VERSION6 = 6                      # 1.22: montages (clips of several recordings) – 1.21 opens these read-only
CURRENT = VERSION6                # read-only ("aus neuerer Version") instead of saving the effects away
ID_SHOWN = 10                     # hex digits of the project id in the file name
STEM_MAX = 80
QFP_BYTES = 1 << 20               # quick fingerprint: size + first and last MiB (preselection only, never proof)
DURATION_SLACK = 0.05             # s: probe durations of the same file
VIEW_POS_S = 0.5                  # a view counts as changed beyond these (Fassung 6, 3.3)
VIEW_SHARE = 0.01
VIEW_PAD_S = 5.0
_BAD_NAME = set('<>:"/\\|?*') | {chr(c) for c in range(32)}
_HEX = set("0123456789abcdef")


def valid_sha(v) -> bool:
    return isinstance(v, str) and len(v) == 64 and set(v) <= _HEX


def new_id() -> str:
    import uuid
    return uuid.uuid4().hex


def clean_stem(stem: str) -> str:
    out = "".join("_" if c in _BAD_NAME else c for c in str(stem or "")).strip(" .")
    return (out or "Projekt")[:STEM_MAX].rstrip(" .") or "Projekt"


def file_name2(source: str, pid: str) -> str:
    """``<recording>--<id10>.fogscout-project.json`` – two recordings of the same name never share a file."""
    stem = os.path.splitext(os.path.basename(source))[0]
    return f"{clean_stem(stem)}--{str(pid)[:ID_SHOWN]}{EXT}"


def file_name_montage(name: str, pid: str) -> str:
    """1.22: ``<montage name>--<id10>.fogscout-project.json`` in MONTAGE_DIR."""
    return f"{clean_stem(name or 'Montage')}--{str(pid)[:ID_SHOWN]}{EXT}"


def montage_sources(d) -> list:
    """1.22: the recordings of a montage's data (paths; [] for a project of one recording)."""
    raw = d.get("sources") if isinstance(d, dict) else None
    if not isinstance(raw, list):
        return []
    out = [s for s in raw[:MAX_SOURCES] if isinstance(s, str) and s]
    return out if len(out) == len(raw[:MAX_SOURCES]) else []


def content_dict(state: EditState, extra: dict | None = None) -> dict:
    """What a project is about – clips, crop, drawings, fades, censoring, the clip's name and export choices. Not:
    ``rev``, ``view``, ``saved``, ``source`` (they change without the work changing)."""
    d = to_dict(state, "", str((extra or {}).get("name") or ""), extra)
    for k in ("format", "version", "saved", "source"):
        d.pop(k, None)
    return d


def canonical(d: dict) -> bytes:
    return json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def content_hash(content: dict) -> str:
    import hashlib
    return hashlib.sha256(canonical(content)).hexdigest()


def to_dict2(content: dict, pid: str, source: dict, rev: dict, view: dict | None) -> dict:
    """The file's data: the content (``content_dict``) plus id, source identity, revision and view."""
    d = {"format": FORMAT, "version": CURRENT, "id": str(pid), "saved": time.time(), "rev": dict(rev or {}),
         "source": dict(source or {}), "view": dict(view) if view else None}
    d.update(content)
    return d


def view_differs(a, b) -> bool:
    """Fassung 6, 3.3: ``a`` (window) noticeably different from ``b`` (on disk) – a missing ``b`` always is."""
    if not a:
        return False
    if not b:
        return True
    try:
        if abs(float(a["pos"]) - float(b["pos"])) > VIEW_POS_S:
            return True
        span = max(float(b["span"]), 1e-6)
        if abs(float(a["span"]) - float(b["span"])) > VIEW_SHARE * span:
            return True
        return abs(float(a["offset"]) - float(b["offset"])) > VIEW_SHARE * max(span, 1.0)
    except (KeyError, TypeError, ValueError):
        return True


def _finite(v) -> float | None:
    import math
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if math.isfinite(f) else None


def _speed(v) -> float:
    f = _finite(v)
    if f is None:
        return 1.0
    return min(SPEEDS, key=lambda s: abs(s - f))


def validate(d, duration: float, default_parts, durations=None) -> tuple[EditState, dict, dict | None, list] | None:
    """Fassung 6, 4.6: (state, extra, view, notes) from project data of format 1 or 2, field by field – a broken
    field never takes the rest with it and never leaves a reference that points nowhere. Clips outside the recording,
    empty, of unknown tempo or of the wrong type drop out; none left → ``default_parts`` (note "parts"). Drawing
    times are seconds of the recording: clamped, never dropped for lying outside a clip. None only for data that is
    not a project of ours. 1.22: a montage's clips and drawings point at its ``sources`` (``durations`` = the length
    of each, 0 = unknown): each is held to its own recording, one pointing at no recording drops out."""
    if not isinstance(d, dict) or d.get("format") != FORMAT:
        return None
    notes = []
    dur = _finite(duration) or 0.0
    sources = montage_sources(d)
    lengths = [(_finite(x) or 0.0) for x in (durations or [])] if sources else []
    lengths += [0.0] * (len(sources) - len(lengths))
    if sources:
        lengths[0] = lengths[0] or dur

    def src_of(v) -> int | None:
        if not sources:
            return 0 if v in (None, 0) else None
        if v is None:
            return 0
        return v if isinstance(v, int) and not isinstance(v, bool) and 0 <= v < len(sources) else None
    parts = []
    raw_parts = d.get("parts") if isinstance(d.get("parts"), list) else []
    for raw in raw_parts[:MAX_PARTS]:
        if not isinstance(raw, (list, tuple)) or len(raw) < 2:
            continue
        s, e = _finite(raw[0]), _finite(raw[1])
        if s is None or e is None:
            continue
        fx = raw[3] if len(raw) > 3 and isinstance(raw[3], dict) else {}       # 1.19: the clip's effects
        src = src_of(fx.get("src"))
        if src is None:                                # 1.22: a clip of no recording of this montage
            continue
        pdur = lengths[src] if sources else dur
        s, e = max(0.0, s), (min(e, pdur) if pdur > 0 else e)
        hold = _finite(fx.get("hold")) or 0.0
        color = clipedit.clean_color(fx.get("color")) if fx.get("color") is not None else None
        zoom = clipedit.clean_zoom(fx.get("zoom")) if fx.get("zoom") is not None else None
        if hold > 0:                                   # a still: its picture inside the recording
            if pdur > 0:
                s = min(s, max(0.0, pdur - clipedit.HOLD_READ_S))
            hold = min(max(hold, 0.1), clipedit.HOLD_MAX_S)
            parts.append(Part(s, s, 1.0, color=color, zoom=zoom, hold=hold, src=src))
        elif e - s >= 0.1 - 1e-9:
            parts.append(Part(s, e, _speed(raw[2]) if len(raw) > 2 else 1.0, color=color, zoom=zoom,
                              reverse=fx.get("reverse") is True, src=src))
    if not parts:
        parts = [replace(p) for p in default_parts]
        notes.append("parts")
    shapes = []
    for raw in list(d.get("shapes") or [])[:MAX_SHAPES] if isinstance(d.get("shapes"), list) else []:
        s = annotate.from_dict(raw) if isinstance(raw, dict) else None
        if s is None:
            continue
        ssrc = src_of(s.src)
        if ssrc is None:                               # 1.22: drawn on no recording of this montage
            continue
        s.src = ssrc
        sdur = lengths[ssrc] if sources else dur
        t0, t1 = _finite(s.t0) if s.t0 is not None else None, _finite(s.t1) if s.t1 is not None else None
        if t0 is not None:
            t0 = min(max(0.0, t0), sdur) if sdur > 0 else max(0.0, t0)
        if t1 is not None:
            t1 = min(max(0.0, t1), sdur) if sdur > 0 else max(0.0, t1)
        if t0 is not None and t1 is not None and t0 > t1:
            t0 = t1 = None
        s.t0, s.t1 = t0, t1
        shapes.append(s)
    censor = d.get("censor") if isinstance(d.get("censor"), dict) else {}
    boxes = [b for b in (_box(x) for x in list(censor.get("boxes") or [])[:MAX_BOXES]) if b is not None] \
        if isinstance(censor.get("boxes"), list) else []
    style = str(censor.get("style") or "pixel")
    crop = _box(d.get("crop")) if d.get("crop") else None
    total = sum(clipedit.part_seconds(p) for p in parts)
    fades = []
    for key in ("fade_in", "fade_out"):
        f = _finite(d.get(key)) or 0.0
        fades.append(min(max(0.0, f), total / 2))
    from . import musictrack, shorts
    state = EditState(parts, tuple(crop) if crop else None, str(d.get("crop_key") or ("free" if crop else "none")),
                      shapes, fades[0], fades[1], boxes, bool(censor.get("on")),
                      style if style in ("pixel", "blur", "black", "retouch") else "pixel",
                      shorts.from_dict(d.get("short")), musictrack.from_dict(d.get("music")), list(sources))
    extra = dict(d.get("extra")) if isinstance(d.get("extra"), dict) else {}
    extra.setdefault("name", str(d.get("name") or ""))
    view = None
    raw_view = d.get("view") if isinstance(d.get("view"), dict) else None
    if raw_view:
        pos, span, off = (_finite(raw_view.get(k)) for k in ("pos", "span", "offset"))
        if pos is not None and span is not None and off is not None and span > 0 \
                and (dur <= 0 or span <= (max(dur, total) if sources else dur) + VIEW_PAD_S):
            view = {"pos": min(max(0.0, pos), total), "span": span, "offset": max(0.0, off)}
    return state, extra, view, notes


# ---- the catalog: heads of the project files in a folder (Fassung 6, 2.2/2.5)
class Entry:
    """One project file: ``version`` 1 or 2, ``id`` (format 2), ``source`` dict, ``saved``, ``rev``, ``ok`` (readable),
    ``hash`` (full SHA-256 of the file bytes – the basis of later checks)."""

    __slots__ = ("path", "name", "version", "id", "source", "saved", "rev", "ok", "hash", "size", "mtime_ns",
                 "migrated_from")

    def __init__(self, path, data, raw_hash, st):
        self.path, self.name = path, os.path.basename(path)
        self.hash, self.size, self.mtime_ns = raw_hash, st.st_size, st.st_mtime_ns
        ok = isinstance(data, dict) and data.get("format") == FORMAT
        self.ok = ok
        d = data if ok else {}
        self.version = int(d.get("version") or 1) if ok else 0
        self.id = str(d.get("id")) if ok and d.get("id") else None
        self.source = d.get("source") if isinstance(d.get("source"), dict) else {}
        self.saved = _finite(d.get("saved")) or 0.0
        self.rev = d.get("rev") if isinstance(d.get("rev"), dict) else {}
        self.migrated_from = str(self.source.get("migrated_from") or "") or None


_SCAN_CACHE = {}


def read_entry(path: str) -> Entry | None:
    """The head of one project file, cached by mtime and size; None when it cannot be read at all."""
    import hashlib
    try:
        st = os.stat(path)
    except OSError:
        return None
    hit = _SCAN_CACHE.get(path)
    if hit is not None and hit[0] == (st.st_mtime_ns, st.st_size):
        return hit[1]
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError:
        return None
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        data = None
    entry = Entry(path, data, hashlib.sha256(raw).hexdigest(), st)
    _SCAN_CACHE[path] = ((st.st_mtime_ns, st.st_size), entry)
    return entry


def scan(folder: str) -> list:
    """Every project file directly in ``folder`` (``Sicherungen`` and hidden temp names are not projects)."""
    try:
        names = sorted(os.listdir(folder))
    except OSError:
        return []
    out = []
    for name in names:
        if name.startswith(".") or not name.endswith(EXT):
            continue
        e = read_entry(os.path.join(folder, name))
        if e is not None:
            out.append(e)
    return out


class Resolution:
    """What ``resolve`` found: ``kind`` one of auto / ambiguous_recording / ambiguous_id / verify / mismatch /
    unverified / legacy / changed / none, and the ``entries`` it is about."""

    __slots__ = ("kind", "entries")

    def __init__(self, kind, entries=()):
        self.kind, self.entries = kind, list(entries)

    def __repr__(self):
        return f"Resolution({self.kind!r}, {[e.name for e in self.entries]})"


def _same_size(e, rec) -> bool:
    try:
        return int(e.source.get("size") or -1) == int(rec["size"])
    except (TypeError, ValueError):
        return False


def _same_duration(e, rec) -> bool:
    a, b = _finite(e.source.get("duration")), _finite(rec.get("duration"))
    return a is None or b is None or a <= 0 or b <= 0 or abs(a - b) <= DURATION_SLACK


def resolve(rec: dict, entries: list) -> Resolution:
    """Fassung 6, 2.5: which project belongs to the recording ``rec`` (``size``, ``qfp``, ``sha256`` – None while
    the full hash is not known yet –, ``duration``, ``file``, ``t``). Automatic ("auto") only when exactly one
    format-2 project carries the recording's full SHA-256 and size and no other file shares its id; everything else
    is for the user to decide."""
    v2 = [e for e in entries if e.ok and e.version >= VERSION2 and e.id]
    by_id = {}
    for e in v2:
        by_id.setdefault(e.id, []).append(e)

    def with_twins(found):
        ids = {e.id for e in found}
        twins = [x for i in ids for x in by_id.get(i, ()) if len(by_id[i]) > 1]
        return twins

    sha = rec.get("sha256") if valid_sha(rec.get("sha256")) else None
    if sha:
        hit = [e for e in v2 if e.source.get("sha256") == sha and _same_size(e, rec) and _same_duration(e, rec)]
        if hit:
            twins = with_twins(hit)
            if twins:
                return Resolution("ambiguous_id", sorted(twins, key=lambda e: e.name))
            if len(hit) > 1:
                return Resolution("ambiguous_recording", sorted(hit, key=lambda e: e.name))
            return Resolution("auto", hit)
    near = [e for e in v2 if e.source.get("qfp") == rec.get("qfp") and rec.get("qfp") and _same_size(e, rec)]
    if near:
        twins = with_twins(near)
        if twins:
            return Resolution("ambiguous_id", sorted(twins, key=lambda e: e.name))
        if not sha:
            return Resolution("verify", near)
        unverified = [e for e in near if not valid_sha(e.source.get("sha256"))]
        if unverified:
            return Resolution("unverified", unverified)
        return Resolution("mismatch", near)
    stem = os.path.splitext(str(rec.get("file") or ""))[0]
    migrated = {e.migrated_from for e in v2 if e.migrated_from}
    for e in entries:
        if e.ok and e.version < VERSION2 and e.name == stem + EXT and e.name not in migrated \
                and e.source.get("file") == rec.get("file") and _same_size(e, rec) and int(rec.get("size") or 0) > 0:
            return Resolution("legacy", [e])
    changed = [e for e in entries if e.ok and (
        (e.source.get("file") and e.source.get("file") == rec.get("file"))
        or (rec.get("t") and e.source.get("t") == rec.get("t")))]
    if changed:
        return Resolution("changed", changed)
    return Resolution("none")
