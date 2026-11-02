"""1.18.1 (Implementierungsplan Fassung 6): the editor's side of project saving – mixed into qt_editor.EditorWindow.

* loading in a thread: the recording's identity (size, quick fingerprint, duration; the full SHA-256 from the hasher
  and its cache), the catalog of project files, ``project.resolve`` → load / ask / start new (2.5);
* a slot in ``projectsave.registry()`` per project (claim on open, release on close; a reopened window starts from
  the slot's newest state);
* autosave: ``_changed`` restarts a 1.5 s timer (at most 10 s while changes keep coming), never during a drag; a
  5 s safety net; the view (playhead, visible span) on focus loss, close, Strg+S and quit;
* ``NoticeBar`` – every question in one bar under the top bar, the first button the safe choice, never modal;
* the status beside the project name from ``projectsave.status_of``.

Nothing here writes a file itself – projectsave does, through fsops."""
from __future__ import annotations

import json
import os
import threading
import time

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QLabel, QMenu, QPushButton

from . import filehash, project, projectsave, sequence
from .projectsave import source_meta
from .i18n import _

SAVE_DELAY_MS = 1500
SAVE_MAX_MS = 10000
SAFETY_MS = 5000
STATUS_MS = 400


class NoticeBar(QFrame):
    """One question at a time under the top bar: text and up to three buttons (the first is the safe choice), or a
    button with a menu. ``show_notice(key, text, buttons)`` – buttons = [(id, label) | (id, label, [(sub_id, sub_label)])];
    ``on_choice(key, id)``; ``choose(id)`` for tests. Esc never answers it."""

    def __init__(self, on_choice):
        super().__init__()
        self.setObjectName("noticebar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.on_choice = on_choice
        self.key = None
        self.buttons = {}
        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 6, 12, 6)
        lay.setSpacing(8)
        self.text = QLabel("")
        self.text.setWordWrap(True)
        self.text.setTextFormat(Qt.PlainText)
        lay.addWidget(self.text, 1)
        self._row = lay
        self.setVisible(False)

    def show_notice(self, key: str, text: str, buttons):
        for b in self.buttons.values():
            b.setParent(None)
            b.deleteLater()
        self.buttons = {}
        self.key = key
        self.text.setText(text)
        for i, spec in enumerate(buttons):
            ident, label = spec[0], spec[1]
            btn = QPushButton(label)
            btn.setFocusPolicy(Qt.NoFocus)
            if i == 0:
                btn.setObjectName("primary")
            if len(spec) > 2:
                menu = QMenu(btn)
                for sub, sub_label in spec[2]:
                    menu.addAction(sub_label).triggered.connect(lambda _c=False, s=sub: self.choose(s))
                btn.setMenu(menu)
            else:
                btn.clicked.connect(lambda _c=False, i_=ident: self.choose(i_))
            self._row.addWidget(btn)
            self.buttons[ident] = btn
        self.setVisible(True)

    def clear(self, key: str | None = None):
        if key is None or key == self.key:
            self.key = None
            self.setVisible(False)

    def choose(self, ident):
        key = self.key
        self.clear()
        self.on_choice(key, ident)


def _when(ts) -> str:
    try:
        return time.strftime("%d.%m. %H:%M", time.localtime(float(ts)))
    except (TypeError, ValueError, OverflowError, OSError):
        return "?"


class ProjectMixin:
    """Mixed into EditorWindow (``self.path``, ``self.info``, ``self.clips_dir``, ``self.bridge``, ``self.preview``,
    ``self.timeline``, ``self.history``, ``_state``/``_apply``/``_project_extra``/``_apply_project_extra``)."""

    # ---- set-up
    def _project_init(self, registry=None, autosave: bool = True, round_t=None):
        self._reg = registry if registry is not None else projectsave.registry()
        self._token = object()
        self._slot = None
        self._pstate = "loading"          # loading / verify / bound / unbound
        self._rec = None
        self._entries = []
        self._autosave = bool(autosave)
        self._round_t = round_t
        self._pdirty = False
        self._ploading = False
        self._save_after_gesture = False
        self._last_submitted = None
        self._last_view = None
        self._last_view_event = False
        self._last_meta = None
        self._saved_at = None
        self._seen_written = 0
        self._hash_progress = None
        self._unverified = False
        self._local_seq = 0
        self._pending_take_over = None
        self._manual_seq = None
        self._migrated_from = None
        self._closing_asked = False
        self._project_loaded = False

    def _project_widgets(self, topbar_layout, index):
        """The status label beside the name (inserted at ``index`` of the top bar) and the notice bar."""
        self.save_status = QLabel("")
        self.save_status.setObjectName("savestatus")
        self.save_status.setProperty("class", "dim")
        topbar_layout.insertWidget(index, self.save_status)
        self.notice = NoticeBar(self._notice_choice)
        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(SAVE_DELAY_MS)
        self._save_timer.timeout.connect(self._save_due)
        self._max_timer = QTimer(self)
        self._max_timer.setSingleShot(True)
        self._max_timer.setInterval(SAVE_MAX_MS)
        self._max_timer.timeout.connect(self._save_due)
        self._safety = QTimer(self)
        self._safety.setInterval(SAFETY_MS)
        self._safety.timeout.connect(self._safety_net)
        self._status_timer = QTimer(self)
        self._status_timer.setInterval(STATUS_MS)
        self._status_timer.timeout.connect(self._status_tick)
        self.bridge.project.connect(self._project_found)
        self.bridge.hash.connect(self._hash_event)
        self.name_edit.textEdited.connect(lambda _t: self._changed())

    # ---- identity and loading (2.5)
    def _project_folder(self) -> str:
        return os.path.join(self.clips_dir, project.PROJECT_DIR)

    def _src_key(self) -> str:
        return "src:" + os.path.normcase(os.path.abspath(self.path))

    def _project_begin(self):
        """Called by ``_ready`` once the recording is known: the lookup runs in a thread, the result comes back
        through the bridge (``project``); the full hash through ``hash``."""
        path, folder, duration, t, b = self.path, self._project_folder(), float(self.info.duration or 0), \
            self._round_t, self.bridge
        cache = filehash.hasher().cache

        def lookup():
            rec = {"file": os.path.basename(path), "duration": round(duration, 2), "t": t, "sha256": None,
                   "size": 0, "qfp": None}
            try:
                st = os.stat(path)
                rec["size"] = st.st_size
                rec["qfp"] = filehash.qfp(path)
                rec["sha256"] = cache.get(st)
            except OSError:
                pass
            entries = project.scan(folder)
            b.project.emit(rec, entries)
        threading.Thread(target=lookup, name="project-lookup", daemon=True).start()
        self._status_timer.start()
        self._safety.start()
        self._status_tick()

    def _request_hash(self):
        b = self.bridge
        filehash.hasher().request(self.path, lambda r: b.hash.emit(r),
                                  on_progress=lambda d, total: b.hash.emit({"kind": "progress", "done": d,
                                                                             "total": total}))

    def _project_found(self, rec, entries):
        if self._closed:
            return
        self._rec, self._entries = rec, entries
        if not rec.get("sha256"):
            self._request_hash()
        self._resolve_now()

    def _hash_event(self, result):
        if self._closed or self._rec is None:
            return
        kind = result.get("kind")
        if kind == "progress":
            total = max(1, int(result.get("total") or 1))
            self._hash_progress = int(100 * int(result.get("done") or 0) / total)
            return
        self._hash_progress = None
        if kind == "done":
            self._rec["sha256"] = result.get("sha256")
            if self._slot is not None and result.get("sha256"):
                with self._reg.lock:                              # the slot is found by the recording's hash too
                    self._slot.keys.add(result["sha256"])
                if self._slot.pid and self._autosave:             # a file written before the hash was known gets it
                    self._submit(view_event=False, force=True)
            if self._pstate == "verify":
                self._resolve_now()
        elif kind == "placeholder" and self._pstate == "verify":
            self.notice.show_notice("verify", _("Die Aufnahme liegt nur in der Cloud – die Prüfung würde sie ganz "
                                                "herunterladen."),
                                    [("new", _("Neu beginnen")), ("load_unverified", _("Ohne Prüfung laden")),
                                     ("hash_anyway", _("Prüfen"))])
        elif kind in ("error", "changed") and self._pstate == "verify":
            self.notice.show_notice("verify", _("Die Aufnahme konnte nicht geprüft werden."),
                                    [("new", _("Neu beginnen")), ("load_unverified", _("Ohne Prüfung laden")),
                                     ("rehash", _("Erneut prüfen"))])

    def _resolve_now(self):
        res = project.resolve(self._rec, self._entries)
        self._resolution = res
        kind, entries = res.kind, res.entries
        if kind == "auto":
            self._load_entry(entries[0], manual=False)
        elif kind == "none":
            self._start_new()
        elif kind == "verify":
            self._pstate = "verify"
            self._lock_editing(True)
            self.notice.show_notice("verify", _("Gespeichertes Projekt gefunden – die Aufnahme wird geprüft."),
                                    [("new", _("Neu beginnen")), ("load_unverified", _("Ohne Prüfung laden"))])
        elif kind == "mismatch":
            self._start_new(quiet=True)
            self.notice.show_notice("mismatch", _("Die Aufnahme passt nicht zum gespeicherten Projekt (ihr Inhalt "
                                                  "ist anders). Es wurde nicht geladen."),
                                    [("ignore", _("Neu beginnen")), ("load_unverified", _("Trotzdem laden"))])
        elif kind == "unverified":
            self._start_new(quiet=True)
            self.notice.show_notice("unverified", _("Zu dieser Aufnahme gibt es ein Projekt, das nie vollständig "
                                                    "geprüft wurde. Anfang, Ende und Grösse stimmen; ob es die "
                                                    "ganze Aufnahme ist, kann Fog Scout nicht bestätigen."),
                                    [("ignore", _("Nicht laden")), ("load_unverified", _("Trotzdem laden"))])
        elif kind == "legacy":
            self._start_new(quiet=True)
            self.notice.show_notice("legacy", _("Projekt aus Fog Scout 1.17 oder älter gefunden (gleicher Name, "
                                                "gleiche Grösse)."),
                                    [("ignore", _("Ignorieren")), ("load_legacy", _("Laden"))])
        elif kind == "changed":
            self._start_new(quiet=True)
            self.notice.show_notice("changed", _("Es gibt ein Projekt zu einer gleichnamigen, aber veränderten "
                                                 "Aufnahme."),
                                    [("ignore", _("Ignorieren")), ("load_unverified", _("Trotzdem laden"))])
        elif kind in ("ambiguous_id", "ambiguous_recording"):
            self._start_new(quiet=True)
            menu = [(f"pick:{i}", f"{e.name} · {_when(e.saved)}") for i, e in enumerate(entries)]
            self.notice.show_notice("ambiguous", _("{n} Projektdateien passen zu dieser Aufnahme – keine wurde "
                                                   "geöffnet.", n=len(entries)),
                                    [("ignore", _("Keine öffnen")), ("pick", _("Eine wählen …"), menu)])
        self._offer_local()
        self._status_tick()

    def _edit_locked(self) -> bool:
        """While the recording is checked against a saved project, nothing may be edited (it would be replaced). The
        lookup before ("loading") takes milliseconds under the loading screen and locks nothing."""
        return self._pstate == "verify"

    def _lock_editing(self, on: bool):
        for w in (self.tl_panel, self.inspector):
            w.setEnabled(not on)
        for b in self.mode_btns.values():
            b.setEnabled(not on)
        self.project_btn.setEnabled(not on)

    def _read_entry(self, entry):
        try:
            with open(entry.path, "rb") as fh:
                raw = fh.read()
            return raw, json.loads(raw.decode("utf-8"))
        except (OSError, ValueError, UnicodeDecodeError):
            return None, None

    def _apply_data(self, data) -> dict | None:
        """Show project ``data`` (format 1 or 2, field by field – project.validate); its view, or None."""
        got = project.validate(data, float(self.info.duration or 0), self.parts or [])
        if got is None:
            return None
        state, extra, view, notes = got
        self._ploading = True
        try:
            self._apply_project_extra(extra)
            if state.crop_key == "content" and self.crop_box.findData("content") < 0:
                from .qt_clip import CONTENT_LABEL
                self.crop_box.insertItem(1, _(CONTENT_LABEL), "content")
            self._apply(state)
            self._crop_chosen = True                              # a project's crop (or none) is the user's choice
            self.history = sequence.History(self._state())
            self._refresh_undo()
        finally:
            self._ploading = False
        if "parts" in notes:
            self.status.setText(_("Die Clips des Projekts waren unlesbar – der Standardclip wird gezeigt."))
        self._project_loaded = True
        return view or {}

    def _load_entry(self, entry, manual: bool):
        raw, data = self._read_entry(entry)
        if data is None:
            self._start_new(quiet=True)
            self.notice.show_notice("broken", _("Die Projektdatei ist unlesbar und wurde nicht geladen."),
                                    [("ignore", _("Neu beginnen"))])
            return
        view = self._apply_data(data)
        if view is None:
            self._start_new(quiet=True)
            return
        self._lock_editing(False)
        self.notice.clear()
        self._saved_at = entry.saved or None
        content = project.content_dict(self._state(), self._project_extra())
        newer_version = int(data.get("version") or 1) > project.VERSION2
        if entry.version >= project.VERSION2 and entry.id:
            self._bind(entry.id, entry.path, base={"base_hash": entry.hash, "content_hash": project.content_hash(content),
                                                   "view": data.get("view"), "baseline_hash": project.content_hash(content),
                                                   "meta": projectsave.source_meta(entry.source)})
            if manual and self._slot is not None:
                self._reg.submit_fifo(self._slot, "vor-zuordnung", raw)
                self._unverified = True
                self._pdirty = True
            if newer_version and self._slot is not None:
                self._slot.status = "readonly"
        else:                                                    # format 1, carried on as a new format-2 project
            self._migrated_from = entry.name
            self._unverified = True
            self._bind(None, "", base={"baseline_hash": None})
            self._pdirty = True
        self._restore_view(view)
        self.status.setText(_("Projekt geladen: {name}", name=self.name_edit.text() or entry.name))
        if self._pending_take_over is not None:
            self._offer_take_over()
        if self._pdirty:
            self._changed()

    def _start_new(self, quiet: bool = False):
        """No project (yet): the state at opening is the baseline – a file is made only for a real change."""
        self._lock_editing(False)
        if not quiet:
            self.notice.clear()
        content = project.content_dict(self._state(), self._project_extra())
        self._bind(None, "", base={"baseline_hash": project.content_hash(content)})
        if self._pending_take_over is not None:
            start, end, pos = self._pending_take_over
            self._pending_take_over = None
            self._apply_take_over(start, end, pos)

    def _unbind(self):
        """Give up the current slot: released, and no longer found by this recording (a project loaded or started
        instead gets a slot of its own)."""
        slot, self._slot = self._slot, None
        if slot is None:
            return
        with self._reg.lock:
            slot.keys.discard(self._src_key())
            slot.keys.discard((self._rec or {}).get("sha256"))
        self._reg.release(slot, self._token)

    def _bind(self, pid, path, base):
        self._unbind()
        keys = [pid, self._src_key(), (self._rec or {}).get("sha256")]
        slot, memory = self._reg.claim(keys, self._token, path, pid, base=base)
        if memory is False:                                       # another window holds this project
            self._slot = None
            self._pstate = "unbound"
            self.notice.show_notice("open_elsewhere", _("Dieses Projekt ist schon in einem anderen Fenster offen – "
                                                        "hier wird nichts gespeichert."), [("ok", _("Verstanden"))])
            return
        self._slot = slot
        self._pstate = "bound"
        self._seen_written = slot.written_seq
        if memory is not None:                                    # a closing window's save is still running
            self._apply_data(dict(project.to_dict2(memory.content, slot.pid or "", {}, {}, memory.view)))
            self._restore_view(memory.view or {})

    def _restore_view(self, view):
        """F5: the saved playhead and visible span (seconds, so another window width shows the same stretch); a span
        that was "the whole sequence" stays automatic."""
        if not view:
            return
        try:
            span, offset, pos = float(view.get("span")), float(view.get("offset")), float(view.get("pos"))
        except (TypeError, ValueError):
            return
        from . import qt_timeline
        tl = self.timeline
        fit_span = max(1.0, tl.total() + qt_timeline.PAD_END_S)
        if span > 0 and abs(span - fit_span) > project.VIEW_SHARE * fit_span:
            tl.auto_fit = False
            tl.scale = min(qt_timeline.MAX_SCALE, max(qt_timeline.MIN_SCALE, tl._track_width() / span))
            tl.offset = max(0.0, offset)
            tl._clamp_offset()
            tl.viewed.emit()
            tl.update()
        self.goto(min(max(0.0, pos), tl.total()))

    def _view(self) -> dict:
        tl = self.timeline
        return {"pos": round(float(self.pos), 3), "span": round(tl._track_width() / max(tl.scale, 1e-6), 3),
                "offset": round(float(tl.offset), 3)}

    def _offer_local(self):
        """Local copies (4.3/4.5) newer than what was loaded: rescue copies are taken over silently (they are the
        newer state of this project), copies of a deleted project and unsaved states are offered."""
        folder = self._reg.local_folder()
        pid = self._slot.pid if self._slot is not None else None
        key = projectsave.local_key(pid, self.path)
        cands = projectsave.local_candidates(folder, key)
        if not cands:
            return
        seq, art, path = cands[0]
        if self._slot is not None and art == "rettung" and seq > self._slot.written_seq and pid:
            try:
                with open(path, encoding="utf-8") as fh:
                    data = json.load(fh)
            except (OSError, ValueError):
                return
            view = self._apply_data(data)
            if view is not None:
                self._restore_view(view)
                self.status.setText(_("Neuerer Stand aus der lokalen Rettungskopie geladen."))
                self._pdirty = True
                self._changed()
            return
        if art in ("fehlt", "wiederherstellung"):
            self._local_offer = path
            text = _("Ungespeicherte Änderungen von {when} gefunden.", when=_when(os.path.getmtime(path))) \
                if art == "wiederherstellung" else _("Lokal gesicherter Stand eines fehlenden Projekts gefunden.")
            self.notice.show_notice("local", text, [("ignore", _("Ignorieren")), ("restore_local", _("Wiederherstellen"))])

    # ---- the bar's answers
    def _notice_choice(self, key, ident):
        if ident in ("ignore", "ok", "keep", "nothing"):
            if key == "take_over":
                self._pending_take_over = None
                self.status.setText(_("Projekt geöffnet – der Bereich aus der Vorschau wurde nicht übernommen."))
            elif key == "missing":
                self._detach(_("Kein Projekt – Strg+S legt ein neues an."))
            return
        if ident == "new":
            self._lock_editing(False)
            self._start_new()
        elif ident == "load_unverified":
            entries = getattr(self._resolution, "entries", []) or []
            if entries:
                self._load_entry(entries[0], manual=True)
        elif ident == "load_legacy":
            self._load_entry(self._resolution.entries[0], manual=True)
        elif ident.startswith("pick:"):
            i = int(ident.split(":")[1])
            entries = self._resolution.entries
            if 0 <= i < len(entries):
                self._load_entry(entries[i], manual=True)
        elif ident in ("hash_anyway", "rehash"):
            self._hash_progress = 0
            filehash.hasher().request(self.path, lambda r: self.bridge.hash.emit(r),
                                      on_progress=lambda d, t: self.bridge.hash.emit({"kind": "progress", "done": d,
                                                                                       "total": t}),
                                      allow_placeholder=(ident == "hash_anyway"))
        elif ident == "take":
            self._take_over_confirmed()
        elif ident == "restore_local":
            path = getattr(self, "_local_offer", None)
            try:
                with open(path, encoding="utf-8") as fh:
                    data = json.load(fh)
            except (OSError, ValueError, TypeError):
                return
            view = self._apply_data(data)
            if view is not None:
                self._restore_view(view)
                self._pdirty = True
                self._changed()
        elif ident == "restore_file" and self._slot is not None:
            slot = self._slot
            with slot.cv:
                slot.status, slot.reason, slot.base_hash = "saved", "", None
            self._submit(view_event=True, force=True)
        elif ident == "as_new":
            self._detach(None)
            self._pdirty = True
            self._changed()
        elif ident == "close_anyway":
            self._closing_asked = True
            self.close()
        elif ident == "save_close":
            self._submit(view_event=True, force=True, to_project=True)
            self._closing_asked = True
            self.close()

    def _detach(self, message):
        """Leave the current project alone (deleted/foreign/ambiguous): the window goes on without one; the next
        save makes a new project with a new id (``message`` None: at once – the state is worth keeping)."""
        content = project.content_dict(self._state(), self._project_extra())
        self._bind(None, "", base={"baseline_hash": project.content_hash(content) if message else None})
        if message:
            self.status.setText(message)

    def _baseline_moved(self):
        """The window changed its state by itself (black borders found → their crop): no project file for that."""
        slot = self._slot
        if slot is not None and slot.pid is None and not self._pdirty:
            slot.baseline_hash = project.content_hash(project.content_dict(self._state(), self._project_extra()))

    # ---- changes and saving (3.2/3.3)
    def _changed(self):
        if getattr(self, "_ploading", False) or getattr(self, "_applying", False) or self._closed:
            return
        self._pdirty = True
        if not hasattr(self, "_save_timer"):
            return
        self._save_timer.start()
        if not self._max_timer.isActive():
            self._max_timer.start()
        self._status_tick()

    def _gesture_active(self) -> bool:
        pv, tl = self.preview, self.timeline
        if pv.gesture_active() or tl.gesture_active():
            return True
        app = QApplication.instance()
        fw = app.focusWidget() if app is not None else None
        return hasattr(fw, "isSliderDown") and fw.isSliderDown()

    def _save_due(self):
        if self._gesture_active():
            self._save_after_gesture = True
            self._save_timer.start()
            return
        self._save_timer.stop()
        self._max_timer.stop()
        self._submit(view_event=False)

    def _safety_net(self):
        if self._pstate != "bound" or self._gesture_active():
            return
        content = project.content_dict(self._state(), self._project_extra())
        if project.content_hash(content) != self._last_submitted:
            self._submit(view_event=False)

    def _source(self) -> dict:
        rec = self._rec or {}
        src = {"sha256": rec.get("sha256"), "qfp": rec.get("qfp"), "size": rec.get("size"),
               "duration": rec.get("duration"), "file": os.path.basename(self.path), "t": rec.get("t"),
               "path": self.path}
        try:
            src["rel"] = os.path.relpath(self.path, os.path.dirname(self.clips_dir))
        except ValueError:
            src["rel"] = None
        if self._migrated_from:
            src["migrated_from"] = self._migrated_from
        if self._unverified:
            src["verified"] = "user"
            src["verified_at"] = time.time()
        return src

    def _submit(self, view_event: bool, force: bool = False, to_project: bool | None = None):
        """The window's state to its slot (Autosave on, or Strg+S) – or, Autosave off, as a local recovery state."""
        slot = self._slot
        if slot is None or self._pstate != "bound" or self._gesture_active() and not force:
            return
        content = project.content_dict(self._state(), self._project_extra())
        chash = project.content_hash(content)
        to_project = self._autosave if to_project is None else to_project
        if not to_project:
            if chash != slot.disk_content_hash:
                self._local_seq += 1
                job = projectsave.Job(max(self._local_seq, slot.latest_seq + 1), content, self._view(), False,
                                      self._source())
                self._reg.rescue(slot, job, "wiederherstellung")
            self._pdirty = False
            return
        if slot.pid is None:
            if chash == slot.baseline_hash and not force:
                self._pdirty = False
                return
            pid = project.new_id()
            path = os.path.join(self._project_folder(), project.file_name2(self.path, pid))
            self._reg.set_identity(slot, pid, path)
        view = self._view()
        if chash == self._last_submitted and not project.view_differs(view, self._last_view) \
                and source_meta(self._source()) == self._last_meta and (self._last_view_event or not view_event):
            self._pdirty = False                                  # handed over already (focus away twice, quit)
            return None
        seq = self._reg.submit(slot, self._token, content, view=view, view_event=view_event, source=self._source())
        self._last_submitted, self._last_view, self._last_meta = chash, view, source_meta(self._source())
        self._last_view_event = bool(view_event)
        self._pdirty = False
        self._save_after_gesture = False
        self._status_tick()
        return seq

    def save_project(self):
        """Strg+S: the state now (Autosave off: this is the only way into the project file)."""
        if not self.info.ok or self._pstate != "bound":
            return
        self._manual_seq = self._submit(view_event=True, force=True, to_project=True)
        if self._manual_seq:
            self.status.setText(_("Projekt wird gespeichert …"))
        elif self._slot is not None and self._slot.has_file and self._slot.written_seq >= self._slot.latest_seq:
            self.status.setText(_("Projekt gespeichert: {file}", file=os.path.basename(self._slot.path)))

    def project_flush(self):
        """Quit/close: the state now, with the view."""
        if self._pstate == "bound" and self._slot is not None:
            self._submit(view_event=True, force=True)

    def set_autosave(self, on: bool):
        """The setting changed (App): on → a state not in the project yet is saved now."""
        self._autosave = bool(on)
        if self._autosave and self._pstate == "bound":
            self._changed()
        self._status_tick()

    # ---- status (3.9)
    def _status_tick(self):
        if not hasattr(self, "save_status"):
            return
        slot = self._slot
        if self._pstate == "loading":
            text = _("Projekt wird gesucht …")
        elif self._pstate == "verify":
            p = self._hash_progress
            text = _("Prüft Aufnahme … {p} %", p=p) if p is not None else _("Prüft Aufnahme …")
        elif slot is None:
            text = _("Kein Projekt")
        else:
            if slot.written_seq > self._seen_written:
                self._seen_written = slot.written_seq
                self._saved_at = time.time()
                self._library_flag()
            if self._manual_seq and slot.written_seq >= self._manual_seq and slot.status == "saved":
                self._manual_seq = None                           # Strg+S is through: say where it went
                self.status.setText(_("Projekt gespeichert: {file}", file=os.path.basename(slot.path)))
                self.log(_("Projekt gespeichert: {file}", file=slot.path), "System")
            word = projectsave.status_of(slot, dirty=self._pdirty, gesture=self._gesture_active())
            if not self._autosave and word in ("saving",):
                word = "changed"
            text = {
                "readonly": _("Projekt aus neuerer Version – wird nicht überschrieben"),
                "ambiguous": _("⚠ Mehrere Projektdateien – Auswahl nötig"),
                "missing": _("⚠ Projektdatei fehlt – Änderungen nur lokal gesichert"),
                "conflict": _("⚠ Projekt ausserhalb geändert"),
                "error_rescued": _("⚠ Nicht im Projekt gespeichert – lokal gesichert"),
                "error": _("⚠ Nicht gespeichert – {why}", why=slot.reason or "?"),
                "hang": _("⚠ Speichern hängt"),
                "changed": _("● Änderungen"),
                "saving": _("Speichert …"),
                "saved": _("✓ Gespeichert {at}", at=time.strftime("%H:%M", time.localtime(self._saved_at or time.time()))),
                "new": _("Neues Projekt"),
            }.get(word, "")
            self._notice_from_slot(slot)
            if not self._autosave:
                text = _("Autosave aus") + " · " + text
            if self._unverified:
                text += " · " + _("Zuordnung nicht geprüft")
        if self.save_status.text() != text:
            self.save_status.setText(text)

    def _library_flag(self):
        """The library's row of this recording shows its project once a file is written."""
        lib = getattr(self, "library", None)
        it = lib.item_for(self.path) if lib is not None else None
        if it is not None and not it.project and self._slot is not None and self._slot.has_file:
            it.project = True
            lib.view.viewport().update()

    def _notice_from_slot(self, slot):
        if slot.status == "missing" and self.notice.key != "missing":
            if slot.reason == "renamed":
                text = _("Die Projektdatei wurde umbenannt. Dein Stand ist lokal gesichert.")
            else:
                text = _("Die Projektdatei wurde ausserhalb von Fog Scout gelöscht oder verschoben. Dein Stand ist "
                         "lokal gesichert.")
            self.notice.show_notice("missing", text, [("ignore", _("Nicht wiederherstellen")),
                                                      ("restore_file", _("Projekt wiederherstellen")),
                                                      ("as_new", _("Als neues Projekt speichern"))])
        elif slot.status in ("conflict", "ambiguous") and self.notice.key != "conflict":
            self.notice.show_notice("conflict", _("Das Projekt wurde ausserhalb geändert oder liegt doppelt vor. "
                                                  "Deine Fassung liegt unter Sicherungen und lokal."),
                                    [("nothing", _("Nichts tun")), ("as_new", _("Als neues Projekt speichern"))])

    # ---- the hand-over from the compact editor (F1, 6.2)
    def take_over(self, start: float, end: float, pos: float):
        if not self.info.ok:
            return
        if self._pstate in ("loading", "verify"):
            self._pending_take_over = (start, end, pos)
            return
        saved = self._project_loaded or (self._slot is not None and self._slot.pid)
        if saved and self._differs(start, end):
            self._pending_take_over = (start, end, pos)
            self._offer_take_over()
            return
        self._apply_take_over(start, end, pos)

    def _differs(self, start, end) -> bool:
        return not (len(self.parts) == 1 and abs(self.parts[0].start - start) < 0.05
                    and abs(self.parts[0].end - end) < 0.05)

    def _offer_take_over(self):
        start, end, _pos = self._pending_take_over
        if not self._differs(start, end):
            self._pending_take_over = None
            return
        from . import clipedit
        self.notice.show_notice("take_over", _("Für diese Aufnahme gibt es ein gespeichertes Projekt ({n} Clips). "
                                               "Den Bereich aus der Vorschau ({a}–{b}) übernehmen ersetzt seine "
                                               "Clips.", n=len(self.parts), a=clipedit.fmt_pos(start),
                                               b=clipedit.fmt_pos(end)),
                                [("keep", _("Projekt behalten")), ("take", _("Bereich übernehmen"))])

    def _take_over_confirmed(self):
        if self._pending_take_over is None:
            return
        start, end, pos = self._pending_take_over
        self._pending_take_over = None
        slot = self._slot
        if slot is not None and slot.path and os.path.exists(slot.path):
            try:
                with open(slot.path, "rb") as fh:
                    self._reg.submit_fifo(slot, "vor-uebergabe", fh.read())
            except OSError:
                pass
        self._apply_take_over(start, end, pos)
        self.status.setText(_("Bereich übernommen – Strg+Z stellt das Projekt wieder her."))

    # ---- closing (5.2)
    def _project_close_ok(self) -> bool:
        """True when the window may close now; else the bar asks (and the close is ignored)."""
        if self._closing_asked or self._pstate != "bound" or self._slot is None:
            return True
        slot = self._slot
        content = project.content_dict(self._state(), self._project_extra())
        unsaved = project.content_hash(content) != (slot.disk_content_hash if slot.has_file else slot.baseline_hash)
        if not self._autosave and unsaved:
            self.notice.show_notice("close", _("Ungespeicherte Änderungen."),
                                    [("save_close", _("Speichern und schliessen")),
                                     ("close_anyway", _("Verwerfen und schliessen")), ("ignore", _("Abbrechen"))])
            return False
        self.project_flush()
        if slot.status == "error" and slot.rescued_seq < slot.latest_seq and "norescue" in (slot.reason or ""):
            self.notice.show_notice("close", _("Projekt nicht gespeichert und keine Rettungskopie möglich: {why}",
                                               why=slot.reason),
                                    [("ignore", _("Nicht schliessen")), ("close_anyway", _("Trotzdem schliessen"))])
            return False
        return True

    def _project_release(self):
        for t in ("_save_timer", "_max_timer", "_safety", "_status_timer"):
            timer = getattr(self, t, None)
            if timer is not None:
                timer.stop()
        if self._slot is not None:
            self._reg.release(self._slot, self._token)
            self._slot = None
