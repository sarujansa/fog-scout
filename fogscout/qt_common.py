"""Small helpers shared by the Qt pages and views (labels, cards, tooltips, pixmaps, scroll pages).
"""
from __future__ import annotations

import logging
import threading

from PIL import Image
from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QAbstractScrollArea, QAbstractSlider, QAbstractSpinBox, QApplication, QComboBox, QFrame,
                               QLabel, QScrollArea, QVBoxLayout, QWidget)

from . import qt_theme           # 1.24.6: at module level – an import statement in set_glyph cost ~1.9 µs per call
from .i18n import N_, _

log = logging.getLogger("fogscout")


class Channel:
    """One kind of message: ``emit`` from any thread only queues it, the ``connect``-ed handlers run in the GUI
    thread when the window's pump drains the bridge (the same names as Qt signals)."""

    def __init__(self, bridge, name):
        self._bridge, self._name = bridge, name

    def emit(self, *args):
        self._bridge.put(self._name, args)

    def connect(self, fn):
        self._bridge.handlers.setdefault(self._name, []).append(fn)


class Bridge:
    """What worker threads hand to a window – never a QObject. 1.8.66 (clip editor) and 1.38.3 (image editor): a
    thread that emitted a Qt signal on an object of a window closed meanwhile raised "Signal source has been
    deleted", and when the deletion fell into the emit itself the whole program went down. The threads touch no Qt
    object: they append to a plain locked queue, the window's own QTimer (it dies with the window) drains it."""
    NAMES: tuple = ()
    LATEST: tuple = ()          # pictures: only the newest of a batch is handled
    AFTER_CLOSE: tuple = ()     # kinds a closed window still handles
    LABEL = "Fenster"           # in the log line of a failing handler

    def __init__(self, names: tuple = ()):
        self._lock = threading.Lock()
        self._queue = []
        self.handlers = {}
        for name in names or self.NAMES:
            setattr(self, name, Channel(self, name))

    def put(self, name, args):
        with self._lock:
            self._queue.append((name, args))

    def clear(self, keep=()):
        """Drop what is queued – but the kinds in ``keep``."""
        with self._lock:
            self._queue = [m for m in self._queue if m[0] in keep]

    def pending(self) -> bool:
        with self._lock:
            return bool(self._queue)

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
                    log.exception("%s: %s", self.LABEL, name)


# 1.24 (phase 2, prompt_phase2.md): one line under each page's title – what the page is for
PAGE_SUBTITLES = {
    "overview": N_("Status, aktuelle Map und deine Runden auf einen Blick"),
    "maps": N_("Alle Callout-Karten – ansehen, von Hand einblenden, eigene Bilder und Notizen"),
    "overlay": N_("Was im Spiel erscheint, wo und wie gross"),
    "stats": N_("Deine Runden, Kills und Wartezeiten – nur auf diesem PC gespeichert"),
    "recordings": N_("Runden, Clips und Screenshots – abspielen, schneiden, aufräumen"),
    "server": N_("Server-Regionen wählen und die Verbindung im Blick behalten"),
    "settings": N_("Alles, was Fog Scout tut – suchen mit Strg+F"),
    "log": N_("Was das Programm gemacht hat – zum Nachlesen und für die Fehlersuche"),
}


SLIDER_MAX = 420                  # px (logical): longest slider (overlay position, size, opacity)


class WheelGuard(QObject):
    """The mouse wheel scrolls the page, never a setting (1.64.8, user: scrolling the page changed some random
    field). Qt hands the wheel to the combo box or slider under the mouse; here it goes to the page's scroll bar.
    1.11.13: installed on those widgets only (``guard_wheel``) – on the whole application every Qt event of every
    widget went through this Python method (~14 000 while the statistics page was built)."""

    def eventFilter(self, obj, event):
        if event.type() != QEvent.Wheel or not isinstance(obj, (QComboBox, QAbstractSlider, QAbstractSpinBox)):
            return False
        if isinstance(obj, QAbstractSlider) and obj.inherits("QScrollBar"):
            return False                               # the scroll bars themselves scroll as usual
        area = obj.parentWidget()
        while area is not None and not isinstance(area, QAbstractScrollArea):
            area = area.parentWidget()
        if area is not None:
            QApplication.sendEvent(area.verticalScrollBar(), event)
        return True                                    # the setting never changes


_WHEEL_GUARD = None                                    # kept here: Python would free the filter otherwise


def guard_wheel(w):
    """``w`` (a combo box, slider or spin box) no longer takes the mouse wheel – every one the windows create."""
    global _WHEEL_GUARD
    if _WHEEL_GUARD is None:
        _WHEEL_GUARD = WheelGuard()
    w.installEventFilter(_WHEEL_GUARD)
    return w


def pixmap_from_pil(img: Image.Image, height: int, ratio: float = 1.0) -> QPixmap:
    """Map picture (PIL, RGBA) -> QPixmap ``height`` logical px tall, sharp on scaled screens."""
    img = img.convert("RGBA")
    h = max(1, round(height * ratio))
    w = max(1, round(img.width * h / img.height))
    # 1.3.3: reducing_gap shrinks in big integer steps first (a 1440-px card to a 120-px preview: ~5× faster,
    # the same picture to the eye)
    img = img.resize((w, h), Image.LANCZOS, reducing_gap=2.0 if h < img.height else None)
    data = img.tobytes("raw", "RGBA")
    pm = QPixmap.fromImage(QImage(data, w, h, 4 * w, QImage.Format_RGBA8888).copy())
    pm.setDevicePixelRatio(ratio)
    return pm


ZWSP = "\u200b"


def soft_wrap(text: str, run: int = 16) -> str:
    """1.28 (audit F5): a zero-width space into every stretch longer than ``run`` characters without a space – a
    word-wrapped QLabel can only break at spaces, so a long URL or a run of letters from outside widened the layout.
    16, not 32: with the Windows font 32 wide letters took ~296 px, more than the editor's inspector (CI 1.28)."""
    out, n = [], 0
    for ch in str(text or ""):
        n = 0 if ch.isspace() else n + 1
        if n > run:
            out.append(ZWSP)
            n = 1
        out.append(ch)
    return "".join(out)


class PlainLabel(QLabel):
    """1.28 (audit F5): a label for text from outside (Claude's answers): always plain text – "<b>…</b>" or a link is
    shown as typed, never rendered –, wrapped, and long runs without spaces broken (soft_wrap); selectable, never a
    link that could be clicked."""

    def __init__(self, text="", cls=None):
        super().__init__()
        self.setTextFormat(Qt.PlainText)
        self.setWordWrap(True)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        if cls:
            self.setProperty("class", cls)
        self.setText(text)

    def setText(self, text):                     # noqa: N802 – Qt's name
        super().setText(soft_wrap(text))


def _label(text="", cls=None, wrap=False):
    w = QLabel(text)
    if cls:
        w.setProperty("class", cls)
    if wrap:
        w.setWordWrap(True)
    return w


def set_glyph(w, name, primary=False, tone="fg"):
    """1.24 (phase 2): a drawn sign (qt_icons) on a button in the colours of the theme now – set again only when the
    sign, the mode, the accent or the screen's pixel ratio changed (show_control runs on every refresh). The name is
    kept as the property "glyph" (the search knows a closed fold by "chevron_right"). ``tone`` "dim": a quiet sign
    that turns to the accent with the keyboard focus (the rounds' ▶ on the overview). 1.24.5: what was asked is
    kept (``_glyph_args``) – refresh_glyphs draws signs made before the theme was known, or on another screen."""
    ratio = w.devicePixelRatioF() or 1.0
    key = (name, bool(primary), tone, ratio, qt_theme.look_key())   # 1.24.5: no palette built just to compare
    if w.__dict__.get("_glyph_key") == key:             # (getattr of a missing name on a Qt widget: 3.7 µs)
        return                                          # (_glyph_args is part of the key – unchanged on a hit)
    w._glyph_args = (name, bool(primary), tone)
    from PySide6.QtCore import QSize
    from PySide6.QtGui import QIcon
    from . import qt_icons
    c = qt_theme.colours(qt_theme.current_dark())
    normal = c["on_accent"] if primary else c["dim"] if tone == "dim" else c["fg"]
    w._glyph_key = key
    w.setProperty("glyph", name or "")
    if not name:
        w.setIcon(QIcon())
        return
    w.setIcon(qt_icons.icon(name, normal, active=c["accent"] if tone == "dim" else None, disabled=c["fg_dis"],
                            size=qt_theme.ICON["m"], ratio=ratio))
    w.setIconSize(QSize(qt_theme.ICON["m"], qt_theme.ICON["m"]))


def refresh_glyphs(root):
    """1.24.5 (review): signs set once – on pages built before MainWindow.apply_theme (overview, maps) or before the
    window moved to a screen with another scale – drawn again in the colours and pixel ratio of now. Called on a
    theme change and on QEvent.DevicePixelRatioChange; the model's buttons follow on their own (show_control)."""
    from PySide6.QtWidgets import QAbstractButton
    for w in root.findChildren(QAbstractButton):
        args = w.__dict__.get("_glyph_args")
        if args and args[0]:
            set_glyph(w, *args)


def _tip(label: str) -> str:
    """Hover text of a button of the window itself (tooltip.TIPS, by German label)."""
    from .tooltip import tip_for_label
    return tip_for_label(_(label)) or ""


def _card():
    f = QFrame()
    f.setProperty("class", "card")
    return f


def _set(widget, text):
    if widget.text() != text:
        widget.setText(text)


def steady_scroll(sa):
    """1.8.24 (user: "das GUI springt ab und zu kurz nach links und wieder zurück"): a page close to the window's
    height got its scroll bar for a moment whenever a line came and went – everything moved left by its width and
    back. The bar is always there; without anything to scroll its handle is invisible (``idle``)."""
    sa.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    bar = sa.verticalScrollBar()

    def idle(_lo=0, hi=None):
        on = (bar.maximum() if hi is None else hi) <= 0
        if bar.property("idle") != on:
            bar.setProperty("idle", on)
            bar.style().unpolish(bar)
            bar.style().polish(bar)
    bar.rangeChanged.connect(idle)
    idle()
    return sa


def page_head(title: str, page_key: str = "") -> QVBoxLayout:
    """1.24: a page's title and the line under it (PAGE_SUBTITLES) – close together, apart from the page."""
    head = QVBoxLayout()
    head.setContentsMargins(0, 0, 0, 0)
    head.setSpacing(2)
    head.addWidget(_label(title, "h1"))
    sub = PAGE_SUBTITLES.get(page_key)
    if sub:
        head.addWidget(_label(_(sub), "subtitle", wrap=True))
    return head


def _scroll_page(title, scroll=True, page_key=""):
    """(page, body layout): a page that scrolls as a whole, with its title on top (``scroll`` False: a page that
    fits the window, its parts scroll on their own); 1.24: the page's purpose under the title (``page_key``)."""
    page = QWidget()
    page.setObjectName("page")
    outer = QVBoxLayout(page)
    outer.setContentsMargins(0, 0, 0, 0)
    body = QWidget()
    body.setObjectName("page")
    if scroll:
        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setFrameShape(QFrame.NoFrame)
        steady_scroll(sa)
        outer.addWidget(sa)
        sa.setWidget(body)
    else:
        outer.addWidget(body)
    lay = QVBoxLayout(body)
    lay.setContentsMargins(22, 18, 22, 18)
    lay.setSpacing(12)
    lay.addLayout(page_head(title, page_key))
    return page, lay
