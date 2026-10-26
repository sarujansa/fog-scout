"""Screenshots as a gallery of tiles (1.12.2, user on the list of file names: "ich find das nicht schön").

One tile per picture: the thumbnail (letterboxed on black – DBD on an ultrawide screen is 21:9), the day and time
below, a badge for copies edited here. Thumbnails come from ``thumbs.Loader`` (a thread of its own, kept on disk
below ``cache/shots``), the ones on display first; the window thread only turns finished bytes into pixmaps
(the thread never touches Qt – qt_clip 1.8.66). The App keeps the list and the choice; this view reports a click
(``on_pick``), a double click / Enter (``on_open``) and a right click (``on_menu``).
"""
from __future__ import annotations

from PySide6.QtCore import QRect, QRectF, QSize, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import QAbstractItemView, QListView, QListWidget, QListWidgetItem, QStyle, QStyledItemDelegate

from . import qt_theme, thumbs
from .qt_common import steady_scroll

TILE_W, TILE_H = 248, 140          # px (logical) of the picture inside a tile (16:9) at the least
GROW = 1.3                         # tiles widen up to this much so that a row fills the width
ASPECTS = (4 / 3, 2.4)             # the tiles take the pictures' width/height within these (16:9 until one is in)
THUMB_W, THUMB_H = 322, 182        # px (logical) the thumbnails are made in: sharp up to the widest tile
CAPTION_H = 46                     # px below the picture: day/time and the line under it
PAD = 8                            # px around the picture inside the tile
GAP = 12                           # px between tiles
PUMP_MS = 30                       # how often finished thumbnails are taken from the loader
PUMP_TAKE = 6                      # ... at most this many per tick (≈ 1 ms each: scrolling stays smooth)
AHEAD_PX = 400                     # thumbnails are asked for this far below/above what is on display
PIX_KEPT = 240                     # pixmaps kept at most (≈ 40 MB at 322×135): the longest unused far ones go
PATH_ROLE = Qt.UserRole
INFO_ROLE = Qt.UserRole + 1        # (caption, line below, badge or "")


def _smaller(font: QFont, share: float = 0.88) -> QFont:
    """``font`` a little smaller – in whatever unit it was given (the window's zoom sets pixels or points)."""
    f = QFont(font)
    if font.pixelSize() > 0:
        f.setPixelSize(max(9, round(font.pixelSize() * share)))
    elif font.pointSizeF() > 0:
        f.setPointSizeF(max(7.0, font.pointSizeF() * share))
    return f


class _TileDelegate(QStyledItemDelegate):
    def __init__(self, view):
        super().__init__(view)
        self.view = view

    def sizeHint(self, option, index):
        return self.view.tile_size()

    def paint(self, p: QPainter, option, index):
        c = self.view.colours()
        r = QRectF(option.rect).adjusted(GAP / 2, GAP / 2, -GAP / 2, -GAP / 2)
        selected = bool(option.state & QStyle.State_Selected)
        hover = bool(option.state & QStyle.State_MouseOver)
        p.save()
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QPen(QColor(c["accent"]), 2) if selected else QPen(QColor(c["border"]), 1))
        p.setBrush(QColor(c["hover"] if hover or selected else c["card"]))
        p.drawRoundedRect(r.adjusted(1, 1, -1, -1), 8, 8)
        pic = QRectF(r.left() + PAD, r.top() + PAD, r.width() - 2 * PAD, (r.width() - 2 * PAD) / self.view.aspect)
        clip = QPainterPath()
        clip.addRoundedRect(pic, 6, 6)
        p.setClipPath(clip)
        p.fillRect(pic, QColor("#000000"))
        pm = self.view.pixmap(index.data(PATH_ROLE))
        if pm is not None and not pm.isNull():
            dpr = pm.devicePixelRatio() or 1.0
            w, h = pm.width() / dpr, pm.height() / dpr
            s = min(pic.width() / max(1.0, w), pic.height() / max(1.0, h))
            dw, dh = w * s, h * s
            p.drawPixmap(QRectF(pic.center().x() - dw / 2, pic.center().y() - dh / 2, dw, dh), pm, QRectF(pm.rect()))
        p.setClipping(False)
        caption, sub, badge = index.data(INFO_ROLE) or ("", "", "")
        f = QFont(option.font)
        f.setWeight(QFont.DemiBold)
        p.setFont(f)
        p.setPen(QColor(c["head"]))
        text_r = QRect(int(pic.left()), int(pic.bottom() + 6), int(pic.width()), 20)
        p.drawText(text_r, Qt.AlignLeft | Qt.AlignVCenter, caption)
        p.setFont(_smaller(option.font))
        p.setPen(QColor(c["dim"]))
        p.drawText(text_r.translated(0, 19), Qt.AlignLeft | Qt.AlignVCenter, sub)
        if badge:                                              # "Bearbeitet": a small pill on the picture
            fm = p.fontMetrics()
            bw = fm.horizontalAdvance(badge) + 14
            br = QRectF(pic.left() + 6, pic.top() + 6, bw, fm.height() + 4)
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(c["accent"]))
            p.drawRoundedRect(br, br.height() / 2, br.height() / 2)
            p.setPen(QColor(c["on_accent"]))
            p.drawText(br, Qt.AlignCenter, badge)
        p.restore()


class ShotGallery(QListWidget):
    """The tiles; ``set_items([(path, caption, line below, badge)])`` keeps the scroll position and the choice
    when the list is the same."""

    def __init__(self, cache_dir: str | None, dark=True, on_pick=None, on_open=None, on_menu=None):
        super().__init__()
        self.setObjectName("gallery")
        self.dark = dark
        self.on_pick, self.on_open, self.on_menu = on_pick, on_open, on_menu
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setMovement(QListView.Static)
        self.setFlow(QListView.LeftToRight)
        self.setWrapping(True)
        self.setUniformItemSizes(True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(24)
        steady_scroll(self)                                    # the bar is always there: the row width stays
        self.setMouseTracking(True)                           # hover look
        self.setSpacing(0)
        self.setItemDelegate(_TileDelegate(self))
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._menu)
        self.itemSelectionChanged.connect(self._picked)
        self.itemActivated.connect(lambda it: self.on_open and self.on_open(it.data(PATH_ROLE)))
        ratio = self.devicePixelRatioF()
        self._ratio = ratio
        self._loader = thumbs.Loader((round(THUMB_W * ratio), round(THUMB_H * ratio)), cache_dir, name="shot-thumbs")
        self._tile = QSize(TILE_W + 2 * PAD + GAP, TILE_H + 2 * PAD + GAP + CAPTION_H)
        self.aspect = 16 / 9
        self._pix = {}                                         # path -> QPixmap, the longest unused first
        self._awaited = set()                                  # paths of the latest request not yet in
        self._key = None
        self._pump = QTimer(self)
        self._pump.setInterval(PUMP_MS)
        self._pump.timeout.connect(self._take)
        self._ask_soon = QTimer(self)
        self._ask_soon.setSingleShot(True)
        self._ask_soon.setInterval(60)
        self._ask_soon.timeout.connect(self._ask_visible)
        self.verticalScrollBar().valueChanged.connect(lambda _v: self._ask_soon.start())

    def colours(self) -> dict:
        return qt_theme.colours(self.dark)

    def tile_size(self) -> QSize:
        return self._tile

    def _fit_tiles(self):
        """As many tiles per row as fit at their least width, widened (≤ GROW) so that the row ends at the edge."""
        avail = max(1, self.viewport().width() - 4)            # Qt wraps a row that would end exactly at the edge
        least = TILE_W + 2 * PAD + GAP
        n = max(1, avail // least)
        w = min(int(least * GROW), avail // n - 1)
        size = QSize(w, round((w - GAP - 2 * PAD) / self.aspect) + 2 * PAD + GAP + CAPTION_H)
        if size != self._tile:
            self._tile = size
            self.setGridSize(size)

    # ---- data
    def set_items(self, items, selected: str | None = None):
        key = tuple(items)
        if key != self._key:
            self._key = key
            self.blockSignals(True)
            self.clear()
            for path, caption, sub, badge in items:
                it = QListWidgetItem()
                it.setData(PATH_ROLE, path)
                it.setData(INFO_ROLE, (caption, sub, badge))
                it.setToolTip(path)
                self.addItem(it)
            self.blockSignals(False)
            known = {i[0] for i in items}
            self._pix = {p: pm for p, pm in self._pix.items() if p in known}
            self._awaited &= known
        self.select_path(selected)
        self._ask_soon.start()

    def select_path(self, path: str | None):
        self.blockSignals(True)
        try:
            self.clearSelection()
            for i in range(self.count()):
                it = self.item(i)
                if path and it.data(PATH_ROLE) == path:
                    it.setSelected(True)
                    self.setCurrentItem(it)
                    break
        finally:
            self.blockSignals(False)

    def selected_path(self) -> str | None:
        items = self.selectedItems()
        return items[0].data(PATH_ROLE) if items else None

    def paths(self) -> list:
        return [self.item(i).data(PATH_ROLE) for i in range(self.count())]

    def pixmap(self, path):
        return self._pix.get(path)

    # ---- thumbnails
    def _ask_visible(self):
        """The thumbnails on display (and a little beyond) that are not yet made, top to bottom – all of them each
        time: the loader keeps only the newest request, so what an earlier one still owed is asked for again
        (review of 1.12.2: a path asked once was never asked again and its tile stayed black)."""
        view = self.viewport().rect().adjusted(0, -AHEAD_PX, 0, AHEAD_PX)
        near, want = set(), []
        for i in range(self.count()):
            it = self.item(i)
            if not self.visualItemRect(it).intersects(view):
                continue
            path = it.data(PATH_ROLE)
            near.add(path)
            if path in self._pix:
                self._pix[path] = self._pix.pop(path)          # used now: the last to go
            else:
                want.append(path)
        self._forget_far(near)
        self._awaited = set(want)
        if want:
            self._loader.request(want)
            self._pump.start()

    def _forget_far(self, near: set):
        """At most PIX_KEPT pixmaps: the longest unused ones away from the display go (a gallery of years of
        screenshots scrolled through held all of them, ~370 MB for 2000) – scrolled back, they come again from
        the disk cache."""
        extra = len(self._pix) - PIX_KEPT
        if extra > 0:
            for path in [p for p in self._pix if p not in near][:extra]:
                del self._pix[path]

    def _take(self):
        for path, w, h, data in self._loader.take(PUMP_TAKE):
            self._apply(path, w, h, data)
        if not self._awaited:          # not Loader.busy: that is False while the thread still makes the last one
            self._pump.stop()

    def _apply(self, path, w, h, data):
        self._awaited.discard(path)
        if w and h and data:
            img = QImage(data, w, h, w * 4, QImage.Format_RGBA8888).copy()
            pm = QPixmap.fromImage(img)
            pm.setDevicePixelRatio(self._ratio)
            if not any(not p.isNull() for p in self._pix.values()):      # the first picture sets the tiles' shape
                aspect = min(max(w / h, ASPECTS[0]), ASPECTS[1])
                if abs(aspect - self.aspect) > 0.01:
                    self.aspect = aspect
                    self._fit_tiles()
        else:
            pm = QPixmap()                                     # unreadable: the tile stays black
        self._pix[path] = pm
        self.viewport().update()

    def load_all(self):
        """Tests: every thumbnail now, in this thread."""
        for path in self.paths():
            if path not in self._pix:
                self._apply(*self._loader.make(path))

    # ---- events
    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._fit_tiles()
        self._ask_soon.start()

    def showEvent(self, e):
        super().showEvent(e)
        self._ask_soon.start()

    def _picked(self):
        if self.on_pick:
            self.on_pick(self.selected_path())

    def _menu(self, pos):
        it = self.itemAt(pos)
        if it is None:
            return
        if not it.isSelected():
            self.select_path(it.data(PATH_ROLE))
            self._picked()
        if self.on_menu:
            gp = self.viewport().mapToGlobal(pos)
            self.on_menu((gp.x(), gp.y()))                     # like the tables: popup_menu takes (x, y)
