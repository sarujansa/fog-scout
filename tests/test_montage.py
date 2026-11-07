"""1.22 (user: "Mehrere Aufnahmen" → Montage: Clips aus verschiedenen Runden hintereinander, eigene Liste
„Montagen“, Format wie die erste Aufnahme): parts of several recordings (Part.src), project format 6, the export
graph (each part fitted to the first recording's picture, silence for a recording without sound), a real export of
two different recordings, and the editor/app. Real ffmpeg / Qt parts are skipped without imageio-ffmpeg / PySide6."""
import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import annotate, clipedit, obsrec, project, sequence  # noqa: E402
from fogscout.clipedit import Part  # noqa: E402

FF = obsrec.ffmpeg_exe()


def test_a_clip_keeps_its_recording_through_split_hold_and_move():
    parts = [Part(0, 4), Part(10, 14, src=1)]
    out, j = sequence.split(parts, 6.0)
    assert [p.src for p in out] == [0, 1, 1] and (out[1].end, out[2].start) == (12.0, 12.0)
    out, j = sequence.insert_hold(parts, 5.0, 2.0)
    assert out[j].src == 1 and out[j].hold == 2.0
    assert [p.src for p in sequence.move(parts, 1, 0)] == [1, 0]
    assert sequence.occurrences(parts, 2.0) == [2.0] and sequence.occurrences(parts, 12.0, source=1) == [6.0]
    assert sequence.occurrences(parts, 2.0, source=1) == []
    st = sequence.EditState(parts, sources=["a.mkv", "b.mkv"])
    assert st.copy().sources == ["a.mkv", "b.mkv"] and st.copy().sources is not st.sources


def test_format_6_keeps_the_montage_and_a_single_recording_keeps_its_hash():
    shape = annotate.Shape("arrow", [(0.1, 0.1), (0.3, 0.3)], t0=11.0, t1=13.0, src=1)
    st = sequence.EditState([Part(0, 4), Part(10, 14, src=1)], shapes=[shape], sources=["a.mkv", "b.mkv"])
    d = project.to_dict2(project.content_dict(st, {"name": "m"}), "a" * 32, {"kind": "montage"}, {}, None)
    assert d["version"] == project.CURRENT == 7 and d["sources"] == ["a.mkv", "b.mkv"]    # 1.39.1: format 7
    back = project.validate(json.loads(json.dumps(d)), 60.0, [], durations=[60.0, 12.0])[0]
    assert [(p.start, p.end, p.src) for p in back.parts] == [(0.0, 4.0, 0), (10.0, 12.0, 1)]   # held to its file
    assert back.shapes[0].src == 1 and back.shapes[0].t1 == 12.0 and back.sources == ["a.mkv", "b.mkv"]
    plain = sequence.EditState([Part(0, 4)])
    assert "sources" not in project.content_dict(plain)
    d["parts"].append([1, 2, 1.0, {"src": 7}])                        # a clip of no recording of the montage
    assert len(project.validate(d, 60.0, [], durations=[60.0, 12.0])[0].parts) == 2
    assert project.file_name_montage("Beste Runden: Nurse", "f" * 32).startswith("Beste Runden_ Nurse--ffffffffff")


def test_one_recording_gives_the_old_graph_and_a_montage_fits_each_part():
    info = clipedit.Info(60.0, 640, 272, 30.0, 1)
    one = clipedit.edit_graph(clipedit.Edit([Part(0, 2), Part(4, 6)]), info)[0]
    assert "pad=" not in one and "anullsrc" not in one and "aresample" not in one
    assert [g[:3] for g in clipedit.source_inputs([Part(0, 2), Part(4, 6)])] == \
        [(0, a, b) for a, b, _m in clipedit.part_inputs([Part(0, 2), Part(4, 6)])]
    small = clipedit.Info(30.0, 320, 180, 25.0, 0)                  # another size and rate, no sound
    edit = clipedit.Edit([Part(0, 2), Part(3, 5, src=1), Part(4, 6)], sources=["a", "b"])
    g, _v, a, _enc = clipedit.edit_graph(edit, info, infos=[info, small])
    assert [(s, m) for s, _a, _b, m in clipedit.source_inputs(edit.parts)] == [(0, [0, 2]), (1, [1])]   # per file
    assert "[1:v]scale=640:272:force_original_aspect_ratio=decrease" in g and "pad=640:272" in g
    assert "fps=30,format=yuv420p[vn1]" in g and "anullsrc=r=48000:cl=stereo,atrim=duration=2.000[a1]" in g
    assert "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[an0]" in g and a == "[aend]"
    shape_inputs = [(3, None, None, 0, 0, 1)]                       # drawn on the second recording only
    g = clipedit.edit_graph(edit, info, shape_inputs=shape_inputs, infos=[info, small])[0]
    assert g.count("[3:v]overlay") == 1 and "[vn1]" in g
    assert not clipedit.Edit([Part(3, 5, src=1)]).simple()


def _video(path, size, rate, seconds, sound=True):
    a = ["-f", "lavfi", "-i", f"sine=duration={seconds}"] if sound else []
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    f"testsrc2=size={size}:rate={rate}:duration={seconds}", *a, "-c:v", "libx264", "-preset",
                    "ultrafast", "-pix_fmt", "yuv420p", *(["-c:a", "aac", "-shortest"] if sound else []), path],
                   check=True, timeout=120)


@pytest.mark.skipif(FF is None, reason="imageio-ffmpeg not installed")
def test_a_real_montage_of_two_different_recordings(tmp_path):
    a, b = str(tmp_path / "a.mp4"), str(tmp_path / "b.mp4")
    _video(a, "640x272", 30, 4)
    _video(b, "320x180", 25, 4, sound=False)
    edit = clipedit.Edit([Part(0, 2), Part(1, 3, src=1), Part(2, 3, 2.0)], sources=[a, b])
    out = str(tmp_path / "m.mp4")
    ok, why = clipedit.export(a, edit, out, "exact", FF)
    assert ok, why
    got = clipedit.probe(out, FF)
    assert (got.width, got.height, round(got.fps)) == (640, 272, 30) and got.audio_tracks == 1
    assert got.duration == pytest.approx(4.5, abs=0.2)
    mid = clipedit.frame_at(out, 3.0, 272, got, FF)                    # the second recording, fitted with borders
    assert max(mid.getpixel((5, 136))) < 30 and max(mid.getpixel((320, 136))) > 30
    edit = clipedit.Edit([Part(0, 2), Part(1, 3, src=1)], sources=[a, str(tmp_path / "weg.mp4")])
    ok, why = clipedit.export(a, edit, str(tmp_path / "x.mp4"), "exact", FF)
    assert not ok and "weg.mp4" in why


def test_the_hasher_answers_every_window_that_asked_for_a_file(tmp_path):
    from fogscout import filehash
    f = tmp_path / "rec.mkv"
    f.write_bytes(b"x" * 1000)
    h = filehash.Hasher(filehash.Cache(str(tmp_path / "cache.json")))
    got = []
    h.request(str(f), lambda r: got.append(("a", r["kind"])))
    h.request(str(f), lambda r: got.append(("b", r["kind"])))       # the same file again: both get the answer
    assert len(h._jobs) == 1
    h.start()
    import time
    end = time.time() + 30
    while len(got) < 2 and time.time() < end:
        time.sleep(0.01)
    h.stop()
    assert sorted(got) == [("a", "done"), ("b", "done")]


# ---- the editor
@pytest.fixture
def qapp():
    if FF is None:
        pytest.skip("imageio-ffmpeg not installed")
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_window
    return qt_window.application()


@pytest.fixture
def reg(tmp_path):
    from fogscout import projectsave
    r = projectsave.Registry(data_dir=str(tmp_path / "local"), sleep=lambda s: None)
    yield r
    r.wait_idle(10)
    r.stop()


def _pump(app, until=lambda: False, seconds=60):
    import time
    deadline = time.time() + seconds
    while time.time() < deadline and not until():
        app.processEvents()
        time.sleep(0.01)
    return until()


def _window(app, clip, tmp_path, reg, **kw):
    from fogscout import qt_editor
    win = qt_editor.EditorWindow(clip, [], str(tmp_path / "Clips"), sound=False, registry=reg, **kw)
    win.resize(1400, 860)
    win.show()
    assert _pump(app, lambda: win.preview._img is not None and (win.loading is None or win.loading.finished)
                 and win._pstate != "loading")
    return win


def _montage_files(tmp_path):
    folder = tmp_path / "Clips" / project.MONTAGE_DIR
    return sorted(str(folder / n) for n in os.listdir(folder) if n.endswith(project.EXT)) if folder.is_dir() else []


def test_a_drop_on_v1_makes_a_montage_that_saves_and_opens_again(qapp, tmp_path, reg):
    a = str(tmp_path / "2026-11-02 21-00 Midwich – Pinhead.mp4")
    b = str(tmp_path / "2026-11-02 21-30 Ormond – Nurse.mp4")
    _video(a, "320x180", 30, 6)
    _video(b, "320x180", 30, 5)
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", b, "-vf", "negate", "-c:a", "copy",
                    str(tmp_path / "neg.mp4")], check=True, timeout=120)
    os.replace(str(tmp_path / "neg.mp4"), b)                                # a picture unlike the first one's
    win = _window(qapp, a, tmp_path, reg)
    try:
        win.timeline.dropped.emit(b)
        assert _pump(qapp, lambda: len(win.parts) == 2)
        assert win._montage and win.sources == [a, b] and win.parts[1].src == 1
        assert win.timeline.source_duration(1) == pytest.approx(5.0, abs=0.2)
        assert win.notice.key == "montage"
        first = win.preview._img.copy()
        win.goto(7.0)                                                       # inside the second recording's clip
        assert _pump(qapp, lambda: win.preview._img is not None and win.preview._img != first)
        plan = win.edit_plan()
        assert plan.sources == [a, b] and plan.montage()
        win.undo()
        assert len(win.parts) == 1 and win._montage
        win.redo()
        assert _pump(qapp, lambda: len(_montage_files(tmp_path)) == 1 and win._slot.written_seq >= win._slot.latest_seq)
        saved = _montage_files(tmp_path)[0]
        with open(saved, encoding="utf-8") as fh:
            data = json.load(fh)
        assert data["version"] == project.CURRENT and data["sources"] == [a, b] and data["source"]["kind"] == "montage"
        assert not os.path.isdir(tmp_path / "Clips" / project.PROJECT_DIR) or \
            not any(n.endswith(project.EXT) for n in os.listdir(tmp_path / "Clips" / project.PROJECT_DIR))
    finally:
        win._closing_asked = True
        win.close()
        _pump(qapp, seconds=0.1)
    reg.wait_idle(10)
    again = _window(qapp, a, tmp_path, reg, montage_file=saved)
    try:
        assert _pump(qapp, lambda: again._montage and len(again.parts) == 2)
        assert again.sources == [a, b] and again.parts[1].src == 1 and again.save_btn.isEnabled()
    finally:
        again._closing_asked = True
        again.close()
        _pump(qapp, seconds=0.1)
    reg.wait_idle(10)
    os.rename(b, b + ".weg")                                                # the second recording is gone
    gone = _window(qapp, a, tmp_path, reg, montage_file=saved)
    try:
        assert _pump(qapp, lambda: gone._montage and len(gone.parts) == 2)
        assert gone._missing == {1} and not gone.save_btn.isEnabled() and gone.notice.key == "src_missing"
        gone.timeline.select(1)
        gone.delete_selected()                                              # without its clips: export again
        assert gone.save_btn.isEnabled()
    finally:
        gone._closing_asked = True
        gone.close()
        _pump(qapp, seconds=0.1)
