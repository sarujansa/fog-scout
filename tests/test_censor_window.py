"""1.41: censor boxes for a while – [x, y, w, h, t0, t1] with t0/t1 in seconds of the recording (like the drawings'
times): the export hides them only then (ffmpeg enable, a still: in or out), the preview shows them only then, the
project keeps the window (format 8) and drops a box with a broken one, the editor sets it at the playhead."""
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import clipedit, obsrec, project, sequence  # noqa: E402
from fogscout.clipedit import Part  # noqa: E402

FF = obsrec.ffmpeg_exe()


def test_a_box_with_a_window_hides_only_then_in_the_graph():
    always, later = [0.0, 0.0, 0.5, 0.5], [0.5, 0.5, 0.25, 0.25, 12.0, 20.0]
    assert clipedit.box_window(always) is None and clipedit.box_window(later) == (12.0, 20.0)
    assert clipedit.box_active(later, 12.0) and clipedit.box_active(later, 20.0) and not clipedit.box_active(later, 21)
    g = clipedit.censor_graph([always, later], "black", 320, 180, base=10.0)
    assert "drawbox=x=0:y=0:w=160:h=90:color=black:t=fill[c0]" in g               # no window: no enable
    assert "t=fill:enable='between(t,2.000,10.000)'[c1]" in g                     # seconds of this input
    g = clipedit.censor_graph([later], "pixel", 320, 180, base=15.0)
    assert "overlay=160:90:enable='between(t,0.000,5.000)'" in g                  # started inside: from 0
    assert "delogo" in clipedit.censor_graph([later], "retouch", 320, 180) and \
        ":enable='between(t,12.000,20.000)'" in clipedit.censor_graph([later], "retouch", 320, 180)
    assert "drawbox" not in clipedit.censor_graph([later], "black", 320, 180, still_at=5.0)   # a still before it
    assert "enable" not in clipedit.censor_graph([later], "black", 320, 180, still_at=15.0)   # a still inside it
    assert clipedit.boxes_in([always, later], 0, 12) == [always]                  # ends where the window starts
    assert clipedit.boxes_in([always, later], 19, 30) == [always, later]
    assert clipedit.boxes_in([always, later], 25, 25, still=True) == [always]


def test_the_project_keeps_the_window_and_drops_a_box_with_a_broken_one():
    st = sequence.EditState([Part(0, 30)], boxes=[[0.1, 0.1, 0.2, 0.2], [0.5, 0.5, 0.2, 0.2, 4.0, 9.5]],
                            censor_on=True)
    data = project.to_dict2(project.content_dict(st, {}), "pid", {}, {}, None)
    assert data["version"] == project.CURRENT == project.VERSION8
    data["censor"]["boxes"] += [[0.1, 0.1, 0.1, 0.1, 9.0, 3.0], [0.1, 0.1, 0.1, 0.1, -1, 3],
                                [0.1, 0.1, 0.1, 0.1, "nan", 3], [0.1, 0.1, 0.1, 0.1, 3]]
    state, _e, _v, _n = project.validate(data, 30.0, [Part(0, 30)])
    assert state.boxes == [[0.1, 0.1, 0.2, 0.2], [0.5, 0.5, 0.2, 0.2, 4.0, 9.5]]
    assert project._box([0.1, 0.1, 0.2, 0.2, 1, 2]) is None                      # a crop never takes a window


@pytest.fixture(scope="module")
def clip(tmp_path_factory):
    if FF is None:
        pytest.skip("imageio-ffmpeg not installed")
    path = str(tmp_path_factory.mktemp("cw") / "2026-11-07 03-10 Coal Tower – Nurse.mkv")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "color=c=white:size=320x180:rate=30:duration=8", "-c:v", "libx264", "-preset", "veryfast",
                    "-g", "30", "-pix_fmt", "yuv420p", path], check=True, timeout=120)
    return path


def _dark(path, t, info):
    img = clipedit.frame_at(path, t, 180, info=info, ffmpeg=FF)
    return sum(img.getpixel((40, 40))) < 60                                      # inside the box's top-left corner


def test_the_export_hides_a_box_only_in_its_window_also_after_a_cut_and_in_a_still(clip, tmp_path):
    info = clipedit.probe(clip, FF)
    box = [0.0, 0.0, 0.5, 0.5, 4.0, 6.0]                                         # seconds 4–6 of the recording
    edit = clipedit.Edit([Part(3.0, 7.0), Part(5.0, 5.0, hold=1.0), Part(1.0, 2.0)])
    out = str(tmp_path / "w.mp4")
    ok, why = clipedit.export(clip, edit, out, "exact", FF, info=info, censor=[box], censor_style="black")
    assert ok, why
    oi = clipedit.probe(out, FF)
    assert not _dark(out, 0.5, oi)                                               # recording 3.5 s: not yet
    assert _dark(out, 2.0, oi)                                                   # recording 5.0 s: hidden
    assert not _dark(out, 3.6, oi)                                               # recording 6.6 s: over
    assert _dark(out, 4.5, oi)                                                   # the still shows 5.0 s: hidden
    assert not _dark(out, 5.5, oi)                                               # recording 1.5 s: never


def test_the_compact_cut_hides_a_box_only_in_its_window(clip, tmp_path):
    info = clipedit.probe(clip, FF)
    out = str(tmp_path / "c.mp4")
    ok, why = clipedit.cut(clip, 2.0, 6.0, out, "exact", FF, info=info, censor=[[0.0, 0.0, 0.5, 0.5, 4.0, 5.0]],
                           censor_style="black")
    assert ok, why
    oi = clipedit.probe(out, FF)
    assert not _dark(out, 1.0, oi) and _dark(out, 2.5, oi) and not _dark(out, 3.6, oi)


# ---- the editor
@pytest.fixture
def qapp():
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_window
    return qt_window.application()


def test_the_editor_limits_the_marked_box_at_the_playhead_with_undo(qapp, clip, tmp_path):
    import time
    from fogscout import qt_editor
    win = qt_editor.EditorWindow(clip, [], str(tmp_path / "Clips"), sound=False)
    win.show()
    deadline = time.time() + 30
    while time.time() < deadline and win.preview._img is None:
        qapp.processEvents()
        time.sleep(0.01)
    try:
        saved = []
        win.on_setting = lambda k, v: saved.append((k, v))
        win.preview.add_box([0.0, 0.0, 0.5, 0.5])
        win.goto(3.0)
        win.box_from_here()
        assert win.preview.boxes[0] == [0.0, 0.0, 0.5, 0.5, 3.0, pytest.approx(info_len(win))]
        win.goto(5.0)
        win.box_until_here()
        assert win.preview.boxes[0] == [0.0, 0.0, 0.5, 0.5, 3.0, 5.0]
        assert "0:05" in win.status.text()
        assert ("clip_censor_boxes", []) in saved                                 # a window is not for the next clip
        win.preview.set_now(6.0)
        assert not clipedit.box_active(win.preview.boxes[0], win.preview.now)
        win.undo()
        assert win.preview.boxes[0][4:] == [3.0, pytest.approx(info_len(win))]
        win.box_always()
        assert win.preview.boxes[0] == [0.0, 0.0, 0.5, 0.5]
        win.goto(0.0)
        win.box_until_here()                                                      # nothing before the start
        assert win.preview.boxes[0] == [0.0, 0.0, 0.5, 0.5]
    finally:
        win.close()


def info_len(win):
    return float(win.info.duration)
