"""The overlay editor (1.46, user: "Overlay-Steuerung grundlegend modernisieren … das Overlay-Fenster ist sehr klein"):
the page "Overlay" as one workspace – a tool bar (Anordnen, Rückgängig, Vorlage, Test, Fokus), the list of the
elements on the left (shown / own place / size, eye and lock), the canvas in the middle with all the room the
window has (qt_preview.PreviewView in fill mode) and a status line below it, and on the right the inspector of the
element picked (quick places, size, opacity, its settings). Built by qt_pages.FormPage from the spec kind "editor";
every control is still one of the page's ``controls`` – the search, ``open_tab`` and the App work as before.
"""
from __future__ import annotations

from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea,
                               QSizePolicy, QToolButton, QVBoxLayout, QWidget)

from . import qt_icons, qt_theme
from .i18n import N_, _

# element -> its settings tab (appconst.ELEMENT_TABS; repeated here: the Qt side never imports the App's mixins)
TABS = {"map": "ov.look", "text": "ov.look", "hud": "ov.sys", "today": "ov.today_f", "music": "ov.music_f",
        "inputs": "ov.inputs_f"}
GENERAL_TAB = "ov.pos"
NAMES = {"map": N_("Karte"), "text": N_("Infos"), "hud": N_("Systemwerte"), "today": N_("Heute"),
         "music": N_("Musik"), "inputs": N_("Eingaben")}
WHAT = {"map": N_("Callout-Karte der Map"), "text": N_("Timer, Bilanz, Server"), "hud": N_("CPU, GPU, RAM"),
        "today": N_("Runden und Zeit heute"), "music": N_("Läuft gerade"), "inputs": N_("Tasten und Gamepad")}
RAIL_W = 236                 # px at text zoom 1.0: the list of elements
INSPECTOR_W = 344            # px at text zoom 1.0: the settings of the element picked
WIDE_FROM = 1180             # px (× zoom): list | canvas | inspector side by side
MEDIUM_FROM = 720            # px (× zoom): the list as a row of chips on top, canvas | inspector below it
ALIGN_LABEL, ALIGN_COMBO = 104, 196     # px: row labels / choices of the inspector aligned at most this wide
PRESET_W = 190               # px: the choice of a preset in the tool bar
CELL = QSize(30, 20)         # one cell of the quick places (a small screen, 3×3)


def _icon_button(glyph: str, tip: str) -> QToolButton:
    b = QToolButton()
    b.setObjectName("ovicon")
    b.setAutoRaise(True)
    b.setCursor(Qt.PointingHandCursor)
    b.setFocusPolicy(Qt.TabFocus)
    b.setIconSize(QSize(qt_theme.ICON["m"], qt_theme.ICON["m"]))
    b._glyph = glyph
    b.setToolTip(tip)
    return b


def _paint_icon(b: QToolButton, glyph: str, on: bool):
    c = qt_theme.colours(qt_theme.current_dark())
    if b.__dict__.get("_painted") != (glyph, on, c["accent"], c["dim"]):
        b._painted = (glyph, on, c["accent"], c["dim"])
        b.setIcon(qt_icons.icon(glyph, c["accent"] if on else c["dim"]))


class _Row(QFrame):
    """One element in the list: its name and state, an eye (shown) and a lock (stays where it is)."""

    def __init__(self, rail, name: str):
        super().__init__()
        self.setObjectName("ovrow")
        self.name = name
        self._rail = rail
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.TabFocus)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(8, 5, 4, 5)
        lay.setSpacing(4)
        texts = QVBoxLayout()
        texts.setSpacing(0)
        self.title = QLabel(_(NAMES.get(name, name)) if name != "general" else _("Allgemein"))
        self.title.setObjectName("ovrowname")
        self.info = QLabel(_(WHAT.get(name, "")) if name != "general" else _("Stil, Abstand, Grenzen, Discord"))
        self.info.setObjectName("ovrowinfo")
        for lbl in (self.title, self.info):
            lbl.setAttribute(Qt.WA_TransparentForMouseEvents)
        texts.addWidget(self.title)
        texts.addWidget(self.info)
        lay.addLayout(texts, 1)
        self.eye = self.lock = None
        if name != "general":
            self.eye = _icon_button("eye", _("Ein- oder ausblenden"))
            self.eye.clicked.connect(lambda: rail.post(("show", name, not self.eye.property("on"))))
            self.lock = _icon_button("lock_open", _("Sperren: im Modus „Anordnen“ nicht mehr verschiebbar"))
            self.lock.clicked.connect(lambda: rail.post(("lock", name, not self.lock.property("on"))))
            lay.addWidget(self.eye)
            lay.addWidget(self.lock)

    def show_row(self, row: dict, selected: bool, can_hide: bool):
        if self.property("selected") != selected:
            self.setProperty("selected", selected)
            self.style().unpolish(self)
            self.style().polish(self)
        if self.eye is None:
            return
        shown, locked = bool(row.get("shown")), bool(row.get("locked"))
        off = not shown
        if self.title.property("off") != off:
            self.title.setProperty("off", off)
            self.title.style().unpolish(self.title)
            self.title.style().polish(self.title)
        parts = [_("eigener Platz") if row.get("own") else _("automatisch")] if shown else [_("ausgeblendet")]
        if shown and row.get("size"):
            parts.append(f"{round(row['size'])} %")
        info = " · ".join(parts)
        if self.info.text() != info:
            self.info.setText(info)
        self.eye.setProperty("on", shown)
        self.eye.setVisible(can_hide)
        _paint_icon(self.eye, "eye" if shown else "eye_off", False)
        self.eye.setToolTip(_("Ausblenden") if shown else _("Einblenden"))
        self.lock.setProperty("on", locked)
        _paint_icon(self.lock, "lock" if locked else "lock_open", locked)
        self.lock.setToolTip(_("Entsperren: wieder verschiebbar") if locked else
                             _("Sperren: im Modus „Anordnen“ nicht mehr verschiebbar"))

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._rail.post(("general",) if self.name == "general" else ("select", self.name))
            e.accept()
            return
        super().mousePressEvent(e)

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space):
            self._rail.post(("general",) if self.name == "general" else ("select", self.name))
            return
        super().keyPressEvent(e)

    def contextMenuEvent(self, e):
        if self.name != "general":
            gp = e.globalPos()
            self._rail.post(("menu", self.name, gp.x(), gp.y()))


class ElementRail(QWidget):
    """The list of the overlay's elements (control kind "elements", model ``ui.Elements``): a click picks one, the
    eye shows / hides it, the lock keeps it where it is, a right click opens its quick actions. Posts
    ("act", (key, value)) like every control."""

    COMPACT_COLS = 4                # columns of the list on a narrower page

    def __init__(self, key, post):
        super().__init__()
        self._key, self._post = key, post
        self._rows = {}
        self._order = ()
        self._compact = False
        self.general = False        # the tab "Allgemein" is open (the editor says so)
        self._data = {}
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(2)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    def post(self, value):
        self._post("act", (self._key, value))

    def rows(self) -> dict:
        return dict(self._rows)

    def set_compact(self, on: bool):
        if bool(on) != self._compact:
            self._compact = bool(on)
            self._place()

    def _place(self):
        for row in self._rows.values():
            self.grid.removeWidget(row)
        names = list(self._order) + ["general"]
        cols = self.COMPACT_COLS if self._compact else 1
        for i, name in enumerate(n for n in names if n in self._rows):
            self.grid.addWidget(self._rows[name], i // cols, i % cols)

    def show_state(self, st):
        self.setVisible(bool(st.get("visible", True)))
        data = st.get("data") or {}
        self._data = data
        order = tuple(data.get("order") or ())
        if order != self._order:
            for name in order + ("general",):
                if name not in self._rows:
                    self._rows[name] = _Row(self, name)
            for name in set(self._rows) - set(order) - {"general"}:
                self._rows.pop(name).deleteLater()
            self._order = order
            self._place()
        self.refresh()

    def refresh(self):
        data = self._data
        rows = data.get("rows") or {}
        sel = None if self.general else data.get("selected")
        for name, row in self._rows.items():
            if name == "general":
                row.show_row({}, self.general, False)
            else:
                r = rows.get(name) or {}
                row.show_row(r, name == sel, r.get("can_hide", True))


class AnchorGrid(QWidget):
    """Quick places for the element picked (control kind "anchors", model ``ui.Anchors``): a small screen of 3×3
    cells – corners, edges, centre – and "Üblicher Platz" (the automatic place). Posts ("cell", col, row) /
    ("auto",)."""

    def __init__(self, key, post):
        super().__init__()
        self._key, self._post = key, post
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)
        self.screen = QFrame()
        self.screen.setObjectName("ovcanvas")
        g = QGridLayout(self.screen)
        g.setContentsMargins(5, 5, 5, 5)
        g.setSpacing(4)
        self.cells = {}
        words = {(0, 0): N_("oben links"), (1, 0): N_("oben Mitte"), (2, 0): N_("oben rechts"),
                 (0, 1): N_("links Mitte"), (1, 1): N_("Mitte"), (2, 1): N_("rechts Mitte"),
                 (0, 2): N_("unten links"), (1, 2): N_("unten Mitte"), (2, 2): N_("unten rechts")}
        for (c, r), word in words.items():
            b = QPushButton()
            b.setObjectName("ovcell")
            b.setCheckable(True)
            b.setFixedSize(CELL)
            b.setCursor(Qt.PointingHandCursor)
            b.setFocusPolicy(Qt.TabFocus)
            b.setToolTip(_("Nach {where} legen (mit Rand)", where=_(word)))
            b.clicked.connect(lambda _c=False, c=c, r=r: self._click(("cell", c, r)))
            g.addWidget(b, r, c)
            self.cells[(c, r)] = b
        lay.addWidget(self.screen)
        side = QVBoxLayout()
        side.setSpacing(6)
        self.auto = QPushButton(_("Üblicher Platz"))
        self.auto.setCheckable(True)
        self.auto.setProperty("class", "toggle")
        self.auto.setFocusPolicy(Qt.TabFocus)
        self.auto.setToolTip(_("Zurück an den automatischen Platz (im schwarzen Balken, neben den anderen)"))
        self.auto.clicked.connect(lambda _c=False: self._click(("auto",)))
        self.note = QLabel("")
        self.note.setProperty("class", "hint")
        self.note.setWordWrap(True)
        side.addWidget(self.auto, 0, Qt.AlignLeft)
        side.addWidget(self.note)
        side.addStretch()
        lay.addLayout(side, 1)
        self._data = {}

    def _click(self, value):
        self._post("act", (self._key, value))
        self._show(self._data)                  # the App's answer sets the real state (no half-checked cell)

    def show_state(self, st):
        self.setVisible(bool(st.get("visible", True)))
        self._data = st.get("data") or {}
        self._show(self._data)

    def _show(self, data):
        cell = data.get("cell")
        on = tuple(cell) if isinstance(cell, (list, tuple)) else None
        for key, b in self.cells.items():
            if b.isChecked() != (key == on):
                b.setChecked(key == on)
        if self.auto.isChecked() != (cell == "auto"):
            self.auto.setChecked(cell == "auto")
        enabled = bool(data.get("enabled", True))
        self.screen.setEnabled(enabled)
        self.auto.setEnabled(enabled)
        text = _("Gesperrt – erst entsperren") if not enabled else data.get("note", "")
        if self.note.text() != text:
            self.note.setText(text)


class OverlayEditor(QWidget):
    """The page "Overlay" as an editor (see the module's text). ``item`` = ("editor", toolbar, rail, canvas,
    inspector): lists of spec items, built through the FormPage ``page`` (so every control is in page.controls)."""

    def __init__(self, page, item, page_key):
        super().__init__()
        from .qt_layouts import FlowRow
        self.page = page
        self._post = page._post
        _kind, toolbar, rail, canvas, inspector = item
        self._focus = False
        self._editing = False
        self._selected = None
        self._wide = None
        self._arranging = False
        # its width is the page's: its parts' minimum must not widen it (each width picks its own arrangement)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(10)
        # ---- tool bar: the moving mode first (the main action), the rarer ones after it, focus at the right end
        self.bar = QFrame()
        self.bar.setObjectName("ovbar")
        bl = QVBoxLayout(self.bar)
        bl.setContentsMargins(10, 8, 10, 8)
        row = FlowRow()
        cut = next((i for i, c in enumerate(toolbar) if c[0] == "stretch"), len(toolbar))
        row.right = len([c for c in toolbar[cut:] if c[0] != "stretch"])
        for c in toolbar:
            if c[0] != "stretch":
                page._add(c, row)
        bl.addLayout(row)
        preset = page.controls.get("ov.preset")
        if preset is not None:                          # the presets' names are long: the bar stays one line
            preset[1].setMaximumWidth(round(PRESET_W * qt_theme.current_zoom()))
        outer.addWidget(self.bar)
        # ---- body: list | canvas + status | inspector (a grid: arrange() puts them per width)
        self.body = QGridLayout()
        self.body.setSpacing(10)
        self.rail = QFrame()
        self.rail.setObjectName("ovrail")
        rl = QVBoxLayout(self.rail)
        rl.setContentsMargins(8, 10, 8, 10)
        rl.setSpacing(4)
        self.rail_head = QLabel(_("Elemente").upper())
        self.rail_head.setObjectName("ovsection")
        rl.addWidget(self.rail_head)
        page._items(rail, rl, page_key)
        rl.addStretch()
        self.canvas_box = QFrame()
        self.canvas_box.setObjectName("ovcanvas")
        cl = QVBoxLayout(self.canvas_box)
        cl.setContentsMargins(8, 8, 8, 6)
        cl.setSpacing(4)
        page._items(canvas, cl, page_key)
        self.canvas = next((w for k, (kind, w, _x) in page.controls.items() if kind == "preview"), None)
        if self.canvas is not None:
            self.canvas.set_fill(True)
            self.canvas.status_changed.connect(self._status)
            cl.setStretchFactor(self.canvas, 1)
        sl = QHBoxLayout()
        sl.setSpacing(12)
        self.status = QLabel("")
        self.status.setObjectName("ovstatus")
        self.status.setWordWrap(True)
        self.layout_label = QLabel("")
        self.layout_label.setObjectName("ovstatus")
        self.layout_label.setToolTip(_("Position und Grösse werden je DBD-Fenstergrösse gemerkt (Reiter Allgemein)."))
        sl.addWidget(self.status, 1)
        sl.addWidget(self.layout_label, 0, Qt.AlignRight | Qt.AlignTop)
        cl.addLayout(sl)
        self.inspector = QFrame()
        self.inspector.setObjectName("ovinspector")
        il = QVBoxLayout(self.inspector)
        il.setContentsMargins(0, 0, 0, 0)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        from .qt_common import steady_scroll
        steady_scroll(self.scroll)
        content = QWidget()
        content.setObjectName("page")
        self.content = content
        cl2 = QVBoxLayout(content)
        cl2.setContentsMargins(*qt_theme.PAD_CARD)
        cl2.setSpacing(6)
        self.head = QLabel("")
        self.head.setObjectName("ovhead")
        self.subhead = QLabel("")
        self.subhead.setObjectName("ovrowinfo")
        cl2.addWidget(self.head)
        cl2.addWidget(self.subhead)
        page.align_label_max, page.align_combo_max = ALIGN_LABEL, ALIGN_COMBO   # a narrow column: compact rows
        # the element's own part (quick place, size, opacity): one box the editor hides for "Allgemein" – never
        # the controls themselves (show_control shows them again on every refresh)
        self.element_box = QWidget()
        eb = QVBoxLayout(self.element_box)
        eb.setContentsMargins(0, 0, 0, 0)
        eb.setSpacing(6)
        cut = next((i for i, it in enumerate(inspector) if it[0] == "tabs"), len(inspector))
        page._group = []
        page._items(inspector[:cut], eb, page_key)
        page._align()                                   # sizes and opacity line up (aligned once texts are in)
        cl2.addWidget(self.element_box)
        page._items(inspector[cut:], cl2, page_key)
        cl2.addStretch()
        self.scroll.setWidget(content)
        il.addWidget(self.scroll)
        outer.addLayout(self.body, 1)
        # the element tabs: the inspector shows the one of the element picked – no tab row (the list is it)
        self.tabs = next((w for k, (kind, w, _x) in page.controls.items() if kind == "tab"), None)
        if self.tabs is not None:
            self.tabs.tabBar().hide()
            self.tabs.currentChanged.connect(self._tab_changed)
        self.rail_view = next((w for k, (kind, w, _x) in page.controls.items() if kind == "elements"), None)
        for body in (b for _k, (kind, _w, b) in page.controls.items() if kind == "tab"):
            body.layout().setContentsMargins(0, 4, 0, 0)    # the inspector has its own padding
        QShortcut(QKeySequence(Qt.Key_Escape), self, activated=self._escape, context=Qt.WidgetWithChildrenShortcut)
        self.arrange(1400)

    # ------------------------------------------------------------ layout
    def mode_for(self, width: int) -> str:
        z = qt_theme.current_zoom()
        return "wide" if width >= WIDE_FROM * z else "medium" if width >= MEDIUM_FROM * z else "narrow"

    def arrange(self, width: int):
        """"wide": list | canvas | inspector; "medium": the list as chips on top, canvas | inspector below it;
        "narrow": all below each other (the page scrolls). The canvas always gets the room left over."""
        mode = self.mode_for(width)
        if mode == self._wide:
            return
        self._wide = mode
        z = qt_theme.current_zoom()
        for w in (self.rail, self.canvas_box, self.inspector):
            self.body.removeWidget(w)
            w.setMinimumSize(0, 0)
            w.setMaximumSize(16777215, 16777215)
        for i in range(3):
            self.body.setColumnStretch(i, 0)
            self.body.setRowStretch(i, 0)
        if self.rail_view is not None:
            self.rail_view.set_compact(mode != "wide")
        self.rail_head.setVisible(mode == "wide")
        if mode == "wide":
            self.rail.setFixedWidth(round(RAIL_W * z))
            self.inspector.setFixedWidth(round(INSPECTOR_W * z))
            self.body.addWidget(self.rail, 0, 0)
            self.body.addWidget(self.canvas_box, 0, 1)
            self.body.addWidget(self.inspector, 0, 2)
            self.body.setColumnStretch(1, 1)
            self.body.setRowStretch(0, 1)
        elif mode == "medium":
            self.inspector.setFixedWidth(round(INSPECTOR_W * 0.92 * z))
            self.body.addWidget(self.rail, 0, 0, 1, 2)
            self.body.addWidget(self.canvas_box, 1, 0)
            self.body.addWidget(self.inspector, 1, 1)
            self.body.setColumnStretch(0, 1)
            self.body.setRowStretch(1, 1)
        else:
            self.inspector.setMinimumHeight(420)
            self.body.addWidget(self.rail, 0, 0)
            self.body.addWidget(self.canvas_box, 1, 0)
            self.body.addWidget(self.inspector, 2, 0)
            self.body.setColumnStretch(0, 1)
            self._narrow_canvas()

    def _narrow_canvas(self):
        h = max(220, round(self.width() * 0.5))
        if self.canvas_box.minimumHeight() != h:
            self.canvas_box.setMinimumHeight(h)

    def mode(self) -> str:
        return self._wide or ""

    def beside(self) -> bool:
        return self._wide == "wide"

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if self.mode_for(self.width()) != self._wide and not self._arranging:
            # never re-arrange inside a resize: removing and adding the parts makes the layout resize again (it
            # crashed Qt) – once, right after this event
            self._arranging = True
            QTimer.singleShot(0, self, self._arrange_now)
        elif self._wide == "narrow":
            self._narrow_canvas()

    def _arrange_now(self):
        self._arranging = False
        self.arrange(self.width())

    # ------------------------------------------------------------ state from the App
    def show_states(self, states):
        st = states.get("ov.focus_mode")
        if st is not None:
            self._set_focus(bool(st.get("pressed")))
        st = states.get("ov.elements")
        if st is not None:
            data = st.get("data") or {}
            self._editing = bool(data.get("editing"))
            self._selected = data.get("selected")
            if self.canvas_box.property("editing") != self._editing:
                self.canvas_box.setProperty("editing", self._editing)
                self.canvas_box.style().unpolish(self.canvas_box)
                self.canvas_box.style().polish(self.canvas_box)
            key = data.get("layout") or ""
            text = _("Layout für {size}", size=key.replace("x", "×")) if key else ""
            if self.layout_label.text() != text:
                self.layout_label.setText(text)
            self._head(data)
            if self.canvas is not None:
                self._status(self.canvas.__dict__.get("_status") or {})

    def _head(self, data):
        general = self.tabs is not None and self._current_frame() == GENERAL_TAB
        if self.rail_view is not None and self.rail_view.general != general:
            self.rail_view.general = general
            self.rail_view.refresh()
        name = data.get("selected")
        row = (data.get("rows") or {}).get(name) or {}
        if general:
            head, sub = _("Allgemein"), _("Gilt für alle Elemente")
        else:
            head = _(NAMES.get(name, name or ""))
            sub = _("gesperrt") if row.get("locked") else ""
            place = (_("eigener Platz") if row.get("own") else _("automatisch")) if row.get("shown", True) \
                else _("ausgeblendet")
            sub = " · ".join(p for p in (place, sub) if p)
        if self.head.text() != head:
            self.head.setText(head)
        if self.subhead.text() != sub:
            self.subhead.setText(sub)
        if self.element_box.isHidden() != general:
            self.element_box.setVisible(not general)

    def _current_frame(self):
        if self.tabs is None:
            return None
        cur = self.tabs.currentWidget()
        return next((k for k, (kind, w, body) in self.page.controls.items() if kind == "tab" and body is cur), None)

    def _tab_changed(self, _i):
        """A tab opened by the search / reveal: the list follows (the element of that tab is picked). A tab the App
        opened for its own pick (MainWindow.open_tab) is not reported back – with a stale pick on a page not shown,
        the two picks sent each other back and forth for ever."""
        frame = self._current_frame()
        if self.tabs.__dict__.get("_by_app"):
            pass
        elif frame == GENERAL_TAB:
            self._post("act", ("ov.elements", ("general",)))
        elif frame and TABS.get(self._selected) != frame:
            name = next((n for n, f in TABS.items() if f == frame), None)
            if name:
                self._post("act", ("ov.elements", ("select", name)))
        if self.rail_view is not None:
            self.rail_view.general = frame == GENERAL_TAB
            self.rail_view.refresh()
        self.scroll.verticalScrollBar().setValue(0)

    # ------------------------------------------------------------ focus view, Esc, status line
    def _set_focus(self, on: bool):
        if on == self._focus:
            return
        self._focus = on
        self.rail.setVisible(not on)
        self.inspector.setVisible(not on)
        for lbl in self.page.findChildren(QLabel):
            if lbl.property("class") in ("h1", "subtitle") and not self.isAncestorOf(lbl):
                lbl.setVisible(not on)

    def focus_on(self) -> bool:
        return self._focus

    def _escape(self):
        if self._focus:
            self._post("act", ("ov.focus_mode", None))
        elif self._editing:
            self._post("act", ("ov.edit", None))

    def _status(self, st: dict):
        name = lambda n: _(NAMES.get(n, n or ""))          # noqa: E731
        editing = bool(st.get("editing", self._editing))
        if st.get("limit"):
            text = _("Grenzlinie: ziehen, bis wohin die Elemente im Balken reichen")
        elif st.get("sizing"):
            text = _("Grösse von {name}: Ecke ziehen", name=name(st["sizing"]))
        elif st.get("grab"):
            text = _("Ziehst: {name}", name=name(st["grab"])) + " · " + \
                (_("eingerastet") if st.get("snapped") else _("rastet an Mitte, Balken und anderen ein (Alt = frei)"))
        elif editing and st.get("hover") and st["hover"] in (st.get("locked") or ()):
            text = _("{name} ist gesperrt – das Schloss in der Liste löst es", name=name(st["hover"]))
        elif editing and st.get("hover"):
            text = _("{name}: ziehen = verschieben · Ecke oder Strg+Mausrad = Grösse · Rechtsklick = Menü",
                     name=name(st["hover"]))
        elif editing:
            text = _("Anordnen aktiv – auch im Spiel: Elemente ziehen · Pfeiltasten = fein (Shift = 10 px) · "
                     "Tab = nächstes Element · Esc = fertig")
            if st.get("limits_off"):
                text += " · " + _("graue Linien in den Balken = Grenzen (aus) – eine ziehen schaltet sie ein")
        elif st.get("hover"):
            text = _("Klick wählt {name}", name=name(st["hover"]))
        else:
            text = _("Klick wählt ein Element · „Anordnen“ schaltet das Verschieben ein – hier und im Spiel")
        if self.status.text() != text:
            self.status.setText(text)
        if self.status.property("editing") != editing:
            self.status.setProperty("editing", editing)
            self.status.style().unpolish(self.status)
            self.status.style().polish(self.status)

