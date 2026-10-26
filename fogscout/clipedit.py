"""Clip editor, the ffmpeg side (1.5.1, user's wish: "direkt im Programm bearbeiten wie in Medal"). Pure
functions and small threads around the ffmpeg binary of imageio-ffmpeg (``obsrec.ffmpeg_exe``) – no Qt here,
so it is testable without a window. Nothing touches the game; only the recording files the user chose.

Qt Multimedia was tried and works, but lives in PySide6-Addons (175 MB, with Qt WebEngine/Chromium inside) –
not worth it for a preview: ffmpeg decodes single frames in ~40 ms (scrubbing) and streams scaled frames for
playback; the sound of the clip is played by Windows (winsound) from a temporary WAV of the same stretch.
"""
from __future__ import annotations

import copy
import math
import os
import re
import subprocess
import tempfile
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field, replace

from .i18n import _
from .obsrec import (AUDIO_STREAM_RE, CLIPS_DIR as _CLIPS_DIR, NAME_CHARS, PART_EXT, PARTS_WRITING, audio_graph,
                     ffmpeg_exe, part_key)

PREVIEW_H = 540                  # px: frames for the preview picture
THUMB_H = 54                     # px: pictures of the timeline strip
THUMBS = 24                      # pictures along the strip
THUMB_WORKERS = 4                # 1.8.3: key-frame seeks for the strip running at once
THUMB_SRC_H = 108                # 1.12.6: pictures of the strip fetched this tall – they show the game part only
CONTENT_DARK = 24                # 1.12.6, black borders of a recording: brightest colour at most this (H.264 black ≈ 0–16)
CONTENT_SHARE = 0.01             # a row/column holds picture from 1 % of its pixels on
CONTENT_MARGIN = 0.03            # a border from 3 % of the width/height on (less: compression noise, nothing to gain)
CONTENT_SKEW = 0.02              # both borders of an axis alike within 2 % – a centred picture
CONTENT_FRAMES = 6               # pictures with anything in them before borders are trusted
CONTENT_MIN = 0.3                # a game part smaller than this share of the recording is no border case
CONTENT_SLACK = 0.02             # refine_box: how far a side may move on the sharper picture
FPS_CAP = 30.0                   # playback: at most this many frames a second (preview, not the file)
SIZE_RE = re.compile(rb"Video: .*?, (\d{2,5})x(\d{2,5})")
FPS_RE = re.compile(rb"(\d+(?:\.\d+)?) fps")
DURATION_RE = re.compile(rb"Duration: (\d+):(\d\d):(\d\d(?:\.\d+)?)")
CLIPS_DIR = _CLIPS_DIR         # one place for the folder name (obsrec)
CENSOR_STYLES = ("pixel", "blur", "black", "retouch")   # 1.7.2: how a censored area looks; 1.7.3 retouch = delogo
EDGE_PX = 2                                # delogo refuses a box that touches the frame edge: keep this far away
NAMES_BOX = (0.004, 0.50, 0.26, 0.32)      # DBD's survivor list bottom left (portraits + names + status text), as
                                           # fractions of the 16:9 game picture – 1.7.4 after the user's screenshot:
                                           # the list sits higher (≈ 50–82 % of the height) and long names reach further
MODES = ("copy", "exact", "discord", "gif")   # key frames, no re-encoding / frame exact / 1.6.1: fits a size
                                              # (Discord) / 1.12: an animated GIF (no sound)
TARGETS_MB = (10, 25, 50, 500)  # 1.6.1: Discord's upload limits (free 10 MB, Nitro Basic 50, Nitro 500)
DEFAULT_TARGET_MB = 10
AUDIO_KBPS = 96                 # sound of a size-fitted clip
SIZE_MARGIN = 0.90              # aim this far below the limit (container overhead, rate control)
MUXERS = {".mp4": "mp4", ".mkv": "matroska", ".mov": "mov", ".webm": "webm", ".flv": "flv", ".gif": "gif"}
PUBLISH_TRIES = 5               # renaming the finished clip: a virus scanner may hold a new file for a moment (Windows)
NO_COPY_EXTS = (".gif",)        # pictures that cannot be stream-copied into an mp4 clip (the editor's own GIFs)


@dataclass
class Info:
    duration: float = 0.0
    width: int = 0
    height: int = 0
    fps: float = 30.0
    audio_tracks: int = 0           # 1.8.5: OBS writes track 2 (without Discord) when set up for it

    @property
    def ok(self) -> bool:
        return self.duration > 0 and self.width > 0 and self.height > 0


def _flags() -> int:
    return getattr(subprocess, "CREATE_NO_WINDOW", 0)


PROBE_KEPT = 16                     # 1.12.3: probe results kept (preview, then the big editor of the same file)
_PROBED = OrderedDict()             # (path, size, mtime_ns) -> Info
_PROBED_LOCK = threading.Lock()


def probe(path: str, ffmpeg: str | None = None) -> Info:
    """Length, picture size and frame rate from ``ffmpeg -i`` (imageio-ffmpeg ships no ffprobe). 1.12.3: the result of
    an unchanged file (same size and time) is kept – a copy each call, so a caller may change it."""
    ffmpeg = ffmpeg or ffmpeg_exe()
    if not ffmpeg:
        return Info()
    try:
        st = os.stat(path)
        key = (os.path.abspath(path), st.st_size, st.st_mtime_ns)
    except OSError:
        key = None
    with _PROBED_LOCK:
        if key in _PROBED:
            _PROBED.move_to_end(key)
            return replace(_PROBED[key])
    info = _probe(path, ffmpeg)
    if key is not None and info.ok:
        with _PROBED_LOCK:
            _PROBED[key] = replace(info)
            while len(_PROBED) > PROBE_KEPT:
                _PROBED.popitem(last=False)
    return info


def _probe(path: str, ffmpeg: str) -> Info:
    try:
        p = subprocess.run([ffmpeg, "-hide_banner", "-i", path], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                           stderr=subprocess.PIPE, timeout=30, creationflags=_flags())
    except (OSError, subprocess.TimeoutExpired):
        return Info()
    err = p.stderr or b""
    info = Info()
    m = DURATION_RE.search(err)
    if m:
        info.duration = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    m = SIZE_RE.search(err)
    if m:
        info.width, info.height = int(m.group(1)), int(m.group(2))
    info.audio_tracks = len(AUDIO_STREAM_RE.findall(err))
    m = FPS_RE.search(err)
    if m:
        info.fps = float(m.group(1)) or 30.0
    return info


def scaled(info: Info, height: int) -> tuple[int, int]:
    """Preview size: ``height`` tall, width even (ffmpeg's scale=-2)."""
    if not info.ok:
        return 16 * height // 9 // 2 * 2, height
    h = min(height, info.height)
    return max(2, round(info.width * h / info.height / 2) * 2), h


SILENT_DB = -60.0                # 1.8.18: a track whose loudest moment stays below this held nothing (silence ≈ -91)
LEVEL_RE = re.compile(rb"\[volumedetect@t(\d+) @ [^\]]*\] max_volume: (-?[\d.]+|-inf) dB")


def track_levels(path: str, n_tracks: int, ffmpeg: str | None = None, timeout: float = 180) -> dict:
    """1.8.18 (user: Discord never heard in the clips): the loudest moment of each audio track in dB {index:
    dB}, from one ffmpeg run over the sound only (seconds even for a long round) – which source OBS really
    recorded. {} without ffmpeg, with fewer than two tracks or on failure."""
    ffmpeg = ffmpeg or ffmpeg_exe()
    if not ffmpeg or n_tracks < 2:
        return {}
    graph = ";".join(f"[0:a:{i}]volumedetect@t{i}" for i in range(n_tracks))
    try:
        p = subprocess.run([ffmpeg, "-hide_banner", "-nostats", "-i", path, "-vn", "-filter_complex", graph,
                            "-f", "null", "-"], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                           stderr=subprocess.PIPE, timeout=timeout, creationflags=_flags())
    except (OSError, subprocess.TimeoutExpired):
        return {}
    return {int(i): float(db) for i, db in LEVEL_RE.findall(p.stderr or b"")}


def frame_at(path: str, t: float, height: int = PREVIEW_H, info: Info | None = None, ffmpeg: str | None = None,
             keyframe: bool = False):
    """One picture at second ``t`` as PIL image (RGB), or None. Seeks to the key frame before ``t`` and decodes
    up to it – about 40 ms for 1080p, more for 1440p and up to a key-frame interval of decoding (OBS: 2–4 s of
    frames, measured 70–190 ms at 1080p60). ``keyframe`` (1.8.3): only the key frame at or before ``t``, no decoding
    up to ``t`` – ~40 ms whatever the interval, the picture up to one interval early (strip, first look). Needs
    ``-fps_mode passthrough``: that frame carries a negative output timestamp, and the constant-rate default
    drops it unless a later frame follows – near the end of a file none does (measured: nothing came back)."""
    from PIL import Image
    ffmpeg = ffmpeg or ffmpeg_exe()
    info = info or probe(path, ffmpeg)
    if not ffmpeg or not info.ok:
        return None
    w, h = scaled(info, height)
    quick = ["-noaccurate_seek", "-skip_frame", "nokey"] if keyframe else []
    out = ["-an", "-fps_mode", "passthrough"] if keyframe else []
    try:
        p = subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", *quick, "-ss", f"{max(0.0, t):.3f}", "-i", path,
                            *out, "-frames:v", "1", "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=30,
                           creationflags=_flags())
    except (OSError, subprocess.TimeoutExpired):
        return None
    need = w * h * 3
    if len(p.stdout) < need:
        return None
    return Image.frombytes("RGB", (w, h), p.stdout[:need])


def thumb_strip(path: str, times: list, height: int = THUMB_H, info: Info | None = None, ffmpeg: str | None = None,
                stop=lambda: False, workers: int = THUMB_WORKERS):
    """The pictures of the strip for ``times``, yielded as (index, image) in the order they finish. 1.8.3 (user:
    "das Laden optimieren"): ``workers`` key-frame seeks at once (frame_at(keyframe=True)) – the strip takes
    ~0.4 s whatever the length of the recording (measured 1080p60, 4 cores). 1.7.1 streamed it from one
    key-frame-only run over the whole file, which grew with its length (6 min: 1.7 s, 15 min: ~4.5 s). A picture
    may show the key frame up to one key-frame interval earlier (OBS: ~2–4 s), fine for a strip. ``stop()`` True
    ends it; a picture ffmpeg could not give is left out (the caller fetches it the exact way)."""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    ffmpeg = ffmpeg or ffmpeg_exe()
    info = info or probe(path, ffmpeg)
    if not ffmpeg or not info.ok or len(times) < 2 or stop():
        return
    with ThreadPoolExecutor(max(1, int(workers)), thread_name_prefix="clip-thumb") as ex:
        jobs = {ex.submit(frame_at, path, t, height, info, ffmpeg, True): i for i, t in enumerate(times)}
        for fut in as_completed(jobs):
            if stop():
                for other in jobs:
                    other.cancel()
                return
            img = fut.result()
            if img is not None:
                yield jobs[fut], img


def thumb_times(duration: float, n: int = THUMBS) -> list[float]:
    """Moments for the strip: the middle of n equal stretches."""
    n = max(1, n)
    return [duration * (i + 0.5) / n for i in range(n)]


def _lit(img, dark: int, share: float):
    """Rows and columns of ``img`` that hold picture: at least ``share`` of their pixels brighter than ``dark`` in
    any colour (a saturated red is dim as grey). numpy bool arrays, or None for a picture that is black all over."""
    import numpy as np
    a = np.asarray(img.convert("RGB")).max(axis=2) > dark
    if not a.any():
        return None
    return a.mean(axis=1) >= share, a.mean(axis=0) >= share


def _sides(lit) -> tuple:
    """(before, after) of the first and last True as fractions of the length: the empty share at each end."""
    import numpy as np
    on = np.flatnonzero(lit)
    return on[0] / len(lit), 1.0 - (on[-1] + 1) / len(lit)


def content_box(images, dark: int = CONTENT_DARK, share: float = CONTENT_SHARE, margin: float = CONTENT_MARGIN,
                skew: float = CONTENT_SKEW, frames: int = CONTENT_FRAMES):
    """1.12.6 (user's screenshot: the round small in a big black box, the strip in slivers): the part of the
    recording that holds the game when it has black borders, as fractions (x, y, w, h) – None without borders.
    From the strip's pictures together: a row or column belongs to the game when it holds picture in any of
    them (a dark corner of one moment is lit in another). Borders count only in pairs: both sides of an axis at
    least ``margin`` and alike within ``skew`` – a source centred in a bigger canvas (or DBD's 16:9 in a 21:9
    window) has even bars, a dark ceiling over a whole round would be one side only. Needs ``frames`` pictures
    with anything in them; pictures of another size are left out. Pure."""
    rows = cols = None
    seen = 0
    shape = None
    for img in images:
        if img is None:
            continue
        if shape is None:
            shape = img.size
        elif img.size != shape:
            continue
        lit = _lit(img, dark, share)
        if lit is None:
            continue
        seen += 1
        rows = lit[0] if rows is None else rows | lit[0]
        cols = lit[1] if cols is None else cols | lit[1]
    if seen < frames or rows is None or not rows.any() or not cols.any():
        return None

    def pair(a, b):
        return (a, b) if min(a, b) >= margin and abs(a - b) <= skew else (0.0, 0.0)

    top, bottom = pair(*_sides(rows))
    left, right = pair(*_sides(cols))
    w, h = 1.0 - left - right, 1.0 - top - bottom
    if not (left or top) or w < CONTENT_MIN or h < CONTENT_MIN:
        return None
    return left, top, w, h


def refine_box(box, img, dark: int = CONTENT_DARK, share: float = CONTENT_SHARE, slack: float = CONTENT_SLACK):
    """``box`` from content_box (small pictures: one of their pixels is ~13 px of a 1440p round) moved to the
    edges of one sharper picture ``img``: each side with a border goes to the first row/column of picture within
    ``slack`` of it, one more inwards – the outermost is blended with the black and would stay a thin dark line
    in the clip. A side without picture near it in this frame (dark there right now) stays where it was. Pure."""
    if not box or img is None:
        return box
    lit = _lit(img, dark, share)
    if lit is None:
        return box
    x, y, w, h = box
    edges = []
    for start, size, line in ((x, w, lit[1]), (y, h, lit[0])):
        n = len(line)
        if start <= 0:
            edges.append((start, size))
            continue
        near = int(slack * n) + 1
        lo, hi = int(start * n), int((start + size) * n)
        first = [i for i in range(max(0, lo - near), min(n, lo + near + 1)) if line[i]]
        last = [i for i in range(max(0, hi - near - 1), min(n, hi + near)) if line[i]]
        a = (first[0] + 1) / n if first else start
        b = last[-1] / n if last else start + size
        edges.append((a, b - a) if b - a >= CONTENT_MIN else (start, size))
    return edges[0][0], edges[1][0], edges[0][1], edges[1][1]


def fmt_pos(seconds: float) -> str:
    """m:ss.t for the editor (tenths matter when cutting)."""
    s = max(0.0, float(seconds))
    m, s = int(s // 60), s % 60
    return f"{m}:{s:04.1f}"


def clip_name(round_name: str, start: float, end: float) -> str:
    """'2026-10-17 21-40 Coal Tower – Nurse – Clip 3m12s-3m40s' (file name without extension)."""
    base = os.path.splitext(re.split(r"[\\/]", round_name)[-1])[0]        # a Windows path on any system

    def tag(t):
        return f"{int(t // 60)}m{int(t % 60):02d}s"
    return NAME_CHARS.sub("", f"{base} – Clip {tag(start)}-{tag(end)}")[:150]


def unique_path(folder: str, name: str, ext: str) -> str:
    out = os.path.join(folder, name + ext)
    n = 2
    while os.path.exists(out) or os.path.exists(out + PART_EXT):       # … nor one another save is writing
        out = os.path.join(folder, f"{name} ({n}){ext}")
        n += 1
    return out


def copyable(path: str) -> bool:
    """False for a source whose picture cannot be stream-copied into a clip (an animated GIF): "copy" re-encodes it
    like "exact" – the mp4 muxer has no tag for the gif codec, every save failed."""
    return os.path.splitext(path)[1].lower() not in NO_COPY_EXTS


def _writing(out: str) -> tuple[str, list]:
    """(file ffmpeg writes, its ``-f`` arguments): ``out`` + PART_EXT in ``out``'s format, renamed by _publish once
    ffmpeg succeeded; ``out`` itself for an extension without a known muxer."""
    fmt = MUXERS.get(os.path.splitext(out)[1].lower())
    return (out + PART_EXT, ["-f", fmt]) if fmt else (out, [])


def _remove(path: str):
    try:
        os.remove(path)
    except OSError:
        pass


def _publish(tmp: str, out: str) -> tuple[bool, str]:
    """The finished file gets its real name (only now does the clips list see it) – tried again for a moment
    before the encode is given up."""
    for attempt in range(PUBLISH_TRIES if tmp != out else 0):
        try:
            os.replace(tmp, out)
            break
        except OSError as e:
            if attempt == PUBLISH_TRIES - 1:
                _remove(tmp)
                return False, str(e)
            time.sleep(0.2 * (attempt + 1))
    return True, ""


def cut(path: str, start: float, end: float, out: str, mode: str = "copy", ffmpeg: str | None = None,
        run=None, target_mb: float = DEFAULT_TARGET_MB, info: Info | None = None,
        retry: bool = True, censor=None, censor_style: str = "pixel", mix=None) -> tuple[bool, str]:
    """Write the stretch ``start``..``end`` of ``path`` to ``out``. "copy" = stream copy (seconds of work; the
    cut lands on the key frame before ``start``, so the clip may begin up to a few seconds early), "exact" =
    frame exact, picture re-encoded (x264 veryfast, CRF 18; a 30-s clip takes some seconds), sound as AAC;
    "discord" (1.6.1) = re-encoded to stay under ``target_mb`` (discord_plan picks rate, size, frame rate).
    ``censor`` (1.7.2): boxes to hide (fractions of the picture, see censor_graph) – needs the picture re-encoded,
    so "copy" becomes "exact" (as for a source that cannot be copied, see copyable). ``mix`` (1.8.6): {source:
    volume} over the recording's own audio tracks (obsrec.audio_graph) – one track as it is stays a stream copy,
    anything else re-encodes the sound (AAC), the picture stays as the mode says. ffmpeg writes ``out`` + PART_EXT,
    renamed to ``out`` once it succeeded. Returns (ok, ffmpeg's last words on failure)."""
    ffmpeg = ffmpeg or ffmpeg_exe()
    if not ffmpeg:
        return False, "ffmpeg fehlt"
    censor = list(censor or ())
    if mode == "copy" and (censor or not copyable(path)):
        mode = "exact"
    start, end = max(0.0, float(start)), float(end)
    if end <= start:
        return False, "Ende vor Anfang"
    if (censor or mix) and (info is None or not info.ok):
        info = probe(path, ffmpeg)
    flt, amap = audio_graph(info.audio_tracks if info else 0, mix)
    try:
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    except OSError as e:                                        # the drive is gone: an answer, not a dead thread
        return False, str(e)
    args = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", path]
    vf = ""
    if mode == "discord":
        kbps, h, fps = discord_plan(end - start, target_mb, info)
        vf = f"scale=-2:{h},fps={fps:g}"
        args += ["-c:v", "libx264", "-preset", "veryfast", "-b:v", f"{kbps}k",
                 "-maxrate", f"{int(kbps * 1.1)}k", "-bufsize", f"{kbps * 2}k", "-pix_fmt", "yuv420p",
                 "-c:a", "aac", "-b:a", f"{AUDIO_KBPS}k"]
    elif mode == "exact":
        args += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac",
                 "-b:a", "160k"]
    elif flt:                                                   # mixed sound: picture copied, sound re-encoded
        args += ["-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-avoid_negative_ts", "make_zero"]
    else:
        args += ["-c", "copy", "-avoid_negative_ts", "make_zero"]
    graphs, vmap = [], "0:v:0"
    if censor:
        graphs.append(censor_graph(censor, censor_style, info.width, info.height, vf))
        vmap = "[vout]"
    elif vf:
        args += ["-vf", vf]
    if flt:
        graphs.append(flt)
    if graphs:
        args += ["-filter_complex", ";".join(graphs)]
    if censor or flt or amap != "0:a?":
        args += ["-map", vmap] + (["-an"] if amap is None else ["-map", amap])
    tmp, fmt = _writing(out)
    args += (["-movflags", "+faststart"] if out.lower().endswith(".mp4") else []) + fmt + [tmp]
    if run is None:
        def run(a):
            p = subprocess.run(a, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                               timeout=1800, creationflags=_flags())
            return p.returncode, p.stderr or b""
    key = part_key(tmp)
    PARTS_WRITING.add(key)                                      # obsrec.settle_parts leaves it alone meanwhile
    try:
        rc, err = run(args)
    except (OSError, subprocess.TimeoutExpired) as e:
        rc, err = 1, str(e).encode()
    finally:
        PARTS_WRITING.discard(key)
    ok = rc == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 0
    if not ok:
        _remove(tmp)
        return False, err[-300:].decode("utf-8", "replace").strip()
    if mode == "discord" and retry and os.path.getsize(tmp) > target_mb * 1024 * 1024:
        # the rate control overshot (very busy pictures): once more with less, never a file over the limit
        _remove(tmp)
        return cut(path, start, end, out, mode, ffmpeg, run, target_mb * 0.8, info, retry=False, censor=censor,
                   censor_style=censor_style, mix=mix)
    return _publish(tmp, out)


def names_box(width: int, height: int) -> tuple:
    """1.7.2: where DBD draws the survivor names (bottom left of the game picture) as a box (x, y, w, h) in
    fractions of a frame ``width`` × ``height`` – the game picture is 16:9 centred in a wider frame (ultrawide
    recordings of the whole screen carry the black bars)."""
    if width <= 0 or height <= 0:
        return NAMES_BOX
    gw = min(width, height * 16 / 9)
    off = (width - gw) / 2 / width
    x, y, w, h = NAMES_BOX
    return (off + x * gw / width, y, w * gw / width, h)


def box_px(box, width: int, height: int) -> tuple:
    """A fraction box -> whole, even pixel values (x, y, w, h) inside the frame (ffmpeg wants even sizes)."""
    x, y, w, h = box
    x0 = min(max(0, int(x * width)), width - 2) // 2 * 2
    y0 = min(max(0, int(y * height)), height - 2) // 2 * 2
    x1 = min(width, int((x + w) * width + 1)) // 2 * 2
    y1 = min(height, int((y + h) * height + 1)) // 2 * 2
    return x0, y0, max(2, x1 - x0), max(2, y1 - y0)


def censor_graph(boxes, style: str, width: int, height: int, tail: str = "", src: str = "[0:v]",
                 out: str = "[vout]", tag: str = "") -> str:
    """1.7.2 (user: censor the names on the left): the ffmpeg filter graph that hides ``boxes`` (fraction
    boxes) in a ``width`` × ``height`` picture – "pixel" = coarse blocks, "blur" = blurred, "black" = a black
    box, "retouch" = ffmpeg's delogo (the area is interpolated from its surroundings, no visible box); ``tail`` =
    filters to run after it (scale/fps of the Discord mode). From ``src`` (default [0:v]) to ``out`` (default
    [vout]); ``tag`` = a suffix for the labels inside (one graph per part of an edit)."""
    parts, cur = [], src
    for i, box in enumerate(boxes):
        x, y, w, h = box_px(box, width, height)
        nxt = f"[c{i}{tag}]"
        if style == "black":
            parts.append(f"{cur}drawbox=x={x}:y={y}:w={w}:h={h}:color=black:t=fill{nxt}")
        elif style == "retouch":            # 1.7.3 (user: "retouchieren"): painted over from the surroundings
            x, y = max(EDGE_PX, x), max(EDGE_PX, y)
            w, h = max(2, min(w, width - EDGE_PX - x)), max(2, min(h, height - EDGE_PX - y))
            parts.append(f"{cur}delogo=x={x}:y={y}:w={w}:h={h}{nxt}")
        else:
            if style == "blur":
                r = max(2, min(w, h) // 6)
                inner = f"boxblur=luma_radius={r}:luma_power=3:chroma_radius={max(1, r // 2)}:chroma_power=3"
            else:
                p = max(4, min(w, h) // 8)
                inner = f"scale={max(1, w // p)}:{max(1, h // p)}:flags=area,scale={w}:{h}:flags=neighbor"
            a, b, pix = f"[a{i}{tag}]", f"[b{i}{tag}]", f"[p{i}{tag}]"
            parts.append(f"{cur}split{a}{b};{b}crop={w}:{h}:{x}:{y},{inner}{pix};{a}{pix}overlay={x}:{y}{nxt}")
        cur = nxt
    parts.append(f"{cur}{tail or 'null'}{out}")
    return ";".join(parts)


def discord_plan(seconds: float, target_mb: float, info: Info | None = None) -> tuple[int, int, float]:
    """1.6.1: (video kbit/s, picture height, frame rate) so a clip of ``seconds`` stays under ``target_mb`` MB.
    Less room → smaller picture and 30 fps instead of a blurred 1440p (rules of thumb for x264: 1080p60 needs
    ~6000 kbit/s, 1080p30 ~4000, 720p30 ~2000, 480p30 ~900)."""
    seconds = max(1.0, float(seconds))
    total = target_mb * 8 * 1024 * SIZE_MARGIN / seconds          # kbit/s for picture + sound
    video = max(150, int(total - AUDIO_KBPS))
    src_h = info.height if info and info.height else 1080
    src_fps = info.fps if info and info.fps else 30.0
    if video >= 6000:
        h, fps = 1080, 60.0
    elif video >= 4000:
        h, fps = 1080, 30.0
    elif video >= 2000:
        h, fps = 720, 30.0
    elif video >= 900:
        h, fps = 480, 30.0
    else:
        h, fps = 360, 30.0
    return video, max(2, min(h, src_h) // 2 * 2), min(fps, src_fps)    # even: x264 refuses an odd 4:2:0 height


def sound_wav(path: str, start: float, end: float, ffmpeg: str | None = None, mix=None,
              n_tracks: int = 0) -> str | None:
    """The sound of ``start``..``end`` as a temporary WAV (for winsound while the preview plays); None on failure
    or when the ``mix`` (1.8.6, as in cut(); ``n_tracks`` = the file's audio tracks) leaves no sound."""
    ffmpeg = ffmpeg or ffmpeg_exe()
    if not ffmpeg or end <= start:
        return None
    flt, amap = audio_graph(n_tracks, mix)
    if amap is None:
        return None
    pick = ["-filter_complex", flt, "-map", amap] if flt else ([] if amap == "0:a?" else ["-map", amap])
    fd, tmp = tempfile.mkstemp(prefix="dbdms-clip-", suffix=".wav")
    os.close(fd)
    try:
        p = subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{start:.3f}", "-to",
                            f"{end:.3f}", "-i", path, *pick, "-vn", "-ac", "2", "-ar", "44100", "-acodec", "pcm_s16le", tmp],
                           stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120,
                           creationflags=_flags())
        if p.returncode == 0 and os.path.getsize(tmp) > 44:
            return tmp
    except (OSError, subprocess.TimeoutExpired):
        pass
    try:
        os.remove(tmp)
    except OSError:
        pass
    return None


class FramePlayer(threading.Thread):
    """Streams scaled frames from ``start`` on through ffmpeg (rawvideo on stdout) and hands each one to
    ``on_frame(t, image)`` at the file's pace (frames that come late are dropped, at most FPS_CAP shown);
    ``on_end()`` when the file or the stretch is over. ``stop()`` ends it at once."""

    def __init__(self, path: str, start: float, info: Info, on_frame, on_end, end: float | None = None,
                 height: int = PREVIEW_H, ffmpeg: str | None = None):
        super().__init__(name="clip-player", daemon=True)
        self.path, self.start_t, self.info = path, max(0.0, start), info
        self.end_t = end
        self.on_frame, self.on_end = on_frame, on_end
        self.height = height
        self.ffmpeg = ffmpeg or ffmpeg_exe()
        self._stop = threading.Event()
        self._proc = None
        self.position = self.start_t

    def stop(self):
        self._stop.set()
        p = self._proc
        if p is not None:
            try:
                p.kill()
            except OSError:
                pass

    def _read(self, n: int) -> bytes:
        out = bytearray()
        stream = self._proc.stdout
        while len(out) < n and not self._stop.is_set():
            chunk = stream.read(n - len(out))
            if not chunk:
                break
            out += chunk
        return bytes(out)

    def run(self):
        from PIL import Image
        if not self.ffmpeg or not self.info.ok:
            self.on_end()
            return
        w, h = scaled(self.info, self.height)
        fps = min(FPS_CAP, self.info.fps or 30.0)
        args = [self.ffmpeg, "-hide_banner", "-loglevel", "error", "-ss", f"{self.start_t:.3f}"]
        if self.end_t is not None:
            args += ["-to", f"{self.end_t:.3f}"]
        args += ["-i", self.path, "-an", "-vf", f"fps={fps:g},scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
        try:
            self._proc = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                          stderr=subprocess.DEVNULL, creationflags=_flags(), bufsize=0)
        except OSError:
            self.on_end()
            return
        need = w * h * 3
        t0 = None                                         # the clock starts with the first frame (ffmpeg's start-up
        i = 0                                             # and seek take 0.1–0.5 s and must not count as "late")
        try:
            while not self._stop.is_set():
                buf = self._read(need)                    # a pipe gives short reads: collect a whole frame
                if len(buf) < need:
                    break
                t = self.start_t + i / fps
                i += 1
                if t0 is None:
                    t0 = time.monotonic()
                due = t0 + (t - self.start_t)
                late = time.monotonic() - due
                if late > 2.0 / fps:                      # behind: drop this frame, catch up
                    continue
                if late < 0:
                    self._stop.wait(-late)
                    if self._stop.is_set():
                        break
                self.position = t
                self.on_frame(t, Image.frombytes("RGB", (w, h), buf))
        finally:
            self.stop()
            self.on_end()                                 # the window ignores it when it stopped the player itself


# ---------------------------------------------------------------------------------------------- 1.12: the edit plan
SPEEDS = (0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 4.0)   # tempo of a part (slow motion … fast forward)
FADES = (0.0, 0.5, 1.0, 2.0)                       # seconds of fade-in / fade-out offered
GIF_FPS = 15
GIF_HEIGHTS = (360, 480, 720)
DEFAULT_GIF_H = 480
GIF_MAX_S = 60.0                # a longer GIF is refused (a GIF is for chats): a whole round as GIF was one click in
                                # the compact editor, minutes of encoding for a file of tens of MB
JOIN_GAP_S = 5.0                # a part shares the input of the part before it when the gap between them is at most
                                # this long: decoding the gap costs about what a new input's seek does (the key frame
                                # before it), and no decoder more (part_inputs)
MAX_INPUTS = 4                  # more far-apart scenes than this share inputs across the shortest gaps: every input
                                # is a decoder for the whole run (measured 3440x1440: ~220 MB each, 20 parts 5 GB)
ASPECTS = (("free", None), ("16:9", 16 / 9), ("9:16", 9 / 16), ("1:1", 1.0), ("4:5", 4 / 5))


@dataclass
class Part:
    start: float                 # seconds of the recording
    end: float
    speed: float = 1.0


@dataclass
class Edit:
    """1.12 (user: "Bildausschnitt / Hochformat, mehrere Abschnitte, Text, Pfeile, Markierungen, Tempo & Übergänge"):
    everything the clip editor does to a recording besides censoring and the sound mix. ``parts`` play one after
    the other (each with its own tempo), ``crop`` cuts a box (fractions) out of the picture, ``shapes``
    (annotate.Shape, times in seconds of the recording) are drawn over it, ``fade_in``/``fade_out`` dim picture
    and sound at the start/end of the finished clip."""
    parts: list = field(default_factory=list)
    crop: tuple | None = None
    shapes: list = field(default_factory=list)
    fade_in: float = 0.0
    fade_out: float = 0.0

    def simple(self) -> bool:
        """One part at normal tempo and nothing else – cut() alone does it (stream copy possible)."""
        return (len(self.parts) == 1 and abs(self.parts[0].speed - 1.0) < 1e-6 and not self.crop
                and not self.shapes and self.fade_in <= 0 and self.fade_out <= 0)

    def seconds(self) -> float:
        """Length of the finished clip."""
        return sum(max(0.0, p.end - p.start) / max(0.01, p.speed) for p in self.parts)


def clean_parts(parts, duration: float = 0.0) -> list:
    """Parts in time order, inside the recording, at least 0.1 s long, tempo within SPEEDS' range."""
    lo, hi = SPEEDS[0], SPEEDS[-1]
    out = []
    for p in parts:
        start, end = max(0.0, float(p.start)), float(p.end)
        if duration > 0:
            end = min(end, duration)
        if end - start >= 0.1:
            out.append(Part(start, end, max(lo, min(hi, float(p.speed or 1.0)))))
    return sorted(out, key=lambda p: p.start)


def atempo(speed: float) -> str:
    """ffmpeg's atempo takes 0.5–2 per filter: a chain for any tempo (0.25 = 0.5 · 0.5)."""
    parts, s = [], float(speed)
    while s < 0.5 - 1e-9:
        parts.append(0.5)
        s /= 0.5
    while s > 2.0 + 1e-9:
        parts.append(2.0)
        s /= 2.0
    parts.append(s)
    return ",".join(f"atempo={v:.4g}" for v in parts if abs(v - 1.0) > 1e-9) or "anull"


def crop_px(box, width: int, height: int) -> tuple:
    """(w, h, x, y) of a fraction crop box in even pixels (ffmpeg's crop filter, x264 wants even sizes)."""
    x, y, w, h = box_px(box, width, height)
    return w, h, x, y


def part_inputs(parts, join_gap: float | None = None, most: int | None = None) -> list:
    """How export reads ``parts`` (time order, see clean_parts): [(start, end, part indices)] per ffmpeg input,
    seeked to ``start`` and read to ``end``. Parts that overlap never share an input – one input split for both kept
    every frame they share as a raw picture until concat reached the later part (GBs for a part added twice). Parts
    one after the other share one when the gap between them is at most ``join_gap`` (JOIN_GAP_S; the gap is
    decoded and dropped), longer gaps get an input of their own while there are fewer than ``most`` (MAX_INPUTS) –
    the longest gaps first – since every input stays a decoder for the whole run (one per part: 5 GB for 20 parts
    of a 3440x1440 round). Pure."""
    join_gap = JOIN_GAP_S if join_gap is None else join_gap
    most = MAX_INPUTS if most is None else most
    lanes = []                                       # parts that never overlap, as few lanes as the overlaps allow
    for i, p in enumerate(parts):
        free = [ln for ln in lanes if parts[ln[-1]].end <= p.start + 1e-6]
        if free:
            max(free, key=lambda ln: parts[ln[-1]].end).append(i)     # the lane with the shortest gap
        else:
            lanes.append([i])
    gaps = sorted(((parts[b].start - parts[a].end, k, j) for k, ln in enumerate(lanes)
                   for j, (a, b) in enumerate(zip(ln, ln[1:]))), reverse=True)
    cuts, count = set(), len(lanes)
    for gap, k, j in gaps:
        if gap <= join_gap or count >= most:
            break
        cuts.add((k, j))
        count += 1
    groups = []
    for k, ln in enumerate(lanes):
        groups.append([ln[0]])
        for j, b in enumerate(ln[1:]):
            if (k, j) in cuts:
                groups.append([b])
            else:
                groups[-1].append(b)
    groups.sort(key=lambda g: g[0])
    return [(parts[g[0]].start, max(parts[i].end for i in g), g) for g in groups]


def edit_graph(edit: Edit, info: Info, mode: str = "exact", target_mb: float = DEFAULT_TARGET_MB, censor=None,
               censor_style: str = "pixel", mix=None, shape_inputs=(), gif_h: int = DEFAULT_GIF_H,
               palette: int | None = None):
    """The filter graph of ``edit`` (graph, video label, audio label or None, encoder arguments). The first inputs
    are the recording as part_inputs reads it (each seeked to its first part); an input that holds several parts is
    split and cut (trim) per part – the gaps are dropped right there, censor, drawings and crop work on the part
    only. ``shape_inputs`` = [(input index, t0, t1, x, y)] of the drawings' pictures (one PNG each, cut to the
    drawing and laid at x, y – see export; without x, y at the top left), laid over each part they show in. A GIF
    takes two runs: ``palette`` None = the first, ending in the palette (palettegen), else the input index of that
    palette for the second (paletteuse) – in one run ffmpeg kept every frame until the palette came at the end
    (~32 MB per second of GIF). Pure – tested without ffmpeg."""
    w, h = info.width, info.height
    parts = edit.parts
    n = len(parts)
    sound = mode != "gif" and audio_graph(info.audio_tracks, mix)[1] is not None and info.audio_tracks > 0
    chains = []
    out_w, out_h = w, h
    where, vsrc, asrc = {}, {}, {}                   # part → (input, its start, shared); its picture / sound
    for k, (start, _end, members) in enumerate(part_inputs(parts)):
        shared = len(members) > 1
        for i in members:
            where[i] = (k, start, shared)
        if shared:
            chains.append(f"[{k}:v]split={len(members)}" + "".join(f"[sv{i}]" for i in members))
        vsrc.update({i: f"[sv{i}]" if shared else f"[{k}:v]" for i in members})
        if sound:
            flt, amap = audio_graph(info.audio_tracks, mix, inp=k, tag=f"_i{k}")   # (censor_graph has "_{part}")
            if flt:
                chains.append(flt)
            a = amap if flt else (f"[{amap}]" if amap != f"{k}:a?" else f"[{k}:a:0]")
            if shared:
                chains.append(f"{a}asplit={len(members)}" + "".join(f"[sa{i}]" for i in members))
            asrc.update({i: f"[sa{i}]" if shared else a for i in members})
    for i, p in enumerate(parts):
        k, base, shared = where[i]
        cur = vsrc[i]
        if shared:                                       # this part of the input (its times stay those of the input)
            chains.append(f"{cur}trim=start={p.start - base:.3f}:end={p.end - base:.3f}[vt{i}]")
            cur = f"[vt{i}]"
        if censor:                                               # on the recording's own picture
            chains.append(censor_graph(censor, censor_style, w, h, src=cur, out=f"[vc{i}]", tag=f"_{i}"))
            cur = f"[vc{i}]"
        for j, inp in enumerate(shape_inputs):
            idx, t0, t1 = inp[:3]
            x, y = inp[3:5] if len(inp) >= 5 else (0, 0)
            if (t1 is not None and t1 <= p.start) or (t0 is not None and t0 >= p.end):
                continue                                         # not shown in this part
            when = ""
            if t0 is not None or t1 is not None:                 # times of the recording → of this part's input
                a = max(0.0, (t0 if t0 is not None else 0.0) - base)
                b = (t1 - base) if t1 is not None else 1e9
                when = f":enable='between(t,{a:.3f},{b:.3f})'"
            chains.append(f"{cur}[{idx}:v]overlay={x}:{y}:format=auto{when}[vs{i}_{j}]")
            cur = f"[vs{i}_{j}]"
        if edit.crop:
            cw, ch, cx, cy = crop_px(edit.crop, w, h)
            chains.append(f"{cur}crop={cw}:{ch}:{cx}:{cy}[vcr{i}]")
            cur, out_w, out_h = f"[vcr{i}]", cw, ch
        chains.append(f"{cur}setpts=(PTS-STARTPTS)/{p.speed:.4g}[v{i}]")
        if sound:
            trim = f"atrim=start={p.start - base:.3f}:end={p.end - base:.3f}," if shared else ""
            chains.append(f"{asrc[i]}{trim}asetpts=PTS-STARTPTS,{atempo(p.speed)}[a{i}]")
    if n > 1:
        ins = "".join(f"[v{i}]" + (f"[a{i}]" if sound else "") for i in range(n))
        chains.append(f"{ins}concat=n={n}:v=1:a={1 if sound else 0}[vcat]" + ("[acat]" if sound else ""))
        vcur, acur = "[vcat]", "[acat]" if sound else None
    else:
        vcur, acur = "[v0]", "[a0]" if sound else None
    total = edit.seconds()
    post = []
    args = []
    if mode == "discord":
        kbps, dh, fps = discord_plan(total, target_mb, Info(total, out_w, out_h, info.fps, info.audio_tracks))
        post += [f"scale=-2:{dh}", f"fps={fps:g}"]
        args += ["-c:v", "libx264", "-preset", "veryfast", "-b:v", f"{kbps}k", "-maxrate", f"{int(kbps * 1.1)}k",
                 "-bufsize", f"{kbps * 2}k", "-pix_fmt", "yuv420p"] + (["-c:a", "aac", "-b:a", f"{AUDIO_KBPS}k"]
                                                                      if sound else [])
    elif mode == "gif":
        # rgb24 before the fades: palettegen wants RGBA, and a fade on RGBA fades the alpha too – the fade-in came
        # out transparent, the fade-out froze on grey (paletteuse: alpha < 128 = "keep the previous picture")
        post += [f"fps={GIF_FPS}", f"scale=-2:{min(int(gif_h), out_h) // 2 * 2}:flags=lanczos", "format=rgb24"]
    else:
        # the file's own frame rate: setpts leaves the rate unknown, and ffmpeg then made 25 fps of a 60-fps round
        post.append(f"fps={info.fps:g}")
        args += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p"] + (
            ["-c:a", "aac", "-b:a", "160k"] if sound else [])
        if out_w % 2 or out_h % 2:
            post.append("scale=trunc(iw/2)*2:trunc(ih/2)*2")
    fi, fo = max(0.0, edit.fade_in), max(0.0, edit.fade_out)
    if fi > 0:
        post.append(f"fade=t=in:st=0:d={min(fi, total):.3f}")
    if fo > 0:
        post.append(f"fade=t=out:st={max(0.0, total - fo):.3f}:d={min(fo, total):.3f}")
    if mode == "gif" and palette is None:
        chains.append(f"{vcur}{','.join(post)},palettegen=stats_mode=diff[vout]")
    elif mode == "gif":
        chains.append(f"{vcur}{','.join(post)}[vg];[vg][{palette}:v]paletteuse=dither=bayer:bayer_scale=4[vout]")
    else:
        chains.append(f"{vcur}{','.join(post) or 'null'}[vout]")
    if sound:
        apost = []
        if fi > 0:
            apost.append(f"afade=t=in:st=0:d={min(fi, total):.3f}")
        if fo > 0:
            apost.append(f"afade=t=out:st={max(0.0, total - fo):.3f}:d={min(fo, total):.3f}")
        chains.append(f"{acur}{','.join(apost) or 'anull'}[aend]")
    return ";".join(chains), "[vout]", "[aend]" if sound else None, args


def _drop_dir(path: str):
    """Remove export's temporary folder (the drawings' PNGs, the GIF palette)."""
    if not path or not os.path.isdir(path):
        return
    for name in os.listdir(path):
        _remove(os.path.join(path, name))
    try:
        os.rmdir(path)
    except OSError:
        pass


def export(path: str, edit: Edit, out: str, mode: str = "exact", ffmpeg: str | None = None, run=None,
           target_mb: float = DEFAULT_TARGET_MB, info: Info | None = None, censor=None, censor_style: str = "pixel",
           mix=None, gif_h: int = DEFAULT_GIF_H, retry: bool = True) -> tuple[bool, str]:
    """1.12: write ``edit`` of ``path`` to ``out`` (mp4, or gif in mode "gif"). A simple edit (one part, nothing
    else) goes through cut() – stream copy stays possible; anything else re-encodes (mode "copy" becomes "exact").
    The recording is read as part_inputs says (input seeking: overlapping parts from inputs of their own, the gaps
    between scenes far apart not decoded, at most a few decoders however many parts). The drawings are drawn by
    annotate into one transparent PNG each (temporary, removed afterwards), cut to what they cover and laid over
    the picture at their spot for their time – a full-size picture per drawing cost ffmpeg as much again as the
    drawing (measured: 10 s 1080p60, four drawings, 5.5 s → 4.2 s). A GIF is made in two runs (palette, then the
    GIF – memory stays flat) and is at most GIF_MAX_S long. ffmpeg writes ``out`` + PART_EXT, renamed to ``out``
    once it succeeded. Returns (ok, ffmpeg's last words or the reason on failure)."""
    ffmpeg = ffmpeg or ffmpeg_exe()
    if not ffmpeg:
        return False, "ffmpeg fehlt"
    if info is None or not info.ok:
        info = probe(path, ffmpeg)
    parts = clean_parts(edit.parts, info.duration if info.ok else 0.0)
    if not parts:
        return False, "Ende vor Anfang"
    # the editor's drawings as they are now: the window keeps changing its own (colour, size, times, text)
    edit = Edit(parts, edit.crop, copy.deepcopy(list(edit.shapes)), edit.fade_in, edit.fade_out)
    if edit.simple() and mode != "gif":
        extra = {"censor": censor, "censor_style": censor_style} if censor else {}
        return cut(path, parts[0].start, parts[0].end, out, mode, ffmpeg, run=run, target_mb=target_mb, info=info,
                   retry=retry, mix=mix, **extra)
    if not info.ok:
        return False, "Video nicht lesbar"
    if mode == "gif" and edit.seconds() > GIF_MAX_S + 0.05:
        over = math.ceil(edit.seconds() * 10 - 1e-6) / 10     # rounded up: 60.06 s is no "60 s" over the limit
        return False, _("Ein GIF ist höchstens {limit} s lang, dieser Clip {seconds} s – kürzer schneiden oder als "
                        "Video speichern.", limit=f"{GIF_MAX_S:g}", seconds=f"{over:.1f}")
    if mode == "copy":
        mode = "exact"
    if run is None:
        def run(a):
            p = subprocess.run(a, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                               timeout=3600, creationflags=_flags())
            return p.returncode, p.stderr or b""

    def call(a):
        try:
            return run(a)
        except (OSError, subprocess.TimeoutExpired) as e:
            return 1, str(e).encode()
    tmpdir = ""
    tmp, fmt = _writing(out)
    key = part_key(tmp)
    PARTS_WRITING.add(key)                                      # obsrec.settle_parts leaves it alone meanwhile
    try:
        try:
            tmpdir = tempfile.mkdtemp(prefix="dbdms-edit-")
            args = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y"]
            inputs = part_inputs(parts)
            for start, end, _members in inputs:
                args += ["-ss", f"{start:.3f}", "-t", f"{end - start:.3f}", "-i", path]
            shape_inputs = []
            if edit.shapes:
                from . import annotate
                for shape in edit.shapes:
                    pic = annotate.layer(info.width, info.height, [shape])
                    box = pic.getbbox()
                    if box is None:                              # nothing to see (an empty text)
                        continue
                    png = os.path.join(tmpdir, f"shape{len(shape_inputs)}.png")
                    pic.crop(box).save(png)
                    # read as one PNG – image2 would take a "%d" in %TEMP% for a numbered sequence and fail
                    args += ["-f", "png_pipe", "-i", png]
                    shape_inputs.append((len(inputs) + len(shape_inputs), shape.t0, shape.t1, box[0], box[1]))
            os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        except OSError as e:                                     # %TEMP% full or not writable, the drive gone
            return False, str(e)

        def graph(palette=None):
            return edit_graph(edit, info, mode, target_mb, censor, censor_style, mix, shape_inputs, gif_h, palette)
        if mode == "gif":
            pal = os.path.join(tmpdir, "palette.png")              # "-update 1": a file name, not a pattern
            rc, err = call(args + ["-filter_complex", graph()[0], "-map", "[vout]", "-frames:v", "1", "-update", "1",
                                   "-f", "image2", pal])
            if rc == 0:
                rc, err = call(args + ["-f", "png_pipe", "-i", pal, "-filter_complex",
                                       graph(len(inputs) + len(shape_inputs))[0], "-map", "[vout]", "-an", *fmt, tmp])
        else:
            g, vmap, amap, enc = graph()
            rc, err = call(args + ["-filter_complex", g, "-map", vmap] + (["-map", amap] if amap else ["-an"]) + enc
                           + (["-movflags", "+faststart"] if out.lower().endswith(".mp4") else []) + fmt + [tmp])
    finally:
        PARTS_WRITING.discard(key)
        _drop_dir(tmpdir)
    ok = rc == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 0
    if not ok:
        _remove(tmp)
        return False, err[-300:].decode("utf-8", "replace").strip()
    if mode == "discord" and retry and os.path.getsize(tmp) > target_mb * 1024 * 1024:
        _remove(tmp)
        return export(path, edit, out, mode, ffmpeg, run, target_mb * 0.8, info, censor, censor_style, mix, gif_h,
                      retry=False)
    return _publish(tmp, out)
