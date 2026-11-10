"""1.27 (user: Claude in the clip editor, "Befehle in Worten"): the editor's section „Mit Claude bearbeiten“ –
mixed into qt_editor.EditorWindow.

The user writes what should happen („erste 10 s weg, ab 0:40 doppelt so schnell, als Short“); a thread sends the
wish and the edit as numbers (editcommands.content – no picture, no path, no map, no killer) to Claude
(askclaude.request); the answer comes back over the bridge, ``editcommands.apply`` turns it into a checked copy of
the state, the section lists what would happen and what was skipped. „Übernehmen“ shows it as one undo step,
„Verwerfen“ forgets it. A proposal made for an older state of the cut is not applied (the user changed the cut
meanwhile). The key and the user's permission come from the App (``claude_key``: a callable, "" = off).
1.43.1: Claude may ask back (``editcommands.question``); the next text in the field is the answer, sent with the
talk so far (only in memory, at most ``editcommands.MAX_ROUNDS`` requests, dropped with „Verwerfen“ or a changed
cut)."""
from __future__ import annotations

import json
import logging
import os
import threading

from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout

from . import askclaude, clipedit, editcommands, highlights, i18n, imageedit, moments, sequence, textfind
from .i18n import N_, _
from .qt_common import PlainLabel
from .qt_views import ElideButton

log = logging.getLogger(__name__)

ERROR_WORDS = {**askclaude.ERRORS,                                           # 1.38.3: the one table
               "still": N_("Das Standbild liess sich nicht lesen – nichts gesendet.")}


WISH_HINT = N_("z. B. erste 10 s weg, ab 0:40 doppelt so schnell, als Short")
CHECK_WORDS = {"name": N_("Name lesbar"), "chat": N_("Chat lesbar"), "other": N_("Auffällig")}   # 1.42


def highlights_thumbnail(img, title: str):
    """1.43: ``img`` (RGB) with ``title`` drawn centred in its lower part (shorts.text_picture: Inter Bold, white,
    dark outline); without a title the picture as it is."""
    if not title:
        return img
    from . import shorts
    text = shorts.text_picture(title, max(12, int(img.height * highlights.THUMB_TITLE_SHARE)), int(img.width * 0.9))
    if text is None:
        return img
    out = img.convert("RGB").copy()
    x = (out.width - text.width) // 2
    y = max(0, out.height - text.height - int(out.height * 0.06))
    out.paste(text, (x, y), text)
    return out


def _why(op) -> str:
    """1.43.1: Claude's short reason of one step, as plain text behind it ("" without one)."""
    why = editcommands.plain(op.get("why"), editcommands.MAX_WHY) if isinstance(op, dict) else ""
    return f" – {why}" if why else ""


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
        self._claude_talk = None             # 1.43.1: (base, mode, picture, messages, rounds) while Claude asks back
        self.templates_from = lambda: []     # 1.44: set by the App – the stored cut templates (settings)
        self._claude_ops = []                # 1.44: the steps of the shown proposal, as apply took them
        self._tpl_source = None              # 1.44: (state, ops, mode) of the last proposal taken – may become one

    # ---- the inspector section
    def _section_claude(self, sec, mode):
        self.bridge.claude.connect(self._claude_answer)
        self.cl_field = QLineEdit()
        self.cl_field.setPlaceholderText(_(WISH_HINT))
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
        self.cl_short_btn = QPushButton(_("Short vorschlagen"))  # 1.39.2: the whole short at once
        self.cl_short_btn.setToolTip(_("Schickt Standbilder an den gefundenen Momenten (aus Tasten, Spielton und "
                                       "F8-Marken, nur als Zahlen) und den Schnitt an Claude; Claude schlägt einen "
                                       "ganzen Short vor – Ausschnitt, Zeitlupe, Titel, Untertitel. Erst "
                                       "„Übernehmen“ ändert den Schnitt. Die Bilder können Spielernamen zeigen."))
        self.cl_short_btn.clicked.connect(self.claude_short)
        self.cl_check_btn = QPushButton(_("Export prüfen"))      # 1.42: the finished cut checked before sharing
        self.cl_check_btn.setToolTip(_("Schickt acht Standbilder des fertigen Schnitts (Bildausschnitt wie im Export, "
                                       "bereits zensierte Bereiche zensiert) an Claude; Claude meldet noch lesbare "
                                       "Namen oder Chat und anderes, das so nicht geteilt werden sollte. Ein Klick auf "
                                       "einen Fund springt hin und schlägt einen Zensurkasten vor."))
        self.cl_check_btn.clicked.connect(self.claude_check)
        self.cl_thumb_btn = QPushButton(_("Titel & Vorschaubild"))   # 1.43: proposed, saved only on a click
        self.cl_thumb_btn.setToolTip(_("Schickt dieselben acht Standbilder wie „Export prüfen“ an Claude; Claude wählt "
                                       "das beste Vorschaubild und schlägt einen Titel vor. Den Titel übernimmst du "
                                       "selbst, das Vorschaubild wird nur als Bild in „Clips“ gespeichert – nichts "
                                       "wird hochgeladen."))
        self.cl_thumb_btn.clicked.connect(self.claude_thumb)
        hl_row = QHBoxLayout()
        hl_row.setSpacing(6)
        hl_row.addWidget(self.cl_hl_btn)
        hl_row.addWidget(self.cl_short_btn)
        hl_row.addWidget(self.cl_check_btn)
        hl_row.addWidget(self.cl_thumb_btn)
        hl_row.addStretch()
        sec.body.addLayout(hl_row)
        self.cl_hl_rows = QVBoxLayout()                           # one button per highlight Claude named
        self.cl_hl_rows.setSpacing(4)
        sec.body.addLayout(self.cl_hl_rows)
        self._hl_found = []
        self._check_found = []                             # 1.42: the export check's findings
        self._thumb = None                                 # 1.43: (title, job of the still or None, base)
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
        self._section_templates(sec)
        self._claude_buttons(False)
        self._claude_refresh()

    # ---- 1.44: cut templates – local, no request
    def _section_templates(self, sec):
        save = QHBoxLayout()
        save.setSpacing(6)
        self.tpl_name = QLineEdit()
        self.tpl_name.setPlaceholderText(_("Name der Vorlage"))
        self.tpl_name.setMaxLength(editcommands.MAX_NAME)
        self.tpl_name.returnPressed.connect(self.template_save)
        self.tpl_save_btn = QPushButton(_("Als Vorlage speichern"))
        self.tpl_save_btn.setToolTip(_("Merkt sich die eben übernommenen Schritte (ohne Zensurkästen) als Vorlage – "
                                       "Zeiten vom Anfang bzw. vom Ende aus, damit sie auch bei anderen Längen passen."))
        self.tpl_save_btn.clicked.connect(self.template_save)
        save.addWidget(self.tpl_name, 1)
        save.addWidget(self.tpl_save_btn)
        sec.body.addLayout(save)
        use = QHBoxLayout()
        use.setSpacing(6)
        self.tpl_box = self._choice()                 # no focus, no wheel – like every box of the editor
        self.tpl_apply_btn = QPushButton(_("Vorlage anwenden"))
        self.tpl_apply_btn.setToolTip(_("Schlägt die Schritte der Vorlage für diesen Schnitt vor – ohne Claude, "
                                        "kostenlos; erst „Übernehmen“ ändert den Schnitt."))
        self.tpl_apply_btn.clicked.connect(self.template_apply)
        self.tpl_del_btn = QPushButton(_("Vorlage löschen"))
        self.tpl_del_btn.setToolTip(_("Entfernt die gewählte Vorlage."))
        self.tpl_del_btn.clicked.connect(self.template_delete)
        use.addWidget(self.tpl_box, 1)
        use.addWidget(self.tpl_apply_btn)
        use.addWidget(self.tpl_del_btn)
        sec.body.addLayout(use)
        self._tpl_widgets = (self.tpl_box, self.tpl_apply_btn, self.tpl_del_btn)
        self._templates_refresh()

    def _templates(self) -> list:
        try:
            return editcommands.templates(self.templates_from())
        except Exception:                                # a broken store never breaks the editor
            return []

    def _templates_refresh(self):
        if getattr(self, "tpl_box", None) is None:
            return
        found = self._templates()
        picked = self.tpl_box.currentText()
        self.tpl_box.blockSignals(True)
        self.tpl_box.clear()
        for t in found:
            self.tpl_box.addItem(t["name"])
        if picked:
            self.tpl_box.setCurrentIndex(max(0, self.tpl_box.findText(picked)))
        self.tpl_box.blockSignals(False)
        for w in self._tpl_widgets:
            w.setVisible(bool(found))
        for w in (self.tpl_name, self.tpl_save_btn):
            w.setVisible(self._tpl_source is not None)

    def template_save(self):
        source, name = self._tpl_source, self.tpl_name.text()
        if source is None:
            return
        state, ops, mode = source
        tpl = editcommands.to_template(state, ops, mode, name)
        if tpl is None:
            self.cl_status.setText(_("Bitte einen Namen für die Vorlage eingeben.")
                                   if not editcommands.plain(name, editcommands.MAX_NAME)
                                   else _("Nichts, was als Vorlage taugt (Zensurkästen gehören nicht dazu)."))
            return
        self._setting("edit_templates", editcommands.with_template(self.templates_from(), tpl))
        self._tpl_source = None
        self.tpl_name.clear()
        self.tpl_box.setCurrentIndex(-1)
        self._templates_refresh()
        self.tpl_box.setCurrentIndex(max(0, self.tpl_box.findText(tpl["name"])))
        self.cl_status.setText(_("Vorlage „{name}“ gespeichert.", name=tpl["name"]))

    def _template_picked(self):
        found = self._templates()
        i = self.tpl_box.currentIndex()
        return found[i] if 0 <= i < len(found) else None

    def template_apply(self):
        tpl = self._template_picked()
        if tpl is None or self.history is None or self._claude_busy:
            return
        base = self._state()
        mode = str(self.mode_box.currentData() or "copy")
        ops = editcommands.from_template(base, tpl, mode)
        self._claude_base, self._claude_result = base, None
        self._claude_show(base, mode, {"summary": _("Vorlage „{name}“", name=tpl["name"]), "ops": ops}, None)

    def template_delete(self):
        tpl = self._template_picked()
        if tpl is None:
            return
        self._setting("edit_templates", [t for t in self._templates() if t["name"] != tpl["name"]])
        self._templates_refresh()
        self.cl_status.setText(_("Vorlage „{name}“ gelöscht.", name=tpl["name"]))

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
        self.cl_short_btn.setVisible(frame_ok)                                   # 1.39.2
        self.cl_short_btn.setEnabled(frame_ok and self.history is not None and not self._claude_busy)
        self.cl_check_btn.setVisible(frame_ok)                                   # 1.42
        self.cl_check_btn.setEnabled(frame_ok and self.history is not None and not self._claude_busy)
        self.cl_thumb_btn.setVisible(frame_ok)                                   # 1.43
        self.cl_thumb_btn.setEnabled(frame_ok and self.history is not None and not self._claude_busy)
        self.cl_field.setEnabled(on)
        self.cl_ask_btn.setEnabled(on and self.history is not None and not self._claude_busy)
        if not on and self._claude_result is None:
            self.cl_status.setText(_("Aus – in Einstellungen → Verbindungen → Claude „Im Clip-Editor Claude "
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
        talk, self._claude_talk = self._claude_talk, None
        if talk is not None and talk[0] == self._state():          # 1.43.1: the answer to Claude's question
            base, mode, picture, history, rounds = talk
            still = None
            text = editcommands.follow_up(wish, rounds)
        else:
            base = self._state()
            mode = str(self.mode_box.currentData() or "copy")
            still = self._claude_still_job(base) if self.cl_frame_box.isChecked() and self.claude_frame() else None
            text = editcommands.content(wish, base, mode, self._claude_marks(), picture=still is not None)
            picture, history = None, []
        self.cl_field.setPlaceholderText(_(WISH_HINT))
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
                seen = (images != []) if picture is None else picture
                sent = history + [{"role": "user", "content": images + [{"type": "text", "text": text}]
                                   if images else text}]
                emit((seq, base, mode, askclaude.request(key, editcommands.SYSTEM, text, editcommands.SCHEMA,
                                                         images=images, history=history), seen, sent))
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
        if item and item[0] == "th":                     # 1.43: title and thumbnail
            self._thumb_answer(*item[1:])
            return
        if item and item[0] == "ck":                     # 1.42: the export check's findings
            self._check_answer(*item[1:])
            return
        if item and item[0] == "tx":                     # 1.41.1: which text boxes show names
            self._text_names_answer(*item[1:])
            return
        seq, base, mode, data, error, *sent = item       # 1.43.1: a wish also carries the messages it sent
        picture = error is True                          # 1.35: the slot carries "a still went along" on success
        error = None if isinstance(error, bool) else error
        if self._closed or seq != self._claude_seq:
            return                                       # an older wish (the window was busy with a newer one)
        self._claude_busy = False                        # 1.28: whatever comes next, asking works again
        try:
            self._claude_show(base, mode, data, error, picture, sent[0] if sent else None)
        except Exception:                                # never left on „Claude denkt nach …“
            self._claude_result = None
            self._claude_buttons(False)
            self.cl_status.setText(_(ERROR_WORDS["bad"]))
        finally:
            self._claude_refresh()

    def _claude_show(self, base, mode, data, error, picture=False, sent=None):
        self._claude_talk = None
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
        asked = editcommands.question(data)
        rounds = sum(1 for m in sent or () if m.get("role") == "user")
        if asked and sent is not None and rounds < editcommands.MAX_ROUNDS:    # 1.43.1: Claude asks back
            reply = {"role": "assistant", "content": json.dumps(data, ensure_ascii=False)}
            self._claude_talk = (base, mode, picture, list(sent) + [reply], rounds)
            self.cl_list.hide()
            self.cl_status.setText(_("Claude fragt: {question}", question=asked))
            self.cl_field.clear()
            self.cl_field.setPlaceholderText(_("Deine Antwort …"))
            self.cl_field.setFocus()
            self.cl_drop_btn.show()
            return
        self._claude_ops = [op for op, _w in done]       # 1.44: what „Übernehmen“ would take (for a template)
        self._claude_mode = mode
        lines = ["• " + _(w, **kw) + _why(op) for op, (w, kw) in done]
        lines += ["– " + _("übersprungen: {why}", why=_(w, **kw)) for _op, (w, kw) in skipped]
        self.cl_list.setText("\n".join(lines))
        self.cl_list.setVisible(bool(lines))
        if not done:
            self.cl_status.setText(summary or asked or _("Claude hat keinen passenden Schritt gefunden."))
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
        language = i18n.language_name()
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

    # ---- 1.42: „Export prüfen“ – stills of the finished cut (the export's crop), every censor box hidden
    def _cut_jobs(self, base) -> list:
        """[(output second, recording path, info, source second)] of the check stills (highlights.check_times)."""
        jobs = []
        for t in highlights.check_times(sequence.duration(base.parts)):
            i, src_t = sequence.source_at(base.parts, t)
            part = base.parts[i] if i is not None else None
            if part is not None:
                jobs.append((t, self._src_path(part), self._src_info(part), src_t))
        return jobs

    def _cut_picture(self, base):
        """A function (path, info, source second, height) → the picture as the export shows it – every censor box
        hidden (also outside a box's time: safer) and cut to the export's crop – or None. Safe in a thread."""
        boxes = [list(b) for b in base.boxes]
        style = base.censor_style if base.censor_style in imageedit.CENSOR_STYLES else "pixel"
        crop = tuple(base.crop) if base.crop else None
        ffmpeg = self.ffmpeg

        def picture(path, info, src_t, height):
            img = clipedit.frame_at(path, src_t, height, info, ffmpeg)
            if img is None:
                return None
            for b in boxes:                      # always hidden in what is sent – also while „anwenden“ is off
                img = imageedit.censor_area(img, b, style)
            if crop:                             # the part the export shows
                img = img.crop(imageedit.box_px(crop, img.size))
            return img
        return picture

    def claude_check(self):
        if self._claude_busy or self.history is None:
            return
        key = self.claude_key()
        if not key or not self.claude_frame():
            self._claude_refresh()
            return
        base = self._state()
        length = sequence.duration(base.parts)
        jobs = self._cut_jobs(base)
        if not jobs:
            return
        picture = self._cut_picture(base)
        language = i18n.language_name()
        self._claude_seq += 1
        seq = self._claude_seq
        self._claude_busy, self._claude_result = True, None
        self._claude_buttons(False)
        self._highlights_clear()
        self.cl_list.hide()
        self.cl_status.setText(_("Claude prüft {n} Standbilder des fertigen Schnitts …", n=len(jobs)))
        self._claude_refresh()
        emit = self.bridge.claude.emit

        def work():
            try:
                stills = []
                for t, path, info, src_t in jobs:
                    img = picture(path, info, src_t, highlights.CHECK_H)
                    if img is not None:
                        stills.append((t, askclaude.image_block(img, highlights.CHECK_SIDE)))
                if not stills:
                    raise _NoStill()
                data = askclaude.request(key, highlights.CHECK_SYSTEM,
                                         highlights.check_blocks(length, stills, language), highlights.CHECK_SCHEMA)
                emit(("ck", seq, base, data, None))
            except askclaude.AskError as e:
                emit(("ck", seq, base, None, e.kind))
            except _NoStill:
                emit(("ck", seq, base, None, "still"))
            except Exception as e:               # only the kind – never a picture or the key
                log.warning("Claude-Prüfung: unerwarteter Fehler %s", e.__class__.__name__)
                emit(("ck", seq, base, None, "bad"))
        threading.Thread(target=work, name="claude-check", daemon=True).start()

    # ---- 1.43: „Titel & Vorschaubild“ – the check stills; Claude picks one and proposes a title, nothing uploaded
    def claude_thumb(self):
        if self._claude_busy or self.history is None:
            return
        key = self.claude_key()
        if not key or not self.claude_frame():
            self._claude_refresh()
            return
        base = self._state()
        length = sequence.duration(base.parts)
        jobs = self._cut_jobs(base)
        if not jobs:
            return
        picture = self._cut_picture(base)
        language = i18n.language_name()
        self._claude_seq += 1
        seq = self._claude_seq
        self._claude_busy, self._claude_result = True, None
        self._claude_buttons(False)
        self._highlights_clear()
        self.cl_list.hide()
        self.cl_status.setText(_("Claude sucht unter {n} Standbildern ein Vorschaubild …", n=len(jobs)))
        self._claude_refresh()
        emit = self.bridge.claude.emit

        def work():
            try:
                stills, sent = [], []
                for job in jobs:
                    img = picture(job[1], job[2], job[3], highlights.CHECK_H)
                    if img is not None:
                        stills.append((job[0], askclaude.image_block(img, highlights.CHECK_SIDE)))
                        sent.append(job)
                if not stills:
                    raise _NoStill()
                data = askclaude.request(key, highlights.THUMB_SYSTEM,
                                         highlights.thumb_blocks(length, stills, language), highlights.THUMB_SCHEMA)
                emit(("th", seq, base, sent, data, None))
            except askclaude.AskError as e:
                emit(("th", seq, base, [], None, e.kind))
            except _NoStill:
                emit(("th", seq, base, [], None, "still"))
            except Exception as e:               # only the kind – never a picture or the key
                log.warning("Claude-Vorschaubild: unerwarteter Fehler %s", e.__class__.__name__)
                emit(("th", seq, base, [], None, "bad"))
        threading.Thread(target=work, name="claude-thumb", daemon=True).start()

    def _thumb_answer(self, seq, base, sent, data, error):
        if self._closed or seq != self._claude_seq:
            return
        self._claude_busy = False
        try:
            if error is not None:
                self.cl_status.setText(_(ERROR_WORDS.get(error, ERROR_WORDS["net"])))
                return
            try:
                summary, title, index = highlights.thumb_parse(data, len(sent))
            except ValueError:
                self.cl_status.setText(_(ERROR_WORDS["bad"]))
                return
            job = sent[index] if index >= 0 else None
            self._thumb = (title, job, base)
            self.cl_status.setText(summary)
            if title:
                btn = ElideButton()
                btn.set_full_text(_("Als Short-Titel: „{title}“", title=title))
                btn.setToolTip(_("Übernimmt den Titel als Titel des Shorts (ein Schritt zum Rückgängigmachen). Für "
                                 "YouTube kopierst du ihn selbst."))
                btn.clicked.connect(self.thumb_take_title)
                self.cl_hl_rows.addWidget(btn)
            if job is not None:
                btn = ElideButton()
                btn.set_full_text(_("Vorschaubild bei {at} speichern", at=clipedit.fmt_pos(job[0])))
                btn.setToolTip(_("Speichert dieses Standbild in voller Grösse als PNG in „Clips“ – zensiert wie im "
                                 "Export, mit dem Titel. Hochgeladen wird nichts."))
                btn.clicked.connect(self.thumb_save)
                self.cl_hl_rows.addWidget(btn)
                self.goto(job[0])
        except Exception:                                # never left on „Claude sucht …“
            self.cl_status.setText(_(ERROR_WORDS["bad"]))
        finally:
            self._claude_refresh()

    def thumb_take_title(self):
        """1.43: Claude's title becomes the short's title – one undo step (the short's own way)."""
        if not self._thumb or not self._thumb[0]:
            return
        from . import shorts
        spec = self._short_spec()
        spec.title = shorts.clean_text(self._thumb[0])
        self._short_set(spec)
        self.status.setText(_("Short-Titel übernommen."))

    def thumb_save(self):
        """1.43: the picked still in full size as a PNG next to the clips – every censor box hidden and cut like the
        export, the proposed title drawn in the lower part (shorts.text_picture). Saved like a still (_SaveJob,
        the clips list); nothing is uploaded."""
        if not self._thumb or self._thumb[1] is None:
            return
        title, job, base = self._thumb
        _t, path, info, src_t = job
        picture = self._cut_picture(base)
        try:
            os.makedirs(self.clips_dir, exist_ok=True)
        except OSError as e:
            self.status.setText(_("Clips-Ordner nicht anlegbar: {error}", error=e))
            return
        name = clipedit.NAME_CHARS.sub("", "{} – {}".format(os.path.splitext(os.path.basename(path))[0],
                                                         _("Vorschaubild")))
        out = clipedit.unique_path(self.clips_dir, name, ".png")
        b, height = self.bridge, min(int(getattr(info, "height", 0) or 1080), 2160)
        from .qt_clip import _SAVES, _SaveJob
        save = _SaveJob(self, out)

        def work():
            ok = False
            try:
                img = picture(path, info, src_t, height)
                if img is not None:
                    img = highlights_thumbnail(img, title)
                    img.save(out)
                    ok = True
            except Exception:                    # OSError, PIL: a result in any case
                log.exception("Vorschaubild speichern")
            b.still.emit(ok, out)
        save.thread = threading.Thread(target=work, name="clip-thumb", daemon=True)
        _SAVES.append(save)
        save.thread.start()

    def _check_answer(self, seq, base, data, error):
        if self._closed or seq != self._claude_seq:
            return
        self._claude_busy = False
        try:
            if error is not None:
                self.cl_status.setText(_(ERROR_WORDS.get(error, ERROR_WORDS["net"])))
                return
            try:
                summary, found = highlights.check_parse(data, sequence.duration(base.parts))
            except ValueError:
                self.cl_status.setText(_(ERROR_WORDS["bad"]))
                return
            self.cl_status.setText(summary or (_("Claude hat nichts gefunden, das so nicht geteilt werden sollte.")
                                               if not found else ""))
            self._check_found = [(at, kind, why, box, base) for at, kind, why, box in found]
            for i, (at, kind, why, box) in enumerate(found):
                btn = ElideButton()
                text = f"{clipedit.fmt_pos(at)} · {_(CHECK_WORDS[kind])}" + (f" – {why}" if why else "")
                btn.set_full_text(text)
                btn.setToolTip(text + "\n" + (_("Springt hin und schlägt einen Zensurkasten für diese Stelle vor.")
                                               if box else _("Springt hin.")))
                btn.setProperty("finding", i)        # a bound method, never a lambda holding the window
                btn.clicked.connect(self._finding_clicked)
                self.cl_hl_rows.addWidget(btn)
        except Exception:                                # never left on „Claude prüft …“
            self.cl_status.setText(_(ERROR_WORDS["bad"]))
        finally:
            self._claude_refresh()

    def _finding_clicked(self):
        n = self.sender().property("finding") if self.sender() is not None else None
        if isinstance(n, int):
            self.finding_pick(n)

    def finding_pick(self, n: int):
        """A finding → the playhead there; a name/chat box → a suggested censor box (whole recording picture, for
        CHECK_WINDOW_S around the moment of the recording), taken with „Vorschläge übernehmen“ (one undo step)."""
        found = getattr(self, "_check_found", [])
        if not 0 <= n < len(found):
            return
        at, _kind, _why, box, base = found[n]
        self.goto(at)
        if box is None:
            return
        _i, src_t = sequence.source_at(base.parts, at)
        if src_t is None:
            return
        full = highlights.uncrop(box, base.crop)
        w = highlights.CHECK_WINDOW_S
        self.preview.set_suggest([full + [round(max(0.0, src_t - w), 2), round(src_t + w, 2)]])
        if self.mode != "censor":
            self.mode_btns["censor"].setChecked(True)
        self.status.setText(_("Vorschlag bei {at} – „Vorschläge übernehmen“ verdeckt die Stelle.",
                              at=clipedit.fmt_pos(at)))
        self._censor_hint()

    # ---- 1.41.1: „Claude: nur Namen“ – the still with the numbered text boxes, the answer only numbers
    def claude_text_names(self):
        hits = [list(b) for b in self.preview.suggest]
        if self._claude_busy or not hits:
            return
        key = self.claude_key()
        if not key or not self.claude_frame():
            self._censor_hint()
            return
        i, src_t = sequence.source_at(self.parts, self.pos)
        part = self.parts[i] if i is not None else None
        if part is None:
            return
        path, info, ffmpeg = self._src_path(part), self._src_info(part), self.ffmpeg
        boxes = [list(b) for b in self.preview.boxes]
        style = self._censor_style if self._censor_style in imageedit.CENSOR_STYLES else "pixel"
        language = i18n.language_name()
        self._claude_seq += 1
        seq = self._claude_seq
        self._claude_busy = True
        self.status.setText(_("Claude sieht sich {n} Fundstellen an …", n=len(hits)))
        self._censor_hint()
        emit = self.bridge.claude.emit

        def work():
            try:
                img = clipedit.frame_at(path, src_t, min(int(getattr(info, "height", 0) or 1080), 1440), info, ffmpeg)
                if img is None:
                    raise _NoStill()
                for b in boxes:                  # always hidden in what is sent – also while „anwenden“ is off
                    img = imageedit.censor_area(img, b, style)
                block = askclaude.image_block(textfind.numbered(img, hits))
                data = askclaude.request(key, textfind.SYSTEM, textfind.blocks(len(hits), language, block),
                                         textfind.SCHEMA)
                emit(("tx", seq, hits, data, None))
            except askclaude.AskError as e:
                emit(("tx", seq, hits, None, e.kind))
            except _NoStill:
                emit(("tx", seq, hits, None, "still"))
            except Exception as e:               # only the kind – never a picture or the key
                log.warning("Claude-Namen: unerwarteter Fehler %s", e.__class__.__name__)
                emit(("tx", seq, hits, None, "bad"))
        threading.Thread(target=work, name="claude-names", daemon=True).start()

    def _text_names_answer(self, seq, hits, data, error):
        if self._closed or seq != self._claude_seq:
            return
        self._claude_busy = False
        try:
            if error is not None:
                self.status.setText(_(ERROR_WORDS.get(error, ERROR_WORDS["net"])))
                return
            if [list(b) for b in self.preview.suggest] != hits:
                return                                   # found again or taken meanwhile: the answer is stale
            try:
                summary, keep = textfind.parse(data, len(hits))
            except ValueError:
                self.status.setText(_(ERROR_WORDS["bad"]))
                return
            self.preview.set_suggest([hits[k] for k in keep])
            self.status.setText(summary or (_("Claude hält keine Fundstelle für einen Namen oder Chat.") if not keep
                                            else _("{n} Fundstellen zeigen laut Claude Namen oder Chat.",
                                                   n=len(keep))))
        except Exception:                                # never left on „Claude sieht sich … an“
            self.status.setText(_(ERROR_WORDS["bad"]))
        finally:
            self._claude_refresh()
            self._censor_hint()

    # ---- 1.39.2: „Short vorschlagen“
    def claude_short(self):
        """Stills at the local moments (and marks, and spread over the cut) + the cut and the moments as numbers →
        Claude proposes a whole short as editcommands operations; shown like a wish, taken on „Übernehmen“."""
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
        found = self._moments_now()
        peaks = [(x + y) / 2 for x, y, *_r in sorted(found, key=lambda m: -m[2])]
        jobs = []
        for t in highlights.still_times(length, marks, peaks):
            i, src_t = sequence.source_at(base.parts, t)
            part = base.parts[i] if i is not None else None
            jobs.append((t, self._src_path(part), self._src_info(part), src_t))
        if not jobs:
            return
        boxes = [list(b) for b in base.boxes]
        style = base.censor_style if base.censor_style in imageedit.CENSOR_STYLES else "pixel"
        language = i18n.language_name()
        from . import shorts
        wish = highlights.SHORT_WISH.format(limit=int(min(60, shorts.MAX_S)), language=language)
        text = (editcommands.content(wish, base, mode, marks, picture=False) + "\n\n"
                + moments.facts([(x, y, s, k) for x, y, s, k, *_r in found], length, marks))
        ffmpeg = self.ffmpeg
        self._claude_seq += 1
        seq = self._claude_seq
        self._claude_base, self._claude_result = base, None
        self._claude_busy = True
        self._claude_buttons(False)
        self._highlights_clear()
        self.cl_list.hide()
        self.cl_status.setText(_("Claude baut einen Short aus {n} Standbildern …", n=len(jobs)))
        self._claude_refresh()
        emit = self.bridge.claude.emit

        def work():
            try:
                content = [{"type": "text", "text": text}]
                for t, path, info, src_t in jobs:
                    img = clipedit.frame_at(path, src_t, highlights.STILL_H, info, ffmpeg)
                    if img is None:
                        continue
                    for b in boxes:              # always hidden in what is sent
                        img = imageedit.censor_area(img, b, style)
                    content += [{"type": "text", "text": f"Still at {round(t, 1):g} s:"},
                                askclaude.image_block(img, highlights.STILL_SIDE)]
                if len(content) == 1:
                    raise _NoStill()
                emit((seq, base, mode, askclaude.request(key, editcommands.SYSTEM, content, editcommands.SCHEMA),
                      False))
            except askclaude.AskError as e:
                emit((seq, base, mode, None, e.kind))
            except _NoStill:
                emit((seq, base, mode, None, "still"))
            except Exception as e:               # only the kind – never a picture or the key
                log.warning("Claude-Short: unerwarteter Fehler %s", e.__class__.__name__)
                emit((seq, base, mode, None, "bad"))
        threading.Thread(target=work, name="claude-short", daemon=True).start()

    def _highlights_clear(self):
        self._hl_found, self._check_found, self._thumb = [], [], None
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
        self._tpl_source = (base, list(self._claude_ops), getattr(self, "_claude_mode", "copy"))
        self._templates_refresh()
        self._claude_result = None
        self._claude_buttons(False)
        self.cl_list.hide()
        self.cl_status.setText(_("Übernommen – Strg+Z macht es rückgängig."))

    def claude_drop(self):
        self._claude_talk = None                         # 1.43.1: a question back is forgotten as well
        self.cl_field.setPlaceholderText(_(WISH_HINT))
        self._claude_result = None
        self._claude_buttons(False)
        self.cl_list.hide()
        self.cl_status.setText("")
