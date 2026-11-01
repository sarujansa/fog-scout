"""The compact clip editor beside the recordings and clips tables and what every editor shares (1.5.1, user's
wish: cut rounds "wie in Medal"): a preview picture (PreviewView, the canvas of the picture editor too), the strip
with thumbnails (Timeline), playback (frames streamed by ffmpeg, the sound by Windows from a WAV of the same
stretch), the F8 marks, "Clip speichern" (stream copy or frame exact, see clipedit.cut) into the folder "Clips"
next to the recordings. 1.16: the big editor is qt_editor.EditorWindow (timeline with tracks, library, inspector);
ClipBase here holds the machinery both use.

All ffmpeg work runs in threads (clipedit); results come back over the bridge (_Bridge). The compact window is a
plain QWidget the App puts beside the tables (app_recordings._rec_preview_build)."""
from __future__ import annotations

import logging
import math
import os
import subprocess
import threading
import time

from PySide6.QtCore import QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QImage, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit,
                               QProgressBar, QPushButton, QSizePolicy, QSlider, QVBoxLayout, QWidget)

from . import annotate, clipedit, encoders, imageedit, obsrec, qt_theme
from .i18n import N_, _
from .qt_common import guard_wheel
from .qt_layouts import FlowRow

log = logging.getLogger("fogscout")

CENSOR_LABELS = {"pixel": N_("Verpixelt"), "blur": N_("Verwischt"), "black": N_("Schwarz"),
                 "retouch": N_("Retusche (aus der Umgebung übermalt)")}   # 1.7.2, retouch 1.7.3
SIDE_W = 400                                     # 1.12.5: px of the big editor's side column (tools, saving)
MARK_BEFORE_S, MARK_AFTER_S = 20.0, 10.0          # a clip around an F8 mark (on opening, „Clip um Marke“)
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
HEIGHT_LABELS = {0: N_("Wie aufgenommen"), 1440: "1440p", 1080: "1080p", 720: "720p"}   # 1.15: export height
SPEED_LABELS = {0.25: "×0.25", 0.5: "×0.5", 0.75: "×0.75", 1.0: N_("normal"), 1.5: "×1.5", 2.0: "×2", 4.0: "×4"}
CONTENT_LABEL = N_("Ohne schwarze Ränder")      # 1.12.6: crop to the game part, offered when the recording has borders
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
VIEWER_BG = "#0e0f11"             # 1.16: the editor's viewer around the picture (dark whatever the theme, like players)
PUMP_MS = 15                      # 1.8.66: how often the window takes what its threads produced
CLOSED_PUMP_MS = 200              # how often the saves of closed editors are looked after (_drain_closed)
SAVE_TIMEOUT_S = 3600             # one ffmpeg run of a save at most (clipedit.export's own limit)
STOP_WAIT_S = 2.0                 # quitting waits this long for the stopped saves to tidy up (within QUIT_WATCHDOG_S)


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
             "levels",       # 1.8.18: {track index: loudest moment in dB}
             "content",      # 1.12.6: the game part of a recording with black borders (x, y, w, h)
             "encoders",     # 1.15: {ffmpeg encoder: works} once the self-tests are through
             "wave")         # 1.16: the loudness along the recording (clipedit.waveform) for the audio track
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


class _SaveJob:
    """A clip or still being saved in a thread. It outlives the window that started it: a compact editor beside
    the tables is deleted when another row is picked, its pump with it – the result then comes through
    ``_drain_closed`` and still reaches the log and the clips list (else: no index entry, no automatic upload, a GIF
    the program never listed). ``run`` is clipedit's ``run`` with ffmpeg as a child ``stop`` can end: quitting must
    not leave ffmpeg writing on its own (half file, temp folder of the drawings) – clipedit removes both when the
    run fails."""

    def __init__(self, win, out: str):
        self.win, self.out = win, out
        self.thread = None
        self.stopped = False
        self._proc = None
        self._lock = threading.Lock()

    def run(self, args):
        with self._lock:
            if self.stopped:
                return 1, b""
            self._proc = proc = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                                 stderr=subprocess.PIPE,
                                                 creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        try:
            _out, err = proc.communicate(timeout=SAVE_TIMEOUT_S)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
            raise                                       # clipedit reports it like its own timeout
        return proc.returncode, err or b""

    def stop(self):
        with self._lock:
            self.stopped = True
            proc = self._proc
        if proc is not None and proc.poll() is None:
            try:
                proc.kill()
            except OSError:
                pass


_SAVES = []                       # the _SaveJob of every editor still running or not yet handed over (GUI thread)
_closed_pumping = False


def running_saves() -> list:
    """The files the clip editors are still writing (the App holds back an update restart meanwhile)."""
    return [job.out for job in _SAVES]


def stop_saves(wait: float = STOP_WAIT_S) -> list:
    """The program quits: every running save is stopped (ffmpeg ended; clipedit removes the half file and its temp
    folder), its thread gets up to ``wait`` s in all, then each result goes to its editor – a save that was done
    anyway still reaches the clips list. Returns the files of the saves stopped."""
    jobs = list(_SAVES)
    for job in jobs:
        job.stop()
    deadline = time.monotonic() + wait
    for job in jobs:
        if job.thread is not None:
            job.thread.join(max(0.0, deadline - time.monotonic()))
    wins = []
    for job in jobs:
        if all(w is not job.win for w in wins):
            wins.append(job.win)
    for w in wins:
        w._drain()
    return [job.out for job in jobs]


def _forget_save(win, out):
    """The result of ``win``'s save of ``out`` was handled: off the list (the job, or None)."""
    for job in _SAVES:
        if job.win is win and job.out == out:
            _SAVES.remove(job)
            return job
    return None


def _watch_closed():
    global _closed_pumping
    if not _closed_pumping:
        _closed_pumping = True
        QTimer.singleShot(CLOSED_PUMP_MS, _drain_closed)


def _drain_closed():
    """The results of editors closed while saving (their own pump may be gone with them); again while any runs."""
    global _closed_pumping
    wins = []
    for job in _SAVES:
        if job.win._closed and all(w is not job.win for w in wins):
            wins.append(job.win)
    for w in wins:
        w._drain()
    if any(job.win._closed for job in _SAVES):
        QTimer.singleShot(CLOSED_PUMP_MS, _drain_closed)
    else:
        _closed_pumping = False


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
        self.view = None                  # 1.12.6: the game part of each picture (x, y, w, h), None = all of it
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

    def set_view(self, box):
        self.view = tuple(box) if box else None
        self.update()

    def tiles(self) -> list:
        """1.12.6: [(target rect, thumbnail index)] along the strip – pictures side by side in their own shape (the
        game part, ``view``), each the thumbnail nearest its middle; the last one cut at the end. They were squeezed
        into THUMBS equal cells: in the narrower left column of the big editor a 21:9 round became slivers."""
        img = next(iter(self.thumbs.values()), None)
        r = self._strip()
        if img is None or r.width() < 2 or r.height() < 2:
            return []
        _x, _y, vw, vh = self.view or (0.0, 0.0, 1.0, 1.0)
        step = max(8.0, r.height() * img.width() * vw / max(1.0, img.height() * vh))
        n = max(1, self.n_thumbs)
        out, x = [], r.left()
        while x < r.right() - 0.5:
            mid = (x + step / 2 - r.left()) / r.width()
            out.append((QRectF(x, r.top(), min(step, r.right() - x), r.height()), min(n - 1, max(0, int(mid * n)))))
            x += step
        return out

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
        vx, vy, vw, vh = self.view or (0.0, 0.0, 1.0, 1.0)
        gap = QColor(c["field"])
        for target, i in self.tiles():
            img = self.thumbs.get(i)
            if img is None:
                continue
            sw, sh = img.width() * vw, img.height() * vh          # the game part, the last tile its left share
            full = r.height() * sw / max(1.0, sh)
            p.drawImage(target, img, QRectF(img.width() * vx, img.height() * vy, sw * target.width() / full, sh))
            p.fillRect(QRectF(target.right() - 1, r.top(), 1, r.height()), gap)
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
        menu.setAttribute(Qt.WA_DeleteOnClose)
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
    view_changed = Signal()               # 1.12.6: the part of the picture on display changed (zoom to the crop)
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
        self.zoom_crop = False            # 1.12.6: show only the crop box, large (the clip editor's "no black borders")
        self.shapes = []
        self.shape_tool = None            # annotate kind to draw, None = off
        self.shape_sel = None             # index of the picked drawing
        self.pen = {"colour": annotate.COLOURS[0], "size": annotate.DEFAULT_SIZE, "text_size": annotate.TEXT_SIZE,
                    "text": ""}
        self.now = None                   # seconds of the recording on display: drawings of other times hide
        self.new_times = lambda: (None, None)   # (t0, t1) a new drawing gets (the clip editor: from the playhead)
        self._layer = None                # (key, QImage) of the drawings at the drawn size
        self.source_size = None           # (w, h) of the real picture when the frame is a smaller copy of it
        self.plain = False                # 1.16: the editor's viewer – a flat dark area instead of the card frame
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
        was = self.view
        self.crop = tuple(box) if box else None
        self.crop_ratio = ratio
        self._view_moved(was)

    def set_crop_edit(self, on: bool):
        was = self.view
        self.crop_edit = bool(on)
        if on:
            self.set_editing(False)
            self.set_shape_tool(None)
        self.setCursor(Qt.CrossCursor if on else Qt.ArrowCursor)
        self._view_moved(was)

    def set_zoom_crop(self, on: bool):
        was = self.view
        self.zoom_crop = bool(on)
        self._view_moved(was)

    @property
    def view(self):
        """1.12.6: the part of the picture on display (x, y, w, h), None = all of it. The crop box while
        ``zoom_crop`` is on – but not while the crop tool is: its frame needs the picture around it."""
        if self.zoom_crop and self.crop and not self.crop_edit:
            return self.crop
        return None

    def _view_moved(self, was):
        self.update()
        if self.view != was:
            self.view_changed.emit()

    def set_shapes(self, shapes):
        self.shapes = list(shapes)
        self.shape_sel = None if self.shape_sel is None or self.shape_sel >= len(self.shapes) else self.shape_sel
        self._layer = None
        self._end_shape_move()
        self.update()

    def _end_shape_move(self):
        """The drawings were replaced or one removed (Entf, undo) while one is dragged: that drag ends – it held the
        old drawing and wrote it back at its index on every move (TypeError once the index was gone)."""
        if self._drag and self._drag[0] == "shape_move":
            self._drag = None

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
        self._end_shape_move()
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
        """A crop box from the corner that stays (``x0``, ``y0``) and the mouse (fractions), held to ``crop_ratio``
        (the width leads). A box under MIN_BOX comes back empty – the release drops it (clamp_box raised it to a
        1 % box of the wrong shape)."""
        x, y, w, h = min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0)
        if self.crop_ratio:
            iw, ih = self.image_size()
            h = w * iw / (self.crop_ratio * ih)
            room = y0 if y1 < y0 else 1.0 - y0                # above / below the corner that stays
            if h > room:                                      # too tall for the room: the height leads (upwards
                h = room                                      # too – clamp_box cut only h there, 9:16 became 0.8)
                w = h * ih * self.crop_ratio / iw
            y = y0 - h if y1 < y0 else y0
            x = x0 - w if x1 < x0 else x0
        if w < self.MIN_BOX or h < self.MIN_BOX:
            return x, y, 0.0, 0.0
        return imageedit.clamp_box((x, y, w, h), self.MIN_BOX)

    # ---- geometry
    def frame_rect(self) -> QRectF:
        """Where the picture lies (aspect kept, centred); 16:9 while there is no picture yet. 1.12.6: with a
        ``view`` that part fills the area and the rest of the picture lies beyond the edges (not drawn) – all
        fractions (boxes, drawings, the crop) stay fractions of the whole picture."""
        area = QRectF(self.rect()).adjusted(2, 2, -2, -2)
        iw, ih = (self._img.width(), self._img.height()) if self._img is not None else (16, 9)
        if iw <= 0 or ih <= 0:
            return area
        vx, vy, vw, vh = self.view or (0.0, 0.0, 1.0, 1.0)
        s = min(area.width() / (iw * vw), area.height() / (ih * vh))
        w, h = iw * s, ih * s
        return QRectF(area.center().x() - (vx + vw / 2) * w, area.center().y() - (vy + vh / 2) * h, w, h)

    def view_rect(self) -> QRectF:
        """1.12.6: the part of the widget that shows picture (the whole frame_rect without a view)."""
        view = self.view
        return self._box_rect(view) if view else self.frame_rect()

    def _box_rect(self, box) -> QRectF:
        f = self.frame_rect()
        x, y, w, h = box
        return QRectF(f.left() + x * f.width(), f.top() + y * f.height(), w * f.width(), h * f.height())

    def _to_frac(self, pt) -> tuple:
        f = self.frame_rect()
        vx, vy, vw, vh = self.view or (0.0, 0.0, 1.0, 1.0)          # 1.12.6: never into the part not shown
        return (min(max(vx, (pt.x() - f.left()) / max(1.0, f.width())), vx + vw),
                min(max(vy, (pt.y() - f.top()) / max(1.0, f.height())), vy + vh))

    # ---- drawing
    def _frame_scaled(self, size, view=None):
        """The frame at the drawn ``size`` – 1.12.6: of the ``view`` part only (a zoomed picture is not scaled up
        whole to cut most of it away)."""
        key = (size, view)
        if self._scaled is None or self._scaled[0] != key:
            img = self._img
            if view:
                x, y, w, h = view
                img = img.copy(QRectF(x * img.width(), y * img.height(), w * img.width(), h * img.height()).toRect())
            self._scaled = (key, img.scaled(size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        return self._scaled[1]

    def paintEvent(self, e):
        c = qt_theme.colours(self.dark)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        # 1.12.5: black only behind the picture – around it the card colour, so a dark frame no longer reads as one
        # big black box (user's screenshot of the big editor at 0:00 of a round)
        if self.plain:
            p.fillRect(self.rect(), QColor(VIEWER_BG))
        else:
            p.setPen(QPen(QColor(c["border"]), 1))
            p.setBrush(QColor(c["card"]))
            p.drawRoundedRect(QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5), 8, 8)
        p.setPen(Qt.NoPen)
        f = self.frame_rect()
        vr = self.view_rect()
        p.fillRect(vr, QColor("#000000"))
        if self._img is None:
            p.end()
            return
        size = f.toRect().size()
        shown = vr.toRect().size()
        if size.width() < 2 or size.height() < 2 or shown.width() < 2 or shown.height() < 2:
            p.end()
            return
        scaled = self._frame_scaled(shown, self.view)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        if self.view:
            p.setClipRect(vr)                                   # 1.12.6: a zoomed picture stops at its part
        p.drawImage(vr.topLeft(), scaled)
        accent = QColor(c["accent"])
        for i, box in enumerate(self.boxes):
            r = self._box_rect(box)
            if self.active:
                self._draw_censored(p, scaled, r, vr)
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
        """1.12: outside the crop box darkened; with the tool on its frame and four corner handles. 1.12.6: nothing
        while the view is the crop – the picture shown is the clip."""
        box = self._drag[2] if self._drag and self._drag[0].startswith("crop") else self.crop
        if not box or self.view is not None:
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
        """The box as the clip will show it: coarse blocks, a blur, or black (same rules as clipedit.censor_graph).
        ``scaled`` is the picture drawn at ``f`` (1.12.6: the view part at view_rect)."""
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
            if not self.view_rect().contains(pt):
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
            f = self.frame_rect()                             # a click (a pixel of hand jitter) is no new box
            moved = abs(fx - px) * f.width() + abs(fy - py) * f.height()
            far = moved >= QApplication.startDragDistance()
            self._drag = (kind, (px, py), self._crop_box_for(px, py, fx, fy) if far else (px, py, 0.0, 0.0))
        elif kind == "crop_move":
            x, y, w, h = orig
            self._drag = (kind, (px, py), imageedit.clamp_box((x + fx - px, y + fy - py, w, h), self.MIN_BOX))
        elif kind.startswith("crop_"):
            x, y, w, h = orig
            ax = x + w if kind in ("crop_tl", "crop_bl") else x           # the opposite corner stays
            ay = y + h if kind in ("crop_tl", "crop_tr") else y
            self._drag = (kind, (px, py), self._crop_box_for(ax, ay, fx, fy))
        elif kind == "shape_move":
            if self.shape_sel is None or not 0 <= self.shape_sel < len(self.shapes):
                self._drag = None                             # the drawing is gone
            else:
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
            if not self.view_rect().contains(pt):
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


class ClipBase(QWidget):
    """What every editor of one recording shares (1.16: split out of ClipWindow when the big editor became
    qt_editor.EditorWindow): the file and its facts, the bridge from the ffmpeg threads, the scrub/strip/level
    threads, playback (frames from a FramePlayer, the sound as a WAV through Windows), saving a clip or a still in
    a thread that outlives the window, the export choices (format, encoding, sound mix) and the censor state.
    ``on_saved(path)`` / ``on_setting(key, value)`` / ``log(text, kind)`` come from the App. A subclass builds the
    widgets (``_build``), says what is saved (``edit_plan``), where the playhead is (``goto``, ``_played_at``) and
    what plays from it (``_segments``)."""
    compact = False

    def __init__(self, path: str, marks: list, clips_dir: str, mode: str = "copy", sound: bool = True,
                 on_saved=None, on_setting=None, log=None, dark=True, qss: str = "", title: str = "",
                 target_mb: int = clipedit.DEFAULT_TARGET_MB, censor_on: bool = False, censor_style: str = "pixel",
                 censor_boxes=(), mix_on=None, mix_vol=None, parent=None, sources=None, info=None, encoding=None,
                 flags=Qt.Window):
        super().__init__(parent, flags)
        self.path, self.marks, self.clips_dir = path, sorted(float(m) for m in marks or ()), clips_dir
        self.on_saved, self.on_setting, self.log = on_saved, on_setting, (log or (lambda text, kind="System": None))
        self.saved_seconds = {}           # 1.8.13: out path -> length of the clip (the clips list shows it)
        self.dark = dark
        self.info = info if info is not None else clipedit.probe(path)   # 1.12.3: the previews probe in a thread
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
        self._queue = []                    # 1.16: the stretches still to play after the current one
        self._seg = None                    # (src start, src end, speed, output start) of the stretch playing
        self._volume = 1.0                  # 1.16: the preview's own volume (the editor's slider)
        self._censor_on, self._censor_style = bool(censor_on), censor_style        # 1.7.2: remembered boxes
        # 1.15: encoder, quality and picture height of a re-encoded clip; the hardware encoders this PC has come
        # from encoders.detect (once per program run, in a thread – the first editor shows the CPU until then)
        self._encoding = encoding if isinstance(encoding, encoders.Encoding) else encoders.Encoding(hw="auto")
        self._avail = encoders.known(self.ffmpeg)
        self._censor_boxes = [list(b) for b in (censor_boxes or ()) if len(b) == 4]
        self._mix_on = {k: bool((mix_on or {}).get(k, True)) for k in obsrec.SOURCES}     # 1.8.6: sound mix
        self._mix_vol = {k: int((mix_vol or {}).get(k, 100) or 0) for k in obsrec.SOURCES}
        self._sources = obsrec.track_sources(self.info.audio_tracks)
        self._silent = set()                # 1.8.18: sources whose own track holds nothing in this recording
        # 1.8.23: the sources OBS had on their own track when the round was recorded (None = not known: older
        # recordings) – a silent track of a source that was not there says "keine Quelle", not "still"
        self._recorded = None if sources is None else set(sources)
        self._absent = set()
        self._content = None                # 1.12.6: the game part when the recording has black borders
        self.setObjectName("page")
        self.setWindowTitle(title or _("Clip bearbeiten – {name}", name=os.path.basename(path)))
        if qss:
            self.setStyleSheet(qss)
        self.sound_box = QCheckBox(_("Ton"))
        self.sound_box.setChecked(bool(sound))
        self.sound_box.setToolTip(_("Beim Abspielen den Ton der Aufnahme mitlaufen lassen (Windows)."))
        self.sound_box.toggled.connect(lambda v: self._setting("clip_sound", bool(v)))
        self._build(mode, sound)
        self.setFocusPolicy(Qt.StrongFocus)
        self.loading = None                 # 1.8.3: LoadingScreen until picture + strip are there
        self._load_state = {"frame": False, "strip": False, "thumbs": 0}
        self.preview.set_boxes(self._censor_boxes)
        self.preview.set_look(self._censor_on, self._censor_style)
        if not self.info.ok or not self.ffmpeg:
            self.status.setText(_("Datei nicht lesbar oder ffmpeg fehlt – keine Vorschau."))
            self.save_btn.setEnabled(False)
            self._ready(False)
            return
        self.loading = LoadingScreen(self, os.path.basename(path), self.timeline.n_thumbs + 1)
        self.loading.setGeometry(self.rect())
        self.loading.raise_()
        self._load_timer = QTimer(self)
        self._load_timer.setSingleShot(True)
        self._load_timer.timeout.connect(self._load_late)
        self._load_timer.start(LOAD_TIMEOUT_MS)
        self._ready(True)
        self._start_threads()

    def _load_late(self):
        if self.loading is not None:
            self.loading.finish(late=True)

    # ---- hooks of the subclasses
    def _build(self, mode, sound):
        raise NotImplementedError

    def _ready(self, ok: bool):
        """The file is (not) readable: set up the timeline and the first position."""

    def edit_plan(self) -> clipedit.Edit:
        raise NotImplementedError

    def goto(self, t: float):
        raise NotImplementedError

    def _segments(self) -> list:
        """What plays from the playhead on: [(source start, source end, tempo, output time at its start)]."""
        raise NotImplementedError

    def _played_at(self, t: float):
        """The playback is at source second ``t`` of the stretch playing: move the playhead."""

    def _show_pos(self):
        pass

    def _content_found(self, box):
        """1.12.6: the recording has black borders around the game – the strip shows the game part."""
        self._content = tuple(box)
        self.timeline.set_view(self._content)

    # ---- small builders
    def _btn(self, row, text, slot, tip=""):
        b = QPushButton(text)
        b.setFocusPolicy(Qt.NoFocus)                      # the keys stay with the window
        b.clicked.connect(slot)
        if tip:
            b.setToolTip(tip)
        row.addWidget(b)
        return b

    @staticmethod
    def _card(title, head=True):
        """A card like the main window's, with a small heading (not on a tab page: the tab names it); returns
        (frame, its layout)."""
        card = QFrame()
        card.setProperty("class", "card")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(14, 10 if head else 12, 14, 12)
        lay.setSpacing(8 if not head else 6)
        if head:
            label = QLabel(title.upper())
            label.setProperty("class", "sub")
            lay.addWidget(label)
        return card, lay

    @staticmethod
    def _choice() -> QComboBox:
        """A choice box: no mouse wheel (guard_wheel), no keyboard focus – like the buttons the keys stay with the
        window. A box picked with the mouse kept the focus and took the window's keys: Home/End set the tempo to
        ×0.25/×4 or the crop to none/4:5, letters picked an item ("A" on a fade: "aus"), Space opened it."""
        box = guard_wheel(QComboBox())
        box.setFocusPolicy(Qt.NoFocus)
        return box

    def _combo(self, row, items, current, tip, slot):
        """A choice box of (data, label) with ``current`` picked (see _choice)."""
        box = self._choice()
        for data, label in items:
            box.addItem(label, data)
        idx = next((i for i, (d, _l) in enumerate(items) if d == current), 0)
        box.setCurrentIndex(idx)
        box.setToolTip(tip)
        box.currentIndexChanged.connect(slot)
        if row is not None:
            row.addWidget(box)
        return box

    def _mode_boxes(self, mode):
        """The format box with its two companions (target size for Discord, height for a GIF)."""
        self.mode_box = self._choice()
        self.mode_box.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        for key in clipedit.MODES:
            self.mode_box.addItem(_(MODE_LABELS[key]), key)
            self.mode_box.setItemData(self.mode_box.count() - 1, _(MODE_TIPS[key]), Qt.ToolTipRole)
        self.mode_box.setCurrentIndex(max(0, list(clipedit.MODES).index(mode) if mode in clipedit.MODES else 0))
        self.mode_box.currentIndexChanged.connect(self._mode_changed)
        self.target_box = self._choice()
        for mb in clipedit.TARGETS_MB:
            self.target_box.addItem(_("≤ {n} MB", n=mb), mb)
        self.target_box.setCurrentIndex(list(clipedit.TARGETS_MB).index(self._target_mb))
        self.target_box.setToolTip(_("Discord: ohne Nitro 10 MB, Nitro Basic 50 MB, Nitro 500 MB."))
        self.target_box.currentIndexChanged.connect(self._target_changed)
        self.gif_box = self._choice()                                               # 1.12: GIF height
        for gh in clipedit.GIF_HEIGHTS:
            self.gif_box.addItem(f"{gh}p", gh)
        self.gif_box.setCurrentIndex(list(clipedit.GIF_HEIGHTS).index(clipedit.DEFAULT_GIF_H))
        self.gif_box.setToolTip(_("Höhe des GIFs – kleiner = kleinere Datei (Discord, Chats)."))
        self.gif_box.currentIndexChanged.connect(lambda _i: self._show_size())

    def _encoding_row(self):
        """1.15: codec, encoder (CPU or a graphics-card encoder that passed its self-test), quality and picture
        height of a re-encoded clip – the arguments go to encoders.Encoding; a stream-copied clip ignores them."""
        row = QHBoxLayout() if self.compact else FlowRow(spacing=8)
        self.enc_label = QLabel(_("Kodierung"))
        row.addWidget(self.enc_label)
        self.codec_box = self._choice()
        for key in encoders.CODECS:
            self.codec_box.addItem(encoders.CODEC_LABELS[key], key)
        self.codec_box.setToolTip(_("H.264 spielt überall; HEVC (H.265) ist bei gleicher Qualität etwa ein Drittel "
                                    "kleiner, braucht aber einen neueren Player."))
        self.hw_box = self._choice()
        self.hw_box.setToolTip(_("Womit der Clip kodiert wird: die Grafikkarte (NVENC, AMF, Quick Sync – nur, wenn "
                                 "ffmpeg sie hier wirklich ansprechen kann) belastet den Prozessor kaum; "
                                 "„Automatisch“ nimmt die erste, die geht."))
        self.quality_box = self._choice()
        for key in encoders.QUALITIES:
            self.quality_box.addItem(_(encoders.QUALITY_LABELS[key]), key)
        self.quality_box.setToolTip(_("Schnell: kleiner und schneller, sichtbar weicher. Ausgewogen: wie bisher. "
                                      "Hoch: grösser, nahe am Original."))
        self.height_box = self._choice()
        for key, label in HEIGHT_LABELS.items():
            self.height_box.addItem(_(label) if key == 0 else label, key)
        self.height_box.setToolTip(_("Bildhöhe des Clips – kleiner als die Aufnahme verkleinert, nie vergrössert."))
        self._encoding_fill()
        for box in (self.codec_box, self.hw_box, self.quality_box, self.height_box):
            row.addWidget(box)
            box.currentIndexChanged.connect(self._encoding_changed)
        self.enc_widgets = (self.enc_label, self.codec_box, self.hw_box, self.quality_box, self.height_box)
        if self.compact:
            row.addStretch()
        return row

    def _encoding_fill(self):
        """The boxes show self._encoding; the encoder box offers what this PC has (and "Automatisch")."""
        e = self._encoding
        boxes = (self.codec_box, self.hw_box, self.quality_box, self.height_box)
        for box in boxes:
            box.blockSignals(True)
        try:
            self.codec_box.setCurrentIndex(max(0, self.codec_box.findData(e.codec)))
            self.hw_box.clear()
            self.hw_box.addItem(_(encoders.HW_LABELS["auto"]), "auto")
            for key, label in encoders.hw_choices(self._avail, e.codec):
                self.hw_box.addItem(_(label) if key == "" else label, key)
            i = self.hw_box.findData(e.hw)
            self.hw_box.setCurrentIndex(i if i >= 0 else 0)
            self.quality_box.setCurrentIndex(max(0, self.quality_box.findData(e.quality)))
            self.height_box.setCurrentIndex(max(0, self.height_box.findData(int(e.height or 0))))
        finally:
            for box in boxes:
                box.blockSignals(False)

    def _encoding_changed(self, _i=None):
        e = encoders.Encoding(self.codec_box.currentData() or "h264", self.quality_box.currentData() or "balanced",
                              int(self.height_box.currentData() or 0),
                              self.hw_box.currentData() if self.hw_box.currentData() is not None else "auto")
        if e.codec != self._encoding.codec:                   # HEVC may have other hardware encoders than H.264
            self._encoding = e
            self._encoding_fill()
        self._encoding = e
        for key, value in (("clip_codec", e.codec), ("clip_quality", e.quality), ("clip_height", int(e.height)),
                           ("clip_hw", e.hw)):
            self._setting(key, value)
        self._show_size()

    def _encoders_known(self, avail):
        """The self-tests are through: the encoder box offers the graphics-card encoders that work."""
        self._avail = dict(avail or {})
        if not self._closed and hasattr(self, "hw_box"):
            self._encoding_fill()
            self._show_size()

    def encoding(self) -> encoders.Encoding:
        """What the save will encode with: the wish resolved against this PC's encoders (CPU until known)."""
        return self._encoding.resolve(self._avail)

    # ---- 1.8.6: the sound mix (like Medal – each source on its own OBS track, on/off and a level each)
    def _mix_row(self, stacked=False):
        """The label and the sources in a row, the hint in a line of its own below them (1.12.2: beside them it
        squeezed the row into a column of single words next to the recordings table); with no sources to pick the
        hint stands beside the label (``_mix_fill`` moves it). ``stacked`` (1.12.5, the big editor's side column):
        the label on top, one source per line (box, level, value), the hint below."""
        lines = QVBoxLayout()
        lines.setSpacing(4 if stacked else 2)
        self.mix_label = QLabel(_("Ton im Clip"))
        self.mix_boxes, self.mix_sliders, self.mix_values = {}, {}, {}
        if stacked:
            self._mix_top = self._mix_below = None        # the hint stays below
            lines.addWidget(self.mix_label)
            for key in obsrec.SOURCES:
                line = QHBoxLayout()
                box = QCheckBox(_(SOURCE_LABELS[key]))
                box.setToolTip(_(SOURCE_TIPS[key]))
                box.setMinimumWidth(130)
                sl = guard_wheel(QSlider(Qt.Horizontal))
                sl.setRange(0, MIX_MAX)
                sl.setToolTip(_("Lautstärke dieser Quelle im Clip (100 % = wie aufgenommen)."))
                val = QLabel("")
                val.setProperty("class", "dim")
                val.setMinimumWidth(44)
                val.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.mix_boxes[key], self.mix_sliders[key], self.mix_values[key] = box, sl, val
                line.addWidget(box)
                line.addWidget(sl, 1)
                line.addWidget(val)
                lines.addLayout(line)
            self.mix_hint = QLabel(_("Eine Tonspur – zum Mischen nimmt OBS mit Spur 1–4 auf (Einstellungen → "
                                     "Aufnahmen)."))
            self.mix_hint.setProperty("class", "dim")
            self.mix_hint.setWordWrap(True)
            lines.addWidget(self.mix_hint)
            self._mix_fill()
            for key in obsrec.SOURCES:
                self.mix_boxes[key].toggled.connect(self._mix_changed)
                self.mix_sliders[key].valueChanged.connect(lambda v, k=key: self._mix_slid(k))
                self.mix_sliders[key].sliderReleased.connect(self._mix_changed)
            return lines
        row = self._mix_top = QHBoxLayout()
        row.addWidget(self.mix_label)
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
        if self.playing and self._sound_wanted():                 # hear the change at once
            back = self._play_to
            self._stop_player()
            self._play_to = back
            self.toggle_play()

    def _setting(self, key, value):
        if self.on_setting:
            self.on_setting(key, value)

    # ---- censoring (1.7.2)
    def _censor_args(self) -> dict:
        if self._censor_on and self.preview.boxes:
            return {"censor": [tuple(b) for b in self.preview.boxes], "censor_style": self._censor_style}
        return {}

    def _boxes_changed(self):
        self._setting("clip_censor_boxes", [[round(v, 4) for v in b] for b in self.preview.boxes])
        self._show_size()

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
        b.content.connect(self._content_found)
        b.encoders.connect(self._encoders_known)
        if self._avail is None and self.ffmpeg:
            encoders.detect_async(self.ffmpeg, b.encoders.emit)
        threading.Thread(target=self._scrub_loop, name="clip-scrub", daemon=True).start()
        if any(i >= 0 for i in self._sources.values()):
            threading.Thread(target=self._level_loop, name="clip-levels", daemon=True).start()
        threading.Thread(target=self._thumb_loop, name="clip-thumbs", daemon=True).start()
        self._extra_threads()

    def _extra_threads(self):
        """A subclass starts what else it needs (the editor: the waveform)."""

    def _scrub(self, t: float, quick: bool | None = None):
        """Ask the scrub thread for the picture at source second ``t``."""
        with self._scrub_lock:
            self._want = (t, self._first_look if quick is None else quick)
            self._first_look = False
            self._scrub_lock.notify()

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
        got = {}                                     # 1.7.1: one ffmpeg run for the whole strip (key frames only)
        for i, img in clipedit.thumb_strip(self.path, times, clipedit.THUMB_SRC_H, self.info, self.ffmpeg,
                                           stop=lambda: self._closed):
            got[i] = img
            self.bridge.thumb.emit(i, img)
        for i, t in enumerate(times):                # whatever the run did not deliver: the old way
            if self._closed:
                return
            if i in got:
                continue
            img = clipedit.frame_at(self.path, t, clipedit.THUMB_SRC_H, self.info, self.ffmpeg)
            if img is not None and not self._closed:
                got[i] = img
                self.bridge.thumb.emit(i, img)
        self._find_content(times, got)
        if not self._closed:
            self.bridge.strip_done.emit()

    def _find_content(self, times, got):
        """1.12.6 (thread, PIL only): black borders from the strip's pictures, the edges on one sharper picture –
        the strip picture with the most game in it, fetched again at preview size (key frame, ~40 ms)."""
        box = clipedit.content_box(got.values())
        if box is None or self._closed:
            return
        best = max(got, key=lambda i: sum(got[i].convert("L").point(lambda v: v > clipedit.CONTENT_DARK and 255)
                                          .histogram()[255:]))
        sharp = clipedit.frame_at(self.path, times[best], clipedit.PREVIEW_H, self.info, self.ffmpeg, keyframe=True)
        box = clipedit.refine_box(box, sharp)
        if not self._closed:
            self.bridge.content.emit(box)

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

    # ---- pictures
    def _show_frame(self, t, img):
        if not self.playing:
            self._paint(img)
        self._loaded("frame")

    def _show_played(self, t, img):
        if self.playing:
            self._played_at(t)
            self.preview.set_now(t)
            self._show_pos()
            self._paint(img)

    def _paint(self, img):
        self.preview.set_frame(_qimage(img))

    # ---- playback
    def _sound_wanted(self) -> bool:
        return self.sound_box.isChecked() and os.name == "nt" and self._volume > 0

    def toggle_play(self):
        if self.playing:
            self._play_to = None
            self._stop_player()
            return
        segs = self._segments()
        if not segs:
            return
        self.playing = True
        self._show_playing(True)
        self._queue = list(segs)
        self._next_segment()

    def _next_segment(self):
        """Start the next stretch of the queue (sound first when wanted, then the frames)."""
        if not self._queue:
            self._finish_playing()
            return
        self._seg = seg = self._queue.pop(0)
        start, end, speed, _out = seg
        if self._sound_wanted():
            mix, n, vol = self.mix(), self.info.audio_tracks, self._volume
            threading.Thread(target=lambda: self.bridge.sound.emit(
                clipedit.sound_wav(self.path, start, end, self.ffmpeg, mix=mix, n_tracks=n, speed=speed, volume=vol),
                start), name="clip-sound", daemon=True).start()
        else:
            self._run_player(seg)

    def _sound_ready(self, wav, start):
        if not self.playing or self.player is not None or self._seg is None or abs(self._seg[0] - start) > 1e-6:
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
        self._run_player(self._seg)

    def _run_player(self, seg):
        b = self.bridge
        start, end, speed, _out = seg
        self.player = clipedit.FramePlayer(self.path, start, self.info, lambda t, img: b.played.emit(t, img),
                                           lambda: b.ended.emit(self.player), end=end, ffmpeg=self.ffmpeg,
                                           speed=speed)
        self.player.start()

    def _show_playing(self, on: bool):
        """The play button shows pause while playing."""
        if hasattr(self, "play_btn"):
            self.play_btn.setText(_("⏸ Pause") if on else _("▶ Abspielen"))

    def _stop_player(self):
        self.playing = False
        self._queue = []
        self._seg = None
        self._show_playing(False)
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
            self.player = None
            if self._wav:
                self._drop_wav(self._wav)
                self._wav = None
            if self._queue:
                self._next_segment()
            else:
                self._finish_playing()

    def _finish_playing(self):
        """The last stretch is over: back to where "Clip ansehen" started, else stay."""
        self._stop_player()
        back, self._play_to = self._play_to, None
        self._after_playing(back)

    def _after_playing(self, back):
        """The subclass puts the playhead where it belongs once playback ended (``back`` = return to here)."""

    # ---- saving
    def _show_size(self):
        """1.6.1: what the chosen format makes of the clip – for Discord the picture size and frame rate."""
        mode = self.mode_box.currentData() if hasattr(self, "mode_box") else "copy"
        edit = self.edit_plan()
        if not edit.parts:
            self.size_label.setText(_("Keine Clips auf der Zeitleiste."))
            return
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
        reencoded = mode in ("exact", "discord") or (mode == "copy" and (self._censor_args() or not edit.simple()))
        if reencoded and hasattr(self, "hw_box"):                  # 1.15: what will encode it
            parts.append(self.encoding().summary(_))
        self.size_label.setText(" · ".join(parts))

    def _mode_changed(self, _i, save=True):
        mode = self.mode_box.currentData()
        self.target_box.setVisible(mode == "discord")
        self.gif_box.setVisible(mode == "gif")
        for w in getattr(self, "enc_widgets", ()):               # 1.15: a GIF has no video encoder
            w.setVisible(mode != "gif")
        if save:
            self._setting("clip_mode", mode)
        self._show_size()

    def _target_changed(self, _i):
        self._target_mb = int(self.target_box.currentData() or clipedit.DEFAULT_TARGET_MB)
        self._setting("clip_target_mb", self._target_mb)
        self._show_size()

    def _default_name(self) -> str:
        edit = self.edit_plan()
        if not edit.parts:
            return clipedit.clip_name(self.path, 0.0, 0.0)
        return clipedit.clip_name(self.path, edit.parts[0].start, edit.parts[-1].end)

    def save(self):
        name = clipedit.NAME_CHARS.sub("", self.name_edit.text()).strip() or self._default_name()
        mode = self.mode_box.currentData() or "copy"
        edit = self.edit_plan()                                   # 1.12: parts, tempo, crop, drawings, fades
        if not edit.parts:
            self.status.setText(_("Keine Clips auf der Zeitleiste."))
            return
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
        encoding = self.encoding()                                # 1.15: resolved now, the thread keeps it
        if mode != "copy" or censor or not edit.simple():
            self.status.setText(_("Kodiere {file} … ({how}, dauert etwas)", file=os.path.basename(out),
                                  how=encoding.summary(_)))
        job = _SaveJob(self, out)                         # outlives the window, stoppable on quit (_SaveJob)
        path, ffmpeg, bridge = self.path, self.ffmpeg, self.bridge

        def work():
            try:
                ok, why = clipedit.export(path, edit, out, mode, ffmpeg, run=job.run, target_mb=target, info=info,
                                          mix=mix, gif_h=gif_h, encoding=encoding, **censor)
            except Exception as e:                        # a result in any case: the save must not hang on
                log.exception("Clip speichern")
                ok, why = False, f"{type(e).__name__}: {e}"
            bridge.saved.emit(ok, out, why)
        job.thread = threading.Thread(target=work, name="clip-save", daemon=True)
        _SAVES.append(job)
        job.thread.start()
        self._saving(True)

    def _saving(self, on: bool):
        """A save started / ended: the subclass may show it (the editor's top bar)."""

    def save_still(self, t):
        """1.8.10: the picture at source second ``t`` in full size as PNG next to the clips (Clips/<round> – Bild
        m:ss.png). 1.12.7: cut like the clip when a crop is chosen – "Ohne schwarze Ränder" kept the borders."""
        if not self.info.ok or not self.ffmpeg:
            return
        crop = self.edit_plan().crop
        name = clipedit.NAME_CHARS.sub("", "{} – {} {}".format(
            os.path.splitext(os.path.basename(self.path))[0], _("Bild"), clipedit.fmt_pos(t).replace(":", "-")))
        try:
            os.makedirs(self.clips_dir, exist_ok=True)
        except OSError as e:
            self.status.setText(_("Clips-Ordner nicht anlegbar: {error}", error=e))
            return
        out = clipedit.unique_path(self.clips_dir, name, ".png")
        path, info, ffmpeg, b = self.path, self.info, self.ffmpeg, self.bridge
        job = _SaveJob(self, out)

        def work():
            ok = False
            try:
                img = clipedit.frame_at(path, t, info.height, info, ffmpeg)
                if img is not None:
                    if crop:                              # the same pixels as the clip's crop filter
                        w, h, x, y = clipedit.crop_px(crop, img.width, img.height)
                        img = img.crop((x, y, x + w, y + h))
                    img.save(out)
                    ok = True
            except Exception:                             # OSError, PIL: a result in any case
                log.exception("Standbild speichern")
            b.still.emit(ok, out)
        job.thread = threading.Thread(target=work, name="clip-still", daemon=True)
        _SAVES.append(job)
        job.thread.start()

    def _still_saved(self, ok, out):
        _forget_save(self, out)
        if ok:
            self._last_out = out
        if not self._closed:                        # closed: a compact editor may be deleted, widgets and all
            self.show_btn.setEnabled(bool(self._last_out))
            self.status.setText(_("Standbild gespeichert: {file}", file=os.path.basename(out)) if ok
                                else _("Standbild nicht gespeichert."))
        if ok:
            self.log(_("Standbild gespeichert: {file}", file=out), "System")
            if self.on_saved:                       # 1.8.13: stills are in the clips list too
                self.on_saved(out)

    def _saved(self, ok, out, why):
        job = _forget_save(self, out)
        if job is not None and job.stopped and not ok:
            why = _("beim Beenden abgebrochen")
        if ok:
            self._last_out = out
        if not self._closed:                        # closed: a compact editor may be deleted, widgets and all
            self.save_btn.setEnabled(True)
            self._saving(False)
            if ok:
                self.show_btn.setEnabled(True)
                try:
                    mb = os.path.getsize(out) / 1024 ** 2
                except OSError:
                    mb = 0.0
                self.status.setText(_("Gespeichert: {file} ({mb} MB)", file=os.path.basename(out), mb=f"{mb:.1f}"))
            else:
                self.status.setText(_("Clip nicht gespeichert: {why}", why=why or "ffmpeg"))
        if ok:
            self.log(_("Clip gespeichert: {file}", file=out), "System")
            if self.on_saved:
                self.on_saved(out)
        else:
            self.log(_("Clip nicht gespeichert: {why}", why=why or "ffmpeg"), "Fehler")

    def _show_saved(self):
        if not self._last_out:
            return
        if os.name == "nt":
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

    # ---- closing
    def stop(self):
        """1.8.8: stop playback (the recordings tab was left)."""
        if self.playing:
            self._play_to = None
            self._stop_player()

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
        if any(job.win is self for job in _SAVES):  # its result must come even when the window is deleted now
            _watch_closed()
        self._release()
        super().closeEvent(e)

    def _release(self):
        """1.16.1 (audit, measured: a closed editor kept ~28 MB – lambdas in its signal connections hold the window,
        a cycle through Qt the collector never clears): the pump slows to CLOSED_PUMP_MS (a closed editor drained
        67×/s on; a late save still arrives through it or through _drain_closed), the pictures and the strip go, the
        bridge keeps only the handlers a late save still needs."""
        self._pump.setInterval(CLOSED_PUMP_MS)
        for name in list(self.bridge.handlers):
            if name not in _Bridge.AFTER_CLOSE:
                self.bridge.handlers.pop(name, None)
        pv = getattr(self, "preview", None)
        if pv is not None:
            pv._img = pv._scaled = pv._layer = None
        tl = getattr(self, "timeline", None)
        if tl is not None:
            tl.thumbs.clear()
            if hasattr(tl, "wave"):
                tl.wave = []
            if hasattr(tl, "_layer"):
                tl._layer = None


class ClipWindow(ClipBase):
    """The compact editor beside the recordings and clips tables (1.8.8): the picture, the strip with start and
    end, playback, the clip's facts and saving – no window of its own (``parent`` = the table's host), no tools.
    "Grosser Editor" (``on_expand``) opens qt_editor.EditorWindow with the same range and position. Until 1.15
    this class was the big editor too (``compact`` False); that one is EditorWindow now."""
    compact = True

    def __init__(self, path: str, marks: list, clips_dir: str, mode: str = "copy", sound: bool = True,
                 compact: bool = True, parent=None, on_expand=None, **kw):
        self.on_expand = on_expand
        super().__init__(path, marks, clips_dir, mode, sound, parent=parent, flags=Qt.Widget, **kw)

    def _ready(self, ok: bool):
        if not ok:
            return
        self.timeline.set_duration(self.info.duration)
        self.timeline.marks = self.marks
        self.timeline.set_range(0.0, self.info.duration)
        first = self.marks[0] if self.marks else 0.0
        if self.marks:                                        # a mark: the clip starts 20 s before it, ends 10 s after
            self.timeline.set_range(max(0.0, first - MARK_BEFORE_S), min(self.info.duration, first + MARK_AFTER_S))
        self._show_range()
        self.goto(self.timeline.start)

    # ---- building
    def _build(self, mode, sound):
        """Everything below the preview: the strip, playback, the clip card and the save card side by side."""
        self.preview = PreviewView(self.dark)
        self.preview.boxes_changed.connect(self._boxes_changed)
        self.preview.setMinimumSize(320, 180)
        self.preview.setMaximumHeight(COMPACT_PREVIEW_H)
        self.timeline = Timeline(self.dark)
        self.timeline.seek.connect(self.goto)
        self.timeline.picked.connect(self._timeline_pick)
        self.timeline.changed.connect(self._show_range)
        row = self._transport_row()
        clip_card = self._clip_card()
        export_card = self._save_card(mode)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(10)
        lay.addWidget(self.preview, 1)
        lay.addWidget(self.timeline)
        lay.addLayout(row)
        lay.addWidget(clip_card)
        lay.addWidget(export_card)
        self._mode_changed(self.mode_box.currentIndex(), save=False)

    def _transport_row(self):
        """Position left, playback in the middle."""
        row = QHBoxLayout()
        self.pos_label = QLabel("")
        self.pos_label.setProperty("class", "dim")
        row.addWidget(self.pos_label)
        row.addStretch()
        self.b_back5 = self._btn(row, "−5 s", lambda: self.step(-STEP_BIG), _("5 Sekunden zurück (Shift+←)"))
        self.play_btn = self._btn(row, _("▶ Abspielen"), self.toggle_play, _("Abspielen / Pause (Leertaste)"))
        self.play_btn.setObjectName("primary")
        self.play_btn.setMinimumWidth(120)
        self.b_fwd5 = self._btn(row, "+5 s", lambda: self.step(STEP_BIG), _("5 Sekunden vor (Shift+→)"))
        row.addStretch()
        return row

    def _clip_card(self):
        """The clip: its range, size and what saving does to it; "Clip ansehen", start/end/mark."""
        clip_card, cl = self._card(_("Clip"))
        self.range_label = QLabel("")
        self.range_label.setProperty("class", "big")
        cl.addWidget(self.range_label)
        self.size_label = QLabel("")
        self.size_label.setProperty("class", "dim")
        self.size_label.setWordWrap(True)
        cl.addWidget(self.size_label)
        wr = QHBoxLayout()
        self.watch_btn = self._btn(wr, _("▶ Clip ansehen"), self.watch_clip,
                                   _("Spielt genau den Ausschnitt ab und springt danach an seinen Anfang zurück."))
        self._btn(wr, _("Start setzen"), self.set_start, _("Der Clip beginnt am Abspielkopf (Taste I)."))
        self._btn(wr, _("Ende setzen"), self.set_end, _("Der Clip endet am Abspielkopf (Taste O)."))
        self.mark_btn = self._btn(wr, _("Zur Marke ▸"), self.next_mark, _("Springt zur nächsten F8-Marke (Taste M)."))
        self.mark_btn.setEnabled(bool(self.marks))
        wr.addStretch()
        cl.addLayout(wr)
        return clip_card

    def _save_card(self, mode):
        """Name, format (target size / GIF height) and the playback-sound box in one row, the encoding, the sources
        on/off, save / show / big editor with the status beside them."""
        export_card, el = self._card(_("Speichern"))
        row2 = QHBoxLayout()
        row2.addWidget(QLabel(_("Name")))
        self.name_edit = QLineEdit()
        row2.addWidget(self.name_edit, 1)
        el.addLayout(row2)
        fmt = QHBoxLayout()
        fmt.addWidget(QLabel(_("Format")))
        self._mode_boxes(mode)
        fmt.addWidget(self.mode_box)
        fmt.addWidget(self.target_box)
        fmt.addWidget(self.gif_box)
        fmt.addWidget(self.sound_box)
        fmt.addStretch()
        el.addLayout(fmt)
        el.addLayout(self._encoding_row())                                          # 1.15: encoder, quality, size
        el.addLayout(self._mix_row(stacked=False))                                  # 1.8.6: the sound mix
        row3 = QHBoxLayout()
        self.save_btn = self._btn(row3, _("Clip speichern"), self.save, _("Schreibt den Ausschnitt als MP4 in den Ordner „Clips“ neben den Aufnahmen."))
        self.save_btn.setObjectName("primary")
        self.show_btn = self._btn(row3, _("Im Explorer zeigen"), self._show_saved, _("Zeigt den zuletzt gespeicherten Clip im Explorer."))
        self.show_btn.setEnabled(False)
        self.expand_btn = self._btn(row3, _("Grosser Editor …"), self._expand,
                                    _("Öffnet den Clip im eigenen Fenster – mit Zensieren, Lautstärke je Tonquelle "
                                      "und allen Tasten."))
        self.status = QLabel("")
        self.status.setProperty("class", "dim")
        self.status.setWordWrap(True)
        row3.addWidget(self.status, 1)
        el.addLayout(row3)
        return export_card

    def _expand(self):
        """1.8.8: compact preview → the full editor (same range and position); this one stops playing."""
        if self.playing:
            self._play_to = None
            self._stop_player()
        if self.on_expand is not None:
            self.on_expand(self.timeline.start, self.timeline.end, self.timeline.pos)

    # ---- the plan and the position
    def edit_plan(self) -> clipedit.Edit:
        """What will be saved: the start/end range (no crop, drawings or fades beside the tables)."""
        tl = self.timeline
        return clipedit.Edit([clipedit.Part(tl.start, tl.end, 1.0)], None, [], 0.0, 0.0)

    def goto(self, t: float):
        """The playhead to source second ``t``: stops a playback, asks the scrub thread for the picture."""
        if self.playing:
            self._stop_player()
        t = min(max(0.0, float(t)), self.info.duration or 0.0)
        self.timeline.set_position(t)
        self.preview.set_now(t)
        self._show_pos()
        self._scrub(t)

    def _segments(self) -> list:
        start = self.timeline.pos
        end = self.timeline.end if start < self.timeline.end - 0.05 else self.info.duration
        return [(start, end, 1.0, start)]

    def _played_at(self, t):
        self.timeline.set_position(t)

    def _after_playing(self, back):
        self.goto(back if back is not None else self.timeline.pos)

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

    def watch_clip(self):
        """1.6.1: play the clip as it will be saved – from its start to its end, then back to its start."""
        tl = self.timeline
        self.goto(tl.start)
        self._play_to = tl.start
        self.toggle_play()

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

    # ---- keys
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
        elif k == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(e)
