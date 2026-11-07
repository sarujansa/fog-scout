"""1.41.1: „Text finden“ – the local detector's boxes joined per line and left out where already hidden, numbered on
the picture; Claude gets only that picture (censored) and answers numbers; the editor shows the finds as suggestions
and takes them as one undo step."""
import json
import os
import subprocess
import sys

import pytest
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import askclaude, obsrec, textfind  # noqa: E402

from test_claude_pictures import KEY, FakeOpener, _decoded, _pump  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
FF = obsrec.ffmpeg_exe()


def test_pieces_of_a_line_join_and_hidden_or_huge_ones_drop():
    found = [(100, 500, 200, 530), (210, 502, 300, 528),          # one line in two pieces, 10 px apart
             (100, 300, 180, 330),                                 # another line
             (0, 0, 1000, 700)]                                    # most of the picture: not text
    boxes = textfind.join(found, 1000, 1000)
    assert len(boxes) == 2 and boxes[0][1] < boxes[1][1]            # reading order
    line = boxes[1]
    assert line[0] == pytest.approx(0.1 - textfind.PAD) and line[0] + line[2] == pytest.approx(0.3 + textfind.PAD)
    assert textfind.join(found, 1000, 1000, existing=[[0.05, 0.45, 0.4, 0.15, 3.0, 9.0]]) == [boxes[0]]
    assert textfind.join([(10, 10, 5, 5)], 100, 100) == [] and textfind.join(found, 0, 0) == []
    many = [(10, 20 * k, 30, 20 * k + 10) for k in range(40)]
    assert len(textfind.join(many, 1000, 1000)) == textfind.MAX_SUGGEST


def test_claude_s_answer_is_numbers_inside_the_list_once():
    assert textfind.parse({"summary": " zwei Namen ", "names": [2, 2, 5, 0, 1, True, "3"]}, 4) == ("zwei Namen", [1, 0])
    with pytest.raises(ValueError):
        textfind.parse({"summary": "x"}, 3)
    pic = textfind.numbered(Image.new("RGB", (400, 200)), [[0.1, 0.5, 0.2, 0.1]])
    assert pic.getpixel((int(0.1 * 400), int(0.55 * 200))) == (255, 0, 255) and pic.size == (400, 200)
    assert pic.getpixel((int(0.3 * 400) + 6, int(0.55 * 200))) != (0, 0, 0)            # the number right of it


def test_the_real_detector_finds_drawn_text():
    pytest.importorskip("onnxruntime")
    pytest.importorskip("cv2")
    finder = textfind.Finder(os.path.join(ROOT, "models"))
    if not finder.available():
        pytest.skip("model not in this checkout")
    img = Image.new("RGB", (1280, 720), (30, 40, 50))
    ImageDraw.Draw(img).text((60, 600), "PlayerOne", fill=(240, 240, 240), font=ImageFont.load_default(size=32))
    boxes = finder.find(img)
    assert len(boxes) == 1 and boxes[0][0] < 60 / 1280 + 0.01 and boxes[0][1] < 600 / 720 + 0.01
    assert finder.find(img, existing=[[0.0, 0.8, 0.5, 0.2]]) == []
    assert not textfind.Finder(os.path.join(ROOT, "nowhere")).available()


# ---- the editor
@pytest.fixture
def qapp():
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_window
    return qt_window.application()


def test_the_editor_suggests_found_text_takes_it_as_one_step_and_claude_keeps_only_names(qapp, tmp_path,
                                                                                         monkeypatch):
    if FF is None:
        pytest.skip("imageio-ffmpeg not installed")
    from fogscout import qt_editor
    clip = str(tmp_path / "2026-11-07 07-00 Coal Tower – Nurse.mkv")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "testsrc=duration=4:size=320x180:rate=15", "-c:v", "libx264", "-preset", "veryfast",
                    "-pix_fmt", "yuv420p", clip], check=True, timeout=120)
    found = [[0.1, 0.1, 0.2, 0.05], [0.5, 0.8, 0.3, 0.06], [0.6, 0.1, 0.1, 0.05]]
    seen = []
    monkeypatch.setattr(textfind.Finder, "available", lambda self: True)
    monkeypatch.setattr(textfind.Finder, "find", lambda self, img, existing=(): (seen.append(img.size), found)[1])
    fake = FakeOpener({"summary": "Ein Name.", "names": [2]})
    monkeypatch.setattr(askclaude, "OPENER", fake)
    win = qt_editor.EditorWindow(clip, [], str(tmp_path / "Clips"), sound=False, models_dir=str(tmp_path))
    win.show()
    try:
        assert _pump(qapp, lambda: win.preview._img is not None and win.history is not None)
        win.preview.clear_boxes()
        win.goto(1.0)
        win.find_text()
        assert _pump(qapp, lambda: not win._text_busy)
        assert seen == [(320, 180)] and win.preview.suggest == found and win.mode == "censor"
        assert win.text_take_btn.isVisibleTo(win) and not win.cl_names_btn.isVisibleTo(win)   # Claude not allowed
        win.claude_key, win.claude_frame = (lambda: KEY), (lambda: True)
        win._censor_hint()
        assert win.cl_names_btn.isVisibleTo(win)
        win.claude_text_names()
        assert _pump(qapp, lambda: not win._claude_busy, 60)
        content = fake.bodies[0]["messages"][0]["content"]
        assert "Coal" not in json.dumps([b for b in content if b["type"] == "text"]) and "mkv" not in json.dumps(
            [b for b in content if b["type"] == "text"])
        assert _decoded(next(b for b in content if b["type"] == "image")).size[0] > 0
        assert win.preview.suggest == [found[1]] and "Ein Name" in win.status.text()
        before = [list(b) for b in win.preview.boxes]
        win.take_text()
        assert win.preview.boxes == before + [found[1]] and win.preview.suggest == [] and win._censor_on
        win.undo()                                                          # one step: boxes and „anwenden“
        assert win.preview.boxes == before and not win._censor_on
    finally:
        win.close()


def test_without_the_model_the_editor_says_so_and_sends_nothing(qapp, tmp_path):
    if FF is None:
        pytest.skip("imageio-ffmpeg not installed")
    from fogscout import qt_editor
    clip = str(tmp_path / "a.mkv")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "testsrc=duration=2:size=320x180:rate=15", "-c:v", "libx264", "-pix_fmt", "yuv420p", clip],
                   check=True, timeout=120)
    win = qt_editor.EditorWindow(clip, [], str(tmp_path / "Clips"), sound=False, models_dir=str(tmp_path / "x"))
    win.show()
    try:
        assert _pump(qapp, lambda: win.preview._img is not None)
        win.find_text()
        assert not win._text_busy and "nicht vorhanden" in win.status.text()
    finally:
        win.close()
