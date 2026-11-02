"""1.19 (user: "Bild & Effekte", je Clip): colour, zoom, stills and clips played backwards – the model (clipedit,
sequence, project format 3), the ffmpeg graph and a real export. The export test is skipped without
imageio-ffmpeg."""
import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import clipedit, obsrec, project, sequence  # noqa: E402
from fogscout.clipedit import Part  # noqa: E402

FF = obsrec.ffmpeg_exe()


def test_values_are_held_inside_their_ranges():
    assert clipedit.clean_color((0, 1, 1)) is None                                  # changes nothing
    assert clipedit.clean_color((2, 9, -1)) == (0.5, 2.0, 0.0)
    assert clipedit.clean_color(("x", 1, 1)) is None and clipedit.clean_color((float("nan"), 1, 1)) is None
    assert clipedit.clean_zoom(((0, 0, 1, 1), (0, 0, 1, 1))) is None
    assert clipedit.clean_zoom(((0.9, 0.9, 0.5, 0.5), (0, 0, 0.01, 0.01))) == ((0.5, 0.5, 0.5, 0.5),
                                                                              (0.0, 0.0, 0.1, 0.1))
    assert clipedit.zoom_at(((0, 0, 1, 1), (0.5, 0.5, 0.5, 0.5)), 0.5) == (0.25, 0.25, 0.75, 0.75)


def test_the_reverse_limit_follows_the_picture_size():
    """Measured: ffmpeg's reverse holds ~430 MB per second of 3440x1440@60 – the limit keeps it near 1.5 GB."""
    big = clipedit.Info(60, 3440, 1440, 60.0, 1)
    assert clipedit.reverse_max_s(big) == 3.0
    assert clipedit.reverse_max_s(clipedit.Info(60, 1920, 1080, 60.0, 1)) == 8.0
    assert clipedit.reverse_max_s(clipedit.Info(60, 7680, 4320, 120.0, 1)) == clipedit.REVERSE_FLOOR_S


def test_a_still_and_a_backwards_clip_move_the_clocks():
    parts = [Part(0, 4), Part(10, 14, reverse=True)]
    parts, j = sequence.insert_hold(parts, 2.0, 3.0)
    assert j == 1 and [round(sequence.length(p), 2) for p in parts] == [2.0, 3.0, 2.0, 4.0]
    assert parts[1].hold == 3.0 and parts[1].start == parts[1].end == 2.0
    assert sequence.duration(parts) == 11.0
    assert sequence.source_at(parts, 3.5) == (1, 2.0)                   # the still shows one moment
    assert sequence.source_at(parts, 7.0) == (3, 14.0)                  # backwards: starts at its end
    assert sequence.source_at(parts, 10.0) == (3, 11.0)
    assert sequence.output_at(parts, 3, 11.0) == pytest.approx(10.0)
    assert sequence.split(parts, 3.5) == (parts, None)                  # a still is not split


def test_splitting_keeps_effects_and_shares_the_zoom_ride():
    zoom = ((0.0, 0.0, 1.0, 1.0), (0.5, 0.5, 0.5, 0.5))
    parts, j = sequence.split([Part(0, 10, color=(0.1, 1.2, 1.0), zoom=zoom)], 5.0)
    assert j == 1 and all(p.color == (0.1, 1.2, 1.0) for p in parts)
    assert parts[0].zoom == ((0.0, 0.0, 1.0, 1.0), (0.25, 0.25, 0.75, 0.75)) == (zoom[0], parts[1].zoom[0])
    back, _j = sequence.split([Part(0, 10, reverse=True)], 2.0)
    assert [(p.start, p.end) for p in back] == [(8.0, 10.0), (0.0, 8.0)]     # the later source plays first
    assert sequence.duration(back) == 10.0


def test_a_project_keeps_the_effects_and_old_projects_load_without():
    zoom = ((0.0, 0.0, 1.0, 1.0), (0.2, 0.2, 0.5, 0.5))
    st = sequence.EditState([Part(1, 5, 2.0, color=(0.1, 1.3, 0.8), zoom=zoom, reverse=True),
                             Part(5, 5, hold=2.5)])
    content = project.content_dict(st, {"name": "fx"})
    d = project.to_dict2(content, "a" * 32, {}, {}, None)
    assert d["version"] == project.CURRENT == 3
    back, _extra, _view, notes = project.validate(json.loads(json.dumps(d)), 60.0, [])
    assert notes == [] and back.parts == st.parts
    old = {"format": project.FORMAT, "version": 2, "parts": [[1, 5, 1.0]]}
    parts = project.validate(old, 60.0, [])[0].parts
    assert parts == [Part(1, 5, 1.0)] and not clipedit.has_effects(parts[0])
    plain = sequence.EditState([Part(1, 5)])                            # no effects: the same content hash as 1.18
    assert project.content_dict(plain)["parts"] == [[1, 5, 1.0]]
    bad = {"format": project.FORMAT, "version": 3,
           "parts": [[1, 5, 1.0, {"color": [9, 9, 9], "zoom": "x", "reverse": "yes", "hold": -1}],
                     [70, 70, 1.0, {"hold": 99}]]}
    got = project.validate(bad, 60.0, [])[0].parts
    assert got[0] == Part(1, 5, 1.0, color=(0.5, 2.0, 2.0))
    assert got[1].hold == clipedit.HOLD_MAX_S and got[1].start == 60.0 - clipedit.HOLD_READ_S


def test_the_graph_applies_each_effect_per_clip():
    info = clipedit.Info(20.0, 320, 180, 30.0, 1)
    zoom = ((0.0, 0.0, 1.0, 1.0), (0.5, 0.5, 0.5, 0.5))
    edit = clipedit.Edit([Part(1, 3, color=(0.1, 1.2, 0.5)), Part(4, 6, zoom=zoom, reverse=True), Part(7, 7, hold=2.0)])
    assert not edit.simple() and edit.seconds() == 6.0
    g, _v, a, _enc = clipedit.edit_graph(edit, info, "exact")
    assert "eq=brightness=0.100:contrast=1.200:saturation=0.500" in g
    assert "eval=frame" in g and "]reverse,setpts" in g and "areverse," in g
    assert "trim=end_frame=1,loop=loop=59:size=1:start=0" in g
    assert "volume=0,apad=whole_dur=2.000,atrim=duration=2.000" in g and a == "[aend]"
    # backwards, the zoom rides from its end box at the source's end: the boxes swap in source time
    assert "(0.50000+(-0.50000)*" in g
    assert not clipedit.Edit([Part(1, 3, color=(0.1, 1.0, 1.0))]).simple()


@pytest.mark.skipif(FF is None, reason="imageio-ffmpeg not installed")
def test_a_real_export_with_every_effect(tmp_path):
    src = str(tmp_path / "src.mp4")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "testsrc2=size=320x180:rate=30:duration=10", "-f", "lavfi", "-i", "sine=frequency=440:duration=10",
                    "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", src],
                   check=True, timeout=120)
    info = clipedit.probe(src, FF)
    zoom = ((0.0, 0.0, 1.0, 1.0), (0.25, 0.25, 0.5, 0.5))
    edit = clipedit.Edit([Part(0, 2, color=(-0.3, 1.0, 0.0)), Part(3, 5, zoom=zoom, reverse=True),
                          Part(6, 6, hold=1.5), Part(6, 8, 2.0)])
    out = str(tmp_path / "out.mp4")
    ok, why = clipedit.export(src, edit, out, "exact", FF, info=info)
    assert ok, why
    got = clipedit.probe(out, FF)
    assert got.duration == pytest.approx(edit.seconds(), abs=0.25) and (got.width, got.height) == (320, 180)
    first = clipedit.frame_at(out, 0.5, 180, got, FF)
    r, g, b = first.convert("RGB").resize((1, 1)).getpixel((0, 0))
    assert max(r, g, b) - min(r, g, b) < 8                              # saturation 0: grey
    a, b_ = clipedit.frame_at(out, 4.3, 180, got, FF), clipedit.frame_at(out, 5.2, 180, got, FF)
    assert _diff(a, b_) < 2.0                                           # the still does not move
    c, d = clipedit.frame_at(out, 2.2, 180, got, FF), clipedit.frame_at(out, 3.8, 180, got, FF)
    assert _diff(c, d) > 2.0                                            # the zoomed clip does


def _diff(a, b) -> float:
    from PIL import ImageChops, ImageStat
    return sum(ImageStat.Stat(ImageChops.difference(a.convert("RGB"), b.convert("RGB"))).mean) / 3


# ---- the editor (offscreen)
@pytest.fixture(scope="module")
def clip(tmp_path_factory):
    if FF is None:
        pytest.skip("imageio-ffmpeg not installed")
    path = str(tmp_path_factory.mktemp("fx") / "2026-11-02 20-00 Haddonfield – Myers.mkv")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                    "-i", "testsrc=duration=12:size=320x180:rate=30", "-f", "lavfi", "-i", "sine=frequency=440:duration=12",
                    "-c:v", "libx264", "-preset", "veryfast", "-g", "30", "-pix_fmt", "yuv420p", "-c:a", "aac",
                    "-shortest", path], check=True, timeout=120)
    return path


@pytest.fixture
def win(clip, tmp_path):
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_editor, qt_window
    app = qt_window.application()
    w = qt_editor.EditorWindow(clip, [], str(tmp_path / "Clips"), sound=False)
    w.resize(1400, 860)
    w.show()
    assert _pump(app, lambda: w.preview._img is not None and (w.loading is None or w.loading.finished)
                 and w._pstate != "loading")
    w.app = app
    yield w
    w._closing_asked = True
    w.close()


def _pump(app, until, seconds=30):
    import time
    end = time.time() + seconds
    while time.time() < end and not until():
        app.processEvents()
        time.sleep(0.01)
    return until()


def test_colour_per_clip_one_undo_step_per_drag_and_to_all_clips(win):
    win.goto(6.0)
    win.split_at_playhead()
    win.timeline.select(0)
    win._clip_selected(0)
    assert win.sections["fx"].isVisibleTo(win)
    steps = len(win.history._past)
    for v in (-10, -20, -30):                                            # one drag of the slider
        win.fx_sliders["brightness"].setValue(v)
    win.fx_sliders["saturation"].setValue(0)
    assert win.parts[0].color == (-0.3, 1.0, 0.0) and win.parts[1].color is None
    assert len(win.history._past) == steps + 1                            # the drag and the next slider: one step each
    win._color_to_all()
    assert all(p.color == (-0.3, 1.0, 0.0) for p in win.parts)
    win.undo()
    assert win.parts[1].color is None and win.parts[0].color == (-0.3, 1.0, 0.0)
    assert win.edit_plan().parts[0].color == (-0.3, 1.0, 0.0)            # what is exported keeps it


def test_p_puts_a_still_in_and_playback_runs_through_it(win):
    win.goto(3.0)
    win.keyPressEvent(_key("P"))
    assert [p.hold for p in win.parts] == [0.0, 2.0, 0.0] and win.timeline.selection == 1
    from fogscout.qt_timeline import clip_label
    assert "Standbild 2 s" in clip_label(1, win.parts[1])
    assert win.timeline.total() == pytest.approx(win.info.duration + 2.0, abs=0.01)
    win.hold_box.setCurrentIndex(win.hold_box.findData(1.0))
    assert win.parts[1].hold == 1.0
    win.goto(2.5)
    win.toggle_play()
    assert _pump(win.app, lambda: win.pos > 4.5 or not win.playing, 20)   # through the still into the next clip
    win.toggle_play() if win.playing else None
    win.undo()
    win.undo()
    assert len(win.parts) == 1


def test_the_zoom_frame_sets_the_clips_boxes_and_leaves_the_crop_alone(win):
    win.timeline.select(0)
    win._clip_selected(0)
    win._zoom_tool(0)
    assert win._zoom_edit == (0, 0) and win.preview.crop_edit
    win.preview.crop = (0.25, 0.25, 0.5, 0.5)
    win.preview.crop_changed.emit()
    assert win.parts[0].zoom == ((0.25, 0.25, 0.5, 0.5), (0.0, 0.0, 1.0, 1.0))
    assert win._state().crop is None                                     # the borrowed frame is no clip crop
    win._zoom_tool(1)
    assert win._zoom_edit == (0, 1)
    win.zoom_still.setChecked(True)
    win.preview.crop = (0.1, 0.1, 0.5, 0.5)
    win.preview.crop_changed.emit()
    assert win.parts[0].zoom[0] == win.parts[0].zoom[1] == (0.1, 0.1, 0.5, 0.5)
    win._escape()                                                        # Esc ends the zoom frame first
    assert win._zoom_edit is None and not win.preview.crop_edit and win.preview.crop is None
    win._timeline_pick("fx_clear", 0.0, 0)
    assert win.parts[0].zoom is None


def test_backwards_only_up_to_the_limit(win, monkeypatch):
    win.timeline.select(0)
    win._clip_selected(0)
    monkeypatch.setattr(clipedit, "reverse_max_s", lambda info: 5.0)
    win._fx_show()
    assert not win.reverse_box.isEnabled() and "5 s" in win.reverse_hint.text()     # 12 s clip
    win.goto(4.0)
    win.split_at_playhead()
    win.timeline.select(0)
    win._clip_selected(0)
    assert win.reverse_box.isEnabled()
    win.reverse_box.setChecked(True)
    assert win.parts[0].reverse and not win.parts[1].reverse
    win.goto(1.0)
    seg = win._segments()[0]
    assert seg[4].reverse and seg[:2] == (0.0, pytest.approx(3.0))         # backwards: the source up to here


def _key(ch):
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QKeyEvent
    return QKeyEvent(QKeyEvent.Type.KeyPress, getattr(Qt, f"Key_{ch}"), Qt.NoModifier, ch.lower())
