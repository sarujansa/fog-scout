"""1.21 (user: "eigene Tonspur" – eine Spur A2, Spielton automatisch leiser unter der Musik mit Regler, Ausblenden
am Ende; nur eigene Dateien): the editor's side of the own audio track – mixed into qt_editor.EditorWindow.

* the track (``musictrack.MusicSpec``) is part of the editor's state: undo/redo, the project (format 5), the export;
* adding: „Musik hinzufügen …“ (Qt's non-modal file dialog) or a file dropped on A2 – the file's length is read in
  a thread (ffprobe through ffmpeg), the clip lands at the playhead / the drop, at most to the end of the cut;
* the timeline's A2 lane moves and trims the clips, the inspector's sound section sets the levels, the ducking and
  the fades, and the selected clip's own level;
* the preview's sound mixes the track with the same chain as the export (``_play_music`` → ``sound_wav(music=)``).

Only files the user picks are read; nothing is recorded, nothing comes from Spotify or YouTube."""
from __future__ import annotations

import os
import threading
from dataclasses import replace

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QSlider, QWidget

from . import musictrack
from .i18n import N_, _
from .qt_common import guard_wheel
from .qt_layouts import FlowRow

DUCK_LABELS = {"off": N_("aus"), "light": N_("leicht"), "medium": N_("mittel"), "strong": N_("stark")}
FADES = (0.0, 0.5, 1.0, 2.0, 3.0, 5.0)
FILTER = "*.mp3 *.wav *.m4a *.aac *.ogg *.opus *.flac *.wma *.mp4 *.mkv *.mov *.webm"


class MusicMixin:
    def _music_init(self):
        self._music = None               # musictrack.MusicSpec of this cut (None = no track, game sound as recorded)
        self._music_lengths = {}         # {path: seconds of the file's sound}
        self._music_dialog = None
        self._music_probing = set()

    # ---- the inspector (called from _section_sound)
    def _slider(self, lo, hi, value, tip, slot):
        sl = guard_wheel(QSlider(Qt.Horizontal))
        sl.setRange(lo, hi)
        sl.setValue(value)
        sl.setToolTip(tip)
        sl.setFocusPolicy(Qt.NoFocus)
        val = QLabel("")
        val.setProperty("class", "dim")
        val.setMinimumWidth(42)
        box = QHBoxLayout()
        box.setSpacing(6)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(sl, 1)
        box.addWidget(val)
        holder = QWidget()
        holder.setLayout(box)
        sl.value_label = val
        sl.valueChanged.connect(slot)
        sl.valueChanged.connect(lambda v: val.setText(f"{v} %"))
        val.setText(f"{value} %")
        return sl, holder

    def _section_music(self, sec, mode):
        self.bridge.music.connect(self._music_probed)
        lbl = QLabel(_("Eigene Tonspur (A2)"))
        lbl.setProperty("class", "label")
        sec.body.addWidget(lbl)
        row = FlowRow(spacing=6)
        self.music_add_btn = self._btn(row, _("Musik hinzufügen …"), lambda: self._music_add_dialog(),
                                       _("Eine eigene Ton- oder Videodatei (Musik, Kommentar) am Abspielkopf auf die "
                                         "Spur A2 legen – oder die Datei direkt auf A2 ziehen."))
        sec.body.addLayout(row)
        tip_game = _("Lautstärke des Spieltons im fertigen Clip.")
        self.game_vol, holder = self._slider(0, round(musictrack.VOL_MAX * 100), 100, tip_game, self._music_levels)
        sec.row(_("Spielton"), holder)
        self.music_vol, holder = self._slider(0, round(musictrack.VOL_MAX * 100), 80,
                                              _("Lautstärke der ganzen Spur A2."), self._music_levels)
        sec.row(_("Musik"), holder)
        self.duck_box = self._combo(None, [(k, _(DUCK_LABELS[k])) for k in musictrack.DUCK_ORDER], "medium",
                                    _("Der Spielton wird von selbst leiser, solange Musik läuft – „stark“ drückt "
                                      "ihn am meisten. Aus: beide gleich laut wie eingestellt."), self._music_duck)
        sec.row(_("Spielton unter Musik"), self.duck_box)
        fades = [(f, _("aus") if f == 0 else f"{f:g} s") for f in FADES]
        self.music_in_box = self._combo(None, fades, 0.0, _("Die Musik wird am Anfang des Clips lauter."),
                                        self._music_fades)
        self.music_out_box = self._combo(None, fades, 2.0, _("Die Musik wird zum Ende des Clips leiser."),
                                         self._music_fades)
        sec.row(_("Musik ein"), self.music_in_box)
        sec.row(_("Musik aus"), self.music_out_box)
        self.music_clip_label = QLabel("")
        self.music_clip_label.setProperty("class", "dim")
        self.music_clip_label.setWordWrap(True)
        sec.body.addWidget(self.music_clip_label)
        self.music_clip_vol, self.music_clip_row = self._slider(
            0, round(musictrack.VOL_MAX * 100), 100, _("Lautstärke nur dieses Ton-Clips."), self._music_clip_level)
        lab = QLabel(_("Clip"))
        lab.setProperty("class", "label")
        self.music_clip_row.layout().insertWidget(0, lab)
        sec.body.addWidget(self.music_clip_row)
        row = FlowRow(spacing=6)
        self.music_here_btn = self._btn(row, _("Beginnt am Abspielkopf"), self._music_here,
                                        _("Der markierte Ton-Clip beginnt am Abspielkopf."))
        self.music_del_btn = self._btn(row, _("Ton-Clip entfernen"), lambda: self._music_remove(),
                                       _("Nimmt den markierten Ton-Clip von der Spur A2 – die Datei bleibt."))
        sec.body.addLayout(row)
        self.music_hint = QLabel(_("Die Vorschau spielt die Musik mit – Standbilder sind in der Vorschau still, im "
                                   "Export läuft die Musik weiter."))
        self.music_hint.setProperty("class", "dim")
        self.music_hint.setWordWrap(True)
        sec.body.addWidget(self.music_hint)

    def _music_wire(self, tl):
        """The timeline's A2 (built after the inspector)."""
        tl.music_edited.connect(self._music_edited)
        tl.music_selected.connect(lambda _k: self._music_show())
        tl.music_dropped.connect(self._music_add)
        self._music_show()

    # ---- the state
    def _music_spec(self) -> musictrack.MusicSpec:
        return self._music.copy() if self._music is not None else musictrack.MusicSpec()

    def _music_state(self):
        return self._music.copy() if self._music is not None else None

    def _music_apply(self, spec):
        """A state's track (undo/redo, a loaded project) – without writing history."""
        self._music = spec.copy() if spec is not None else None
        for c in self._music.clips if self._music else ():
            self._music_learn(c.path)
        self._music_show()

    def _music_set(self, spec, key=None, select=None):
        """The track changed: one undo step (``key`` merges a slider's drag), the timeline and section follow."""
        spec.clips = musictrack.clean(spec.clips)
        self._music = None if spec.empty() else spec
        if select is not None:
            self.timeline.music_sel = None
        self._music_show(select)
        self._commit(key)

    def _music_show(self, select=None):
        """The timeline's A2 and the section show the track (without firing the handlers)."""
        if getattr(self, "game_vol", None) is None or getattr(self, "timeline", None) is None:
            return
        spec = self._music_spec()
        self.timeline.set_music(spec.clips, self._music_lengths)
        if select is not None:
            self.timeline.select(None)
            self.timeline.select_music(select)
        for sl, v in ((self.game_vol, spec.game_vol), (self.music_vol, spec.music_vol)):
            if sl.isSliderDown():
                continue
            sl.blockSignals(True)
            sl.setValue(round(v * 100))
            sl.blockSignals(False)
            sl.value_label.setText(f"{sl.value()} %")
        for box, value in ((self.duck_box, spec.duck), (self.music_in_box, spec.fade_in),
                           (self.music_out_box, spec.fade_out)):
            box.blockSignals(True)
            idx = box.findData(value)
            if idx < 0 and isinstance(value, float):          # a fade from a project between the steps
                idx = min(range(box.count()), key=lambda i: abs(float(box.itemData(i)) - value))
            box.setCurrentIndex(max(0, idx))
            box.blockSignals(False)
        k = self.timeline.music_sel
        clip = spec.clips[k] if k is not None and k < len(spec.clips) else None
        has = bool(spec.clips)
        for w in (self.music_vol, self.duck_box, self.music_in_box, self.music_out_box):
            w.setEnabled(has)
        self.music_clip_row.setVisible(clip is not None)
        self.music_here_btn.setVisible(clip is not None)
        self.music_del_btn.setVisible(clip is not None)
        self.music_hint.setVisible(has)
        if clip is None:
            self.music_clip_label.setText(_("{n} Ton-Clip(s) auf A2.", n=len(spec.clips)) if has else
                                          _("Noch keine Musik – Spielton wie aufgenommen."))
        else:
            missing = "" if os.path.isfile(clip.path) else "  " + _("(Datei fehlt – wird nicht exportiert)")
            self.music_clip_label.setText(_("{file}: {start} – {end} der Datei, im Clip ab {at}",
                                            file=os.path.basename(clip.path), start=_fmt(clip.start),
                                            end=_fmt(clip.end), at=_fmt(clip.at)) + missing)
            sl = self.music_clip_vol
            if not sl.isSliderDown():
                sl.blockSignals(True)
                sl.setValue(round(clip.volume * 100))
                sl.blockSignals(False)
                sl.value_label.setText(f"{sl.value()} %")

    # ---- the controls
    def _music_levels(self, _v=None):
        if self._applying:
            return
        spec = self._music_spec()
        spec.game_vol, spec.music_vol = self.game_vol.value() / 100, self.music_vol.value() / 100
        self._music_set(spec, key=("music", "levels"))

    def _music_duck(self, _i=None):
        if self._applying:
            return
        spec = self._music_spec()
        spec.duck = self.duck_box.currentData() or "medium"
        self._music_set(spec)

    def _music_fades(self, _i=None):
        if self._applying:
            return
        spec = self._music_spec()
        spec.fade_in = float(self.music_in_box.currentData() or 0.0)
        spec.fade_out = float(self.music_out_box.currentData() or 0.0)
        self._music_set(spec)

    def _music_clip_level(self, v):
        k = self.timeline.music_sel
        spec = self._music_spec()
        if self._applying or k is None or k >= len(spec.clips):
            return
        spec.clips[k] = replace(spec.clips[k], volume=v / 100)
        self._music_set(spec, key=("music", "clip", k), select=k)

    def _music_here(self):
        self._music_move(self.timeline.music_sel, self.pos)

    def _music_move(self, k, at):
        spec = self._music_spec()
        if k is None or k >= len(spec.clips):
            return
        moved = replace(spec.clips[k], at=round(max(0.0, at), 3))
        others = spec.clips[:k] + spec.clips[k + 1:]
        spec.clips = musictrack.clean(others + [moved])
        self._music_set(spec, select=_index_of(spec.clips, moved))

    def _music_remove(self, k=None):
        k = self.timeline.music_sel if k is None else k
        spec = self._music_spec()
        if k is None or k >= len(spec.clips):
            return False
        name = os.path.basename(spec.clips[k].path)
        del spec.clips[k]
        self.timeline.music_sel = None
        self._music_set(spec)
        self.status.setText(_("Ton-Clip {file} entfernt – die Datei bleibt.", file=name))
        return True

    def _music_edited(self, clips):
        """A drag on A2 (move, trim) ended."""
        k = self.timeline.music_sel
        moved = clips[k] if k is not None and k < len(clips) else None
        spec = self._music_spec()
        spec.clips = musictrack.clean(clips)
        self._music_set(spec, select=_index_of(spec.clips, moved) if moved is not None else None)

    def _music_pick(self, ident, t, k) -> bool:
        """The timeline's right-click menu on A2 (True when it was one of these)."""
        if ident == "m_add":
            self._music_add_dialog(t)
        elif ident == "m_remove":
            self._music_remove(k)
        elif ident == "m_here":
            self._music_move(k, t)
        elif ident == "m_volume" and k is not None:
            spec = self._music_spec()
            if k < len(spec.clips):
                spec.clips[k] = replace(spec.clips[k], volume=float(t))
                self._music_set(spec, select=k)
        else:
            return False
        return True

    # ---- adding a file
    def _music_add_dialog(self, at=None):
        """Qt's own non-modal file dialog (no second message loop, like the library's import)."""
        at = self.pos if at is None else at
        start = os.path.dirname(self._music.clips[-1].path) if self._music and self._music.clips else \
            os.path.join(os.path.expanduser("~"), "Music")
        if not os.path.isdir(start):
            start = os.path.expanduser("~")
        dlg = QFileDialog(self, _("Musik hinzufügen"), start, _("Ton und Video") + f" ({FILTER});;* (*.*)")
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.fileSelected.connect(lambda path: self._music_add(path, at))
        dlg.open()
        self._music_dialog = dlg

    def _music_add(self, path, at):
        """A file for A2 at output second ``at``: its length is read in a thread, ``_music_probed`` places it."""
        if not path or not os.path.isfile(path) or not musictrack.is_audio(path):
            self.status.setText(_("Keine Ton- oder Videodatei: {file}", file=os.path.basename(path or "")))
            return
        self.status.setText(_("Lese {file} …", file=os.path.basename(path)))
        self._music_probe(path, max(0.0, float(at)))

    def _music_probe(self, path, at=None):
        ffmpeg, b = self.ffmpeg, self.bridge

        def run():
            b.music.emit(path, at, musictrack.file_seconds(path, ffmpeg))
        threading.Thread(target=run, name="clip-music", daemon=True).start()

    def _music_learn(self, path):
        """A clip from undo or a project: its file's length for trimming (once, in a thread)."""
        if path in self._music_lengths or path in self._music_probing or not os.path.isfile(path):
            return
        self._music_probing.add(path)
        self._music_probe(path)

    def _music_probed(self, path, at, seconds):
        self._music_probing.discard(path)
        if seconds > 0:
            self._music_lengths[path] = seconds
            self.timeline.music_lengths = dict(self._music_lengths)
        if at is None or self._closed:
            return
        name = os.path.basename(path)
        if seconds <= 0:
            self.status.setText(_("Kein Ton in {file}.", file=name))
            return
        spec = self._music_spec()
        if len(spec.clips) >= musictrack.MAX_CLIPS:
            self.status.setText(_("Höchstens {n} Ton-Clips.", n=musictrack.MAX_CLIPS))
            return
        room = self.timeline.total() - at
        length = min(seconds, room) if room >= 1.0 else seconds    # to the end of the cut; drag it longer
        clip = musictrack.AudioClip(path, round(at, 3), 0.0, round(length, 3))
        spec.clips = musictrack.clean(spec.clips + [clip])
        self._music_set(spec, select=_index_of(spec.clips, clip))
        self.status.setText(_("{file} liegt auf A2 ab {at} – der Spielton wird darunter leiser.", file=name,
                              at=_fmt(spec.clips[_index_of(spec.clips, clip) or 0].at)))

    def _play_music(self, seg):
        """The preview's sound for a stretch: (spec, its output start, its output length, the cut's length)."""
        if self._music is None:
            return None
        start, end, speed, out0 = seg[:4]
        return (self._music.copy(), float(out0), (end - start) / max(speed, 1e-6), self.timeline.total())


def _index_of(clips, clip):
    """Where ``clip`` (the same file part) landed after ``musictrack.clean`` – None when it dropped out."""
    found = [k for k, c in enumerate(clips) if (c.path, c.start, c.end) == (clip.path, round(clip.start, 3),
                                                                             round(clip.end, 3))]
    if not found:
        return None
    return min(found, key=lambda k: abs(clips[k].at - clip.at))


def _fmt(t: float) -> str:
    from .clipedit import fmt_pos
    return fmt_pos(t)
