"""The editor's timeline (1.16, user: "eine echte Timeline wie in DaVinci Resolve / CapCut, keine tabellenartige
Darstellung"): a ruler, a video track with the clips' thumbnails and an audio track with their waveform, the
playhead, the F8 marks, zoom and horizontal scrolling. Clips are selected with a click, moved by dragging, trimmed
at their edges, split at the playhead; everything the user does comes out as a signal with the new list of parts
– the window keeps the parts (and the undo history), the timeline only shows them (``set_parts``).

All arithmetic on the parts is sequence.py (pure, tested); here is the painting and the mouse."""
from __future__ import annotations

from PySide6.QtCore import QMimeData, QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPainterPath, QPen, QPixmap, QPolygonF
from PySide6.QtWidgets import QApplication, QMenu, QSizePolicy, QWidget

from . import clipedit, qt_theme, sequence
from .i18n import _

MIME = "application/x-fogscout-media"          # a library row dragged onto the timeline (its path as text)
HEAD_W = 56                                    # px: the track names at the left
RULER_H = 26
V_H, A_H = 64, 40                              # px: the two tracks (the video track grows with the panel, up to V_MAX)
V_MAX = 120
GAP = 3                                        # px between the tracks
EDGE = 7                                       # px from a clip's edge that trims instead of moving
MIN_SCALE, MAX_SCALE = 0.02, 600.0             # px per second
ZOOM_STEP = 1.4
PAD_END_S = 2.0                                # seconds of room after the last clip at "fit"
SNAP_PX = 6                                    # a trimmed edge snaps to the playhead / a mark this close
CLIP_COLOURS = {True: {"video": "#355a80", "audio": "#2f6b4c", "text": "#ffffff", "label": QColor(0, 0, 0, 110)},
                False: {"video": "#a9c4e2", "audio": "#b4dac2", "text": "#17191c", "label": QColor(255, 255, 255, 140)}}
MARK_COLOUR = "#e8a33d"
PLAYHEAD = "#ffffff"


def _qimage(img) -> QImage:
    img = img.convert("RGB")
    w, h = img.size
    return QImage(img.tobytes(), w, h, w * 3, QImage.Format_RGB888).copy()


class SequenceTimeline(QWidget):
    seek = Signal(float)              # the playhead wanted at this output time
    scrubbed = Signal(float)          # show this source second (a trimmed edge) without moving the playhead
    selected = Signal(object)         # a clip index or None
    edited = Signal(str, object)      # (what, new parts): "trim" / "move" / "split" / "delete" / "speed"
    picked = Signal(str, float, object)   # right-click menu: (ident, output time, clip index or None)
    dropped = Signal(str)             # a media path from the library was dropped here
    viewed = Signal()                 # scale or offset changed (the scroll bar follows)

    def __init__(self, dark=True):
        super().__init__()
        self.dark = dark
        self.parts = []
        self.pos = 0.0                # output time of the playhead
        self.duration = 1.0           # seconds of the recording (the strip's thumbnails span it)
        self.fps = 30.0
        self.marks = []
        self.thumbs = {}
        self.n_thumbs = clipedit.THUMBS
        self.view = None              # the game part of each thumbnail (x, y, w, h), None = all of it
        self.wave = []
        self.wave_per_s = clipedit.WAVE_PER_S
        self.scale = 10.0             # px per output second
        self.offset = 0.0             # output second at the left edge of the tracks
        self.auto_fit = True          # keep the whole sequence in view until the user zooms
        self.selection = None
        self.hover = None             # (kind, index) under the mouse: ("edge_start"/"edge_end"/"body", i)
        self._drag = None             # see mousePressEvent
        self._drop_hover = False
        self._menu = None
        self._layer = None            # 1.16.1: (key, QPixmap) of everything but the playhead – playback moves only that
        self.setMinimumHeight(RULER_H + V_H + A_H + GAP + 6)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setAcceptDrops(True)

    # ---- data
    def set_parts(self, parts, keep_selection=True):
        self.parts = list(parts)
        if self.selection is not None and self.selection >= len(self.parts):
            self.selection = None
            self.selected.emit(None)
        if self.auto_fit:
            self.fit()
        self.update()

    def set_duration(self, d: float, fps: float = 30.0):
        self.duration = max(0.1, float(d))
        self.fps = fps or 30.0
        self.update()

    def set_marks(self, marks):
        self.marks = sorted(float(m) for m in marks)
        self.update()

    def set_playhead(self, t: float):
        self.pos = max(0.0, float(t))
        self.update()

    def set_thumb(self, i: int, img):
        self.thumbs[i] = _qimage(img)
        self.update()

    def set_view(self, box):
        self.view = tuple(box) if box else None
        self.update()

    def set_wave(self, bins, per_s: int):
        self.wave = list(bins)
        self.wave_per_s = max(1, int(per_s))
        self.update()

    def select(self, i):
        i = i if i is not None and 0 <= i < len(self.parts) else None
        if i != self.selection:
            self.selection = i
            self.update()
            self.selected.emit(i)

    # ---- zoom and scrolling
    def _track_width(self) -> float:
        return max(1.0, self.width() - HEAD_W - 8)

    def total(self) -> float:
        return sequence.duration(self.parts)

    def fit(self):
        """The whole sequence (plus a little room) across the tracks."""
        span = max(1.0, self.total() + PAD_END_S)
        self.scale = min(MAX_SCALE, max(MIN_SCALE, self._track_width() / span))
        self.offset = 0.0
        self.viewed.emit()
        self.update()

    def zoom(self, factor: float, around_x: float | None = None):
        """Zoom by ``factor`` keeping the moment under ``around_x`` (px) where it is (None: the playhead)."""
        self.auto_fit = False
        x = around_x if around_x is not None else self._x(self.pos)
        t = self._t(x)
        self.scale = min(MAX_SCALE, max(MIN_SCALE, self.scale * factor))
        self.offset = max(0.0, t - (x - HEAD_W) / self.scale)
        self._clamp_offset()
        self.viewed.emit()
        self.update()

    def zoom_in(self):
        self.zoom(ZOOM_STEP)

    def zoom_out(self):
        self.zoom(1 / ZOOM_STEP)

    def zoom_fit(self):
        self.auto_fit = True
        self.fit()

    def max_offset(self) -> float:
        return max(0.0, self.total() + PAD_END_S - self._track_width() / self.scale)

    def set_offset(self, t: float):
        t = min(max(0.0, t), self.max_offset())
        if abs(t - self.offset) > 1e-9:
            self.offset = t
            self.viewed.emit()
            self.update()

    def _clamp_offset(self):
        self.offset = min(max(0.0, self.offset), self.max_offset())

    def ensure_visible(self, t: float):
        """Scroll so output time ``t`` is in view (playback: when the playhead leaves on the right, it comes back
        at the left tenth)."""
        w = self._track_width() / self.scale
        if t < self.offset or t > self.offset + w:
            self.set_offset(t - w * 0.1)

    def resizeEvent(self, e):
        if self.auto_fit:
            self.fit()
        else:
            self._clamp_offset()
            self.viewed.emit()
        super().resizeEvent(e)

    # ---- geometry
    def _x(self, t: float) -> float:
        return HEAD_W + (t - self.offset) * self.scale

    def _t(self, x: float) -> float:
        return max(0.0, self.offset + (x - HEAD_W) / self.scale)

    def _v_h(self) -> float:
        return min(V_MAX, max(V_H, self.height() - RULER_H - 2 - GAP - A_H - 8))

    def _v_rect(self) -> QRectF:
        return QRectF(HEAD_W, RULER_H + 2, self._track_width(), self._v_h())

    def _a_rect(self) -> QRectF:
        return QRectF(HEAD_W, RULER_H + 2 + self._v_h() + GAP, self._track_width(), A_H)

    def clip_rect(self, i: int, lane: str = "video") -> QRectF:
        """Where clip ``i`` lies on the video (or audio) track, in widget px."""
        st = sequence.starts(self.parts)
        lane_r = self._v_rect() if lane == "video" else self._a_rect()
        x0, x1 = self._x(st[i]), self._x(st[i + 1])
        return QRectF(x0, lane_r.top(), max(1.0, x1 - x0), lane_r.height())

    def _hit(self, pt) -> tuple:
        """("ruler" | "edge_start" | "edge_end" | "body" | "lane" | "head" | None, clip index or None)."""
        x, y = pt.x(), pt.y()
        if x < HEAD_W:
            return "head", None
        if y < RULER_H:
            return "ruler", None
        lanes = (self._v_rect(), self._a_rect())
        if not any(r.top() <= y <= r.bottom() for r in lanes):
            return None, None
        for i in range(len(self.parts)):
            r = self.clip_rect(i)
            if r.left() - EDGE <= x <= r.right() + EDGE:
                if abs(x - r.left()) <= EDGE and (i == 0 or x >= r.left()):
                    return "edge_start", i
                if abs(x - r.right()) <= EDGE and (i == len(self.parts) - 1 or x <= r.right()):
                    return "edge_end", i
                if r.left() <= x <= r.right():
                    return "body", i
        return "lane", None

    # ---- painting
    def _layer_key(self) -> tuple:
        return (self.width(), self.height(), round(self.scale, 6), round(self.offset, 6),
                tuple((p.start, p.end, p.speed) for p in self.parts), self.selection, self.hover, len(self.thumbs),
                len(self.wave), self.view, tuple(self.marks), self.dark, self.devicePixelRatioF(),
                tuple(sorted(qt_theme.colours(self.dark).items())))   # post-review: a theme change redraws

    def paintEvent(self, e):
        """1.16.1 (audit, measured 9.9 ms per repaint at 30 fps = a third of a core): the tracks, ruler and head
        are drawn into a pixmap once per state and only blitted while just the playhead moves; a drag (trim, move,
        drop) paints live as before."""
        c = qt_theme.colours(self.dark)
        cc = CLIP_COLOURS[bool(self.dark)]
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        live = (self._drag is not None and self._drag[0] in ("trim_start", "trim_end", "move")) or self._drop_hover
        if live:
            self._paint_tracks(p, c, cc)
        else:
            key = self._layer_key()
            if self._layer is None or self._layer[0] != key:
                ratio = self.devicePixelRatioF()
                pm = QPixmap(int(self.width() * ratio), int(self.height() * ratio))
                pm.setDevicePixelRatio(ratio)
                pm.fill(Qt.transparent)
                lp = QPainter(pm)
                lp.setRenderHint(QPainter.Antialiasing)
                self._paint_tracks(lp, c, cc)
                lp.end()
                self._layer = (key, pm)
            p.drawPixmap(0, 0, self._layer[1])
        p.setClipRect(QRectF(HEAD_W, 0, self._track_width(), self.height()))
        self._paint_playhead(p, c)
        p.end()

    def _paint_tracks(self, p, c, cc):
        p.fillRect(self.rect(), QColor(c["panel"]))
        vr, ar = self._v_rect(), self._a_rect()
        for r in (vr, ar):
            p.fillRect(r, QColor(c["field"]))
        p.setClipRect(QRectF(HEAD_W, 0, self._track_width(), self.height()))
        self._paint_ruler(p, c)
        parts = self._drag[2] if self._drag and self._drag[0] in ("trim_start", "trim_end") else self.parts
        st = sequence.starts(parts)
        for i, part in enumerate(parts):
            x0, x1 = self._x(st[i]), self._x(st[i + 1])
            if x1 < HEAD_W or x0 > self.width():
                continue
            ghost = self._drag and self._drag[0] == "move" and self._drag[1] == i
            self._paint_clip(p, c, cc, i, part, QRectF(x0, vr.top(), x1 - x0, vr.height()),
                             QRectF(x0, ar.top(), x1 - x0, ar.height()), faded=bool(ghost))
        if self._drag and self._drag[0] == "move":
            self._paint_move(p, c, cc, st)
        if self._drop_hover:                                     # a library row over the tracks
            pen = QPen(QColor(c["accent"]), 2, Qt.DashLine)
            p.setPen(pen)
            p.setBrush(Qt.NoBrush)
            p.drawRoundedRect(vr.adjusted(1, 1, -1, -1), 4, 4)
        p.setClipping(False)
        self._paint_head(p, c)

    def _paint_head(self, p, c):
        """The track names at the left."""
        p.fillRect(QRectF(0, 0, HEAD_W, self.height()), QColor(c["panel"]))
        p.setPen(QPen(QColor(c["border"]), 1))
        p.drawLine(QPointF(HEAD_W - 0.5, 0), QPointF(HEAD_W - 0.5, self.height()))
        font = QFont(self.font())
        font.setPixelSize(11)
        font.setBold(True)
        p.setFont(font)
        p.setPen(QColor(c["dim"]))
        for name, r in (("V1", self._v_rect()), ("A1", self._a_rect())):
            p.drawText(QRectF(0, r.top(), HEAD_W - 10, r.height()), Qt.AlignRight | Qt.AlignVCenter, name)

    def _paint_ruler(self, p, c):
        step, minor = sequence.ruler_step(self.scale)
        font = QFont(self.font())
        font.setPixelSize(11)
        p.setFont(font)
        first = int(self.offset // step)
        last = int(self._t(self.width()) // step) + 1
        dim = QColor(c["dim"])
        tick = QColor(c["border"])
        for k in range(first, last + 1):
            t = k * step
            x = self._x(t)
            p.setPen(QPen(tick, 1))
            p.drawLine(QPointF(x, RULER_H - 9), QPointF(x, RULER_H))
            for m in range(1, minor):
                xm = self._x(t + step * m / minor)
                p.drawLine(QPointF(xm, RULER_H - 4), QPointF(xm, RULER_H))
            p.setPen(dim)
            p.drawText(QRectF(x + 4, 2, 70, RULER_H - 8), Qt.AlignLeft | Qt.AlignVCenter, sequence.fmt_ruler(t, step))
        p.setPen(QPen(tick, 1))
        p.drawLine(QPointF(HEAD_W, RULER_H - 0.5), QPointF(self.width(), RULER_H - 0.5))
        total = self.total()                                          # the end of the sequence
        xe = self._x(total)
        p.setPen(QPen(QColor(c["dim"]), 1, Qt.DotLine))
        p.drawLine(QPointF(xe, RULER_H), QPointF(xe, self.height()))
        mark = QColor(MARK_COLOUR)
        p.setPen(Qt.NoPen)
        p.setBrush(mark)
        for m in self.marks:                                          # F8 marks wherever their moment plays
            for t in sequence.occurrences(self.parts, m):
                x = self._x(t)
                p.drawPolygon(QPolygonF([QPointF(x - 4, RULER_H - 14), QPointF(x + 4, RULER_H - 14),
                                         QPointF(x, RULER_H - 7)]))

    def _paint_clip(self, p, c, cc, i, part, vrect, arect, faded=False):
        sel = i == self.selection
        video, audio = QColor(cc["video"]), QColor(cc["audio"])
        if faded:
            video.setAlpha(90)
            audio.setAlpha(90)
        for r, col in ((vrect, video), (arect, audio)):
            p.setPen(Qt.NoPen)
            p.setBrush(col)
            p.drawRoundedRect(r.adjusted(0.5, 0.5, -0.5, -0.5), 3, 3)
        if not faded:
            self._paint_thumbs(p, vrect, part)
            self._paint_wave(p, arect, part, audio)
        # the label strip: number and tempo
        font = QFont(self.font())
        font.setPixelSize(11)
        font.setBold(True)
        p.setFont(font)
        label = QRectF(vrect.left(), vrect.top(), vrect.width(), 16).adjusted(0.5, 0.5, -0.5, 0)
        p.setClipRect(vrect.adjusted(0, 0, -0.5, 0), Qt.IntersectClip)
        p.fillRect(label, cc["label"])
        p.setPen(QColor(cc["text"]))
        tempo = "" if abs(part.speed - 1.0) < 1e-6 else f"   ×{part.speed:g}"
        p.drawText(label.adjusted(6, 0, -4, 0), Qt.AlignLeft | Qt.AlignVCenter,
                   f"{i + 1}  {clipedit.fmt_pos(part.start)} – {clipedit.fmt_pos(part.end)}{tempo}")
        p.setClipRect(QRectF(HEAD_W, 0, self._track_width(), self.height()))
        pen = QPen(QColor(c["accent"]) if sel else QColor(0, 0, 0, 120), 2 if sel else 1)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        for r in (vrect, arect):
            p.drawRoundedRect(r.adjusted(1, 1, -1, -1) if sel else r.adjusted(0.5, 0.5, -0.5, -0.5), 3, 3)
        if sel or (self.hover and self.hover[1] == i and self.hover[0].startswith("edge")):
            p.setPen(Qt.NoPen)                                        # the trim handles
            p.setBrush(QColor(c["accent"]) if sel else QColor(255, 255, 255, 170))
            for x in (vrect.left() + 1, vrect.right() - 4):
                p.drawRoundedRect(QRectF(x, vrect.top() + 18, 3, vrect.height() - 22), 1.5, 1.5)

    def _paint_thumbs(self, p, r, part):
        img = next(iter(self.thumbs.values()), None)
        if img is None or r.width() < 4:
            return
        vx, vy, vw, vh = self.view or (0.0, 0.0, 1.0, 1.0)
        tile_h = r.height() - 16                                      # below the label strip
        tile_w = max(8.0, tile_h * img.width() * vw / max(1.0, img.height() * vh))
        src_per_tile = tile_w / self.scale * part.speed
        p.setClipRect(QRectF(r.left() + 0.5, r.top() + 16, r.width() - 1, tile_h), Qt.IntersectClip)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        left = max(r.left(), HEAD_W)
        j = int((left - r.left()) // tile_w)
        x = r.left() + j * tile_w
        while x < min(r.right(), self.width()) and x < r.right():
            src = part.start + (j + 0.5) * src_per_tile
            idx = min(self.n_thumbs - 1, max(0, int(src / self.duration * self.n_thumbs)))
            im = self.thumbs.get(idx)
            if im is not None:
                p.drawImage(QRectF(x, r.top() + 16, tile_w, tile_h),
                            im, QRectF(im.width() * vx, im.height() * vy, im.width() * vw, im.height() * vh))
            x += tile_w
            j += 1
        p.setClipRect(QRectF(HEAD_W, 0, self._track_width(), self.height()))

    def _paint_wave(self, p, r, part, fill):
        if not self.wave or r.width() < 2:
            return
        mid = r.center().y()
        half = r.height() / 2 - 3
        col = QColor(fill).lighter(160 if self.dark else 85)
        col.setAlpha(230)
        p.setPen(QPen(col, 1))
        left, right = max(int(r.left()) + 1, HEAD_W), min(int(r.right()), self.width())
        per_px = part.speed / self.scale                              # source seconds under one pixel
        n = len(self.wave)
        for x in range(left, right):
            s0 = part.start + (x - r.left()) * per_px
            b0 = int(s0 * self.wave_per_s)
            b1 = max(b0 + 1, int((s0 + per_px) * self.wave_per_s))
            if b0 >= n:
                break
            v = max(self.wave[b0:min(n, b1)], default=0.0)
            h = max(1.0, v * half)
            p.drawLine(QPointF(x + 0.5, mid - h), QPointF(x + 0.5, mid + h))

    def _paint_move(self, p, c, cc, st):
        """The dragged clip as a ghost under the mouse and the insertion line where it will land."""
        _k, i, _parts, x_off, x_now = self._drag
        part = self.parts[i]
        w = sequence.length(part) * self.scale
        x = x_now - x_off
        vr = self._v_rect()
        ghost = QRectF(x, vr.top(), w, vr.height() + GAP + A_H)   # both tracks
        col = QColor(cc["video"])
        col.setAlpha(170)
        p.setPen(QPen(QColor(c["accent"]), 1))
        p.setBrush(col)
        p.drawRoundedRect(ghost, 4, 4)
        j = sequence.drop_index(self.parts, i, self._t(x))
        others = [k for k in range(len(self.parts)) if k != i]
        xi = self._x(sum(sequence.length(self.parts[k]) for k in others[:j]))   # the sequence without the clip
        p.setPen(QPen(QColor(c["accent"]), 3))
        p.drawLine(QPointF(xi, vr.top() - 2), QPointF(xi, self._a_rect().bottom() + 2))

    def _paint_playhead(self, p, c):
        x = self._x(self.pos)
        if x < HEAD_W - 1:
            return
        p.setPen(QPen(QColor(PLAYHEAD), 1.5))
        p.drawLine(QPointF(x, RULER_H - 8), QPointF(x, self.height()))
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(PLAYHEAD))
        path = QPainterPath()
        path.moveTo(x - 6, 4)
        path.lineTo(x + 6, 4)
        path.lineTo(x + 6, RULER_H - 12)
        path.lineTo(x, RULER_H - 6)
        path.lineTo(x - 6, RULER_H - 12)
        path.closeSubpath()
        p.drawPath(path)

    # ---- mouse
    def _cursor_for(self, kind):
        if kind in ("edge_start", "edge_end"):
            return Qt.SizeHorCursor
        if kind == "body":
            return Qt.OpenHandCursor
        if kind in ("ruler", "lane"):
            return Qt.PointingHandCursor
        return Qt.ArrowCursor

    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return
        pt = e.position()
        kind, i = self._hit(pt)
        if kind == "ruler" or kind == "lane":
            self._drag = ("seek",)
            if kind == "lane":
                self.select(None)
            self.seek.emit(self._t(pt.x()))
        elif kind in ("edge_start", "edge_end"):
            self.select(i)
            self._drag = ("trim_start" if kind == "edge_start" else "trim_end", i, list(self.parts))
            self.setCursor(Qt.SizeHorCursor)
        elif kind == "body":
            self.select(i)
            r = self.clip_rect(i)
            self._drag = ("press", i, pt.x() - r.left(), pt.x(), pt)
            self.setCursor(Qt.ClosedHandCursor)
        e.accept()

    def mouseMoveEvent(self, e):
        pt = e.position()
        if self._drag is None:
            kind, i = self._hit(pt)
            hover = (kind, i) if kind in ("edge_start", "edge_end", "body") else None
            if hover != self.hover:
                self.hover = hover
                self.update()
            self.setCursor(self._cursor_for(kind))
            return
        kind = self._drag[0]
        if kind == "seek":
            self.seek.emit(self._t(pt.x()))
        elif kind in ("trim_start", "trim_end"):
            _k, i, _orig = self._drag
            self._trim_to(i, kind, pt.x())
        elif kind == "press":
            _k, i, x_off, x0, p0 = self._drag
            if (pt - p0).manhattanLength() >= QApplication.startDragDistance():
                self._drag = ("move", i, list(self.parts), x_off, pt.x())
                self.update()
        elif kind == "move":
            self._drag = self._drag[:4] + (pt.x(),)
            self.update()

    def _trim_to(self, i, kind, x):
        """The edge of clip ``i`` under the mouse, snapped to the playhead or a mark when close."""
        part = self.parts[i]
        st = sequence.starts(self.parts)
        if kind == "trim_start":
            out = self._t(x)
            src = part.start + (out - st[i]) * part.speed               # the clip's left edge in source seconds
        else:
            out = self._t(x)
            src = part.start + (out - st[i]) * part.speed
        src = self._snap(src, part, kind)
        new = sequence.trim(self.parts, i, "start" if kind == "trim_start" else "end", src, self.duration)
        self._drag = (kind, i, new)
        edge = new[i].start if kind == "trim_start" else new[i].end
        self.scrubbed.emit(edge)
        self.update()

    def _snap(self, src, part, kind) -> float:
        """Source second ``src`` pulled onto the playhead's source moment or an F8 mark within SNAP_PX."""
        tol = SNAP_PX / self.scale * part.speed
        targets = list(self.marks)
        pi, psrc = sequence.source_at(self.parts, self.pos)
        if pi is not None:
            targets.append(psrc)
        for t in targets:
            if abs(t - src) <= tol:
                return t
        return src

    def mouseReleaseEvent(self, e):
        drag, self._drag = self._drag, None
        self.setCursor(Qt.ArrowCursor)
        if not drag:
            return
        kind = drag[0]
        if kind in ("trim_start", "trim_end"):
            _k, i, new = drag
            if new != self.parts:
                self.edited.emit("trim", new)
        elif kind == "move":
            _k, i, _parts, x_off, x_now = drag
            j = sequence.drop_index(self.parts, i, self._t(x_now - x_off))
            if j != i:
                new = sequence.move(self.parts, i, j)
                self.selection = j
                self.edited.emit("move", new)
                self.selected.emit(j)
        self.update()

    def mouseDoubleClickEvent(self, e):
        kind, i = self._hit(e.position())
        if kind == "body" and i is not None:
            self.seek.emit(sequence.starts(self.parts)[i])

    def leaveEvent(self, e):
        if self.hover is not None:
            self.hover = None
            self.update()
        super().leaveEvent(e)

    def wheelEvent(self, e):
        d = e.angleDelta().y() or e.angleDelta().x()
        if not d:
            return
        if e.modifiers() & Qt.ControlModifier:
            self.zoom(ZOOM_STEP if d > 0 else 1 / ZOOM_STEP, e.position().x())
        else:
            self.auto_fit = False
            self.set_offset(self.offset - d / 120.0 * (self._track_width() / self.scale) * 0.1)
        e.accept()

    def contextMenuEvent(self, e):
        kind, i = self._hit(e.pos())
        if kind in ("head", None):
            return
        t = self._t(e.pos().x())
        menu = QMenu(self)
        menu.setAttribute(Qt.WA_DeleteOnClose)                   # 1.16.1: else every right click stays a child
        if kind in ("body", "edge_start", "edge_end") and i is not None:
            self.select(i)
            menu.addAction(_("Hier teilen")).triggered.connect(lambda _c=False: self.picked.emit("split", t, i))
            menu.addAction(_("Clip beginnt hier")).triggered.connect(lambda _c=False: self.picked.emit("start", t, i))
            menu.addAction(_("Clip endet hier")).triggered.connect(lambda _c=False: self.picked.emit("end", t, i))
            tempo = menu.addMenu(_("Tempo"))
            for speed in clipedit.SPEEDS:
                act = tempo.addAction(_("normal") if speed == 1.0 else f"×{speed:g}")
                act.setCheckable(True)
                act.setChecked(abs(self.parts[i].speed - speed) < 1e-6)
                act.triggered.connect(lambda _c=False, s=speed: self.picked.emit("speed", s, i))
            menu.addAction(_("Clip löschen")).triggered.connect(lambda _c=False: self.picked.emit("delete", t, i))
            menu.addSeparator()
        menu.addAction(_("Abspielkopf hierher")).triggered.connect(lambda _c=False: self.picked.emit("seek", t, i))
        menu.addAction(_("Standbild hier speichern")).triggered.connect(lambda _c=False: self.picked.emit("still", t, i))
        menu.addSeparator()
        menu.addAction(_("Zeitleiste einpassen")).triggered.connect(lambda _c=False: self.zoom_fit())
        self._menu = menu
        menu.popup(e.globalPos())

    # ---- drag and drop from the library
    @staticmethod
    def mime_path(mime: QMimeData) -> str:
        if mime.hasFormat(MIME):
            return bytes(mime.data(MIME)).decode("utf-8", "replace")
        if mime.hasUrls():
            for url in mime.urls():
                if url.isLocalFile():
                    return url.toLocalFile()
        return ""

    def dragEnterEvent(self, e):
        if self.mime_path(e.mimeData()):
            self._drop_hover = True
            self.update()
            e.acceptProposedAction()

    def dragMoveEvent(self, e):
        if self.mime_path(e.mimeData()):
            e.acceptProposedAction()

    def dragLeaveEvent(self, e):
        self._drop_hover = False
        self.update()

    def dropEvent(self, e):
        self._drop_hover = False
        self.update()
        path = self.mime_path(e.mimeData())
        if path:
            e.acceptProposedAction()
            self.dropped.emit(path)
