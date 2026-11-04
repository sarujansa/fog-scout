"""1.35 (user's release of 3.11.2026): pictures to Claude on a click – the screenshot editor (imageclaude) and a
still in the clip editor (editcommands censor) – and statistics questions with summed-up round values
(statsclaude). No network: askclaude's opener is a fake that records the request."""
import base64
import io
import json
import os
import queue
import subprocess
import sys
import time

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import askclaude, editcommands, history, imageclaude, imageedit, obsrec, official, sequence, statsclaude  # noqa: E402,E501

KEY = "sk-ant-api03-" + "p" * 40
FF = obsrec.ffmpeg_exe()


class _Reply(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class FakeOpener:
    def __init__(self, answer):
        self.answer, self.bodies, self.timeouts = answer, [], []

    def open(self, req, timeout=None):
        self.bodies.append(json.loads(req.data.decode("utf-8")))
        self.timeouts.append(timeout)
        return _Reply(json.dumps({"stop_reason": "end_turn",
                                  "content": [{"type": "text", "text": json.dumps(self.answer)}]}).encode())


def _decoded(block) -> Image.Image:
    assert block["type"] == "image" and block["source"]["media_type"] == "image/jpeg"
    return Image.open(io.BytesIO(base64.standard_b64decode(block["source"]["data"])))


# ------------------------------------------------------------------ askclaude: picture blocks
def test_a_picture_goes_as_a_small_jpeg_before_the_text_with_a_longer_timeout(monkeypatch):
    big = Image.new("RGB", (3440, 1440), (200, 30, 30))
    block = askclaude.image_block(big)
    pic = _decoded(block)
    assert pic.format == "JPEG" and max(pic.size) == askclaude.IMAGE_SIDE and big.size == (3440, 1440)
    assert "\n" not in block["source"]["data"]
    fake = FakeOpener({"summary": "ok", "ops": []})
    monkeypatch.setattr(askclaude, "OPENER", fake)
    askclaude.request(KEY, "sys", "Wish: x", imageclaude.SCHEMA, images=[block])
    content = fake.bodies[0]["messages"][0]["content"]
    assert [b["type"] for b in content] == ["image", "text"] and content[1]["text"] == "Wish: x"
    assert fake.timeouts == [askclaude.IMAGE_TIMEOUT]
    askclaude.request(KEY, "sys", "Wish: y", imageclaude.SCHEMA)                 # without: text only, as before
    assert fake.bodies[1]["messages"][0]["content"] == "Wish: y" and fake.timeouts[1] == askclaude.HTTP_TIMEOUT


# ------------------------------------------------------------------ imageclaude (pure)
def test_boxes_crop_and_colour_refer_to_the_picture_claude_saw_and_turning_comes_last():
    ops = [{"op": "rotate", "quarters": 1},
           {"op": "censor", "x": 0.0, "y": 0.0, "w": 0.2, "h": 0.1},
           {"op": "crop", "x": 0.1, "y": 0.1, "w": 0.5, "h": 0.5},
           {"op": "adjust", "brightness": 1.3, "contrast": 9},
           {"op": "censor_style", "value": "blur"}]
    new, done, skipped = imageclaude.apply(imageedit.ImageEdit(), ops, (1600, 900))
    assert not skipped and len(done) == 5
    assert new.rotate == 1 and new.censor_style == "blur"
    assert new.brightness == pytest.approx(1.3) and new.contrast == imageedit.ADJUST_RANGE[1]   # held in range
    # the censor box was set on the unturned picture, then turned along: the top left corner went top right
    (x, y, w, h), = new.censor
    assert (round(x, 3), round(y, 3), round(w, 3), round(h, 3)) == (0.9, 0.0, 0.1, 0.2)
    assert new.crop is not None


def test_unusable_operations_are_skipped_never_guessed():
    base = imageedit.ImageEdit()
    new, done, skipped = imageclaude.apply(base, [{"op": "censor", "x": 2, "y": 0, "w": 0.1, "h": 0.1},
                                                  {"op": "crop", "x": 0.1}, {"op": "rotate", "quarters": 4},
                                                  {"op": "flip", "value": "diagonal"}, {"op": "explode"},
                                                  {"op": "adjust"}, {"op": "censor_style", "value": "retouch"}],
                                           (100, 100))
    assert new == base and not done and len(skipped) == 7
    with pytest.raises(ValueError):
        imageclaude.apply(base, {"op": "crop"}, (100, 100))


def test_the_picture_sent_keeps_censored_areas_hidden():
    img = Image.new("RGB", (400, 200), (0, 0, 0))
    for x in range(0, 400, 2):                       # a fine pattern a pixelate box cannot keep
        for y in range(0, 100):
            img.putpixel((x, y), (255, 255, 255))
    edit = imageedit.ImageEdit(censor=[(0.0, 0.0, 0.5, 0.5)], censor_style="black")
    sent = imageclaude.picture(img, edit)
    assert sent.size == img.size                     # not cropped
    assert sent.crop((0, 0, 200, 100)).getextrema() == ((0, 0), (0, 0), (0, 0))
    assert sent.crop((200, 0, 400, 100)).getextrema()[0] == (0, 255)


# ------------------------------------------------------------------ editcommands: censor only with a still
def test_a_censor_box_needs_a_still():
    state = sequence.EditState(parts=[sequence.Part(0.0, 10.0)])
    op = [{"op": "censor", "x": 0.02, "y": 0.1, "w": 0.2, "h": 0.3}]
    new, _mode, done, skipped = editcommands.apply(state, op, "copy")
    assert not done and new.boxes == [] and not new.censor_on and skipped
    new, _mode, done, skipped = editcommands.apply(state, op, "copy", picture=True)
    assert new.boxes == [[0.02, 0.1, 0.2, 0.3]] and new.censor_on and not skipped and state.boxes == []
    assert "No picture is attached." in editcommands.content("x", state, "copy")
    assert "Attached: a still" in editcommands.content("x", state, "copy", picture=True)


# ------------------------------------------------------------------ statsclaude (pure)
def _round(t, map_, role, killer="", region="eu-central-1", seconds=600, custom=False, farming=False):
    return history.Round(t=t, seconds=seconds, map_id=map_.lower(), map=map_, region=region, role=role,
                         killer=killer, custom=custom, farming=farming, wait=60.0, ping=40.0)


def test_the_summary_holds_only_counts_and_rates_per_group():
    base = time.mktime((2026, 11, 2, 20, 0, 0, 0, 0, -1))
    rounds = [_round(base + i * 900, "Coal Tower", "killer", "The Nurse") for i in range(3)]
    rounds += [_round(base + 4000, "Coal Tower", "survivor"), _round(base + 5000, "Coal Tower", "survivor")]
    rounds += [_round(base + 6000, "Ormond", "killer", "The Blight")]                       # one round: left out
    rounds += [_round(base + 7000, "Ormond", "killer", "The Blight", custom=True)]           # custom: never
    off = {}
    for r, n_dead in zip(rounds[:3], (4, 2, 3)):
        opp = [official.Player("survivor", "Meg Thomas", "Sacrificed" if i < n_dead else "Escaped")
               for i in range(4)]
        off[id(r)] = official.Match(t=r.t, map=r.map, role="killer", character="The Nurse", bp=30000, opp=opp)
    for r, st in zip(rounds[3:5], ("Escaped", "Sacrificed")):
        off[id(r)] = official.Match(t=r.t, map=r.map, role="survivor", character="Meg Thomas", status=st,
                                    opp=[official.Player("killer", "The Trapper")])
    data = statsclaude.summary(rounds, off)
    assert data["rounds"] == 6 and data["first_day"] == data["last_day"] == "2026-11-02"
    nurse = data["killer_by_own_killer"]["The Nurse"]
    assert nurse["n"] == 3 and nurse["kills"] == 3.0 and nurse["four_k"] == pytest.approx(0.33, abs=0.01)
    assert "The Blight" not in data["killer_by_own_killer"]                 # one round would be raw data
    assert data["survivor_by_opposing_killer"]["The Trapper"]["escape"] == 0.5
    assert data["by_time_of_day"]["evening"]["n"] == 6
    words = statsclaude.private_words(data)
    assert not any(":" in w and w.count(":") >= 1 and w[:2].isdigit() for w in words)   # no clock times
    sent = statsclaude.content("Wo verliere ich am meisten?" + "x" * 1000, data)
    assert sent.endswith("x" * (statsclaude.MAX_QUESTION - len("Wo verliere ich am meisten?")))


def test_a_statistics_question_comes_back_as_plain_text(monkeypatch):
    fake = FakeOpener({"answer": "  Auf   Coal Tower\nhast du die meisten Kills. "})
    monkeypatch.setattr(askclaude, "OPENER", fake)
    got = queue.Queue()
    a = askclaude.Asker(lambda kind, **kw: got.put((kind, kw)))
    a.start()
    try:
        a.ask_stats(KEY, "Wo habe ich die meisten Kills?", {"rounds": 3})
        kind, kw = got.get(timeout=10)
    finally:
        a.stop()
    assert kind == "stats" and kw["answer"] == "Auf Coal Tower hast du die meisten Kills."
    body = fake.bodies[0]
    assert body["output_config"]["format"]["schema"] == statsclaude.SCHEMA
    summary, asked = body["messages"][0]["content"]                 # 1.36: the summary cached, the question after
    assert '"rounds": 3' in summary["text"] and summary["cache_control"] == {"type": "ephemeral"}
    assert asked["text"] == "Question: Wo habe ich die meisten Kills?" and a.answered == 1


# ------------------------------------------------------------------ the windows (offscreen)
@pytest.fixture
def qapp():
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_window
    return qt_window.application()


def _pump(app, until=lambda: False, seconds=30):
    deadline = time.time() + seconds
    while time.time() < deadline and not until():
        app.processEvents()
        time.sleep(0.01)
    return until()


def test_the_image_editor_sends_the_picture_only_on_a_click_and_applies_as_one_step(qapp, tmp_path, monkeypatch):
    from fogscout.qt_image import ImageWindow
    path = tmp_path / "shot.png"
    Image.new("RGB", (640, 360), (40, 90, 160)).save(path)
    fake = FakeOpener({"summary": "Name verpixelt.", "ops": [{"op": "censor", "x": 0.05, "y": 0.05, "w": 0.3,
                                                              "h": 0.1}, {"op": "teleport"}]})
    monkeypatch.setattr(askclaude, "OPENER", fake)
    win = ImageWindow(str(path), str(tmp_path / "out"))
    win.show()
    try:
        win.tools.setCurrentIndex(4)                                             # the tab „Claude“
        assert not win.cl_field.isEnabled() and "Aus" in win.cl_status.text()     # off until the App allows it
        win.claude_key = lambda: KEY
        win._claude_refresh()
        assert win.cl_field.isEnabled() and win.cl_ask_btn.isEnabled()
        win.claude_ask()                                                          # no wish: nothing sent
        assert fake.bodies == []
        win.cl_field.setText("Spielernamen oben links verpixeln")
        win.claude_ask()
        assert _pump(qapp, lambda: win.cl_take_btn.isVisible())
        content = fake.bodies[0]["messages"][0]["content"]
        assert content[0]["type"] == "image" and "Spielernamen oben links" in content[1]["text"]
        assert "shot.png" not in json.dumps(fake.bodies[0]) and str(tmp_path) not in json.dumps(fake.bodies[0])
        assert _decoded(content[0]).size == (640, 360)
        assert win.edit.censor == [] and "übersprungen" in win.cl_list.text()      # nothing before „Übernehmen“
        win.claude_take()
        assert len(win.edit.censor) == 1 and not win.cl_take_btn.isVisible()
        win.undo()
        assert win.edit.censor == []
    finally:
        win.close()


@pytest.mark.skipif(FF is None, reason="imageio-ffmpeg not installed")
def test_the_clip_editor_sends_a_still_only_when_allowed_and_ticked(qapp, tmp_path, monkeypatch):
    from fogscout import qt_editor
    clip = str(tmp_path / "2026-11-03 20-15 Coal Tower – Nurse.mkv")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                    "-i", "testsrc=duration=6:size=320x180:rate=30", "-c:v", "libx264", "-preset", "veryfast",
                    "-g", "30", "-pix_fmt", "yuv420p", clip], check=True, timeout=120)
    fake = FakeOpener({"summary": "Name zensiert.", "ops": [{"op": "censor", "x": 0.0, "y": 0.0, "w": 0.25,
                                                             "h": 0.2}]})
    monkeypatch.setattr(askclaude, "OPENER", fake)
    win = qt_editor.EditorWindow(clip, [], str(tmp_path / "Clips"), sound=False)
    win.resize(1400, 860)
    win.show()
    try:
        assert _pump(qapp, lambda: win.preview._img is not None and (win.loading is None or win.loading.finished)
                     and win._pstate != "loading")
        win.claude_key = lambda: KEY
        win._claude_refresh()
        assert not win.cl_frame_box.isVisible()                    # the App has not allowed stills
        win.cl_field.setText("Namen oben links zensieren")
        win.claude_ask()
        assert _pump(qapp, lambda: not win._claude_busy)
        assert isinstance(fake.bodies[0]["messages"][0]["content"], str)        # no picture
        assert "übersprungen" in win.cl_list.text() and win._state().boxes == []
        win.claude_frame = lambda: True
        win._claude_refresh()
        assert win.cl_frame_box.isVisible() and not win.cl_frame_box.isChecked()
        win.cl_frame_box.setChecked(True)
        win.claude_ask()
        assert _pump(qapp, lambda: win.cl_take_btn.isVisible())
        content = fake.bodies[1]["messages"][0]["content"]
        assert content[0]["type"] == "image" and "Attached: a still" in content[1]["text"]
        assert "Coal" not in content[1]["text"] and "mkv" not in content[1]["text"]
        assert _decoded(content[0]).size == (320, 180)
        win.claude_take()
        assert win._state().boxes == [[0.0, 0.0, 0.25, 0.2]] and win._state().censor_on
        win.claude_frame = lambda: False                           # switched off: the tick goes too
        win._claude_refresh()
        assert not win.cl_frame_box.isVisible() and not win.cl_frame_box.isChecked()
    finally:
        win.close()


# ------------------------------------------------------------------ 1.36: own perks, the week, fixed questions
def test_own_perks_become_groups_and_the_week_compares_two_summaries():
    now = time.mktime((2026, 11, 4, 21, 0, 0, 0, 0, -1))                    # a Wednesday
    rounds = [_round(now - 3600 * h, "Coal Tower", "killer", "The Nurse") for h in (1, 2, 3)]
    rounds += [_round(now - 7 * 24 * 3600 - 3600 * h, "Ormond", "killer", "The Nurse") for h in (1, 2)]
    off = {}
    for i, r in enumerate(rounds):
        dead = 4 if i < 3 else 1
        off[id(r)] = official.Match(t=r.t, map=r.map, role="killer", character="The Nurse",
                                    perks=[["p1", "Pain Resonance"], ["p2", "Grim Embrace" if i % 2 else "Lethal"]],
                                    opp=[official.Player("survivor", "Meg", "Sacrificed" if k < dead else "Escaped")
                                         for k in range(4)])
    data = statsclaude.summary(rounds, off)
    assert data["killer_by_own_perk"]["Pain Resonance"]["n"] == 5
    assert data["killer_by_own_perk"]["Lethal"]["n"] == 3 and "Grim Embrace" in data["killer_by_own_perk"]
    wk = statsclaude.week(rounds, off, now)
    assert wk["this_week"]["rounds"] == 3 and wk["last_week"]["rounds"] == 2
    assert wk["this_week"]["all"]["kills"] == 4.0 and wk["last_week"]["all"]["kills"] == 1.0
    assert "Meg" not in statsclaude.private_words(data)                    # survivors only as a count


def test_a_fixed_question_reopens_the_palette_and_sends_the_week(tmp_path):
    from types import SimpleNamespace

    from fogscout import app_palette
    from fogscout.config import Settings
    shown = []

    class Pal:
        def open(self, entries, recent, claude, text=""):
            shown.append(("open", text))

        def show_waiting(self):
            shown.append(("waiting",))

        def show_error(self, text):
            shown.append(("error", text))
    asked = []

    class Stub(app_palette.PaletteMixin):
        pass
    s = Stub()
    s.settings = Settings(str(tmp_path / "settings.json"))
    s.settings.set("claude_stats", True)
    s._claude_session_key = KEY
    s.qt = SimpleNamespace(palette=Pal(), _palette_entries=[], _palette_recent=[], _palette_claude=False)
    s.asker = SimpleNamespace(ask_stats=lambda key, q, data: asked.append((q, data)))
    s._joined = lambda: SimpleNamespace(rounds=[], off={})
    s._palette_ask_fixed("week")
    assert shown[0][0] == "open" and "Woche" in shown[0][1] and shown[-1][0] == "error" and not asked
    now = time.time()
    s._joined = lambda: SimpleNamespace(rounds=[_round(now - 60, "Coal Tower", "killer", "The Nurse")], off={})
    shown.clear()
    s._palette_ask_fixed("week")
    assert shown[-1] == ("waiting",) and asked[0][0] == shown[0][1] and asked[0][1]["this_week"]["rounds"] == 1
    s.settings.set("claude_stats", False)                                   # switched off: nothing at all
    shown.clear()
    s._palette_ask_fixed("build")
    assert shown == [] and len(asked) == 1
