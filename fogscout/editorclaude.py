"""1.27 (user: Claude in the clip editor, "Befehle in Worten"): the editor's section „Mit Claude bearbeiten“ –
mixed into qt_editor.EditorWindow.

The user writes what should happen („erste 10 s weg, ab 0:40 doppelt so schnell, als Short“); a thread sends the
wish and the edit as numbers (editcommands.content – no picture, no path, no map, no killer) to Claude
(askclaude.request); the answer comes back over the bridge, ``editcommands.apply`` turns it into a checked copy of
the state, the section lists what would happen and what was skipped. „Übernehmen“ shows it as one undo step,
„Verwerfen“ forgets it. A proposal made for an older state of the cut is not applied (the user changed the cut
meanwhile). The key and the user's permission come from the App (``claude_key``: a callable, "" = off)."""
from __future__ import annotations

import logging
import threading

from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton

from . import askclaude, editcommands, sequence
from .i18n import N_, _
from .qt_common import PlainLabel

log = logging.getLogger(__name__)

ERROR_WORDS = {"auth": N_("Claude: Der API-Key wird nicht angenommen – unter Einstellungen › Verbindungen prüfen "
                       "(„API-Key holen“ öffnet die Anthropic Console)."),
               "rate": N_("Claude: Zu viele Anfragen – gleich noch einmal versuchen."),
               "quota": N_("Claude: Kein Guthaben mehr auf dem API-Konto – Einstellungen › Verbindungen › "
                        "„Guthaben aufladen“."),
               "refused": N_("Claude hat die Frage abgelehnt."),
               "bad": N_("Claude hat unverständlich geantwortet."),
               "net": N_("Claude ist nicht erreichbar – keine Internetverbindung?")}


class ClaudeMixin:
    def _claude_init(self):
        self.claude_key = lambda: ""         # set by the App: the key while the user allows Claude in the editor
        self._claude_seq = 0                 # number of the last wish sent (older answers are dropped)
        self._claude_base = None             # the state the shown proposal was made for
        self._claude_result = None           # (new state, new mode or None)
        self._claude_busy = False            # 1.28 (audit F3): a wish is on its way – no second (paid) request

    # ---- the inspector section
    def _section_claude(self, sec, mode):
        self.bridge.claude.connect(self._claude_answer)
        self.cl_field = QLineEdit()
        self.cl_field.setPlaceholderText(_("z. B. erste 10 s weg, ab 0:40 doppelt so schnell, als Short"))
        self.cl_field.setMaxLength(editcommands.MAX_REQUEST)
        self.cl_field.returnPressed.connect(self.claude_ask)
        sec.body.addWidget(self.cl_field)
        row = QHBoxLayout()
        row.setSpacing(6)
        self.cl_ask_btn = QPushButton(_("Vorschlagen"))
        self.cl_ask_btn.setToolTip(_("Schickt deine Bitte und den Schnitt als Zahlen (Zeiten, Tempo, Blenden – kein "
                                     "Bild, kein Dateiname) an Claude; nichts wird geändert, bevor du übernimmst."))
        self.cl_ask_btn.clicked.connect(self.claude_ask)
        row.addWidget(self.cl_ask_btn)
        row.addStretch()
        sec.body.addLayout(row)
        self.cl_status = PlainLabel("", "dim")             # 1.28: Claude's summary – plain text, long runs broken
        sec.body.addWidget(self.cl_status)
        self.cl_list = PlainLabel("")                      # … and the steps (a short title comes from Claude)
        self.cl_list.hide()
        sec.body.addWidget(self.cl_list)
        row2 = QHBoxLayout()
        row2.setSpacing(6)
        self.cl_take_btn = QPushButton(_("Übernehmen"))
        self.cl_take_btn.setObjectName("primary")
        self.cl_take_btn.setToolTip(_("Führt die vorgeschlagenen Schritte aus – ein Schritt zum Rückgängigmachen (Strg+Z)."))
        self.cl_take_btn.clicked.connect(self.claude_take)
        self.cl_drop_btn = QPushButton(_("Verwerfen"))
        self.cl_drop_btn.setToolTip(_("Vergisst den Vorschlag; der Schnitt bleibt, wie er ist."))
        self.cl_drop_btn.clicked.connect(self.claude_drop)
        row2.addWidget(self.cl_take_btn)
        row2.addWidget(self.cl_drop_btn)
        row2.addStretch()
        sec.body.addLayout(row2)
        self._claude_buttons(False)
        self._claude_refresh()

    def _claude_buttons(self, shown: bool):
        for b in (self.cl_take_btn, self.cl_drop_btn):
            b.setVisible(shown)

    def _claude_refresh(self):
        """Field and button follow the permission (the App may switch it while the window is open)."""
        if getattr(self, "cl_field", None) is None:
            return
        on = bool(self.claude_key())
        self.cl_field.setEnabled(on)
        self.cl_ask_btn.setEnabled(on and self.history is not None and not self._claude_busy)
        if not on and self._claude_result is None:
            self.cl_status.setText(_("Aus – in Einstellungen › Verbindungen › Claude „Im Clip-Editor Claude "
                                     "nutzen“ einschalten und einen API-Key eintragen."))
            self._claude_off_shown = True
        elif on and getattr(self, "_claude_off_shown", False):
            self._claude_off_shown = False
            self.cl_status.setText("")

    # ---- asking
    def _claude_marks(self) -> list:
        out = []
        for src, m in self._mark_rows():
            out += sequence.occurrences(self.parts, m, src if getattr(self, "_montage", False) else None)
        return out

    def claude_ask(self):
        if self._claude_busy:                            # 1.28: Enter again while waiting – nothing is sent
            return
        key = self.claude_key()
        wish = self.cl_field.text().strip()
        if not key or not wish or self.history is None:
            self._claude_refresh()
            return
        self._claude_seq += 1
        seq = self._claude_seq
        base = self._state()
        mode = str(self.mode_box.currentData() or "copy")
        text = editcommands.content(wish, base, mode, self._claude_marks())
        self._claude_base, self._claude_result = base, None
        self._claude_busy = True
        self.cl_ask_btn.setEnabled(False)
        self._claude_buttons(False)
        self.cl_list.hide()
        self.cl_status.setText(_("Claude denkt nach …"))
        emit = self.bridge.claude.emit

        def work():
            try:
                emit((seq, base, mode, askclaude.request(key, editcommands.SYSTEM, text, editcommands.SCHEMA), None))
            except askclaude.AskError as e:
                emit((seq, base, mode, None, e.kind))
            except Exception as e:               # 1.34.2 (review W1): only the kind – never request or key
                log.warning("Claude im Editor: unerwarteter Fehler %s", e.__class__.__name__)
                emit((seq, base, mode, None, "bad"))
        threading.Thread(target=work, name="claude-edit", daemon=True).start()

    def _claude_answer(self, item):
        seq, base, mode, data, error = item
        if self._closed or seq != self._claude_seq:
            return                                       # an older wish (the window was busy with a newer one)
        self._claude_busy = False                        # 1.28: whatever comes next, asking works again
        try:
            self._claude_show(base, mode, data, error)
        except Exception:                                # never left on „Claude denkt nach …“
            self._claude_result = None
            self._claude_buttons(False)
            self.cl_status.setText(_(ERROR_WORDS["bad"]))
        finally:
            self._claude_refresh()

    def _claude_show(self, base, mode, data, error):
        if error is not None:
            self.cl_status.setText(_(ERROR_WORDS.get(error, ERROR_WORDS["net"])))
            return
        if self._state() != base:
            self.cl_status.setText(_("Der Schnitt hat sich inzwischen geändert – bitte neu vorschlagen."))
            return
        try:
            new, new_mode, done, skipped = editcommands.apply(base, data.get("ops"), mode)
        except ValueError:                               # "ops" not a list: an answer it cannot read
            self.cl_list.hide()
            self.cl_status.setText(_(ERROR_WORDS["bad"]))
            return
        summary = " ".join(str(data.get("summary") or "").split())[:300]
        lines = ["• " + _(w, **kw) for _op, (w, kw) in done]
        lines += ["– " + _("übersprungen: {why}", why=_(w, **kw)) for _op, (w, kw) in skipped]
        self.cl_list.setText("\n".join(lines))
        self.cl_list.setVisible(bool(lines))
        if not done:
            self.cl_status.setText(summary or _("Claude hat keinen passenden Schritt gefunden."))
            return
        self._claude_result = (new, new_mode)
        self.cl_status.setText(summary)
        self._claude_buttons(True)

    # ---- taking it over
    def claude_take(self):
        result, base = self._claude_result, self._claude_base
        if result is None:
            return
        if self._edit_locked() or self._gesture_active():
            self.cl_status.setText(_("Gerade nicht möglich – erst die laufende Bearbeitung beenden, dann übernehmen."))
            return
        if self._state() != base:
            self.claude_drop()
            self.cl_status.setText(_("Der Schnitt hat sich inzwischen geändert – bitte neu vorschlagen."))
            return
        new, new_mode = result
        if new_mode is not None and new_mode != self.mode_box.currentData():   # 1.28: only an explicit mode step
            self.mode_box.setCurrentIndex(max(0, self.mode_box.findData(new_mode)))
        self._apply(new)
        self._commit()                                   # one step back with Ctrl+Z
        self._claude_result = None
        self._claude_buttons(False)
        self.cl_list.hide()
        self.cl_status.setText(_("Übernommen – Strg+Z macht es rückgängig."))

    def claude_drop(self):
        self._claude_result = None
        self._claude_buttons(False)
        self.cl_list.hide()
        self.cl_status.setText("")
