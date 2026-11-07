"""The editor window of 1.16 (qt_editor, qt_timeline, qt_library, qt_icons): the timeline's mouse work – select,
trim, move, split, delete – changes the clips and the undo history, playback follows the sequence's clocks,
projects come back, the library opens and drops media, the icons draw. Offscreen; skipped without imageio-ffmpeg."""
import os
import subprocess
import sys
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import obsrec  # noqa: E402

FF = obsrec.ffmpeg_exe()
pytestmark = pytest.mark.skipif(FF is None, reason="imageio-ffmpeg not installed")


@pytest.fixture(scope="module")
def clip(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("editor") / "2026-10-17 21-40 Coal Tower – Nurse.mkv")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                    "-i", "testsrc=duration=12:size=320x180:rate=30", "-f", "lavfi", "-i", "sine=frequency=440:duration=12",
                    "-c:v", "libx264", "-preset", "veryfast", "-g", "30", "-pix_fmt", "yuv420p", "-c:a", "aac",
                    "-shortest", path], check=True, timeout=120)
    return path


@pytest.fixture
def qapp():
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_window
    return qt_window.application()


@pytest.fixture(autouse=True)
def _no_save_left():
    yield
    qt_clip = sys.modules.get("fogscout.qt_clip")
    if qt_clip is not None and getattr(qt_clip, "_SAVES", None):
        qt_clip.stop_saves(wait=5)
        qt_clip._SAVES.clear()


def _pump(app, until=lambda: False, seconds=30):
    deadline = time.time() + seconds
    while time.time() < deadline and not until():
        app.processEvents()
        time.sleep(0.01)
    return until()


def _window(app, clip, tmp_path, **kw):
    from fogscout import qt_editor
    win = qt_editor.EditorWindow(clip, kw.pop("marks", []), str(tmp_path / "Clips"), sound=False, **kw)
    win.resize(1400, 860)
    win.show()
    assert _pump(app, lambda: win.preview._img is not None and (win.loading is None or win.loading.finished)
                 and win._pstate != "loading")                     # 1.18.1: the project lookup is through
    return win


def _mouse(w, kind, x, y, button=None):
    from PySide6.QtCore import QPointF, Qt
    from PySide6.QtGui import QMouseEvent
    button = Qt.LeftButton if button is None else button
    pt = QPointF(x, y)
    types = {"press": QMouseEvent.Type.MouseButtonPress, "move": QMouseEvent.Type.MouseMove,
             "release": QMouseEvent.Type.MouseButtonRelease}
    ev = QMouseEvent(types[kind], pt, w.mapToGlobal(pt), button, button if kind != "move" else Qt.LeftButton,
                     Qt.NoModifier)
    {"press": w.mousePressEvent, "move": w.mouseMoveEvent, "release": w.mouseReleaseEvent}[kind](ev)


def test_the_timeline_selects_trims_moves_splits_and_deletes_with_undo(qapp, clip, tmp_path):
    """The mouse on the tracks: a click marks a clip, its edge trims it (the sequence re-flows), the body dragged
    far enough moves it before or after another clip, S splits at the playhead, Entf removes – every step one
    undo step, the plan for ffmpeg follows the play order."""
    from fogscout import sequence
    win = _window(qapp, clip, tmp_path)
    tl = win.timeline
    try:
        _pump(qapp, seconds=0.3)
        assert [(p.start, round(p.end, 1)) for p in win.parts] == [(0.0, 12.0)] and tl.total() == pytest.approx(12.0, abs=0.1)
        win.goto(4.0)
        win.split_at_playhead()
        win.goto(8.0)
        win.split_at_playhead()
        assert [(round(p.start, 1), round(p.end, 1)) for p in win.parts] == [(0.0, 4.0), (4.0, 8.0), (8.0, 12.0)]
        assert win.history.can_undo() and tl.selection == 2
        # a click on the first clip's body marks it
        r0 = tl.clip_rect(0)
        _mouse(tl, "press", r0.center().x(), r0.center().y())
        _mouse(tl, "release", r0.center().x(), r0.center().y())
        assert tl.selection == 0 and win.sections["clip"].isVisibleTo(win) and "Clip 1 von 3" in win.clip_title.text()
        # the right edge of clip 1 dragged left by 2 s: the clip ends at 2 s, the others move up
        px = tl.scale
        x_edge = tl.clip_rect(0).right()
        _mouse(tl, "press", x_edge - 1, r0.center().y())
        _mouse(tl, "move", x_edge - 2 * px, r0.center().y())
        _mouse(tl, "release", x_edge - 2 * px, r0.center().y())
        assert win.parts[0].end == pytest.approx(2.0, abs=0.15) and tl.total() == pytest.approx(10.0, abs=0.2)
        assert sequence.starts(win.parts)[1] == pytest.approx(win.parts[0].end, abs=1e-6)
        # the last clip dragged to the front
        r2 = tl.clip_rect(2)
        _mouse(tl, "press", r2.center().x(), r2.center().y())
        _mouse(tl, "move", r2.center().x() - 20, r2.center().y())
        _mouse(tl, "move", tl.clip_rect(0).left() + 2, r2.center().y())
        assert tl._drag is not None and tl._drag[0] == "move"
        _mouse(tl, "release", tl.clip_rect(0).left() + 2, r2.center().y())
        assert [round(p.start, 1) for p in win.parts] == [8.0, 0.0, 4.0] and tl.selection == 0
        plan = win.edit_plan()
        assert [round(p.start, 1) for p in plan.parts] == [8.0, 0.0, 4.0]          # the play order, not the source order
        # delete the marked (moved) clip, then undo everything step by step
        win.delete_selected()
        assert [round(p.start, 1) for p in win.parts] == [0.0, 4.0]
        win.undo()
        assert [round(p.start, 1) for p in win.parts] == [8.0, 0.0, 4.0]
        win.undo()
        assert [round(p.start, 1) for p in win.parts] == [0.0, 4.0, 8.0]
        win.undo()
        assert win.parts[0].end == pytest.approx(4.0, abs=1e-6)                       # the trim
        win.redo()
        assert win.parts[0].end == pytest.approx(2.0, abs=0.15)
        # the keys: I/O trim the clip under the playhead, S splits, Entf deletes the marked one
        win.goto(5.0)
        win.set_start()                                                              # clip 2 (4–8) begins at 7 s
        assert win.parts[1].start == pytest.approx(7.0, abs=0.05) and win.pos == pytest.approx(2.0, abs=0.15)
        win.goto(0.5)
        win.set_end()
        assert win.parts[0].end == pytest.approx(0.5, abs=0.05)
        assert win.size_label.text() and "Abschnitt" in win.size_label.text()         # several parts: re-encoded
    finally:
        win.close()


def test_playback_runs_through_the_clips_in_play_order_and_at_their_tempo(qapp, clip, tmp_path):
    """Space from the playhead: the clip under it to its end, then the next ones – each at its tempo (a ×4 clip
    takes a quarter of its source time); the playhead moves in output time and ends at the sequence's end."""
    from fogscout import clipedit
    win = _window(qapp, clip, tmp_path)
    try:
        win.parts = [clipedit.Part(8.0, 10.0), clipedit.Part(0.0, 4.0, 4.0)]      # 2 s + 1 s of output
        win.timeline.set_parts(win.parts)
        win._commit()
        win.goto(0.0)
        assert win.preview.now == pytest.approx(8.0) and win.pos == 0.0
        win.goto(2.5)
        assert win.preview.now == pytest.approx(2.0)                          # 0.5 s into the ×4 clip = 2 s of source
        win.goto(0.0)
        seen = []
        orig = win._played_at

        def spy(t):
            orig(t)
            seen.append((win._seg[0], round(win.pos, 2)))
        win._played_at = spy
        t0 = time.monotonic()
        win.toggle_play()
        assert win.playing
        assert _pump(qapp, lambda: not win.playing, 25)
        took = time.monotonic() - t0
        assert took < 8.0, took                                               # 3 s of output, not 6 s of source
        starts = [s for s, _p in seen]
        assert 8.0 in starts and 0.0 in starts and starts.index(8.0) < starts.index(0.0)
        assert max(p for _s, p in seen) <= 3.05 and win.pos == pytest.approx(win.timeline.total(), abs=0.2)
    finally:
        win.close()


def test_a_project_is_saved_and_comes_back_when_the_recording_opens_again(qapp, clip, tmp_path):
    from fogscout import annotate, project
    win = _window(qapp, clip, tmp_path)
    try:
        win.goto(3.0)
        win.split_at_playhead()
        win.timeline.select(1)
        win.speed_box.setCurrentIndex(win.speed_box.findData(2.0))
        win.preview._new_shape(annotate.Shape("arrow", [(0.2, 0.2), (0.5, 0.5)]))
        win.fade_out_box.setCurrentIndex(win.fade_out_box.findData(1.0))
        win.name_edit.setText("Nurse Doppel-Blink")
        win.name_edit.setModified(True)
        win.save_project()                                                    # 1.18.1: format 2 through projectsave
        slot = win._slot
        assert _pump(qapp, lambda: slot.has_file and slot.written_seq >= slot.latest_seq
                     and (win._rec or {}).get("sha256") and slot.disk_meta and slot.disk_meta[0])
        folder = str(tmp_path / "Clips" / project.PROJECT_DIR)
        names = [n for n in os.listdir(folder) if n.endswith(project.EXT)]
        assert names == [project.file_name2(clip, slot.pid)]
        assert not os.path.exists(project.project_path(str(tmp_path / "Clips"), clip))     # never format 1 again
        assert _pump(qapp, lambda: win.save_status.text().startswith("✓"))
        assert win.library.item_for(clip) is None                              # no App list here: nothing to flag
    finally:
        win.close()
    again = _window(qapp, clip, tmp_path)
    try:
        assert _pump(qapp, lambda: again._project_loaded)
        assert [(round(p.start, 1), round(p.end, 1), p.speed) for p in again.parts] == [(0.0, 3.0, 1.0), (3.0, 12.0, 2.0)]
        assert len(again.preview.shapes) == 1 and again.fade_out_box.currentData() == 1.0
        assert again.name_edit.text() == "Nurse Doppel-Blink" and "Projekt geladen" in again.status.text()
        assert not again.history.can_undo()                                    # the loaded state is the start
        plan = again.edit_plan()
        assert plan.fade_out == 1.0 and len(plan.parts) == 2 and plan.parts[1].speed == 2.0
    finally:
        again.close()


def test_the_library_lists_media_and_opens_a_row(qapp, clip, tmp_path):
    """The library shows the App's items with search and sort, a row carries its path when dragged, opening a row
    (double click) asks the App to open it – in place of this window while nothing was cut here, else beside it;
    an unknown video file dropped from outside joins the library first. 1.22: a drop on V1 joins the timeline
    (montage – tests/test_montage.py)."""
    from PySide6.QtCore import QMimeData
    from fogscout import medialib, qt_timeline
    other = str(tmp_path / "other.mkv")
    with open(other, "wb") as f:
        f.write(b"\0" * 100)
    items = [medialib.MediaItem(clip, "Coal Tower · Nurse", "round", time.time(), 12.0, 100, [2.0]),
             medialib.MediaItem(other, "Ormond · Wraith", "round", time.time() - 10, 600.0, 200)]
    opened = []
    win = _window(qapp, clip, tmp_path, media=lambda: items, on_open=lambda it, rep: opened.append((it.path, rep)))
    try:
        lib = win.library
        assert lib.model.rowCount() == 2 and lib.model.items[0].path == clip      # newest first, the open one flagged
        assert lib.model.current == os.path.normcase(os.path.abspath(clip))
        lib.search.setText("ormond")
        assert [it.path for it in lib.model.items] == [other]
        lib.search.setText("")
        lib.sort_box.setCurrentIndex(lib.sort_box.findData("long"))
        assert [it.path for it in lib.model.items] == [other, clip]
        mime = lib.model.mimeData([lib.model.index(0, 0)])
        assert qt_timeline.SequenceTimeline.mime_path(mime) == other
        win._open_media(lib.item_for(other))                                 # pristine: replaces this window
        assert opened == [(other, win)]
        win._open_media(lib.item_for(clip))                                  # the one open already: nothing
        assert len(opened) == 1 and "schon auf der Zeitleiste" in win.status.text()
        win.goto(4.0)
        win.split_at_playhead()                                               # cut here: a window of its own
        win._open_media(lib.item_for(other))
        assert opened[-1] == (other, None)
        new = str(tmp_path / "fresh.mp4")
        with open(new, "wb") as f:
            f.write(b"\0" * 100)
        win.timeline.dropped.emit(new)                                        # 1.22: joins the library and is read
        assert lib.item_for(new) is not None and lib.item_for(new).kind == "file" and len(opened) == 2
        assert _pump(qapp, lambda: "nicht lesbar" in win.status.text(), 20) and not win._montage
        win.timeline.dropped.emit(str(tmp_path / "notes.txt"))
        assert "Keine Videodatei" in win.status.text()
        mm = QMimeData()
        mm.setText("x")
        assert qt_timeline.SequenceTimeline.mime_path(mm) == ""
        assert _pump(qapp, lambda: clip in lib.model.thumbs, 20)              # the picture of the recording came
        assert not lib.model.thumbs[clip].isNull()
    finally:
        win.close()


def test_the_timeline_zooms_scrolls_and_maps_marks(qapp, clip, tmp_path):
    from fogscout import clipedit, sequence
    win = _window(qapp, clip, tmp_path, marks=[5.0])
    tl = win.timeline
    try:
        _pump(qapp, seconds=0.2)
        fit = tl.scale
        assert tl.auto_fit and tl.offset == 0.0 and tl._x(tl.total()) <= tl.width()
        tl.zoom_in()
        assert tl.scale > fit and not tl.auto_fit
        tl.zoom_in()
        tl.zoom_in()
        win.goto(tl.total())
        assert tl.offset > 0 and tl._x(win.pos) <= tl.width()                  # scrolled to keep the playhead in view
        assert win.tl_scroll.maximum() > 0 and abs(win.tl_scroll.value() / 1000 - tl.offset) < 0.01
        win.tl_scroll.setValue(0)
        assert tl.offset == 0.0
        tl.zoom_fit()
        assert tl.auto_fit and tl.scale == pytest.approx(fit, rel=0.01)
        win.parts = [clipedit.Part(2.0, 8.0), clipedit.Part(4.0, 6.0, 2.0)]   # 5 s used twice
        tl.set_parts(win.parts)
        assert sequence.occurrences(win.parts, 5.0) == pytest.approx([3.0, 6.5])
        step, minor = sequence.ruler_step(tl.scale)
        assert step * tl.scale >= sequence.LABEL_GAP_PX and minor >= 2
        win.resize(1000, 700)
        _pump(qapp, seconds=0.2)
        assert tl._x(tl.total()) <= tl.width()                                   # auto fit follows the size
    finally:
        win.close()


def test_every_icon_draws_something_in_every_state(qapp):
    from PySide6.QtGui import QIcon
    from fogscout import qt_icons
    for name in qt_icons.GLYPHS:
        pm = qt_icons.pixmap(name, "#ffffff", 20, 2.0)
        img = pm.toImage()
        assert pm.width() == 40 and any(img.pixelColor(x, y).alpha() > 0 for x in range(0, 40, 3) for y in range(0, 40, 3)), name
        ic = qt_icons.icon(name, "#e3e5e8", "#ffffff", "#666666", "#1a1406")
        assert not ic.pixmap(20, QIcon.Disabled, QIcon.Off).isNull() and not ic.pixmap(20, QIcon.Normal, QIcon.On).isNull()
    assert qt_icons.pixmap("no-such-glyph", "#ffffff", 20).toImage().pixelColor(10, 10).alpha() == 0


def test_the_timeline_keeps_a_layer_while_only_the_playhead_moves_and_a_closed_editor_lets_go(qapp, clip, tmp_path):
    """1.16.1 (audit, measured 9.9 → 0.8 ms per repaint): moving the playhead reuses the pixmap of the tracks; any
    change of the clips, zoom or selection draws a new one. A closed editor drops its pictures, strip and
    library and stops its pump – it kept ~28 MB each time before."""
    from PySide6.QtGui import QImage
    from fogscout import qt_clip
    win = _window(qapp, clip, tmp_path)
    tl = win.timeline
    try:
        _pump(qapp, lambda: tl._layer is not None, 10)
        img = QImage(tl.size(), QImage.Format_ARGB32)
        tl.render(img)
        layer = tl._layer
        win.goto(3.0)
        tl.render(img)
        assert tl._layer is layer                                 # the playhead moved: the same layer
        tl.zoom_in()
        tl.render(img)
        assert tl._layer is not layer                             # the zoom changed: a new one
        layer = tl._layer
        win.goto(4.0)
        win.split_at_playhead()
        tl.render(img)
        assert tl._layer is not layer                             # the clips changed: a new one
        assert win.preview._img is not None and tl.thumbs
        pump = win._pump
        win.close()
        assert win._closed and pump.interval() == qt_clip.CLOSED_PUMP_MS   # 15 ms → 200 ms until the object goes
        assert win.preview._img is None and tl.thumbs == {} and tl.wave == [] and tl._layer is None
        assert set(win.bridge.handlers) <= set(win.bridge.AFTER_CLOSE)
        assert win.library.model.rowCount() == 0
    finally:
        if not win._closed:
            win.close()


def _gone(app, seconds=3):
    """Pump events, the deferred deletions included (WA_DeleteOnClose; processEvents alone may leave them queued)."""
    from PySide6.QtCore import QCoreApplication, QEvent
    deadline = time.time() + seconds
    while time.time() < deadline:
        app.processEvents()
        QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
        time.sleep(0.01)


def test_a_closed_editor_is_freed_and_one_still_saving_only_after_its_save(qapp, clip, tmp_path, monkeypatch):
    """1.38.5 (measured during 1.38.3): a closed editor stayed in memory until Fog Scout quit. The "Ton" box is never
    shown in the big editor (the mute button stands for it) and had no Qt parent: its C++ object outlived the window,
    and its two lambdas held the window. A save still running keeps the window until its result is handed over."""
    import gc
    import threading
    import weakref
    from fogscout import qt_clip
    win = _window(qapp, clip, tmp_path)
    win.mute_btn.click()                                     # every kind of slot the window connects, used once
    win.mute_btn.click()
    win.goto(3.0)
    win.split_at_playhead()
    win.volume.setValue(60)
    win.close()
    _gone(qapp)
    ref = weakref.ref(win)
    win = None
    gc.collect()
    assert ref() is None

    saved = []
    win = _window(qapp, clip, tmp_path, on_saved=saved.append)
    gate = threading.Event()
    real_run = qt_clip._SaveJob.run

    def slow_run(job, args):
        gate.wait(30)
        return real_run(job, args)
    monkeypatch.setattr(qt_clip._SaveJob, "run", slow_run)
    win.save()
    win.close()                                              # closed while ffmpeg still writes the clip
    _gone(qapp, 0.5)
    ref = weakref.ref(win)
    win = None
    gc.collect()
    assert ref() is not None                                 # kept until the save is picked up …
    gate.set()
    assert _pump(qapp, lambda: saved, 60)                    # … through _drain_closed, so the App still hears of it
    assert len(saved) == 1 and os.path.getsize(saved[0]) > 0 and not qt_clip._SAVES
    _gone(qapp, 0.5)
    gc.collect()
    assert ref() is None


def test_closing_the_editor_while_it_analyses_ends_its_threads_and_ffmpeg(qapp, clip, tmp_path, monkeypatch):
    """Post-review 1.16.2: closed at once after opening – the waveform/level analysis gets the cancel, its threads
    end, no ffmpeg it started is left running, and nothing arrives at the closed window afterwards."""
    import threading
    from fogscout import clipedit, qt_editor
    started = []
    real = clipedit.subprocess.Popen

    def popen(*a, **k):
        p = real(*a, **k)
        started.append(p)
        return p

    monkeypatch.setattr(clipedit.subprocess, "Popen", popen)
    before = set(threading.enumerate())                # windows of earlier tests may keep theirs
    win = qt_editor.EditorWindow(clip, [], str(tmp_path / "Clips"), sound=False)
    win.show()
    qapp.processEvents()
    win.close()
    assert win._cancel.is_set()
    deadline = time.time() + 30                        # the strip lets its running key-frame seeks finish (~0.2 s)
    mine = lambda: [t.name for t in threading.enumerate() if t not in before and t.is_alive()   # noqa: E731
                    and t.name.startswith("clip-")]
    while time.time() < deadline and mine():
        qapp.processEvents()
        time.sleep(0.05)
    assert not mine()
    assert not [p.args for p in started if p.poll() is None]


def test_a_file_that_is_no_video_opens_without_a_crash(qapp, tmp_path):
    """Post-review 1.16.2: a broken recording (not a video) – probe, waveform and levels give nothing, the editor
    window opens and closes without raising."""
    from fogscout import clipedit, qt_editor
    bad = tmp_path / "2026-10-17 21-40 Coal Tower – Nurse.mkv"
    bad.write_bytes(b"\x1aE\xdf\xa3 this is not a matroska file" * 100)
    assert not clipedit.probe(str(bad), FF).ok
    assert clipedit.waveform(str(bad), 12.0, FF) == [] and clipedit.track_levels(str(bad), 3, FF) == {}
    assert clipedit.frame_at(str(bad), 1.0, ffmpeg=FF) is None
    win = qt_editor.EditorWindow(str(bad), [], str(tmp_path / "Clips"), sound=False)
    win.show()
    _pump(qapp, seconds=1.0)
    win.close()
    _pump(qapp, seconds=0.3)


def test_the_timeline_layer_follows_a_theme_change(qapp, clip, tmp_path):
    """Post-review 1.16.2 (F4): the cached layer of the tracks kept the old colours after a theme/OLED change
    while the editor was open – the theme's colours are part of its key now."""
    from fogscout import qt_theme
    win = _window(qapp, clip, tmp_path)
    try:
        before = win.timeline._layer_key()
        old = (qt_theme._theme, qt_theme._oled, qt_theme._custom)
        qt_theme.set_theme(old[0], oled=not old[1], custom=old[2])
        try:
            assert win.timeline._layer_key() != before
        finally:
            qt_theme.set_theme(old[0], oled=old[1], custom=old[2])
        assert win.timeline._layer_key() == before
    finally:
        win.close()


def test_comma_and_period_step_one_frame(qapp, clip, tmp_path):
    """1.17: , and . step one frame back / on (as in most players), besides Ctrl+←/→."""
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QKeyEvent
    win = _window(qapp, clip, tmp_path)
    try:
        win.goto(5.0)
        frame = 1 / win.info.fps
        win.keyPressEvent(QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key_Period, Qt.NoModifier, "."))
        assert abs(win.pos - (5.0 + frame)) < 1e-6
        win.keyPressEvent(QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key_Comma, Qt.NoModifier, ","))
        win.keyPressEvent(QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key_Comma, Qt.NoModifier, ","))
        assert abs(win.pos - (5.0 - frame)) < 1e-6
    finally:
        win.close()


def test_every_key_in_the_help_does_what_it_says(qapp, clip, tmp_path, monkeypatch):
    """1.17.1: the help (?) is made from qt_editor.SHORTCUTS only, and each row names the key presses behind it –
    every one is pressed here and must reach the action it documents (method of the window, of the timeline, a tool,
    or the help itself). A key that does not work cannot be in the help."""
    from PySide6.QtGui import QKeyEvent, QKeySequence, QShortcut
    from fogscout import qt_editor, qt_timeline
    calls = []
    quiet = {"save", "toggle_play", "toggle_fullscreen", "save_project", "close"}   # export / play / full screen / close

    def spy(cls, name):
        orig = getattr(cls, name)

        def wrapped(self, *a, **k):
            calls.append(name)
            return None if name in quiet else orig(self, *a, **k)
        monkeypatch.setattr(cls, name, wrapped)

    targets = {chk[-1] for _g, rows in qt_editor.SHORTCUTS for _k, _w, checks in rows for chk in checks}
    for t in targets:
        if t.startswith("tl:"):
            spy(qt_timeline.SequenceTimeline, t[3:])
        elif not t.startswith("mode:") and t != "help":
            spy(qt_editor.EditorWindow, t)
    win = _window(qapp, clip, tmp_path, marks=[3.0, 8.0])
    try:
        shortcuts = win.findChildren(QShortcut)
        for group, rows in qt_editor.SHORTCUTS:
            assert rows, group
            for keys, what, checks in rows:
                assert checks, (keys, what)                    # every row is backed by at least one check
                for chk in checks:
                    target = chk[-1]
                    if target == "mode:select":
                        win.mode_btns["crop"].setChecked(True)
                    calls.clear()
                    if len(chk) == 2:                          # a QShortcut
                        seq = QKeySequence(chk[0])
                        sc = next((s for s in shortcuts if seq in s.keys()), None)
                        assert sc is not None, chk
                        sc.activated.emit()
                    else:
                        key, mods = chk[0], chk[1]
                        text = {qt_editor.Qt.Key_Question: "?", qt_editor.Qt.Key_Comma: ",",
                                qt_editor.Qt.Key_Period: ".", qt_editor.Qt.Key_Plus: "+",
                                qt_editor.Qt.Key_Minus: "-", qt_editor.Qt.Key_Space: " "}.get(key, "")
                        win.keyPressEvent(QKeyEvent(QKeyEvent.Type.KeyPress, key, qt_editor.Qt.KeyboardModifier(mods),
                                                    text))
                    if target.startswith("mode:"):
                        assert win.mode == target[5:], (chk, win.mode)
                    elif target == "help":
                        assert win.key_help is not None and not win.key_help.isHidden()
                        win.toggle_help()
                        assert win.key_help.isHidden()
                    else:
                        name = target[3:] if target.startswith("tl:") else target
                        assert name in calls, (keys, chk, calls)
        assert win.isVisible()                                 # Esc went back to select, it did not close
    finally:
        monkeypatch.undo()                                     # the real close again
        win.close()


def test_the_help_opens_with_question_mark_and_closes_with_esc_and_typing_stays_in_text_fields(qapp, clip, tmp_path):
    """1.17.1: ? opens the help panel over the window, ? or Esc closes it (Esc then does not close the window);
    while the project name field has the focus , . and ? are typed into it – no frame step, no help."""
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    win = _window(qapp, clip, tmp_path)
    try:
        win.activateWindow()
        win.setFocus()
        QTest.keyClick(win, Qt.Key_Question, Qt.ShiftModifier, 10)
        assert not win.key_help.isHidden()
        assert win.key_help.width() <= win.width() and win.key_help.height() <= win.height()
        QTest.keyClick(win, Qt.Key_Escape)
        assert win.key_help.isHidden() and win.isVisible()
        win.toggle_help()
        QTest.keyClick(win, Qt.Key_Question, Qt.ShiftModifier)
        assert win.key_help.isHidden()
        win.goto(5.0)
        before = win.pos
        win.name_edit.setFocus()
        win.name_edit.setText("Clip")
        win.name_edit.setCursorPosition(4)
        for ch in ",.?":
            QTest.keyClick(win.name_edit, ch)
        qapp.processEvents()
        assert win.name_edit.text() == "Clip,.?" and win.pos == before and win.key_help.isHidden()
    finally:
        win.close()


def test_no_key_is_bound_twice_in_the_editor(qapp, clip, tmp_path):
    """1.17.1: every QShortcut key of the editor once; the keys the help lists for keyPressEvent are not taken by a
    QShortcut (it would win and the documented action would never run)."""
    from PySide6.QtGui import QKeySequence, QShortcut
    from fogscout import qt_editor
    win = _window(qapp, clip, tmp_path)
    try:
        keys = [k.toString() for s in win.findChildren(QShortcut) for k in s.keys()]
        assert len(keys) == len(set(keys)), sorted(k for k in keys if keys.count(k) > 1)
        for _g, rows in qt_editor.SHORTCUTS:
            for _k, _w, checks in rows:
                for chk in checks:
                    if len(chk) == 3:
                        seq = QKeySequence(qt_editor.Qt.KeyboardModifier(chk[1]).value | chk[0]).toString()
                        assert seq not in keys, seq
    finally:
        win.close()


def _press_esc(win):
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QKeyEvent
    win.keyPressEvent(QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key_Escape, Qt.NoModifier, ""))


def _on_picture(view, kind, fx, fy):
    f = view.frame_rect()
    _mouse(view, kind, f.left() + fx * f.width(), f.top() + fy * f.height())


def test_esc_goes_one_step_per_press_and_never_closes_the_editor(qapp, clip, tmp_path):
    """1.18 (user: „Esc darf den Editor nie schliessen“, order F2): with a tool on, a clip marked and the full screen,
    each Esc does one thing – tool back to select, then the selection goes, then the full screen ends – and further
    presses leave the window open (one hint in the status line)."""
    win = _window(qapp, clip, tmp_path)
    try:
        win.goto(6.0)
        win.split_at_playhead()
        win.timeline.select(0)
        win.mode_btns["draw"].setChecked(True)
        win.toggle_fullscreen()
        assert win.mode == "draw" and win.timeline.selection == 0 and win._fullscreen is not None
        _press_esc(win)
        assert win.mode == "select" and win.timeline.selection == 0 and win._fullscreen is not None
        _press_esc(win)
        assert win.timeline.selection is None and win._fullscreen is not None
        _press_esc(win)
        assert win._fullscreen is None and win.isVisible()
        _press_esc(win)
        assert win.isVisible() and "Strg+W" in win.status.text()
        for _i in range(3):
            _press_esc(win)
        assert win.isVisible()
    finally:
        win.close()


def test_esc_cancels_a_trim_and_a_clip_move_without_an_undo_step(qapp, clip, tmp_path):
    """1.18: Esc during a drag on the timeline – the clips stay as they were, no undo step, and the release that
    follows changes nothing."""
    win = _window(qapp, clip, tmp_path)
    tl = win.timeline
    try:
        win.goto(6.0)
        win.split_at_playhead()
        before = [(p.start, p.end) for p in win.parts]
        steps = len(win.history._past)
        r0 = tl.clip_rect(0)
        x_edge = r0.right()
        _mouse(tl, "press", x_edge - 1, r0.center().y())
        _mouse(tl, "move", x_edge - 2 * tl.scale, r0.center().y())
        assert tl.gesture_active()
        _press_esc(win)
        assert not tl.gesture_active() and win.status.text() == "Abgebrochen."
        _mouse(tl, "move", x_edge - 3 * tl.scale, r0.center().y())
        _mouse(tl, "release", x_edge - 3 * tl.scale, r0.center().y())
        assert [(p.start, p.end) for p in win.parts] == before and len(win.history._past) == steps
        r1 = tl.clip_rect(1)                                                  # the second clip dragged to the front
        _mouse(tl, "press", r1.center().x(), r1.center().y())
        _mouse(tl, "move", r1.center().x() - 20, r1.center().y())
        _mouse(tl, "move", tl.clip_rect(0).left() + 2, r1.center().y())
        assert tl._drag[0] == "move"
        _press_esc(win)
        _mouse(tl, "release", tl.clip_rect(0).left() + 2, r1.center().y())
        assert [(p.start, p.end) for p in win.parts] == before and len(win.history._past) == steps
    finally:
        win.close()


def test_moving_a_drawing_or_a_box_changes_nothing_until_release_and_esc_drops_it(qapp, clip, tmp_path):
    """1.18: a drawing or censor box being moved is a copy until the release (a save in between sees the state
    before the drag); Esc drops the copy – no undo step; a normal release takes it over as one step."""
    win = _window(qapp, clip, tmp_path)
    pv = win.preview
    try:
        win.mode_btns["draw"].setChecked(True)
        win.draw_btns["rect"].setChecked(True)
        _on_picture(pv, "press", 0.2, 0.2)
        _on_picture(pv, "move", 0.5, 0.5)
        _on_picture(pv, "release", 0.5, 0.5)
        assert len(pv.shapes) == 1
        pts = list(pv.shapes[0].pts)
        steps = len(win.history._past)
        _on_picture(pv, "press", 0.2, 0.35)                                   # grab it at its edge
        _on_picture(pv, "move", 0.3, 0.45)
        assert pv.gesture_active() and pv.shapes[0].pts == pts                # the list keeps the original
        assert [list(s.pts) for s in win._state().shapes] == [pts]
        _press_esc(win)
        assert not pv.gesture_active() and win.mode == "draw"                 # Esc ended the drag, not the tool
        _on_picture(pv, "release", 0.3, 0.45)
        assert pv.shapes[0].pts == pts and len(win.history._past) == steps
        _on_picture(pv, "press", 0.2, 0.35)                                   # moved for real: one step
        _on_picture(pv, "move", 0.3, 0.45)
        _on_picture(pv, "release", 0.3, 0.45)
        assert pv.shapes[0].pts != pts and len(win.history._past) == steps + 1
        # a censor box
        win.mode_btns["censor"].setChecked(True)
        pv.add_box([0.1, 0.1, 0.2, 0.2])
        box = list(pv.boxes[-1])
        steps = len(win.history._past)
        _on_picture(pv, "press", 0.2, 0.2)
        _on_picture(pv, "move", 0.4, 0.4)
        assert pv.boxes[-1] == box and pv._boxes_shown()[-1] != box
        _press_esc(win)
        _on_picture(pv, "release", 0.4, 0.4)
        assert pv.boxes[-1] == box and len(win.history._past) == steps
        _on_picture(pv, "press", 0.2, 0.2)
        _on_picture(pv, "move", 0.4, 0.4)
        _on_picture(pv, "release", 0.4, 0.4)
        assert pv.boxes[-1] != box and len(win.history._past) == steps + 1
    finally:
        win.close()


def test_esc_in_a_text_field_only_leaves_the_field(qapp, clip, tmp_path):
    """1.18: Esc while the project name has the focus – the focus goes back to the window, the text stays, the
    window stays open (before 1.18 the key reached the window and closed it)."""
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QApplication
    win = _window(qapp, clip, tmp_path)
    try:
        win.activateWindow()
        win.name_edit.setFocus()
        win.name_edit.setText("Mein Clip")
        qapp.processEvents()
        QTest.keyClick(win.name_edit, Qt.Key_Escape)
        qapp.processEvents()
        assert win.isVisible() and win.name_edit.text() == "Mein Clip"
        assert QApplication.focusWidget() is not win.name_edit
    finally:
        win.close()


def test_ctrl_w_closes_the_editor(qapp, clip, tmp_path):
    """1.18 (F6): Strg+W closes the editor (Esc does not)."""
    import shiboken6
    from PySide6.QtGui import QKeySequence, QShortcut
    win = _window(qapp, clip, tmp_path)
    sc = next(s for s in win.findChildren(QShortcut) if QKeySequence("Ctrl+W") in s.keys())
    sc.activated.emit()
    qapp.processEvents()
    assert not shiboken6.isValid(win) or not win.isVisible()             # closed (deleted on close)


def test_the_compact_editor_still_closes_its_preview_on_esc(qapp, clip, tmp_path, monkeypatch):
    """1.18 (F3): beside the tables Esc keeps closing the compact preview – it holds no project."""
    from fogscout import qt_clip
    closed = []
    monkeypatch.setattr(qt_clip.ClipWindow, "close", lambda self: closed.append(True))
    win = qt_clip.ClipWindow(clip, [], str(tmp_path / "Clips"), sound=False, compact=True)
    try:
        _press_esc(win)
        assert closed == [True]
    finally:
        monkeypatch.undo()
        win.close()


def test_no_key_but_ctrl_w_closes_the_editor(qapp, clip, tmp_path, monkeypatch):
    """1.18 guard: every key of the help (and Esc) pressed in every tool, with and without a marked clip, in and out
    of the full screen – the window stays open. Exports, playback and project saves are stubbed."""
    from PySide6.QtGui import QKeyEvent, QKeySequence, QShortcut
    from fogscout import qt_editor
    for name in ("save", "toggle_play", "save_project"):
        monkeypatch.setattr(qt_editor.EditorWindow, name, lambda self, *a, **k: None)
    win = _window(qapp, clip, tmp_path, marks=[3.0])
    try:
        shortcuts = [s for s in win.findChildren(QShortcut) if QKeySequence("Ctrl+W") not in s.keys()]
        keys = [(c[0], c[1]) for _g, rows in qt_editor.SHORTCUTS for _k, _w, checks in rows for c in checks
                if len(c) == 3] + [(qt_editor.Qt.Key_Escape, 0)]
        for mode in ("select", "crop", "draw", "censor"):
            for marked in (False, True):
                for full in (False, True):
                    win.mode_btns[mode].setChecked(True)
                    if not win.parts:
                        win.goto(0.0)
                        win.clip_around_mark()
                    win.timeline.select(0 if marked else None)
                    if (win._fullscreen is not None) != full:
                        win.toggle_fullscreen()
                    for key, mods in keys:
                        win.keyPressEvent(QKeyEvent(QKeyEvent.Type.KeyPress, key, qt_editor.Qt.KeyboardModifier(mods), ""))
                        assert win.isVisible(), (mode, marked, full, key)
                    for sc in shortcuts:
                        sc.activated.emit()
                        assert win.isVisible(), (mode, marked, full, [k.toString() for k in sc.keys()])
                    if getattr(win, "key_help", None) is not None:
                        win.key_help.hide()
    finally:
        monkeypatch.undo()
        win.close()


def test_editor_sliders_draw_a_thin_track_not_a_grey_box(qapp):
    """1.22.2 (user: „warum ist bei den Scrollbars der Hintergrund grau?“ – the sound sliders of the inspector): the
    rule ``QSlider:disabled::sub-page`` (pseudo-state before the sub-control) made Qt ignore the groove's 4 px and
    paint it over the slider's whole height – 15 of 15 rows in the border colour beside the handle. Right: a thin
    track, in dark and light, enabled and not; a disabled slider's filled part stays grey."""
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QFrame, QHBoxLayout, QSlider
    from fogscout import qt_theme
    from fogscout.qt_editor import editor_qss
    for dark in (True, False):
        c = qt_theme.colours(dark)
        for enabled in (True, False):
            frame = QFrame()
            frame.setObjectName("panel")
            lay = QHBoxLayout(frame)
            s = QSlider(Qt.Horizontal)
            s.setRange(0, 200)
            s.setValue(120)
            s.setEnabled(enabled)
            lay.addWidget(s)
            frame.setStyleSheet(qt_theme.stylesheet(dark) + editor_qss(c))
            frame.resize(300, 40)
            frame.show()
            qapp.processEvents()
            img = s.grab().toImage()
            track = sum(1 for y in range(img.height()) if img.pixelColor(img.width() - 12, y).name() == c["border"])
            filled = {img.pixelColor(10, y).name() for y in range(img.height())}
            frame.close()
            assert 0 < track <= 6 < img.height(), (dark, enabled, track, img.height())
            assert (c["accent"] if enabled else c["border"]) in filled


def test_stepping_on_shows_cached_pictures_without_a_new_decode(qapp, clip, tmp_path, monkeypatch):
    """1.40: one scrub read decodes the wanted picture and the next ones (clipedit.frames_from); stepping on then
    shows them from the cache – no new ffmpeg run (clipedit's test checks they are frame_at's pictures)."""
    from fogscout import clipedit
    win = _window(qapp, clip, tmp_path)
    try:
        win.goto(5.0)
        assert _pump(qapp, lambda: win._last_key == clipedit.frame_key(5.0, win.info.fps))
        runs = []
        for name in ("frames_from", "frame_at"):
            orig = getattr(clipedit, name)
            monkeypatch.setattr(clipedit, name, lambda *a, _o=orig, _n=name, **k: (runs.append(_n), _o(*a, **k))[1])
        for _ in range(4):
            win.step_frame(1)
        want = clipedit.frame_key(win.pos, win.info.fps)
        assert _pump(qapp, lambda: win._last_key == want)
        assert runs == []                                      # the four pictures came from the first read
        win.goto(9.0)                                         # far away: a new read
        assert _pump(qapp, lambda: win._last_key == clipedit.frame_key(9.0, win.info.fps))
        assert "frames_from" in runs
    finally:
        win.close()



def test_j_k_l_play_spool_faster_without_sound_stop_and_jump_back(qapp, clip, tmp_path):
    """1.40: L plays, L again ×2 then ×4 (picture only – no sound while spooling); the playhead still runs in the
    cut's output time; K stops where it is; J stops and jumps 5 s back."""
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QKeyEvent
    from fogscout import clipedit

    def key(k):
        win.keyPressEvent(QKeyEvent(QKeyEvent.Type.KeyPress, k, Qt.NoModifier, ""))
    win = _window(qapp, clip, tmp_path)
    try:
        win.parts = [clipedit.Part(0.0, 12.0, 2.0)]                   # a ×2 clip: 6 s of output
        win.timeline.set_parts(win.parts)
        win._commit()
        win.goto(0.0)
        key(Qt.Key_L)
        assert win.playing and win._shuttle == 1.0 and win._seg[2] == 2.0
        key(Qt.Key_L)
        assert win.playing and win._shuttle == 2.0 and win._seg[2] == 4.0 and "×2" in win.pos_label.text()
        win.sound_box.setChecked(True)
        win._volume = 1.0
        assert win._shuttle == 2.0 and win.playing                         # a sound change keeps the tempo
        assert not win._sound_wanted()
        key(Qt.Key_L)
        key(Qt.Key_L)
        assert win._shuttle == 4.0 and win._seg[2] == 8.0                 # never past ×4
        win._played_at(win._seg[0] + 4.0)                                  # 4 s of source in a ×2 clip
        assert win.pos == pytest.approx(win._seg[3] + 2.0)
        key(Qt.Key_K)
        assert not win.playing and win._shuttle == 1.0
        at = win.pos
        key(Qt.Key_K)
        assert win.pos == at
        win.goto(5.5)
        key(Qt.Key_J)
        assert not win.playing and win.pos == pytest.approx(0.5)
    finally:
        win.close()
