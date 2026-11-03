"""The pages of the control window: the overview, the hand-made pages (SPECS) with their controls, the pages built from
a tab's structure (AutoPage), dialogs and the setup assistant.
"""
from __future__ import annotations

from PySide6.QtCore import QEvent, QRectF, QSize, Qt, QTimer
from PySide6.QtGui import QColor, QGuiApplication, QPainter, QPen
from PySide6.QtWidgets import (QBoxLayout, QComboBox, QDialog, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QProgressBar,
                               QPushButton, QRadioButton, QScrollArea, QSizePolicy, QSlider, QStackedWidget,
                               QStyle, QStyleOptionSlider, QTabWidget, QVBoxLayout, QWidget)

from . import qt_theme
from .qt_layouts import FlowRow, TileGrid, WrapCheck
from .i18n import N_, _
from .qt_common import SLIDER_MAX, guard_wheel, pixmap_from_pil, steady_scroll, _label, _tip, _card, _set, _scroll_page, page_head, set_glyph
from .qt_views import FactBox, Table, LogView, HotkeyButton, Chart, SwatchView, TilesView, DashboardView
from .qt_preview import PreviewView


THUMB_H = 170                     # px (logical) of the map picture on the overview


SETUP_W = 820                     # px (logical): widest step of the setup assistant


# The setup assistant on the first start (1.60, user's wish): three steps of controls that are also on the pages
# (same keys – the same widgets of the UI model). ("note", text) = an explaining line of the step itself.
GAME_LANGS = ("en", "de", "fr", "es", "es-MX", "it", "pl", "pt-BR", "tr")   # app.LANGS (test: the same)


SETUP_HOTKEYS = ("toggle_overlay", "rotate_map", "edit_position", "scan_now", "reject_map")


SETUP = (
    (N_("Sprache"), (
        ("note", N_("Das Programm liest beim Match-Start den Map-Namen aus dem Bild. Hake die Sprache an, in der "
                    "du Dead by Daylight spielst (mehrere gehen).")),
        ("grid", 5, tuple(("check", f"det.lang.{code}") for code in GAME_LANGS)),
        ("note", N_("Sprache dieses Programms:")),
        ("row", (("combo", "st.lang"), ("stretch",))), ("hint", "st.lang_note"))),
    (N_("Overlay"), (
        ("note", N_("Die Karte erscheint beim Match-Start von selbst und verschwindet nach der Runde. „automatisch“ "
                    "legt sie in den schwarzen Rand neben dem Spielbild (Ultrawide) bzw. neben das DBD-Fenster.")),
        # 1.8.45: in exclusive fullscreen no window can show above the game – said only in the README before
        ("note", N_("Wichtig: In DBD unter Einstellungen → Grafik den Anzeigemodus „Fenster-Vollbild“ wählen. Im "
                    "exklusiven Vollbild kann Windows kein Fenster über dem Spiel zeigen – die Karte bliebe "
                    "unsichtbar.")),
        ("preview", "ov.preview"),                   # 1.2.19: the live preview of the overlay page here too
        ("row", (("label", "ov.anchor.label"), ("combo", "ov.anchor"), ("stretch",))),
        ("slider", "ov.size"),
        ("row", (("button", "ov.test"), ("button", "ov.edit"), ("stretch",))),
        ("note", N_("„Overlay testen“ zeigt die Karte sofort, „Mit der Maus verschieben“ lässt sie dich hinziehen.")),
        ("sub", N_("Systemwerte")),              # 1.8.2: "Position" alone did not say what it places
        ("row", (("label", "ov.sysinfo.label"), ("combo", "ov.sysinfo"), ("stretch",))),
        ("check", "ov.today"), ("check", "ov.media"))),
    (N_("Tasten und Start"), (
        ("note", N_("Die wichtigsten Tasten – zum Ändern draufklicken und die neue Kombination drücken. Alle "
                    "Tasten findest du später unter Einstellungen.")),
        ("grid", 1, tuple(("row", (("label", f"st.hk.{k}.label"), ("stretch",), ("hotkey", f"st.hk.{k}")))
                          for k in SETUP_HOTKEYS)),
        ("check", "st.autostart"), ("check", "st.lobby_notify"))),
    # 1.2.15: the stats-page link was only deep in the settings; new users never found it
    (N_("Match-Daten"), (
        ("note", N_("Kills, Entkommen und Bloodpoints deiner Runden kommen von stats.deadbydaylight.com – geladen "
                    "von deinem Browser, nicht vom Programm. Lässt sich auch später einrichten (Einstellungen → "
                    "Match-Daten → Offizielle Match-Daten).")),
        ("row", (("button", "setup.script"), ("button", "setup.open_site"), ("stretch",))),
        ("check", "setup.off_notify"), ("check", "setup.off_open"), ("hint", "setup.off_text"))),
)


class OverviewPage(QWidget):
    def __init__(self, post):
        super().__init__()
        self.setObjectName("page")
        self._post = post
        self._thumb_rev = None
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        steady_scroll(scroll)
        outer.addWidget(scroll)
        body = QWidget()
        body.setObjectName("page")
        scroll.setWidget(body)
        page = QVBoxLayout(body)
        page.setContentsMargins(22, 18, 22, 18)
        page.setSpacing(12)                       # 1.11.14: like every other page (_scroll_page), was 14

        # 1.24 (phase 2): title and purpose like every page – the state went to the foot of the navigation
        # (MainWindow.show_status), where every page shows it; the pill here showed it on the overview only
        page.addLayout(page_head(_("Übersicht"), "overview"))
        # 1.24.5 (review): narrow window – the navigation shows only the state's sign; here the words again
        self.status_line = _label(cls="dim", wrap=True)
        self.status_line.setVisible(False)
        self._status_now = ("idle", "")
        page.addWidget(self.status_line)

        # the map on display: picture, name, values, actions
        card = _card()
        cl = QHBoxLayout(card)
        cl.setContentsMargins(16, 16, 16, 16)
        cl.setSpacing(18)
        self.thumb = QLabel()
        self.thumb.setObjectName("thumb")
        self.thumb.setFixedSize(THUMB_H + 12, THUMB_H + 12)
        self.thumb.setAlignment(Qt.AlignCenter)
        cl.addWidget(self.thumb, alignment=Qt.AlignTop)
        info = QVBoxLayout()
        info.setSpacing(4)
        info.addWidget(_label(_("Aktuelle Map").upper(), "h2"))
        self.map_name = _label(cls="map", wrap=True)
        info.addWidget(self.map_name)
        self.map_line = _label(cls="dim", wrap=True)
        info.addWidget(self.map_line)
        self.queue = _label(cls="dim", wrap=True)
        info.addWidget(self.queue)
        info.addSpacing(8)
        grid = TileGrid(min_width=110, columns=4, spacing=20)    # four values side by side, or two by two
        self.facts = [FactBox(post=post) for _i in range(4)]
        for box in self.facts:
            grid.addWidget(box)
        info.addLayout(grid)
        self.note = _label(cls="note", wrap=True)
        info.addWidget(self.note)
        self.unknown = QWidget()
        ul = QHBoxLayout(self.unknown)
        ul.setContentsMargins(0, 0, 0, 0)
        self.unknown_text = _label(cls="note", wrap=True)
        ul.addWidget(self.unknown_text, 1)
        for text, action in ((N_("Zuordnen …"), "assign"), (N_("Bild hinzufügen …"), "picture"),
                             ("", "dismiss_unknown")):
            ub = QPushButton(_(text) if text else "")
            if action == "dismiss_unknown":       # 1.24: a drawn cross, not "✕"
                set_glyph(ub, "close")
                ub.setToolTip(_("Hinweis ausblenden."))
                ub.setAccessibleName(_("Hinweis ausblenden."))
            else:
                ub.setToolTip(_tip(text))
            ub.clicked.connect(lambda _c=False, a=action: self._post(a))
            ul.addWidget(ub)
        info.addWidget(self.unknown)
        info.addStretch()
        btns = FlowRow(spacing=6)                 # the buttons wrap instead of running out of the card
        self.buttons = {}
        for key in ("scan", "choose", "rotate", "toggle", "reject", "confirm", "layout", "floor", "power"):
            b = QPushButton()
            b.clicked.connect(lambda _c=False, k=key: self._post(k))
            btns.addWidget(b)
            self.buttons[key] = b
        info.addLayout(btns)
        cl.addLayout(info, 1)
        card.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)    # without a picture: only as tall as its text
        page.addWidget(card)

        # 1.14: "Schnell ein/aus" – one tick box per feature (overview.switches), made as the model names them
        self.switch_card = _card()
        swl = QVBoxLayout(self.switch_card)
        swl.setContentsMargins(*qt_theme.PAD_CARD)
        swl.setSpacing(8)
        # 1.24 (phase 2): "Funktionen" – each box with what it does now below it (overview.switch_state)
        swl.addWidget(_label(_("Funktionen").upper(), "h2"))
        # 1.28.3 (user: "nicht alles sauber in einer Reihe"): equal columns, rows evened out (9 = 3 × 3 or 5 + 4)
        self.switch_row = TileGrid(min_width=SWITCH_W, columns=6, spacing=18)
        swl.addLayout(self.switch_row)
        self.switches = []
        self.switch_states = []                   # the words under each box (QLabel, property "state")
        self.switch_card.setVisible(False)
        page.addWidget(self.switch_card)

        # 1.8.79: what changed since the version last run (HISTORY.md rows), until "Verstanden"
        self.news_card = _card()
        self.news_lay = QVBoxLayout(self.news_card)
        self.news_lay.setContentsMargins(*qt_theme.PAD_CARD)
        nh = QHBoxLayout()
        self.news_title = _label(cls="h2")
        nh.addWidget(self.news_title)
        nh.addStretch()
        self.news_button = QPushButton(_("Verstanden"))
        self.news_button.setToolTip(_tip("Verstanden"))
        self.news_button.clicked.connect(lambda _c=False: self._post("news_seen"))
        nh.addWidget(self.news_button)
        self.news_lay.addLayout(nh)
        self.news_rows = []
        self.news_lay.addWidget(_label(_("Aus HISTORY.md (Deutsch), die neuesten zuerst."), "dim"))
        self.news_card.setVisible(False)
        page.addWidget(self.news_card)

        # today
        head = QHBoxLayout()
        head.addWidget(_label(_("Heute").upper(), "h2"))
        head.addStretch()
        self.today_note = _label(cls="dim")
        head.addWidget(self.today_note)
        page.addLayout(head)
        self.today_grid = TileGrid(min_width=170, columns=5)
        self.tiles, self.tile_cards = [], []
        for _i in range(4):                       # 1.24.7: more on demand (_today_tile) – up to seven facts
            self._today_tile().setVisible(True)
        page.addLayout(self.today_grid)

        # 1.8.83: this week against the last one – shown only once a week has rounds
        head = QHBoxLayout()
        self.week_title = _label(_("Diese Woche").upper(), "h2")
        head.addWidget(self.week_title)
        head.addStretch()
        self.week_note = _label(cls="dim", wrap=True)
        head.addWidget(self.week_note, 1)
        page.addLayout(head)
        wgrid = TileGrid(min_width=170, columns=5, stretch=False)   # 1.24.7: two tiles not half the page wide
        self.week_tiles, self.week_cards = [], []
        for _i in range(5):
            t = _card()
            tl = QVBoxLayout(t)
            tl.setContentsMargins(*qt_theme.PAD_CARD)
            box = FactBox(post=post)
            box.sub.setWordWrap(True)
            tl.addWidget(box)
            wgrid.addWidget(t)
            self.week_tiles.append(box)
            self.week_cards.append(t)
            t.setVisible(False)
        self.week_title.setVisible(False)
        self.week_note.setVisible(False)
        page.addLayout(wgrid)

        # system values and the last rounds
        row = TileGrid(min_width=300, columns=2)  # side by side, below each other in a narrow window
        sysc = _card()
        self.sys_lay = QVBoxLayout(sysc)
        self.sys_lay.setContentsMargins(*qt_theme.PAD_CARD)
        self.sys_lay.addWidget(_label(_("System").upper(), "h2"))
        self.sys_rows = []
        self.sys_note = _label(cls="dim", wrap=True)
        self.sys_lay.addWidget(self.sys_note)
        self.sys_lay.addStretch()
        row.addWidget(sysc)
        last = _card()
        self.last_lay = QVBoxLayout(last)
        self.last_lay.setContentsMargins(*qt_theme.PAD_CARD)
        self.last_lay.addWidget(_label(_("Letzte Runden").upper(), "h2"))
        self.last_rows = []
        self.last_empty = _label(_("Noch keine Runden gespeichert."), "dim")
        self.last_lay.addWidget(self.last_empty)
        self.last_lay.addStretch()
        row.addWidget(last)
        page.addLayout(row)
        # 1.11.14: rounds per day over the last two weeks (the room below the cards was empty)
        self.days_card = _card()
        dl = QVBoxLayout(self.days_card)
        dl.setContentsMargins(14, 8, 14, 8)
        self.days_chart = Chart()
        dl.addWidget(self.days_chart)
        self.days_card.setVisible(False)
        page.addWidget(self.days_card)
        page.addStretch()

    # ------------------------------------------------------------- update
    def show_status_line(self, on: bool):
        """1.24.5: the state in words under the title while the navigation is narrow (MainWindow._compact_nav)."""
        if self.status_line.isHidden() == bool(on):
            self.status_line.setVisible(bool(on))
        if on:
            self._status_paint()

    def _status_paint(self):
        kind, text = self._status_now
        level = {"ok": "ok", "warn": "warn", "err": "err"}.get(kind, "")
        if self.status_line.__dict__.get("_level") != level:
            self.status_line._level = level
            self.status_line.setProperty("state", level)
            self.status_line.style().unpolish(self.status_line)
            self.status_line.style().polish(self.status_line)
        _set(self.status_line, text)

    def update_page(self, o, thumb=None, tips=None):
        self._status_now = (o.status_kind, o.status_text)
        if not self.status_line.isHidden():
            self._status_paint()
        _set(self.map_name, o.map_label or _("Noch keine Map"))
        _set(self.map_line, o.map_line)
        _set(self.queue, o.queue)
        self.queue.setVisible(bool(o.queue))
        # 1.66.3: without a map no empty picture box and no row of dashes – only the line how one comes
        self.thumb.setVisible(bool(o.map_label))
        empty = not o.map_label and all(f.value == "–" for f in o.facts)
        for box in self.facts:
            box.setVisible(not empty)
        if o.thumb_rev != self._thumb_rev:
            self._thumb_rev = o.thumb_rev
            if thumb is None:
                self.thumb.clear()
            else:
                h = THUMB_H if thumb.height >= thumb.width else round(THUMB_H * thumb.height / thumb.width)
                self.thumb.setPixmap(pixmap_from_pil(thumb, max(1, h), self.devicePixelRatioF()))   # fits both ways
        for box, f in zip(self.facts, o.facts):
            box.show_fact(f)
        _set(self.note, o.note)
        self.note.setVisible(bool(o.note))
        _set(self.unknown_text, o.unknown)
        self.unknown.setVisible(bool(o.unknown))
        for key, b in self.buttons.items():
            a = o.actions.get(key)
            b.setVisible(a is not None)
            if a is not None:
                _set(b, a[1])
                b.setEnabled(a[0])
                name = "primary" if key == o.primary else ""      # 1.24: the main action follows the state
                if b.objectName() != name:
                    b.setObjectName(name)
                    b.style().unpolish(b)
                    b.style().polish(b)
                set_glyph(b, OVERVIEW_GLYPHS.get(key), primary=key == o.primary)
                if tips:
                    tip = tips(key, a[1]) or ""
                    if b.toolTip() != tip:
                        b.setToolTip(tip)
        _set(self.today_note, o.today_note)
        while len(self.tiles) < len(o.today):
            self._today_tile()
        for i, (box, card) in enumerate(zip(self.tiles, self.tile_cards)):
            if i < len(o.today):
                box.show_fact(o.today[i])
            if card.isVisible() != (i < len(o.today)):
                card.setVisible(i < len(o.today))
        self.week_title.setVisible(bool(o.week))
        self.week_note.setVisible(bool(o.week))
        _set(self.week_note, o.week_note)
        for i, (box, card) in enumerate(zip(self.week_tiles, self.week_cards)):
            if i < len(o.week):
                box.show_fact(o.week[i])
            card.setVisible(i < len(o.week))
        self._show_switches(getattr(o, "switches", None) or [])
        self._show_system(o)
        self._show_rounds(o.rounds)
        self._show_news(o)
        days = getattr(o, "days", None) or {}
        if days:
            self.days_chart.show_state({"data": days, "dark": getattr(o, "dark", True), "panels": ("rounds",)})
        self.days_card.setVisible(bool(days))

    def _today_tile(self) -> QWidget:
        """One tile of „Heute“ (1.24.7: made when needed – five fixed widgets dropped the sixth and seventh fact)."""
        t = _card()
        tl = QVBoxLayout(t)
        tl.setContentsMargins(*qt_theme.PAD_CARD)
        box = FactBox(bar=True, post=self._post)
        box.sub.setWordWrap(True)
        tl.addWidget(box)
        self.today_grid.addWidget(t)
        self.tiles.append(box)
        self.tile_cards.append(t)
        t.setVisible(False)
        return t

    def _show_switches(self, switches):
        """The boxes follow the model: text, tooltip (by the German label, tooltip.TIPS), state – setChecked
        does not emit clicked, so only the user's click posts ("switch", (key, on))."""
        from .tooltip import tip_for_label
        while len(self.switches) < len(switches):
            item = QWidget()
            col = QVBoxLayout(item)
            col.setContentsMargins(0, 0, 0, 0)
            col.setSpacing(0)
            w = WrapCheck()
            w.key = ""
            w.clicked.connect(lambda on, w=w: self._post("switch", (w.key, bool(on))))
            state = _label(cls="dim")                          # under the box's text, not under the box
            pol = state.sizePolicy()                           # a box with nothing to say keeps the line: the
            pol.setRetainSizeWhenHidden(True)                  # row's boxes stay on one height
            state.setSizePolicy(pol)
            col.addWidget(w)
            col.addWidget(state)
            col.addStretch(1)                                  # top-aligned when a neighbour wraps to two lines
            self.switch_row.addWidget(item)
            self.switches.append(w)
            self.switch_states.append(state)
        look = (qt_theme.look_key(), qt_theme.current_zoom())
        for i, w in enumerate(self.switches):
            shown = i < len(switches)
            item = w.parentWidget()
            if item.isHidden() == shown:
                item.setVisible(shown)
            if w.isHidden() == shown:                 # the box too: callers ask the box (isHidden)
                w.setVisible(shown)
            if not shown:
                continue
            sw = switches[i]
            label = self.switch_states[i]
            if label.__dict__.get("_look") != look:   # 1.24.7 (visual QA): the indent of the box's own text
                label._look = look                      # (indicator + spacing of WrapCheck), not a fixed 27 px
                label.setContentsMargins(w.box.sizeHint().width() + w.layout().spacing(), 0, 0, 0)
            level = getattr(sw, "level", "")
            if label.__dict__.get("_level") != level:            # 1.24.5: a Python attribute, not a property read
                label._level = level
                label.setProperty("state", level)
                label.style().unpolish(label)
                label.style().polish(label)
            _set(label, getattr(sw, "state", ""))
            if label.isHidden() == bool(getattr(sw, "state", "")):
                label.setVisible(bool(getattr(sw, "state", "")))
            w.key = sw.key
            if w.text() != sw.label:
                w.setText(sw.label)
                w.setToolTip(tip_for_label(sw.label) or "")
            if w.isChecked() != sw.on:
                w.setChecked(sw.on)
            if w.isEnabled() != sw.enabled:
                w.setEnabled(sw.enabled)
        self.switch_card.setVisible(bool(switches))

    def _show_news(self, o):
        while len(self.news_rows) < len(o.news):
            head, body = _label(wrap=True), _label(cls="dim", wrap=True)
            pos = 1 + 2 * len(self.news_rows)
            self.news_lay.insertWidget(pos, head)
            self.news_lay.insertWidget(pos + 1, body)
            self.news_rows.append((head, body))
        for i, (head, body) in enumerate(self.news_rows):
            shown = i < len(o.news)
            head.setVisible(shown)
            body.setVisible(shown and bool(o.news[i][2]))
            if shown:
                version, title, detail = o.news[i]
                _set(head, f"{version} – {title}")
                _set(body, detail)
        _set(self.news_title, o.news_since.upper())
        self.news_card.setVisible(bool(o.news))      # isVisible() lies while the window is hidden

    def _show_system(self, o):
        while len(self.sys_rows) < len(o.system):
            r = QHBoxLayout()
            name, value = _label(cls="dim"), _label()
            r.addWidget(name)
            r.addStretch()
            r.addWidget(value)
            bar = QProgressBar()
            bar.setTextVisible(False)
            bar.setRange(0, 1000)
            pos = 1 + 2 * len(self.sys_rows)
            self.sys_lay.insertLayout(pos, r)
            self.sys_lay.insertWidget(pos + 1, bar)
            self.sys_rows.append((name, value, bar, [None]))
        for i, (name, value, bar, colour) in enumerate(self.sys_rows):
            shown = i < len(o.system)
            for w in (name, value):
                w.setVisible(shown)
            if not shown:
                bar.setVisible(False)
                continue
            label, text, frac, col = o.system[i]
            _set(name, label)
            _set(value, text)
            bar.setVisible(frac is not None)
            bar.setValue(round(1000 * min(1.0, max(0.0, frac or 0.0))))
            want = qt_theme.bar_style(col) if col is not None else ""
            if want != colour[0]:
                colour[0] = want
                bar.setStyleSheet(want)
        _set(self.sys_note, o.system_note)
        self.sys_note.setVisible(bool(o.system_note))

    def _show_rounds(self, rounds):
        while len(self.last_rows) < len(rounds):
            row = RoundRowView(self._post)
            self.last_lay.insertWidget(1 + len(self.last_rows), row)
            self.last_rows.append(row)
        for i, row in enumerate(self.last_rows):
            shown = i < len(rounds)
            row.setVisible(shown)
            if shown:
                row.show_round(rounds[i])
        self.last_empty.setVisible(not rounds)


class RoundRowView(QFrame):
    """1.17.1: one row of the overview's "Letzte Runden" – a click opens the round in Statistik › Letzte Runden,
    ▶ (only with a recording of it) opens it on the page Aufnahmen. Rows are made once and refilled."""

    def __init__(self, post):
        super().__init__()
        self._post, self._t = post, None
        self.setObjectName("roundrow")
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(_("In der Statistik zeigen"))
        lay = QHBoxLayout(self)
        lay.setContentsMargins(4, 1, 2, 1)
        lay.setSpacing(6)
        self.left, self.right = _label(), _label(cls="dim")
        self.left.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)   # long names must not widen it
        lay.addWidget(self.left, 1)
        lay.addWidget(self.right)
        self.play = QPushButton()
        set_glyph(self.play, "play", tone="dim")  # 1.24: a drawn sign, not "▶"; 1.24.5: quiet like #rowplay was
        self.play.setAccessibleName(_("Aufnahme dieser Runde öffnen"))
        self.play.setObjectName("rowplay")
        self.play.setCursor(Qt.PointingHandCursor)
        self.play.setFocusPolicy(Qt.TabFocus)
        self.play.setToolTip(_("Aufnahme dieser Runde öffnen"))
        self.play.clicked.connect(lambda: self._t is not None and self._post("ov_recording", self._t))
        lay.addWidget(self.play)

    def show_round(self, r):
        _set(self.left, r[0])
        _set(self.right, r[1])
        self._t = r[2] if len(r) > 2 else None
        has = len(r) > 3 and bool(r[3])
        if self.play.isHidden() == has:              # its own flag – isVisible() is False before the window shows
            self.play.setVisible(has)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self._t is not None:
            self._post("ov_round", self._t)
            e.accept()
            return
        super().mousePressEvent(e)


class HintLabel(QLabel):
    """1.17.1: a hint text. Standing on a line of its own (in a vertical layout) it wraps at about HINT_CHARS
    characters instead of running across a 1400-px card; beside controls (a row) it takes the room as before. The
    cap is part of heightForWidth – the page's own layouts ask with the full width and would cut the last lines."""

    def __init__(self, cls="hint"):
        super().__init__("")
        self.setProperty("class", cls)
        self.setWordWrap(True)
        self._capped = None                       # None = not decided yet (first show), then True/False

    def _cap(self) -> int:
        return self.fontMetrics().averageCharWidth() * HINT_CHARS

    def _decide(self):
        p = self.parentWidget()
        holder = _holder(p.layout(), self) if p is not None and p.layout() is not None else None
        self._capped = isinstance(holder, QBoxLayout) and holder.direction() in (QBoxLayout.TopToBottom,
                                                                                QBoxLayout.BottomToTop)
        self.setMaximumWidth(self._cap() if self._capped else 16777215)
        self.updateGeometry()

    def showEvent(self, e):
        if self._capped is None:
            self._decide()
        super().showEvent(e)

    def changeEvent(self, e):
        super().changeEvent(e)
        if self._capped and e.type() in (QEvent.FontChange, QEvent.StyleChange):
            self.setMaximumWidth(self._cap())          # zoom: the cap follows the font

    def heightForWidth(self, w: int) -> int:
        return super().heightForWidth(min(w, self._cap()) if self._capped else w)


def _holder(layout, w):
    """The layout (nested ones included) that holds widget ``w``, or None."""
    for i in range(layout.count()):
        it = layout.itemAt(i)
        if it.widget() is w:
            return layout
        if it.layout() is not None:
            found = _holder(it.layout(), w)
            if found is not None:
                return found
    return None


SWITCH_W = 180                              # 1.28.3: width of a column in the card „Funktionen“ (one line for most labels)
HINT_CHARS = 100                            # 1.17.1: a hint line wraps at about this many characters

NOTE_KEYS = {"ov.size_cap"}                 # 1.8.24: hints that warn (amber) instead of explaining (grey)


class CapSlider(QSlider):
    """A slider that marks ``cap`` (1.8.24, user: "Map mit der Scrollbar grösser – ändert sich nicht"): from that
    value on the element does not grow any more (the black bar is full) – a line there, the rest of the groove
    tinted."""
    cap = None

    def set_cap(self, cap):
        if cap != self.cap:
            self.cap = cap
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        lo, hi = self.minimum(), self.maximum()
        if self.cap is None or hi <= lo or not lo <= self.cap < hi:
            return
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        groove = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
        handle = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)
        span = max(1, groove.width() - handle.width())
        x = groove.x() + handle.width() / 2 + QStyle.sliderPositionFromValue(lo, hi, round(self.cap), span)
        colour = QColor(qt_theme.dot_colour("warn"))
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        tint = QColor(colour)
        tint.setAlpha(70)
        cy = groove.center().y()
        p.fillRect(QRectF(x, cy - 3, groove.right() - x, 6), tint)
        p.setPen(QPen(colour, 2))
        p.drawLine(round(x), self.rect().top() + 3, round(x), self.rect().bottom() - 3)
        p.end()


def make_control(kind, key, post):
    """(widget, extra) of one control of the UI model; clicks go out as post("act", (key, value))."""
    extra = None
    if kind == "check":
        w = WrapCheck()                           # its text wraps in a narrow window (QCheckBox's does not)
        w.clicked.connect(lambda checked: post("act", (key, checked)))
    elif kind == "button":
        w = QPushButton()
        # Tab only, no focus by click (1.62.2): a button that disables itself on click passed its focus on and
        # the page scrolled to whatever came next in the tab order
        w.setFocusPolicy(Qt.TabFocus)
        w.clicked.connect(lambda _c=False: post("act", (key, None)))
    elif kind == "combo":
        w = guard_wheel(QComboBox())
        w.setMinimumWidth(140)
        w.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        w.activated.connect(lambda i: post("act", (key, w.itemText(i))))
        w.editTextChanged.connect(lambda text: w.isEditable() and w.hasFocus() and post("act", (key, text)))
    elif kind == "slider":
        w = QWidget()
        r = QHBoxLayout(w)
        r.setContentsMargins(0, 0, 0, 0)
        name, value = _label(), _label()
        name.setMinimumWidth(110)
        value.setMinimumWidth(56)
        value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        s = guard_wheel(CapSlider(Qt.Horizontal))
        s.setMaximumWidth(SLIDER_MAX)              # a wide window: no slider across the whole page
        s.valueChanged.connect(lambda v: post("act", (key, v)))
        r.addWidget(name)
        r.addWidget(s, 1)
        r.addWidget(value)
        r.addStretch()
        extra = (name, s, value)
    elif kind == "table":
        w = Table(key, post)
    elif kind == "chart":
        w = Chart()
    elif kind == "dashboard":
        w = DashboardView(key, post)
    elif kind == "tiles":
        w = TilesView()
    elif kind == "preview":
        w = PreviewView(key, post)
    elif kind == "swatches":
        w = SwatchView(key, post)
    elif kind == "host":
        w = HostView()
    elif kind == "log":
        w = LogView()
    elif kind == "radio":
        w = QRadioButton()
        w.setAutoExclusive(False)                 # the model decides which one is on
        w.clicked.connect(lambda _c=False: post("act", (key, None)))
    elif kind == "entry":
        w = QLineEdit()
        w.setMinimumWidth(220)
        w.textEdited.connect(lambda text: post("act", (key, text)))
    elif kind == "image":
        w = QLabel()
        w.setAlignment(Qt.AlignCenter)
        w.setMinimumSize(200, 120)
    elif kind == "hotkey":
        w = HotkeyButton(key, post)
    elif kind == "hint":                     # 1.17.1: a hint on a line of its own keeps a readable line length
        w = HintLabel(cls="note" if key in NOTE_KEYS else "hint")
    elif kind == "plain":
        w = _label(cls="dim", wrap=True)
    elif kind == "big":
        w = _label(cls="big", wrap=True)
    elif kind == "value":
        w = _label()
        w.setStyleSheet("font-weight: 600;")
    else:                                                     # label, entry (shown, not edited)
        w = _label(wrap=True)
    return w, extra


# 1.24 (phase 2): the overview's buttons with a sign of their own (rotate, step on to the next layout/floor)
INDENT_W = 28                       # 1.29.1: options under the one they depend on (about the tick box + gap)
OVERVIEW_GLYPHS = {"rotate": "rotate", "layout": "chevron_right", "floor": "chevron_right", "scan": "search"}


def show_control(kind, w, extra, st):
    """Put a model widget's state (app_qt.ui_state) into its Qt control – never sends anything back."""
    if kind == "tab":                    # a tab of a hand-made page: hidden with its frame (extra = its body widget)
        idx = w.indexOf(extra)
        if idx >= 0 and w.isTabVisible(idx) != bool(st.get("visible", True)):
            w.setTabVisible(idx, bool(st.get("visible", True)))
        return
    if kind == "title":                  # 1.66.3: a card whose model frame is hidden is not shown
        card, shown = w.parentWidget(), bool(st.get("visible", True))
        if card is not None and card.isHidden() == shown:
            card.setVisible(shown)
    else:
        shown = bool(st.get("visible", True))
        if kind in ("hint", "plain", "big", "label"):
            shown = shown and bool(st.get("text"))            # empty lines take no room
        w.setVisible(shown)
    if "enabled" in st:
        w.setEnabled(st["enabled"])
    if st.get("danger") and w.objectName() != "danger":       # 1.12.3: the warning colour (style sheet)
        w.setObjectName("danger")
        w.style().unpolish(w)
        w.style().polish(w)
    if st.get("primary") and w.objectName() != "primary":     # 1.24: the main action (ui.primary)
        w.setObjectName("primary")
        w.style().unpolish(w)
        w.style().polish(w)
    # 1.24.5 (measured): the caches are read from the widget's own __dict__ – getattr() of a name a PySide widget
    # lacks searches Qt's meta data first (3.7 µs, every control on every refresh), a dict lookup costs 0.17 µs
    if "glyph" in st or w.__dict__.get("_glyph_key"):
        set_glyph(w, st.get("glyph"), primary=bool(st.get("primary")))
    if "level" in st and w.__dict__.get("_level", "") != st["level"]:   # 1.24.3: ui.level – state colour
        w._level = st["level"]                            # 1.24.5: compared in Python, not via a Qt property read
        w.setProperty("state", st["level"])
        w.style().unpolish(w)
        w.style().polish(w)
    if st.get("tip") is not None and w.toolTip() != st["tip"]:
        w.setToolTip(st["tip"])
    if kind in ("check", "radio"):
        _set(w, st.get("text", ""))
        if w.isChecked() != bool(st.get("value")):
            w.setChecked(bool(st.get("value")))                 # setChecked does not emit clicked
    elif kind == "entry":
        if not w.hasFocus() and w.text() != st.get("value", ""):     # never overwrite while typing
            w.setText(st.get("value", ""))
        if st.get("placeholder", "") != w.placeholderText():
            w.setPlaceholderText(st.get("placeholder", ""))
        if st.get("secret") and w.echoMode() != QLineEdit.Password:   # 1.4: the OBS password
            w.setEchoMode(QLineEdit.Password)
    elif kind == "image":
        pil = st.get("pil")
        if pil is not getattr(w, "_pil", None):
            w._pil = pil
            if pil is None:
                w.setText(st.get("text", ""))
            else:
                w.setPixmap(pixmap_from_pil(pil, pil.height, w.devicePixelRatioF()))
    elif kind == "combo":
        if w.isEditable() != bool(st.get("editable")):
            w.setEditable(bool(st.get("editable")))
        values = st.get("values", [])
        if [w.itemText(i) for i in range(w.count())] != values:
            w.blockSignals(True)
            w.clear()
            w.addItems(values)
            w.blockSignals(False)
        if w.currentText() != st.get("value") and not (w.isEditable() and w.hasFocus()):
            w.blockSignals(True)
            i = w.findText(st.get("value", ""))
            if i >= 0:
                w.setCurrentIndex(i)
            elif w.isEditable():
                w.setEditText(st.get("value", ""))
            else:
                w.setCurrentIndex(-1)
            w.blockSignals(False)
    elif kind == "slider":
        name, s, value = extra
        _set(name, st.get("label", ""))
        _set(value, st.get("text", ""))
        if not s.isSliderDown():                                  # the user is dragging: no pull back
            s.blockSignals(True)
            s.setRange(round(st.get("lo", 0)), round(st.get("hi", 100)))
            s.setValue(round(st.get("value", 0)))
            s.blockSignals(False)
        s.set_cap(st.get("cap"))
    elif kind in ("table", "chart", "log", "dashboard", "tiles", "preview", "swatches", "host"):
        w.show_state(st)
    elif kind == "hotkey":
        w.show_text(st.get("text", ""))
        w.show_recording(bool(st.get("recording")))
    elif kind in ("box", "card"):
        pass
    else:                                                         # button, label, hint, value, title, big
        text = st.get("text", "")
        _set(w, text.upper() if kind == "title" else text)


class Grip(QWidget):
    """The handle at the right of a card's title: six dots; dragging it moves the card (CardColumn)."""

    def __init__(self, column, card):
        super().__init__()
        self._column, self._card = column, card
        self.setFixedSize(16, 18)
        self.setCursor(Qt.OpenHandCursor)
        self.setToolTip(_("Ziehen, um den Kasten zu verschieben"))
        self._hover = False                       # 1.17: quiet until the pointer is on it

    def enterEvent(self, e):
        self._hover = True
        self.update()

    def leaveEvent(self, e):
        self._hover = False
        self.update()

    def paintEvent(self, _e):
        from PySide6.QtGui import QPainter
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        c = qt_theme.colours(qt_theme.current_dark())       # 1.25: the theme's grip colour (>= 3:1), not Mid (1.3:1)
        p.setBrush(QColor(c["dim"] if self._hover else c["handle"]))
        for x in (5, 11):
            for y in (4, 9, 14):
                p.drawEllipse(x - 1.5, y - 1.5, 3, 3)
        p.end()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
            self._column.begin(self._card)

    def mouseMoveEvent(self, e):
        self._column.drag_to(e.globalPosition().toPoint())

    def mouseReleaseEvent(self, _e):
        self.setCursor(Qt.OpenHandCursor)
        self._column.end()


class CardColumn(QWidget):
    """Cards below each other that the user can put in their own order (1.59, user's wish: "Updates nach oben
    schieben"): drag a card at its grip, the others make room as it passes them; the page scrolls at its edges.
    No QDrag – that runs a second event loop. ``on_order(ids)`` gets the new order (saved by the App)."""

    def __init__(self, on_order=None):
        super().__init__()
        self._lay = QVBoxLayout(self)
        self._lay.setContentsMargins(0, 0, 0, 0)
        self._lay.setSpacing(12)
        self.cards = []                   # [(id, card)] in the order shown
        self._default = []
        self._drag = None
        self._before = None
        self.on_order = on_order
        self._scroll = None
        self._timer = QTimer(self)        # scrolls the page while the card is held at its top/bottom edge
        self._timer.setInterval(30)
        self._timer.timeout.connect(self._autoscroll)

    def add(self, card_id, card, head_row):
        """``head_row``: the card's title layout – the grip goes to its right end."""
        head_row.addWidget(Grip(self, card), 0, Qt.AlignVCenter)
        self.cards.append((card_id, card))
        self._default.append(card_id)
        self._lay.addWidget(card)

    def ids(self) -> list:
        return [i for i, _c in self.cards]

    def apply(self, ids):
        """Show the cards in this order; ids it does not know, or a missing card (another version), = default."""
        if not ids or sorted(ids) != sorted(self._default):
            ids = self._default
        if ids == self.ids():
            return
        by_id = dict(self.cards)
        for _i, card in self.cards:
            self._lay.removeWidget(card)
        self.cards = [(i, by_id[i]) for i in ids]
        for _i, card in self.cards:
            self._lay.addWidget(card)
        self._tab_order()

    def _tab_order(self):
        """Tab order = the order shown (1.62.2): Qt keeps the order the widgets were made in. A button that
        disables itself on click ("Jetzt nach Updates suchen") hands its focus to the next one in that chain –
        a card that now sits far below – and the page scrolled down to it."""
        def focusable(card):
            return [w for w in card.findChildren(QWidget) if w.focusPolicy() & Qt.TabFocus]
        widgets = [w for _i, card in self.cards for w in focusable(card)]
        if len(widgets) < 2:
            return
        inside = set(map(id, widgets))
        by_id = dict(self.cards)
        first = next((w for i in self._default for w in focusable(by_id[i])), None)
        prev = first.previousInFocusChain() if first is not None else None
        while prev is not None and id(prev) in inside:
            prev = prev.previousInFocusChain()
        chain = ([prev] if prev is not None else []) + widgets
        for a, b in zip(chain, chain[1:]):
            QWidget.setTabOrder(a, b)

    def begin(self, card):
        self._drag = card
        self._before = self.ids()
        card.setProperty("dragging", True)
        card.style().unpolish(card)
        card.style().polish(card)
        w = self.parentWidget()
        while w is not None and not isinstance(w, QScrollArea):
            w = w.parentWidget()
        self._scroll = w
        self._timer.start()

    def drag_to(self, global_pos):
        card = self._drag
        if card is None:
            return
        y = self.mapFromGlobal(global_pos).y()
        others = [(i, c) for i, c in self.cards if c is not card]
        pos = len(others)
        for n, (_i, c) in enumerate(others):
            if c.isVisible() and y < c.geometry().center().y():
                pos = n
                break
        me = next(e for e in self.cards if e[1] is card)
        if self.cards.index(me) != pos:
            others.insert(pos, me)
            self.cards = others
            self._lay.removeWidget(card)
            self._lay.insertWidget(pos, card)

    def _autoscroll(self):
        from PySide6.QtGui import QCursor
        sa = self._scroll
        if self._drag is None or sa is None:
            return
        y = sa.viewport().mapFromGlobal(QCursor.pos()).y()
        h = sa.viewport().height()
        step = -18 if y < 40 else 18 if y > h - 40 else 0
        if step:
            bar = sa.verticalScrollBar()
            bar.setValue(bar.value() + step)
            self.drag_to(QCursor.pos())

    def end(self):
        card, self._drag = self._drag, None
        self._timer.stop()
        if card is None:
            return
        card.setProperty("dragging", False)
        card.style().unpolish(card)
        card.style().polish(card)
        if self.ids() != self._before:
            self._tab_order()
            if self.on_order is not None:
                self.on_order(self.ids())


def _card_head(card_layout):
    """Title row of a card: (title label, row) – CardColumn puts its grip at the end of the row."""
    row = QHBoxLayout()
    row.setContentsMargins(0, 0, 0, 0)
    head = _label(cls="h2")
    row.addWidget(head, 1)
    card_layout.addLayout(row)
    return head, row


class _Arranged:
    """Pages whose cards the user can put in order: one CardColumn per run of cards (a run ends at anything
    else, e.g. Settings' "Mehr" button). ``post("card_order", (page, run, ids))`` saves; ``apply_order``."""

    def _column(self, page_key):
        n = len(self.columns)
        col = CardColumn(lambda ids, n=n: self._post("card_order", (page_key, n, ids)))
        self.columns.append(col)
        return col

    def apply_order(self, saved: dict):
        for n, col in enumerate(self.columns):
            col.apply((saved or {}).get(str(n)))

    # ---- 1.7.6 (user: "move the tab rows as I like"): the tabs of a row can be dragged; the order is remembered
    _tabsets = ()                          # [(tabs id, QTabWidget, {tab id: its widget})], set by the page
    _applying = False                      # apply_tab_order is moving tabs: no posts

    @staticmethod
    def _tab_ids(tw, ids: dict) -> list:
        """The tab ids in the order the row shows them now."""
        by_widget = {w: i for i, w in ids.items()}
        return [by_widget.get(tw.widget(k)) for k in range(tw.count())]

    def _movable(self, tabs_id, tw, ids: dict, page_key):
        """Let the user drag the tabs of ``tw``; a move posts ("tab_order", (page, tabs id, [ids]))."""
        self._tabsets = list(self._tabsets) + [(tabs_id, tw, ids)]
        tw.tabBar().setMovable(True)
        # 1.8.46: many tabs (statistics: eleven, 1.8.48 twelve) – less padding, so they fit side by side again
        tw.tabBar().setProperty("dense", len(ids) >= DENSE_TABS)
        if page_key:
            tw.tabBar().tabMoved.connect(lambda *_a, t=tw, i=ids, tid=tabs_id: self._applying or self._post(
                "tab_order", (page_key, tid, self._tab_ids(t, i))))

    def apply_tab_order(self, saved: dict):
        """{tabs id: [ids]} (setting tab_order[page]); none means the built-in order. 1.8.46: a tab the saved order
        does not know yet (a new version's tab) goes to the end and ids no longer there are dropped – the
        user's order stays (before, any such list fell back to the built-in order)."""
        for tabs_id, tw, ids in self._tabsets:
            want = list(dict.fromkeys(str(i) for i in (saved or {}).get(tabs_id, []) if str(i) in ids))
            want += [i for i in ids if i not in want]
            if want == self._tab_ids(tw, ids):
                continue
            # not blockSignals: the QTabWidget moves its pages along only from the bar's tabMoved signal
            self._applying = True
            try:
                for pos, i in enumerate(want):
                    now = self._tab_ids(tw, ids).index(i)
                    if now != pos:
                        tw.tabBar().moveTab(now, pos)
            finally:
                self._applying = False


DENSE_TABS = 11                        # from this many tabs in a row the bar gets less padding (qt_theme)


class HostView(QWidget):
    """1.8.8: holds one widget the App puts in (``set_content``); the old one is closed and deleted."""

    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.content = None

    def set_content(self, w):
        old, self.content = self.content, w
        if old is not None:
            self.box.removeWidget(old)
            old.close()
            old.deleteLater()
        if w is not None:
            self.box.addWidget(w)
            w.show()

    def show_state(self, st):
        pass


SPLIT_FROM = 940                  # px (logical): from this page width a "split" page shows its two columns beside
                                  # 1.24.2 (phase 2): was 1080 – a 1280-px window (page ~1036) had the tabs below the fold


class SideBySide(QWidget):
    """1.8.2: two cards next to each other while the page is wide enough (the overlay preview and the tools of the
    picked element), one below the other on a narrow page. The first card takes the larger share."""

    BESIDE_FROM = 820                 # px (logical): from this width the cards sit side by side

    def __init__(self, beside_from=None, weights=(3, 2)):
        super().__init__()
        if beside_from:
            self.BESIDE_FROM = beside_from
        self.weights = weights               # share of the width: first card, the others
        self.box = QBoxLayout(QBoxLayout.TopToBottom, self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(10)
        self.cards = []

    def add(self, card):
        self.cards.append(card)
        self.box.addWidget(card, self.weights[0] if len(self.cards) == 1 else self.weights[1])

    def beside(self) -> bool:
        return self.box.direction() == QBoxLayout.LeftToRight

    def resizeEvent(self, e):
        self.arrange(self.width())
        super().resizeEvent(e)

    def arrange(self, width: int):
        """Side by side from BESIDE_FROM px on, else below each other (1.11.14: apart from resizeEvent, so a test
        does not depend on the screen size – a Windows runner's screen is smaller than a wide page)."""
        want = QBoxLayout.LeftToRight if width >= self.BESIDE_FROM else QBoxLayout.TopToBottom
        if self.box.direction() != want:
            self.box.setDirection(want)
            for i, card in enumerate(self.cards):       # beside: the short card hangs at the top, not stretched
                self.box.setAlignment(card, Qt.AlignTop if want == QBoxLayout.LeftToRight and i else Qt.Alignment())
            self.updateGeometry()


class FitTabs(QTabWidget):
    """Tabs as tall as the open tab, not the tallest one (QStackedLayout asks every page): no empty room below
    a short tab."""

    def __init__(self):
        super().__init__()
        self.currentChanged.connect(lambda _i: self._fit())

    def addTab(self, page, label):
        page.installEventFilter(self)            # 1.8.8: rows shown/hidden in a tab → its height again
        return super().addTab(page, label)

    def eventFilter(self, obj, e):
        if e.type() == QEvent.LayoutRequest and obj is self.currentWidget():
            QTimer.singleShot(0, self, self._fit)    # 1.11.14: bound to self – dropped once the tabs are deleted
        return False

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._fit()

    def _fit(self):
        """1.8.8: the parent kept the height of the tab shown before (an empty band below a short tab, e.g.
        "Heute") – at most as tall as the open tab needs at this width."""
        h = self.heightForWidth(max(1, self.width()))
        if self.maximumHeight() != h:
            self.setMaximumHeight(h)
        self.updateGeometry()

    def _extra(self):
        return self.tabBar().sizeHint().height() + 2

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, w):
        page = self.currentWidget()
        if page is None:
            return super().heightForWidth(w)
        return self._extra() + (page.heightForWidth(w - 2) if page.hasHeightForWidth() else page.sizeHint().height())

    def sizeHint(self):
        hint = super().sizeHint()
        page = self.currentWidget()
        return hint if page is None else QSize(hint.width(), self._extra() + page.sizeHint().height())

    def minimumSizeHint(self):
        hint = super().minimumSizeHint()
        page = self.currentWidget()
        return hint if page is None else QSize(hint.width(), self._extra() + page.minimumSizeHint().height())


class FormPage(QWidget, _Arranged):
    """A hand-made page (SPECS): one control per widget of the UI model, which does the work."""

    def __init__(self, post, title, spec, page_key=""):
        super().__init__()
        self._post = post
        self._page_key = page_key
        self.controls = {}                 # key -> (kind, widget, extra)
        self.columns = []
        self._tabsets = []
        page, lay = _scroll_page(title, page_key=page_key)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(page)
        self._items(spec, lay, page_key)
        lay.addStretch()

    def _items(self, spec, lay, page_key):
        """The items of a page spec (or of one column of a "split") into ``lay``."""
        col = None
        for item in spec:
            kind = item[0]
            if kind != "card":
                col = None
            if kind == "card":
                if col is None:
                    col = self._column(page_key)
                    lay.addWidget(col)
                card, hrow = self._card_widget(item)
                col.add(item[1], card, hrow)
            elif kind == "panel":
                lay.addWidget(self._panel(item[1]))
            elif kind == "side":
                side = SideBySide()
                for panel in item[1]:
                    side.add(self._panel(panel[1]))
                lay.addWidget(side)
            elif kind == "tabs":
                tabs = FitTabs()
                tabs.setObjectName("formtabs")
                bodies = {}
                for frame, label, rows in item[1]:
                    body = QWidget()
                    body.setObjectName("page")
                    bl = QVBoxLayout(body)
                    if rows and all(r[0] == "card" for r in rows):    # 1.8.90: a tab of cards (the settings page)
                        bl.setContentsMargins(0, 8, 0, 0)             # – the cards bring their own padding
                    else:
                        bl.setContentsMargins(*qt_theme.PAD_CARD)
                    bl.setSpacing(6)
                    self._group = []
                    self._place(rows, bl, page_key)
                    self._align()
                    bl.addStretch()
                    tabs.addTab(body, _(label).replace("&", "&&"))
                    self.controls[frame] = ("tab", tabs, body)
                    bodies[frame] = body
                self._movable(item[1][0][0], tabs, bodies, page_key)     # id = the first tab's frame key
                lay.addWidget(tabs)
            elif kind == "links":
                row = QHBoxLayout()
                for c in item[1]:
                    self._add(c, row)
                row.addStretch()
                lay.addLayout(row)
            elif kind == "split":
                # 1.11.14 (user picked "Vorschau links, Einstellungen rechts"): two columns of items side by side
                # from SPLIT_FROM px on (the overlay page: preview + tools | the tabs), below each other when narrow
                split = SideBySide(SPLIT_FROM, weights=(1, 1))
                split.setObjectName("split")
                for items in item[1:]:
                    w = QWidget()
                    w.setObjectName("page")
                    wl = QVBoxLayout(w)
                    wl.setContentsMargins(0, 0, 0, 0)
                    wl.setSpacing(12)
                    self._items(items, wl, page_key)
                    wl.addStretch()
                    split.add(w)
                lay.addWidget(split)
            else:
                self._add(item, lay)

    def _card_widget(self, item):
        """("card", key, rows) → (card, its head row): a titled card whose title is the "title" control of ``key``
        (shown/hidden with the model's frame)."""
        card = _card()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(*qt_theme.PAD_CARD)
        cl.setSpacing(6)
        head, hrow = _card_head(cl)
        self.controls[item[1]] = ("title", head, None)
        self._group = []
        for row in item[2]:
            self._add(row, cl)
        self._align()
        return card, hrow

    def _place(self, rows, lay, page_key):
        """1.8.90: rows of a tab body – cards standing together go into one draggable column (CardColumn, like on
        the page itself), everything else straight into ``lay``."""
        col = None
        for item in rows:
            if item[0] == "card":
                if col is None:
                    col = self._column(page_key)
                    lay.addWidget(col)
                card, hrow = self._card_widget(item)
                col.add(item[1], card, hrow)
            else:
                col = None
                self._add(item, lay)

    def _panel(self, rows):
        card = _card()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(*qt_theme.PAD_CARD)
        self._group = []
        for row in rows:
            self._add(row, cl)
        self._align()
        return card

    def _align(self):
        """1.8.8: in one card / tab the controls after a row's label start at the same x and choice boxes there
        are equally wide (they were ragged: 'Preset' 140 px next to 'Map style' 300 px, each at its own x)."""
        group, self._group = getattr(self, "_group", []), []
        if len(group) > 1:
            if not hasattr(self, "_groups"):
                self._groups = {}
            self._groups[id(group)] = [group, None]       # aligned once the texts are in (show_states)

    def _align_group(self, entry):
        group, done = entry
        key = tuple((lbl.text(), w.count() if isinstance(w, QComboBox) else 0) for lbl, w in group)
        if key == done:
            return
        entry[1] = key
        labels = [lbl for lbl, _w in group]
        if len(labels) > 1:
            width = min(ALIGN_LABEL_MAX, max(_one_line_width(lbl) for lbl in labels))
            for lbl in labels:
                lbl.setMinimumWidth(width)
        combos = [w for _l, w in group if isinstance(w, QComboBox)]
        if len(combos) > 1:
            width = min(ALIGN_COMBO_MAX, max(c.sizeHint().width() for c in combos))
            for c in combos:
                c.setMinimumWidth(width)

    def _add(self, item, lay):
        kind = item[0]
        if kind == "row":
            kids = item[1]
            if any(c[0] in ("hint", "slider") for c in kids):    # text that wraps beside controls: a plain row
                row = QHBoxLayout()
                row.setSpacing(8)
                for c in kids:
                    self._add(c, row)
            else:                                     # controls only: they wrap when the window is narrow
                row = FlowRow()
                cut = next((i for i, c in enumerate(kids) if c[0] == "stretch"), len(kids))
                row.right = len([c for c in kids[cut:] if c[0] != "stretch"])
                for c in kids:
                    if c[0] != "stretch":
                        self._add(c, row)
            parts = [c for c in kids if c[0] != "stretch"]
            if len(parts) >= 2 and parts[0][0] == "label" and hasattr(self, "_group"):
                self._group.append((self.controls[parts[0][1]][1], self.controls[parts[1][1]][1]))
            lay.addLayout(row)
            return
        if kind == "grid":                          # ("grid", columns, rows): the rows side by side (hotkeys)
            g = QGridLayout()
            g.setHorizontalSpacing(28)
            g.setVerticalSpacing(6)
            cols = item[1]
            per = -(-len(item[2]) // cols)            # down the first column, then the next
            for i, c in enumerate(item[2]):
                box = _GridCell()                     # 1.8.8: GRID_CELL_W wide at most – a hotkey stays by its name
                cell = QVBoxLayout(box)
                cell.setContentsMargins(0, 0, 0, 0)
                self._add(c, cell)
                g.addWidget(box, i % per, i // per)
            g.setColumnStretch(cols, 1)               # the free room goes to the right, not between name and key
            lay.addLayout(g)
            return
        if kind == "stretch":
            lay.addStretch()
            return
        if kind == "sub":                           # a small heading inside a card (1.66.3: groups of tick boxes)
            lay.addWidget(_label(_(item[1]).upper(), "sub"))
            return
        if kind == "indent":                        # 1.29.1: options that only count with the one above them
            box = QWidget()
            box.setProperty("class", "indent")
            il = QVBoxLayout(box)
            il.setContentsMargins(INDENT_W, 0, 0, 0)
            il.setSpacing(6)
            for c in item[1]:
                self._add(c, il)
            lay.addWidget(box)
            return
        if kind == "fold":                          # 1.29.1: a long explanation behind "Erklärung" – shut at first
            btn = QPushButton(_(item[1]))
            btn.setObjectName("fold")
            btn.setFlat(True)
            btn.setCursor(Qt.PointingHandCursor)
            body = QWidget()
            body.setProperty("fold_body", True)
            bl = QVBoxLayout(body)
            bl.setContentsMargins(0, 0, 0, 0)
            bl.setSpacing(4)
            for c in item[2]:
                self._add(c, bl)
            body.hide()

            def flip(_checked=False, b=btn, w=body):
                w.setVisible(not w.isVisibleTo(w.parentWidget()))
                set_glyph(b, "chevron_down" if w.isVisibleTo(w.parentWidget()) else "chevron_right")
            set_glyph(btn, "chevron_right")
            btn.clicked.connect(flip)
            btn._dbdms_fold = body
            row = QHBoxLayout()
            row.addWidget(btn)
            row.addStretch(1)
            lay.addLayout(row)
            lay.addWidget(body)
            return
        if kind == "note":                          # a fixed text of the page itself (setup assistant)
            lay.addWidget(_label(_(item[1]), wrap=True))
            return
        w, extra = make_control(kind, item[1], self._post)
        if isinstance(lay, FlowRow):
            lay.addWidget(w)
        else:
            lay.addWidget(w, 1 if kind == "hint" and isinstance(lay, QHBoxLayout) else 0)  # text beside: takes the room
        self.controls[item[1]] = (kind, w, extra)
        if kind == "slider" and hasattr(self, "_group"):   # 1.8.8: its name lines up with the row labels
            self._group.append((extra[0], extra[1]))

    def show_states(self, states):
        for key, (kind, w, extra) in self.controls.items():
            st = states.get(key)
            if st is not None:
                show_control(kind, w, extra, st)
        for entry in getattr(self, "_groups", {}).values():   # 1.8.8: after the texts are in
            self._align_group(entry)


class _GridCell(QWidget):
    """A cell of a FormPage grid: wants GRID_CELL_W (a wide window does not pull name and key apart), shrinks in a
    narrow one."""

    def __init__(self):
        super().__init__()
        self.setMaximumWidth(GRID_CELL_W)

    def sizeHint(self):
        s = super().sizeHint()
        return QSize(max(s.width(), GRID_CELL_W), s.height())


ALIGN_LABEL_MAX = 220            # 1.8.8: a longer row label does not push the controls of its card further right
ALIGN_COMBO_MAX = 320


def _one_line_width(label) -> int:
    fm = label.fontMetrics()
    return max(fm.horizontalAdvance(t) for t in (label.text() or " ").split("\n")) + 4


GRID_CELL_W = 520                # 1.8.8: a cell of a FormPage grid (hotkeys: name … key) is not wider
HOST_BESIDE_FROM = 1000          # 1.8.8: table + clip preview side by side from this page width

FLOW_KINDS = ("button", "combo", "check", "radio", "label", "entry", "value", "big")   # rows of these may wrap


def _grows(node) -> bool:
    """A table, chart or the log below this node: it may take the free height of the page."""
    return (node.get("kind") in ("table", "chart", "log") and not node.get("fit")) or \
        (node.get("kind") == "host" and bool(node.get("grow"))) or \
        any(_grows(c) for c in node.get("children", ()))


def _fills(node) -> bool:
    """A notebook below this node fills the page (packed with expand): the page does not scroll as a whole."""
    return (node.get("kind") == "tabs" and bool(node.get("fill"))) or any(_fills(c) for c in node.get("children", ()))


class AutoPage(QWidget, _Arranged):
    """A page built from the structure of a tab of the UI model (app_qt.ui_layout): frames → cards/rows,
    notebooks → tabs, tables, charts and controls like FormPage (Statistik, Server, Erkennung, Log, dialogs)."""

    def __init__(self, post, title, node, page_key=""):
        super().__init__()
        self._post = post
        self._page_key = page_key
        self.controls = {}                 # key -> (kind, widget, extra)
        self._tabs = []                    # (key, QTabWidget, [keys of each page], [widget of each page])
        self._tabsets = []
        self._all = []
        self.columns = []
        fill = _fills(node) if node else False
        page, lay = _scroll_page(title, scroll=not fill, page_key=page_key)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(page)
        if node:
            self._build(node, lay, self._all, top=True)
        if not fill:
            lay.addStretch()

    def _build(self, n, lay, keys, top=False, column=None):
        kind, key = n["kind"], n["key"]
        keys.append(key)
        if kind in ("box", "card"):
            holder = _card() if kind == "card" else QWidget()
            v = QVBoxLayout(holder)
            v.setContentsMargins(*((14, 12, 14, 12) if kind == "card" else (0, 0, 0, 0)))
            v.setSpacing(6)
            if kind == "card":
                head, hrow = _card_head(v)
                self.controls[key + "#title"] = ("title", head, None)
            kids = n.get("children", [])
            if n.get("grid"):                         # e.g. the game languages
                g = QGridLayout()
                g.setHorizontalSpacing(14)
                wide = set()
                for c in kids:
                    cell = QVBoxLayout()
                    self._build(c, cell, keys)
                    r, col = c.get("cell", (0, 0))
                    g.addLayout(cell, r, col, 1, int(c.get("span", 1)))
                    if c.get("wide"):                  # 1.8.8: an entry/choice stretched to the right edge
                        wide.add(col)
                        for i in range(cell.count()):
                            w = cell.itemAt(i).widget()
                            if w is not None:
                                w.setSizePolicy(QSizePolicy.Expanding, w.sizePolicy().verticalPolicy())
                                cell.setAlignment(w, Qt.Alignment())     # a choice box sits left otherwise
                for col in wide:
                    g.setColumnStretch(col, 1)
                if not wide:
                    g.setColumnStretch(g.columnCount(), 1)
                v.addLayout(g)
                if column is not None:
                    column[0].add(column[1], holder, hrow)
                else:
                    lay.addWidget(holder, 1 if top and _grows(n) else 0)
                self.controls[key] = (kind, holder, None)
                return
            if n.get("row") and any(c["kind"] == "host" for c in kids):
                # 1.8.8: a table with a host beside it (recordings + clip preview): side by side on a wide page,
                # below each other on a narrow one; the host is hidden until the App fills it
                sb = SideBySide(HOST_BESIDE_FROM)
                for c in kids:
                    if c["kind"] == "host":
                        hw, _x = make_control("host", c["key"], self._post)
                        self.controls[c["key"]] = ("host", hw, None)
                        keys.append(c["key"])
                        sb.add(hw)
                        continue
                    wrap = QWidget()
                    wl = QVBoxLayout(wrap)
                    wl.setContentsMargins(0, 0, 0, 0)
                    self._build(c, wl, keys, top=True)
                    sb.add(wrap)
                v.addWidget(sb, 1)
                lay.addWidget(holder, 1 if top else 0)
                self.controls[key] = (kind, holder, None)
                return
            first = [c for c in kids if c.get("side") != "right"]
            last = list(reversed([c for c in kids if c.get("side") == "right"]))
            flow = n.get("row") and all(c["kind"] in FLOW_KINDS for c in kids)   # controls only: they wrap
            inner = (FlowRow() if flow else QHBoxLayout()) if n.get("row") else v
            if inner is not v:
                inner.setSpacing(8)
                v.addLayout(inner)
                if flow:
                    inner.right = len(last)
            arrange = bool(self._page_key) and top and kind == "box" and inner is v and not _grows(n)  # own order
            col, run = None, 0
            for c in first:
                if arrange and c["kind"] == "card":
                    if col is None:
                        col, run = self._column(self._page_key), 0
                        v.addWidget(col)
                    self._build(c, v, keys, column=(col, f"#{run}"))
                    run += 1
                    continue
                col = None
                self._build(c, inner, keys, top=top and inner is v)    # a table further down still gets the height
            if n.get("row") and not flow:
                inner.addStretch()
            for c in last:
                self._build(c, inner, keys, top=top and inner is v)
            if inner is v and top and _grows(n):
                v.addStretch()     # 1.11.14: the growing child hidden (empty statistics) – the rest stays on top
            if column is not None:
                column[0].add(column[1], holder, hrow)
            else:
                lay.addWidget(holder, 1 if top and _grows(n) else 0)
            self.controls[key] = (kind, holder, None)
            return
        if kind == "tabs":
            tw = QTabWidget()
            if n.get("segments"):                      # 1.11.14: groups as a segment switch (statistics)
                tw.setObjectName("segments")
                tw.tabBar().setObjectName("segbar")
                tw.tabBar().setDrawBase(False)
            fill = bool(n.get("fill"))
            pages = []
            ids = {}                                   # model tab index (str) -> the tab's widget
            for j, c in enumerate(n.get("children", [])):
                pw = QWidget()
                pl = QVBoxLayout(pw)
                pl.setContentsMargins(*((0, 0, 0, 0) if n.get("segments") else (8, 8, 8, 8)))   # segments: no frame
                ks = []
                self._build(c, pl, ks, top=fill)       # filling tabs: a table takes the height of its page
                pl.addStretch()
                if fill:                               # each page scrolls on its own, the filters stay on top
                    pw.setObjectName("page")
                    sa = QScrollArea()
                    sa.setWidgetResizable(True)
                    sa.setFrameShape(QFrame.NoFrame)
                    steady_scroll(sa)
                    sa.setWidget(pw)
                    tw.addTab(sa, "")
                    ids[str(j)] = sa
                else:
                    tw.addTab(pw, "")
                    ids[str(j)] = pw
                # 1.8.82: every tab is a search hit by its name (like the hand-made pages' tabs) – the statistics'
                # groups and parts; going there opens the tab, the App's model follows through currentChanged
                self.controls[f"{key}#tab{j}"] = ("tab", tw, ids[str(j)])
                pages.append(ks)
                keys.extend(ks)
            by_widget = {w: int(i) for i, w in ids.items()}
            tw.currentChanged.connect(lambda i, k=key, t=tw, b=by_widget: self._post("act", (k, b.get(t.widget(i), i))))
            self._movable(key, tw, ids, self._page_key)
            lay.addWidget(tw, 1 if fill else 0)
            self._tabs.append((key, tw, pages, [ids[str(j)] for j in range(len(pages))]))
            self.controls[key] = ("tabs", tw, None)
            return
        w, extra = make_control(kind, key, self._post)
        if n.get("note"):                                 # 1.23: a warning line of the model ("Note.TLabel")
            w.setProperty("class", "note")
        if kind == "table" and n.get("fit"):
            w.fit_rows()
        grow = kind in ("table", "chart", "log") or (kind == "hint" and isinstance(lay, QHBoxLayout)) or \
            (kind == "host" and bool(n.get("grow")))
        if isinstance(lay, FlowRow):
            lay.addWidget(w)
        elif kind in ("button", "combo") and not isinstance(lay, QHBoxLayout):
            lay.addWidget(w, 0, Qt.AlignLeft)             # a button on a line of its own keeps its size
        else:
            lay.addWidget(w, 1 if grow else 0)
        self.controls[key] = (kind, w, extra)

    def visible_keys(self) -> set:
        """Keys to read now: everything except the pages of tabs that are not on display. 1.8.70: by the page's
        widget – after a tab was dragged (tab_order) the position in the row is not the model's index; comparing them
        left the tab on display out, its content came only with the next page switch."""
        hidden = set()
        for _key, tw, pages, widgets in self._tabs:
            shown = tw.currentWidget()
            for ks, w in zip(pages, widgets):
                if w is not shown:
                    hidden.update(ks)
        return set(self._all) - hidden

    def show_states(self, states):
        for key, (kind, w, extra) in self.controls.items():
            if kind == "tabs":
                st = states.get(key)
                if st:
                    tw = w
                    ids = next((i for tid, t, i in self._tabsets if t is tw), {})
                    order = self._tab_ids(tw, ids)                   # 1.7.6: model index per shown position
                    texts = [t.replace("&", "&&") for t in st.get("tabs", [])]   # 1.8.76: "&" is no mnemonic
                    for qi in range(tw.count()):
                        mi = int(order[qi]) if qi < len(order) and order[qi] is not None else qi
                        if mi < len(texts) and tw.tabText(qi) != texts[mi]:
                            tw.setTabText(qi, texts[mi])
                    want = str(st.get("index", 0))
                    qi = order.index(want) if want in order else st.get("index", 0)
                    if tw.currentIndex() != qi:
                        tw.blockSignals(True)
                        tw.setCurrentIndex(qi)
                        tw.blockSignals(False)
                    if "visible" in st and tw.isHidden() == bool(st["visible"]):    # 1.11.14: hidden notebooks
                        tw.setVisible(bool(st["visible"]))
                continue
            if key.endswith("#title"):
                st = states.get(key[:-6])
                if st is not None:
                    show_control("title", w, extra, st)
                continue
            st = states.get(key)
            if st is not None:
                show_control(kind, w, extra, st)


class DialogWindow(QDialog):
    """A dialog of the UI model (Zuordnen, Kartenbild hinzufügen): built like AutoPage, not modal; closing it
    (X, Esc) destroys the model's dialog too."""

    def __init__(self, parent, post, key, title, node):
        super().__init__(parent)
        self._post, self._key = post, key
        self.closing_from_app = False
        self.setWindowTitle(title)
        self.setModal(False)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self.page = AutoPage(post, title, node)
        lay.addWidget(self.page)
        # 1.8.8: as tall as its content (the "Zuordnen" dialog was mostly empty at a fixed 560 px); 1.8.91: the content's
        # own size up to the screen (the export dialog is 750 px tall – capped at 560 it needed a scrollbar), wider too
        self._fit()
        QTimer.singleShot(0, self._fit)           # once laid out (wrapped labels report their real height then)

    def _fit(self):
        """Size the window to its content, up to the screen; it only grows (the content scrolls anyway)."""
        area = self.page.findChild(QScrollArea)
        body = area.widget() if area is not None and area.widget() is not None else self.page
        lay = body.layout()
        hint = lay.sizeHint() if lay is not None else body.sizeHint()
        screen = QGuiApplication.primaryScreen()
        avail = screen.availableGeometry() if screen is not None else None
        max_w, max_h = (avail.width() - 80, avail.height() - 80) if avail is not None else (1000, 900)
        w = max(self.width(), 640, min(max_w, hint.width() + 48))
        h = max(self.height() if self.isVisible() else 0, 220, min(max_h, hint.height() + 72))
        if (w, h) != (self.width(), self.height()):
            self.resize(w, h)

    def done(self, r):                            # Esc / X: the model's dialog goes too
        if not self.closing_from_app:
            self._post("dlg_close", self._key)
        super().done(r)


class MessageBox(QDialog):
    """1.8.44: a note, an error or an OK/Cancel question (App._ask/_inform) as a small window of its own that has
    to be answered (user: instead of the bar at the top of the window). Application-modal, but opened with show(),
    never exec(): no second message loop, the timers keep running. OK -> post("answer", True); Cancel, Esc and X
    -> post("answer", False) (a note has nothing to run, so that is its OK too)."""

    WIDTH = 460

    def __init__(self, parent, post):
        super().__init__(parent)
        self._post = post
        self._open = False                        # shown and not answered yet
        self.setObjectName("message")
        self.setWindowTitle("Fog Scout")
        self.setWindowModality(Qt.ApplicationModal)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(22, 18, 22, 16)
        lay.setSpacing(10)
        self.heading = _label(cls="big", wrap=True)
        self.heading.setTextFormat(Qt.PlainText)
        self.text = _label(wrap=True)
        self.text.setTextFormat(Qt.PlainText)
        self.text.setTextInteractionFlags(Qt.TextSelectableByMouse)      # an error can be copied
        lay.addWidget(self.heading)
        lay.addWidget(self.text)
        row = QHBoxLayout()
        row.addStretch(1)
        self.ok = QPushButton(_("OK"))
        self.ok.setObjectName("primary")
        self.ok.setDefault(True)
        self.ok.clicked.connect(lambda: self._answer(True))
        self.cancel = QPushButton(_("Abbrechen"))
        self.cancel.clicked.connect(lambda: self._answer(False))
        row.addWidget(self.ok)
        row.addWidget(self.cancel)
        lay.addSpacing(6)
        lay.addLayout(row)
        self.setFixedWidth(self.WIDTH)

    def ask(self, title: str, text: str, ask: bool, activate: bool = True, ok_text: str | None = None,
            danger: bool = False):
        """Show it; ``activate`` False = without taking the focus (DBD in front). 1.23 (audit, prompt.md): the
        button says what it does (``ok_text``), and a question that deletes or replaces data (``danger``) has a red
        button and Cancel as its default – Enter and the focus keep the data."""
        self.heading.setText(title)
        self.text.setText(text)
        self.cancel.setVisible(ask)
        risky = bool(danger and ask)
        self.ok.setText(ok_text or _("OK"))
        name = "danger" if risky else "primary"
        if self.ok.objectName() != name:
            self.ok.setObjectName(name)
            self.ok.style().unpolish(self.ok)
            self.ok.style().polish(self.ok)
        self.ok.setDefault(not risky)
        self.cancel.setDefault(risky)
        # 1.23.1 (CI Windows): unactivated (DBD in front) the focus may stay on the red button – a focused
        # autoDefault button takes Enter; without autoDefault Enter goes to the default, Cancel
        self.ok.setAutoDefault(not risky)
        self._open = True
        self.setAttribute(Qt.WA_ShowWithoutActivating, not activate)
        self.adjustSize()
        # 1.29 (offscreen screenshot of the quality steps): adjustSize took the wrapped text's height for a wider
        # line than WIDTH leaves it – the last line of a long text was cut off; the layout's height for the width
        lay = self.layout()
        lay.activate()
        self.resize(self.WIDTH, max(self.height(), lay.totalHeightForWidth(self.WIDTH)))
        self.show()
        self.raise_()
        (self.cancel if risky else self.ok).setFocus()   # 1.23.1: also unactivated – Enter later = this button
        if activate:
            self.activateWindow()

    def withdraw(self):
        """The program took the question back: closed without an answer."""
        self._open = False
        self.hide()

    def _answer(self, ok: bool):
        if self._open:
            self._open = False
            self._post("answer", ok)
        self.hide()

    def done(self, r):                            # Esc / X
        if self._open:
            self._open = False
            self._post("answer", False)
        super().done(r)


class SetupPage(QWidget):
    """The setup assistant (first start, or "Einrichtung starten" in the settings): SETUP's steps one at a time,
    "Zurück" / "Weiter" / "Fertig" and "Überspringen". Done or skipped: post("setup_done")."""

    def __init__(self, post):
        super().__init__()
        self.setObjectName("page")
        self._post = post
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self.steps = QStackedWidget()
        self.pages = [FormPage(post, _("Einrichtung: {step}", step=_(title)), items) for title, items in SETUP]
        for page in self.pages:
            page.setMaximumWidth(SETUP_W)               # a wide window: the keys stay next to their names
            self.steps.addWidget(page)
        lay.addWidget(self.steps, 1)
        foot = QHBoxLayout()
        foot.setContentsMargins(22, 10, 22, 16)
        self.skip = QPushButton(_("Überspringen"))
        self.skip.clicked.connect(lambda: self._post("setup_done"))
        self.where = _label(cls="dim")
        self.back = QPushButton(_("Zurück"))
        self.back.clicked.connect(lambda: self.go(self.steps.currentIndex() - 1))
        self.next = QPushButton()
        self.next.setObjectName("primary")
        self.next.clicked.connect(self._next)
        foot.addWidget(self.skip)
        foot.addStretch()
        foot.addWidget(self.where)
        foot.addSpacing(12)
        foot.addWidget(self.back)
        foot.addSpacing(8)                                # 1.8.8: the two did touch
        foot.addWidget(self.next)
        lay.addLayout(foot)
        self.go(0)

    def go(self, i: int):
        i = max(0, min(len(self.pages) - 1, i))
        self.steps.setCurrentIndex(i)
        _set(self.where, _("Schritt {n} von {total}", n=i + 1, total=len(self.pages)))
        self.back.setEnabled(i > 0)
        _set(self.next, _("Fertig") if i == len(self.pages) - 1 else _("Weiter"))

    def _next(self):
        if self.steps.currentIndex() == len(self.pages) - 1:
            self._post("setup_done")
        else:
            self.go(self.steps.currentIndex() + 1)

    def show_states(self, states):
        for page in self.pages:
            page.show_states(states)
