"""1.26: the command palette – Ctrl+F or a click in the navigation's search field darkens the window and opens a
card in its middle: a field and the suggestions for what is typed (palette.rank), grouped by kind. Enter runs a
row, Ctrl+Enter its second action (a map in the game, a round's recording), Esc or a click on the dark area closes.
With Claude switched on (askclaude, setting claude_on) a last row asks Claude; its answer shows above the rows it
suggests. Everything the user picks goes to the App as ("palette_pick", (entry id, alt)); nothing here runs an
action itself."""
from __future__ import annotations

from PySide6.QtCore import QEasingCurve, QEvent, QPropertyAnimation, QRect, QSize, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsOpacityEffect, QLineEdit, QListWidget, QListWidgetItem,
                               QStyle, QStyledItemDelegate, QVBoxLayout, QWidget)

from . import palette, qt_theme
from .i18n import N_, _
from .qt_common import PlainLabel, _label

DIM = {True: 170, False: 110}          # alpha of the black over the window (dark, light)
CARD_W = (420, 640)                    # the card's width: between these, 80 % of the window
CARD_TOP = 0.14                        # the card's top as a share of the window's height
ROW_H, HEAD_H = 44, 26
FADE_MS = 120
GROUP_TITLES = {"action": N_("Aktionen"), "page": N_("Seiten"), "setting": N_("Einstellungen"),
                "map": N_("Maps"), "round": N_("Runden"), "claude": N_("Vorschlag von Claude")}
ROLE = Qt.UserRole + 1                 # an item's ("head", title) / ("entry", Entry) / ("ask", question)


class _Rows(QStyledItemDelegate):
    """Group heads in small capitals; entries with the title, a dim line below and the key on the right."""

    def sizeHint(self, opt, index):
        kind = (index.data(ROLE) or ("entry",))[0]
        return QSize(opt.rect.width(), HEAD_H if kind == "head" else ROW_H)

    def paint(self, p, opt, index):
        kind, value = index.data(ROLE) or ("entry", None)
        c = qt_theme.colours(qt_theme.current_dark())
        r = opt.rect
        p.save()
        if kind == "head":
            f = opt.font
            f.setBold(True)
            f.setPointSizeF(max(7.0, f.pointSizeF() * 0.85))
            p.setFont(f)
            p.setPen(QColor(c["dim"]))
            p.drawText(r.adjusted(14, 0, -14, 0), Qt.AlignLeft | Qt.AlignBottom, str(value).upper())
            p.restore()
            return
        selected = bool(opt.state & QStyle.State_Selected)
        if selected:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(c["sel_bg"]))
            p.drawRoundedRect(r.adjusted(6, 2, -6, -2), qt_theme.RADIUS["m"], qt_theme.RADIUS["m"])
        fm = p.fontMetrics()
        key = ""
        if kind == "ask":
            title, sub = _("Claude fragen: „{q}“", q=value), _("Schickt nur die Frage und die Namen der "
                                                                 "Einstellungen an Claude")
            key = _("Enter")
        else:
            title, sub = value.title, value.sub
            if selected:
                key = _("Enter") + (" · " + _("Strg+Enter") if value.alt else "")
        right = fm.horizontalAdvance(key) + 16 if key else 0
        text = r.adjusted(16, 4, -(14 + right), -4)
        p.setPen(QColor(c["fg"]))
        top = QRect(text.x(), text.y(), text.width(), text.height() // 2 + 2) if sub else text   # no sub: centred
        p.drawText(top, Qt.AlignLeft | Qt.AlignVCenter, fm.elidedText(title, Qt.ElideRight, text.width()))
        if sub:
            p.setPen(QColor(c["dim"]))
            p.drawText(QRect(text.x(), text.y() + text.height() // 2, text.width(), text.height() // 2),
                       Qt.AlignLeft | Qt.AlignVCenter, fm.elidedText(sub, Qt.ElideRight, text.width()))
        if key:
            p.drawText(r.adjusted(0, 0, -16, 0), Qt.AlignRight | Qt.AlignVCenter, key)
        p.restore()


class CommandPalette(QWidget):
    """A child of the main window over its whole content. ``post(action, arg)`` = the window's post."""

    def __init__(self, parent, post):
        super().__init__(parent)
        self._post = post
        self.setObjectName("palette")
        self._entries, self._recent, self._claude = [], [], False
        self._answer_ids = None                  # Claude's suggestion shown instead of the ranking
        self._return_to = None                   # 1.28 (audit F14): the widget that had the focus before opening
        self.setAccessibleName(_("Befehlspalette"))
        self.card = QFrame(self)
        self.card.setProperty("class", "card")
        self.card.setObjectName("palettecard")
        lay = QVBoxLayout(self.card)
        lay.setContentsMargins(*qt_theme.PAD_CARD)
        lay.setSpacing(8)
        self.field = QLineEdit()
        self.field.setObjectName("palettefield")
        self.field.setPlaceholderText(_("Suchen: Einstellung, Seite, Map, Aktion, Runde …"))
        self.field.setClearButtonEnabled(True)
        self.field.textChanged.connect(self._typed)
        self.field.installEventFilter(self)
        self.field.setAccessibleName(_("Suchen"))
        self.card.setAccessibleName(_("Befehlspalette"))
        lay.addWidget(self.field)
        self.answer = PlainLabel("")             # 1.28: Claude's answer – plain text, long runs broken
        self.answer.setObjectName("paletteanswer")
        self.answer.hide()
        lay.addWidget(self.answer)
        self.rows = QListWidget()
        self.rows.setObjectName("paletterows")
        self.rows.setItemDelegate(_Rows(self.rows))
        self.rows.setFocusPolicy(Qt.NoFocus)                    # the field keeps the keyboard
        self.rows.setUniformItemSizes(False)
        self.rows.setAccessibleName(_("Vorschläge"))
        self.rows.itemClicked.connect(lambda it: self._run(it, alt=False))
        lay.addWidget(self.rows, 1)
        self.empty = _label(_("Nichts gefunden"), "dim")
        self.empty.hide()
        lay.addWidget(self.empty)
        self.hint = _label(_("Pfeiltasten wählen · Enter öffnen · Strg+Enter im Spiel bzw. die Aufnahme · Esc schliesst"),
                           "dim")
        lay.addWidget(self.hint)
        self._fade = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._fade)
        self._anim = QPropertyAnimation(self._fade, b"opacity", self)
        self._anim.setDuration(FADE_MS)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        parent.installEventFilter(self)
        self.hide()

    # ------------------------------------------------------------------ open / close
    def open(self, entries, recent=(), claude=False, text="", return_to=None):
        """Show the palette with ``entries`` (palette.Entry, prepared here once). ``return_to``: the widget that
        gets the focus back when the palette closes without a pick (default: the one focused now)."""
        if return_to is None:
            here = QApplication.focusWidget()
            return_to = None if here is not None and self.isAncestorOf(here) else here
        self._return_to = return_to
        self._entries = [e.prepare() for e in entries]
        self._recent, self._claude = list(recent or ()), bool(claude)
        self._answer_ids = None
        self.answer.hide()
        self.field.blockSignals(True)
        self.field.setText(text)
        self.field.blockSignals(False)
        self._fill()
        self.show()
        self._fit()
        self.raise_()
        self._fade.setOpacity(0.0)
        self._anim.stop()
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()
        self.field.setFocus(Qt.ShortcutFocusReason)
        self.field.selectAll()

    def update_entries(self, entries):
        """New entries while open (the settings came once the pages were filled) – the ranking again."""
        self._entries = [e.prepare() for e in entries]
        if self.isVisible():
            self._fill()

    def close_palette(self):
        """Esc or a click beside the card: closed, the focus back where it was (1.28, audit F14)."""
        if self.isVisible():
            self.hide()
            self._give_focus_back()
            self._post("palette_closed")

    def _give_focus_back(self):
        w, self._return_to = self._return_to, None
        try:
            if w is not None and w.isVisible() and w.isEnabled() and w.window() is self.window():
                w.setFocus(Qt.OtherFocusReason)
        except RuntimeError:                          # the widget is gone meanwhile
            pass

    # ------------------------------------------------------------------ Claude
    def show_answer(self, text: str, ids):
        """Claude's sentence and the rows it suggests (ids of entries shown here)."""
        self._answer_ids = list(ids)
        self.answer.setText(text or _("Claude hat nichts Passendes gefunden."))
        self.answer.setProperty("state", "")
        self.answer.show()
        self._fill()

    def show_error(self, text: str):
        self.answer.setText(text)
        self.answer.setProperty("state", "err")
        self.answer.style().unpolish(self.answer)
        self.answer.style().polish(self.answer)
        self.answer.show()
        self._fit()

    def show_waiting(self):
        self.answer.setText(_("Claude denkt nach …"))
        self.answer.setProperty("state", "")
        self.answer.style().unpolish(self.answer)
        self.answer.style().polish(self.answer)
        self.answer.show()
        self._fit()

    # ------------------------------------------------------------------ list
    def _typed(self, _text):
        self._answer_ids = None
        self.answer.hide()
        self._fill()

    def _fill(self):
        query = self.field.text()
        if self._answer_ids is not None:
            by_id = {e.id: e for e in self._entries}
            hits = [by_id[i] for i in self._answer_ids if i in by_id]
            groups = [("claude", hits)] if hits else []
        else:
            hits = palette.rank(query, self._entries, self._recent)
            groups = []
            for e in hits:
                if groups and groups[-1][0] == e.kind:
                    groups[-1][1].append(e)
                else:
                    groups.append((e.kind, [e]))
        self.rows.clear()
        first = None
        for kind, items in groups:
            head = QListWidgetItem()
            head.setData(ROLE, ("head", _(GROUP_TITLES.get(kind, kind))))
            head.setData(Qt.DisplayRole, _(GROUP_TITLES.get(kind, kind)))
            head.setFlags(Qt.NoItemFlags)
            self.rows.addItem(head)
            for e in items:
                it = QListWidgetItem()
                it.setData(ROLE, ("entry", e))
                words = e.title + (" · " + e.sub if e.sub else "")
                it.setData(Qt.DisplayRole, words)           # 1.28: what a screen reader reads (the delegate paints)
                it.setData(Qt.AccessibleTextRole, words)
                it.setToolTip(words)
                self.rows.addItem(it)
                first = first or it
        ask = self._claude and len(query.strip()) >= 3 and self._answer_ids is None
        if ask:
            it = QListWidgetItem()
            it.setData(ROLE, ("ask", query.strip()))
            words = _("Claude fragen: „{q}“", q=query.strip())
            it.setData(Qt.DisplayRole, words)
            it.setData(Qt.AccessibleTextRole, words)
            self.rows.addItem(it)
            first = first or it
        if first is not None:
            self.rows.setCurrentItem(first)
        self.empty.setVisible(first is None and bool(query.strip()))
        self.rows.setVisible(first is not None)
        if self.isVisible():
            self._fit()                               # the card as tall as its rows

    def _selectable(self):
        return [self.rows.item(i) for i in range(self.rows.count())
                if self.rows.item(i).flags() & Qt.ItemIsSelectable]

    def _move(self, step: int):
        items = self._selectable()
        if not items:
            return
        cur = self.rows.currentItem()
        n = items.index(cur) if cur in items else -1
        n = max(0, min(len(items) - 1, n + step))
        self.rows.setCurrentItem(items[n])
        self.rows.scrollToItem(items[n])

    def _run(self, item, alt: bool):
        if item is None or not item.flags() & Qt.ItemIsSelectable:
            return
        kind, value = item.data(ROLE)
        if kind == "ask":
            self._post("palette_ask", value)
            self.show_waiting()
            return
        self._recent = palette.remember(self._recent, value.id)
        self._return_to = None                        # a pick: the place it opens takes the focus
        self.hide()
        self._post("palette_pick", (value.id, bool(alt and value.alt)))

    # ------------------------------------------------------------------ keys, mouse, size
    def eventFilter(self, obj, e):
        if obj is self.parent() and e.type() == QEvent.Resize and self.isVisible():
            self._fit()
        elif obj is self.field and e.type() == QEvent.KeyPress:
            key = e.key()
            if key == Qt.Key_Escape:
                self.close_palette()
                return True
            if key in (Qt.Key_Down, Qt.Key_Up):
                self._move(1 if key == Qt.Key_Down else -1)
                return True
            if key in (Qt.Key_PageDown, Qt.Key_PageUp):
                self._move(5 if key == Qt.Key_PageDown else -5)
                return True
            if key == Qt.Key_Backtab:                 # 1.28: Shift+Tab stays in the field (focus behind the dark)
                return True
            if key == Qt.Key_Tab:
                items = self._selectable()
                if items and items[-1].data(ROLE)[0] == "ask":
                    self.rows.setCurrentItem(items[-1])
                return True
            if key in (Qt.Key_Return, Qt.Key_Enter):
                self._run(self.rows.currentItem(), alt=bool(e.modifiers() & Qt.ControlModifier))
                return True
        return super().eventFilter(obj, e)

    def mousePressEvent(self, e):
        if not self.card.geometry().contains(e.position().toPoint()):
            self.close_palette()
            return
        super().mousePressEvent(e)

    def _fit(self):
        """Over the whole parent; the card centred, as tall as its rows (scrolling once they need more room)."""
        par = self.parent()
        self.setGeometry(0, 0, par.width(), par.height())
        w = min(max(CARD_W[0], min(CARD_W[1], int(par.width() * 0.8))), par.width() - 32)
        top = int(par.height() * CARD_TOP)
        room = max(160, min(int(par.height() * 0.72), par.height() - top - 16))
        lay = self.card.layout()
        shown = self.rows.isVisibleTo(self.card)
        rows_h = sum(self.rows.sizeHintForRow(i) for i in range(self.rows.count())) + 2 * self.rows.frameWidth() + 4
        self.rows.setFixedHeight(rows_h)
        self.card.setFixedWidth(w)
        lay.invalidate()
        other = lay.sizeHint().height() - (rows_h if shown else 0)       # field, answer, hint and margins
        if shown:
            self.rows.setFixedHeight(max(ROW_H, min(rows_h, room - other)))
        lay.invalidate()
        self.card.setGeometry((par.width() - w) // 2, top, w, min(room, lay.sizeHint().height()))

    def paintEvent(self, _e):
        p = QPainter(self)
        p.fillRect(self.rect(), QColor(0, 0, 0, DIM[qt_theme.current_dark()]))
        p.end()

