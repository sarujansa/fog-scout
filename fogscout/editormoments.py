"""1.39.2 (user's pick "Short vorschlagen" – local first, Claude on click): the big editor's section „Momente“ –
mixed into qt_editor.EditorWindow.

* the moments of each recording of the cut (moments.find: input changes, game sound, F8 marks), listed in output
  time; a click jumps there, „Clip um Moment“ makes the cut that moment (not in a montage);
* „Leerlauf kürzen“ cuts the stretches where nothing was held (moments.idle, needs the inputs) – one undo step;
* „Ladebildschirm abschneiden“ looks at the pictures of the first/last seconds in a thread (detector.is_dark) and
  cuts a dark start/end – one undo step;
* editorclaude's „Short vorschlagen“ takes the moments as numbers and their pictures as stills.

Everything here runs locally; nothing is sent."""
from __future__ import annotations

import logging
import threading

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget

from . import clipedit, editcommands, moments, sequence
from .i18n import N_, _
from .qt_common import PlainLabel
from .qt_layouts import FlowRow

log = logging.getLogger(__name__)

KIND_WORDS = {"mark": N_("F8-Marke"), "keys": N_("viele Tasten"), "sound": N_("laut")}
DARK_SCAN_S = 20.0             # seconds looked at, at the start and at the end
DARK_STEP_S = 1.0


class MomentsMixin:
    def _moments_init(self):
        self._moments_key = None
        self._moments = []             # [(out t0, out t1, score, kind, src, src t0, src t1)]
        self._dark_busy = False

    # ---- what the moments are made of
    def _moment_sources(self):
        """{source: (events, wave, wave per s, marks, length)} of every recording in the cut."""
        tl = self.timeline
        out = {}
        for s in sorted({getattr(p, "src", 0) for p in self.parts} or {0}):
            events = (getattr(self, "_input_events", {}) or {}).get(s) or []
            if s == 0:
                wave, marks, length = tl.wave, list(self.marks), float(self.info.duration or 0)
            else:
                wave = tl.src_wave.get(s, [])
                marks = list(getattr(self, "_src_marks", {}).get(s, []))
                length = float(tl.source_duration(s))
            out[s] = (events, wave, tl.wave_per_s, marks, length)
        return out

    def _moments_now(self) -> list:
        srcs = self._moment_sources()
        key = (tuple(repr(p) for p in self.parts),
               tuple((s, len(e), len(w), tuple(m), round(n, 2)) for s, (e, w, _ps, m, n) in srcs.items()))
        if key != self._moments_key:
            found = []
            for s, (events, wave, per_s, marks, length) in srcs.items():
                for a, b, _peak, score, kind in moments.find(events, wave, per_s, marks, length):
                    for x, y in moments.to_output(self.parts, [(a, b)], s):
                        found.append((x, y, score, kind, s, a, b))
            self._moments, self._moments_key = sorted(found), key
        return self._moments

    # ---- the inspector section
    def _section_moments(self, sec, mode):
        self.bridge.moments.connect(self._dark_answer)
        self.moment_list = QListWidget()
        self.moment_list.setObjectName("marks")
        self.moment_list.setMaximumHeight(140)
        self.moment_list.setFocusPolicy(Qt.NoFocus)
        self.moment_list.itemClicked.connect(self._moment_clicked)
        sec.body.addWidget(self.moment_list)
        row = FlowRow(spacing=6)
        self.moment_clip_btn = self._btn(row, _("Clip um Moment"), self.clip_around_moment,
                                         _("Der Schnitt wird der markierte Moment ({before} s davor bis {after} s "
                                           "danach).", before=f"{moments.BEFORE_S:g}", after=f"{moments.AFTER_S:g}"))
        self.idle_btn = self._btn(row, _("Leerlauf kürzen"), self.trim_idle,
                                  _("Schneidet Stellen heraus, an denen mindestens {n} s nichts gedrückt war "
                                    "(aus den Eingaben der Aufnahme) – ein Schritt zum Rückgängigmachen.",
                                    n=f"{moments.IDLE_MIN_S:g}"))
        self.dark_btn = self._btn(row, _("Ladebildschirm abschneiden"), self.trim_dark,
                                  _("Sieht sich die ersten und letzten {n} s an und schneidet einen schwarzen "
                                    "Anfang oder ein schwarzes Ende weg – ein Schritt zum Rückgängigmachen.",
                                    n=f"{DARK_SCAN_S:g}"))
        sec.body.addLayout(row)
        self.moment_status = PlainLabel("", "dim")
        sec.body.addWidget(self.moment_status)

    def _moments_refresh(self):
        if getattr(self, "moment_list", None) is None:
            return
        found = self._moments_now()
        self.moment_list.clear()
        for x, y, _score, kind, s, _a, _b in found:
            name = self.timeline.src_names.get(s, "") if getattr(self, "_montage", False) else ""
            self.moment_list.addItem(f"{clipedit.fmt_pos(x)}–{clipedit.fmt_pos(y)} · {_(KIND_WORDS[kind])}"
                                     + (f" · {name}" if name else ""))
        has_inputs = any((getattr(self, "_input_events", {}) or {}).values())
        self.moment_list.setVisible(bool(found))
        self.moment_clip_btn.setEnabled(bool(found) and not getattr(self, "_montage", False))
        self.idle_btn.setEnabled(has_inputs and bool(self.parts))
        self.dark_btn.setEnabled(bool(self.parts) and not self._dark_busy)
        sec = getattr(self, "sections", {}).get("moments")
        if sec is not None:
            sec.setVisible(bool(self.parts) and self.info.ok)

    def _moment_row(self):
        row = self.moment_list.currentRow()
        found = self._moments
        return found[row] if 0 <= row < len(found) else (found[0] if found else None)

    def _moment_clicked(self, _item=None):
        m = self._moment_row()
        if m is not None:
            self.goto(m[0])

    def clip_around_moment(self):
        m = self._moment_row()
        if m is None or getattr(self, "_montage", False):          # a montage keeps its clips
            return
        self.parts = [clipedit.Part(m[5], m[6])]
        self.timeline.set_parts(self.parts)
        self._commit()
        self.goto(0.0)

    def _take_ops(self, ops, done_text):
        """Local operations (editcommands) on the cut as one undo step."""
        if not ops:
            return False
        if self._edit_locked() or self._gesture_active():
            self.moment_status.setText(_("Gerade nicht möglich – erst die laufende Bearbeitung beenden."))
            return False
        mode = str(self.mode_box.currentData() or "copy")
        new, _new_mode, done, _skipped = editcommands.apply(self._state(), ops, mode)
        if not done:
            return False
        cut = sequence.duration(self.parts) - sequence.duration(new.parts)
        self._apply(new)
        self._commit()
        self.moment_status.setText(_(done_text, n=len(done), seconds=f"{cut:.0f}"))
        return True

    def trim_idle(self):
        ops = []
        for s, (events, _w, _ps, _m, length) in self._moment_sources().items():
            ops += [(a, b) for a, b in moments.to_output(self.parts, moments.idle(events, length), s)]
        if not self._take_ops(moments.cut_ops(ops), N_("{n} Leerlauf-Stelle(n) gekürzt ({seconds} s) – Strg+Z "
                                                         "macht es rückgängig.")):
            self.moment_status.setText(_("Kein Leerlauf gefunden."))

    def trim_dark(self):
        if self._dark_busy or not self.parts:
            return
        total = sequence.duration(self.parts)
        n = int(min(DARK_SCAN_S, total / 2) / DARK_STEP_S)
        start = [i * DARK_STEP_S for i in range(n)]
        end = [total - (i + 1) * DARK_STEP_S for i in range(n)]
        jobs = []
        for t in start + end:
            i, src_t = sequence.source_at(self.parts, t)
            part = self.parts[i] if i is not None else None
            jobs.append((self._src_path(part), self._src_info(part), src_t))
        ffmpeg, emit, base = self.ffmpeg, self.bridge.moments.emit, self._state()
        self._dark_busy = True
        self.dark_btn.setEnabled(False)
        self.moment_status.setText(_("Sehe mir Anfang und Ende an …"))

        def work():
            try:
                import numpy as np

                from .detector import is_dark
                darks = []
                for path, info, src_t in jobs:
                    img = clipedit.frame_at(path, src_t, 360, info, ffmpeg)
                    darks.append(bool(img is not None and is_dark(np.asarray(img)[:, :, ::-1])))
                emit((base, moments.dark_edges(darks[:n], darks[n:], DARK_STEP_S, total)))
            except Exception as e:                 # only the kind
                log.warning("Ladebildschirm-Suche: %s", e.__class__.__name__)
                emit((base, None))
        threading.Thread(target=work, name="dark-edges", daemon=True).start()

    def _dark_answer(self, item):
        base, ranges = item
        self._dark_busy = False
        if self._closed:
            return
        self.dark_btn.setEnabled(bool(self.parts))
        if ranges is None:
            self.moment_status.setText(_("Die Bilder liessen sich nicht lesen."))
            return
        if self._state() != base:
            self.moment_status.setText(_("Der Schnitt hat sich inzwischen geändert – bitte noch einmal."))
            return
        if not self._take_ops(moments.cut_ops(ranges), N_("{n} schwarze Stelle(n) abgeschnitten ({seconds} s) – "
                                                          "Strg+Z macht es rückgängig.")):
            self.moment_status.setText(_("Kein Ladebildschirm am Anfang oder Ende gefunden."))
