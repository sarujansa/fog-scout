"""1.42: „Export prüfen“ – eight stills of the finished cut (the export's crop, every censor box hidden) go to Claude;
the findings are times inside the cut with a known kind, a box only for names/chat; a click jumps there and suggests a
censor box for a few seconds of the recording, taken as one undo step."""
import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import askclaude, highlights, obsrec  # noqa: E402

from test_claude_pictures import KEY, FakeOpener, _decoded, _pump  # noqa: E402

FF = obsrec.ffmpeg_exe()


def test_stills_spread_and_only_good_findings_count():
    assert highlights.check_times(80) == [5.0, 15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0]
    assert highlights.check_times(0) == []
    data = {"summary": " Ein Name ", "findings": [
        {"at": 30, "kind": "name", "why": "Name links", "box": [0.1, 0.8, 0.2, 0.05]},
        {"at": 5, "kind": "other", "why": "Menü", "box": [0.1, 0.1, 0.2, 0.2]},       # no box for "other"
        {"at": 99, "kind": "name", "why": "zu spät", "box": []},                       # outside the cut
        {"at": 10, "kind": "overlap", "why": "?", "box": []},                          # unknown kind
        {"at": 12, "kind": "chat", "why": "Chat", "box": [0.9, 0.9, 0.5, 0.5]},       # cut to the picture
        {"at": 14, "kind": "chat", "why": "Chat", "box": [0.1, 0.1]}]}                 # a broken box: none
    summary, found = highlights.check_parse(data, 80)
    assert summary == "Ein Name"
    assert found == [(5.0, "other", "Menü", None), (12.0, "chat", "Chat", [0.9, 0.9, 0.1, 0.1]),
                     (14.0, "chat", "Chat", None), (30.0, "name", "Name links", [0.1, 0.8, 0.2, 0.05])]
    with pytest.raises(ValueError):
        highlights.check_parse({"summary": "x"}, 80)
    assert highlights.uncrop([0.5, 0.5, 0.5, 0.5], (0.2, 0.0, 0.4, 1.0)) == [0.4, 0.5, 0.2, 0.5]
    assert highlights.uncrop([0.5, 0.5, 0.1, 0.1], None) == [0.5, 0.5, 0.1, 0.1]


@pytest.fixture
def qapp():
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_window
    return qt_window.application()


def test_the_editor_checks_the_cut_and_a_finding_becomes_a_box_for_a_while(qapp, tmp_path, monkeypatch):
    if FF is None:
        pytest.skip("imageio-ffmpeg not installed")
    from fogscout import clipedit, qt_editor
    clip = str(tmp_path / "2026-11-07 07-10 Coal Tower – Nurse.mkv")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "color=c=white:size=320x180:rate=15:duration=12", "-c:v", "libx264", "-preset", "veryfast",
                    "-pix_fmt", "yuv420p", clip], check=True, timeout=120)
    fake = FakeOpener({"summary": "Ein Name ist lesbar.", "findings": [
        {"at": 2.5, "kind": "name", "why": "Name unten", "box": [0.5, 0.5, 0.25, 0.25]},
        {"at": 1.0, "kind": "other", "why": "Menü", "box": []}]})
    monkeypatch.setattr(askclaude, "OPENER", fake)
    win = qt_editor.EditorWindow(clip, [], str(tmp_path / "Clips"), sound=False)
    win.show()
    try:
        assert _pump(qapp, lambda: win.preview._img is not None and win.history is not None)
        win.parts = [clipedit.Part(4.0, 10.0)]                                # 6 s of output from 4 s on
        win.timeline.set_parts(win.parts)
        win._commit()
        win.preview.clear_boxes()
        win.preview.add_box([0.0, 0.0, 0.5, 0.5])                             # top left: must arrive hidden
        win._censor_style = "black"
        win.claude_key = lambda: KEY
        win._claude_refresh()
        assert not win.cl_check_btn.isVisible()                               # stills not allowed
        win.claude_check()
        assert fake.bodies == []
        win.claude_frame = lambda: True
        win._claude_refresh()
        assert win.cl_check_btn.isVisible()
        win.claude_check()
        assert _pump(qapp, lambda: not win._claude_busy, 60)
        content = fake.bodies[0]["messages"][0]["content"]
        words = json.dumps([b for b in content if b["type"] == "text"])
        assert "Coal" not in words and "Nurse" not in words and "mkv" not in words and "Clip length: 6.0 s" in words
        pictures = [_decoded(b) for b in content if b["type"] == "image"]
        assert len(pictures) == highlights.CHECK_STILLS
        pic = pictures[0].convert("RGB")
        assert sum(pic.getpixel((5, 5))) < 60 and sum(pic.getpixel((pic.width - 5, pic.height - 5))) > 600
        assert win.cl_hl_rows.count() == 2 and "Ein Name" in win.cl_status.text()
        win.finding_pick(1)                                                   # sorted by time: the name is second
        assert win.pos == pytest.approx(2.5)
        assert win.preview.suggest == [[0.5, 0.5, 0.25, 0.25, 4.5, 8.5]]        # 2.5 s of output = 6.5 s recorded
        before = [list(b) for b in win.preview.boxes]
        win.take_text()
        assert win.preview.boxes == before + [[0.5, 0.5, 0.25, 0.25, 4.5, 8.5]]
        win.undo()
        assert win.preview.boxes == before
        win.finding_pick(0)                                                   # "other": only the jump
        assert win.pos == pytest.approx(1.0) and win.preview.suggest == []
    finally:
        win.close()


def test_a_thumbnail_answer_is_a_clean_title_and_a_still_in_range():
    assert highlights.thumb_parse({"summary": "Gut", "title": "  Knapp\n entkommen​!  ", "still": 3}, 8) == \
        ("Gut", "Knapp entkommen!", 2)
    assert highlights.thumb_parse({"summary": "", "title": "x" * 200, "still": 99}, 8)[1:] == ("x" * 70, -1)
    with pytest.raises(ValueError):
        highlights.thumb_parse({"summary": "", "title": " ", "still": 0}, 8)
    texts = [b["text"] for b in highlights.thumb_blocks(6, [(1.0, {"type": "image"}), (2.0, {"type": "image"})],
                                                         "German") if b.get("type") == "text"]
    assert texts[1:] == ["Still 1 at 1.0 s:", "Still 2 at 2.0 s:"]


def test_the_editor_proposes_a_title_and_saves_a_censored_thumbnail_without_uploading(qapp, tmp_path, monkeypatch):
    if FF is None:
        pytest.skip("imageio-ffmpeg not installed")
    from PIL import Image
    from fogscout import qt_editor
    clip = str(tmp_path / "2026-11-07 09-40 Coal Tower – Nurse.mkv")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "color=c=white:size=320x180:rate=15:duration=8", "-c:v", "libx264", "-preset", "veryfast",
                    "-pix_fmt", "yuv420p", clip], check=True, timeout=120)
    fake = FakeOpener({"summary": "Das dritte Bild ist am spannendsten.", "title": "Knapp entkommen", "still": 3})
    monkeypatch.setattr(askclaude, "OPENER", fake)
    saved = []
    win = qt_editor.EditorWindow(clip, [], str(tmp_path / "Clips"), sound=False, on_saved=saved.append)
    win.show()
    try:
        assert _pump(qapp, lambda: win.preview._img is not None and win.history is not None)
        win.preview.clear_boxes()
        win.preview.add_box([0.0, 0.0, 0.5, 0.5])
        win._censor_style = "black"
        win.claude_key, win.claude_frame = (lambda: KEY), (lambda: True)
        win._claude_refresh()
        assert win.cl_thumb_btn.isVisible()
        win.claude_thumb()
        assert _pump(qapp, lambda: not win._claude_busy, 60)
        content = fake.bodies[0]["messages"][0]["content"]
        words = json.dumps([b for b in content if b["type"] == "text"])
        assert "Coal" not in words and "Nurse" not in words and "mkv" not in words and "Still 8 at" in words
        pic = _decoded(next(b for b in content if b["type"] == "image")).convert("RGB")
        assert sum(pic.getpixel((5, 5))) < 60                                   # censored in what was sent
        assert win.cl_hl_rows.count() == 2 and win.pos == pytest.approx(highlights.check_times(8)[2])
        win.thumb_take_title()
        assert win._short.title == "Knapp entkommen"
        win.undo()
        assert win._short is None or win._short.title == ""
        win.thumb_save()
        assert _pump(qapp, lambda: saved, 30)
        out = saved[0]
        assert out.endswith(".png") and "Vorschaubild" in os.path.basename(out)
        img = Image.open(out).convert("RGB")
        assert img.size == (320, 180) and sum(img.getpixel((10, 10))) < 60     # censored in the file too
        assert len(fake.bodies) == 1                                            # saving sent nothing
    finally:
        win.close()
