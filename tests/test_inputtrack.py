"""1.39.1: the input card in the clip editor's export – its changes mapped through the cut (tempo, backwards,
stills, montage sources), laid over the finished picture in output time, never lost to a stream copy."""
import subprocess

import numpy as np
import pytest

from fogscout import clipedit, inputs, inputtrack, obsrec, project, sequence
from fogscout.clipedit import Edit, Info, Part
from fogscout.inputtrack import InputSpec

FF = obsrec.ffmpeg_exe()
W = inputs.encode(inputs.InputState(keys=frozenset({"w"})))
PAD_A = inputs.encode(inputs.InputState(pad=frozenset({"a"})))
EV = [(1.0, W), (2.0, 0), (5.0, PAD_A)]


def test_the_changes_follow_the_cut():
    assert inputtrack.segments([Part(0, 6)], {0: EV}) == [(0.0, 1.0, 0), (1.0, 2.0, W), (2.0, 5.0, 0), (5.0, 6.0, PAD_A)]
    assert inputtrack.segments([Part(0, 6, speed=2.0)], {0: EV}) == [(0.0, 0.5, 0), (0.5, 1.0, W), (1.0, 2.5, 0),
                                                                    (2.5, 3.0, PAD_A)]
    # backwards: the clip starts at its end (pad held) and a press becomes a release
    assert inputtrack.segments([Part(0, 6, reverse=True)], {0: EV}) == [(0.0, 1.0, PAD_A), (1.0, 4.0, 0),
                                                                       (4.0, 5.0, W), (5.0, 6.0, 0)]
    # a still holds its moment; the next clip starts with what was held at its start
    assert inputtrack.segments([Part(1.5, 1.5, hold=2.0), Part(4, 6)], {0: EV}) == [(0.0, 2.0, W), (2.0, 3.0, 0),
                                                                                    (3.0, 4.0, PAD_A)]


def test_a_montage_source_without_inputs_shows_nothing_held():
    segs = inputtrack.segments([Part(0, 3, src=1), Part(0, 3, src=0)], {0: EV})
    assert segs == [(0.0, 4.0, 0), (4.0, 5.0, W), (5.0, 6.0, 0)]


def test_density_and_state_at():
    d = inputtrack.density([(0.1, 1), (0.2, 0), (2.0, 1)], 3.0, per_s=1)
    assert d == [1.0, 0.0, 0.5, 0.0]
    assert inputtrack.state_at(EV, 0.5) == 0 and inputtrack.state_at(EV, 1.0) == W and inputtrack.state_at([], 1) == 0
    assert inputtrack.state_before(EV, 1.0) == 0


def test_auto_follows_the_device_along_the_clip():
    segs = inputtrack.segments([Part(0, 6)], {0: EV})
    assert inputtrack.layouts(segs, "auto") == ["keyboard", "keyboard", "keyboard", "gamepad"]
    assert inputtrack.layouts(segs, "gamepad") == ["gamepad"] * 4


def test_the_card_sits_in_its_corner_and_never_leaves_the_picture():
    x, y, h = inputtrack.card_box(InputSpec(corner="bottom_right", size=20), 1920, 1080)
    assert h == 216 and y + h == 1080 - 22 and x + round(h * inputtrack_ratio()) == 1920 - 22
    x, y, h = inputtrack.card_box(InputSpec(corner="top_left", size=25), 1080, 1920)   # a short: narrower
    assert (x, y) == (38, 38) and round(h * inputtrack_ratio()) <= 1080 - 2 * 38


def inputtrack_ratio():
    from fogscout.overlay_render import INPUT_RATIO
    return INPUT_RATIO


def test_the_spec_reads_back_and_bad_values_take_their_default():
    s = InputSpec(on=True, layout="gamepad", corner="top_left", size=20, backdrop=False)
    assert inputtrack.from_dict(s.to_dict()) == s
    assert inputtrack.from_dict({"on": "yes", "layout": "x", "corner": 3, "size": 999}) == InputSpec(size=25)
    assert inputtrack.from_dict(None) is None


def test_concat_list_names_the_last_picture_twice_and_quotes():
    text = inputtrack.concat_text([("/t/a.png", 1.0), ("/t/it's.png", 0.5)])
    assert text.splitlines() == ["ffconcat version 1.0", "file '/t/a.png'", "duration 1.000",
                                 "file '/t/it'\\''s.png'", "duration 0.500", "file '/t/it'\\''s.png'"]


def test_the_card_makes_a_cut_no_stream_copy_and_lands_after_the_concat():
    plain = Edit([Part(0, 5)])
    off = Edit([Part(0, 5)], inputs=(InputSpec(on=False), {0: EV}))
    on = Edit([Part(0, 5)], inputs=(InputSpec(on=True), {0: EV}))
    none = Edit([Part(0, 5)], inputs=(InputSpec(on=True), {0: []}))
    assert plain.simple() and off.simple() and none.simple() and not on.simple()
    info = Info(10.0, 640, 360, 30.0, 1)
    two = Edit([Part(0, 2), Part(3, 5, speed=2.0)], fade_in=0.5, inputs=on.inputs)
    g, _v, _a, _args = clipedit.edit_graph(two, info, "exact", card_input=(2, 400, 250))
    assert "[vcat][2:v]overlay=400:250:eof_action=pass:format=auto[vin]" in g
    assert g.index("concat=n=2") < g.index("[2:v]overlay") < g.index("fade=t=in")
    g, _v, _a, _args = clipedit.edit_graph(Edit([Part(0, 2)], short=None), info, "shorts", card_input=(1, 10, 20))
    assert g.index("[vsh]") < g.index("[1:v]overlay=10:20")


def test_project_keeps_the_card_and_an_old_cut_its_hash():
    st = sequence.EditState([Part(0, 5)])
    old = project.content_hash(project.content_dict(st, {"name": "x"}))
    assert "inputs" not in project.content_dict(st, {"name": "x"})
    st2 = st.copy()
    st2.inputs = InputSpec(on=True, corner="top_left")
    d = project.to_dict(st2, "", "x", {"name": "x"})
    assert d["inputs"]["corner"] == "top_left"
    back, _extra, _view, _notes = project.validate(d, 5.0, [Part(0, 5)])
    assert back.inputs == st2.inputs and back.copy().inputs == st2.inputs and back.copy().inputs is not back.inputs
    st3 = st2.copy()
    st3.inputs = None
    assert project.content_hash(project.content_dict(st3, {"name": "x"})) == old


@pytest.fixture
def clip(tmp_path):
    p = tmp_path / "round.mkv"
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc=duration=6:size=320x180:rate=30",
                    "-f", "lavfi", "-i", "sine=frequency=440:duration=6", "-c:v", "libx264", "-g", "30", "-c:a", "aac",
                    str(p)], check=True)
    return p


@pytest.mark.skipif(FF is None, reason="imageio-ffmpeg not installed")
@pytest.mark.parametrize("mode", ["exact", "gif"])
def test_a_real_export_shows_the_held_key_at_its_time(clip, tmp_path, mode):
    """Two exports of the same cut – one with W held from 2 s to 4 s, one with nothing held: they differ only in the
    card's box and only while W is held."""
    spec = InputSpec(on=True, layout="keyboard", corner="bottom_right", size=25, backdrop=True)
    ext = ".gif" if mode == "gif" else ".mp4"
    held, idle = tmp_path / ("held" + ext), tmp_path / ("idle" + ext)
    for out, ev in ((held, [(2.0, W), (4.0, 0)]), (idle, [(0.0, 0)])):
        ok, msg = clipedit.export(str(clip), Edit([Part(0, 6)], inputs=(spec, {0: ev or [(0.0, 0)]})), str(out),
                                  mode, FF)
        assert ok, msg
    assert abs(clipedit.probe(str(held), FF).duration - 6.0) < 0.2
    x, y, h = inputtrack.card_box(spec, 320, 180)
    from fogscout.overlay_render import input_card
    lit = np.asarray(input_card(inputs.decode(W), "keyboard", h, None, True), dtype=int)
    dark = np.asarray(input_card(inputs.EMPTY, "keyboard", h, None, True), dtype=int)
    key = np.abs(lit - dark).max(axis=2) > 80                   # the W key's pixels on the card

    def diff(t):                                                # how far apart the two exports are on that key
        a, b = (np.asarray(clipedit.frame_at(str(o), t, 180, ffmpeg=FF), dtype=int) for o in (held, idle))
        d = np.abs(a - b).max(axis=2)[y:y + h, x:x + key.shape[1]]
        return d[key].mean()
    assert key.sum() > 20 and diff(3.0) > 40                    # W lit up
    assert diff(1.0) < 20 and diff(5.0) < 20                    # before and after: the same key


@pytest.mark.skipif(FF is None, reason="imageio-ffmpeg not installed")
def test_a_stream_copy_cut_keeps_its_card(clip, tmp_path):
    spec = InputSpec(on=True, layout="keyboard")
    out = tmp_path / "copy.mp4"
    ok, msg = clipedit.export(str(clip), Edit([Part(1, 5)], inputs=(spec, {0: [(0.0, W)]})), str(out), "copy", FF)
    assert ok, msg
    a = np.asarray(clipedit.frame_at(str(out), 2.0, 180, ffmpeg=FF), dtype=int)
    plain = tmp_path / "plain.mp4"
    clipedit.export(str(clip), Edit([Part(1, 5)]), str(plain), "copy", FF)
    b = np.asarray(clipedit.frame_at(str(plain), 2.0, 180, ffmpeg=FF), dtype=int)
    x, y, h = inputtrack.card_box(spec, 320, 180)
    assert np.abs(a[y:y + h, x:] - b[y:y + h, x:]).mean() > 10          # the card is there, not cut away


# ---- the editor (Qt, real ffmpeg)
def _pump(app, until, seconds=30):
    import time
    end = time.time() + seconds
    while time.time() < end and not until():
        app.processEvents()
        time.sleep(0.01)
    return until()


def _editor(tmp_path, with_inputs):
    if FF is None:
        pytest.skip("imageio-ffmpeg not installed")
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_editor, qt_window
    clip = str(tmp_path / "2026-11-07 20-00 Coal Tower – Nurse.mkv")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "testsrc=duration=8:size=320x180:rate=30", "-c:v", "libx264", "-preset", "veryfast",
                    "-pix_fmt", "yuv420p", clip], check=True, timeout=120)
    if with_inputs:
        with open(clip + inputs.INPUTS_SUFFIX, "wb") as f:
            f.write(inputs.dump([(2.0, W), (4.0, 0)]))
    app = qt_window.application()
    w = qt_editor.EditorWindow(clip, [], str(tmp_path / "Clips"), sound=False)
    w.resize(1400, 860)
    w.show()
    assert _pump(app, lambda: w.preview._img is not None and w._pstate != "loading")
    w.app = app
    return w


def test_the_editor_shows_the_section_only_with_inputs_and_burns_the_card(tmp_path):
    w = _editor(tmp_path, with_inputs=True)
    try:
        assert w.sections["inputs"].isVisibleTo(w) and w.timeline.input_bins[0]
        assert w.edit_plan().inputs is None                          # off until switched on
        w.input_on_box.setChecked(True)
        plan = w.edit_plan()
        assert plan.card_on() and plan.inputs[1] == {0: [(2.0, W), (4.0, 0)]} and not plan.simple()
        assert w._state().inputs.on
        w.input_corner_box.setCurrentIndex(w.input_corner_box.findData("top_left"))
        assert w._input_spec.corner == "top_left"
        w.goto(3.0)                                                   # the preview draws the card with W held
        segs, lays = w._input_track()
        assert segs == [(0.0, 2.0, 0), (2.0, 4.0, W), (4.0, 8.0, 0)] and lays == ["keyboard"] * 3
        from PIL import Image
        base = Image.new("RGB", (320, 180), (0, 0, 0))
        painted = w._input_paint(base)
        x, y, h = inputtrack.card_box(w._input_spec, 320, 180)
        assert painted.getpixel((x + h, y + h // 2)) != (0, 0, 0)
        w.undo()                                                      # the corner back …
        assert w._input_spec.corner == "bottom_right" and w.input_corner_box.currentData() == "bottom_right"
        w.undo()                                                      # … then untouched again (no project field)
        assert w._input_spec is None and not w.input_on_box.isChecked() and w.edit_plan().inputs is None
    finally:
        w._closing_asked = True
        w.close()


def test_the_editor_without_inputs_hides_the_section(tmp_path):
    w = _editor(tmp_path, with_inputs=False)
    try:
        assert not w.sections["inputs"].isVisibleTo(w) and not w.timeline.input_bins
        assert w._state().inputs is None and w.edit_plan().inputs is None
    finally:
        w._closing_asked = True
        w.close()
