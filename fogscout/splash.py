"""Splash screen while the program starts (1.14.2, user: "während dem Starten der App soll ein Ladebildschirm
kommen, der sehr modern aussieht").

``start()`` runs in __main__ before ``fogscout.app`` is imported – the imports and App() take seconds, during which
nothing was on screen. Only PySide6, the pure theme module and the icon are loaded for it. App reports its steps
through ``progress(fraction, text)`` (the bar never runs backwards); each step repaints at once – no event loop runs
while the App is built, and ``processEvents`` there could fire the App's own timers early. ``finish()`` fades the
card away once the main loop runs, i.e. while the window behind it comes up. Nothing here may stop the start: start()
answers None on any error. Colours: the user's theme from settings.json (theme_from_file), the title in Fira Sans
like the map names. Not shown for the silent autostart in the tray (--tray)."""
from __future__ import annotations

import json
import logging
import os
import time

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import (QColor, QFont, QGuiApplication, QLinearGradient, QPainter, QPainterPath, QPen,
                           QRadialGradient)
from PySide6.QtWidgets import QWidget

from . import icon, qt_theme
from .i18n import _

log = logging.getLogger("fogscout")

CARD_W, CARD_H = 460, 190         # logical px of the card
MARGIN = 28                       # room around it for the shadow
RADIUS = 18
ICON = 84                         # the program symbol, logical px
FADE_MS = 280                     # finish(): opacity 1 → 0 over this time
STEP_MS = 16
SHADOW = 14                       # rings of the soft shadow


def theme_from_file(path: str) -> bool:
    """The colour theme from settings.json before the App (and its Settings) exists, like i18n.init_from_settings:
    sets qt_theme's theme and answers whether the dark mode is on (defaults: gold, dark)."""
    data = {}
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        pass
    if not isinstance(data, dict):
        data = {}
    qt_theme.set_theme(str(data.get("color_theme", "gold")), bool(data.get("oled_black", False)),
                       data.get("accent_custom"))
    return bool(data.get("dark_mode", True))


class Splash(QWidget):
    """A frameless, translucent card in the middle of the main screen: icon, name, version, one line for the
    current step and a thin bar. Never takes the focus (a start while something else is in front)."""

    def __init__(self, version: str, dark: bool = True):
        super().__init__(None, Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.version = version
        self.dark = bool(dark)
        self.c = qt_theme.colours(self.dark)
        self.fraction = 0.0
        self.text = ""
        self._fade = None
        self._fade_t0 = 0.0
        self.setFixedSize(CARD_W + 2 * MARGIN, CARD_H + 2 * MARGIN)
        screen = QGuiApplication.primaryScreen()
        ratio = screen.devicePixelRatio() if screen is not None else 1.0
        from .qt_common import pixmap_from_pil
        self._icon = pixmap_from_pil(icon.draw(ICON * 2), ICON, ratio)
        if screen is not None:
            geo = screen.availableGeometry()
            self.move(geo.center().x() - self.width() // 2, geo.center().y() - self.height() // 2)

    # ------------------------------------------------------------- the App's steps
    def progress(self, fraction: float, text: str = ""):
        """The step reached: the bar grows to ``fraction`` (never shrinks), ``text`` names the step."""
        try:
            fraction = float(fraction)
        except (TypeError, ValueError):
            fraction = self.fraction
        fraction = max(self.fraction, min(1.0, fraction))
        if fraction == self.fraction and (not text or text == self.text):
            return
        self.fraction = fraction
        if text:
            self.text = str(text)
        if self.isVisible():
            self.repaint()                       # synchronous: no event loop runs while the App is built

    def finish(self):
        """Done: fade away over FADE_MS once the event loop runs (App.run), then close."""
        self.progress(1.0)
        if self._fade is not None:
            return
        if not self.isVisible():
            self.close()
            return
        self._fade_t0 = time.perf_counter()
        self._fade = QTimer(self)
        self._fade.timeout.connect(self._fade_step)
        self._fade.start(STEP_MS)

    def _fade_step(self):
        k = (time.perf_counter() - self._fade_t0) / (FADE_MS / 1000.0)
        if k >= 1.0:
            self._fade.stop()
            self.close()
            return
        self.setWindowOpacity(1.0 - k)

    # ------------------------------------------------------------- drawing
    def paintEvent(self, _event):
        c = self.c
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        card = QRectF(MARGIN, MARGIN, CARD_W, CARD_H)
        # soft shadow: rings growing outwards (a little more below), alpha falling off
        peak = 34 if self.dark else 22
        for i in range(SHADOW, 0, -1):
            ring = card.adjusted(-i, -i + 3, i, i + 5)
            path = QPainterPath()
            path.addRoundedRect(ring, RADIUS + i, RADIUS + i)
            p.fillPath(path, QColor(0, 0, 0, int(peak * (1 - i / (SHADOW + 1)) ** 2)))
        path = QPainterPath()
        path.addRoundedRect(card, RADIUS, RADIUS)
        grad = QLinearGradient(card.topLeft(), card.bottomLeft())
        grad.setColorAt(0.0, QColor(c["card"]).lighter(114) if self.dark else QColor(c["card"]))
        grad.setColorAt(1.0, QColor(c["bg"]))
        p.fillPath(path, grad)
        p.save()
        p.setClipPath(path)
        glow = QRadialGradient(card.topLeft() + QPointF(70, 10), 300)      # a breath of the accent, top left
        a0, a1 = QColor(c["accent"]), QColor(c["accent"])
        a0.setAlpha(64 if self.dark else 40)
        a1.setAlpha(0)
        glow.setColorAt(0.0, a0)
        glow.setColorAt(1.0, a1)
        p.fillRect(card, glow)
        p.restore()
        p.setPen(QPen(QColor(c["border"]), 1))
        p.setBrush(Qt.NoBrush)
        p.drawRoundedRect(card.adjusted(0.5, 0.5, -0.5, -0.5), RADIUS, RADIUS)

        x0 = card.left() + 28
        p.drawPixmap(QPointF(x0, card.top() + 30), self._icon)
        tx = x0 + ICON + 26
        right = card.right() - 28
        title = QFont("Fira Sans ExtraBold")
        title.setPixelSize(30)
        title.setWeight(QFont.ExtraBold)
        p.setFont(title)
        p.setPen(QColor(c["head"]))
        p.drawText(QRectF(tx, card.top() + 26, right - tx, 40), Qt.AlignLeft | Qt.AlignVCenter, "Fog Scout")
        small = QFont()
        small.setPixelSize(13)
        p.setFont(small)
        p.setPen(QColor(c["dim"]))
        p.drawText(QRectF(tx, card.top() + 66, right - tx, 18), Qt.AlignLeft | Qt.AlignVCenter,
                   _("Version {version}", version=self.version))
        # the step and its share
        p.drawText(QRectF(tx, card.bottom() - 70, right - tx - 48, 18), Qt.AlignLeft | Qt.AlignVCenter, self.text)
        p.drawText(QRectF(right - 48, card.bottom() - 70, 48, 18), Qt.AlignRight | Qt.AlignVCenter,
                   f"{round(self.fraction * 100)} %")
        track = QRectF(tx, card.bottom() - 44, right - tx, 6)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(c["bar"]))
        p.drawRoundedRect(track, 3, 3)
        w = track.width() * self.fraction
        if w > 0:
            fill = QRectF(track.left(), track.top(), max(6.0, w), track.height())
            halo = QColor(c["accent"])
            halo.setAlpha(70)
            p.setBrush(halo)
            p.drawRoundedRect(fill.adjusted(-2, -2, 2, 2), 5, 5)
            bar = QLinearGradient(fill.topLeft(), fill.topRight())
            bar.setColorAt(0.0, QColor(c["accent"]))
            bar.setColorAt(1.0, QColor(c["accent_hover"]))
            p.setBrush(bar)
            p.drawRoundedRect(fill, 3, 3)
        p.end()


def start(root_dir: str, version: str):
    """The splash on screen, before anything heavy loads – None when it cannot be shown (the start goes on)."""
    try:
        from .qt_app import application
        app = application()
        dark = theme_from_file(os.path.join(root_dir, "settings.json"))
        s = Splash(version, dark)
        s.progress(0.04, _("Wird gestartet …"))
        s.show()
        app.processEvents()                  # the only pump before the App exists: puts the first frame on screen
        return s
    except Exception:
        log.exception("Ladebildschirm")
        return None
