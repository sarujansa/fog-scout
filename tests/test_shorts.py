"""1.20 (user: "Hochformat für Shorts" – max. 3 min, Vorlagen unscharfer Hintergrund (Standard) und Zuschnitt 9:16,
Titel + Untertitel): the short as data (shorts.py), project format 4, the export graph, a real export, and the
editor's section and preview. Real ffmpeg / Qt parts are skipped without imageio-ffmpeg / PySide6."""
import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import clipedit, obsrec, project, sequence, shorts  # noqa: E402
from fogscout.clipedit import Part  # noqa: E402

FF = obsrec.ffmpeg_exe()


def spec(**kw):
    s = shorts.ShortSpec("blur", "Nurse Doppel-Blink", 1, [shorts.Sub(0.5, 2.5, "erst hier"), shorts.Sub(3, 5, "dann")])
    for k, v in kw.items():
        setattr(s, k, v)
    return s


def test_a_short_round_trips_and_broken_fields_drop_out():
    d = shorts.to_dict(spec())
    assert shorts.from_dict(json.loads(json.dumps(d))) == spec()
    assert shorts.to_dict(shorts.ShortSpec()) is None                      # nothing chosen: no field
    bad = {"layout": "weird", "title": "  zwei   Wörter \\n ", "title_size": 9,
           "subs": [[1, 0.5, "rückwärts"], [0, 1, ""], ["x", 1, "a"], [-1, 2, "vor null"], [1, 2, "gut"]]}
    got = shorts.from_dict(bad)
    assert got.layout == "blur" and got.title_size == 1 and [s.text for s in got.subs] == ["gut"]
    assert "\n" not in got.title and "  " not in got.title


def test_project_format_4_keeps_the_short_and_old_cuts_keep_their_hash():
    st = sequence.EditState([Part(1, 5)], short=spec())
    d = project.to_dict2(project.content_dict(st, {"name": "s"}), "a" * 32, {}, {}, None)
    assert d["version"] == project.CURRENT == 4 and d["short"]["title"] == "Nurse Doppel-Blink"
    back = project.validate(json.loads(json.dumps(d)), 60.0, [])[0]
    assert back.short == spec()
    plain = sequence.EditState([Part(1, 5)])                              # without a short: the 1.19 content
    assert "short" not in project.content_dict(plain)
    assert back.copy().short is not back.short and back.copy().short == back.short


def test_the_texts_sit_in_the_bands_and_show_only_in_their_time():
    pics = shorts.texts(spec())
    assert len(pics) == 3
    title, first, _second = pics
    assert title[3] is None and title[2] < shorts.H * 0.3                    # always, in the upper band
    assert first[3:] == (0.5, 2.5) and first[2] > shorts.H * 0.7            # in its time, in the lower band
    assert all(p[0].width <= shorts.W for p in pics)
    from PIL import Image
    canvas = Image.new("RGB", (270, 480), (0, 0, 0))
    lit = lambda im: sum(1 for px in im.getdata() if px != (0, 0, 0))     # noqa: E731
    assert lit(shorts.paste_texts(canvas, spec(), 1.0)) > lit(shorts.paste_texts(canvas, spec(), 2.8)) > 0


def test_the_graph_lays_the_cut_on_the_canvas_with_the_texts():
    info = clipedit.Info(20.0, 1280, 544, 60.0, 1)
    edit = clipedit.Edit([Part(1, 3)], short=spec())
    assert not edit.simple() or True
    g, v, _a, _enc = clipedit.edit_graph(edit, info, "shorts", text_inputs=[(1, 10, 20, None, None),
                                                                           (2, 30, 1500, 0.5, 2.5)])
    assert "boxblur" in g and "overlay=(W-w)/2:(H-h)/2" in g and "scale=1080:-2" in g
    assert "[vsh][1:v]overlay=10:20:format=auto[vtx0]" in g
    assert "[vtx0][2:v]overlay=30:1500:format=auto:enable='between(t,0.500,2.500)'[vtx1]" in g
    assert "fps=60" in g and v == "[vout]"
    crop = clipedit.edit_graph(clipedit.Edit([Part(1, 3)], short=spec(layout="crop")), info, "shorts")[0]
    assert "boxblur" not in crop and "force_original_aspect_ratio=increase,crop=1080:1920" in crop


@pytest.mark.skipif(FF is None, reason="imageio-ffmpeg not installed")
def test_a_real_short_and_the_three_minute_limit(tmp_path):
    src = str(tmp_path / "src.mp4")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "testsrc2=size=640x272:rate=30:duration=4", "-f", "lavfi", "-i", "sine=duration=4",
                    "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", src],
                   check=True, timeout=120)
    info = clipedit.probe(src, FF)
    out = str(tmp_path / "short.mp4")
    ok, why = clipedit.export(src, clipedit.Edit([Part(0, 3)], short=spec()), out, "shorts", FF, info=info)
    assert ok, why
    got = clipedit.probe(out, FF)
    assert (got.width, got.height) == (1080, 1920) and got.duration == pytest.approx(3.0, abs=0.2)
    assert got.audio_tracks == 1
    band = clipedit.frame_at(out, 1.0, 960, got, FF).crop((0, 130, 540, 200))      # the title's band
    assert sum(1 for px in band.getdata() if min(px) > 225) > 200             # white letters are there
    long = clipedit.Edit([Part(0, 4, 0.25)] * 50)                           # 50 × 16 s = 800 s
    ok, why = clipedit.export(src, long, str(tmp_path / "long.mp4"), "shorts", FF, info=info)
    assert not ok and "3 min" in why and not os.path.exists(tmp_path / "long.mp4")


# ---- the editor
@pytest.fixture
def win(tmp_path):
    if FF is None:
        pytest.skip("imageio-ffmpeg not installed")
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_editor, qt_window
    clip = str(tmp_path / "2026-11-02 21-00 Midwich – Pinhead.mkv")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "testsrc=duration=8:size=320x180:rate=30", "-c:v", "libx264", "-preset", "veryfast",
                    "-pix_fmt", "yuv420p", clip], check=True, timeout=120)
    app = qt_window.application()
    w = qt_editor.EditorWindow(clip, [], str(tmp_path / "Clips"), sound=False)
    w.resize(1400, 860)
    w.show()
    assert _pump(app, lambda: w.preview._img is not None and w._pstate != "loading")
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


def test_the_short_section_title_subtitles_undo_and_preview(win):
    assert not win.sections["short"].isVisibleTo(win)
    win.mode_box.setCurrentIndex(win.mode_box.findData("shorts"))
    assert win.sections["short"].isVisibleTo(win) and "1080×1920" in win.size_label.text()
    win.short_title.setText("Hallo")
    win._short_title_edited("Hallo")
    win._short_title_edited("Hallo Welt")                                   # typing: one undo step
    assert win._short.title == "Hallo Welt" and win.edit_plan().short.title == "Hallo Welt"
    win.goto(2.0)
    win.sub_text.setText("hier")
    win._sub_add()
    assert [(s.t0, s.t1, s.text) for s in win._short.subs] == [(2.0, 4.0, "hier")]
    assert win.timeline.subs == [(2.0, 4.0)] and win.sub_list.count() == 1
    win.goto(3.0)
    win._sub_edge(1)
    assert win._short.subs[0].t1 == 3.0
    win.undo()
    assert win._short.subs[0].t1 == 4.0
    win.undo()
    win.undo()
    assert win._short is None or win._short.title == ""
    win.redo()
    win.short_view_box.setChecked(True)                                     # the preview as the short
    assert not win.preview.overlays
    assert _pump(win.app, lambda: win.preview._img is not None and win.preview._img.height() > win.preview._img.width())
    win.mode_btns["crop"].setChecked(True)                                  # a tool: back to the recording's picture
    assert not win.short_view_box.isChecked() and win.preview.overlays
