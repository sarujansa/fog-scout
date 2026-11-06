"""Loading map pictures for the overlay, and the Win32 constants the overlay windows share.

The overlay windows themselves: overlay_win32.Win32Overlay (Windows), overlay_qt.QtOverlay (fallback)."""
from __future__ import annotations

import collections
import ctypes
import os
import sys
import threading

from PIL import Image, ImageSequence

from .mapimage import rotate_frames

IS_WIN = sys.platform == "win32"
BACKDROP = (18, 18, 20)         # behind half-transparent picture edges

GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_NOACTIVATE = 0x08000000
WS_EX_TOPMOST = 0x00000008

if IS_WIN:
    from ctypes import wintypes
    _user32 = ctypes.WinDLL("user32", use_last_error=True)
    if ctypes.sizeof(ctypes.c_void_p) == 8:
        _GetLong = _user32.GetWindowLongPtrW
        _SetLong = _user32.SetWindowLongPtrW
    else:  # pragma: no cover - 32-bit Python
        _GetLong = _user32.GetWindowLongW
        _SetLong = _user32.SetWindowLongW
    _GetLong.argtypes = [wintypes.HWND, ctypes.c_int]
    _GetLong.restype = ctypes.c_ssize_t
    _SetLong.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_ssize_t]
    _SetLong.restype = ctypes.c_ssize_t
    _user32.GetParent.argtypes = [wintypes.HWND]
    _user32.GetParent.restype = wintypes.HWND
    _user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int,
                                     ctypes.c_int, ctypes.c_int, wintypes.UINT]
    _user32.SetWindowPos.restype = wintypes.BOOL
    HWND_TOPMOST = wintypes.HWND(-1)
    HWND_NOTOPMOST = wintypes.HWND(-2)
    SWP_NOSIZE, SWP_NOMOVE, SWP_NOACTIVATE, SWP_FRAMECHANGED = 0x1, 0x2, 0x10, 0x20


MAX_LOAD_H = 1440          # the overlay is never taller than the screen (0.9 × 1440): bigger pictures shrink on load


def _fit(img: Image.Image) -> Image.Image:
    if img.height <= MAX_LOAD_H:
        return img
    # BOX: fast and clean for this step; the overlay scales down again with LANCZOS anyway
    return img.resize((max(1, round(img.width * MAX_LOAD_H / img.height)), MAX_LOAD_H), Image.BOX)


FRAMES_KEPT = 2            # 1.8.84: decoded maps kept (the one on display and the one before it)
_frames = collections.OrderedDict()     # (path, mtime, size, rotation) -> frames
_frames_lock = threading.Lock()


def load_frames(path: str, rotation: int = 0):
    """[(PIL RGBA image, duration ms)] – several for animated GIFs; ``rotation``: map turned clockwise (°).
    Pictures taller than MAX_LOAD_H are scaled down (Midwich: 6 × 2000² px = 96 MB otherwise). 1.8.84: the last
    FRAMES_KEPT results are kept by path, file time, size and rotation – show_map and set_map both load, a map
    shown again (layout, floor, the same round) is not decoded again (Midwich: 0.43 s each time). The callers
    only read the frames; a changed file (other time or size) is read anew."""
    try:
        st = os.stat(path)
        key = (os.path.abspath(path), st.st_mtime_ns, st.st_size, int(rotation))
    except OSError:
        key = None
    if key is not None:
        with _frames_lock:
            cached = _frames.get(key)
            if cached is not None:
                _frames.move_to_end(key)
                return list(cached)
    frames = _decode(path, rotation)
    if key is not None:
        with _frames_lock:
            _frames[key] = frames
            while len(_frames) > FRAMES_KEPT:
                _frames.popitem(last=False)
    return list(frames)


def clear_frames():
    """Forget the decoded maps (tests; after a map picture was replaced in place)."""
    with _frames_lock:
        _frames.clear()


# 1.38.57 (security review): user_maps/ is user-writable – a crafted picture must not take the memory. Bundled maps:
# ≤ 2000² px, ≤ 6 frames (Midwich), a few MB.
MAX_FILE_BYTES = 128 * 1024 * 1024     # a picture file above this is not read
MAX_PIXELS = 64 * 1024 * 1024          # one frame (canvas) above this is not decoded
MAX_FRAMES = 600                       # frames of an animation
MAX_KEPT_PIXELS = 256 * 1024 * 1024    # all decoded frames together (after _fit), ≈ 1 GB RGBA


def _decode(path: str, rotation: int):
    if os.path.getsize(path) > MAX_FILE_BYTES:
        raise OSError(f"picture file too big: {path}")
    try:
        im = Image.open(path)
    except Image.DecompressionBombError as e:            # a broken picture to the callers (they catch OSError)
        raise OSError(str(e)) from e
    with im:
        w, h = im.size
        if w <= 0 or h <= 0 or w * h > MAX_PIXELS:
            raise OSError(f"picture too big: {w}×{h} px")
        frames, kept = [], 0
        if getattr(im, "is_animated", False):
            if getattr(im, "n_frames", 1) > MAX_FRAMES:
                raise OSError(f"too many frames: {im.n_frames}")
            for fr in ImageSequence.Iterator(im):
                pic = fr.convert("RGBA")          # first: an animated WebP knows a frame's duration only once loaded
                d = fr.info.get("duration", 100) or 100
                pic = _fit(pic)
                kept += pic.width * pic.height
                if kept > MAX_KEPT_PIXELS or len(frames) >= MAX_FRAMES:
                    raise OSError("animation too big")
                frames.append((pic, max(40, int(d))))
        else:
            frames.append((_fit(im.convert("RGBA")), 0))
    return rotate_frames(frames, rotation)
