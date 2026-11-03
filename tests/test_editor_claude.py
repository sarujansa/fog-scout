"""1.27: „Mit Claude bearbeiten“ in the big clip editor (editorclaude) – a wish goes out as numbers only, the
answer becomes a checked proposal, „Übernehmen“ applies it as one undo step, „Verwerfen“ changes nothing, an answer
for an older cut is not applied. No network: askclaude's opener is a fake. Offscreen; skipped without ffmpeg."""
import io
import json
import os
import subprocess
import sys
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import askclaude, obsrec  # noqa: E402

FF = obsrec.ffmpeg_exe()
pytestmark = pytest.mark.skipif(FF is None, reason="imageio-ffmpeg not installed")
KEY = "sk-ant-api03-" + "e" * 40


@pytest.fixture(scope="module")
def clip(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("claude") / "2026-11-03 20-15 Coal Tower – Nurse.mkv")
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


class _Reply(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class FakeOpener:
    def __init__(self, answer):
        self.answer, self.bodies = answer, []

    def open(self, req, timeout=None):
        self.bodies.append(json.loads(req.data.decode("utf-8")))
        return _Reply(json.dumps({"stop_reason": "end_turn",
                                  "content": [{"type": "text", "text": json.dumps(self.answer)}]}).encode())


def _pump(app, until=lambda: False, seconds=30):
    deadline = time.time() + seconds
    while time.time() < deadline and not until():
        app.processEvents()
        time.sleep(0.01)
    return until()


def _window(app, clip, tmp_path):
    from fogscout import qt_editor
    win = qt_editor.EditorWindow(clip, [6.0], str(tmp_path / "Clips"), sound=False)
    win.resize(1400, 860)
    win.show()
    assert _pump(app, lambda: win.preview._img is not None and (win.loading is None or win.loading.finished)
                 and win._pstate != "loading")
    return win


def _spans(win):
    return [(round(p.start, 1), round(p.end, 1), p.speed) for p in win.parts]


def test_a_wish_becomes_one_undo_step_and_sends_numbers_only(qapp, clip, tmp_path, monkeypatch):
    fake = FakeOpener({"summary": "Anfang weg, Rest schneller.",
                       "ops": [{"op": "keep", "from": 0, "to": 12}, {"op": "cut", "from": 0, "to": 2},
                               {"op": "speed", "from": 4, "to": 10, "factor": 2},
                               {"op": "fade", "out": 1}, {"op": "explode"}]})
    monkeypatch.setattr(askclaude, "OPENER", fake)
    win = _window(qapp, clip, tmp_path)
    try:
        assert not win.cl_field.isEnabled()                          # off until the App hands a key
        win.claude_key = lambda: KEY
        win._claude_refresh()
        assert win.cl_field.isEnabled() and win.cl_ask_btn.isEnabled()
        before = _spans(win)
        win.cl_field.setText("erste 2 s weg, ab 0:04 doppelt so schnell, am Ende ausblenden")
        win.claude_ask()
        assert _pump(qapp, lambda: win.cl_take_btn.isVisible())
        sent = fake.bodies[0]["messages"][0]["content"]
        assert "Coal" not in sent and "Nurse" not in sent and "mkv" not in sent and str(tmp_path) not in sent
        assert '"marks": [6.0]' in sent and "erste 2 s weg" in sent
        assert "übersprungen" in win.cl_list.text() and _spans(win) == before        # nothing yet
        win.claude_take()
        assert _spans(win) == [(2.0, 6.0, 1.0), (6.0, 12.0, 2.0)] and win.fade_out_box.currentData() == 1.0
        assert not win.cl_take_btn.isVisible()
        win.undo()                                                       # one step back: all of it
        assert _spans(win) == before and win.fade_out_box.currentData() == 0.0
    finally:
        win.close()


def test_discard_changes_nothing_and_an_answer_for_an_older_cut_is_not_applied(qapp, clip, tmp_path, monkeypatch):
    fake = FakeOpener({"summary": "ok", "ops": [{"op": "cut", "from": 0, "to": 3}]})
    monkeypatch.setattr(askclaude, "OPENER", fake)
    win = _window(qapp, clip, tmp_path)
    try:
        win.claude_key = lambda: KEY
        win._claude_refresh()
        before = _spans(win)
        win.cl_field.setText("erste 3 s weg")
        win.claude_ask()
        assert _pump(qapp, lambda: win.cl_take_btn.isVisible())
        win.claude_drop()
        assert _spans(win) == before and not win.cl_take_btn.isVisible()
        win.claude_ask()
        assert _pump(qapp, lambda: win.cl_take_btn.isVisible())
        win.goto(5.0)
        win.split_at_playhead()                                          # the user cuts meanwhile
        cut = _spans(win)
        win.claude_take()
        assert _spans(win) == cut and "geändert" in win.cl_status.text()
    finally:
        win.close()


def test_a_shorts_wish_switches_the_export_type_and_sets_the_title(qapp, clip, tmp_path, monkeypatch):
    fake = FakeOpener({"summary": "Als Short.", "ops": [{"op": "mode", "value": "shorts"},
                                                       {"op": "short_title", "text": "4K Nurse"}]})
    monkeypatch.setattr(askclaude, "OPENER", fake)
    win = _window(qapp, clip, tmp_path)
    try:
        win.claude_key = lambda: KEY
        win._claude_refresh()
        win.cl_field.setText("als Short mit Titel 4K Nurse")
        win.claude_ask()
        assert _pump(qapp, lambda: win.cl_take_btn.isVisible())
        win.claude_take()
        assert win.mode_box.currentData() == "shorts" and win._short is not None and win._short.title == "4K Nurse"
    finally:
        win.close()
