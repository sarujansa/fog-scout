"""1.18.1: the big editor with the saving core (editorproject + projectsave): autosave, the view, no save during a
drag, close/reopen while a write is slow, the hand-over from the compact editor (F1), old projects only on a click,
ambiguous and deleted project files, Autosave off. Offscreen; skipped without imageio-ffmpeg. Waiting is pumping
until a condition holds – never a time limit on the work (the pump's own limit only ends a hung test)."""
import json
import os
import subprocess
import sys
import threading
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import obsrec, project, projectsave  # noqa: E402

FF = obsrec.ffmpeg_exe()
pytestmark = pytest.mark.skipif(FF is None, reason="imageio-ffmpeg not installed")


@pytest.fixture(scope="module")
def clip(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("edproj") / "2026-10-30 22-10 Badham – Trapper.mkv")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                    "-i", "testsrc=duration=12:size=320x180:rate=30", "-c:v", "libx264", "-preset", "veryfast",
                    "-g", "30", "-pix_fmt", "yuv420p", path], check=True, timeout=120)
    return path


@pytest.fixture
def qapp():
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_window
    return qt_window.application()


@pytest.fixture
def reg(tmp_path):
    r = projectsave.Registry(data_dir=str(tmp_path / "local"), sleep=lambda s: None)
    yield r
    r.wait_idle(10)
    r.stop()


def _pump(app, until=lambda: False, seconds=60):
    deadline = time.time() + seconds
    while time.time() < deadline and not until():
        app.processEvents()
        time.sleep(0.01)
    return until()


def _window(app, clip, tmp_path, reg, size=(1400, 860), **kw):
    from fogscout import qt_editor
    win = qt_editor.EditorWindow(clip, [], str(tmp_path / "Clips"), sound=False, registry=reg, **kw)
    win.resize(*size)
    win.show()
    assert _pump(app, lambda: win.preview._img is not None and (win.loading is None or win.loading.finished)
                 and win._pstate != "loading")
    return win


def _folder(tmp_path):
    return str(tmp_path / "Clips" / project.PROJECT_DIR)


def _files(tmp_path):
    try:
        return sorted(n for n in os.listdir(_folder(tmp_path)) if n.endswith(project.EXT))
    except OSError:
        return []


def _read(path):
    with open(path, "rb") as fh:
        return fh.read()


def _idle(app, win):
    """The window's newest state is on disk (or nothing was due) and the hash is known."""
    slot = win._slot
    return _pump(app, lambda: slot is not None and not win._pdirty and slot.pending is None and slot.in_flight is None
                 and slot.written_seq >= slot.latest_seq and (win._rec or {}).get("sha256"))


def _cut(win, at=3.0):
    win.goto(at)
    win.split_at_playhead()


def _close(app, win):
    win.close()
    _pump(app, lambda: False, 0.05)


def test_a_change_is_saved_by_itself_and_only_looking_writes_nothing(qapp, clip, tmp_path, reg):
    win = _window(qapp, clip, tmp_path, reg)
    try:
        assert _idle(qapp, win)
        win.goto(5.0)                                                     # looking around is no change
        win._safety_net()
        win._save_due()
        assert reg.wait_idle(30) and _files(tmp_path) == []
        assert win.save_status.text() == "Neues Projekt"
        _cut(win)
        assert win._pdirty and win._save_timer.isActive()                # 1.5 s after the last change
        assert _pump(qapp, lambda: len(_files(tmp_path)) == 1) and _idle(qapp, win)
        data = json.loads(_read(os.path.join(_folder(tmp_path), _files(tmp_path)[0])))
        assert data["version"] == project.CURRENT and len(data["parts"]) == 2
        assert data["source"]["sha256"] == win._rec["sha256"] and data["source"]["size"] == os.path.getsize(clip)
        assert _pump(qapp, lambda: win.save_status.text().startswith("✓"))
        n = len(win._slot.written)
        for t in (1.0, 2.0, 7.0):                                        # seeks: no write
            win.goto(t)
            win._safety_net()
        assert reg.wait_idle(30) and len(win._slot.written) == n
    finally:
        _close(qapp, win)


def test_the_view_is_saved_on_close_and_comes_back(qapp, clip, tmp_path, reg):
    win = _window(qapp, clip, tmp_path, reg)
    try:
        _cut(win)
        win.save_project()
        assert _idle(qapp, win)
        win.timeline.zoom(4.0)
        win.goto(6.5)
        view = win._view()
    finally:
        _close(qapp, win)
    assert reg.wait_idle(30)
    path = os.path.join(_folder(tmp_path), _files(tmp_path)[0])
    saved = json.loads(_read(path))["view"]
    assert saved["pos"] == pytest.approx(6.5, abs=0.05) and saved["span"] == pytest.approx(view["span"], rel=0.01)
    again = _window(qapp, clip, tmp_path, reg, size=(1100, 860))    # another width: the same stretch in seconds
    try:
        assert _pump(qapp, lambda: again._project_loaded)
        assert again.pos == pytest.approx(6.5, abs=0.05) and not again.timeline.auto_fit
        span = again.timeline._track_width() / again.timeline.scale
        assert span == pytest.approx(view["span"], rel=0.05)
    finally:
        _close(qapp, again)


def test_nothing_is_saved_during_a_drag_and_once_after_it(qapp, clip, tmp_path, reg):
    win = _window(qapp, clip, tmp_path, reg)
    try:
        _cut(win)
        win.save_project()
        assert _idle(qapp, win)
        before = win._slot.latest_seq
        dragging = [True]
        win.preview.gesture_active = lambda: dragging[0]
        _cut(win, 6.0)                                                  # a change made while a drag is under way
        win._save_due()
        win._safety_net()
        win._submit(view_event=True)
        assert win._slot.latest_seq == before and win._save_after_gesture
        win._status_tick()
        assert win.save_status.text().startswith("●")                  # „Änderungen“ while the drag lasts
        dragging[0] = False                                             # released: one job
        win._save_due()
        assert win._slot.latest_seq == before + 1 and _idle(qapp, win)
    finally:
        _close(qapp, win)


def test_closing_while_the_writer_hangs_and_opening_again_keeps_the_newer_state(qapp, clip, tmp_path):
    """Point 3 with real windows: W1 closes while its write is held, W2 opens at once – it starts from the slot's
    newest state, never from the older file; the file ends as W2 left it."""
    gate, reached = threading.Event(), threading.Event()
    reg = projectsave.Registry(data_dir=str(tmp_path / "local"), sleep=lambda s: None)
    w1 = _window(qapp, clip, tmp_path, reg)
    try:
        _cut(w1)
        w1.save_project()
        assert _idle(qapp, w1)

        def hook(slot, n):
            if n == 0 and not gate.is_set():
                reached.set()
                gate.wait(60)
        reg.hook = hook
        _cut(w1, 8.0)                                                   # three clips now
        w1.save_project()
        assert reached.wait(60)
    finally:
        _close(qapp, w1)
    w2 = _window(qapp, clip, tmp_path, reg)
    try:
        assert _pump(qapp, lambda: w2._slot is not None and w2._project_loaded)
        assert len(w2.parts) == 3                                        # the newer state, not the file's two clips
        _cut(w2, 10.0)
        w2.save_project()
        gate.set()
        assert _idle(qapp, w2) and reg.wait_idle(30)
        data = json.loads(_read(os.path.join(_folder(tmp_path), _files(tmp_path)[0])))
        assert len(data["parts"]) == 4 and len(_files(tmp_path)) == 1
    finally:
        gate.set()
        _close(qapp, w2)
        reg.wait_idle(10)
        reg.stop()


def test_the_hand_over_asks_before_it_replaces_a_saved_project(qapp, clip, tmp_path, reg):
    """F1: the compact editor's range over a saved project with other clips – the bar asks, the file stays byte for
    byte until „Bereich übernehmen“, the old state is kept as a backup, Strg+Z brings it back."""
    win = _window(qapp, clip, tmp_path, reg)
    try:
        _cut(win)
        win.save_project()
        assert _idle(qapp, win)
    finally:
        _close(qapp, win)
    assert reg.wait_idle(30)
    path = os.path.join(_folder(tmp_path), _files(tmp_path)[0])
    before = _read(path)
    again = _window(qapp, clip, tmp_path, reg)
    try:
        assert _pump(qapp, lambda: again._project_loaded)
        again.take_over(1.0, 5.0, 2.0)
        assert again.notice.key == "take_over" and len(again.parts) == 2
        assert reg.wait_idle(30) and _read(path) == before
        again.notice.choose("keep")
        assert len(again.parts) == 2 and _read(path) == before
        again.take_over(1.0, 5.0, 2.0)
        again.notice.choose("take")
        assert [(round(p.start, 1), round(p.end, 1)) for p in again.parts] == [(1.0, 5.0)]
        assert _idle(qapp, again)
        backups = os.listdir(projectsave.backup_folder(path))
        assert any("-vor-uebergabe-" in n for n in backups)
        again.undo()
        assert len(again.parts) == 2
    finally:
        _close(qapp, again)


def test_an_old_project_is_loaded_only_on_a_click_and_its_file_stays(qapp, clip, tmp_path, reg):
    from fogscout import annotate, clipedit, sequence
    old = project.project_path(str(tmp_path / "Clips"), clip)
    state = sequence.EditState([clipedit.Part(1.0, 4.0), clipedit.Part(6.0, 9.0)], None, "none",
                               [annotate.Shape("arrow", [(0.1, 0.1), (0.3, 0.3)])], 0.0, 0.0, [], False, "pixel")
    assert project.save(old, project.to_dict(state, clip, "Alt", {}))
    raw = _read(old)
    win = _window(qapp, clip, tmp_path, reg)
    try:
        assert win.notice.key == "legacy" and len(win.parts) == 1        # not loaded by itself
        assert win.notice.isVisible()
        win._escape()                                                    # Esc never answers the bar
        assert win.notice.key == "legacy"
        win.notice.choose("load_legacy")
        assert len(win.parts) == 2 and len(win.preview.shapes) == 1 and win.name_edit.text() == "Alt"
        assert _pump(qapp, lambda: len(_files(tmp_path)) == 2) and _idle(qapp, win)
        new = [n for n in _files(tmp_path) if "--" in n]
        data = json.loads(_read(os.path.join(_folder(tmp_path), new[0])))
        assert data["source"]["migrated_from"] == os.path.basename(old) and data["source"]["verified"] == "user"
        assert _read(old) == raw                                         # the old file byte for byte
        assert "Zuordnung nicht geprüft" in win.save_status.text()
    finally:
        _close(qapp, win)


def test_two_project_files_of_the_recording_open_none(qapp, clip, tmp_path, reg):
    win = _window(qapp, clip, tmp_path, reg)
    try:
        _cut(win)
        win.save_project()
        assert _idle(qapp, win)
    finally:
        _close(qapp, win)
    assert reg.wait_idle(30)
    first = os.path.join(_folder(tmp_path), _files(tmp_path)[0])
    data = json.loads(_read(first))
    data["id"] = project.new_id()
    data["parts"] = [[0.0, 2.0, 1.0]]
    with open(os.path.join(_folder(tmp_path), project.file_name2(clip, data["id"])), "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    again = _window(qapp, clip, tmp_path, reg)
    try:
        assert again.notice.key == "ambiguous" and len(again.parts) == 1 and not again._project_loaded
        assert "pick" in again.notice.buttons and again.notice.buttons["pick"].menu() is not None
        again.notice.choose("pick:1")
        assert again._project_loaded and len(again.parts) in (1, 2)
    finally:
        _close(qapp, again)


def test_a_deleted_project_file_is_never_made_again(qapp, clip, tmp_path, reg):
    win = _window(qapp, clip, tmp_path, reg)
    try:
        _cut(win)
        win.save_project()
        assert _idle(qapp, win)
        path = win._slot.path
        os.remove(path)                                                  # deleted outside Fog Scout
        _cut(win, 8.0)
        win.save_project()
        assert _pump(qapp, lambda: win._slot.status == "missing" and win.notice.key == "missing")
        assert reg.wait_idle(30) and not os.path.exists(path)
        local = os.listdir(str(tmp_path / "local"))
        assert any(".fehlt." in n for n in local)
        assert "fehlt" in win.save_status.text()
        win.notice.choose("ignore")                                      # „Nicht wiederherstellen“: no project now
        assert win._slot is not None and win._slot.pid is None and not os.path.exists(path)
    finally:
        _close(qapp, win)


def test_with_autosave_off_only_a_local_state_is_kept_and_closing_asks(qapp, clip, tmp_path, reg):
    win = _window(qapp, clip, tmp_path, reg, autosave=False)
    try:
        assert _idle(qapp, win)
        _cut(win)
        win._save_due()
        assert reg.wait_idle(30) and _files(tmp_path) == []
        assert any(".wiederherstellung." in n for n in os.listdir(str(tmp_path / "local")))
        assert win.save_status.text().startswith("Autosave aus")
        win.close()
        assert win.isVisible() and win.notice.key == "close"             # asked, not closed
        assert list(win.notice.buttons) == ["save_close", "close_anyway", "ignore"]
        win.notice.choose("ignore")
        assert win.isVisible()
        win.save_project()                                               # Strg+S writes the project
        assert _idle(qapp, win) and len(_files(tmp_path)) == 1
        win.close()
        assert not win.isVisible() or win._closed
    finally:
        if win.isVisible():
            win._closing_asked = True
            _close(qapp, win)


# ---- the App: quitting in two phases, the update, the setting (C5)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def app_root(tmp_path, monkeypatch):
    if sys.platform == "win32":
        pytest.skip("Linux: the Windows job tests the native parts; the app would touch the system there")
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    for name in ("maps", "models", "maps.json"):
        os.symlink(os.path.join(ROOT, name), tmp_path / name)
    (tmp_path / "sim").mkdir()
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "home"))
    return tmp_path


def _held(monkeypatch):
    """The program's registry with its writer and its rescue copies held until ``gate`` is set."""
    gate = threading.Event()
    reg = projectsave.registry()
    reg.hook = lambda slot, n: gate.wait(60) if n == 0 else None
    real = projectsave.Registry.rescue_now

    def slow(self, *a, **k):
        gate.wait(60)
        return real(self, *a, **k)
    monkeypatch.setattr(projectsave.Registry, "rescue_now", slow)
    return gate, reg


def _app_editor(app, clip, tmp_path):
    from fogscout import qt_editor
    win = qt_editor.EditorWindow(clip, [], str(tmp_path / "Clips"), sound=False)
    win.resize(1400, 860)
    win.show()
    assert _pump(app.root.qapp, lambda: win.preview._img is not None and win._pstate != "loading")
    app._clip_windows.append(win)
    return win


def test_quitting_waits_until_the_editor_states_are_safe_and_never_ends_with_one_unsaved(app_root, clip, tmp_path,
                                                                                         monkeypatch):
    from fogscout import app as app_mod
    from fogscout.app import App
    timers = []
    real_timer = threading.Timer
    monkeypatch.setattr(app_mod.threading, "Timer", lambda *a, **k: timers.append(a) or real_timer(3600, lambda: None))
    gate, reg = _held(monkeypatch)
    app = App(str(app_root), simulate=str(app_root / "sim"))
    app.exit_watchdog = True
    win = None
    try:
        qapp = app.root.qapp
        win = _app_editor(app, clip, tmp_path)
        _cut(win)
        app.quit()
        assert not app._quitting and timers == []                     # phase 1: no watchdog, no os._exit yet
        assert reg.unsecured() and win._closing_asked
        from fogscout import app_recordings
        app._secure_since = time.monotonic() - app_recordings.SECURE_ASK_S - 1     # as if it hung for long
        assert _pump(qapp, lambda: app.qt.message.isVisible(), 10)
        assert app._qt_question[0] == "Editor-Projekte nicht gesichert" and not app._quitting
        app.qt.message.cancel.click()                                 # Cancel: the program runs on
        assert _pump(qapp, lambda: app._qt_question is None) and not app._quitting
        assert not app.qt.message.isVisible()
        gate.set()                                                    # the disk is back
        app.quit()                                                    # quitting again: secured, then it ends
        assert _pump(qapp, lambda: app._quitting) and len(timers) == 1
        assert not reg.unsecured()
    finally:
        gate.set()
        if win is not None and not app._quitting:
            win._closing_asked = True
            win.close()
        app.quit()


def test_going_on_without_saving_is_the_users_choice(app_root, clip, tmp_path, monkeypatch):
    from fogscout import app_recordings
    from fogscout.app import App
    gate, reg = _held(monkeypatch)
    app = App(str(app_root), simulate=str(app_root / "sim"))
    try:
        qapp = app.root.qapp
        win = _app_editor(app, clip, tmp_path)
        _cut(win)
        app.quit()
        app._secure_since = time.monotonic() - app_recordings.SECURE_ASK_S - 1
        assert _pump(qapp, lambda: app.qt.message.isVisible(), 10)
        app.qt.message.ok.click()                                     # OK: end without those states
        assert _pump(qapp, lambda: app._quitting) and not app.qt.message.isVisible()
    finally:
        gate.set()
        app.quit()


def test_an_update_waits_for_the_editor_states(app_root, clip, tmp_path, monkeypatch):
    from fogscout import restart
    from fogscout.app import App
    spawned = []
    monkeypatch.setattr(restart, "spawn_helper", lambda root: spawned.append(root) or False)
    gate, reg = _held(monkeypatch)
    app = App(str(app_root), simulate=str(app_root / "sim"))
    win = None
    try:
        qapp = app.root.qapp
        win = _app_editor(app, clip, tmp_path)
        _cut(win)
        app.apply_update()
        assert spawned == [] and "Update wartet" in app.upd_status.get()
        gate.set()
        assert _pump(qapp, lambda: spawned == [str(app_root)])         # secured: the update goes on by itself
    finally:
        gate.set()
        if win is not None:
            win._closing_asked = True
            win.close()
        app.quit()


def test_the_autosave_setting_reaches_the_open_editors(app_root, clip, tmp_path):
    from fogscout.app import App
    app = App(str(app_root), simulate=str(app_root / "sim"))
    win = None
    try:
        win = _app_editor(app, clip, tmp_path)
        assert win._autosave
        app.editor_autosave_var.set(False)
        app._editor_autosave_changed()
        assert not win._autosave and app.settings.get("editor_autosave") is False
        assert win.save_status.text().startswith("Autosave aus")
        app.editor_autosave_var.set(True)
        app._editor_autosave_changed()
        assert win._autosave and app.settings.get("editor_autosave") is True
    finally:
        if win is not None:
            win.close()
        app.quit()
