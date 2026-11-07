"""Native Windows overlay: a layered, click-through, always-on-top popup window.

The picture is pushed with UpdateLayeredWindow (per-pixel alpha), so the
transparent parts of a map really are transparent; Qt's window handling is not involved.
The window never takes the keyboard focus
(WS_EX_NOACTIVATE, shown with SW_SHOWNOACTIVATE) and lets every click through
to the game (WS_EX_TRANSPARENT) – except in edit mode, where it can be dragged.
"""
from __future__ import annotations

import ctypes
import re
import sys
import time

from PIL import Image

from .capture import is_above
from .layout import fit_height
from .mapimage import FONT as FIRA, floor_frames, floor_view   # FIRA: re-exported (tests, old imports)
from .overlay import BACKDROP, MAX_LOAD_H, load_frames   # BACKDROP: re-exported
from .overlay_render import (  # 1.38.34: the drawing lives there; every name stays importable from here
    _HAS, _GLYPHS, _CHAR_LEN,
    BORDER, CARD_BACKDROP, CARD_EDGE, DIM_LABEL, FALLBACK_FONTS, FIT_MIN, GLYPHS_KEPT, INFO_DOT, INFO_MEMO,
    INFO_SERVER, INFO_TIMER, INFO_WARN, PING_COLOURS, REC_DOT, TIMER_GAP, TITLE_SCALE, UPNEXT_SCALE, _ascent, _below,
    _beside, _char_len, _content_bottom, _draw_run, _fallback_font, _font, _font_key, _glyph, _has_glyph, _line_cap,
    _paste, _run_len, _stack, _tracked_width, add_border, add_info, backdrop, backdrop_pad, blend_cards, body_cols,
    compose, cover_radius, fira, fit_lines, font_for, guide_line, info_card, lines_above, map_backdrop, map_body,
    music_body, music_card, music_picture, pad_to, ping_colour, premultiplied_bgra, premultiplied_bgra_numpy,
    progress_strip, rec_dot, rec_phase, render_hud, render_music, render_music_compact, upnext_block, upnext_rows)
from .overlay_render import (  # 1.39: the input card
    INPUT_BG, INPUT_CAP, INPUT_CAP_DOWN, INPUT_EDGE, INPUT_EDGE_PX, INPUT_GAP, INPUT_H, INPUT_IDLE, INPUT_KEPT, INPUT_PAD, INPUT_PATCHES_KEPT, INPUT_RATIO, INPUT_SS, INPUT_W, PAD_FACE, _INPUT_MEMO, _INPUT_PATCHES, _cap_font, _centred_text, _draw_gamepad, _draw_keyboard, _input_box, _input_controls, _input_full, _input_keys, input_card, input_size)
_RENDER_NAMES = (FIRA, BACKDROP, _HAS, _GLYPHS, _CHAR_LEN, BORDER, CARD_BACKDROP, CARD_EDGE, DIM_LABEL, FALLBACK_FONTS, FIT_MIN, GLYPHS_KEPT, INFO_DOT, INFO_MEMO, INFO_SERVER, INFO_TIMER, INFO_WARN, PING_COLOURS, REC_DOT, TIMER_GAP, TITLE_SCALE, UPNEXT_SCALE, _ascent, _below, _beside, _char_len, _content_bottom, _draw_run, _fallback_font, _font, _font_key, _glyph, _has_glyph, _line_cap, _paste, _run_len, _stack, _tracked_width, add_border, add_info, backdrop, backdrop_pad, blend_cards, body_cols, compose, cover_radius, fira, fit_lines, font_for, guide_line, info_card, lines_above, map_backdrop, map_body, music_body, music_card, music_picture, pad_to, ping_colour, premultiplied_bgra, premultiplied_bgra_numpy, progress_strip, rec_dot, rec_phase, render_hud, render_music, render_music_compact, upnext_block, upnext_rows, INPUT_BG, INPUT_CAP, INPUT_CAP_DOWN, INPUT_EDGE, INPUT_EDGE_PX, INPUT_GAP, INPUT_H, INPUT_IDLE, INPUT_KEPT, INPUT_PAD, INPUT_PATCHES_KEPT, INPUT_RATIO, INPUT_SS, INPUT_W, PAD_FACE, _INPUT_MEMO, _INPUT_PATCHES, _cap_font, _centred_text, _draw_gamepad, _draw_keyboard, _input_box, _input_controls, _input_full, _input_keys, input_card, input_size)   # re-exported (keeps pyflakes from calling them unused)

IS_WIN = sys.platform == "win32"

WS_POPUP = 0x80000000
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
WS_EX_TOPMOST = 0x00000008
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_NOACTIVATE = 0x08000000
GWL_EXSTYLE = -20
GWLP_WNDPROC = -4
SW_HIDE = 0
SW_SHOWNOACTIVATE = 4
SWP_NOSIZE, SWP_NOMOVE, SWP_NOACTIVATE, SWP_FRAMECHANGED = 0x1, 0x2, 0x10, 0x20
ULW_ALPHA = 2
WM_NCHITTEST = 0x0084
WM_MOUSEWHEEL = 0x020A
MK_CONTROL = 0x0008                     # wParam key state of WM_MOUSEWHEEL: Ctrl held
WM_EXITSIZEMOVE = 0x0232
HTCAPTION = 2

if IS_WIN:
    from ctypes import wintypes

    _u = ctypes.WinDLL("user32", use_last_error=True)
    _g = ctypes.WinDLL("gdi32", use_last_error=True)
    _k = ctypes.WinDLL("kernel32", use_last_error=True)
    LRESULT = ctypes.c_ssize_t
    WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [("biSize", wintypes.DWORD), ("biWidth", wintypes.LONG), ("biHeight", wintypes.LONG),
                    ("biPlanes", wintypes.WORD), ("biBitCount", wintypes.WORD), ("biCompression", wintypes.DWORD),
                    ("biSizeImage", wintypes.DWORD), ("biXPelsPerMeter", wintypes.LONG),
                    ("biYPelsPerMeter", wintypes.LONG), ("biClrUsed", wintypes.DWORD),
                    ("biClrImportant", wintypes.DWORD)]

    class BITMAPINFO(ctypes.Structure):
        _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", wintypes.DWORD * 3)]

    class BLENDFUNCTION(ctypes.Structure):
        _fields_ = [("BlendOp", ctypes.c_ubyte), ("BlendFlags", ctypes.c_ubyte),
                    ("SourceConstantAlpha", ctypes.c_ubyte), ("AlphaFormat", ctypes.c_ubyte)]

    _k.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
    _k.GetModuleHandleW.restype = wintypes.HMODULE
    _u.CreateWindowExW.argtypes = [wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD,
                                   ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                   wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE, wintypes.LPVOID]
    _u.CreateWindowExW.restype = wintypes.HWND
    _u.DestroyWindow.argtypes = [wintypes.HWND]
    _u.DestroyWindow.restype = wintypes.BOOL
    _u.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
    _u.ShowWindow.restype = wintypes.BOOL
    _u.IsWindowVisible.argtypes = [wintypes.HWND]
    _u.IsWindowVisible.restype = wintypes.BOOL
    _u.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                ctypes.c_int, wintypes.UINT]
    _u.SetWindowPos.restype = wintypes.BOOL
    _u.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
    _u.GetWindowRect.restype = wintypes.BOOL
    _u.UpdateLayeredWindow.argtypes = [wintypes.HWND, wintypes.HDC, ctypes.POINTER(wintypes.POINT),
                                       ctypes.POINTER(wintypes.SIZE), wintypes.HDC, ctypes.POINTER(wintypes.POINT),
                                       wintypes.DWORD, ctypes.POINTER(BLENDFUNCTION), wintypes.DWORD]
    _u.UpdateLayeredWindow.restype = wintypes.BOOL
    _u.GetDC.argtypes = [wintypes.HWND]
    _u.GetDC.restype = wintypes.HDC
    _u.ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]
    _u.ReleaseDC.restype = ctypes.c_int
    _u.CallWindowProcW.argtypes = [ctypes.c_void_p, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    _u.CallWindowProcW.restype = LRESULT
    if ctypes.sizeof(ctypes.c_void_p) == 8:
        _GetLong, _SetLong = _u.GetWindowLongPtrW, _u.SetWindowLongPtrW
    else:  # pragma: no cover
        _GetLong, _SetLong = _u.GetWindowLongW, _u.SetWindowLongW
    _GetLong.argtypes = [wintypes.HWND, ctypes.c_int]
    _GetLong.restype = ctypes.c_ssize_t
    _SetLong.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_ssize_t]
    _SetLong.restype = ctypes.c_ssize_t
    _g.CreateCompatibleDC.argtypes = [wintypes.HDC]
    _g.CreateCompatibleDC.restype = wintypes.HDC
    _g.CreateDIBSection.argtypes = [wintypes.HDC, ctypes.POINTER(BITMAPINFO), wintypes.UINT,
                                    ctypes.POINTER(ctypes.c_void_p), wintypes.HANDLE, wintypes.DWORD]
    _g.CreateDIBSection.restype = wintypes.HBITMAP
    _g.SelectObject.argtypes = [wintypes.HDC, wintypes.HGDIOBJ]
    _g.SelectObject.restype = wintypes.HGDIOBJ
    _g.DeleteObject.argtypes = [wintypes.HGDIOBJ]
    _g.DeleteObject.restype = wintypes.BOOL
    _g.DeleteDC.argtypes = [wintypes.HDC]
    _g.DeleteDC.restype = wintypes.BOOL
    HWND_TOPMOST = wintypes.HWND(-1)
    HWND_NOTOPMOST = wintypes.HWND(-2)




class LayeredSurface:
    """1.34.1 (review P1): the memory DC and DIB section of one layered window, kept while its size stays – before,
    every push (once a second for the timer, every 30 ms while fading) made and freed both. The pixels are copied
    only when they are other bytes than last time: a fade pushes the same picture with another opacity."""

    def __init__(self):
        self._dc = self._bmp = self._old = None
        self._bits, self._size, self._data = 0, None, None

    def push(self, hwnd, data: bytes, w: int, h: int, pos, opacity: float) -> str:
        """Show premultiplied BGRA pixels in the layered window ``hwnd`` at ``pos``; returns an error text or ""."""
        try:
            if self._dc is None or self._size != (w, h):
                self.free()
                self._make(w, h)
            if data is not self._data:
                ctypes.memmove(self._bits, data, min(len(data), w * h * 4))
                self._data = data
            screen = _u.GetDC(None)
            try:
                blend = BLENDFUNCTION(0, 0, max(1, min(255, int(round(opacity * 255)))), 1)
                ok = _u.UpdateLayeredWindow(hwnd, screen, ctypes.byref(wintypes.POINT(int(pos[0]), int(pos[1]))),
                                            ctypes.byref(wintypes.SIZE(w, h)), self._dc,
                                            ctypes.byref(wintypes.POINT(0, 0)), 0, ctypes.byref(blend), ULW_ALPHA)
            finally:
                _u.ReleaseDC(None, screen)
            return "" if ok else f"UpdateLayeredWindow Fehler {ctypes.get_last_error()}"
        except OSError as e:
            self.free()
            return str(e)

    def _make(self, w: int, h: int) -> None:
        screen = _u.GetDC(None)
        try:
            dc = _g.CreateCompatibleDC(screen)
            if not dc:
                raise OSError(f"CreateCompatibleDC fehlgeschlagen (Fehler {ctypes.get_last_error()})")
            bmi = BITMAPINFO()
            bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
            bmi.bmiHeader.biWidth = w
            bmi.bmiHeader.biHeight = -h               # top-down rows
            bmi.bmiHeader.biPlanes = 1
            bmi.bmiHeader.biBitCount = 32
            bits = ctypes.c_void_p()
            bmp = _g.CreateDIBSection(screen, ctypes.byref(bmi), 0, ctypes.byref(bits), None, 0)
        finally:
            _u.ReleaseDC(None, screen)
        if not bmp or not bits.value:
            if bmp:
                _g.DeleteObject(bmp)
            _g.DeleteDC(dc)
            raise OSError(f"CreateDIBSection fehlgeschlagen (Fehler {ctypes.get_last_error()})")
        self._dc, self._bmp, self._bits, self._size = dc, bmp, bits.value, (w, h)
        self._old = _g.SelectObject(dc, bmp)

    def free(self) -> None:
        if self._dc is not None:
            _g.SelectObject(self._dc, self._old)
            _g.DeleteObject(self._bmp)
            _g.DeleteDC(self._dc)
        self._dc = self._bmp = self._old = None
        self._bits, self._size, self._data = 0, None, None


def _surface(win) -> LayeredSurface:
    s = win.__dict__.get("_surface")
    if s is None:
        s = win._surface = LayeredSurface()
    return s




class HudWindow:
    """Small click-through layered window for the system values at the top of a black bar (and, 1.64, the
    music card). In edit mode (the overlay's "Mit der Maus verschieben") it can be dragged like the map:
    ``on_moved(x, y)`` after the drop."""

    MEMO_KEPT = 4    # 1.8.31: the last pictures by key – the App measures at the natural size and then draws at
    #                  the steady one each tick; with one key only, both were drawn anew every tick

    def __init__(self, title: str = "Fog Scout Systemwerte"):
        ex = WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE
        self._hwnd = _u.CreateWindowExW(ex, "Static", title, WS_POPUP, 0, 0, 16, 16,
                                        None, None, _k.GetModuleHandleW(None), None)
        if not self._hwnd:
            raise OSError(f"CreateWindowExW fehlgeschlagen (Fehler {ctypes.get_last_error()})")
        self._hwnd = int(self._hwnd)
        self._key = None
        self._data = None
        self._pos = None
        self._bodies = {}                      # the music card's bodies (1.2.13), kept while a song plays
        self._pic = None                       # 1.8.89: the RGBA picture on display (obsoverlay composes it)
        self._memo = {}                        # 1.8.31: {key: (data, size)} of the last MEMO_KEPT pictures
        self._shown = False
        self.size = (0, 0)
        self._raised = 0.0
        self.opacity = 0.85
        self.last_error = ""
        self.editing = False
        self.edit_label = ""                   # name on the edit frame ("SYSTEMWERTE", "MUSIK")
        self.fade = 1.0                        # share of the opacity while fading in/out (music card, 1.2.4)
        self.on_moved = None
        self._proc = WNDPROC(self._wndproc)                    # keep a reference!
        self._old_proc = _SetLong(self._hwnd, GWLP_WNDPROC, ctypes.cast(self._proc, ctypes.c_void_p).value)

    def _wndproc(self, hwnd, msg, wp, lp):
        try:
            if self.editing:
                if msg == WM_NCHITTEST:
                    return HTCAPTION                  # drag anywhere on it
                if msg == WM_EXITSIZEMOVE:
                    rc = wintypes.RECT()
                    _u.GetWindowRect(self._hwnd, ctypes.byref(rc))
                    self._pos = (rc.left, rc.top, round(self.opacity, 3))
                    if self.on_moved:
                        self.on_moved(rc.left, rc.top)
        except Exception as e:  # never let an exception escape into Windows
            self.last_error = repr(e)
        return _u.CallWindowProcW(self._old_proc, hwnd, msg, wp, lp)

    def set_editing(self, on: bool):
        """Edit mode: clickable and draggable, with the yellow edit border."""
        if bool(on) == self.editing:
            return
        self.editing = bool(on)
        ex = _GetLong(self._hwnd, GWL_EXSTYLE)
        ex = ex & ~(WS_EX_TRANSPARENT | WS_EX_NOACTIVATE) if on else ex | WS_EX_TRANSPARENT | WS_EX_NOACTIVATE
        _SetLong(self._hwnd, GWL_EXSTYLE, ex)
        _u.SetWindowPos(self._hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_FRAMECHANGED)
        self._key = None                                  # re-render with/without border

    def set_picture(self, pic, key):
        """Show a ready picture (the centre guide lines, 1.64.5); ``key`` says when it changed."""
        if key != self._key:
            self._key = key
            self._data, self.size, self._pic = premultiplied_bgra(pic), pic.size, pic
            self._pos = None
        return self.size

    def picture(self):
        """1.8.89: the RGBA picture on display, None without one – composed into the picture OBS shows
        (obsoverlay) where the window capture lacks our windows."""
        return self._pic if self._data else None

    def render(self, rows, height: int, cover=None, style=None, progress=None, look=(), skin="classic",
               accent=None, title=None, upnext=None, upnext_pos="below", min_w=0, min_h=0):
        """Prepare the picture; returns its size (0, 0 without rows). ``cover``/``style``/``progress``/``look``: the
        music card (progress = (elapsed, total) seconds; redrawn once a second while a song plays). ``skin``
        (1.3): the overlay style – glass / chips / line draw the card in skin.py (``accent`` = the theme's colour,
        ``title`` = the card's header); "classic" as before. ``upnext`` (1.8) = (label, items) of the Spotify
        queue on the music card, ``upnext_pos`` below / right. ``min_w`` (1.8.28): at least this wide – the
        App's steady width, so a card never shrinks while its values change."""
        progress = (int(progress[0]), int(progress[1])) if progress else None
        look = tuple(sorted(look))
        upnext = (str(upnext[0]), tuple(tuple(i) for i in upnext[1])) if upnext and upnext[1] else None
        min_w, min_h = int(min_w or 0), int(min_h or 0)
        key = (tuple(tuple(r) for r in rows), int(height), self.editing, id(cover), style, progress, look, skin,
               accent, title, upnext, upnext_pos, min_w, min_h)
        if key != self._key:
            self._key = key
            memo = getattr(self, "_memo", None)
            if memo is None:
                memo = self._memo = {}
            hit = memo.get(key) if rows else None
            if hit is not None:                       # drawn a moment ago (natural size ↔ steady size)
                self._data, self.size, self._pic = hit
                self._pos = None
                return self.size
            if not rows:
                self._data, self.size, self._pic = None, (0, 0), None
            elif style is not None:                   # the music card (1.2.13: body once per song, strip every second)
                pic = music_picture(rows, height, cover, style, progress, look, skin, accent, upnext, upnext_pos,
                                    None, self._bodies, min_w, min_h)
            elif skin != "classic":
                from . import skin as skins
                pic = skins.card(rows, height, skin, accent, title, min_w=min_w)
            else:
                pic = pad_to(render_hud(rows, height), min_w)
                if "backdrop" in look:
                    pic = backdrop(pic, height)
            if rows:
                if self.editing:
                    pic = add_border(pic, self.edit_label)
                self._data, self.size, self._pic = premultiplied_bgra(pic), pic.size, pic
                self._pos = None                      # push again
                memo[key] = (self._data, self.size, self._pic)
                while len(memo) > self.MEMO_KEPT:
                    memo.pop(next(iter(memo)))
        return self.size

    def render_blend(self, old: dict, new: dict, t: float):
        """A song change (1.8.1): the card of the ``old`` song cross-faded into the ``new`` one at ``t`` (0 → 1) –
        both dicts are keyword arguments of music_picture (``new`` may carry ``anim`` for the sliding queue rows).
        Drawn anew every frame; the next ``render`` draws the final card again."""
        a = music_picture(bodies=self._bodies, **old)
        b = music_picture(bodies=self._bodies, **new)
        pic = blend_cards(a, b, t, new.get("style", "big") == "big" and new.get("cover") is not None)
        self._key = None
        self._data, self.size, self._pic = premultiplied_bgra(pic), pic.size, pic
        self._pos = None
        return self.size

    def show_at(self, x: int, y: int):
        if not self._data:
            self.hide()
            return
        pos = (int(x), int(y), round(self.opacity, 3))
        if pos != self._pos:
            self._pos = pos
            err = _surface(self).push(self._hwnd, self._data, self.size[0], self.size[1], pos[:2],
                                      self.opacity * self.fade)
            if err:
                self.last_error = err
        flags = SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
        if not self._shown:
            _u.ShowWindow(self._hwnd, SW_SHOWNOACTIVATE)
            self._shown = True
            self._raised = 0.0
        now = time.monotonic()
        if now - self._raised >= 1.0:                 # stay above DBD; once a second is enough (the UI ticks 4×/s)
            self._raised = now
            _u.SetWindowPos(self._hwnd, HWND_TOPMOST, 0, 0, 0, 0, flags)

    def hide(self):
        if self._shown:
            _u.ShowWindow(self._hwnd, SW_HIDE)
            self._shown = False

    def set_fade(self, fade: float):
        """Opacity share 0…1 while fading (1.2.4); pushed again at once when shown."""
        fade = min(1.0, max(0.0, fade))
        if fade == self.fade:
            return
        self.fade = fade
        if self._shown and self._data and self._pos:
            err = _surface(self).push(self._hwnd, self._data, self.size[0], self.size[1], self._pos[:2],
                                      self.opacity * fade)
            if err:
                self.last_error = err

    @property
    def shown(self):
        return self._shown

    def hwnd(self) -> int:
        return self._hwnd

    def destroy(self):
        try:
            _u.DestroyWindow(self._hwnd)
        except Exception:
            pass
        _surface(self).free()




class PictureOverlay:
    """The overlay's content and logic: map picture (+ caption), timer/server/ping/notes below it, the waiting
    card, floors, animation, edit mode. The window that shows it is a subclass's (Win32Overlay, QtOverlay):
    ``_push(pos)``, ``_show_window()``, ``_hide_window()``, ``_apply_editing()``, ``_raise()``,
    ``_destroy_window()``, ``hwnd()``, ``is_visible()``. ``root`` = mainloop.MainLoop (timers)."""

    def __init__(self, root):
        self.root = root
        self.opacity = 0.85
        self.transparent = True
        self.show_caption = True
        self.show_map = True            # off: only timer, server and ping ("nur Infos")
        self.edit_label = ""            # name on the edit frame (1.64.7: "KARTE · Strg+Mausrad = Grösse")
        self.info_beside = False        # timer/server right of the map (low bar above/below the picture)
        self.info_apart = False         # 1.8.24: the lines are an element of their own (info_picture), not drawn here
        self.lines_top = False          # 1.8.34: the lines drawn here go above the map (one block with it)
        self.text_height = 0            # px the timer/name/info are sized for (1.65: not the map's size); 0 = map
        self.backdrop = False           # dark area with rounded corners behind map and lines (1.2.4)
        self.skin = "classic"           # 1.3.1: overlay style of the map card (skin.map_card) – classic as before
        self.accent = None              # the theme's accent for the modern styles
        self.realm = ""                 # realm name for the card's header (glass, line)
        self.fade = 1.0                 # share of the opacity while fading in/out (1.2.9)
        self.on_moved = None
        self.on_wheel = None
        self.game_hwnd = None
        self.raised_over_game = 0
        self.last_error = ""
        self._frames = []               # [(PIL RGBA, duration)]
        self._caption = ""
        self._timer = ""                # round timer text below the map ("" = none)
        self._server = ""               # connected server region below the timer ("" = none)
        self._ping = None               # ping to that region in ms, below the region
        self._waiting = ()              # lines of the waiting card: shown instead of everything else
        self._note = ""                 # warning below the timer ("" = none)
        self._record = ""               # own results on this map below the timer ("" = none)
        self._memo = ()                 # 1.8.54: lines of the own note on this map (mapnotes.lines)
        self._rec = False               # 1.4.1: OBS records the round – blinking red dot right of the timer
        self._base = []                 # [(PIL RGBA, duration)] scaled map (+ caption), cached per size
        self._base_key = None
        self._prepared = []             # [(bytes, w, h, duration)]
        self._pics = []                 # 1.8.89: the frames' RGBA pictures (obsoverlay composes the shown one)
        self._key = None
        self._pushed_key = None         # _key of the picture last put on the screen
        self._fit = None                # fit_width(): (content key, text height, map height)
        self._fit_room = None           # fit_room(): (content key, map height) – 1.8.23
        self._frame_i = 0
        self._anim_job = None
        self._floor = None              # frame index of the floor on display; None = all floors one below the other
        self._view = None               # (frames on display, floors stacked) – mapimage.floor_view, cached
        self._shown = False
        self._editing = False
        self._pos = None
        self._size = (0, 0)

    def _start(self):
        """End of a subclass's __init__ (window made): stay on top from now on."""
        self._keep_on_top()

    # ------------------------------------------------------------ content
    def set_map(self, path, caption: str = "", rotation: int = 0, realm: str = "", frames=None):
        """``frames``: load_frames(path, rotation) when the caller has them already (1.11.1: App.show_map decoded
        every map twice – ~80 ms of the 290 ms the window stood when a banner was detected)."""
        self._stop_anim()
        self._frames = (frames if frames is not None else load_frames(path, rotation)) if path else []
        self._floor = self._view = None
        self._caption = caption
        self.realm = realm or ""
        self._base_key = self._key = None

    def set_skin(self, style: str, accent=None):
        """1.3.1: the overlay style of the map card (classic | glass | chips | line) and the theme's accent."""
        style = style if style in ("classic", "glass", "chips", "line") else "classic"
        if (style, accent) != (self.skin, self.accent):
            self.skin, self.accent = style, accent
            self._base_key = self._key = self._fit = self._fit_room = None

    def set_timer(self, text: str):
        """Round timer shown below the map; only re-renders when the text changes."""
        self._timer = text or ""

    def set_server(self, text: str, ping: float | None = None):
        """Connected server region (and its ping) shown below the timer."""
        self._server = text or ""
        self._ping = round(ping) if ping is not None and self._server else None

    def set_waiting(self, lines):
        """No map on screen: show only these lines ("Warte auf Map", lobby state); () = off."""
        self._waiting = tuple(lines or ())

    def set_note(self, text: str):
        """Warning in amber below the timer, e.g. a doubtful detection; "" = none."""
        self._note = text or ""

    def set_record(self, text: str):
        """Own results on the map on display ("Ø 2.8 Kills · 12 Runden"); "" = none."""
        self._record = text or ""

    def set_memo(self, lines):
        """1.8.54: the own note on the map on display as lines (mapnotes.lines); () = none."""
        self._memo = tuple(lines or ())

    def set_rec(self, on: bool):   # 1.4.1 / 1.5.2: blinking red dot right of the round timer
        """1.4.1: a red dot top right while OBS records the round."""
        self._rec = bool(on)

    def has_map(self) -> bool:
        return bool(self._frames)

    def _title_split(self, frames):
        """Row where the map starts below its drawn-in name (first picture; GIF floors have none), cached – with
        the columns of the map below it (``_cols``, 1.8.24)."""
        if not frames:
            return None
        key = (id(frames[0][0]), len(frames))
        if getattr(self, "_split_key", None) != key:
            from .mapimage import title_split
            parts = title_split(frames[0][0]) if len(frames) == 1 or self.stacked() <= 1 else None
            self._split_key, self._split = key, (parts[2] if parts else None)
            self._cols = body_cols(frames[0][0], self._split)
        return self._split

    def map_extent(self):
        """(w, h) to fit the map's size by (1.8.24): the loaded picture, as wide as what is drawn below its name."""
        iw, ih = self.map_size()
        if ih and self._title_split(self._view_frames()[0]) and self._cols:
            iw = self._cols[1] - self._cols[0]
        return iw, ih

    def floors(self) -> list:
        """Frame indices of the floors of the map (Midwich: bottom, top); [] = one floor."""
        return floor_frames(self._frames)

    def set_floor(self, index):
        """Show this frame (a floor) alone; None = all floors one below the other. The size changes with it:
        applied by the next render()."""
        index = index if index in floor_frames(self._frames) else None
        if index != self._floor:
            self._floor, self._view = index, None
            self._base_key = self._key = None

    def _view_frames(self):
        if self._view is None:
            self._view = floor_view(self._frames, self._floor, MAX_LOAD_H)
        return self._view

    def stacked(self) -> int:
        """Floors shown one below the other (Midwich: 2), else 1 – the app makes the overlay that much taller."""
        return self._view_frames()[1] if self._frames and self.show_map and not self._waiting else 1

    def map_size(self):
        """Size of the map picture as loaded (w, h) – to fit it without rendering it first."""
        return self._view_frames()[0][0][0].size if self._frames and self.show_map and not self._waiting else (0, 0)

    def has_info(self) -> bool:
        return bool(self._timer or self._server or self._note or self._record or self._memo)

    def set_lines_top(self, on: bool):
        """1.8.34 (user: "mit der Map kombinieren, oben oder unten"): the lines drawn with the map go above it."""
        if bool(on) != self.lines_top:
            self.lines_top = bool(on)
            self._key = self._fit = self._fit_room = None

    def set_info_apart(self, on: bool):
        """1.8.24: timer/record/server as their own element – the map window draws the map (+ name) alone."""
        if bool(on) != self.info_apart:
            self.info_apart = bool(on)
            self._base_key = self._key = self._fit = self._fit_room = None

    def _lines_here(self) -> bool:
        """The lines are drawn in this window (not apart; "nur Infos" always here)."""
        return not (self.info_apart and self.show_map)

    def waiting(self) -> bool:
        return bool(self._waiting)

    def info_picture(self, text_h: int, placeholder: str = ""):
        """The lines as a card of their own (1.8.24), None when there are none; ``placeholder``: a timer text to
        show without any lines (moving mode – something to drag)."""
        timer = self._timer or ("" if self.has_info() else placeholder)
        if not (timer or self._server or self._note or self._record or self._memo):
            return None
        rec = rec_phase() if self._rec else None
        key = (int(text_h), timer, self._server, self._ping, self._note, self._record, self._memo, rec, self.skin,
               self.accent, self.transparent, self.backdrop)
        if getattr(self, "_info_key", None) != key:
            self._info_key = key
            self._info_pic = info_card(timer, self._server, self._ping, self._note, self._record, int(text_h),
                                       self.skin, self.accent, self.transparent, self.backdrop, rec, self._memo)
        return self._info_pic

    def set_show_map(self, on: bool):
        self.show_map = bool(on)
        self._base_key = self._key = None

    def set_transparent(self, on: bool):
        self.transparent = bool(on)
        self._key = None

    def set_backdrop(self, on: bool):
        self.backdrop = bool(on)
        self._key = None

    def set_fade(self, fade: float):
        """Opacity share 0…1 while fading (1.2.9); pushed at once when shown."""
        fade = min(1.0, max(0.0, float(fade)))
        if fade == self.fade:
            return
        self.fade = fade
        if self._shown:
            self._push()
            self._pushed_opacity = round(self.opacity * self.fade, 3)

    def backdrop_pad(self, text_h: int) -> int:
        """Edge the dark area adds around the map (0 without it) – the App lets it use the margin, so the map
        stays as big as without the area (1.2.5, user: "Warum wird die Map kleiner?"). 1.3.1: the frame of the
        glass / line card the same way."""
        if self._modern():
            from .skin import frame_pad
            return frame_pad(self.skin, text_h)
        return backdrop_pad(text_h) if self.backdrop else 0

    def _modern(self) -> bool:
        """The map card is drawn by skin.map_card (not classic; the block beside the map stays classic)."""
        return self.skin != "classic" and not self.info_beside

    def render(self, height: int, push: bool = True):
        """Prepare pictures for this height; returns (w, h) of the overlay. ``push=False``: only measure – the
        screen keeps the picture it has (the App tries sizes before it settles; pushing each one made the
        overlay grow and shrink on every tick)."""
        if self._waiting:
            return self._render_waiting(max(40, int(self.text_height) or int(height)))
        if not self._frames:
            return 0, 0
        height = max(40, int(height))
        if not self.show_map and not self.has_info():
            return 0, 0                   # nothing to show without the map
        # text below/above the map is sized for one floor: stacked floors would double it; since 1.65 the App
        # gives it its own size (user: a bigger map, the same text)
        text_h = max(40, int(self.text_height) or height // self.stacked())
        modern = self._modern()
        headed = modern                   # 1.8.27: every modern style puts the name into the card's header
        base_key = (height, self._caption if self.show_caption and not headed else "", self.transparent,
                    self.show_map, text_h, self.skin if modern else "")
        new_base = base_key != self._base_key
        if new_base:                      # scaling is the slow part: done once per size, not per timer tick
            if self.show_map:
                frames = self._view_frames()[0]
                split = self._title_split(frames)
                if headed:                # 1.3.1: the map alone, its drawn name becomes the header
                    self._base = [(map_body(img, height, split), dur) for img, dur in frames]
                else:
                    self._base = [(compose(img, height, base_key[1], self.transparent, False, text_h, split,
                                           self._cols if split else None), dur)
                                  for img, dur in frames]
            else:                         # info only: an empty picture, the info block is drawn below it
                self._base = [(Image.new("RGBA", (1, 1), (0, 0, 0, 0)), 0)]
            self._base_key = base_key
        here = self._lines_here()                    # 1.8.24: the lines apart – the map alone
        rec = rec_phase() if self._rec and here else None     # 1.5.2: the dot blinks with the seconds
        timer, server, ping, note, record, memo = (self._timer, self._server, self._ping, self._note, self._record,
                                                   self._memo) if here else ("", "", None, "", "", ())
        top = self.lines_top and not self.info_beside
        key = (base_key, self._editing, timer, server, ping, note, record, memo,
               self.info_beside, self.backdrop, self.skin, self.accent, self.realm, rec, top)
        if key != self._key:
            self._prepared, self._pics = [], []
            pics = []
            if modern:
                from .skin import map_card
                for pic, dur in self._base:
                    pics.append(map_card(pic if self.show_map else None, self._caption, self.realm, timer,
                                         note, record, server, ping, (), text_h, self.skin,
                                         self.accent, rec=rec, lines_top=top, memo=memo))
            for pic, dur in ([] if modern else self._base):
                if here and self.has_info() and top and self.show_map:      # 1.8.34: the lines above the map
                    pic = lines_above(pic, add_info(Image.new("RGBA", (1, 1), (0, 0, 0, 0)), self._timer,
                                                    self._server, text_h, backdrop=not self.transparent,
                                                    ping=self._ping, note=self._note, record=self._record,
                                                    rec=rec, memo=self._memo), text_h)
                elif here and self.has_info():
                    pic = add_info(pic, self._timer, self._server, text_h, backdrop=not self.transparent,
                                   ping=self._ping, note=self._note, record=self._record,
                                   beside=self.info_beside and self.show_map, rec=rec, memo=self._memo)
                pics.append(pic)
            if self.backdrop and not modern:
                pics = map_backdrop(pics, text_h)
            for pic, (_b, dur) in zip(pics, self._base):
                if self._editing:
                    pic = add_border(pic.copy(), self.edit_label)
                self._prepared.append((premultiplied_bgra(pic), pic.width, pic.height, dur))
                self._pics.append(pic)
            self._key = key
            self._size = (self._prepared[0][1], self._prepared[0][2])
            if new_base or self._frame_i >= len(self._prepared):
                self._frame_i = 0
                if push:
                    self._restart_anim()
            # else: timer text changed – same frame, the animation keeps running
        if push and self._shown and self._pushed_key != self._key:
            self._push()
            self._pushed_key = self._key
            if self._anim_job is None:
                self._restart_anim()
        return self._size

    def fit_width(self, height: int, text_h: int, avail: float) -> int:
        """Map height and ``text_height`` at which the overlay is at most ``avail`` wide (a black bar): the lines
        below the map get smaller text first, the map only when that is not enough. Measured without putting
        anything on the screen, with the widest digits in the timer, and kept until the content changes – before,
        the App rendered big, showed it, then smaller: the map grew and shrank on every tick."""
        key = (height, text_h, avail) + self._content_key()
        if self._fit is None or self._fit[0] != key:
            timer, self._timer = self._timer, key[3]
            try:
                self.text_height = text_h
                pad2 = 2 * self.backdrop_pad(text_h)
                iw, ih = self.map_extent()
                if pad2 and ih:                 # the dark area's edge does not scale: the map makes room for it
                    height = fit_height(height, avail - pad2, iw, ih)
                w, _h = self.render(height, push=False)
                for _try in range(4):           # the lines below are wider than the bar: smaller text, same map
                    if w <= avail or self.text_height <= 40:
                        break
                    pad2 = 2 * self.backdrop_pad(self.text_height)
                    self.text_height = max(40, int(self.text_height * (avail - pad2) / max(1, w - pad2)) - 1)
                    w, _h = self.render(height, push=False)
                for _try in range(10):          # still too wide (the map with the area's edge): the map too
                    if w <= avail or height <= 80:
                        break
                    # at least 2 px smaller each time: the area's edge and the text's shadow do not scale with the
                    # map, a 1-px step could stall a few px too wide (sweep 1.2.10: 12 maps at text 160 %)
                    height = max(80, min(height - 2, int(height * avail / w)))
                    w, _h = self.render(height, push=False)
            finally:
                self._timer = timer
            self._fit = (key, self.text_height, height)
        self.text_height = self._fit[1]
        return self._fit[2]

    def _content_key(self) -> tuple:
        """What the overlay's size depends on besides the heights (the timer with its widest digits)."""
        return (re.sub(r"\d", "0", self._timer), self._server, self._ping, self._note, self._record, self._memo,
                self.info_beside,
                self.info_apart, self.lines_top,
                self._editing, self.show_map, self.show_caption, self._caption, self.transparent, self.backdrop,
                self._floor, id(self._frames[0][0]) if self._frames else None, self.skin, self.accent, self.realm,
                self._rec)

    def fit_room(self, height: int, room: int) -> int:
        """1.8.23 (user: right after 1.8.22 "the map got bigger and smaller all the time"): the map height at which
        the overlay is at most ``room`` tall – measured without putting anything on the screen and kept until
        the content changes. 1.8.22 rendered (and showed) the full size, then the smaller one, on every tick."""
        key = (height, room, self.text_height) + self._content_key()
        if self._fit_room is None or self._fit_room[0] != key:
            timer, self._timer = self._timer, key[3]
            try:
                _w, h = self.render(height, push=False)
                for _try in range(4):
                    if h <= room or height <= 80:
                        break
                    height = max(80, height - max(2, h - room))
                    _w, h = self.render(height, push=False)
            finally:
                self._timer = timer
            self._fit_room = (key, height)
        return self._fit_room[1]

    def _render_waiting(self, height: int):
        key = ("waiting", height, self.transparent, self._editing, self._waiting, self._server, self._ping,
               self.backdrop, self.skin, self.accent)
        if key != self._key:
            self._stop_anim()
            if self.skin != "classic":                           # 1.3.1: the waiting card in the overlay style
                from .skin import map_card
                pic = map_card(None, "", "", "", "", "", self._server, self._ping, self._waiting, height, self.skin,
                               self.accent)
            else:
                pic = add_info(Image.new("RGBA", (1, 1), (0, 0, 0, 0)), "", self._server, height,
                               backdrop=not self.transparent, ping=self._ping, status=self._waiting)
                if self.backdrop:
                    pic = map_backdrop([pic], height)[0]
            if self._editing:
                pic = add_border(pic.copy(), self.edit_label)
            self._prepared = [(premultiplied_bgra(pic), pic.width, pic.height, 0)]
            self._pics = [pic]
            self._key, self._base_key, self._frame_i = key, None, 0     # the map is rebuilt afterwards
            self._size = (pic.width, pic.height)
            if self._shown:
                self._push()
        return self._size

    # ----------------------------------------------------------- animation
    def _restart_anim(self):
        self._stop_anim()
        if len(self._prepared) > 1:
            self._anim_job = self.root.after(self._prepared[self._frame_i][3], self._next_frame)

    def _next_frame(self):
        if not self._prepared:
            return
        self._frame_i = (self._frame_i + 1) % len(self._prepared)
        if self._shown:
            self._push()
        self._anim_job = self.root.after(self._prepared[self._frame_i][3], self._next_frame)

    def _stop_anim(self):
        if self._anim_job:
            try:
                self.root.after_cancel(self._anim_job)
            except Exception:
                pass
            self._anim_job = None

    # ----------------------------------------------------------- placement
    def show_at(self, x: int, y: int):
        if not self._prepared:
            self.hide()
            return
        pos = (int(x), int(y))
        opacity_key = round(self.opacity * self.fade, 3)
        if not self._shown or pos != self._pos or opacity_key != getattr(self, "_pushed_opacity", None):
            self._pos = pos
            self._push(pos)
            self._pushed_key = self._key
            self._pushed_opacity = opacity_key
        if not self._shown:
            self._show_window()
            self._shown = True

    def hide(self):
        if self._shown:
            self._hide_window()
            self._shown = False

    @property
    def shown(self):
        return self._shown

    def picture(self):
        """1.8.89: the RGBA picture on display (the floor animation's current frame), None while nothing is
        prepared – composed into the picture OBS shows (obsoverlay) where the window capture lacks our windows."""
        if not self._prepared or not self._pics:
            return None
        return self._pics[min(self._frame_i, len(self._pics) - 1)]

    def _keep_on_top(self):
        try:
            if self._shown:
                self._raise()
        except Exception as e:
            self.last_error = repr(e)
        self.root.after(1000, self._keep_on_top)

    # ----------------------------------------------------------- edit mode
    def set_editing(self, on: bool):
        self._editing = bool(on)
        self._apply_editing()
        self._key = None                                  # re-render with/without border

    @property
    def editing(self):
        return self._editing

    @property
    def dragging(self) -> bool:
        """The user is moving it right now (the native window: Windows' own move loop, nothing to wait for)."""
        return False

    def destroy(self):
        self._stop_anim()
        try:
            self._destroy_window()
        except Exception:
            pass


class Win32Overlay(PictureOverlay):
    """The overlay as a layered Win32 popup: per-pixel alpha (UpdateLayeredWindow), click-through, never active."""

    def __init__(self, root):
        super().__init__(root)
        ex = WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE
        self._hwnd = _u.CreateWindowExW(ex, "Static", "Fog Scout Overlay", WS_POPUP, 0, 0, 16, 16,
                                        None, None, _k.GetModuleHandleW(None), None)
        if not self._hwnd:
            raise OSError(f"CreateWindowExW fehlgeschlagen (Fehler {ctypes.get_last_error()})")
        self._hwnd = int(self._hwnd)
        self._proc = WNDPROC(self._wndproc)                    # keep a reference!
        self._old_proc = _SetLong(self._hwnd, GWLP_WNDPROC, ctypes.cast(self._proc, ctypes.c_void_p).value)
        self._start()

    def _wndproc(self, hwnd, msg, wp, lp):
        try:
            if self._editing:
                if msg == WM_NCHITTEST:
                    return HTCAPTION                  # drag anywhere on the picture
                if msg == WM_EXITSIZEMOVE:
                    rc = wintypes.RECT()
                    _u.GetWindowRect(self._hwnd, ctypes.byref(rc))
                    self._pos = (rc.left, rc.top)
                    if self.on_moved:
                        self.on_moved(rc.left, rc.top)
                if msg == WM_MOUSEWHEEL and self.on_wheel and wp & MK_CONTROL:   # 1.3.2: Ctrl + wheel only
                    delta = ctypes.c_short((wp >> 16) & 0xFFFF).value
                    self.on_wheel(1 if delta > 0 else -1)
                    return 0
        except Exception as e:  # never let an exception escape into Windows
            self.last_error = repr(e)
        return _u.CallWindowProcW(self._old_proc, hwnd, msg, wp, lp)

    def _push(self, pos=None):
        """Hand the current frame to Windows (UpdateLayeredWindow)."""
        if not self._prepared:
            return
        data, w, h, _ = self._prepared[self._frame_i]
        err = _surface(self).push(self._hwnd, data, w, h, pos or self._pos or (0, 0), self.opacity * self.fade)
        if err:
            self.last_error = err

    def _show_window(self):
        _u.ShowWindow(self._hwnd, SW_SHOWNOACTIVATE)
        _u.SetWindowPos(self._hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE)

    def _hide_window(self):
        _u.ShowWindow(self._hwnd, SW_HIDE)

    def _raise(self):
        flags = SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
        _u.SetWindowPos(self._hwnd, HWND_TOPMOST, 0, 0, 0, 0, flags)
        game = self.game_hwnd() if self.game_hwnd else None
        if game and is_above(game, self._hwnd):
            _u.SetWindowPos(self._hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, flags)
            _u.SetWindowPos(self._hwnd, HWND_TOPMOST, 0, 0, 0, 0, flags)
            self.raised_over_game += 1

    def _apply_editing(self):
        ex = _GetLong(self._hwnd, GWL_EXSTYLE)
        if self._editing:
            ex &= ~(WS_EX_TRANSPARENT | WS_EX_NOACTIVATE)
        else:
            ex |= WS_EX_TRANSPARENT | WS_EX_NOACTIVATE
        _SetLong(self._hwnd, GWL_EXSTYLE, ex)
        _u.SetWindowPos(self._hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_FRAMECHANGED)

    def _destroy_window(self):
        _u.DestroyWindow(self._hwnd)
        _surface(self).free()

    def hwnd(self) -> int:
        return self._hwnd

    def is_visible(self) -> bool:
        return bool(_u.IsWindowVisible(self._hwnd))


def make_overlay(root, prefer_native: bool = True):
    """Native overlay on Windows (fallback, and elsewhere: a Qt window)."""
    from .overlay_qt import QtOverlay
    if IS_WIN and prefer_native:
        try:
            return Win32Overlay(root)
        except Exception as e:
            ov = QtOverlay(root)
            ov.last_error = f"natives Overlay nicht verfügbar: {e}"
            return ov
    return QtOverlay(root)

