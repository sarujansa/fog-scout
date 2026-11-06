"""1.38.29 (project review F4): a local corpus of the banners the detection decided on, so the detection can be
checked against real pictures – before, the repository held two banner pictures for 45 maps in nine languages, and
a change to a threshold was a guess.

Each decision ("detected") stores the part of the captured banner strip that ``detector.locate_text`` reads (the
separator line with the name above and the realm below, a margin around it – not the whole strip), as JPEG, plus a
JSON side file with everything needed to read it again: frame size, position in the strip, separator, letterbox
bars, the map decided on and the text read. ``check`` puts each crop back onto a black strip of the original size
and runs the full reader (separator search, OCR, lexicon) – a hit when it decides on the stored map.

Everything stays in the data folder (``corpus/``, newest ``KEEP`` decisions); nothing is sent anywhere. A crop can
show the left edge of DBD's HUD beside the banner (the survivor list with player names sits there) – PRIVACY.md
says so, and the export is a click of the user. Files are written new and deleted only through fsops.
"""
from __future__ import annotations

import json
import os
import time
import zipfile
from dataclasses import dataclass, field

import cv2
import numpy as np

from . import fsops

DIR = "corpus"
KEEP = 300                      # newest decisions kept (≈ 300 × 150 KB)
FORMAT = "fogscout-corpus"
JPEG_QUALITY = 90
MAX_ROI = 8192                  # 1.38.57 (security review): largest strip side check() puts a crop back onto
# margin around the separator as fractions of its length – a little more than locate_text reads
# (0.60 L to the left of a short line, 0.30 L above, 0.03 L to the right, 0.11 L below)
MARGIN = (0.65, 0.34, 0.08, 0.20)


@dataclass
class Entry:
    stamp: str
    picture: str                # path of the JPEG
    meta: dict


@dataclass
class Report:
    total: int = 0
    hits: int = 0
    misses: list = field(default_factory=list)      # (stamp, expected map id, got map id or None, text read, fit)
    broken: int = 0                                 # entries that could not be read back
    seconds: float = 0.0


def folder(data_dir: str) -> str:
    return os.path.join(data_dir, DIR)


def crop_box(shape, sep) -> tuple:
    """(x0, y0, x1, y1) of the part of a strip of ``shape`` that is kept around separator ``sep``."""
    h, w = shape[:2]
    L = max(1, sep.x1 - sep.x0)
    left, above, right, below = MARGIN
    x0, x1 = max(0, int(sep.x0 - left * L)), min(w, int(sep.x1 + right * L))
    y0, y1 = max(0, int(sep.y - above * L)), min(h, int(sep.y + below * L))
    return x0, y0, max(x0 + 1, x1), max(y0 + 1, y1)


def save(data_dir: str, img: np.ndarray, sep, res, decision, frame: tuple, letterboxed: bool, bars,
         languages, version: str, now: float | None = None) -> str | None:
    """Store one decision; returns its stamp, None when nothing could be written (never raises for the worker's
    sake beyond what the caller catches)."""
    now = time.time() if now is None else now
    dst = folder(data_dir)
    os.makedirs(dst, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(now)) + f"-{int(now * 1000) % 1000:03d}"
    x0, y0, x1, y1 = crop_box(img.shape, sep)
    ok, buf = cv2.imencode(".jpg", np.ascontiguousarray(img[y0:y1, x0:x1]), [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
    if not ok:
        return None
    meta = {"format": FORMAT, "version": 1, "program": str(version), "t": round(float(now), 3),
            "map_id": str(decision.map_id), "variant": int(decision.variant),
            "probability": round(float(decision.probability), 3),
            "name_text": str(getattr(res, "name_text", "")), "realm_text": str(getattr(res, "realm_text", "")),
            "name_fit": round(float(getattr(res, "name_fit", 0.0)), 2),
            "frame": [int(frame[0]), int(frame[1])], "roi": [int(img.shape[1]), int(img.shape[0])],
            "offset": [int(x0), int(y0)],
            "separator": {"x0": int(sep.x0), "x1": int(sep.x1), "y": int(sep.y), "frac": round(float(sep.frac), 4),
                          "thickness": round(float(sep.thickness), 2)},
            "letterboxed": bool(letterboxed), "bars": [int(bars[0]), int(bars[1])] if bars else None,
            "languages": [str(x) for x in (languages or [])]}
    fsops.write_new(os.path.join(dst, stamp + ".jpg"), buf.tobytes())
    fsops.write_new(os.path.join(dst, stamp + ".json"), json.dumps(meta, ensure_ascii=False, indent=0).encode("utf-8"))
    prune(dst)
    return stamp


def _stamps(dst: str) -> list:
    try:
        names = os.listdir(dst)
    except OSError:
        return []
    return sorted({n[:-5] for n in names if n.endswith(".json") and len(n) == 24})


def prune(dst: str, keep: int | None = None) -> int:
    """Delete the oldest decisions beyond ``keep`` (KEEP; our own pairs only, through fsops.delete_inside); the number."""
    keep = KEEP if keep is None else keep
    gone = 0
    for stamp in _stamps(dst)[:-keep] if keep > 0 else []:
        for ext in (".jpg", ".json"):
            try:
                fsops.delete_inside(dst, os.path.join(dst, stamp + ext))
                gone += 1
            except OSError:
                pass
    return gone


def entries(data_dir: str) -> list:
    """The stored decisions, oldest first; a side file that is not ours or unreadable is skipped."""
    dst = folder(data_dir)
    out = []
    for stamp in _stamps(dst):
        try:
            with open(os.path.join(dst, stamp + ".json"), encoding="utf-8") as fh:
                meta = json.load(fh)
        except (OSError, ValueError):
            continue
        if not isinstance(meta, dict) or meta.get("format") != FORMAT:
            continue
        pic = os.path.join(dst, stamp + ".jpg")
        if os.path.isfile(pic):
            out.append(Entry(stamp, pic, meta))
    return out


def count(data_dir: str) -> int:
    return len(_stamps(folder(data_dir)))


def check(data_dir: str, reader, stop=None) -> Report:
    """Read every stored decision again with ``reader`` (detector.BannerReader) – the crop back on a black strip of
    the original size, then the full pipeline – and count hits (same map id). ``stop()`` True ends early."""
    rep = Report()
    t0 = time.perf_counter()
    for e in entries(data_dir):
        if stop is not None and stop():
            break
        rep.total += 1
        m = e.meta
        try:
            crop = cv2.imdecode(np.fromfile(e.picture, dtype=np.uint8), cv2.IMREAD_COLOR)
            W, H = int(m["roi"][0]), int(m["roi"][1])
            x0, y0 = int(m["offset"][0]), int(m["offset"][1])
            # 1.38.57 (security review): the side file is user-writable – a huge "roi" allocated gigabytes
            if not (0 < W <= MAX_ROI and 0 < H <= MAX_ROI and 0 <= x0 < W and 0 <= y0 < H):
                raise ValueError("roi out of range")
            canvas = np.zeros((H, W, 3), np.uint8)
            h, w = crop.shape[:2]
            canvas[y0:y0 + h, x0:x0 + w] = crop[:H - y0, :W - x0]
            bars = m.get("bars")
            sep, res = reader.read(canvas, int(m["frame"][0]), int(m["frame"][1]),
                                   letterboxed=bool(m.get("letterboxed")), bars=tuple(bars) if bars else None)
        except Exception:
            rep.broken += 1
            continue
        got = res.best[0] if res is not None and res.best else None
        if got == m.get("map_id"):
            rep.hits += 1
        else:
            rep.misses.append((e.stamp, str(m.get("map_id")), got, getattr(res, "name_text", ""),
                               float(getattr(res, "name_fit", 0.0)) if res is not None else None))
    rep.seconds = time.perf_counter() - t0
    return rep


def export_zip(data_dir: str, dest: str) -> int:
    """All stored decisions into the ZIP ``dest`` (the user's chosen file); the number of files written."""
    n = 0
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for e in entries(data_dir):
            z.write(e.picture, os.path.basename(e.picture))
            z.write(os.path.join(folder(data_dir), e.stamp + ".json"), e.stamp + ".json")
            n += 2
    return n
