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

from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout

from . import askclaude, clipedit, editcommands, highlights, i18n, imageedit, sequence
from .i18n import N_, _
from .qt_common import PlainLabel
from .qt_views import ElideButton

log = logging.getLogger(__name__)

ERROR_WORDS = {**askclaude.ERRORS,                                           # 1.38.3: the one table
               "still": N_("Das Standbild liess sich nicht lesen – nichts gesendet.")}


class _NoStill(Exception):
    """1.35: ffmpeg gave no picture at the play head – then nothing is sent."""


class ClaudeMixin:
    def _claude_init(self):
        self.claude_key = lambda: ""         # set by the App: the key while the user allows Claude in the editor
        self._claude_seq = 0                 # number of the last wish sent (older answers are dropped)
        self._claude_base = None             # the state the shown proposal was made for
        self._claude_result = None           # (new state, new mode or None)
        self._claude_busy = False            # 1.28 (audit F3): a wish is on its way – no second (paid) request
        self.claude_frame = lambda: False    # 1.35: set by the App – a still may go along („Standbilder an Claude“)

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
        self.cl_frame_box = QCheckBox(_("Standbild mitsenden"))   # 1.35: per wish, off by default
        self.cl_frame_box.setToolTip(_("Schickt zusätzlich das Bild an der Abspielposition (verkleinert, bereits "
                                       "zensierte Bereiche bleiben zensiert) – damit kann Claude z. B. Namen "
                                       "zensieren. Das Bild kann Spielernamen zeigen."))
        row.addWidget(self.cl_frame_box)
        row.addStretch()
        sec.body.addLayout(row)
        self.cl_hl_btn = QPushButton(_("Highlights finden"))      # 1.37: only with stills allowed
        self.cl_hl_btn.setToolTip(_("Schickt kleine Standbilder des Schnitts (gleichmässig verteilt und an den "
                                    "F8-Marken, bereits zensierte Bereiche zensiert) an Claude; Claude nennt bis zu "
                                    "drei Stellen für einen Short. Die Bilder können Spielernamen zeigen."))
        self.cl_hl_btn.clicked.connect(self.claude_highlights)
        sec.body.addWidget(self.cl_hl_btn)
        self.cl_hl_rows = QVBoxLayout()                           # one button per highlight Claude named
        self.cl_hl_rows.setSpacing(4)
        sec.body.addLayout(self.cl_hl_rows)
        self._hl_found = []
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
        frame_ok = on and bool(self.claude_frame())
        self.cl_frame_box.setVisible(frame_ok)
        if not frame_ok:
            self.cl_frame_box.setChecked(False)
        self.cl_hl_btn.setVisible(frame_ok)
        self.cl_hl_btn.setEnabled(frame_ok and self.history is not None and not self._claude_busy)
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
        still = self._claude_still_job(base) if self.cl_frame_box.isChecked() and self.claude_frame() else None
        text = editcommands.content(wish, base, mode, self._claude_marks(), picture=still is not None)
        self._claude_base, self._claude_result = base, None
        self._claude_busy = True
        self.cl_ask_btn.setEnabled(False)
        self._claude_buttons(False)
        self.cl_list.hide()
        self.cl_status.setText(_("Claude denkt nach …"))
        emit = self.bridge.claude.emit

        def work():
            try:
                images = [] if still is None else [still()]
                emit((seq, base, mode, askclaude.request(key, editcommands.SYSTEM, text, editcommands.SCHEMA,
                                                         images=images), images != []))
            except askclaude.AskError as e:
                emit((seq, base, mode, None, e.kind))
            except _NoStill:
                emit((seq, base, mode, None, "still"))
            except Exception as e:               # 1.34.2 (review W1): only the kind – never request or key
                log.warning("Claude im Editor: unerwarteter Fehler %s", e.__class__.__name__)
                emit((seq, base, mode, None, "bad"))
        threading.Thread(target=work, name="claude-edit", daemon=True).start()

    def _claude_still_job(self, state):
        """1.35: a function the asking thread calls – the recording's picture at the play head as an image block,
        the censor boxes already hidden (fractions of the source picture, like the export's censor_graph)."""
        i, src_t = sequence.source_at(state.parts, self.pos)
        part = state.parts[i] if i is not None else None
        path, info, ffmpeg = self._src_path(part), self._src_info(part), self.ffmpeg
        boxes, style = [list(b) for b in state.boxes], state.censor_style

        def make():
            img = clipedit.frame_at(path, src_t, min(int(getattr(info, "height", 0) or 1080), 1440), info, ffmpeg)
            if img is None:
                raise _NoStill()
            for b in boxes:                       # always hidden in what is sent – also while „anwenden“ is off
                img = imageedit.censor_area(img, b, style if style in imageedit.CENSOR_STYLES else "pixel")
            return askclaude.image_block(img)
        return make

    def _claude_answer(self, item):
        if item and item[0] == "hl":                     # 1.37: the highlight search's answer
            self._highlights_answer(*item[1:])
            return
        seq, base, mode, data, error = item
        picture = error is True                          # 1.35: the slot carries "a still went along" on success
        error = None if isinstance(error, bool) else error
        if self._closed or seq != self._claude_seq:
            return                                       # an older wish (the window was busy with a newer one)
        self._claude_busy = False                        # 1.28: whatever comes next, asking works again
        try:
            self._claude_show(base, mode, data, error, picture)
        except Exception:                                # never left on „Claude denkt nach …“
            self._claude_result = None
            self._claude_buttons(False)
            self.cl_status.setText(_(ERROR_WORDS["bad"]))
        finally:
            self._claude_refresh()

    def _claude_show(self, base, mode, data, error, picture=False):
        if error is not None:
            self.cl_status.setText(_(ERROR_WORDS.get(error, ERROR_WORDS["net"])))
            return
        if self._state() != base:
            self.cl_status.setText(_("Der Schnitt hat sich inzwischen geändert – bitte neu vorschlagen."))
            return
        try:
            new, new_mode, done, skipped = editcommands.apply(base, data.get("ops"), mode, picture)
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
    # ---- 1.37: highlights
    def claude_highlights(self):
        """„Highlights finden“: small stills of the edit (highlights.still_times) go to Claude in a thread – the
        censor boxes hidden in each, like the single still of a wish. Nothing changes before a picked range is taken."""
        if self._claude_busy or self.history is None:
            return
        key = self.claude_key()
        if not key or not self.claude_frame():
            self._claude_refresh()
            return
        base = self._state()
        mode = str(self.mode_box.currentData() or "copy")
        length = sequence.duration(base.parts)
        marks = self._claude_marks()
        jobs = []
        for t in highlights.still_times(length, marks):
            i, src_t = sequence.source_at(base.parts, t)
            part = base.parts[i] if i is not None else None
            jobs.append((t, self._src_path(part), self._src_info(part), src_t))
        if not jobs:
            return
        boxes = [list(b) for b in base.boxes]
        style = base.censor_style if base.censor_style in imageedit.CENSOR_STYLES else "pixel"
        language = "German" if i18n.current() == "de" else "English"
        ffmpeg = self.ffmpeg
        self._claude_seq += 1
        seq = self._claude_seq
        self._claude_busy, self._claude_result = True, None
        self._claude_buttons(False)
        self._highlights_clear()
        self.cl_list.hide()
        self.cl_status.setText(_("Claude sieht sich {n} Standbilder an …", n=len(jobs)))
        self._claude_refresh()
        emit = self.bridge.claude.emit

        def work():
            try:
                stills = []
                for t, path, info, src_t in jobs:
                    img = clipedit.frame_at(path, src_t, highlights.STILL_H, info, ffmpeg)
                    if img is None:
                        continue
                    for b in boxes:              # always hidden in what is sent – also while „anwenden“ is off
                        img = imageedit.censor_area(img, b, style)
                    stills.append((t, askclaude.image_block(img, highlights.STILL_SIDE)))
                if not stills:
                    raise _NoStill()
                data = askclaude.request(key, highlights.SYSTEM,
                                         highlights.blocks(length, marks, stills, language), highlights.SCHEMA)
                emit(("hl", seq, base, mode, data, None))
            except askclaude.AskError as e:
                emit(("hl", seq, base, mode, None, e.kind))
            except _NoStill:
                emit(("hl", seq, base, mode, None, "still"))
            except Exception as e:               # only the kind – never a picture or the key
                log.warning("Claude-Highlights: unerwarteter Fehler %s", e.__class__.__name__)
                emit(("hl", seq, base, mode, None, "bad"))
        threading.Thread(target=work, name="claude-highlights", daemon=True).start()

    def _highlights_clear(self):
        self._hl_found = []
        while self.cl_hl_rows.count():
            w = self.cl_hl_rows.takeAt(0).widget()
            if w is not None:
                w.deleteLater()

    def _highlights_answer(self, seq, base, mode, data, error):
        if self._closed or seq != self._claude_seq:
            return
        self._claude_busy = False
        try:
            if error is not None:
                self.cl_status.setText(_(ERROR_WORDS.get(error, ERROR_WORDS["net"])))
                return
            length = sequence.duration(base.parts)
            try:
                summary, found = highlights.parse(data, length)
            except ValueError:
                self.cl_status.setText(_(ERROR_WORDS["bad"]))
                return
            self.cl_status.setText(summary or (_("Claude hat keine Stelle gefunden, die heraussticht.")
                                               if not found else ""))
            self._hl_found = [(a, b, why, base, mode) for a, b, why in found]
            for i, (a, b, why) in enumerate(found):
                btn = ElideButton()                  # a long reason ends in "…" – the inspector keeps its width
                text = f"{clipedit.fmt_pos(a)}–{clipedit.fmt_pos(b)}" + (f" · {why}" if why else "")
                btn.set_full_text(text)
                btn.setToolTip(text + "\n" + _("Schlägt vor, nur diesen Teil zu behalten – erst „Übernehmen“ "
                                                "ändert den Schnitt."))
                btn.setProperty("highlight", i)      # a bound method, never a lambda holding the window
                btn.clicked.connect(self._highlight_clicked)
                self.cl_hl_rows.addWidget(btn)
        except Exception:                                # never left on „Claude sieht sich … an“
            self.cl_status.setText(_(ERROR_WORDS["bad"]))
        finally:
            self._claude_refresh()

    def _highlight_clicked(self):
        n = self.sender().property("highlight") if self.sender() is not None else None
        if isinstance(n, int):
            self.highlight_pick(n)

    def highlight_pick(self, n: int):
        """A highlight → the proposal keep(from, to), checked by editcommands.apply like any wish; „Übernehmen“
        takes it as one undo step. A cut changed since the search is not touched."""
        if not 0 <= n < len(self._hl_found):
            return
        a, b, why, base, mode = self._hl_found[n]
        self._claude_base, self._claude_result = base, None
        self._claude_show(base, mode, {"summary": why, "ops": [{"op": "keep", "from": a, "to": b}]}, None)

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
