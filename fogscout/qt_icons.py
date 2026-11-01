"""Icons of the clip editor (1.16): drawn with QPainter on a 24-unit grid – one stroke weight, round caps, any
size, sharp on scaled screens (the pixmap is made at the device pixel ratio). No icon font, no picture files, no
emoji: the glyphs below are the whole set. ``icon(name, colours)`` gives a QIcon with the normal, hover (active),
disabled and checked (on) colours of the window's palette; ``pixmap`` one picture."""
from __future__ import annotations

from functools import lru_cache

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen, QPixmap, QPolygonF

STROKE = 1.8                       # units of the 24-grid


def _pen(colour, width=STROKE):
    pen = QPen(QColor(colour), width)
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    return pen


def _tri(p, points):
    p.setPen(Qt.NoPen)
    p.drawPolygon(QPolygonF([QPointF(x, y) for x, y in points]))


def _lines(p, *segs):
    for seg in segs:
        pts = [QPointF(x, y) for x, y in seg]
        p.drawPolyline(QPolygonF(pts))


# ---- the glyphs: each draws on a 24×24 grid with the pen set to the colour (brush = colour too)
def _play(p, c):
    _tri(p, [(7, 4.5), (19.5, 12), (7, 19.5)])


def _pause(p, c):
    p.setPen(Qt.NoPen)
    p.drawRoundedRect(QRectF(6, 4.5, 4, 15), 1, 1)
    p.drawRoundedRect(QRectF(14, 4.5, 4, 15), 1, 1)


def _to_start(p, c):
    p.setPen(Qt.NoPen)
    p.drawRoundedRect(QRectF(5, 5, 2.4, 14), 1, 1)
    _tri(p, [(19, 5.5), (19, 18.5), (9, 12)])


def _to_end(p, c):
    p.setPen(Qt.NoPen)
    p.drawRoundedRect(QRectF(16.6, 5, 2.4, 14), 1, 1)
    _tri(p, [(5, 5.5), (5, 18.5), (15, 12)])


def _rewind(p, c):
    _tri(p, [(12, 6), (12, 18), (4, 12)])
    _tri(p, [(20.5, 6), (20.5, 18), (12.5, 12)])


def _forward(p, c):
    _tri(p, [(3.5, 6), (3.5, 18), (11.5, 12)])
    _tri(p, [(12, 6), (12, 18), (20, 12)])


def _frame_prev(p, c):
    _lines(p, [(14, 6), (8, 12), (14, 18)])
    p.drawLine(QPointF(6, 6.5), QPointF(6, 17.5))


def _frame_next(p, c):
    _lines(p, [(10, 6), (16, 12), (10, 18)])
    p.drawLine(QPointF(18, 6.5), QPointF(18, 17.5))


def _mark_in(p, c):
    _lines(p, [(10, 5), (6, 5), (6, 19), (10, 19)])
    _tri(p, [(11, 8.5), (17, 12), (11, 15.5)])


def _mark_out(p, c):
    _lines(p, [(14, 5), (18, 5), (18, 19), (14, 19)])
    _tri(p, [(13, 8.5), (7, 12), (13, 15.5)])


def _volume(p, c):
    path = QPainterPath()
    path.moveTo(4, 9.5)
    path.lineTo(7.5, 9.5)
    path.lineTo(12.5, 5.5)
    path.lineTo(12.5, 18.5)
    path.lineTo(7.5, 14.5)
    path.lineTo(4, 14.5)
    path.closeSubpath()
    p.setPen(Qt.NoPen)
    p.drawPath(path)
    p.setPen(_pen(c))
    p.setBrush(Qt.NoBrush)
    p.drawArc(QRectF(10, 8, 9, 8), -50 * 16, 100 * 16)
    p.drawArc(QRectF(9, 4.5, 14, 15), -50 * 16, 100 * 16)


def _mute(p, c):
    path = QPainterPath()
    path.moveTo(4, 9.5)
    path.lineTo(7.5, 9.5)
    path.lineTo(12.5, 5.5)
    path.lineTo(12.5, 18.5)
    path.lineTo(7.5, 14.5)
    path.lineTo(4, 14.5)
    path.closeSubpath()
    p.setPen(Qt.NoPen)
    p.drawPath(path)
    p.setPen(_pen(c))
    p.drawLine(QPointF(15.5, 9.5), QPointF(20.5, 14.5))
    p.drawLine(QPointF(20.5, 9.5), QPointF(15.5, 14.5))


def _fullscreen(p, c):
    _lines(p, [(4, 9), (4, 4), (9, 4)], [(15, 4), (20, 4), (20, 9)], [(20, 15), (20, 20), (15, 20)],
           [(9, 20), (4, 20), (4, 15)])


def _fullscreen_exit(p, c):
    _lines(p, [(4, 9), (9, 9), (9, 4)], [(15, 4), (15, 9), (20, 9)], [(20, 15), (15, 15), (15, 20)],
           [(9, 20), (9, 15), (4, 15)])


def _save(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(QRectF(4, 4, 16, 16), 2, 2)
    p.drawRect(QRectF(8, 4, 8, 5))
    p.drawRoundedRect(QRectF(7.5, 13, 9, 7), 1, 1)


def _undo(p, c):
    p.setBrush(Qt.NoBrush)
    path = QPainterPath()
    path.moveTo(8, 7)
    path.cubicTo(8, 7, 19, 5.5, 19, 13)
    path.cubicTo(19, 18.5, 13, 19, 10, 19)
    p.drawPath(path)
    _lines(p, [(9.5, 3.5), (6, 7), (9.5, 10.5)])


def _redo(p, c):
    p.setBrush(Qt.NoBrush)
    path = QPainterPath()
    path.moveTo(16, 7)
    path.cubicTo(16, 7, 5, 5.5, 5, 13)
    path.cubicTo(5, 18.5, 11, 19, 14, 19)
    p.drawPath(path)
    _lines(p, [(14.5, 3.5), (18, 7), (14.5, 10.5)])


def _export(p, c):
    p.setBrush(Qt.NoBrush)
    _lines(p, [(5, 14), (5, 19), (19, 19), (19, 14)])
    p.drawLine(QPointF(12, 4.5), QPointF(12, 15))
    _lines(p, [(8, 8.5), (12, 4.5), (16, 8.5)])


def _import(p, c):
    p.setBrush(Qt.NoBrush)
    _lines(p, [(5, 14), (5, 19), (19, 19), (19, 14)])
    p.drawLine(QPointF(12, 4), QPointF(12, 14.5))
    _lines(p, [(8, 10.5), (12, 14.5), (16, 10.5)])


def _panel_left(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(QRectF(3.5, 5, 17, 14), 2, 2)
    p.drawLine(QPointF(9.5, 5), QPointF(9.5, 19))


def _panel_right(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(QRectF(3.5, 5, 17, 14), 2, 2)
    p.drawLine(QPointF(14.5, 5), QPointF(14.5, 19))


def _panel_bottom(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(QRectF(3.5, 5, 17, 14), 2, 2)
    p.drawLine(QPointF(3.5, 14), QPointF(20.5, 14))


def _search(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawEllipse(QRectF(4.5, 4.5, 11, 11))
    p.drawLine(QPointF(14, 14), QPointF(19.5, 19.5))


def _sort(p, c):
    p.drawLine(QPointF(8, 5), QPointF(8, 19))
    _lines(p, [(4.5, 15.5), (8, 19), (11.5, 15.5)])
    p.drawLine(QPointF(16, 19), QPointF(16, 5))
    _lines(p, [(12.5, 8.5), (16, 5), (19.5, 8.5)])


def _film(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(QRectF(3.5, 5, 17, 14), 2, 2)
    for y in (8, 12, 16):
        p.drawLine(QPointF(3.5, y), QPointF(6.5, y))
        p.drawLine(QPointF(17.5, y), QPointF(20.5, y))
    p.drawLine(QPointF(6.5, 5), QPointF(6.5, 19))
    p.drawLine(QPointF(17.5, 5), QPointF(17.5, 19))


def _scissors(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawEllipse(QRectF(4, 13, 5.5, 5.5))
    p.drawEllipse(QRectF(4, 5.5, 5.5, 5.5))
    p.drawLine(QPointF(8.8, 9.8), QPointF(20, 17.5))
    p.drawLine(QPointF(8.8, 14.2), QPointF(20, 6.5))


def _file(p, c):
    p.setBrush(Qt.NoBrush)
    path = QPainterPath()
    path.moveTo(6, 4)
    path.lineTo(14, 4)
    path.lineTo(18.5, 8.5)
    path.lineTo(18.5, 20)
    path.lineTo(6, 20)
    path.closeSubpath()
    p.drawPath(path)
    _lines(p, [(14, 4), (14, 8.5), (18.5, 8.5)])


def _folder(p, c):
    p.setBrush(Qt.NoBrush)
    path = QPainterPath()
    path.moveTo(3.5, 7)
    path.lineTo(9, 7)
    path.lineTo(11, 9)
    path.lineTo(20.5, 9)
    path.lineTo(20.5, 19)
    path.lineTo(3.5, 19)
    path.closeSubpath()
    p.drawPath(path)


def _pointer(p, c):
    path = QPainterPath()
    path.moveTo(6, 4)
    path.lineTo(18.5, 12.5)
    path.lineTo(12.8, 13.6)
    path.lineTo(10, 19.5)
    path.closeSubpath()
    p.setPen(_pen(c, 1.6))
    p.setBrush(Qt.NoBrush)
    p.drawPath(path)


def _split(p, c):
    """A clip cut in two: the two halves and the cut between them."""
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(QRectF(3.5, 8, 6, 8), 1.5, 1.5)
    p.drawRoundedRect(QRectF(14.5, 8, 6, 8), 1.5, 1.5)
    p.drawLine(QPointF(12, 4), QPointF(12, 20))


def _trash(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawLine(QPointF(4.5, 7), QPointF(19.5, 7))
    _lines(p, [(9, 7), (9, 4.5), (15, 4.5), (15, 7)])
    _lines(p, [(6.5, 7), (7.5, 19.5), (16.5, 19.5), (17.5, 7)])
    p.drawLine(QPointF(10.5, 10), QPointF(10.5, 16.5))
    p.drawLine(QPointF(13.5, 10), QPointF(13.5, 16.5))


def _zoom_in(p, c):
    _search(p, c)
    p.drawLine(QPointF(7.5, 10), QPointF(12.5, 10))
    p.drawLine(QPointF(10, 7.5), QPointF(10, 12.5))


def _zoom_out(p, c):
    _search(p, c)
    p.drawLine(QPointF(7.5, 10), QPointF(12.5, 10))


def _zoom_fit(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawLine(QPointF(4, 6), QPointF(4, 18))
    p.drawLine(QPointF(20, 6), QPointF(20, 18))
    p.drawLine(QPointF(7, 12), QPointF(17, 12))
    _lines(p, [(9.5, 9.5), (7, 12), (9.5, 14.5)], [(14.5, 9.5), (17, 12), (14.5, 14.5)])


def _magnet(p, c):
    p.setBrush(Qt.NoBrush)
    path = QPainterPath()
    path.moveTo(6.5, 4.5)
    path.lineTo(6.5, 13)
    path.arcTo(QRectF(6.5, 7.5, 11, 11), 180, 180)
    path.lineTo(17.5, 4.5)
    p.drawPath(path)
    p.drawLine(QPointF(6.5, 8.5), QPointF(10, 8.5))
    p.drawLine(QPointF(14, 8.5), QPointF(17.5, 8.5))


def _flag(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawLine(QPointF(6, 4), QPointF(6, 20.5))
    path = QPainterPath()
    path.moveTo(6, 5)
    path.lineTo(18.5, 5)
    path.lineTo(15.5, 9)
    path.lineTo(18.5, 13)
    path.lineTo(6, 13)
    p.drawPath(path)


def _crop(p, c):
    p.setBrush(Qt.NoBrush)
    _lines(p, [(7, 3.5), (7, 17), (20.5, 17)])
    _lines(p, [(3.5, 7), (17, 7), (17, 20.5)])


def _pen_tool(p, c):
    p.setBrush(Qt.NoBrush)
    path = QPainterPath()
    path.moveTo(4.5, 19.5)
    path.lineTo(5.5, 15.5)
    path.lineTo(16.5, 4.5)
    path.lineTo(19.5, 7.5)
    path.lineTo(8.5, 18.5)
    path.closeSubpath()
    p.drawPath(path)
    p.drawLine(QPointF(14, 7), QPointF(17, 10))


def _text(p, c):
    p.drawLine(QPointF(5, 6), QPointF(19, 6))
    p.drawLine(QPointF(12, 6), QPointF(12, 19))
    p.drawLine(QPointF(9, 19), QPointF(15, 19))


def _rect(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(QRectF(4.5, 6, 15, 12), 1.5, 1.5)


def _ellipse(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawEllipse(QRectF(4.5, 6, 15, 12))


def _line(p, c):
    p.drawLine(QPointF(5, 19), QPointF(19, 5))


def _arrow(p, c):
    p.drawLine(QPointF(5, 19), QPointF(18, 6))
    _lines(p, [(10.5, 5.5), (18.5, 5.5), (18.5, 13.5)])


def _free(p, c):
    p.setBrush(Qt.NoBrush)
    path = QPainterPath()
    path.moveTo(4, 15)
    path.cubicTo(6, 6, 10, 6, 11, 12)
    path.cubicTo(12, 18, 16, 18, 20, 8)
    p.drawPath(path)


def _censor(p, c):
    p.setBrush(Qt.NoBrush)
    path = QPainterPath()
    path.moveTo(3.5, 12)
    path.cubicTo(7, 6, 17, 6, 20.5, 12)
    path.cubicTo(17, 18, 7, 18, 3.5, 12)
    p.drawPath(path)
    p.drawEllipse(QRectF(9.5, 9.5, 5, 5))
    p.drawLine(QPointF(5, 19), QPointF(19, 5))


def _names(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(QRectF(3.5, 5.5, 17, 13), 2, 2)
    p.drawEllipse(QRectF(6.5, 8.5, 4, 4))
    p.drawLine(QPointF(13, 9.5), QPointF(17.5, 9.5))
    p.drawLine(QPointF(13, 13), QPointF(17.5, 13))
    p.drawLine(QPointF(6.5, 15.5), QPointF(10.5, 15.5))


def _camera(p, c):
    p.setBrush(Qt.NoBrush)
    path = QPainterPath()
    path.moveTo(3.5, 8)
    path.lineTo(8, 8)
    path.lineTo(9.5, 5.5)
    path.lineTo(14.5, 5.5)
    path.lineTo(16, 8)
    path.lineTo(20.5, 8)
    path.lineTo(20.5, 19)
    path.lineTo(3.5, 19)
    path.closeSubpath()
    p.drawPath(path)
    p.drawEllipse(QRectF(9, 10, 6, 6))


def _close(p, c):
    p.drawLine(QPointF(6, 6), QPointF(18, 18))
    p.drawLine(QPointF(18, 6), QPointF(6, 18))


def _check(p, c):
    _lines(p, [(5, 12.5), (10, 17.5), (19, 7)])


def _plus(p, c):
    p.drawLine(QPointF(12, 5), QPointF(12, 19))
    p.drawLine(QPointF(5, 12), QPointF(19, 12))


def _more(p, c):
    p.setPen(Qt.NoPen)
    for x in (6, 12, 18):
        p.drawEllipse(QPointF(x, 12), 1.6, 1.6)


def _info(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawEllipse(QRectF(4, 4, 16, 16))
    p.drawLine(QPointF(12, 11), QPointF(12, 16.5))
    p.setPen(Qt.NoPen)
    p.setBrush(QColor(c))
    p.drawEllipse(QPointF(12, 8), 1.2, 1.2)


def _compass(p, c):
    """The program's own sign: the compass star of the icon."""
    p.setPen(Qt.NoPen)
    _tri(p, [(12, 3), (14.2, 9.8), (12, 12), (9.8, 9.8)])
    _tri(p, [(12, 21), (14.2, 14.2), (12, 12), (9.8, 14.2)])
    _tri(p, [(3, 12), (9.8, 9.8), (12, 12), (9.8, 14.2)])
    _tri(p, [(21, 12), (14.2, 9.8), (12, 12), (14.2, 14.2)])


def _clip_tool(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(QRectF(3.5, 7, 17, 10), 2, 2)
    p.drawLine(QPointF(8, 7), QPointF(8, 17))
    p.drawLine(QPointF(16, 7), QPointF(16, 17))


def _speed(p, c):
    p.setBrush(Qt.NoBrush)
    p.drawArc(QRectF(4, 5, 16, 16), 20 * 16, 140 * 16)
    p.drawLine(QPointF(12, 13), QPointF(16.5, 8.5))
    p.setPen(Qt.NoPen)
    p.setBrush(QColor(c))
    p.drawEllipse(QPointF(12, 13), 1.6, 1.6)


GLYPHS = {
    "play": _play, "pause": _pause, "to_start": _to_start, "to_end": _to_end, "rewind": _rewind, "forward": _forward,
    "frame_prev": _frame_prev, "frame_next": _frame_next, "mark_in": _mark_in, "mark_out": _mark_out,
    "volume": _volume, "mute": _mute, "fullscreen": _fullscreen, "fullscreen_exit": _fullscreen_exit,
    "save": _save, "undo": _undo, "redo": _redo, "export": _export, "import": _import,
    "panel_left": _panel_left, "panel_right": _panel_right, "panel_bottom": _panel_bottom,
    "search": _search, "sort": _sort, "film": _film, "scissors": _scissors, "file": _file, "folder": _folder,
    "pointer": _pointer, "split": _split, "trash": _trash, "zoom_in": _zoom_in, "zoom_out": _zoom_out,
    "zoom_fit": _zoom_fit, "magnet": _magnet, "flag": _flag, "crop": _crop, "pen": _pen_tool, "text": _text,
    "rect": _rect, "ellipse": _ellipse, "line": _line, "arrow": _arrow, "free": _free, "censor": _censor,
    "names": _names, "camera": _camera, "close": _close, "check": _check, "plus": _plus, "more": _more,
    "info": _info, "compass": _compass, "clip": _clip_tool, "speed": _speed,
}


@lru_cache(maxsize=512)
def pixmap(name: str, colour: str, size: int = 20, ratio: float = 1.0) -> QPixmap:
    """The glyph ``name`` in ``colour``, ``size`` logical px square (drawn at ``ratio`` for scaled screens)."""
    px = max(1, int(round(size * ratio)))
    pm = QPixmap(px, px)
    pm.fill(Qt.transparent)
    draw = GLYPHS.get(name)
    if draw is not None:
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing)
        p.scale(px / 24.0, px / 24.0)
        p.setPen(_pen(colour))
        p.setBrush(QColor(colour))
        draw(p, colour)
        p.end()
    pm.setDevicePixelRatio(ratio)
    return pm


def icon(name: str, colour: str, active: str | None = None, disabled: str | None = None, on: str | None = None,
         size: int = 20, ratio: float = 1.0) -> QIcon:
    """A QIcon with the glyph in ``colour`` (normal), ``active`` (hover), ``disabled`` and ``on`` (a checked
    button) – each at the usual sizes so Qt never scales a bitmap."""
    ic = QIcon()
    for s in sorted({size, 16, 20, 24, 32}):
        ic.addPixmap(pixmap(name, colour, s, ratio), QIcon.Normal, QIcon.Off)
        ic.addPixmap(pixmap(name, active or colour, s, ratio), QIcon.Active, QIcon.Off)
        ic.addPixmap(pixmap(name, disabled or colour, s, ratio), QIcon.Disabled, QIcon.Off)
        ic.addPixmap(pixmap(name, on or colour, s, ratio), QIcon.Normal, QIcon.On)
        ic.addPixmap(pixmap(name, on or colour, s, ratio), QIcon.Active, QIcon.On)
        ic.addPixmap(pixmap(name, disabled or colour, s, ratio), QIcon.Disabled, QIcon.On)
    return ic
