"""1.22 (user: "Mehrere Aufnahmen" → gewählt: Montage – Clips aus verschiedenen Runden hintereinander auf V1, eigene
Liste „Montagen“, Format wie die erste Aufnahme): the editor's side of a montage – mixed into qt_editor.EditorWindow.

* ``sources`` = the recordings (index 0 = the window's own ``path``), ``infos`` their probe; every clip
  (``Part.src``) and drawing (``Shape.src``) points at one. Preview, sound, strip pictures, loudness, marks and the
  export read the clip's own recording (``_src_path``/``_src_info`` – the ClipBase hooks).
* a recording dropped on V1 joins the timeline (``_montage_add``: probed in a thread, bridge channel ``montage``);
  the first one from another file makes the window a montage (``_become_montage``): the round's project keeps the
  state it had, the montage is a new project in Clips/Montagen (``project.MONTAGE_DIR``) bound to no recording.
* opening a montage file (``montage_file``): read and probed in a thread; a missing recording leaves its clips red
  and the export locked, a changed one (another SHA-256 than saved) asks first.
* the project's ``source`` stays a dict (projectsave unchanged): ``kind`` montage, ``items`` = identity of each
  recording, ``sha256`` = one hash over all of theirs once every one is known.

Only the user's own recordings are read; nothing is written but through projectsave."""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time

from . import clipedit, filehash, project, sequence
from .i18n import _

THUMBS_PER_SOURCE = clipedit.THUMBS


class MontageMixin:
    def _montage_init(self, path, montage_file=None, montage_new=None):
        self._montage = bool(montage_file or montage_new is not None)
        self._montage_file = montage_file
        self._montage_new = list(montage_new) if montage_new is not None else None   # [(path, marks)] to append
        self._montage_id = project.new_id()      # names its local copies until it has a project id
        self.sources = [path]
        self.infos = [None]                      # [0] is self.info once probed
        self._items = [{}]                       # identity of each recording (size, qfp, sha256, duration, …)
        self._saved_items = []                   # the identities a loaded montage file holds
        self._src_marks = {}                     # {recording ≥ 1: F8 marks}
        self._missing = set()
        self._src_threads = set()

    def _project_widgets(self, topbar_layout, index):
        super()._project_widgets(topbar_layout, index)
        self.bridge.montage.connect(self._montage_event)

    # ---- the ClipBase hooks: a clip's own recording
    def _src_of(self, part) -> int:
        s = getattr(part, "src", 0) if part is not None else 0
        return s if 0 <= s < len(self.sources) else 0

    def _src_path(self, part=None) -> str:
        s = self._src_of(part)
        return self.sources[s] if s else self.path

    def _src_info(self, part=None):
        s = self._src_of(part)
        info = self.infos[s] if s and s < len(self.infos) else None
        return info if info is not None else self.info

    def _mark_rows(self) -> list:
        """[(recording, source second)] of every F8 mark – the first recording's, then each other one's."""
        rows = [(0, m) for m in self.marks]
        for s in sorted(self._src_marks):
            rows += [(s, m) for m in self._src_marks[s]]
        return rows

    def _export_blocked(self) -> bool:
        return any(getattr(p, "src", 0) in self._missing for p in self.parts)

    def _durations(self):
        if not self._montage:
            return None
        return [float(self.info.duration or 0)] + [float(i.duration) if i is not None and i.ok else 0.0
                                                   for i in self.infos[1:]]

    def _default_name(self) -> str:
        if self._montage:
            return _("Montage {date}", date=time.strftime("%Y-%m-%d %H-%M"))
        return super()._default_name()

    # ---- the project hooks (ProjectMixin)
    def _project_folder(self) -> str:
        if self._montage:
            return os.path.join(self.clips_dir, project.MONTAGE_DIR)
        return super()._project_folder()

    def _src_key(self) -> str:
        if self._montage:
            return "montage:" + self._montage_id
        return super()._src_key()

    def _bind_keys(self, pid) -> list:
        if self._montage:
            return [pid, self._src_key()]
        return super()._bind_keys(pid)

    def _new_file_name(self, pid) -> str:
        if self._montage:
            return project.file_name_montage(self.name_edit.text() or self._default_name(), pid)
        return super()._new_file_name(pid)

    def _local_source_path(self) -> str:
        if self._montage:
            return os.path.join(self._project_folder(), "montage-" + self._montage_id)
        return super()._local_source_path()

    def _source(self) -> dict:
        if not self._montage:
            return super()._source()
        items = []
        for s, path in enumerate(self.sources):
            it = dict(self._items[s]) if s < len(self._items) else {}
            it["file"], it["path"] = os.path.basename(path), path
            try:
                it["rel"] = os.path.relpath(path, os.path.dirname(self.clips_dir))
            except ValueError:
                it["rel"] = None
            items.append(it)
        shas = [it.get("sha256") for it in items]
        combined = hashlib.sha256("".join(shas).encode()).hexdigest() if all(project.valid_sha(h) for h in shas) \
            else None
        return {"kind": "montage", "sha256": combined, "verified": None, "items": items,
                "path": self._local_source_path() if self._slot is None or not self._slot.pid else None}

    def _library_flag(self):
        if not self._montage:
            super()._library_flag()

    def take_over(self, start: float, end: float, pos: float):
        if self._montage:
            self.status.setText(_("Eine Montage übernimmt keinen Bereich aus der Vorschau."))
            return
        super().take_over(start, end, pos)

    # ---- adding a recording (a drop on V1)
    def _montage_add(self, path, marks=()):
        """``path`` joins the timeline at its end: one clip around each F8 mark (as „Clip um Marke“), without
        marks the whole recording. Probed in a thread; ``_montage_event("added")`` places it."""
        self._montage_add_many([(path, marks)])

    def _montage_add_many(self, files):
        """Several recordings, appended in this order (one thread reads them one after the other)."""
        if self._pstate in ("loading", "verify") or not self.info.ok:
            self.status.setText(_("Erst wenn das Projekt geladen ist."))
            return
        todo = []
        for path, marks in files:
            if not path or not os.path.isfile(path):
                self.status.setText(_("Keine Videodatei: {file}", file=os.path.basename(path or "")))
                continue
            todo.append((path, list(marks or ())))
        if not todo:
            return
        if len(set(self.sources) | {p for p, _m in todo}) > project.MAX_SOURCES:
            self.status.setText(_("Höchstens {n} Aufnahmen in einer Montage.", n=project.MAX_SOURCES))
            return
        self.status.setText(_("Lese {file} …", file=os.path.basename(todo[0][0])))
        ffmpeg, b, first, info0 = self.ffmpeg, self.bridge, (self.path if not self._items[0] else None), self.info

        def run():
            first_ident = _identity(first, info0) if first else None
            for path, marks in todo:
                info = clipedit.probe(path, ffmpeg)
                b.montage.emit("added", path, info, _identity(path, info), marks, first_ident)
        threading.Thread(target=run, name="montage-add", daemon=True).start()

    def _montage_event(self, kind, *args):
        if self._closed:
            return
        if kind == "added":
            self._montage_added(*args)
        elif kind == "opened":
            self._montage_opened(*args)
        elif kind == "thumb":
            s, i, img = args
            self.timeline.set_src_thumb(s, i, img)
        elif kind == "wave":
            s, bins = args
            self.timeline.set_source(s, wave=bins)
        elif kind == "hash":
            self._montage_hash(*args)

    def _montage_added(self, path, info, ident, marks, first_ident):
        name = os.path.basename(path)
        if not info.ok:
            self.status.setText(_("Video nicht lesbar: {file}", file=name))
            return
        if first_ident is not None:
            self._items[0] = first_ident
        known = [os.path.normcase(os.path.abspath(p)) for p in self.sources]
        key = os.path.normcase(os.path.abspath(path))
        s = known.index(key) if key in known else None
        if s is None and not self._montage:
            self._become_montage()
        if s is None:
            s = len(self.sources)
            self.sources.append(path)
            self.infos.append(info)
            self._items.append(ident)
            self._src_marks[s] = sorted(float(m) for m in marks)
            self._source_known(s)
        dur, (before, after) = info.duration, qt_marks()
        spans = [(max(0.0, m - before), min(dur, m + after)) for m in sorted(marks)] if marks else [(0.0, dur)]
        new = [clipedit.Part(a, b, src=s) for a, b in spans if b - a >= sequence.MIN_LEN]
        if not new:
            return
        at = sequence.duration(self.parts)
        self.parts = list(self.parts) + new
        self.timeline.set_parts(self.parts)
        self._commit()
        self.goto(at)
        hint = ""
        first = self.info
        if (info.width, info.height) != (first.width, first.height):
            hint = " " + _("Andere Grösse ({w}×{h}) – im Export mit schwarzen Rändern eingepasst.",
                           w=info.width, h=info.height)
        self.status.setText(_("{file}: {n} Clip(s) angehängt.", file=name, n=len(new)) + hint)

    def _become_montage(self):
        """The window turns into a montage: the round's project keeps its last state (flushed now), the montage
        is a new project in Clips/Montagen (made with the first save)."""
        if self._slot is not None and self._pstate == "bound":
            self._submit(view_event=True)                  # a change still waiting goes to the round's project
        self._montage = True
        self._rec = None
        self._unverified, self._migrated_from, self._project_loaded = False, None, False
        self._saved_items = []
        if not self._items[0]:
            self._items[0] = _identity(self.path, self.info)
        self._bind(None, "", base={"baseline_hash": None})
        self.name_edit.setText(self._default_name())
        self.name_edit.setModified(True)                      # the name stays (no round name any more)
        self._source_known(0)
        self.notice.show_notice("montage", _("Jetzt eine Montage – sie wird unter Clips → Montagen gespeichert. Das "
                                             "Projekt der Runde bleibt, wie es zuletzt gespeichert war."),
                                [("ok", _("Verstanden"))])
        self._library_mark()

    def _source_known(self, s):
        """A recording's name, length and marks on the timeline; its strip pictures and loudness in threads; its
        hash when not known yet."""
        tl = self.timeline
        path = self.sources[s]
        tl.set_source(s, name=_short(path))
        if s == 0:
            self._fill_marks()
            if not (self._items[0] or {}).get("sha256"):
                self._montage_hash_request(0)
            return
        info = self.infos[s]
        if info is None or not info.ok:
            return
        tl.set_source(s, duration=info.duration, marks=self._src_marks.get(s, []))
        self._input_source(s, path)                      # 1.39.1: its own input file
        self._fill_marks()
        if s not in self._src_threads:
            self._src_threads.add(s)
            self._source_threads(s, path, info)
        if not (self._items[s] or {}).get("sha256"):
            self._montage_hash_request(s)

    def _source_threads(self, s, path, info):
        ffmpeg, b, cancel = self.ffmpeg, self.bridge, self._cancel

        def strip():
            times = clipedit.thumb_times(info.duration, THUMBS_PER_SOURCE)
            for i, img in clipedit.thumb_strip(path, times, clipedit.THUMB_SRC_H, info, ffmpeg,
                                               stop=lambda: cancel.is_set()):
                b.montage.emit("thumb", s, i, img)

        def wave():
            if info.audio_tracks > 0:
                bins = clipedit.waveform(path, info.duration, ffmpeg, cancel=cancel)
                if not cancel.is_set():
                    b.montage.emit("wave", s, bins)
        threading.Thread(target=strip, name="montage-strip", daemon=True).start()
        threading.Thread(target=wave, name="montage-wave", daemon=True).start()

    def _montage_hash_request(self, s):
        b, path = self.bridge, self.sources[s]
        filehash.hasher().request(path, lambda r: b.montage.emit("hash", s, path, r))

    def _montage_hash(self, s, path, result):
        if not self._montage or s >= len(self.sources) or self.sources[s] != path or result.get("kind") != "done":
            return
        sha = result.get("sha256")
        self._items[s]["sha256"] = sha
        saved = self._saved_items[s].get("sha256") if s < len(self._saved_items) else None
        if project.valid_sha(saved) and saved != sha:
            self._source_changed(s)
            return
        if self._slot is not None and self._slot.pid and self._autosave:
            self._submit(view_event=False, force=True)     # the identity once every hash is known

    def _source_changed(self, s):
        if self.notice.key == "src_changed":
            return
        self.notice.show_notice("src_changed", _("{file} ist nicht mehr dieselbe Aufnahme wie beim Speichern.",
                                                 file=os.path.basename(self.sources[s])),
                                [("src_readonly", _("Nur lesen")), ("src_use", _("Trotzdem verwenden"))])

    def _notice_choice(self, key, ident):
        if ident == "src_readonly":
            if self._slot is not None:
                with self._slot.cv:
                    self._slot.status = "readonly"
            self._status_tick()
            return
        if ident == "src_use":
            self._saved_items = []
            if self._slot is not None and self._slot.pid:
                self._submit(view_event=False, force=True)
            return
        super()._notice_choice(key, ident)

    # ---- opening a montage file
    def _project_begin(self):
        if self._montage_new is not None:              # a new montage of several recordings (App: „Als Montage“)
            return self._montage_start()
        if not self._montage_file:
            return super()._project_begin()
        path, ffmpeg, b, first = self._montage_file, self.ffmpeg, self.bridge, self.path

        def load():
            try:
                with open(path, "rb") as fh:
                    raw = fh.read()
                data = json.loads(raw.decode("utf-8"))
                st = os.stat(path)
            except (OSError, ValueError, UnicodeDecodeError):
                b.montage.emit("opened", path, None, None, None, None)
                return
            srcs = project.montage_sources(data) or [first]
            infos = [None] + [clipedit.probe(p, ffmpeg) if os.path.isfile(p) else clipedit.Info(0, 0, 0, 0, 0)
                              for p in srcs[1:]]
            idents = [_identity(p, i if i is not None else None) for p, i in zip(srcs, infos)]
            entry = project.Entry(path, data, hashlib.sha256(raw).hexdigest(), st)
            b.montage.emit("opened", path, data, entry, srcs, (infos, idents))
        threading.Thread(target=load, name="montage-open", daemon=True).start()
        self._status_timer.start()
        self._safety.start()
        self._status_tick()

    def _montage_start(self):
        """A new montage: the first recording's clips (one around each mark, else all of it), the others appended
        in the order given; saved from the start (it is no recording's project)."""
        self._lock_editing(False)
        dur, (before, after) = float(self.info.duration or 0), qt_marks()
        spans = [(max(0.0, m - before), min(dur, m + after)) for m in sorted(self.marks)] or [(0.0, dur)]
        self.parts = [clipedit.Part(a, b) for a, b in spans if b - a >= sequence.MIN_LEN] or [clipedit.Part(0.0, dur)]
        self.timeline.set_parts(self.parts)
        self.history = sequence.History(self._state())
        self._refresh_undo()
        self._bind(None, "", base={"baseline_hash": None})
        self.name_edit.setText(self._default_name())
        self.name_edit.setModified(True)
        self._source_known(0)
        self._status_timer.start()
        self._safety.start()
        todo, self._montage_new = self._montage_new, None
        if todo:
            self._montage_add_many(todo)
        else:
            self._changed()
        self._refresh()

    def _montage_opened(self, path, data, entry, srcs, probed):
        self._montage = True
        if data is None or not isinstance(data, dict) or data.get("format") != project.FORMAT:
            self._start_new(quiet=True)
            self.notice.show_notice("broken", _("Die Projektdatei ist unlesbar und wurde nicht geladen."),
                                    [("ignore", _("Neu beginnen"))])
            return
        infos, idents = probed
        self.sources = list(srcs)
        self.infos = [None] + list(infos[1:])
        self._items = [dict(i) for i in idents]
        if not self._items[0]:
            self._items[0] = _identity(self.path, self.info)
        items = entry.source.get("items") if isinstance(entry.source.get("items"), list) else []
        self._saved_items = [dict(i) if isinstance(i, dict) else {} for i in items]
        self._missing = {s for s in range(1, len(self.sources)) if not (self.infos[s] and self.infos[s].ok)}
        self.timeline.set_missing(self._missing)
        for s in range(len(self.sources)):
            self._source_known(s)
        self._load_entry(entry, manual=False)
        if self._missing:
            names = ", ".join(os.path.basename(self.sources[s]) for s in sorted(self._missing))
            self.notice.show_notice("src_missing", _("Nicht gefunden: {files} – ihre Clips sind rot, Exportieren "
                                                     "geht erst, wenn sie entfernt sind.", files=names),
                                    [("ok", _("Verstanden"))])
        for s, it in enumerate(self._items):
            saved = self._saved_items[s].get("sha256") if s < len(self._saved_items) else None
            now = it.get("sha256")
            if project.valid_sha(saved) and project.valid_sha(now) and saved != now:
                self._source_changed(s)
                break
        self._inspector_refresh()

    def _library_mark(self):
        lib = getattr(self, "library", None)
        if lib is not None and hasattr(lib, "refresh_montages"):
            lib.refresh_montages()


def _identity(path, info) -> dict:
    """What identifies a recording in a montage file (size, quick fingerprint, the full hash when cached)."""
    if not path:
        return {}
    out = {"size": 0, "qfp": None, "sha256": None,
           "duration": round(float(getattr(info, "duration", 0) or 0), 2) if info is not None else None}
    try:
        st = os.stat(path)
        out["size"] = st.st_size
        out["qfp"] = filehash.qfp(path)
        out["sha256"] = filehash.hasher().cache.get(st)
    except OSError:
        pass
    return out


def _short(path) -> str:
    stem = os.path.splitext(os.path.basename(path))[0]
    return stem if len(stem) <= 28 else stem[:27] + "…"


def qt_marks() -> tuple:
    """(seconds before, after) a mark that „Clip um Marke“ takes – the editor's own constants."""
    from .qt_clip import MARK_AFTER_S, MARK_BEFORE_S
    return MARK_BEFORE_S, MARK_AFTER_S

