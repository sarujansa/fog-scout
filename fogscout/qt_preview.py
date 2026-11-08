"""The overlay preview (1.61): the screen with the game picture and bars, every element as a picture; clicks and drags
in edit mode place, pick and size them.
"""
from __future__ import annotations

import time

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QSizePolicy, QWidget

from . import qt_theme
from .i18n import N_, _
from .qt_common import pixmap_from_pil


PREVIEW_NAMES = {"map": N_("Karte"), "hud": N_("Systemwerte"), "today": N_("Heute"), "music": N_("Musik"),
                 "text": N_("Infos"), "inputs": N_("Eingaben")}     # 1.8.24: the map's lines apart; 1.39
NOTE_H = 40                      # 1.8.8: the strip below the screen for the note while moving


class PreviewView(QWidget):
    """The overlay tab's screen (since 1.61): the monitor in its shape, the 16:9 game picture with its black bars
    and the map on it where and as big as it will be, with its opacity and the lines below it. A click or a drag
    puts the map there: post("act", (key, ("move", x, y))) in screen pixels – the App makes it the own position."""

    MAX_H = 380
    # 1.46: what the mouse does over the canvas, for the overlay editor's status line (GUI thread only)
    status_changed = Signal(dict)

    def __init__(self, key, post):
        super().__init__()
        self._key, self._post = key, post
        self._fill = False                     # 1.46: the overlay editor's canvas – as big as its place, no cap
        self._status = None                    # the last status sent (status_changed only on a change)
        self._data = {}
        self._pix = None                       # (picture object, size) -> QPixmap
        self._dragging = False
        self._grab = None                      # (layer name, dx, dy) while an element is dragged
        self._hover = None                     # layer under the mouse while moving (1.64.7)
        self._sizing = None                    # (layer name, x, y, w, h) while its corner is dragged (1.64.9)
        self._snapped = (None, None)           # lines the dragged element snapped to (1.65), drawn as guides
        self._held = None                      # (name, x, y, since) drawn at once (1.65.2, user: it jumped)
        self._limit = None                     # (side, "top"/"bottom") while a limiter line is dragged (1.8.14)
        self._limit_y = None                   # … and where the mouse has it (screen px), drawn at once
        self._snap_from = ()                   # 1.44.2: the other elements' places when the drag began (snapping)
        self._answered = False                 # 1.44.2: the App sent places since the drag began (landing frame)
        self._boxes = {}                       # 1.44.2: id(picture) -> visible part as shares (hit testing)
        self.setFocusPolicy(Qt.ClickFocus)     # arrow keys after a click (1.65)
        self.setMouseTracking(True)            # open hand over an element
        sp = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sp.setHeightForWidth(True)
        self.setSizePolicy(sp)
        self.setMinimumHeight(120)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(_("Klick auf ein Element wählt es. Mit „Anordnen“: Element ziehen = verschieben (der "
                          "gestrichelte Rahmen zeigt, wo es landet), an der Ecke ziehen oder Strg+Mausrad = Grösse, "
                          "Rechtsklick = Menü. Ende mit „Fertig“ oder Esc."))

    def set_fill(self, on: bool = True):
        """1.46 (user: "das Overlay-Fenster ist sehr klein"): in the overlay editor the canvas takes all the room it
        gets – no height cap, no note strip (the editor's status line says it); the setup page keeps the old view."""
        self._fill = bool(on)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFocusPolicy(Qt.StrongFocus)            # Tab picks the next element (event below)
        self.setMinimumSize(240, 140)
        self.updateGeometry()

    def hasHeightForWidth(self):
        return not self._fill

    def heightForWidth(self, w):
        sw, sh = self._data.get("screen") or (16, 9)
        return min(self.MAX_H, max(120, round(w * sh / max(1, sw)))) + self._note_h()

    def _note_h(self) -> int:
        """1.8.8: in moving mode a strip below the screen holds the note (over the picture it hid the music card)."""
        return NOTE_H if self._data.get("editing") and not self._fill else 0

    def sizeHint(self):
        if self._fill:
            return QSize(720, 400)
        return QSize(560, self.heightForWidth(560))

    def _send_status(self):
        """1.46: hover / held element / snap lines / moving mode → status_changed, only when something changed."""
        d = self._data
        st = {"hover": self._hover, "grab": self._grab[0] if self._grab else None,
              "sizing": self._sizing[0] if self._sizing else None,
              "snapped": self._snapped != (None, None) and bool(self._grab), "limit": bool(self._limit),
              "editing": bool(d.get("editing")), "selected": d.get("selected"),
              "locked": tuple(d.get("locked") or ()), "layout_key": d.get("layout_key") or "",
              "limits_off": bool(d.get("limits") and not d.get("limits_on", True))}
        if st != self._status:
            self._status = st
            self.status_changed.emit(dict(st))

    def _locked(self, name) -> bool:
        return name in (self._data.get("locked") or ())

    def show_state(self, st):
        data = st.get("data") or {}
        key = {k: v for k, v in data.items() if k != "pics"}
        old = {k: v for k, v in self._data.items() if k != "pics"}
        pics, old_pics = data.get("pics") or {}, self._data.get("pics") or {}
        if key == old and pics.keys() == old_pics.keys() and all(pics[k] is old_pics[k] for k in pics):
            return
        shape = data.get("screen") != self._data.get("screen") or \
            bool(data.get("editing")) != bool(self._data.get("editing"))
        self._data = data
        if self._grab:                         # 1.44.2: these places already follow the drag
            self._answered = True
        if self._held and not self._grab:      # dropped: the App's own place counts again
            self._held = None
        if shape:
            self.updateGeometry()
        self.update()
        self._send_status()

    def _frame(self):
        """(left, top, scale): where the screen is drawn in the widget, screen px -> widget px."""
        sw, sh = self._data.get("screen") or (16, 9)
        height = self.height() - self._note_h()
        s = min(self.width() / max(1, sw), height / max(1, sh))
        return (self.width() - sw * s) / 2, (height - sh * s) / 2, s

    def paintEvent(self, _e):
        from PySide6.QtCore import QPointF, QRectF
        from PySide6.QtGui import QFont, QPainter, QPen
        d = self._data
        if not d.get("screen"):
            return
        sw, sh = d["screen"]
        ox, oy, s = self._frame()
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        screen = QRectF(ox, oy, sw * s, sh * s)
        p.setPen(QPen(QColor("#4a4d55"), 1))
        p.setBrush(QColor("#050506"))
        p.drawRoundedRect(screen.adjusted(-1, -1, 1, 1), 4, 4)
        bar = d.get("bar", 0) * s
        game = QRectF(ox + bar, oy, sw * s - 2 * bar, sh * s)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#2b3036"))
        p.drawRect(game)
        p.setPen(QColor("#9aa1ab"))                # 1.25: 5.1:1 on the game picture (was 2.2:1)
        f = QFont(self.font())
        f.setPointSizeF(max(7.0, f.pointSizeF() * 0.9))
        p.setFont(f)
        if not d.get("editing"):                   # moving: the centre cross is there
            p.drawText(game, Qt.AlignCenter, _("Spielbild"))
        # every element as the game shows it (1.64): map + lines, system values, music card – real pictures
        pics = d.get("pics") or {}
        ratio = self.devicePixelRatioF()
        cache = self._pix if isinstance(self._pix, dict) else {}
        fresh = {}
        ops = d.get("opacities") or {}
        for name, lx, ly, lw, lh in self._layers():
            img = pics.get(name)
            if img is None:
                continue
            p.setOpacity(float(ops.get(name, d.get("opacity", 1.0))))     # per element (1.2.7)
            th = max(1, round(lh * s))
            hit = cache.get(name)
            pix = hit[2] if hit and hit[0] is img and hit[1] == th else pixmap_from_pil(img, th, ratio)
            fresh[name] = (img, th, pix)
            p.drawPixmap(round(ox + lx * s), round(oy + ly * s), pix)
        self._pix = fresh
        p.setOpacity(1.0)
        self._paint_zones(p, ox, oy, s)
        self._paint_limits(p, ox, oy, s)
        if d.get("editing"):                       # moving is on: a frame round the screen and a note
            accent = QColor(qt_theme.colours(True)["accent"])
            cx, cy = screen.center().x(), screen.center().y()         # centre cross (1.64.5)
            for pen in (QPen(QColor(0, 0, 0, 150), 3), QPen(QColor(255, 255, 255, 220), 1, Qt.DashLine)):
                p.setPen(pen)
                p.drawLine(QPointF(cx, screen.top()), QPointF(cx, screen.bottom()))
                p.drawLine(QPointF(screen.left(), cy), QPointF(screen.right(), cy))
            p.setPen(QPen(accent, 2))
            p.setBrush(Qt.NoBrush)
            p.drawRoundedRect(screen.adjusted(-1, -1, 1, 1), 4, 4)
            nf = QFont(self.font())
            nf.setBold(True)
            p.setFont(nf)
            p.setPen(QColor(qt_theme.colours(qt_theme.current_dark())["accent"]))   # 1.22.3: on the page, not the screen
            # 1.8.8: in its own strip below the screen (1.8.2 put it on the picture, where it hid the music card)
            note = _("Verschieben aktiv – ziehen (rastet ein, Alt = frei), Pfeiltasten = fein, Ecke/Strg+Mausrad = "
                     "Grösse, Rechtsklick = zurücksetzen")
            if d.get("limits") and not d.get("limits_on", True):       # 1.8.15: the faint limiter lines
                note += "\n" + _("Graue Linien in den Balken = Grenzen (aus) – eine ziehen schaltet sie ein")
            strip = QRectF(screen.left(), screen.bottom() + 4, screen.width(), self.height() - screen.bottom() - 4)
            if not self._fill:                     # 1.46: the editor says it in its status line
                p.drawText(strip, Qt.AlignHCenter | Qt.AlignTop | Qt.TextWordWrap, note)
        if d.get("editing"):                       # every element named; the one under the mouse in accent colour
            accent = QColor(qt_theme.colours(True)["accent"])
            held = self._grab[0] if self._grab else self._hover
            tf = QFont(self.font())
            tf.setBold(True)
            tf.setPixelSize(11)
            p.setFont(tf)
            rects = {name: QRectF(ox + lx * s, oy + ly * s, lw * s, lh * s).adjusted(-2, -2, 2, 2)   # 1.8.8: off the text
                     for name, lx, ly, lw, lh in self._layers()}
            over = set(d.get("overlaps") or ())    # 1.45: put on another by hand – allowed, but shown
            for name, r in rects.items():
                on = name == held or name == d.get("selected")
                colour = QColor("#ef4444") if name in over else accent if on else QColor(255, 255, 255, 140)
                p.setPen(QPen(colour, 2 if on or name in over else 1, Qt.SolidLine if on else Qt.DashLine))
                p.setBrush(Qt.NoBrush)
                p.drawRect(r)
                tag = _(PREVIEW_NAMES.get(name, name))
                if self._locked(name):             # 1.46: locked – not dragged
                    tag = tag + " · " + _("gesperrt")
                tw = p.fontMetrics().horizontalAdvance(tag) + 8
                tr = QRectF(max(screen.left(), min(r.left(), screen.right() - tw)), max(oy, r.top() - 15), tw, 15)
                if any(tr.intersects(o) for n2, o in rects.items() if n2 != name):
                    tr.moveTop(r.top())               # 1.8.8: no room above (stacked cards): inside its own frame
                p.fillRect(tr, accent if on else QColor(30, 30, 34, 220))
                p.setPen(QColor(20, 16, 4) if on else QColor(235, 235, 235))
                p.drawText(tr, Qt.AlignCenter, tag)
            lx, ly = self._snapped if self._grab else (None, None)
            p.setPen(QPen(accent, 1.5))
            if lx is not None:                     # the line the dragged element snapped to (1.65)
                p.drawLine(QPointF(ox + lx * s, screen.top()), QPointF(ox + lx * s, screen.bottom()))
            if ly is not None:
                p.drawLine(QPointF(screen.left(), oy + ly * s), QPointF(screen.right(), oy + ly * s))
            land = self._landing()
            if land is not None:                   # 1.44.2: where the App puts it (bar, lines, others) – no surprise
                _n, ax, ay, aw, ah = land
                p.setPen(QPen(accent, 1.5, Qt.DashLine))
                p.setBrush(QColor(accent.red(), accent.green(), accent.blue(), 40))
                p.drawRect(QRectF(ox + ax * s, oy + ay * s, aw * s, ah * s))
            sel = self._layer(d.get("selected"))
            if sel and not self._locked(sel[0]):   # the picked element: its corner sizes it (1.64.9)
                hr = self._handle_rect(sel, ox, oy, s)
                p.setPen(QPen(QColor(20, 16, 4), 1))
                p.setBrush(accent)
                p.drawRect(hr)
            if held and not self._fill:
                p.setPen(accent)
                p.setFont(tf)
                what = _("Ziehst: {name}", name=_(PREVIEW_NAMES.get(held, held))) if self._grab else \
                    _("Unter der Maus: {name}", name=_(PREVIEW_NAMES.get(held, held)))
                p.drawText(QRectF(screen.left(), screen.bottom() + 4, screen.width(), self.height() - screen.bottom() - 4),
                           Qt.AlignHCenter | Qt.AlignBottom, what)
        x, y, w, h, _mh = d.get("rect") or (0, 0, 0, 0, 0)
        sel = self._layer(d.get("selected"))
        if sel:                                    # the element the size slider works on (1.64.9)
            _n, x, y, w, h = sel
        hov = self._layer(self._hover) if self._fill and not d.get("editing") else None
        if hov and hov[0] != d.get("selected"):     # 1.46: the element a click would pick
            p.setPen(QPen(QColor(255, 255, 255, 110), 1, Qt.DashLine))
            p.setBrush(Qt.NoBrush)
            p.drawRect(QRectF(ox + hov[1] * s, oy + hov[2] * s, hov[3] * s, hov[4] * s))
        if w and h and not d.get("editing"):
            rx, ry = ox + x * s, oy + y * s
            pen = QPen(QColor(qt_theme.colours(True)["accent"]), 1.5, Qt.DashLine)
            p.setPen(pen)
            p.setBrush(Qt.NoBrush)
            p.drawRect(QRectF(rx, ry, w * s, h * s))
        p.end()

    LIMIT_GRAB = 6                             # px (widget) above/below a limiter line that grab it

    def _limit_lines(self):
        """[(side, which, x0, x1, y)] in screen px: the limiter lines of the black bars (1.8.14) – the one being
        dragged where the mouse has it."""
        d = self._data
        bands, sw, bar = d.get("limits"), (d.get("screen") or (0, 0))[0], d.get("bar", 0)
        if not bands or not bar:
            return []
        held = self._limit if self._limit_y is not None else None
        out = []
        for side, (top, bottom) in bands.items():
            x0, x1 = (0, bar) if side == "left" else (sw - bar, sw)
            for which, y in (("top", top), ("bottom", bottom)):
                if held and held[1] == which and (held[0] == side or d.get("limits_same", False)):
                    y = self._limit_y              # with "both alike" the other bar's line moves along
                out.append((side, which, x0, x1, y))
        return out

    def _paint_zones(self, p, ox, oy, s):
        """1.8.25: the keep-out areas (Discord's overlay widgets) – hatched, so it shows why nothing goes there."""
        from PySide6.QtCore import QRectF
        from PySide6.QtGui import QBrush, QPen
        for x, y, w, h in self._data.get("zones") or ():
            r = QRectF(ox + x * s, oy + y * s, w * s, h * s)
            p.setPen(QPen(QColor(88, 101, 242, 200), 1, Qt.DashLine))          # Discord's blurple
            p.setBrush(QBrush(QColor(88, 101, 242, 70), Qt.BDiagPattern))
            p.drawRect(r)
            if r.width() > 40 and r.height() > 14:
                p.setPen(QColor(200, 205, 255, 220))
                p.drawText(r.adjusted(3, 2, -2, -2), Qt.AlignLeft | Qt.AlignTop, "Discord")
        p.setBrush(Qt.NoBrush)

    def _paint_limits(self, p, ox, oy, s):
        """The limiter lines: dashed in the accent colour, a small tab at the inner end; brighter while moving."""
        from PySide6.QtCore import QPointF, QRectF
        from PySide6.QtGui import QPen
        lines = self._limit_lines()
        if not lines:
            return
        accent = QColor(qt_theme.colours(True)["accent"])
        edit = bool(self._data.get("editing"))
        on = self._data.get("limits_on", True) or self._limit is not None
        if not on:                                 # 1.8.15: switched off – faint grey, dragging one switches it on
            accent = QColor(200, 200, 200)
        for side, which, x0, x1, y in lines:
            a, b, yy = QPointF(ox + x0 * s, oy + y * s), QPointF(ox + x1 * s, oy + y * s), oy + y * s
            p.setPen(QPen(QColor(0, 0, 0, 160), 3))
            p.drawLine(a, b)
            c = QColor(accent)
            c.setAlpha((255 if edit else 170) if on else 110)
            p.setPen(QPen(c, 2 if edit and self._limit == (side, which) else 1.5, Qt.DashLine))
            p.drawLine(a, b)
            if edit:                               # a grip at the end facing the game picture
                gx = (b.x() - 10) if side == "left" else (a.x() + 2)
                p.setPen(Qt.NoPen)
                p.setBrush(c)
                p.drawRoundedRect(QRectF(gx, yy - 4, 8, 8), 2, 2)

    def _limit_at(self, e):
        """(side, which) of the limiter line under the mouse (moving mode only), or None."""
        if not self._data.get("editing"):
            return None
        ox, oy, s = self._frame()
        pos = e.position()
        for side, which, x0, x1, y in self._limit_lines():
            if ox + x0 * s <= pos.x() <= ox + x1 * s and abs(oy + y * s - pos.y()) <= self.LIMIT_GRAB:
                return side, which
        return None

    def contextMenuEvent(self, e):
        """1.8.10: right click on an element: the App shows its quick actions (size, dark area, hide …)."""
        ox, oy, s = self._frame()
        if s <= 0:
            return
        hit = self.layer_at((e.pos().x() - ox) / s, (e.pos().y() - oy) / s)
        if hit is None:
            return
        gp = e.globalPos()
        self._post("act", (self._key, ("menu", hit[0], gp.x(), gp.y())))

    def _screen_pos(self, e):
        ox, oy, s = self._frame()
        pos = e.position()
        return ((pos.x() - ox) / s, (pos.y() - oy) / s) if s > 0 else None

    def _layers(self):
        """The layers as drawn: the one held by the mouse where the mouse has it, not where the App last put it
        (that comes only 4×/s – the element jumped behind the mouse)."""
        held = self._held
        if held and time.monotonic() - held[3] > 1.5 and not self._grab:
            held = self._held = None
        return [(n, held[1], held[2], w, h) if held and n == held[0] else (n, x, y, w, h)
                for n, x, y, w, h in self._data.get("layers") or ()]

    def _layer(self, name):
        return next((lay for lay in self._layers() if lay[0] == name), None)

    LANDING_PX = 3                             # screen px: closer than this, the held place is where it lands

    def _landing(self):
        """1.44.2: while dragging, where the App put the element last (its rules: inside the bar, between the
        lines, off the others) when that differs from the mouse's place – drawn as a dashed frame; None else."""
        if not self._grab or not self._answered:          # before the App's answer: still the old place
            return None
        held = self._layer(self._grab[0])
        app = next((lay for lay in self._data.get("layers") or () if lay[0] == self._grab[0]), None)
        if held is None or app is None:
            return None
        if abs(held[1] - app[1]) <= self.LANDING_PX and abs(held[2] - app[2]) <= self.LANDING_PX:
            return None
        return app

    HANDLE = 16                                # px (widget): the corner that sizes the picked element (1.44.2: 12)

    def _handle_rect(self, layer, ox, oy, s):
        from PySide6.QtCore import QRectF
        _n, lx, ly, lw, lh = layer
        k = self.HANDLE
        return QRectF(ox + (lx + lw) * s - k / 2, oy + (ly + lh) * s - k / 2, k, k)

    def _on_handle(self, e):
        """The picked element when the mouse is on its corner (moving mode only; 1.46: not when locked)."""
        sel = self._layer(self._data.get("selected")) if self._data.get("editing") else None
        if sel is None or self._locked(sel[0]):
            return None
        ox, oy, s = self._frame()
        return sel if self._handle_rect(sel, ox, oy, s).adjusted(-3, -3, 3, 3).contains(e.position()) else None

    def wheelEvent(self, e):
        """Moving mode: Ctrl + wheel over an element sizes it (like over the map in the game); else the page
        scrolls. 1.3.2 (user: "nervt, dass sich die Fenster verstellen, wenn ich mit dem Mausrad drin drehe"):
        the plain wheel never changes a size."""
        ctrl = bool(e.modifiers() & Qt.ControlModifier)
        pt = self._screen_pos(e) if self._data.get("editing") and ctrl else None
        hit = self.layer_at(*pt) if pt else None
        steps = e.angleDelta().y() / 120
        if not hit or not steps or self._locked(hit[0]):
            e.ignore()
            return
        lay = self._layer(hit[0])
        self._post("act", (self._key, ("resize", hit[0], lay[4] * 1.06 ** steps)))
        e.accept()

    HIT_PAD = 6                                # px (widget) around an element's visible part that still hit it
    HIT_MIN = 24                               # px (widget): a hit area is at least this big

    def _visible(self, name):
        """1.44.2: the visible part of an element's picture as shares (x0, y0, x1, y1) – its transparent edge
        (shadow room, a card padded to the column's width) took clicks meant for the element below; cached."""
        img = (self._data.get("pics") or {}).get(name)
        if img is None or getattr(img, "mode", "") != "RGBA":
            return 0.0, 0.0, 1.0, 1.0
        hit = self._boxes.get(id(img))
        if hit is None or hit[0] is not img:
            box = img.getchannel("A").point(lambda a: 255 if a > 24 else 0).getbbox()
            w, h = max(1, img.width), max(1, img.height)
            share = (box[0] / w, box[1] / h, box[2] / w, box[3] / h) if box else (0.0, 0.0, 1.0, 1.0)
            if len(self._boxes) > 32:
                self._boxes.clear()
            hit = self._boxes[id(img)] = (img, share)
        return hit[1]

    def _hit_rect(self, layer):
        """Screen-px rectangle that takes the mouse for ``layer``: its visible part, a little wider, never tiny."""
        name, lx, ly, lw, lh = layer
        s = max(1e-6, self._frame()[2])
        x0, y0, x1, y1 = self._visible(name)
        pad, least = self.HIT_PAD / s, self.HIT_MIN / s
        left, top, right, bottom = lx + x0 * lw - pad, ly + y0 * lh - pad, lx + x1 * lw + pad, ly + y1 * lh + pad
        if right - left < least:
            mid = (left + right) / 2
            left, right = mid - least / 2, mid + least / 2
        if bottom - top < least:
            mid = (top + bottom) / 2
            top, bottom = mid - least / 2, mid + least / 2
        return left, top, right, bottom

    def layer_at(self, x, y):
        """(name, dx, dy) of the topmost element under screen point (x, y), or None (1.64.1). 1.44.2: by its
        visible part (``_hit_rect``), not its whole picture."""
        for lay in reversed(self._layers()):
            left, top, right, bottom = self._hit_rect(lay)
            if left <= x <= right and top <= y <= bottom:
                return lay[0], x - lay[1], y - lay[2]
        return None

    def _move(self, e):
        pt = self._screen_pos(e)
        if pt is None:
            return
        if self._grab:                     # an element held at the place it was grabbed: its corner follows
            name, dx, dy = self._grab
            x, y = pt[0] - dx, pt[1] - dy
            lay = self._layer(name)
            self._snapped = (None, None)
            if lay and not e.modifiers() & Qt.AltModifier:        # 1.65: snaps to centre, bars, other elements
                from .layoutmem import SNAP_PX, snap_lines, snap_rect
                xs, ys = snap_lines(self._data["screen"], self._data.get("bar", 0), self._snap_from, name)
                x, y, lx, ly = snap_rect(x, y, lay[3], lay[4], xs, ys, SNAP_PX / max(1e-6, self._frame()[2]))
                self._snapped = (lx, ly)
            self._held = (name, x, y, time.monotonic())
            self._send_status()
            self.update()
            self._post("act", (self._key, ("place", name, x, y)))

    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return
        line = self._limit_at(e)
        if line:                                   # 1.8.14: a limiter line before anything under it
            self._limit, self._limit_y = line, None
            return
        corner = self._on_handle(e)
        if corner:
            self._sizing = corner
            self._send_status()
            return
        pt = self._screen_pos(e)
        hit = self.layer_at(*pt) if pt else None
        if hit and hit[0] != self._data.get("selected"):   # 1.64.9: picks it for the size slider (1.44.2: only a
            self._post("act", (self._key, ("select", hit[0])))   # new pick – each click switched the tab before)
        if self._data.get("editing") and hit and not self._locked(hit[0]):   # 1.46: a locked one stays
            self._grab = hit
            self._snap_from = tuple(self._data.get("layers") or ())   # lines frozen for this drag (no flicker)
            self._answered = False
            self._dragging = True
            self.setCursor(Qt.ClosedHandCursor)
            self._send_status()

    def mouseMoveEvent(self, e):
        if self._limit:
            pt = self._screen_pos(e)
            if pt:
                sh = (self._data.get("screen") or (0, 1))[1]
                self._limit_y = min(max(0.0, pt[1]), float(sh))
                self.update()
                self._post("act", (self._key, ("limit", self._limit[0], self._limit[1], self._limit_y)))
            return
        if self._sizing:                       # the corner: as big as the mouse is from the top left corner
            pt = self._screen_pos(e)
            if pt:
                name, lx, ly, lw, lh = self._sizing
                f = max((pt[0] - lx) / max(1, lw), (pt[1] - ly) / max(1, lh), 0.05)
                self._post("act", (self._key, ("resize", name, lh * f)))
            return
        if self._dragging:
            self._move(e)
        elif not self._data.get("editing"):             # 1.46: a click picks the element under the mouse
            pt = self._screen_pos(e)
            self.setCursor(Qt.PointingHandCursor if pt and self.layer_at(*pt) else Qt.ArrowCursor)
        else:
            pt = self._screen_pos(e)
            hit = self.layer_at(*pt) if pt else None
            self.setCursor(Qt.SizeVerCursor if self._limit_at(e) else Qt.SizeFDiagCursor if self._on_handle(e) else
                           Qt.ForbiddenCursor if hit and self._locked(hit[0]) else
                           Qt.OpenHandCursor if hit else Qt.PointingHandCursor)
        if not self._dragging and not self._sizing and not self._limit:
            pt = self._screen_pos(e)
            hit = self.layer_at(*pt) if pt else None
            if (hit[0] if hit else None) != self._hover:     # 1.46: also outside moving mode (status line)
                self._hover = hit[0] if hit else None
                self.update()
                self._send_status()

    def leaveEvent(self, _e):
        if self._hover:
            self._hover = None
            self.update()
            self._send_status()

    def mouseReleaseEvent(self, _e):
        self._limit = self._limit_y = None
        self._dragging = False
        self._grab = self._sizing = None
        if self._held:
            self._held = self._held[:3] + (time.monotonic(),)
        if self._snapped != (None, None):
            self._snapped = (None, None)
            self.update()
        self._send_status()

    def event(self, e):
        """1.46: Tab / Shift+Tab on the editor's canvas picks the next / previous element (not the next widget)."""
        from PySide6.QtCore import QEvent
        if self._fill and e.type() == QEvent.KeyPress and e.key() in (Qt.Key_Tab, Qt.Key_Backtab):
            self._cycle(-1 if e.key() == Qt.Key_Backtab or e.modifiers() & Qt.ShiftModifier else 1)
            return True
        return super().event(e)

    def _cycle(self, step: int):
        names = [lay[0] for lay in self._data.get("layers") or ()]
        if not names:
            return
        cur = self._data.get("selected")
        i = names.index(cur) if cur in names else (-1 if step > 0 else 0)
        self._post("act", (self._key, ("select", names[(i + step) % len(names)])))

    def keyPressEvent(self, e):
        """Arrow keys (moving mode): the picked element by 1 px, with Shift by 10 px (1.65). 1.46: Esc on the
        editor's canvas ends moving; a locked element does not move."""
        if e.key() == Qt.Key_Escape and self._fill and self._data.get("editing"):
            self._post("act", ("ov.edit", None))
            e.accept()
            return
        step = {Qt.Key_Left: (-1, 0), Qt.Key_Right: (1, 0), Qt.Key_Up: (0, -1), Qt.Key_Down: (0, 1)}.get(e.key())
        if (step is None or not self._data.get("editing") or not self._data.get("selected")
                or self._locked(self._data.get("selected"))):
            super().keyPressEvent(e)
            return
        n = 10 if e.modifiers() & Qt.ShiftModifier else 1
        self._post("act", (self._key, ("nudge", step[0] * n, step[1] * n)))
        e.accept()
        self.setCursor(Qt.PointingHandCursor)
