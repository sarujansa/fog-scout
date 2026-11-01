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
    assert _pump(app, lambda: win.preview._img is not None and (win.loading is None or win.loading.finished))
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
        win.save_project()
        path = project.project_path(str(tmp_path / "Clips"), clip)
        assert os.path.isfile(path) and "Projekt gespeichert" in win.status.text()
        assert win.library.item_for(clip) is None                              # no App list here: nothing to flag
    finally:
        win.close()
    again = _window(qapp, clip, tmp_path)
    try:
        assert [(round(p.start, 1), round(p.end, 1), p.speed) for p in again.parts] == [(0.0, 3.0, 1.0), (3.0, 12.0, 2.0)]
        assert len(again.preview.shapes) == 1 and again.fade_out_box.currentData() == 1.0
        assert again.name_edit.text() == "Nurse Doppel-Blink" and "Projekt geladen" in again.status.text()
        assert not again.history.can_undo()                                    # the loaded state is the start
        plan = again.edit_plan()
        assert plan.fade_out == 1.0 and len(plan.parts) == 2 and plan.parts[1].speed == 2.0
    finally:
        again.close()


def test_the_library_lists_media_and_a_drop_on_the_timeline_opens_it(qapp, clip, tmp_path):
    """The library shows the App's items with search and sort, a row carries its path when dragged, a drop on the
    timeline asks the App to open it – in place of this window while nothing was cut here, else beside it; an
    unknown video file dropped from outside joins the library first."""
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
        win.timeline.dropped.emit(other)                                      # pristine: replaces this window
        assert opened == [(other, win)]
        win.timeline.dropped.emit(clip)                                       # the one open already: nothing
        assert len(opened) == 1 and "schon auf der Zeitleiste" in win.status.text()
        win.goto(4.0)
        win.split_at_playhead()                                               # cut here: a window of its own
        win.timeline.dropped.emit(other)
        assert opened[-1] == (other, None)
        new = str(tmp_path / "fresh.mp4")
        with open(new, "wb") as f:
            f.write(b"\0" * 100)
        win.timeline.dropped.emit(new)
        assert opened[-1][0] == new and lib.item_for(new) is not None and lib.item_for(new).kind == "file"
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
