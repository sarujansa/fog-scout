"""The clip editor window (qt_clip): the crop and drawing tools of the shared canvas, the choice boxes and the
keys, the tempo box, and saves that outlive their window – another row picked beside the tables, the program
quitting or restarting for an update while a clip is written. Offscreen; skipped without imageio-ffmpeg."""
import os
import subprocess
import sys
import tempfile
import threading
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import annotate, obsrec  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = obsrec.ffmpeg_exe()
pytestmark = pytest.mark.skipif(FF is None, reason="imageio-ffmpeg not installed")
OFFSCREEN = os.environ.get("QT_QPA_PLATFORM") == "offscreen"


@pytest.fixture(scope="module")
def clip(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("clipwin") / "2026-10-17 21-40 Coal Tower – Nurse.mkv")
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
    """A failed test must not leave a save registered – the next one (and the update lock) would see it."""
    yield
    qt_clip = sys.modules.get("fogscout.qt_clip")
    if qt_clip is not None and getattr(qt_clip, "_SAVES", None):
        qt_clip.stop_saves(wait=5)
        qt_clip._SAVES.clear()


def _pump(app, until, seconds=30):
    deadline = time.time() + seconds
    while time.time() < deadline and not until():
        app.processEvents()
        time.sleep(0.01)
    return until()


def _window(app, clip, tmp_path, **kw):
    from fogscout import qt_clip
    win = qt_clip.ClipWindow(clip, [], str(tmp_path / "Clips"), sound=False, **kw)
    win.show()
    assert _pump(app, lambda: win.preview._img is not None and (win.loading is None or win.loading.finished))
    return win


def _mouse(view, kind, fx, fy):
    """A mouse event on the picture at (fx, fy), straight to the handler (an exception there reaches the test)."""
    from PySide6.QtCore import QPointF, Qt
    from PySide6.QtGui import QMouseEvent
    f = view.frame_rect()
    pt = QPointF(f.left() + fx * f.width(), f.top() + fy * f.height())
    ev = QMouseEvent({"press": QMouseEvent.Type.MouseButtonPress, "move": QMouseEvent.Type.MouseMove,
                      "release": QMouseEvent.Type.MouseButtonRelease}[kind], pt, pt, Qt.LeftButton, Qt.LeftButton,
                     Qt.NoModifier)
    {"press": view.mousePressEvent, "move": view.mouseMoveEvent, "release": view.mouseReleaseEvent}[kind](ev)


def _drag(view, a, b):
    _mouse(view, "press", *a)
    _mouse(view, "move", *b)
    _mouse(view, "release", *b)


def _canvas(app, size=(1600, 900)):
    from PySide6.QtGui import QColor, QImage
    from fogscout import qt_clip
    view = qt_clip.PreviewView()
    view.resize(800, 450)
    img = QImage(size[0], size[1], QImage.Format_RGB888)
    img.fill(QColor("#405060"))
    view.set_frame(img)
    view.show()
    app.processEvents()
    return view


def _corner(view, name):
    x, y, w, h = view.crop
    return {"tl": (x, y), "tr": (x + w, y), "bl": (x, y + h), "br": (x + w, y + h)}[name]


@pytest.mark.parametrize("handle,to", [("tl", (0.2, 0.05)), ("tr", (0.8, 0.05))])
def test_a_fixed_ratio_crop_keeps_its_shape_when_a_top_corner_is_pulled_up(qapp, handle, to):
    """Review #13: 9:16 on a 16:9 picture, the box made smaller, then a top corner pulled up past the room above
    the corner that stays – the box got cut at the top only and came out 0.81 instead of 0.5625 (the saved clip
    884×1080). Now the height leads there, the opposite corner stays, the shape holds."""
    from fogscout import imageedit
    view = _canvas(qapp)
    try:
        ratio = 9 / 16
        view.set_crop(imageedit.aspect_box((0, 0, 1, 1), ratio, (1600, 900)), ratio)
        view.set_crop_edit(True)
        _drag(view, _corner(view, handle), (0.45 if handle == "tl" else 0.55, 0.5))     # smaller first
        stays = _corner(view, "br" if handle == "tl" else "bl")
        _drag(view, _corner(view, handle), to)
        x, y, w, h = view.crop
        assert w * 1600 / (h * 900) == pytest.approx(ratio, abs=0.005)
        assert y >= 0 and y + h <= 1 + 1e-9 and h == pytest.approx(stays[1], abs=1e-6)   # up to the top edge
        assert _corner(view, "br" if handle == "tl" else "bl") == pytest.approx(stays, abs=1e-6)
        _drag(view, _corner(view, "bl"), (0.3, 0.98))                        # downwards it was right already
        x, y, w, h = view.crop
        assert w * 1600 / (h * 900) == pytest.approx(ratio, abs=0.005) and y + h <= 1 + 1e-9
    finally:
        view.close()


def test_a_click_beside_the_crop_box_keeps_it(qapp):
    """Review #41: a click beside the box with one pixel of hand jitter replaced the crop with a 1 % box (the
    result 16×9 px), as did a drag straight down (a 1:1 box from no width). Only a real drag draws a new box."""
    from fogscout import imageedit
    view = _canvas(qapp)
    try:
        view.set_crop(imageedit.aspect_box((0, 0, 1, 1), 1.0, (1600, 900)), 1.0)
        view.set_crop_edit(True)
        before = view.crop
        f = view.frame_rect()
        _drag(view, (0.05, 0.5), (0.05 + 1 / f.width(), 0.5 + 1 / f.height()))   # left of the square, 1 px
        assert view.crop == before
        _drag(view, (0.05, 0.2), (0.05, 0.8))                                # down only: no width, no box
        assert view.crop == before
        _drag(view, (0.02, 0.1), (0.15, 0.9))                                # a real drag: a new square
        x, y, w, h = view.crop
        assert view.crop != before and x == pytest.approx(0.02, abs=0.01)
        assert w * 1600 / (h * 900) == pytest.approx(1.0, abs=0.01)
    finally:
        view.close()


def test_removing_or_replacing_a_drawing_while_it_is_dragged_ends_the_drag(qapp):
    """Review #39: Entf (or undo in the picture editor) while a drawing was dragged – every further mouse move
    raised TypeError, and after an undo the old drawing was written back over the restored one."""
    view = _canvas(qapp)
    try:
        view.set_shape_tool("rect")
        _drag(view, (0.2, 0.2), (0.5, 0.5))
        assert len(view.shapes) == 1
        _mouse(view, "press", 0.2, 0.35)                                      # grab it at its edge
        _mouse(view, "move", 0.25, 0.4)
        assert view._drag and view._drag[0] == "shape_move"
        assert view.remove_selected_shape()                                   # what Entf does
        _mouse(view, "move", 0.3, 0.45)
        _mouse(view, "release", 0.3, 0.45)
        assert view.shapes == [] and view._drag is None
        _drag(view, (0.2, 0.2), (0.5, 0.5))
        restored = annotate.Shape("rect", [(0.6, 0.6), (0.8, 0.8)])
        _mouse(view, "press", 0.2, 0.35)
        _mouse(view, "move", 0.25, 0.4)
        view.set_shapes([restored])                                          # the picture editor's undo
        _mouse(view, "move", 0.3, 0.45)
        _mouse(view, "release", 0.3, 0.45)
        assert view.shapes == [restored]
    finally:
        view.close()


def test_rahmen_bearbeiten_without_a_crop_switches_the_tool_on(qapp, clip, tmp_path):
    """Review #16: "Rahmen bearbeiten" with no crop chosen showed the button on and a full box, but the tool was
    never switched on – dragging a corner did nothing until the button was clicked off and on again."""
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    win = _window(qapp, clip, tmp_path)
    try:
        win.tools.setCurrentIndex(2)
        assert win.crop_box.currentData() == "none" and not win.preview.crop_edit
        QTest.mouseClick(win.crop_btn, Qt.LeftButton)
        assert win.crop_box.currentData() == "free" and win.crop_btn.isChecked() and win.preview.crop_edit
        assert win.preview.crop == pytest.approx((0.0, 0.0, 1.0, 1.0))
        _drag(win.preview, (0.0, 0.0), (0.3, 0.3))
        assert win.preview.crop == pytest.approx((0.3, 0.3, 0.7, 0.7), abs=0.01)
        assert win.edit_plan().crop == pytest.approx((0.3, 0.3, 0.7, 0.7), abs=0.01)
    finally:
        win.close()


def test_the_choice_boxes_leave_the_keys_with_the_window(qapp, clip, tmp_path):
    """Review #25: a box picked with the mouse kept the keyboard focus and took the window's keys – End set the
    marked part to ×4 instead of moving the playhead, Home/End changed the crop, letters picked items. No box
    takes the focus now; a pick with the mouse leaves the keys with the window."""
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QApplication, QComboBox
    win = _window(qapp, clip, tmp_path)
    try:
        boxes = win.findChildren(QComboBox)
        assert {win.speed_box, win.crop_box, win.fade_in_box, win.mode_box, win.gif_box, win.style_box} <= set(boxes)
        assert [b for b in boxes if b.focusPolicy() != Qt.NoFocus] == []
        if not OFFSCREEN:                    # the popup and the focus below: offscreen only (no real desktop)
            return
        win.timeline.set_range(1.0, 3.0)
        win.add_part()
        win.timeline.set_range(5.0, 7.0)
        win.add_part()
        win.tools.setCurrentIndex(1)
        win.part_list.setCurrentRow(0)
        win.activateWindow()
        win.setFocus()
        qapp.processEvents()
        QTest.mouseClick(win.speed_box, Qt.LeftButton)                       # opens the list
        view = win.speed_box.view()
        view.setCurrentIndex(win.speed_box.model().index(win.speed_box.findData(0.5), 0))
        QTest.keyClick(view, Qt.Key_Return)                                  # picks ×0.5
        _pump(qapp, lambda: not view.isVisible(), 5)
        assert [p.speed for p in win._parts] == [0.5, 1.0]
        assert QApplication.focusWidget() is not win.speed_box
        QTest.keyClick(QApplication.focusWidget() or win, Qt.Key_End)
        assert [p.speed for p in win._parts] == [0.5, 1.0]                   # the tempo stays …
        assert win.timeline.pos == pytest.approx(win.info.duration)          # … the playhead goes to the end
    finally:
        win.close()


def test_the_tempo_box_shows_the_tempo_new_parts_get(qapp, clip, tmp_path):
    """Review #38: after a part was added or removed no row is marked, but the box still showed the tempo of the
    part marked before (×0.5) – the next part came at normal speed, and picking the shown value did nothing."""
    win = _window(qapp, clip, tmp_path)
    try:
        win.tools.setCurrentIndex(1)
        win.timeline.set_range(1.0, 3.0)
        win.add_part()
        win.part_list.setCurrentRow(0)
        win.speed_box.setCurrentIndex(win.speed_box.findData(0.5))
        assert win._parts[0].speed == 0.5 and win._range_speed == 1.0
        win.timeline.set_range(5.0, 7.0)
        win.add_part()
        assert win.part_list.currentRow() == -1 and win.speed_box.currentData() == 1.0
        assert [p.speed for p in win._parts] == [0.5, 1.0]
        win.speed_box.setCurrentIndex(win.speed_box.findData(2.0))           # no row marked: the next parts
        win.timeline.set_range(8.0, 9.0)
        win.add_part()
        assert [p.speed for p in win._parts] == [0.5, 1.0, 2.0] and win.speed_box.currentData() == 2.0
        win.part_list.setCurrentRow(0)
        assert win.speed_box.currentData() == 0.5
        win.remove_part()
        assert win.speed_box.currentData() == 2.0
        win.part_list.setCurrentRow(0)
        win.clear_parts()
        assert win.speed_box.currentData() == 2.0 == win.edit_plan().parts[0].speed
    finally:
        win.close()


def test_the_save_thread_gets_copies_of_the_drawings(qapp, clip, tmp_path, monkeypatch):
    """Review #43/#49: the save thread drew the canvas' own drawings while the window changed the marked one in
    place – a colour, text or time changed after "Clip speichern" (Discord: during the first encode, the retry
    drew again) ended up in the clip. The plan holds copies now."""
    from fogscout import qt_clip
    win = _window(qapp, clip, tmp_path)
    started, go, seen, logs = threading.Event(), threading.Event(), [], []
    win.log = lambda text, kind="System": logs.append((text, kind))

    def export(path, edit, out, mode, ffmpeg, **kw):
        started.set()
        go.wait(20)
        seen.append([(s.text, s.colour, s.t0) for s in edit.shapes])
        return False, "test"
    monkeypatch.setattr(qt_clip.clipedit, "export", export)
    try:
        win.goto(2.0)
        win.preview._new_shape(annotate.Shape("text", [(0.3, 0.3)], annotate.COLOURS[0], annotate.TEXT_SIZE,
                                              "Killer hier"))
        plan = win.edit_plan()
        win.save()
        assert started.wait(20)
        win._draw_colour(annotate.COLOURS[1])                                 # the marked drawing, in place
        win._draw_text_edited("anders")
        win.goto(6.0)
        win._draw_when(0)
        go.set()
        assert _pump(qapp, lambda: logs)
        assert seen == [[("Killer hier", annotate.COLOURS[0], 2.0)]]
        assert win.preview.shapes[0].text == "anders" and plan.shapes[0].text == "Killer hier"
    finally:
        go.set()
        win.close()


def test_a_compact_editor_replaced_while_saving_still_hands_over_its_clip(qapp, clip, tmp_path, monkeypatch):
    """Review #26: picking another row beside the rounds/clips table replaces the compact editor – the old one
    is deleted, its pump with it, and a save still running never reached the clips list (no index entry, no
    automatic upload; a GIF the program never listed). The result now comes all the same, and a still too."""
    import shiboken6
    from PySide6.QtCore import QCoreApplication, QEvent
    from fogscout import qt_clip
    from fogscout.qt_pages import HostView
    go = threading.Event()

    def export(path, edit, out, mode, ffmpeg, **kw):
        go.wait(20)
        with open(out, "wb") as f:
            f.write(b"\0" * 2048)
        return True, ""
    monkeypatch.setattr(qt_clip.clipedit, "export", export)
    host = HostView()
    saved, logs = [], []
    try:
        host.show()
        win = qt_clip.ClipWindow(clip, [], str(tmp_path / "Clips"), sound=False, compact=True,
                                 on_saved=saved.append, log=lambda text, kind="System": logs.append((text, kind)))
        host.set_content(win)
        assert _pump(qapp, lambda: win.preview._img is not None)
        win.mode_box.setCurrentIndex(win.mode_box.findData("gif"))
        out = os.path.join(str(tmp_path / "Clips"), win.name_edit.text() + ".gif")
        win.save()
        win.save_still(1.0)
        host.set_content(qt_clip.ClipWindow(clip, [], str(tmp_path / "Clips"), sound=False, compact=True))
        QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
        assert not shiboken6.isValid(win)                                    # gone, pump and widgets with it
        go.set()
        assert _pump(qapp, lambda: len(saved) == 2)
        assert [p for p in saved if p.endswith(".gif")] == [out]
        assert len([p for p in saved if p.endswith(".png")]) == 1             # the still
        assert ("Clip gespeichert: " + out, "System") in logs
        assert win.saved_seconds[out] > 0 and qt_clip.running_saves() == []
    finally:
        go.set()
        host.set_content(None)
        host.close()
        qapp.processEvents()


def test_quitting_stops_a_running_clip_save_and_leaves_no_half_file(qapp, clip, tmp_path, monkeypatch):
    """Review #27: quitting while a clip was encoded left ffmpeg writing on its own (the clip never reached the
    clips list, a GIF stayed invisible) and the temp folder of the drawings behind. stop_saves ends ffmpeg,
    clipedit removes the half file and the folder, the editor reports it."""
    from fogscout import qt_clip
    temp = tmp_path / "tmp"
    temp.mkdir()
    monkeypatch.setattr(tempfile, "tempdir", str(temp))
    real_run = qt_clip._SaveJob.run                                          # ffmpeg reads in real time: the
    monkeypatch.setattr(qt_clip._SaveJob, "run",                              # export runs 12 s, long enough
                        lambda self, args: real_run(self, [args[0], "-re"] + list(args[1:])))
    saved, logs = [], []
    win = _window(qapp, clip, tmp_path, mode="exact", on_saved=saved.append,
                  log=lambda text, kind="System": logs.append((text, kind)))
    try:
        win.preview.set_shapes([annotate.Shape("arrow", [(0.2, 0.2), (0.6, 0.6)])])   # export with a drawing
        win.timeline.set_range(0.0, 12.0)
        win.save()
        job = qt_clip._SAVES[0]
        half = job.out + qt_clip.clipedit.PART_EXT                           # written under a temporary name
        assert _pump(qapp, lambda: job._proc is not None and os.path.exists(half))
        assert any(n.startswith("dbdms-edit-") for n in os.listdir(temp)) and not os.path.exists(job.out)
        assert qt_clip.running_saves() == [job.out]
        assert qt_clip.stop_saves() == [job.out]
        assert not job.thread.is_alive() and job._proc.poll() is not None
        assert not os.path.exists(job.out) and not os.path.exists(half) and os.listdir(temp) == []
        assert saved == [] and ("Clip nicht gespeichert: beim Beenden abgebrochen", "Fehler") in logs
        assert qt_clip.running_saves() == [] and win.save_btn.isEnabled()
    finally:
        win.close()


@pytest.fixture
def app_root(tmp_path):
    if sys.platform == "win32":
        pytest.skip("Linux: the Windows job tests the native parts; the app would touch the system there")
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    for name in ("maps", "models", "maps.json"):
        os.symlink(os.path.join(ROOT, name), tmp_path / name)
    (tmp_path / "sim").mkdir()
    return tmp_path


def test_an_update_waits_for_a_clip_save_and_quitting_hands_a_finished_one_over(app_root, clip, monkeypatch):
    """Review #27: "Aktualisieren und neu starten" during a clip save quit at once (ffmpeg left on its own, as
    above) – now it is held back like during a round; quitting hands a save that was done just before to the
    clips list first (the recorder still runs then)."""
    from fogscout import qt_clip, restart
    from fogscout.app import App
    spawned, saved = [], []
    monkeypatch.setattr(restart, "spawn_helper", lambda root: spawned.append(root) or False)   # False: no quit
    gates = []

    def export(path, edit, out, mode, ffmpeg, **kw):
        gate = threading.Event()
        gates.append(gate)
        gate.wait(20)
        with open(out, "wb") as f:
            f.write(b"\0" * 2048)
        return True, ""
    monkeypatch.setattr(qt_clip.clipedit, "export", export)
    app = App(str(app_root), simulate=str(app_root / "sim"))
    win = None
    try:
        qapp = app.root.qapp
        win = _window(qapp, clip, app_root, on_saved=saved.append)
        win.save()
        assert _pump(qapp, lambda: gates)
        app.apply_update()
        assert spawned == [] and "Clip" in app.upd_status.get() and "gesperrt" in app.upd_status.get()
        gates[0].set()
        assert _pump(qapp, lambda: saved)
        app.apply_update()
        assert spawned == [str(app_root)]                                    # saved: the update may go
        win.save()
        assert _pump(qapp, lambda: len(gates) == 2)
        gates[1].set()
        job = qt_clip._SAVES[0]
        job.thread.join(20)                                                  # done, its result not handled yet
        assert len(saved) == 1
        app.quit()
        assert len(saved) == 2 and saved[1] == job.out and qt_clip.running_saves() == []
    finally:
        for gate in gates:
            gate.set()
        if win is not None:
            win.close()
        app.quit()


def test_the_big_editor_has_the_picture_left_and_tools_and_saving_in_a_side_column(qapp, clip, tmp_path):
    """1.12.5 (user on two screenshots of the big editor: "gefallen mir nicht" – a big black box with the picture
    small in it, an almost empty clip card, the save card squeezed into two lines): picture, timeline and playback on
    the left, the tool tabs with saving below them in a side column of SIDE_W; the preview no taller than the picture
    at that width; start/end/mark in the clip tab, the playback sound beside the position; one line per sound source.
    Nothing sticks out of the window or hangs without a parent."""
    from PySide6.QtWidgets import QCheckBox, QPushButton, QWidget
    from fogscout import qt_clip
    four = str(tmp_path / "2026-10-26 07-10 Coal Tower – Nurse.mkv")                 # OBS's tracks 1–4
    sines = sum((["-f", "lavfi", "-i", f"sine=frequency={f}:duration=3"] for f in (440, 550, 660, 770)), [])
    maps = ["-map", "0:v"] + sum((["-map", f"{i}:a"] for i in range(1, 5)), [])
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "testsrc=duration=3:size=320x180:rate=30"] + sines + maps
                   + ["-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", four],
                   check=True, timeout=120)
    win = _window(qapp, four, tmp_path)
    try:
        win.resize(1200, 935)
        _pump(qapp, lambda: False, 0.3)
        assert win.side.width() == qt_clip.SIDE_W and win.side.isAncestorOf(win.tools)
        assert win.side.isAncestorOf(win.save_btn) and win.side.isAncestorOf(win.mix_label)
        assert not win.side.isAncestorOf(win.preview) and not win.side.isAncestorOf(win.sound_box)
        side_x = win.side.mapTo(win, win.side.rect().topLeft()).x()
        assert win.preview.mapTo(win, win.preview.rect().topRight()).x() < side_x          # the picture left of it
        assert win.preview.height() <= win.preview.width() * 180 / 320 + 8                # no empty bands (16:9)
        assert win.tools.widget(0).isAncestorOf(win.mark_btn) and win.tools.widget(0).isAncestorOf(win.watch_btn)
        shown = [k for k in win.mix_boxes if win.mix_boxes[k].isVisibleTo(win)]
        box_y = [win.mix_boxes[k].mapTo(win, win.mix_boxes[k].rect().topLeft()).y() for k in shown]
        assert len(shown) >= 3 and len(set(box_y)) == len(box_y)                          # one source per line
        for w in win.findChildren(QWidget):
            if isinstance(w, (QPushButton, QCheckBox)) and w.isVisibleTo(win):
                assert w.window() is win
                r = w.rect().translated(w.mapTo(win, w.rect().topLeft()))
                assert win.rect().contains(r), (w.text(), r)                                # nothing cut off
        for i in range(win.tools.count()):                                                  # every tab fits
            win.tools.setCurrentIndex(i)
            _pump(qapp, lambda: False, 0.05)
            page = win.tools.currentWidget()
            for w in page.findChildren(QPushButton):
                if w.isVisibleTo(page):
                    r = w.rect().translated(w.mapTo(page, w.rect().topLeft()))
                    assert page.rect().contains(r), (i, w.text())
    finally:
        win.close()
    compact = qt_clip.ClipWindow(clip, [], str(tmp_path / "Clips"), sound=False, compact=True)
    try:
        assert not hasattr(compact, "side") and not hasattr(compact, "tools")              # beside the table as before
        assert compact.sound_box.window() is compact and compact.expand_btn is not None
    finally:
        compact.close()


@pytest.fixture(scope="module")
def bordered(tmp_path_factory):
    """1.12.6: a round like the user's – the game picture centred in the video, black on all four sides (the OBS
    source smaller than the canvas): 224×112 of game at (48, 34) in 320×180."""
    path = str(tmp_path_factory.mktemp("border") / "2026-10-26 08-06 Blood Lodge – The Hillbilly.mp4")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                    "-i", "testsrc=duration=6:size=224x112:rate=30", "-f", "lavfi", "-i", "sine=frequency=440:duration=6",
                    "-vf", "pad=320:180:48:34:black", "-c:v", "libx264", "-preset", "veryfast", "-g", "30",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", path], check=True, timeout=120)
    return path


def test_black_borders_of_a_round_are_found_shown_large_and_cut_in_the_big_editor(qapp, bordered, tmp_path):
    """1.12.6 (user's screenshot of the big editor: the round small in a big black box, the strip in slivers): the
    borders are found from the strip, „Ohne schwarze Ränder“ is picked – the preview shows the game part filling
    the box, the clip is saved without the borders, the strip keeps the picture's shape. Boxes drawn on the zoomed
    picture are fractions of the whole one; the hidden border takes no clicks. „Kein Ausschnitt“ shows it all again,
    a frame moved by hand is „Frei“."""
    from PySide6.QtCore import QRectF, Qt
    from PySide6.QtTest import QTest
    from fogscout import clipedit
    win = _window(qapp, bordered, tmp_path)
    try:
        win.resize(1200, 800)
        assert _pump(qapp, lambda: win._content is not None)
        x, y, w, h = win._content
        assert x * 320 == pytest.approx(48, abs=2.5) and (x + w) * 320 == pytest.approx(272, abs=2.5)
        assert y * 180 == pytest.approx(34, abs=2.5) and (y + h) * 180 == pytest.approx(146, abs=2.5)
        assert x * 320 >= 48 and (x + w) * 320 <= 272                      # inside: no black line left in the clip
        assert win.crop_box.currentData() == "content" and not win.content_hint.isHidden()
        assert win.preview.view == win.preview.crop == win._content == win.edit_plan().crop
        _pump(qapp, lambda: False, 0.2)
        vr, area = win.preview.view_rect(), QRectF(win.preview.rect()).adjusted(2, 2, -2, -2)
        assert abs(vr.width() - area.width()) < 1.5 or abs(vr.height() - area.height()) < 1.5      # fills the box
        assert vr.width() / vr.height() == pytest.approx(224 / 112, rel=0.05)
        tiles = win.timeline.tiles()
        assert len(tiles) >= 3
        for t, _i in tiles[:-1]:                                            # the strip: the game part's shape
            assert t.width() / t.height() == pytest.approx(224 / 112, rel=0.05)
        win.preview.set_editing(True)
        _drag(win.preview, (0.3, 0.3), (0.5, 0.5))
        assert win.preview.boxes[-1] == pytest.approx([0.3, 0.3, 0.2, 0.2], abs=0.01)
        n = len(win.preview.boxes)
        _drag(win.preview, (0.05, 0.5), (0.1, 0.6))                         # in the hidden border: nothing
        assert len(win.preview.boxes) == n
        win.preview.set_editing(False)
        win.crop_box.setCurrentIndex(win.crop_box.findData("none"))
        assert win.preview.view is None and win.edit_plan().crop is None
        win.crop_box.setCurrentIndex(win.crop_box.findData("content"))
        assert win.preview.view == win._content
        QTest.mouseClick(win.crop_btn, Qt.LeftButton)                       # the frame tool: the whole picture
        assert win.preview.crop_edit and win.preview.view is None
        cx, cy = x + w / 2, y + h / 2
        _drag(win.preview, (cx, cy), (cx + 0.03, cy))
        assert win.crop_box.currentData() == "free" and win.preview.crop[0] == pytest.approx(x + 0.03, abs=0.01)
        QTest.mouseClick(win.crop_btn, Qt.LeftButton)
        assert not win.preview.crop_edit and win.preview.view is None       # „Frei“ shows the frame on the picture
    finally:
        win.close()
    out = str(tmp_path / "cut.mp4")
    ok, why = clipedit.export(bordered, clipedit.Edit([clipedit.Part(0.0, 2.0)], crop=(x, y, w, h)), out, "exact", FF)
    assert ok, why
    info = clipedit.probe(out, FF)
    assert info.width == pytest.approx(224, abs=4) and info.height == pytest.approx(112, abs=4)


def test_without_borders_nothing_is_cut_and_the_compact_editor_shows_what_it_saves(qapp, clip, bordered, tmp_path):
    """1.12.6: a round without borders gets no „Ohne schwarze Ränder“; the compact editor (no crop there) keeps
    the whole picture in its preview – only its strip shows the game part."""
    from fogscout import qt_clip
    win = _window(qapp, clip, tmp_path)
    try:
        assert _pump(qapp, lambda: win._load_state["strip"])
        _pump(qapp, lambda: False, 0.2)
        assert win._content is None and win.crop_box.findData("content") < 0
        assert win.crop_box.currentData() == "none" and win.preview.view is None
        assert win.content_hint.isHidden()
    finally:
        win.close()
    compact = qt_clip.ClipWindow(bordered, [], str(tmp_path / "Clips"), sound=False, compact=True)
    compact.show()
    try:
        assert _pump(qapp, lambda: compact._content is not None)
        assert compact.timeline.view == compact._content
        assert compact.preview.view is None and compact.edit_plan().crop is None
    finally:
        compact.close()
