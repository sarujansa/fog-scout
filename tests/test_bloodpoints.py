"""1.13: bloodpoint balance from the lobby – unchanged after a counted round = the cap is reached (bloodpoints.py)."""
import os
import sys
from types import SimpleNamespace

import cv2
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fogscout import bloodpoints as bp  # noqa: E402
from fogscout import history  # noqa: E402
from fogscout.bloodpoints import BloodpointWatch  # noqa: E402
from fogscout.detector import _right_region, currency_box  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 3440, 1440


# ------------------------------------------------------------------ parsing
def test_parse_takes_the_first_counter_whatever_the_separators():
    assert bp.parse("1 499 484 | 4 628 | 823") == 1499484
    assert bp.parse("1499 484") == 1499484                 # the OCR drops a space now and then
    assert bp.parse("5,000,000 | 61,250") == 5000000
    assert bp.parse("823") == 823
    assert bp.parse("") is None and bp.parse(None) is None
    assert bp.parse("12 | 4 628") is None                 # too short for a counter
    assert bp.parse("1 234 567 890") is None              # too long for a balance: a misread group
    assert bp.fmt(5000000) == "5 000 000" and bp.fmt(823) == "823" and bp.fmt(0) == "0"


# ------------------------------------------------------------------ confirming readings
def test_a_reading_counts_after_two_identical_looks_only():
    w = BloodpointWatch()
    assert w.note(1499484, 1.0) is None and w.balance is None
    w.note(1490000, 2.0)                                  # one slip of the OCR …
    assert w.balance is None
    w.note(1499484, 3.0)
    assert w.balance is None                              # … breaks the run: again two the same
    w.note(1499484, 4.0)
    assert (w.balance, w.balance_t) == (1499484, 4.0)
    w.note(None, 5.0, text="?")                            # nothing readable: changes nothing
    assert (w.balance, w.balance_t, w.last_text) == (1499484, 4.0, "?")
    assert list(w.changes) == [(4.0, 1499484)]


def _lobby(w, value, t):
    """Two looks a second apart, as the worker posts them."""
    out = [w.note(value, t), w.note(value, t + 1.0)]
    return next((r for r in out if r is not None), None)


def test_unchanged_balance_after_a_round_is_the_cap():
    w = BloodpointWatch()
    _lobby(w, 5000000, 100.0)
    w.round_started(130.0)
    assert w.before == 5000000
    w.round_ended(800.0)
    res = _lobby(w, 5000000, 830.0)
    assert res is not None and (res.round_t, res.before, res.after, res.gain, res.capped) == (130.0, 5000000, 5000000, 0, True)
    assert _lobby(w, 5000000, 840.0) is None              # said once
    assert w.pending is None and w.round_t is None


def test_a_higher_balance_is_a_gain_and_a_lower_one_was_spent():
    w = BloodpointWatch()
    _lobby(w, 4900000, 100.0)
    w.round_started(130.0)
    w.round_ended(800.0)
    res = _lobby(w, 4950000, 830.0)
    assert (res.gain, res.capped) == (50000, False)
    w.round_started(900.0)
    w.round_ended(1500.0)
    res = _lobby(w, 4200000, 1530.0)                      # bloodweb in between
    assert (res.gain, res.capped) == (-750000, False)


def test_an_unchanged_small_balance_is_no_cap():
    w = BloodpointWatch()
    _lobby(w, 400000, 100.0)
    w.round_started(130.0)
    w.round_ended(800.0)
    res = _lobby(w, 400000, 830.0)
    assert res is not None and res.gain == 0 and not res.capped
    assert bp.CAP_FLOOR == 1_000_000


def test_a_round_without_a_fresh_balance_before_it_is_not_compared():
    w = BloodpointWatch()
    _lobby(w, 5000000, 0.0)
    w.round_started(bp.BEFORE_MAX_S + 100.0)             # the last reading is too old to say anything
    assert w.before is None
    w.round_ended(bp.BEFORE_MAX_S + 800.0)
    assert w.pending is None and _lobby(w, 5000000, bp.BEFORE_MAX_S + 830.0) is None
    w2 = BloodpointWatch()                                # never read before the round
    w2.round_started(10.0)
    w2.round_ended(700.0)
    assert _lobby(w2, 5000000, 730.0) is None


def test_custom_games_and_rounds_too_short_are_not_compared():
    w = BloodpointWatch()
    _lobby(w, 5000000, 100.0)
    w.round_started(130.0)
    w.round_ended(800.0, counts=False)
    assert w.pending is None and _lobby(w, 5000000, 830.0) is None
    assert w.balance == 5000000                           # the balance is kept all the same


def test_a_reading_long_after_the_end_or_the_next_round_drops_the_comparison():
    w = BloodpointWatch()
    _lobby(w, 5000000, 100.0)
    w.round_started(130.0)
    w.round_ended(800.0)
    assert _lobby(w, 5000000, 800.0 + bp.AFTER_MAX_S + 5) is None and w.pending is None
    _lobby(w, 5000000, 2000.0)
    w.round_started(2100.0)
    w.round_ended(2800.0)
    w.round_started(2900.0)                               # the lobby was never seen in between
    assert w.pending is None and w.before == 5000000      # the old reading (2001 s) is fresh enough
    w.round_ended(3600.0)
    assert _lobby(w, 5000000, 3630.0).capped


def test_readings_while_a_round_is_open_only_update_the_balance():
    w = BloodpointWatch()
    _lobby(w, 5000000, 100.0)
    w.round_started(130.0)
    assert _lobby(w, 5100000, 200.0) is None and w.balance == 5100000 and w.before == 5000000


def test_describe_tells_the_state():
    w = BloodpointWatch()
    assert w.describe() == "noch nicht gelesen"
    _lobby(w, 5000000, 100.0)
    w.round_started(130.0)
    assert "Stand 5 000 000" in w.describe() and "Runde offen, vorher 5 000 000" in w.describe()
    w.round_ended(800.0)
    w.note(None, 801.0, text="5 000 000")
    d = w.describe()
    assert "wartet auf die Lesung nach der Runde" in d and "„5 000 000“" in d and "Änderungen" in d


# ------------------------------------------------------------------ the strip the worker grabs
@pytest.mark.parametrize("size", [(3440, 1440), (2560, 1440), (1718, 1360), (1920, 1080)])
def test_currency_box_is_the_strip_the_round_end_reads(size):
    fw, fh = size
    x, y, w, h = currency_box(fw, fh)
    frame = np.zeros((fh, fw, 3), np.uint8)
    frame[y:y + h, x:x + w] = 7
    reg = _right_region(frame, 0.62, 0.0, 0.12, full_width=True)
    assert reg.shape[:2] == (h, w) and int(reg.min()) == 7 and int(frame.sum()) == 7 * 3 * w * h
    assert x + w == fw and y == 0                                 # up to the window edge, from the top


def _bar(texts, size=30):
    """A dark 3440×1440 screen with the counters top right in the bundled Inter font (coloured icon before each)."""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (W, H), (18, 14, 12))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(os.path.join(ROOT, "fogscout", "fonts", "Inter-Medium.otf"), size)
    x = 2800
    for i, t in enumerate(texts):
        d.ellipse((x, 28, x + 26, 54), fill=[(170, 30, 30), (30, 150, 160), (200, 160, 40)][i % 3])
        x += 36
        d.text((x, 24), t, font=f, fill=(235, 235, 235))
        x += int(d.textlength(t, font=f)) + 40
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


@pytest.fixture(scope="module")
def watcher():
    from fogscout.detector import OutOfMatchWatcher
    from fogscout.ocr import Recognizer
    return OutOfMatchWatcher(Recognizer(os.path.join(ROOT, "models", "ch_PP-OCRv4_rec_infer.onnx")))


@pytest.mark.parametrize("texts, value", [(["1 499 484", "4 628", "823"], 1499484),
                                          (["5 000 000", "61 250", "1 150"], 5000000),
                                          (["5,000,000", "61,250", "1,150"], 5000000)])
def test_the_leftmost_counter_is_read_as_the_bloodpoints(watcher, texts, value):
    x, y, w, h = currency_box(W, H)
    strip = _bar(texts)[y:y + h, x:x + w]
    text = watcher.currency_text(strip, H)
    assert bp.parse(text) == value and "|" not in text              # only the first group is read
    assert watcher.currency_text(np.full((h, w, 3), 20, np.uint8), H) == ""


# ------------------------------------------------------------------ the worker's look
def _worker():
    import collections
    from fogscout import worker
    w = worker.DetectionWorker.__new__(worker.DetectionWorker)
    w.posted, w.bp_info = [], "–"
    w.post = lambda kind, **d: w.posted.append((kind, d))
    for name in ("overlay_rect", "hud_rect", "media_rect", "today_rect", "info_rect", "toast_rect"):
        setattr(w, name, None)
    w.guide_rects = ()
    w.end_history = collections.deque(maxlen=5)
    return w


class _Watcher:
    def __init__(self, text):
        self.text, self.images = text, []

    def currency_text(self, img, frame_h):
        self.images.append(img.copy())
        return self.text


def test_the_worker_posts_every_reading_of_the_lobby_with_our_windows_blacked_out():
    w = _worker()
    frame = np.full((H, W, 3), 60, np.uint8)
    grab = lambda box: frame[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]   # noqa: E731
    watcher = _Watcher("5 000 000")
    w._bp_look(grab, W, H, 1000.0, (0, 0), False, watcher)
    assert w.posted == [("bloodpoints", {"value": 5000000, "text": "5 000 000", "t": 1000.0})]
    assert "„5 000 000“" in w.bp_info and "5 000 000" in w.bp_info
    x, y, bw, bh = currency_box(W, H)
    w.hud_rect = (x + 20, 10, 100, 40)                      # our system values sit in the strip (screen pixels)
    w._bp_look(grab, W, H, 1001.0, (0, 0), True, watcher)
    img = watcher.images[-1]
    assert int(img[10:50, 20:120].max()) == 0 and int(img[60:, :].min()) == 60   # blacked out before reading
    assert int(frame[10:50, x + 20:x + 120].max()) == 0     # in place, like the other looks (no copy)
    watcher.text = ""
    w._bp_look(grab, W, H, 1002.0, (0, 0), False, watcher)
    assert len(w.posted) == 2 and w.bp_info.endswith("→ –")  # nothing readable: no event, diagnosis says so
    w._bp_look(lambda box: None, W, H, 1003.0, (0, 0), False, watcher)
    assert len(watcher.images) == 3                        # covered by another window: no look at all


# ------------------------------------------------------------------ the app: log, notification, stored balance
def _app(tmp_path, notify=True):
    from fogscout.app_lobby import LobbyInfo
    os.makedirs(tmp_path, exist_ok=True)
    path = str(tmp_path / "rounds.jsonl")
    history.append(path, history.Round(130.0, 670.0, "coal", "Coal Tower", role="killer"))
    app = SimpleNamespace(bloodpoints=BloodpointWatch(), settings={"bp_cap_notify": notify}, logged=[], notified=[],
                          _hist_path=lambda: path, _report_once=lambda *a: (_ for _ in ()).throw(AssertionError(a)))
    app._log = lambda text, cat="System": app.logged.append((cat, text))
    app._notify = lambda title, text, force=False: app.notified.append((title, text, force))
    app.reading = lambda d: LobbyInfo._bp_reading(app, d)
    _lobby(app.bloodpoints, 5000000, 100.0)
    app.bloodpoints.round_started(130.0)
    app.bloodpoints.round_ended(800.0)
    return app, path


def test_the_cap_is_told_with_sound_and_window_and_the_balance_is_stored(tmp_path):
    app, path = _app(tmp_path)
    app.reading({"value": 5000000, "text": "5 000 000", "t": 830.0})
    assert app.logged == [] and app.notified == []
    app.reading({"value": 5000000, "text": "5 000 000", "t": 831.0})
    assert [c for c, _t in app.logged] == ["Erkennung"] and "5 000 000" in app.logged[0][1] and "Cap" in app.logged[0][1]
    assert app.notified == [("Blutpunkte-Cap erreicht",
                             "5 000 000 BP vor und nach der Runde – im Blutnetz ausgeben, sonst bringt auch die "
                             "nächste Runde nichts.", True)]
    assert history.load(path)[0].balance == 5000000
    app.reading({"value": 5000000, "text": "5 000 000", "t": 832.0})
    assert len(app.logged) == 1 and len(app.notified) == 1          # said once


def test_the_notification_can_be_switched_off_and_a_gain_is_only_logged(tmp_path):
    app, path = _app(tmp_path, notify=False)
    app.reading({"value": 5000000, "text": "5 000 000", "t": 830.0})
    app.reading({"value": 5000000, "text": "5 000 000", "t": 831.0})
    assert len(app.logged) == 1 and app.notified == []
    app2, path2 = _app(tmp_path / "b")
    app2.reading({"value": 5031500, "text": "5 031 500", "t": 830.0})
    app2.reading({"value": 5031500, "text": "5 031 500", "t": 831.0})
    assert app2.notified == [] and app2.logged == [("Erkennung", "Blutpunkte: +31 500 in dieser Runde, Stand 5 031 500.")]
    assert history.load(path2)[0].balance == 5031500


def test_the_counter_is_read_seldom_once_the_looks_agree_and_at_once_after_a_round():
    """1.16.2 (A7): every lobby look until CONFIRM_LOOKS readings agree, then every BP_STEADY_S; another value or
    a new map (a round in between) reads every look again – the app still gets its confirming pair at once."""
    from fogscout import worker
    w = _worker()
    w.watch_gen, w._bp_seen = None, (None, 0, -1e9, None)
    frame = np.full((H, W, 3), 60, np.uint8)
    grab = lambda box: frame[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]   # noqa: E731
    watcher = _Watcher("5 000 000")
    looked = []
    for t in range(100, 120):                                 # one lobby look a second for 20 s
        if w._bp_due(float(t)):
            looked.append(t)
            w._bp_look(grab, W, H, float(t), (0, 0), False, watcher)
    assert looked[:2] == [100, 101] and all(b - a == worker.BP_STEADY_S for a, b in zip(looked[1:], looked[2:]))
    watcher.text = "5 100 000"                                # spent / earned: read every look until it agrees
    assert looked[-1] == 116 and w._bp_due(120.0) is False and w._bp_due(121.0)
    w._bp_look(grab, W, H, 121.0, (0, 0), False, watcher)
    assert w._bp_due(122.0)
    w._bp_look(grab, W, H, 122.0, (0, 0), False, watcher)
    assert not w._bp_due(123.0)
    w.watch_gen = (1, "auto")                                 # a map came: the reading after the round is at once
    assert w._bp_due(128.0) and w._bp_due(128.5)
    watcher.text = ""                                         # nothing readable: every look
    w._bp_look(grab, W, H, 129.0, (0, 0), False, watcher)
    assert w._bp_due(129.5)
    assert [v["value"] for k, v in w.posted][-2:] == [5100000, 5100000]
