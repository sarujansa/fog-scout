"""The clip editor window (1.5.1, user's wish: cut rounds "wie in Medal"): a preview picture, a timeline with
thumbnails, the F8 marks, a start/end range and a playhead; play/pause (frames streamed by ffmpeg, the sound
by Windows from a WAV of the same stretch), 1-s / 5-s / frame steps, "Clip speichern" (stream copy or frame
exact, see clipedit.cut) into the folder "Clips" next to the recordings.

All ffmpeg work runs in threads (clipedit); results come back over Qt signals. The window is a plain top-level
QWidget the App opens from the tab "Aufnahmen" (app_recordings._rec_clip)."""
from __future__ import annotations

import logging
import math
import os
import threading

from PySide6.QtCore import QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QImage, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (QButtonGroup, QCheckBox, QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit,
                               QListWidget, QProgressBar, QPushButton, QSizePolicy, QSlider, QTabWidget, QVBoxLayout,
                               QWidget)

from . import annotate, clipedit, imageedit, obsrec, qt_theme
from .i18n import N_, _
from .qt_common import guard_wheel

log = logging.getLogger("fogscout")

CENSOR_LABELS = {"pixel": N_("Verpixelt"), "blur": N_("Verwischt"), "black": N_("Schwarz"),
                 "retouch": N_("Retusche (aus der Umgebung übermalt)")}   # 1.7.2, retouch 1.7.3
COMPACT_PREVIEW_H = 360                          # 1.8.8: picture height of the preview beside the recordings
MIX_MAX = 150                                    # 1.8.6: a source may be raised to 150 %
SOURCE_LABELS = {"dbd": N_("Spiel"), "discord": N_("Discord"), "mic": N_("Mikrofon"), "other": N_("Hintergrund")}
SOURCE_TIPS = {"dbd": N_("Nur der Ton von Dead by Daylight – OBS-Spur 2."),
               "discord": N_("Discord-Sprachchat – OBS-Spur 3. Aus = der Clip hat keinen Discord-Ton."),
               "mic": N_("Dein Mikrofon – OBS-Spur 4 (nur, wenn es in OBS aufgenommen wird)."),
               "other": N_("Andere Programme mit eigener Tonquelle in OBS (z. B. Spotify, Browser) – OBS-Spur 5. Der "
                           "Desktop-Ton von Windows enthält auch DBD und Discord und liegt nur auf Spur 1.")}
ABSENT_TIPS = {"other": N_("In OBS gab es bei dieser Aufnahme keine Hintergrund-Quelle. Für Spotify, Browser & Co. "
                           "in OBS je Programm eine Anwendungs-Audioaufnahme anlegen – das Programm legt sie auf "
                           "Spur 5."),
               "dbd": N_("Diese Tonquelle war bei der Aufnahme unter Einstellungen → Aufnahmen "
                         "ausgeschaltet.")}
# 1.12.2: short names in the box (the long ones were cut off beside the recordings table), the long ones as tips
MODE_LABELS = {"copy": N_("Schnell (ohne Neukodieren)"), "exact": N_("Genau (neu kodiert)"),
               "discord": N_("Für Discord (Zielgrösse)"), "gif": N_("GIF (ohne Ton)")}
MODE_TIPS = {"copy": N_("Schnell (an Schlüsselbildern, Anfang bis zu ein paar Sekunden früher)"),
             "exact": N_("Genau (Bild neu kodiert, dauert etwas)"),
             "discord": N_("Für Discord (passt unter die Zielgrösse)"),
             "gif": N_("GIF (ohne Ton, für Chats)")}                                    # 1.12
SPEED_LABELS = {0.25: "×0.25", 0.5: "×0.5", 0.75: "×0.75", 1.0: N_("normal"), 1.5: "×1.5", 2.0: "×2", 4.0: "×4"}
CROP_LABELS = {"none": N_("Kein Ausschnitt"), "free": N_("Frei"), "16:9": "16:9", "9:16": N_("9:16 (Hochformat)"),
               "1:1": "1:1", "4:5": "4:5"}
DRAW_TOOLS = (("arrow", N_("Pfeil")), ("line", N_("Linie")), ("rect", N_("Rahmen")), ("ellipse", N_("Kreis")),
              ("free", N_("Freihand")), ("text", N_("Text")))
SIZE_LABELS = (N_("Dünn"), N_("Mittel"), N_("Dick"), N_("Sehr dick"))
SHOW_FOR = ((None, N_("Immer")), (1.0, N_("1 s ab Abspielkopf")), (3.0, N_("3 s ab Abspielkopf")),
            (5.0, N_("5 s ab Abspielkopf")), (10.0, N_("10 s ab Abspielkopf")))
KEY_HINT = N_("Leertaste Abspielen · ←/→ 1 s · Shift 5 s · Strg 1 Bild · I/O Start/Ende · A Abschnitt · M Marke · "
              "Pos1/Ende Anfang/Schluss · Entf Kasten/Zeichnung weg · Esc schliessen")
STEP_SMALL, STEP_BIG = 1.0, 5.0
LOAD_TIMEOUT_MS = 30000           # 1.8.3: the loading screen gives up after this and frees the window
PREVIEW_MIN = (640, 360)
PUMP_MS = 15                      # 1.8.66: how often the window takes what its threads produced


def _qimage(img) -> QImage:
    """PIL RGB -> QImage (copied: the PIL buffer may go)."""
    img = img.convert("RGB")
    w, h = img.size
    return QImage(img.tobytes(), w, h, w * 3, QImage.Format_RGB888).copy()


class _Channel:
    """One kind of message: ``emit`` from any thread only queues it, the ``connect``-ed handlers run in the GUI
    thread when the window's pump drains the bridge (the same names as the Qt signals before)."""

    def __init__(self, bridge, name):
        self._bridge, self._name = bridge, name

    def emit(self, *args):
        self._bridge.put(self._name, args)

    def connect(self, fn):
        self._bridge.handlers.setdefault(self._name, []).append(fn)


class _Bridge:
    """What the worker threads hand to the window. 1.8.66 (user: "das Programm crasht ab und zu, wenn ich Videos
    öffne"): this was a QObject whose signals the threads emitted – a window closed (another recording picked in
    the preview, the editor shut) while a thread still sent a frame, the strip or the levels raised "Signal source
    has been deleted", and when the deletion fell into the emit itself the whole program went down. Now the threads
    touch no Qt object at all: they append to a plain locked queue, the window's QTimer (dies with it) drains it."""
    NAMES = ("frame",        # scrub picture (t, PIL)
             "played",       # playback picture (t, PIL)
             "thumb",        # strip picture (index, PIL)
             "ended",        # the player that ended
             "saved",        # ok, path, why
             "sound",        # wav path (or None) ready for a playback from t
             "strip_done",   # 1.8.3: the thumbnail thread is through (all it could get)
             "still",        # 1.8.10: a still picture saved (ok, path)
             "levels")       # 1.8.18: {track index: loudest moment in dB}
    LATEST = ("frame", "played")      # pictures: only the newest of a batch is drawn
    AFTER_CLOSE = ("saved", "still")  # a save that ends after the window closed still reaches the clips list

    def __init__(self):
        self._lock = threading.Lock()
        self._queue = []
        self.handlers = {}
        for name in self.NAMES:
            setattr(self, name, _Channel(self, name))

    def put(self, name, args):
        with self._lock:
            self._queue.append((name, args))

    def clear(self, keep=()):
        """Drop what is queued – but the kinds in ``keep``."""
        with self._lock:
            self._queue = [m for m in self._queue if m[0] in keep]

    def drain(self):
        """Run the handlers of everything queued so far (GUI thread); of the pictures only the newest per kind."""
        with self._lock:
            batch, self._queue = self._queue, []
        last = {name: i for i, (name, _a) in enumerate(batch) if name in self.LATEST}
        for i, (name, args) in enumerate(batch):
            if name in last and last[name] != i:
                continue
            for fn in self.handlers.get(name, ()):
                try:
                    fn(*args)
                except Exception:
                    log.exception("Clip-Editor: %s", name)


class Timeline(QWidget):
    """Thumbnail strip with the start/end range, the playhead and the marks. Drag the handles or the playhead,
    click to seek, wheel = ±1 s (Ctrl: ±0.1 s)."""
    HANDLE = 7
    TOP = 12
    changed = Signal()                    # start/end moved
    seek = Signal(float)                  # the user wants this moment
    picked = Signal(str, float)           # 1.8.10: a line of the right-click menu, at that moment

    def __init__(self, dark=True):
        super().__init__()
        self.duration = 1.0
        self.pos = 0.0
        self.start, self.end = 0.0, 1.0
        self.marks = []
        self.parts = []                   # 1.12: [(start, end)] of the parts kept – bands above the strip
        self.thumbs = {}
        self.n_thumbs = clipedit.THUMBS
        self.dark = dark
        self._drag = None                 # "start" / "end" / "pos"
        self.setMinimumHeight(clipedit.THUMB_H + self.TOP + 4)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.NoFocus)

    # ---- data
    def set_duration(self, d: float):
        self.duration = max(0.1, float(d))
        self.end = min(self.end, self.duration) if self.end > 0 else self.duration
        self.update()

    def set_range(self, start: float, end: float):
        start = min(max(0.0, start), self.duration)
        end = min(max(start + 0.1, end), self.duration)
        if (start, end) != (self.start, self.end):
            self.start, self.end = start, end
            self.update()
            self.changed.emit()

    def set_position(self, t: float):
        self.pos = min(max(0.0, t), self.duration)
        self.update()

    def set_thumb(self, i: int, img):
        self.thumbs[i] = _qimage(img)
        self.update()

    # ---- geometry
    def _strip(self) -> QRectF:
        return QRectF(self.HANDLE, self.TOP, self.width() - 2 * self.HANDLE, self.height() - self.TOP - 2)

    def _x(self, t: float) -> float:
        r = self._strip()
        return r.left() + r.width() * (t / self.duration)

    def _t(self, x: float) -> float:
        r = self._strip()
        return min(max(0.0, (x - r.left()) / max(1.0, r.width()) * self.duration), self.duration)

    # ---- drawing
    def paintEvent(self, e):
        c = qt_theme.colours(self.dark)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = self._strip()
        p.fillRect(r, QColor(c["field"]))
        n = max(1, self.n_thumbs)
        for i in range(n):
            img = self.thumbs.get(i)
            x0, x1 = r.left() + r.width() * i / n, r.left() + r.width() * (i + 1) / n
            if img is not None:
                target = QRectF(x0, r.top(), x1 - x0, r.height())
                p.drawImage(target, img, QRectF(0, 0, img.width(), img.height()))
        shade = QColor(0, 0, 0, 150)
        p.fillRect(QRectF(r.left(), r.top(), self._x(self.start) - r.left(), r.height()), shade)
        p.fillRect(QRectF(self._x(self.end), r.top(), r.right() - self._x(self.end), r.height()), shade)
        accent = QColor(c["accent"])
        band = QColor(accent)
        band.setAlpha(150)
        for a, b in self.parts:                               # 1.12: the parts kept, a band each at the top
            p.fillRect(QRectF(self._x(a), r.top() - 5, max(2.0, self._x(b) - self._x(a)), 4), band)
        p.setPen(QPen(accent, 2))
        p.setBrush(accent)
        for m in self.marks:                                  # marks: small triangles above the strip
            x = self._x(m)
            p.drawPolygon([QRectF(x - 4, 0, 8, self.TOP - 2).topLeft(), QRectF(x - 4, 0, 8, self.TOP - 2).topRight(),
                           QRectF(x - 4, 0, 8, self.TOP - 2).center() + (QRectF(0, 0, 0, self.TOP - 2).bottomLeft())])
        for t in (self.start, self.end):                      # handles
            x = self._x(t)
            p.drawRoundedRect(QRectF(x - self.HANDLE / 2, r.top() - 2, self.HANDLE, r.height() + 4), 2, 2)
        p.setPen(QPen(accent, 2))
        p.drawLine(self._x(self.start), r.top(), self._x(self.end), r.top())
        p.drawLine(self._x(self.start), r.bottom(), self._x(self.end), r.bottom())
        p.setPen(QPen(QColor("#ffffff"), 2))                  # playhead
        x = self._x(self.pos)
        p.drawLine(x, r.top() - 4, x, r.bottom() + 2)
        p.end()

    # ---- mouse
    def _hit(self, x: float):
        for name, t in (("start", self.start), ("end", self.end)):
            if abs(self._x(t) - x) <= self.HANDLE:
                return name
        return "pos"

    def contextMenuEvent(self, e):
        """1.8.10: right click on the strip: the clip starts/ends here, the playhead here, a still picture."""
        from PySide6.QtWidgets import QMenu
        if self.duration <= 0:
            return
        t = self._t(e.pos().x())
        menu = QMenu(self)
        for ident, label in (("seek", _("Abspielkopf hierher")), ("start", _("Clip beginnt hier")),
                             ("end", _("Clip endet hier")), (None, None), ("still", _("Standbild hier speichern"))):
            if ident is None:
                menu.addSeparator()
                continue
            menu.addAction(f"{label}  ({clipedit.fmt_pos(t)})").triggered.connect(
                lambda _c=False, i=ident: self.picked.emit(i, t))
        self._menu = menu
        menu.popup(e.globalPos())

    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return
        self._drag = self._hit(e.position().x())
        self.mouseMoveEvent(e)

    def mouseMoveEvent(self, e):
        if self._drag is None:
            return
        t = self._t(e.position().x())
        if self._drag == "start":
            self.set_range(min(t, self.end - 0.1), self.end)
            self.seek.emit(self.start)
        elif self._drag == "end":
            self.set_range(self.start, max(t, self.start + 0.1))
            self.seek.emit(self.end)
        else:
            self.set_position(t)
            self.seek.emit(t)

    def mouseReleaseEvent(self, e):
        self._drag = None

    def wheelEvent(self, e):
        step = 0.1 if e.modifiers() & Qt.ControlModifier else STEP_SMALL
        d = e.angleDelta().y()
        if d:
            t = self.pos + (step if d > 0 else -step)
            self.set_position(t)
            self.seek.emit(self.pos)
        e.accept()


class PreviewView(QWidget):
    """1.7.2: the picture, letterboxed on a dark rounded area, with the censor boxes drawn over it the way the
    saved clip will look (pixel blocks / blur / black). With the tool on (``editing``) a drag on free picture
    draws a new box, a drag inside a box moves it, its bottom-right corner resizes it, a click picks it."""
    boxes_changed = Signal()
    crop_changed = Signal()               # 1.12: the crop box was drawn/moved/resized
    shapes_changed = Signal()             # 1.12: a drawing was added/moved
    shape_picked = Signal(int)            # 1.12: a drawing was clicked (-1: none)
    HANDLE = 10
    MIN_BOX = 0.01                        # fractions of the picture: smaller drags are dropped

    def __init__(self, dark=True):
        super().__init__()
        self.dark = dark
        self._img = None                  # QImage of the frame
        self._scaled = None               # (size, QImage) cache of the frame at the drawn size
        self.boxes = []                   # [[x, y, w, h] …] fractions of the picture
        self.style = "pixel"
        self.active = False               # boxes are applied when saving (and shown applied here)
        self.editing = False              # the tool is on: boxes can be drawn/moved
        self.selected = None
        self._drag = None                 # (kind, press point, original box)
        # 1.12: the crop box and the drawings (annotate.Shape), both in fractions of the picture
        self.crop = None                  # (x, y, w, h) or None
        self.crop_ratio = None            # width/height in pixels the box keeps (None: free)
        self.crop_edit = False            # the crop tool is on
        self.shapes = []
        self.shape_tool = None            # annotate kind to draw, None = off
        self.shape_sel = None             # index of the picked drawing
        self.pen = {"colour": annotate.COLOURS[0], "size": annotate.DEFAULT_SIZE, "text_size": annotate.TEXT_SIZE,
                    "text": ""}
        self.now = None                   # seconds of the recording on display: drawings of other times hide
        self.new_times = lambda: (None, None)   # (t0, t1) a new drawing gets (the clip editor: from the playhead)
        self._layer = None                # (key, QImage) of the drawings at the drawn size
        self.source_size = None           # (w, h) of the real picture when the frame is a smaller copy of it
        self.setMinimumSize(*PREVIEW_MIN)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFocusPolicy(Qt.NoFocus)
        self.setMouseTracking(True)

    # ---- data
    def pixmap(self) -> QPixmap:
        return QPixmap.fromImage(self._img) if self._img is not None else QPixmap()

    def set_frame(self, img: QImage):
        self._img, self._scaled = img, None
        self.update()

    def set_boxes(self, boxes):
        self.boxes = [list(map(float, b)) for b in boxes if len(b) == 4]
        self.selected = None
        self.update()

    def set_editing(self, on: bool):
        self.editing = bool(on)
        self.setCursor(Qt.CrossCursor if self.editing else Qt.ArrowCursor)
        if not self.editing:
            self.selected = None
        self.update()

    def set_look(self, active: bool, style: str):
        self.active, self.style = bool(active), style
        self.update()

    def add_box(self, box, select=True):
        self.boxes.append(list(map(float, box)))
        if select:
            self.selected = len(self.boxes) - 1
        self.update()
        self.boxes_changed.emit()

    def remove_selected(self) -> bool:
        if self.selected is None or not (0 <= self.selected < len(self.boxes)):
            return False
        del self.boxes[self.selected]
        self.selected = None
        self.update()
        self.boxes_changed.emit()
        return True

    def clear_boxes(self):
        if self.boxes:
            self.boxes, self.selected = [], None
            self.update()
            self.boxes_changed.emit()

    # ---- 1.12: crop and drawings
    def image_size(self) -> tuple:
        if self.source_size:
            return self.source_size
        return (self._img.width(), self._img.height()) if self._img is not None else (16, 9)

    def set_crop(self, box, ratio=None):
        self.crop = tuple(box) if box else None
        self.crop_ratio = ratio
        self.update()

    def set_crop_edit(self, on: bool):
        self.crop_edit = bool(on)
        if on:
            self.set_editing(False)
            self.set_shape_tool(None)
        self.setCursor(Qt.CrossCursor if on else Qt.ArrowCursor)
        self.update()

    def set_shapes(self, shapes):
        self.shapes = list(shapes)
        self.shape_sel = None if self.shape_sel is None or self.shape_sel >= len(self.shapes) else self.shape_sel
        self._layer = None
        self.update()

    def set_shape_tool(self, kind):
        self.shape_tool = kind
        if kind:
            self.crop_edit = False
            if self.editing:
                self.set_editing(False)
        self.setCursor(Qt.CrossCursor if kind else Qt.ArrowCursor)
        self.update()

    def set_now(self, t):
        if t != self.now:
            self.now = t
            self.update()

    def selected_shape(self):
        return self.shapes[self.shape_sel] if self.shape_sel is not None and self.shape_sel < len(self.shapes) else None

    def replace_selected_shape(self, shape):
        if self.selected_shape() is not None:
            self.shapes[self.shape_sel] = shape
            self._layer = None
            self.update()
            self.shapes_changed.emit()

    def remove_selected_shape(self) -> bool:
        if self.selected_shape() is None:
            return False
        del self.shapes[self.shape_sel]
        self.shape_sel = None
        self._layer = None
        self.update()
        self.shapes_changed.emit()
        self.shape_picked.emit(-1)
        return True

    def _shown_shapes(self):
        shown = [s for s in self.shapes if self.now is None or s.shown_at(self.now)]
        drawing = getattr(self, "_preview_new", None)
        return shown + [drawing] if drawing is not None else shown

    def _active_shape(self):
        """The drawing being drawn or moved right now (None without a drag)."""
        kind = self._drag[0] if self._drag else None
        if kind == "shape_new":
            return getattr(self, "_preview_new", None)
        if kind == "shape_move" and self.shape_sel is not None and 0 <= self.shape_sel < len(self.shapes):
            return self.shapes[self.shape_sel]
        return None

    @staticmethod
    def _shape_image(size, shapes) -> QImage:
        img = annotate.layer(size.width(), size.height(), shapes)
        return QImage(img.tobytes(), img.width, img.height, img.width * 4, QImage.Format_RGBA8888).copy()

    def _crop_box_for(self, x0, y0, x1, y1) -> tuple:
        """A crop box from two corners (fractions), held to ``crop_ratio`` (the width leads)."""
        x, y, w, h = min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0)
        if self.crop_ratio:
            iw, ih = self.image_size()
            h = w * iw / (self.crop_ratio * ih)
            if y1 < y0:
                y = y0 - h
            if y + h > 1.0:                                   # too tall for the room: the height leads
                h = 1.0 - y
                w = h * ih * self.crop_ratio / iw
                if x1 < x0:
                    x = x0 - w
        return imageedit.clamp_box((x, y, w, h), self.MIN_BOX)

    # ---- geometry
    def frame_rect(self) -> QRectF:
        """Where the picture lies (aspect kept, centred); 16:9 while there is no picture yet."""
        area = QRectF(self.rect()).adjusted(2, 2, -2, -2)
        iw, ih = (self._img.width(), self._img.height()) if self._img is not None else (16, 9)
        if iw <= 0 or ih <= 0:
            return area
        s = min(area.width() / iw, area.height() / ih)
        w, h = iw * s, ih * s
        return QRectF(area.center().x() - w / 2, area.center().y() - h / 2, w, h)

    def _box_rect(self, box) -> QRectF:
        f = self.frame_rect()
        x, y, w, h = box
        return QRectF(f.left() + x * f.width(), f.top() + y * f.height(), w * f.width(), h * f.height())

    def _to_frac(self, pt) -> tuple:
        f = self.frame_rect()
        return (min(max(0.0, (pt.x() - f.left()) / max(1.0, f.width())), 1.0),
                min(max(0.0, (pt.y() - f.top()) / max(1.0, f.height())), 1.0))

    # ---- drawing
    def _frame_scaled(self, size):
        if self._scaled is None or self._scaled[0] != size:
            self._scaled = (size, self._img.scaled(size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        return self._scaled[1]

    def paintEvent(self, e):
        c = qt_theme.colours(self.dark)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#000000"))
        p.drawRoundedRect(QRectF(self.rect()), 8, 8)
        f = self.frame_rect()
        if self._img is None:
            p.end()
            return
        size = f.toRect().size()
        if size.width() < 2 or size.height() < 2:
            p.end()
            return
        scaled = self._frame_scaled(size)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        p.drawImage(f.topLeft(), scaled)
        accent = QColor(c["accent"])
        for i, box in enumerate(self.boxes):
            r = self._box_rect(box)
            if self.active:
                self._draw_censored(p, scaled, r, f)
            if self.editing or not self.active:
                pen = QPen(accent if i == self.selected else QColor(255, 255, 255, 170), 2 if i == self.selected else 1)
                if not self.active:
                    pen.setStyle(Qt.DashLine)
                p.setPen(pen)
                p.setBrush(Qt.NoBrush)
                p.drawRect(r)
                if self.editing:
                    p.setBrush(accent if i == self.selected else QColor(255, 255, 255, 200))
                    p.setPen(Qt.NoPen)
                    p.drawRect(QRectF(r.right() - self.HANDLE / 2, r.bottom() - self.HANDLE / 2, self.HANDLE, self.HANDLE))
        if self.editing and self._drag and self._drag[0] == "new":
            p.setPen(QPen(accent, 1, Qt.DashLine))
            p.setBrush(Qt.NoBrush)
            p.drawRect(self._box_rect(self._drag[2]))
        self._paint_shapes(p, f, size, accent)
        self._paint_crop(p, f, accent)
        p.end()

    def _paint_shapes(self, p, f, size, accent):
        """1.12: the drawings as the clip/picture will show them (annotate draws them at the shown size). The ones
        that stay still are kept as one picture; only the drawing under the mouse is drawn again on each move."""
        shown = self._shown_shapes()
        active = self._active_shape()
        still = [s for s in shown if s is not active]
        if still:
            key = (size.width(), size.height(), repr(still))
            if self._layer is None or self._layer[0] != key:
                self._layer = (key, self._shape_image(size, still))
            p.drawImage(f.topLeft(), self._layer[1])
        if active is not None and any(s is active for s in shown):
            p.drawImage(f.topLeft(), self._shape_image(size, [active]))
        sel = self.selected_shape()
        if sel is not None and self.shape_tool is not None:
            x0, y0, x1, y1 = annotate.bounds(sel, int(f.width()), int(f.height()))
            p.setPen(QPen(accent, 1, Qt.DashLine))
            p.setBrush(Qt.NoBrush)
            p.drawRect(QRectF(f.left() + x0, f.top() + y0, x1 - x0, y1 - y0))

    def _paint_crop(self, p, f, accent):
        """1.12: outside the crop box darkened; with the tool on its frame and four corner handles."""
        box = self._drag[2] if self._drag and self._drag[0].startswith("crop") else self.crop
        if not box:
            return
        r = self._box_rect(box)
        shade = QColor(0, 0, 0, 170 if self.crop_edit else 150)
        for part in (QRectF(f.left(), f.top(), f.width(), r.top() - f.top()),
                     QRectF(f.left(), r.bottom(), f.width(), f.bottom() - r.bottom()),
                     QRectF(f.left(), r.top(), r.left() - f.left(), r.height()),
                     QRectF(r.right(), r.top(), f.right() - r.right(), r.height())):
            if part.width() > 0 and part.height() > 0:
                p.fillRect(part, shade)
        p.setPen(QPen(accent if self.crop_edit else QColor(255, 255, 255, 160), 2))
        p.setBrush(Qt.NoBrush)
        p.drawRect(r)
        if self.crop_edit:
            p.setBrush(accent)
            p.setPen(Qt.NoPen)
            for cx, cy in ((r.left(), r.top()), (r.right(), r.top()), (r.left(), r.bottom()), (r.right(), r.bottom())):
                p.drawRect(QRectF(cx - self.HANDLE / 2, cy - self.HANDLE / 2, self.HANDLE, self.HANDLE))

    def _draw_censored(self, p, scaled, r, f):
        """The box as the clip will show it: coarse blocks, a blur, or black (same rules as clipedit.censor_graph)."""
        if self.style == "black":
            p.fillRect(r, QColor("#000000"))
            return
        src = QRectF(r.left() - f.left(), r.top() - f.top(), r.width(), r.height()).toRect() \
            .intersected(scaled.rect())
        if src.width() < 2 or src.height() < 2:
            return
        if self.style == "retouch":        # delogo-like: a smooth fill from the pixels around the box
            m = max(2, min(src.width(), src.height()) // 6)
            around = scaled.copy(src.adjusted(-m, -m, m, m).intersected(scaled.rect()))
            look = around.scaled(2, 2, Qt.IgnoreAspectRatio, Qt.SmoothTransformation) \
                .scaled(src.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            p.drawImage(QRectF(src).translated(f.left(), f.top()).topLeft(), look)
            return
        part = scaled.copy(src)
        if self.style == "blur":
            small = part.scaled(max(1, src.width() // 6), max(1, src.height() // 6), Qt.IgnoreAspectRatio,
                                Qt.SmoothTransformation)
            look = small.scaled(src.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        else:
            blk = max(2, min(src.width(), src.height()) // 8)
            small = part.scaled(max(1, src.width() // blk), max(1, src.height() // blk), Qt.IgnoreAspectRatio,
                                Qt.SmoothTransformation)
            look = small.scaled(src.size(), Qt.IgnoreAspectRatio, Qt.FastTransformation)
        p.drawImage(QRectF(src).translated(f.left(), f.top()).topLeft(), look)

    # ---- mouse (tool on)
    def _hit(self, pt):
        for i in reversed(range(len(self.boxes))):
            r = self._box_rect(self.boxes[i])
            if QRectF(r.right() - self.HANDLE, r.bottom() - self.HANDLE, 2 * self.HANDLE, 2 * self.HANDLE).contains(pt):
                return "resize", i
            if r.contains(pt):
                return "move", i
        return None, None

    def _crop_hit(self, pt):
        if not self.crop:
            return None
        r = self._box_rect(self.crop)
        for name, (cx, cy) in (("crop_tl", (r.left(), r.top())), ("crop_tr", (r.right(), r.top())),
                               ("crop_bl", (r.left(), r.bottom())), ("crop_br", (r.right(), r.bottom()))):
            if abs(pt.x() - cx) <= self.HANDLE and abs(pt.y() - cy) <= self.HANDLE:
                return name
        return "crop_move" if r.contains(pt) else None

    def _shape_hit(self, pt):
        f = self.frame_rect()
        x, y = pt.x() - f.left(), pt.y() - f.top()
        shown = set(id(s) for s in self._shown_shapes())
        for i in reversed(range(len(self.shapes))):
            s = self.shapes[i]
            if id(s) in shown and annotate.hit(s, x, y, int(f.width()), int(f.height())):
                return i
        return None

    def _press_extra(self, pt) -> bool:
        """1.12: a press for the crop tool or a drawing tool; True when taken."""
        if self.crop_edit:
            kind = self._crop_hit(pt)
            fx, fy = self._to_frac(pt)
            if kind is None:
                if not self.frame_rect().contains(pt):
                    return True
                self._drag = ("crop_new", (fx, fy), (fx, fy, 0.0, 0.0))
            else:
                self._drag = (kind, (fx, fy), tuple(self.crop))
            self.update()
            return True
        if self.shape_tool:
            if not self.frame_rect().contains(pt):
                return True
            fx, fy = self._to_frac(pt)
            i = self._shape_hit(pt)
            if i is not None:
                self.shape_sel = i
                self._drag = ("shape_move", (fx, fy), self.shapes[i])
                self.shape_picked.emit(i)
            elif self.shape_tool == "text":
                shape = annotate.Shape("text", [(fx, fy)], self.pen["colour"], self.pen["text_size"],
                                       self.pen["text"] or _("Text"))
                self._new_shape(shape)
            else:
                pts = [(fx, fy)] if self.shape_tool == "free" else [(fx, fy), (fx, fy)]
                self._drag = ("shape_new", (fx, fy), annotate.Shape(self.shape_tool, pts, self.pen["colour"],
                                                                    self.pen["size"]))
            self.update()
            return True
        return False

    def _new_shape(self, shape):
        if shape.t0 is None and shape.t1 is None:
            shape.t0, shape.t1 = self.new_times()
        self.shapes.append(shape)
        self.shape_sel = len(self.shapes) - 1
        self._layer = None
        self.update()
        self.shapes_changed.emit()
        self.shape_picked.emit(self.shape_sel)

    def _move_extra(self, pt) -> bool:
        if not self._drag or not (self._drag[0].startswith("crop") or self._drag[0].startswith("shape")):
            return False
        kind, (px, py), orig = self._drag
        fx, fy = self._to_frac(pt)
        if kind == "crop_new":
            self._drag = (kind, (px, py), self._crop_box_for(px, py, fx, fy))
        elif kind == "crop_move":
            x, y, w, h = orig
            self._drag = (kind, (px, py), imageedit.clamp_box((x + fx - px, y + fy - py, w, h), self.MIN_BOX))
        elif kind.startswith("crop_"):
            x, y, w, h = orig
            ax = x + w if kind in ("crop_tl", "crop_bl") else x           # the opposite corner stays
            ay = y + h if kind in ("crop_tl", "crop_tr") else y
            self._drag = (kind, (px, py), self._crop_box_for(ax, ay, fx, fy))
        elif kind == "shape_move":
            self.shapes[self.shape_sel] = orig.moved(fx - px, fy - py)
        elif kind == "shape_new":
            if orig.kind == "free":
                if math.dist(orig.pts[-1], (fx, fy)) > 0.003:
                    orig.pts.append((fx, fy))
            else:
                orig.pts[1] = (fx, fy)
            self._preview_new = orig
        self.update()
        return True

    def _release_extra(self) -> bool:
        if not self._drag or not (self._drag[0].startswith("crop") or self._drag[0].startswith("shape")):
            return False
        kind, _p, box = self._drag
        self._drag = None
        self._preview_new = None
        if kind.startswith("crop"):
            if box[2] >= self.MIN_BOX and box[3] >= self.MIN_BOX:
                self.crop = tuple(box)
                self.crop_changed.emit()
        elif kind == "shape_new":
            a = box.pts[0]
            far = max(math.dist(a, q) for q in box.pts) if len(box.pts) > 1 else 0.0
            if far > 0.01:
                self._new_shape(box)
        elif kind == "shape_move":
            self.shapes_changed.emit()
        self.update()
        return True

    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton or self._img is None:
            return
        if self._press_extra(e.position()):
            return
        if not self.editing:
            return
        pt = e.position()
        kind, i = self._hit(pt)
        if kind is None:
            if not self.frame_rect().contains(pt):
                return
            fx, fy = self._to_frac(pt)
            self.selected = None
            self._drag = ("new", (fx, fy), [fx, fy, 0.0, 0.0])
        else:
            self.selected = i
            self._drag = (kind, self._to_frac(pt), list(self.boxes[i]))
        self.update()

    def mouseMoveEvent(self, e):
        if self._move_extra(e.position()):
            return
        if not self.editing:
            return
        if self._drag is None:
            kind, _i = self._hit(e.position())
            self.setCursor(Qt.SizeFDiagCursor if kind == "resize" else Qt.SizeAllCursor if kind == "move"
                           else Qt.CrossCursor)
            return
        kind, (px, py), orig = self._drag
        fx, fy = self._to_frac(e.position())
        if kind == "new":
            x0, y0 = min(px, fx), min(py, fy)
            self._drag = (kind, (px, py), [x0, y0, abs(fx - px), abs(fy - py)])
        elif kind == "move":
            w, h = orig[2], orig[3]
            x = min(max(0.0, orig[0] + fx - px), 1.0 - w)
            y = min(max(0.0, orig[1] + fy - py), 1.0 - h)
            self.boxes[self.selected] = [x, y, w, h]
        else:
            w = min(max(self.MIN_BOX, orig[2] + fx - px), 1.0 - orig[0])
            h = min(max(self.MIN_BOX, orig[3] + fy - py), 1.0 - orig[1])
            self.boxes[self.selected] = [orig[0], orig[1], w, h]
        self.update()

    def mouseReleaseEvent(self, e):
        if self._release_extra():
            return
        if self._drag is None:
            return
        kind, _p, box = self._drag
        self._drag = None
        if kind == "new":
            if box[2] >= self.MIN_BOX and box[3] >= self.MIN_BOX:
                self.add_box(box)
            else:
                self.update()
            return
        self.update()
        self.boxes_changed.emit()


class LoadingScreen(QWidget):
    """1.8.3 (user's wish): a screen over the editor while the clip loads – the first picture and the strip of
    thumbnails come from ffmpeg threads and took a few seconds on long recordings, during which the window
    looked broken (black picture, empty strip). Shows the file name and a bar; ``finish()`` fades it away."""

    def __init__(self, parent, name: str, total: int):
        super().__init__(parent)
        self.total = max(1, total)
        self.done_n = 0
        self.finished = False
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("LoadingScreen { background: rgba(14, 15, 18, 215); }")
        outer = QVBoxLayout(self)
        outer.addStretch()
        row = QHBoxLayout()
        row.addStretch()
        card = QFrame()
        card.setProperty("class", "card")
        card.setMinimumWidth(380)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(22, 18, 22, 18)
        cl.setSpacing(8)
        self.title = QLabel(_("Clip wird geladen …"))
        self.title.setProperty("class", "kpi")
        cl.addWidget(self.title)
        self.name = QLabel(name)
        self.name.setProperty("class", "dim")
        self.name.setWordWrap(True)
        cl.addWidget(self.name)
        self.bar = QProgressBar()
        self.bar.setRange(0, self.total)
        self.bar.setValue(0)
        self.bar.setTextVisible(False)
        cl.addWidget(self.bar)
        self.detail = QLabel("")
        self.detail.setProperty("class", "dim")
        self.detail.setWordWrap(True)
        cl.addWidget(self.detail)
        row.addWidget(card)
        row.addStretch()
        outer.addLayout(row)
        outer.addStretch()
        self.progress(0, _("Vorschaubild und Zeitleiste kommen aus der Aufnahme."))

    def progress(self, n: int, text: str):
        self.done_n = min(self.total, n)
        self.bar.setValue(self.done_n)
        self.detail.setText(text)

    def finish(self, late: bool = False):
        """Done (or given up): the screen goes away; ``late`` = the timeout, not completion."""
        if self.finished:
            return
        self.finished = True
        self.hide()
        if late:
            self.detail.setText(_("Lädt länger als erwartet – das Fenster ist trotzdem bedienbar."))


class ClipWindow(QWidget):
    """One editor per recording. ``on_saved(path)`` / ``on_setting(key, value)`` / ``log(text, kind)`` come from
    the App; ``mode``/``sound`` are the remembered settings."""

    def __init__(self, path: str, marks: list, clips_dir: str, mode: str = "copy", sound: bool = True,
                 on_saved=None, on_setting=None, log=None, dark=True, qss: str = "", title: str = "",
                 target_mb: int = clipedit.DEFAULT_TARGET_MB, censor_on: bool = False, censor_style: str = "pixel",
                 censor_boxes=(), mix_on=None, mix_vol=None, compact=False, parent=None, on_expand=None, sources=None):
        # 1.8.8: compact = the preview beside the recordings table (no window of its own, no censor card, sound
        # sources only on/off, start/end in the clip card); "Grosser Editor" (on_expand) opens the full window
        super().__init__(parent, Qt.Widget if compact else Qt.Window)
        self.compact, self.on_expand = bool(compact), on_expand
        self.path, self.marks, self.clips_dir = path, sorted(float(m) for m in marks or ()), clips_dir
        self.on_saved, self.on_setting, self.log = on_saved, on_setting, (log or (lambda text, kind="System": None))
        self.saved_seconds = {}           # 1.8.13: out path -> length of the clip (the clips list shows it)
        self.dark = dark
        self.info = clipedit.probe(path)
        self.ffmpeg = clipedit.ffmpeg_exe()
        self.bridge = _Bridge()
        self._pump = QTimer(self)             # 1.8.66: hands the threads' results to the window (GUI thread)
        self._pump.setInterval(PUMP_MS)
        self._pump.timeout.connect(self._drain)
        self._pump.start()
        self.player = None
        self.playing = False
        self._wav = None
        self._want = None                   # latest scrub moment asked for: (t, quick first look?)
        self._first_look = True             # 1.8.3: the first picture comes as a key frame at once, exact after
        self._scrub_lock = threading.Condition()
        self._closed = False
        self._target_mb = int(target_mb) if target_mb in clipedit.TARGETS_MB else clipedit.DEFAULT_TARGET_MB
        self._last_out = None               # 1.6.1: the clip saved last (Explorer button)
        self._play_to = None                # 1.6.1: "Clip ansehen" plays start..end, then back to the start
        self._censor_on, self._censor_style = bool(censor_on), censor_style        # 1.7.2: remembered boxes
        self._censor_boxes = [list(b) for b in (censor_boxes or ()) if len(b) == 4]
        self._mix_on = {k: bool((mix_on or {}).get(k, True)) for k in obsrec.SOURCES}     # 1.8.6: sound mix
        self._mix_vol = {k: int((mix_vol or {}).get(k, 100) or 0) for k in obsrec.SOURCES}
        self._sources = obsrec.track_sources(self.info.audio_tracks)
        self._silent = set()                # 1.8.18: sources whose own track holds nothing in this recording
        # 1.8.23: the sources OBS had on their own track when the round was recorded (None = not known: older
        # recordings) – a silent track of a source that was not there says "keine Quelle", not "still"
        self._recorded = None if sources is None else set(sources)
        self._absent = set()
        self._parts = []                    # 1.12: [clipedit.Part] kept so far (empty: the start/end range alone)
        self._range_speed = 1.0             # tempo of the start/end range while it is no part of its own
        self.setObjectName("page")
        self.setWindowTitle(title or _("Clip bearbeiten – {name}", name=os.path.basename(path)))
        if qss:
            self.setStyleSheet(qss)
        self._build(mode, sound)
        if not self.compact:
            self.resize(1180, 900)
            self.setMinimumSize(800, 680)
        self.setFocusPolicy(Qt.StrongFocus)
        self.loading = None                 # 1.8.3: LoadingScreen until picture + strip are there
        self._load_state = {"frame": False, "strip": False, "thumbs": 0}
        if not self.info.ok or not self.ffmpeg:
            self.status.setText(_("Datei nicht lesbar oder ffmpeg fehlt – keine Vorschau."))
            self.save_btn.setEnabled(False)
            return
        self.loading = LoadingScreen(self, os.path.basename(path), self.timeline.n_thumbs + 1)
        self.loading.setGeometry(self.rect())
        self.loading.raise_()
        QTimer.singleShot(LOAD_TIMEOUT_MS, lambda: self.loading is not None and self.loading.finish(late=True))
        self.timeline.set_duration(self.info.duration)
        self.timeline.marks = self.marks
        self.timeline.set_range(0.0, self.info.duration)
        first = self.marks[0] if self.marks else 0.0
        if self.marks:                                        # a mark: the clip starts 20 s before it, ends 10 s after
            self.timeline.set_range(max(0.0, first - 20), min(self.info.duration, first + 10))
        self._show_range()
        self._start_threads()
        self.goto(self.timeline.start)

    # ---- building
    def _build(self, mode, sound):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(10)
        self.preview = PreviewView(self.dark)
        self.preview.boxes_changed.connect(self._boxes_changed)
        if self.compact:                                  # beside the table: the whole editor fits a screen
            self.preview.setMinimumSize(320, 180)
            self.preview.setMaximumHeight(COMPACT_PREVIEW_H)
        else:                                             # 1.12: room for the tool tabs below
            self.preview.setMinimumSize(480, 270)
        lay.addWidget(self.preview, 1)
        self.timeline = Timeline(self.dark)
        self.timeline.seek.connect(self.goto)
        self.timeline.picked.connect(self._timeline_pick)
        self.timeline.changed.connect(self._show_range)
        lay.addWidget(self.timeline)

        # transport: position left, playback in the middle, start/end/mark right
        row = QHBoxLayout()
        self.pos_label = QLabel("")
        self.pos_label.setProperty("class", "dim")
        self.pos_label.setMinimumWidth(150)
        row.addWidget(self.pos_label)
        row.addStretch()
        self.b_back5 = self._btn(row, "−5 s", lambda: self.step(-STEP_BIG), _("5 Sekunden zurück (Shift+←)"))
        self.b_back1 = self._btn(row, "−1 s", lambda: self.step(-STEP_SMALL), _("1 Sekunde zurück (←)"))
        self.play_btn = self._btn(row, _("▶ Abspielen"), self.toggle_play, _("Abspielen / Pause (Leertaste)"))
        self.play_btn.setObjectName("primary")
        self.play_btn.setMinimumWidth(120)
        self.b_fwd1 = self._btn(row, "+1 s", lambda: self.step(STEP_SMALL), _("1 Sekunde vor (→)"))
        self.b_fwd5 = self._btn(row, "+5 s", lambda: self.step(STEP_BIG), _("5 Sekunden vor (Shift+→)"))
        row.addStretch()
        if self.compact:                                  # narrow: ±1 s by keys only, start/end in the clip card
            self.b_back1.hide()
            self.b_fwd1.hide()
            self.pos_label.setMinimumWidth(0)
        else:
            self._range_buttons(row)
        lay.addLayout(row)

        # two cards: the clip (range, size, "Clip ansehen") and the censor boxes (1.7.2)
        cards = QHBoxLayout()
        cards.setSpacing(10)
        clip_card, cl = self._card(_("Clip"))
        self.range_label = QLabel("")
        self.range_label.setProperty("class", "big")
        cl.addWidget(self.range_label)
        self.size_label = QLabel("")
        self.size_label.setProperty("class", "dim")
        self.size_label.setWordWrap(True)
        cl.addWidget(self.size_label)
        cl.addStretch()
        wr = QHBoxLayout()
        self.watch_btn = self._btn(wr, _("▶ Clip ansehen"), self.watch_clip,
                                   _("Spielt genau den Ausschnitt ab und springt danach an seinen Anfang zurück."))
        if self.compact:
            self._range_buttons(wr)
        wr.addStretch()
        cl.addLayout(wr)
        cards.addWidget(clip_card, 1)

        censor_card, zl = self._card(_("Zensieren"))
        zr = QHBoxLayout()
        self.censor_box = QCheckBox(_("Beim Speichern anwenden"))
        self.censor_box.setChecked(self._censor_on)
        self.censor_box.setToolTip(_("Die Kästen werden im gespeicherten Clip unkenntlich gemacht (dafür wird das "
                                     "Bild neu kodiert, auch im Format „Schnell“)."))
        self.censor_box.toggled.connect(self._censor_toggled)
        zr.addWidget(self.censor_box)
        self.style_box = guard_wheel(QComboBox())
        for key in clipedit.CENSOR_STYLES:
            self.style_box.addItem(_(CENSOR_LABELS[key]), key)
        self.style_box.setCurrentIndex(max(0, list(clipedit.CENSOR_STYLES).index(self._censor_style)
                                           if self._censor_style in clipedit.CENSOR_STYLES else 0))
        self.style_box.currentIndexChanged.connect(self._censor_style_changed)
        zr.addWidget(self.style_box)
        zr.addStretch()
        zl.addLayout(zr)
        zb = QHBoxLayout()
        self.tool_btn = self._btn(zb, _("Kasten zeichnen"), self._tool_toggled,
                                  _("Im Bild einen Bereich aufziehen; Kästen lassen sich verschieben und an der "
                                    "Ecke rechts unten vergrössern. Nochmal drücken beendet das Werkzeug."))
        self.tool_btn.setCheckable(True)
        self.tool_btn.setProperty("class", "seg")       # checked = accent, like Original/Dunkel on the Maps page
        self.names_btn = self._btn(zb, _("Namen links unten"), self._add_names_box,
                                   _("Setzt einen Kasten dorthin, wo DBD die Namen der Survivor zeigt (links unten "
                                     "im Spielbild) – bei Bedarf verschieben."))
        self.remove_btn = self._btn(zb, _("Kasten entfernen"), self._remove_box,
                                    _("Entfernt den markierten Kasten (Taste Entf)."))
        self.clear_btn = self._btn(zb, _("Alle entfernen"), self._clear_boxes, "")
        zb.addStretch()
        zl.addLayout(zb)
        self.censor_hint = QLabel("")
        self.censor_hint.setProperty("class", "dim")
        self.censor_hint.setWordWrap(True)
        zl.addWidget(self.censor_hint)
        zl.addStretch()
        if self.compact:                                  # censor boxes and the 1.12 tools: in the full editor
            censor_card.setVisible(False)
            cards.addWidget(censor_card, 1)
            lay.addLayout(cards)
        else:
            # 1.12 (user: "Bearbeitungstool top machen mit allen Funktionen"): one tab per tool below the timeline –
            # the clip, its parts (each with a tempo), the picture (crop, fades), drawings, censoring
            self.tools = QTabWidget()
            self.tools.setObjectName("cliptools")
            cards.removeWidget(clip_card)
            self.tools.addTab(clip_card, _("Clip"))
            self.tools.addTab(self._parts_card(), _("Abschnitte"))
            self.tools.addTab(self._picture_card(), _("Bild"))
            self.tools.addTab(self._draw_card(), _("Zeichnen"))
            self.tools.addTab(censor_card, _("Zensieren"))
            self.tools.currentChanged.connect(self._tool_tab_changed)
            self.tools.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
            lay.addWidget(self.tools)

        # export: name, format, target size, sound; save / show / folder
        export_card, el = self._card(_("Speichern"))
        row2 = QHBoxLayout()
        row2.addWidget(QLabel(_("Name")))
        self.name_edit = QLineEdit()
        row2.addWidget(self.name_edit, 1)
        if self.compact:                                  # narrow: the format on a line of its own
            el.addLayout(row2)
            row2 = QHBoxLayout()
        row2.addWidget(QLabel(_("Format")))
        self.mode_box = guard_wheel(QComboBox())
        self.mode_box.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        for key in clipedit.MODES:
            self.mode_box.addItem(_(MODE_LABELS[key]), key)
            self.mode_box.setItemData(self.mode_box.count() - 1, _(MODE_TIPS[key]), Qt.ToolTipRole)
        self.mode_box.setCurrentIndex(max(0, list(clipedit.MODES).index(mode) if mode in clipedit.MODES else 0))
        self.mode_box.currentIndexChanged.connect(self._mode_changed)
        row2.addWidget(self.mode_box)
        self.target_box = guard_wheel(QComboBox())
        for mb in clipedit.TARGETS_MB:
            self.target_box.addItem(_("≤ {n} MB", n=mb), mb)
        self.target_box.setCurrentIndex(list(clipedit.TARGETS_MB).index(self._target_mb))
        self.target_box.setToolTip(_("Discord: ohne Nitro 10 MB, Nitro Basic 50 MB, Nitro 500 MB."))
        self.target_box.currentIndexChanged.connect(self._target_changed)
        row2.addWidget(self.target_box)
        self.gif_box = guard_wheel(QComboBox())                                     # 1.12: GIF height
        for gh in clipedit.GIF_HEIGHTS:
            self.gif_box.addItem(f"{gh}p", gh)
        self.gif_box.setCurrentIndex(list(clipedit.GIF_HEIGHTS).index(clipedit.DEFAULT_GIF_H))
        self.gif_box.setToolTip(_("Höhe des GIFs – kleiner = kleinere Datei (Discord, Chats)."))
        self.gif_box.currentIndexChanged.connect(lambda _i: self._show_size())
        row2.addWidget(self.gif_box)
        self.sound_box = QCheckBox(_("Ton"))
        self.sound_box.setChecked(bool(sound))
        self.sound_box.setToolTip(_("Beim Abspielen den Ton der Aufnahme mitlaufen lassen (Windows)."))
        self.sound_box.toggled.connect(lambda v: self._setting("clip_sound", bool(v)))
        row2.addWidget(self.sound_box)
        if self.compact:
            row2.addStretch()
        el.addLayout(row2)
        el.addLayout(self._mix_row())                                               # 1.8.6: the sound mix
        row3 = QHBoxLayout()
        self.save_btn = self._btn(row3, _("Clip speichern"), self.save, _("Schreibt den Ausschnitt als MP4 in den Ordner „Clips“ neben den Aufnahmen."))
        self.save_btn.setObjectName("primary")
        self.show_btn = self._btn(row3, _("Im Explorer zeigen"), self._show_saved, _("Zeigt den zuletzt gespeicherten Clip im Explorer."))
        self.show_btn.setEnabled(False)
        self.open_btn = self._btn(row3, _("Clips-Ordner öffnen"), self._open_clips, _("Öffnet den Ordner „Clips“ im Explorer."))
        self.expand_btn = None
        if self.compact:
            self.open_btn.hide()
            self.expand_btn = self._btn(row3, _("Grosser Editor …"), self._expand,
                                        _("Öffnet den Clip im eigenen Fenster – mit Zensieren, Lautstärke je Tonquelle "
                                          "und allen Tasten."))
        self.status = QLabel("")
        self.status.setProperty("class", "dim")
        self.status.setWordWrap(True)
        row3.addWidget(self.status, 1)
        el.addLayout(row3)
        lay.addWidget(export_card)
        hint = QLabel(_(KEY_HINT))
        hint.setProperty("class", "dim")
        hint.setWordWrap(True)
        lay.addWidget(hint)
        hint.setVisible(not self.compact)
        self.preview.set_boxes(self._censor_boxes)
        self.preview.set_look(self._censor_on, self.style_box.currentData() or "pixel")
        self._censor_hint()
        self._mode_changed(self.mode_box.currentIndex(), save=False)

    def _range_buttons(self, row):
        self._btn(row, _("Start setzen"), self.set_start, _("Der Clip beginnt am Abspielkopf (Taste I)."))
        self._btn(row, _("Ende setzen"), self.set_end, _("Der Clip endet am Abspielkopf (Taste O)."))
        self.mark_btn = self._btn(row, _("Zur Marke ▸"), self.next_mark, _("Springt zur nächsten F8-Marke (Taste M)."))
        self.mark_btn.setEnabled(bool(self.marks))

    def _expand(self):
        """1.8.8: compact preview → the full editor (same range and position); this one stops playing."""
        if self.playing:
            self._play_to = None
            self._stop_player()
        if self.on_expand is not None:
            self.on_expand(self.timeline.start, self.timeline.end, self.timeline.pos)

    def stop(self):
        """1.8.8: stop playback (the recordings tab was left)."""
        if self.playing:
            self._play_to = None
            self._stop_player()

    @staticmethod
    def _card(title):
        """A card like the main window's, with a small heading; returns (frame, its layout)."""
        card = QFrame()
        card.setProperty("class", "card")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(14, 10, 14, 12)
        lay.setSpacing(6)
        head = QLabel(title.upper())
        head.setProperty("class", "sub")
        lay.addWidget(head)
        return card, lay

    # ---- 1.12: parts, picture, drawings
    def _combo(self, row, items, current, tip, slot):
        """A choice box of (data, label) with ``current`` picked (no mouse wheel, see guard_wheel)."""
        box = guard_wheel(QComboBox())
        for data, label in items:
            box.addItem(label, data)
        idx = next((i for i, (d, _l) in enumerate(items) if d == current), 0)
        box.setCurrentIndex(idx)
        box.setToolTip(tip)
        box.currentIndexChanged.connect(slot)
        row.addWidget(box)
        return box

    def _parts_card(self):
        card, cl = self._card(_("Abschnitte"))
        top = QHBoxLayout()
        self.part_list = QListWidget()
        self.part_list.setObjectName("parts")
        self.part_list.setMaximumHeight(110)
        self.part_list.setFocusPolicy(Qt.NoFocus)
        self.part_list.currentRowChanged.connect(self._part_picked)
        top.addWidget(self.part_list, 1)
        side = QVBoxLayout()
        self.part_add_btn = self._btn(side, _("+ Abschnitt"), self.add_part,
                                      _("Nimmt den Bereich zwischen Start und Ende als Abschnitt auf (Taste A). Alle "
                                        "Abschnitte werden nacheinander zu einem Clip zusammengefügt."))
        self.part_del_btn = self._btn(side, _("Abschnitt entfernen"), self.remove_part,
                                      _("Entfernt den markierten Abschnitt."))
        self.part_clear_btn = self._btn(side, _("Alle Abschnitte entfernen"), self.clear_parts,
                                        _("Entfernt alle Abschnitte – gespeichert wird dann wieder der Bereich "
                                          "zwischen Start und Ende."))
        side.addStretch()
        top.addLayout(side)
        cl.addLayout(top)
        tr = QHBoxLayout()
        tr.addWidget(QLabel(_("Tempo")))
        self.speed_box = self._combo(tr, [(v, _(SPEED_LABELS[v]) if v == 1.0 else SPEED_LABELS[v])
                                          for v in clipedit.SPEEDS], 1.0,
                                     _("Zeitlupe oder Zeitraffer für den markierten Abschnitt (ohne Abschnitte: für "
                                       "den Bereich zwischen Start und Ende). Der Ton läuft mit."), self._speed_picked)
        tr.addStretch()
        cl.addLayout(tr)
        self.parts_hint = QLabel("")
        self.parts_hint.setProperty("class", "dim")
        self.parts_hint.setWordWrap(True)
        cl.addWidget(self.parts_hint)
        cl.addStretch()
        self._parts_show()
        return card

    def _picture_card(self):
        card, cl = self._card(_("Bild"))
        cr = QHBoxLayout()
        cr.addWidget(QLabel(_("Ausschnitt")))
        self.crop_box = self._combo(cr, [(k, _(v) if k in ("none", "free", "9:16") else v)
                                         for k, v in CROP_LABELS.items()], "none",
                                    _("Schneidet einen Bereich aus dem Bild – 9:16 für YouTube Shorts und TikTok, 1:1 "
                                      "für Instagram. Den Rahmen in der Vorschau verschieben und an den Ecken ziehen."),
                                    self._crop_picked)
        self.crop_btn = self._btn(cr, _("Rahmen bearbeiten"), self._crop_tool,
                                  _("Rahmen in der Vorschau verschieben oder an den Ecken grösser/kleiner ziehen. "
                                    "Nochmal drücken beendet das Werkzeug."))
        self.crop_btn.setCheckable(True)
        self.crop_btn.setProperty("class", "seg")
        cr.addStretch()
        cl.addLayout(cr)
        fr = QHBoxLayout()
        fades = [(v, _("aus") if v == 0 else f"{v:g} s") for v in clipedit.FADES]
        fr.addWidget(QLabel(_("Einblenden")))
        self.fade_in_box = self._combo(fr, fades, 0.0, _("Der Clip beginnt aus Schwarz und mit leisem Ton."),
                                       lambda _i: self._show_size())
        fr.addWidget(QLabel(_("Ausblenden")))
        self.fade_out_box = self._combo(fr, fades, 0.0, _("Der Clip endet in Schwarz, der Ton wird leiser."),
                                        lambda _i: self._show_size())
        fr.addStretch()
        cl.addLayout(fr)
        hint = QLabel(_("Ausschnitt, Tempo, Blenden und Zeichnungen brauchen ein neu kodiertes Bild – „Schnell“ "
                        "speichert dann wie „Genau“."))
        hint.setProperty("class", "dim")
        hint.setWordWrap(True)
        cl.addWidget(hint)
        cl.addStretch()
        self.preview.crop_changed.connect(self._show_size)
        return card

    def _draw_card(self):
        card, cl = self._card(_("Zeichnen"))
        tr = QHBoxLayout()
        self.draw_group = QButtonGroup(self)
        self.draw_group.setExclusive(False)
        self.draw_btns = {}
        for kind, label in DRAW_TOOLS:
            b = self._btn(tr, _(label), lambda _c=False, k=kind: self._draw_tool(k),
                          _("Im Bild ziehen (Text: klicken). Eine Zeichnung anklicken markiert sie, ziehen verschiebt "
                            "sie, Entf löscht sie."))
            b.setCheckable(True)
            b.setProperty("class", "seg")
            self.draw_btns[kind] = b
        tr.addStretch()
        cl.addLayout(tr)
        pr = QHBoxLayout()
        self.colour_btns = {}
        for colour in annotate.COLOURS:
            b = QPushButton("")
            b.setFixedSize(22, 22)
            b.setFocusPolicy(Qt.NoFocus)
            b.setCheckable(True)
            b.setToolTip(_("Farbe"))
            b.setStyleSheet(f"QPushButton {{ background: {colour}; border: 2px solid #555; border-radius: 4px; }}"
                            f"QPushButton:checked {{ border: 2px solid #ffffff; }}")
            b.clicked.connect(lambda _c=False, c=colour: self._draw_colour(c))
            pr.addWidget(b)
            self.colour_btns[colour] = b
        self.colour_btns[annotate.COLOURS[0]].setChecked(True)
        self.draw_size_box = self._combo(pr, list(enumerate(_(x) for x in SIZE_LABELS)), 1,
                                         _("Strichstärke bzw. Textgrösse."), self._draw_size)
        self.draw_when_box = self._combo(pr, [(v, _(lbl)) for v, lbl in SHOW_FOR], 3.0,
                                         _("Wie lange die Zeichnung im Clip zu sehen ist – ab der Stelle des "
                                           "Abspielkopfs. Gilt für neue und für die markierte Zeichnung."),
                                         self._draw_when)
        pr.addStretch()
        cl.addLayout(pr)
        xr = QHBoxLayout()
        self.draw_text = QLineEdit()
        self.draw_text.setPlaceholderText(_("Text für das Text-Werkzeug"))
        self.draw_text.textEdited.connect(self._draw_text_edited)
        xr.addWidget(self.draw_text, 1)
        self.draw_del_btn = self._btn(xr, _("Zeichnung entfernen"), self._draw_remove,
                                      _("Entfernt die markierte Zeichnung (Entf)."))
        self.draw_clear_btn = self._btn(xr, _("Alle Zeichnungen entfernen"), self._draw_clear, "")
        cl.addLayout(xr)
        cl.addStretch()
        self.preview.shapes_changed.connect(self._show_size)
        self.preview.shape_picked.connect(self._draw_picked)
        self.preview.new_times = self._times_from_here
        return card

    def _tool_tab_changed(self, _i):
        """Leaving a tab ends its tool: the preview takes clicks only for the tab on display."""
        page = self.tools.currentWidget()
        if self.crop_btn.isChecked() and page is not self.tools.widget(2):
            self.crop_btn.setChecked(False)
            self.preview.set_crop_edit(False)
        if page is not self.tools.widget(3):
            for b in self.draw_btns.values():
                b.setChecked(False)
            self.preview.set_shape_tool(None)
        if self.tool_btn.isChecked() and page is not self.tools.widget(4):
            self.tool_btn.setChecked(False)
            self.preview.set_editing(False)

    # parts
    def add_part(self):
        tl = self.timeline
        if tl.end - tl.start < 0.1:
            return
        self._parts = clipedit.clean_parts(self._parts + [clipedit.Part(tl.start, tl.end, self._range_speed)],
                                           self.info.duration)
        self._parts_show()
        self._show_size()

    def remove_part(self):
        row = self.part_list.currentRow()
        if 0 <= row < len(self._parts):
            del self._parts[row]
            self._parts_show()
            self._show_size()

    def clear_parts(self):
        self._parts = []
        self._parts_show()
        self._show_size()

    def _part_picked(self, row):
        if 0 <= row < len(self._parts):
            p = self._parts[row]
            self.timeline.set_range(p.start, p.end)
            self._show_range()
            self.goto(p.start)
            self._select_speed(p.speed)
        self.part_del_btn.setEnabled(0 <= row < len(self._parts))

    def _select_speed(self, speed):
        i = self.speed_box.findData(speed)
        if i >= 0 and i != self.speed_box.currentIndex():
            self.speed_box.blockSignals(True)
            self.speed_box.setCurrentIndex(i)
            self.speed_box.blockSignals(False)

    def _speed_picked(self, _i):
        speed = float(self.speed_box.currentData() or 1.0)
        row = self.part_list.currentRow() if hasattr(self, "part_list") else -1
        if 0 <= row < len(self._parts):
            self._parts[row].speed = speed
            self._parts_show(keep=row)
        else:
            self._range_speed = speed
        self._show_size()

    def _parts_show(self, keep=None):
        if not hasattr(self, "part_list"):
            return
        self.part_list.blockSignals(True)
        self.part_list.clear()
        for i, p in enumerate(self._parts):
            tempo = "" if abs(p.speed - 1.0) < 1e-6 else f"  {SPEED_LABELS.get(p.speed, f'×{p.speed:g}')}"
            self.part_list.addItem(f"{i + 1}.  {clipedit.fmt_pos(p.start)} – {clipedit.fmt_pos(p.end)}"
                                   f"  ({p.end - p.start:.1f} s){tempo}")
        if keep is not None and keep < len(self._parts):
            self.part_list.setCurrentRow(keep)
        self.part_list.blockSignals(False)
        self.part_del_btn.setEnabled(keep is not None and keep < len(self._parts))
        self.part_clear_btn.setEnabled(bool(self._parts))
        self.timeline.parts = [(p.start, p.end) for p in self._parts]
        self.timeline.update()
        if self._parts:
            self.parts_hint.setText(_("Gespeichert werden die {n} Abschnitte nacheinander ({length} s). Einen "
                                      "Abschnitt anklicken zeigt ihn auf der Zeitleiste.", n=len(self._parts),
                                      length=f"{self.edit_plan().seconds():.1f}"))
        else:
            self.parts_hint.setText(_("Noch keine Abschnitte: gespeichert wird der Bereich zwischen Start und Ende. "
                                      "Für mehrere Szenen aus einer Runde: Bereich wählen, „+ Abschnitt“, nächsten "
                                      "Bereich wählen …"))

    # picture
    def _crop_picked(self, _i):
        key = self.crop_box.currentData()
        ratio = dict(clipedit.ASPECTS).get(key)
        if key == "none":
            self.preview.set_crop(None)
            self.crop_btn.setChecked(False)
            self.preview.set_crop_edit(False)
        else:
            base = self.preview.crop or (0.0, 0.0, 1.0, 1.0)
            box = imageedit.aspect_box(base if key == "free" else (0.0, 0.0, 1.0, 1.0), ratio,
                                       (self.info.width or 16, self.info.height or 9))
            self.preview.set_crop(box, ratio)
            if not self.crop_btn.isChecked():
                self.crop_btn.setChecked(True)
                self._crop_tool()
        self._show_size()

    def _crop_tool(self):
        on = self.crop_btn.isChecked()
        if on and self.crop_box.currentData() == "none":
            self.crop_box.setCurrentIndex(self.crop_box.findData("free"))      # draws a full box, tool on
            return
        self.preview.set_crop_edit(on)

    # drawings
    def _draw_tool(self, kind):
        on = self.draw_btns[kind].isChecked()
        for k, b in self.draw_btns.items():
            if k != kind:
                b.setChecked(False)
        self.preview.set_shape_tool(kind if on else None)
        self.preview.pen["text"] = self.draw_text.text()

    def _draw_colour(self, colour):
        for c, b in self.colour_btns.items():
            b.setChecked(c == colour)
        self.preview.pen["colour"] = colour
        sel = self.preview.selected_shape()
        if sel is not None:
            sel.colour = colour
            self.preview.replace_selected_shape(sel)

    def _draw_size(self, _i):
        i = int(self.draw_size_box.currentData() or 0)
        self.preview.pen["size"] = annotate.SIZES[i]
        self.preview.pen["text_size"] = annotate.TEXT_SIZES[i]
        sel = self.preview.selected_shape()
        if sel is not None:
            sel.size = annotate.TEXT_SIZES[i] if sel.kind == "text" else annotate.SIZES[i]
            self.preview.replace_selected_shape(sel)

    def _times_from_here(self):
        dur = self.draw_when_box.currentData()
        t = self.timeline.pos
        return (None, None) if dur is None else (t, min(self.info.duration or t + dur, t + float(dur)))

    def _draw_when(self, _i):
        sel = self.preview.selected_shape()
        if sel is not None:
            sel.t0, sel.t1 = self._times_from_here()
            self.preview.replace_selected_shape(sel)

    def _draw_text_edited(self, text):
        self.preview.pen["text"] = text
        sel = self.preview.selected_shape()
        if sel is not None and sel.kind == "text":
            sel.text = text or " "
            self.preview.replace_selected_shape(sel)

    def _draw_picked(self, i):
        sel = self.preview.selected_shape()
        if sel is None:
            return
        if sel.kind == "text":
            self.draw_text.setText(sel.text)

    def _draw_remove(self):
        self.preview.remove_selected_shape()

    def _draw_clear(self):
        if self.preview.shapes:
            self.preview.set_shapes([])
            self.preview.shapes_changed.emit()

    def edit_plan(self) -> clipedit.Edit:
        """What will be saved: the parts (or the start/end range), crop, drawings, fades."""
        tl = self.timeline
        parts = list(self._parts) or [clipedit.Part(tl.start, tl.end, self._range_speed)]
        full = not self.compact and hasattr(self, "crop_box")
        crop = self.preview.crop if full and self.crop_box.currentData() != "none" else None
        shapes = [s for s in self.preview.shapes if s.kind != "text" or s.text.strip()] if full else []
        fi = float(self.fade_in_box.currentData() or 0) if full else 0.0
        fo = float(self.fade_out_box.currentData() or 0) if full else 0.0
        return clipedit.Edit([clipedit.Part(p.start, p.end, p.speed) for p in parts], crop, shapes, fi, fo)

    # ---- censor boxes (1.7.2)
    def _censor_toggled(self, on):
        self._censor_on = bool(on)
        self.preview.set_look(self._censor_on, self.style_box.currentData() or "pixel")
        self._setting("clip_censor_on", self._censor_on)
        self._censor_hint()
        self._show_size()

    def _censor_style_changed(self, _i):
        style = self.style_box.currentData() or "pixel"
        self.preview.set_look(self._censor_on, style)
        self._setting("clip_censor_style", style)

    def _tool_toggled(self):
        self.preview.set_editing(self.tool_btn.isChecked())
        self._censor_hint()

    def _add_names_box(self):
        self.preview.add_box(clipedit.names_box(self.info.width, self.info.height))
        if not self.censor_box.isChecked():
            self.censor_box.setChecked(True)

    def _remove_box(self):
        if not self.preview.remove_selected() and self.preview.boxes:
            self.preview.selected = len(self.preview.boxes) - 1
            self.preview.remove_selected()

    def _clear_boxes(self):
        self.preview.clear_boxes()

    def _boxes_changed(self):
        self._setting("clip_censor_boxes", [[round(v, 4) for v in b] for b in self.preview.boxes])
        self._censor_hint()
        self._show_size()

    def _censor_hint(self):
        n = len(self.preview.boxes)
        if not n:
            text = _("Noch kein Kasten. „Namen links unten“ setzt einen auf die Survivor-Namen, „Kasten zeichnen“ "
                     "lässt dich einen aufziehen.")
        elif self.preview.editing:
            text = _("{n} Kasten/Kästen – ziehen = verschieben, Ecke rechts unten = Grösse, Klick = markieren.", n=n)
        else:
            text = _("{n} Kasten/Kästen gemerkt – sie gelten auch für den nächsten Clip.", n=n)
        self.censor_hint.setText(text)
        self.remove_btn.setEnabled(n > 0)
        self.clear_btn.setEnabled(n > 0)

    def _censor_args(self) -> dict:
        if self._censor_on and self.preview.boxes:
            return {"censor": [tuple(b) for b in self.preview.boxes],
                    "censor_style": self.style_box.currentData() or "pixel"}
        return {}

    def _btn(self, row, text, slot, tip=""):
        b = QPushButton(text)
        b.setFocusPolicy(Qt.NoFocus)                      # the keys stay with the window
        b.clicked.connect(slot)
        if tip:
            b.setToolTip(tip)
        row.addWidget(b)
        return b

    # ---- 1.8.6: the sound mix (like Medal – each source on its own OBS track, on/off and a level each)
    def _mix_row(self):
        """The label and the sources in a row, the hint in a line of its own below them (1.12.2: beside them it
        squeezed the row into a column of single words next to the recordings table); with no sources to pick the
        hint stands beside the label (``_mix_fill`` moves it)."""
        lines = QVBoxLayout()
        lines.setSpacing(2)
        row = self._mix_top = QHBoxLayout()
        self.mix_label = QLabel(_("Ton im Clip"))
        row.addWidget(self.mix_label)
        self.mix_boxes, self.mix_sliders, self.mix_values = {}, {}, {}
        for key in obsrec.SOURCES:
            box = QCheckBox(_(SOURCE_LABELS[key]))
            box.setToolTip(_(SOURCE_TIPS[key]))
            sl = guard_wheel(QSlider(Qt.Horizontal))
            sl.setRange(0, MIX_MAX)
            sl.setFixedWidth(80)
            sl.setToolTip(_("Lautstärke dieser Quelle im Clip (100 % = wie aufgenommen)."))
            val = QLabel("")
            val.setProperty("class", "dim")
            val.setMinimumWidth(38)
            self.mix_boxes[key], self.mix_sliders[key], self.mix_values[key] = box, sl, val
            row.addWidget(box)
            row.addWidget(sl)
            row.addWidget(val)
            row.addSpacing(8)
        self.mix_hint = QLabel(_("Eine Tonspur – zum Mischen nimmt OBS mit Spur 1–4 auf (Einstellungen → Aufnahmen)."))
        self.mix_hint.setProperty("class", "dim")
        self.mix_hint.setWordWrap(True)
        row.addStretch()
        self._mix_below = QHBoxLayout()
        lines.addLayout(row)
        lines.addLayout(self._mix_below)
        self._mix_fill()
        for key in obsrec.SOURCES:
            self.mix_boxes[key].toggled.connect(self._mix_changed)
            self.mix_sliders[key].valueChanged.connect(lambda v, k=key: self._mix_slid(k))
            self.mix_sliders[key].sliderReleased.connect(self._mix_changed)
        return lines

    def _mix_place_hint(self):
        """No sources: the hint beside the label (before the row's stretch); else in the line below, indented to
        where the sources begin."""
        top, below = getattr(self, "_mix_top", None), getattr(self, "_mix_below", None)
        if top is None or below is None:
            return
        top.removeWidget(self.mix_hint)
        below.removeWidget(self.mix_hint)
        if self._sources:
            below.setContentsMargins(self.mix_label.sizeHint().width() + top.spacing(), 0, 0, 0)
            below.addWidget(self.mix_hint, 1)
        else:
            top.insertWidget(top.count() - 1, self.mix_hint, 1)

    def _mix_fill(self):
        """Controls for the sources the file has on their own tracks; none → only the hint. A source whose track
        is silent in the whole recording says so (1.8.18) – OBS recorded nothing there."""
        self.mix_hint.setVisible(not self._sources or bool(self._silent))
        self._mix_place_hint()
        if self._silent:
            names = ", ".join(_("{name} (Spur {n})", name=_(SOURCE_LABELS[k]), n=self._sources[k] + 1)
                              for k in obsrec.SOURCES if k in self._silent)
            self.mix_hint.setText(_("Still in dieser Aufnahme: {names} – OBS hat dort nichts aufgenommen. In OBS "
                                    "prüfen: Quelle in der Szene der Aufnahme, nicht stumm, Spur angehakt.",
                                    names=names))
        legacy = self._sources.get("discord") == obsrec.LEGACY
        for key in obsrec.SOURCES:
            box, sl, val = self.mix_boxes[key], self.mix_sliders[key], self.mix_values[key]
            have = key in self._sources
            for w in (box, sl, val):
                w.setVisible(bool(self._sources) and (w is box or not self.compact))   # compact: on/off only
                w.setEnabled(have)
            box.setChecked(have and self._mix_on[key])
            silent = key in self._silent
            if key in self._absent:                                # 1.8.23: nothing there to record
                box.setText(_("{name} – keine Quelle", name=_(SOURCE_LABELS[key])) if key == "other"
                            else _("{name} – in OBS aus", name=_(SOURCE_LABELS[key])))
                box.setToolTip(_(ABSENT_TIPS.get(key, ABSENT_TIPS["dbd"])))
            else:
                box.setText(_("{name} – still", name=_(SOURCE_LABELS[key])) if silent else _(SOURCE_LABELS[key]))
                box.setToolTip(_("Auf Spur {n} ist in der ganzen Aufnahme nichts zu hören.", n=self._sources[key] + 1)
                               if silent else _(SOURCE_TIPS[key]))
            sl.setValue(self._mix_vol[key] if have else 100)
            if legacy and key == "discord":                       # 1.8.5 file: Discord only on or off
                sl.setEnabled(False)
            val.setText(f"{sl.value()} %" if have else "")

    def _mix_slid(self, key):
        self.mix_values[key].setText(f"{self.mix_sliders[key].value()} %")
        if not self.mix_sliders[key].isSliderDown():              # keyboard / wheel: no release comes
            self._mix_changed()

    def mix(self):
        """{source: volume} for cut()/sound_wav() – None when the recording has no tracks to pick from."""
        if not self._sources:
            return None
        return {k: (self.mix_sliders[k].value() / 100.0 if self.mix_boxes[k].isChecked() else 0.0)
                for k in obsrec.SOURCES if k in self._sources}

    def _mix_changed(self, *_a):
        if not self._sources:
            return
        for key in obsrec.SOURCES:
            if key in self._sources:
                self._mix_on[key] = self.mix_boxes[key].isChecked()
                self._mix_vol[key] = self.mix_sliders[key].value()
        self._setting("clip_mix_on", dict(self._mix_on))
        self._setting("clip_mix_vol", dict(self._mix_vol))
        self._show_size()
        if self.playing and self.sound_box.isChecked() and os.name == "nt":   # hear the change at once
            back = self._play_to
            self._stop_player()
            self._play_to = back
            self.toggle_play()

    def _setting(self, key, value):
        if self.on_setting:
            self.on_setting(key, value)

    # ---- threads
    def _start_threads(self):
        b = self.bridge
        b.frame.connect(self._show_frame)
        b.played.connect(self._show_played)
        b.thumb.connect(self.timeline.set_thumb)
        b.thumb.connect(self._thumb_loaded)
        b.strip_done.connect(lambda: self._loaded("strip"))
        b.ended.connect(self._player_ended)
        b.saved.connect(self._saved)
        b.still.connect(self._still_saved)
        b.sound.connect(self._sound_ready)
        b.levels.connect(self._show_levels)
        threading.Thread(target=self._scrub_loop, name="clip-scrub", daemon=True).start()
        if any(i >= 0 for i in self._sources.values()):
            threading.Thread(target=self._level_loop, name="clip-levels", daemon=True).start()
        threading.Thread(target=self._thumb_loop, name="clip-thumbs", daemon=True).start()

    def _scrub_loop(self):
        while not self._closed:
            with self._scrub_lock:
                while self._want is None and not self._closed:
                    self._scrub_lock.wait(0.5)
                want, self._want = self._want, None
            if want is None:
                continue
            t, quick = want
            if quick:                                   # 1.8.3: the key frame at once (~40 ms), the exact frame after
                img = clipedit.frame_at(self.path, t, clipedit.PREVIEW_H, self.info, self.ffmpeg, keyframe=True)
                if img is not None and not self._closed:
                    self.bridge.frame.emit(t, img)
                with self._scrub_lock:
                    if self._want is not None:          # a newer wish meanwhile: that one, not this exact frame
                        continue
            img = clipedit.frame_at(self.path, t, clipedit.PREVIEW_H, self.info, self.ffmpeg)
            if img is not None and not self._closed:
                self.bridge.frame.emit(t, img)

    def _level_loop(self):
        levels = clipedit.track_levels(self.path, self.info.audio_tracks, self.ffmpeg)
        if levels and not self._closed:
            self.bridge.levels.emit(levels)

    def _show_levels(self, levels):
        """1.8.18: mark the sources whose own track is silent (a 1.8.5 file's Discord has no track of its own)."""
        silent = {k for k, i in self._sources.items()
                  if i >= 0 and levels.get(i) is not None and levels[i] <= clipedit.SILENT_DB}
        self._absent = {k for k in silent if self._recorded is not None and k not in self._recorded}
        self._silent = silent - self._absent
        if self._silent:
            log.info("Clip: stille Spuren in %s: %s", os.path.basename(self.path), ", ".join(sorted(self._silent)))
        self._mix_fill()

    def _thumb_loop(self):
        times = clipedit.thumb_times(self.info.duration, self.timeline.n_thumbs)
        got = set()                                  # 1.7.1: one ffmpeg run for the whole strip (key frames only)
        for i, img in clipedit.thumb_strip(self.path, times, clipedit.THUMB_H, self.info, self.ffmpeg,
                                           stop=lambda: self._closed):
            got.add(i)
            self.bridge.thumb.emit(i, img)
        for i, t in enumerate(times):                # whatever the run did not deliver: the old way
            if self._closed:
                return
            if i in got:
                continue
            img = clipedit.frame_at(self.path, t, clipedit.THUMB_H, self.info, self.ffmpeg)
            if img is not None and not self._closed:
                self.bridge.thumb.emit(i, img)
        if not self._closed:
            self.bridge.strip_done.emit()

    # ---- loading screen (1.8.3)
    def _thumb_loaded(self, _i, _img):
        self._load_state["thumbs"] += 1
        self._loaded(None)

    def _loaded(self, what):
        """A piece arrived (the first picture, the whole strip); the screen shows the count and goes when all is in."""
        if what:
            self._load_state[what] = True
        if self.loading is None or self.loading.finished:
            return
        st = self._load_state
        n = min(self.timeline.n_thumbs, st["thumbs"]) + (1 if st["frame"] else 0)
        self.loading.progress(n, _("{n} von {total} Bildern", n=n, total=self.timeline.n_thumbs + 1))
        if st["frame"] and st["strip"]:
            self.loading.finish()

    def resizeEvent(self, e):
        if self.loading is not None:
            self.loading.setGeometry(self.rect())
        super().resizeEvent(e)

    # ---- position
    def goto(self, t: float):
        """The playhead to ``t``: stops a playback, asks the scrub thread for the picture."""
        if self.playing:
            self._stop_player()
        t = min(max(0.0, float(t)), self.info.duration or 0.0)
        self.timeline.set_position(t)
        self.preview.set_now(t)                         # 1.12: drawings show at their times
        self._show_pos()
        with self._scrub_lock:
            self._want = (t, self._first_look)
            self._first_look = False
            self._scrub_lock.notify()

    def step(self, seconds: float):
        self.goto(self.timeline.pos + seconds)

    def step_frame(self, n: int):
        self.goto(self.timeline.pos + n / max(1.0, self.info.fps))

    def set_start(self):
        self.timeline.set_range(self.timeline.pos, max(self.timeline.end, self.timeline.pos + 0.1))
        self._show_range()

    def set_end(self):
        self.timeline.set_range(min(self.timeline.start, self.timeline.pos - 0.1), self.timeline.pos)
        self._show_range()

    def next_mark(self):
        later = [m for m in self.marks if m > self.timeline.pos + 0.05]
        if later or self.marks:
            self.goto(later[0] if later else self.marks[0])

    def _show_pos(self):
        self.pos_label.setText(f"{clipedit.fmt_pos(self.timeline.pos)} / {clipedit.fmt_pos(self.info.duration)}")

    def _show_range(self):
        tl = self.timeline
        self.range_label.setText(_("Clip: {start} – {end} ({length} s)", start=clipedit.fmt_pos(tl.start),
                                   end=clipedit.fmt_pos(tl.end), length=f"{tl.end - tl.start:.1f}"))
        self._show_size()
        if not self.name_edit.isModified() or not self.name_edit.text():
            self.name_edit.setText(clipedit.clip_name(self.path, tl.start, tl.end))
            self.name_edit.setCursorPosition(0)                  # 1.12.2: the start of the name, not its cut end
            self.name_edit.setModified(False)

    def _show_size(self):
        """1.6.1: what the chosen format makes of the clip – for Discord the picture size and frame rate."""
        mode = self.mode_box.currentData() if hasattr(self, "mode_box") else "copy"
        edit = self.edit_plan()
        secs = edit.seconds()
        parts = []                                                 # 1.8.8: joined by " · ", no dot in front
        if len(edit.parts) > 1 or abs(edit.parts[0].speed - 1.0) > 1e-6:
            parts.append(_("{n} Abschnitt(e), {length} s", n=len(edit.parts), length=f"{secs:.1f}"))
        if mode == "gif":
            gh = int(self.gif_box.currentData() or clipedit.DEFAULT_GIF_H) if hasattr(self, "gif_box") else 0
            parts.append(_("GIF {h}p, {fps} Bilder/s, ohne Ton", h=gh, fps=clipedit.GIF_FPS))
        elif mode == "discord":
            kbps, h, fps = clipedit.discord_plan(secs, self._target_mb, self.info)
            parts.append(_("wird {h}p {fps} fps, ≈ {kbps} kbit/s, unter {mb} MB",
                           h=h, fps=f"{fps:g}", kbps=kbps, mb=self._target_mb))
        elif self.info.ok and getattr(self.info, "duration", 0) and mode != "gif":
            try:
                size = os.path.getsize(self.path) * secs / self.info.duration
            except OSError:
                size = 0
            if size:
                parts.append(_("etwa {mb} MB", mb=f"{max(1.0, size / 1024 ** 2):.0f}"))
        if self._censor_args() and mode == "copy":                 # 1.7.2: boxes need the picture re-encoded
            parts.append(_("mit Zensur neu kodiert (wie „Genau“)"))
        elif mode == "copy" and not edit.simple():                # 1.12: parts/tempo/crop/drawings/fades too
            parts.append(_("neu kodiert (wie „Genau“)"))
        if edit.crop and self.info.ok:
            w, h, _x, _y = clipedit.crop_px(edit.crop, self.info.width, self.info.height)
            parts.append(_("Ausschnitt {w}×{h}", w=w, h=h))
        if mode == "copy" and hasattr(self, "mix_boxes"):          # 1.8.6: a mix re-encodes only the sound
            flt, amap = obsrec.audio_graph(self.info.audio_tracks, self.mix())
            if flt or amap is None:
                parts.append(_("ohne Ton") if amap is None else _("Ton neu gemischt"))
        self.size_label.setText(" · ".join(parts))

    def _mode_changed(self, _i, save=True):
        mode = self.mode_box.currentData()
        self.target_box.setVisible(mode == "discord")
        self.gif_box.setVisible(mode == "gif")
        if save:
            self._setting("clip_mode", mode)
        self._show_size()

    def _target_changed(self, _i):
        self._target_mb = int(self.target_box.currentData() or clipedit.DEFAULT_TARGET_MB)
        self._setting("clip_target_mb", self._target_mb)
        self._show_size()

    def watch_clip(self):
        """1.6.1: play the clip as it will be saved – from its start to its end, then back to its start."""
        tl = self.timeline
        self.goto(tl.start)
        self._play_to = tl.start
        self.toggle_play()

    def _show_frame(self, t, img):
        if not self.playing:
            self._paint(img)
        self._loaded("frame")

    def _show_played(self, t, img):
        if self.playing:
            self.timeline.set_position(t)
            self.preview.set_now(t)
            self._show_pos()
            self._paint(img)

    def _paint(self, img):
        self.preview.set_frame(_qimage(img))

    # ---- playback
    def toggle_play(self):
        if self.playing:
            self._play_to = None
            self._stop_player()
            return
        start = self.timeline.pos
        end = self.timeline.end if start < self.timeline.end - 0.05 else self.info.duration
        self.playing = True
        self.play_btn.setText(_("⏸ Pause"))
        if self.sound_box.isChecked() and os.name == "nt":
            mix, n = self.mix(), self.info.audio_tracks
            threading.Thread(target=lambda: self.bridge.sound.emit(
                clipedit.sound_wav(self.path, start, end, self.ffmpeg, mix=mix, n_tracks=n), start),
                name="clip-sound", daemon=True).start()
        else:
            self._run_player(start, end)

    def _sound_ready(self, wav, start):
        if not self.playing or self.player is not None:
            if wav:
                self._drop_wav(wav)
            return
        self._wav = wav
        if wav:
            try:
                import winsound
                winsound.PlaySound(wav, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
            except Exception:                                   # no sound device: the picture still plays
                pass
        self._run_player(start, self.timeline.end if start < self.timeline.end - 0.05 else self.info.duration)

    def _run_player(self, start, end):
        b = self.bridge
        self.player = clipedit.FramePlayer(self.path, start, self.info, lambda t, img: b.played.emit(t, img),
                                           lambda: b.ended.emit(self.player), end=end, ffmpeg=self.ffmpeg)
        self.player.start()

    def _stop_player(self):
        self.playing = False
        self.play_btn.setText(_("▶ Abspielen"))
        pl, self.player = self.player, None
        if pl is not None:
            pl.stop()
        if os.name == "nt":
            try:
                import winsound
                winsound.PlaySound(None, winsound.SND_PURGE)
            except Exception:
                pass
        if self._wav:
            self._drop_wav(self._wav)
            self._wav = None

    @staticmethod
    def _drop_wav(path):
        try:
            os.remove(path)
        except OSError:
            pass

    def _player_ended(self, player):
        if player is self.player and self.playing:            # ran to the end (not stopped by us)
            self._stop_player()
            back, self._play_to = self._play_to, None
            self.goto(back if back is not None else self.timeline.pos)

    # ---- saving
    def save(self):
        tl = self.timeline
        name = clipedit.NAME_CHARS.sub("", self.name_edit.text()).strip() or clipedit.clip_name(self.path, tl.start, tl.end)
        mode = self.mode_box.currentData() or "copy"
        edit = self.edit_plan()                                   # 1.12: parts, tempo, crop, drawings, fades
        try:
            os.makedirs(self.clips_dir, exist_ok=True)
        except OSError as e:
            self.status.setText(_("Clips-Ordner nicht anlegbar: {error}", error=e))
            return
        out = clipedit.unique_path(self.clips_dir, name, ".gif" if mode == "gif" else ".mp4")
        self.save_btn.setEnabled(False)
        self.status.setText(_("Schreibe {file} …", file=os.path.basename(out)))
        self.saved_seconds[out] = round(edit.seconds(), 1)

        target, info, mix = self._target_mb, self.info, self.mix()
        censor = self._censor_args()
        gif_h = int(self.gif_box.currentData() or clipedit.DEFAULT_GIF_H)
        if mode != "copy" or censor or not edit.simple():
            self.status.setText(_("Kodiere {file} … (dauert etwas)", file=os.path.basename(out)))

        def work():
            ok, why = clipedit.export(self.path, edit, out, mode, self.ffmpeg, target_mb=target, info=info, mix=mix,
                                      gif_h=gif_h, **censor)
            self.bridge.saved.emit(ok, out, why)
        threading.Thread(target=work, name="clip-save", daemon=True).start()

    def _timeline_pick(self, ident, t):
        """1.8.10: the right-click menu of the strip."""
        tl = self.timeline
        if ident == "seek":
            self.goto(t)
        elif ident == "start" and t < tl.end - 0.1:
            tl.set_range(t, tl.end)
            self._show_range()
            self.goto(t)
        elif ident == "end" and t > tl.start + 0.1:
            tl.set_range(tl.start, t)
            self._show_range()
        elif ident == "still":
            self.save_still(t)

    def save_still(self, t):
        """1.8.10: the picture at ``t`` in full size as PNG next to the clips (Clips/<round> – Bild m:ss.png)."""
        if not self.info.ok or not self.ffmpeg:
            return
        name = clipedit.NAME_CHARS.sub("", "{} – {} {}".format(
            os.path.splitext(os.path.basename(self.path))[0], _("Bild"), clipedit.fmt_pos(t).replace(":", "-")))
        try:
            os.makedirs(self.clips_dir, exist_ok=True)
        except OSError as e:
            self.status.setText(_("Clips-Ordner nicht anlegbar: {error}", error=e))
            return
        out = clipedit.unique_path(self.clips_dir, name, ".png")
        path, info, ffmpeg, b = self.path, self.info, self.ffmpeg, self.bridge

        def work():
            img = clipedit.frame_at(path, t, info.height, info, ffmpeg)
            ok = False
            if img is not None:
                try:
                    img.save(out)
                    ok = True
                except OSError:
                    pass
            b.still.emit(ok, out)
        threading.Thread(target=work, name="clip-still", daemon=True).start()

    def _still_saved(self, ok, out):
        if ok:
            self._last_out = out
            self.show_btn.setEnabled(True)
            self.status.setText(_("Standbild gespeichert: {file}", file=os.path.basename(out)))
            self.log(_("Standbild gespeichert: {file}", file=out), "System")
            if self.on_saved:                       # 1.8.13: stills are in the clips list too
                self.on_saved(out)
        else:
            self.status.setText(_("Standbild nicht gespeichert."))

    def _saved(self, ok, out, why):
        self.save_btn.setEnabled(True)
        if ok:
            self._last_out = out
            self.show_btn.setEnabled(True)
            try:
                mb = os.path.getsize(out) / 1024 ** 2
            except OSError:
                mb = 0.0
            self.status.setText(_("Gespeichert: {file} ({mb} MB)", file=os.path.basename(out), mb=f"{mb:.1f}"))
            self.log(_("Clip gespeichert: {file}", file=out), "System")
            if self.on_saved:
                self.on_saved(out)
        else:
            self.status.setText(_("Clip nicht gespeichert: {why}", why=why or "ffmpeg"))
            self.log(_("Clip nicht gespeichert: {why}", why=why or "ffmpeg"), "Fehler")

    def _show_saved(self):
        if not self._last_out:
            return
        if os.name == "nt":
            import subprocess
            subprocess.Popen(["explorer", "/select,", os.path.normpath(self._last_out)])   # noqa: S603,S607
        else:
            self.status.setText(self._last_out)

    def _open_clips(self):
        try:
            os.makedirs(self.clips_dir, exist_ok=True)
            if os.name == "nt":
                os.startfile(self.clips_dir)                     # noqa: S606 – opens Explorer
            else:
                self.status.setText(self.clips_dir)
        except OSError as e:
            self.status.setText(str(e))

    # ---- keys / closing
    def keyPressEvent(self, e):
        k, mods = e.key(), e.modifiers()
        big, frame = bool(mods & Qt.ShiftModifier), bool(mods & Qt.ControlModifier)
        if k == Qt.Key_Space:
            self.toggle_play()
        elif k == Qt.Key_Left:
            self.step_frame(-1) if frame else self.step(-(STEP_BIG if big else STEP_SMALL))
        elif k == Qt.Key_Right:
            self.step_frame(1) if frame else self.step(STEP_BIG if big else STEP_SMALL)
        elif k == Qt.Key_I:
            self.set_start()
        elif k == Qt.Key_O:
            self.set_end()
        elif k == Qt.Key_M:
            self.next_mark()
        elif k == Qt.Key_Home:
            self.goto(0.0)
        elif k == Qt.Key_End:
            self.goto(self.info.duration)
        elif k in (Qt.Key_Delete, Qt.Key_Backspace) and self.preview.shape_tool and self.preview.selected_shape():
            self.preview.remove_selected_shape()                # 1.12: a drawing
        elif k in (Qt.Key_Delete, Qt.Key_Backspace) and self.preview.editing:
            self.preview.remove_selected()
        elif k == Qt.Key_A and not self.compact:
            self.add_part()                                     # 1.12
        elif k == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(e)

    def _drain(self):
        if self._closed:                    # closed: pictures, levels, playback go; a finished save still counts
            self.bridge.clear(keep=_Bridge.AFTER_CLOSE)
        self.bridge.drain()

    def closeEvent(self, e):
        self._closed = True
        self.bridge.clear(keep=_Bridge.AFTER_CLOSE)
        self._stop_player()
        with self._scrub_lock:
            self._scrub_lock.notify_all()
        super().closeEvent(e)
