"""1.39.2: the moments of a recording (keys, game sound, F8 marks), idle and dark stretches cut locally, and Claude's
„Short vorschlagen“ – stills at the moments, the moments as numbers only, the whole short as one undo step."""
import json
import subprocess

import pytest

from fogscout import askclaude, highlights, inputs, moments, obsrec, sequence
from fogscout.clipedit import Part

from test_claude_pictures import KEY, FakeOpener, _pump


@pytest.fixture
def qapp():
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_window
    return qt_window.application()

FF = obsrec.ffmpeg_exe()
W = inputs.encode(inputs.InputState(keys=frozenset({"w"})))
LMB = inputs.encode(inputs.InputState(keys=frozenset({"lmb"})))


def _busy(t0, t1, step=0.3):
    out, t, k = [], t0, 0
    while t < t1:
        out.append((round(t, 2), (W, LMB, 0)[k % 3]))
        t, k = t + step, k + 1
    return out


def test_busy_keys_loud_sound_and_marks_make_the_moments():
    ev = [(1.0, W), (2.0, 0)] + _busy(40, 49) + [(49.5, 0)]
    wave = [0.05] * (20 * 100)
    for i in range(20 * 80, 20 * 84):                            # loud at 80–84 s
        wave[i] = 1.0
    found = moments.find(ev, wave, 20, [20.0], 100)
    kinds = {round(p): kind for _a, _b, p, _s, kind in found}
    assert set(kinds.values()) == {"mark", "keys", "sound"}
    assert any(38 <= p <= 50 for p in kinds) and any(78 <= p <= 86 for p in kinds) and 20 in kinds
    assert all(b - a <= moments.BEFORE_S + moments.AFTER_S for a, b, *_r in found)
    assert moments.find([], [], 20, [], 100) == [] and moments.find(ev, wave, 20, [], 0) == []


def test_moments_keep_their_distance_and_count():
    ev = []
    for k in range(12):
        ev += _busy(k * 20, k * 20 + 5)
    found = moments.find(ev, [], 20, [], 240)
    peaks = sorted(p for _a, _b, p, _s, _k in found)
    assert len(found) <= moments.MAX_MOMENTS and all(b - a >= moments.MIN_GAP_S for a, b in zip(peaks, peaks[1:]))


def test_idle_is_nothing_held_not_a_held_key():
    ev = [(0.5, W), (30.0, 0), (45.0, LMB), (46.0, 0)]            # W held 30 s = running, not idle
    assert moments.idle(ev, 60) == [(31.0, 44.0), (47.0, 59.0)]
    assert moments.idle([(20.0, W), (21.0, 0)], 30) == [(1.0, 19.0), (22.0, 29.0)]   # before the first change too
    assert moments.idle([], 60) == []                             # no inputs: no guessing


def test_dark_edges_cut_a_loading_screen_at_either_end():
    assert moments.dark_edges([True, True, True, False], [False], 1.0, 60) == [(0.0, 3.0)]
    assert moments.dark_edges([False], [True, True], 1.0, 60) == [(58.0, 60.0)]
    assert moments.dark_edges([True], [False], 0.5, 60) == []        # shorter than DARK_MIN_S


def test_source_ranges_become_cuts_through_tempo_and_order():
    parts = [Part(0, 50), Part(50, 100, speed=2.0), Part(10, 10, hold=2.0)]
    out = moments.to_output(parts, [(3, 39), (61, 99)])
    assert out == [(3.0, 39.0), (55.5, 74.5)]                     # the still is never cut
    ops = moments.cut_ops(out)
    assert [o["from"] for o in ops] == [55.5, 3.0]                # latest first: the earlier times stay right
    from fogscout import editcommands
    new, _m, done, _skip = editcommands.apply(sequence.EditState(parts), ops, "copy")
    assert len(done) == 2 and round(sequence.duration(new.parts), 2) == round(sequence.duration(parts) - 36 - 19, 2)


def test_the_stills_follow_the_moments_and_the_facts_are_numbers_only():
    times = highlights.still_times(100, [20.0], [60.0, 61.0])
    assert 20.0 in times and 60.0 in times and 61.0 not in times   # two peaks closer than MERGE_S: one still
    text = moments.facts([(10.0, 24.0, 1.35, "mark"), (40.0, 54.0, 1.0, "keys")], 100, [20.0])
    assert text.startswith("Clip length: 100 s.") and "10–24 s (mark, score 1.35); 40–54 s (keys" in text
    assert "W" not in text and "shift" not in text.lower()


# ---- the editor (Qt, real ffmpeg)
def _editor(tmp_path, events, seconds=60):
    if FF is None:
        pytest.skip("imageio-ffmpeg not installed")
    from fogscout import qt_editor
    clip = str(tmp_path / "2026-11-07 21-00 Coal Tower – Nurse.mkv")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    f"color=c=black:duration=3:size=320x180:rate=15[a];testsrc=duration={seconds - 3}:size=320x180"
                    f":rate=15[b];[a][b]concat=n=2:v=1:a=0",
                    "-c:v", "libx264", "-preset", "veryfast", "-g", "15", "-pix_fmt", "yuv420p", clip],
                   check=True, timeout=120)
    with open(clip + inputs.INPUTS_SUFFIX, "wb") as f:
        f.write(inputs.dump(events))
    win = qt_editor.EditorWindow(clip, [], str(tmp_path / "Clips"), sound=False)
    win.resize(1400, 860)
    win.show()
    return win


def test_the_editor_lists_moments_and_cuts_idle_and_the_loading_screen(qapp, tmp_path):
    ev = [(4.0, W), (5.0, 0)] + _busy(30, 38) + [(38.5, 0)]
    win = _editor(tmp_path, ev)
    try:
        assert _pump(qapp, lambda: win.preview._img is not None and win._pstate != "loading")
        win._inspector_refresh()
        assert win.sections["moments"].isVisibleTo(win) and win.moment_list.count() >= 1
        assert any(x <= 32 <= y for x, y, *_r in win._moments)
        before = sequence.duration(win.parts)
        win.trim_idle()                                         # 6–29 s and 39.5–59 s: nothing held
        cut = before - sequence.duration(win.parts)
        assert cut > 30 and "Leerlauf" in win.moment_status.text()
        win.undo()
        assert sequence.duration(win.parts) == before
        win.trim_dark()                                         # the first 3 s are black
        assert _pump(qapp, lambda: not win._dark_busy, 60)
        assert 2.5 <= before - sequence.duration(win.parts) <= 3.5 and win.parts[0].start >= 2.5
        win.undo()
        win.moment_list.setCurrentRow(0)
        m = win._moments[0]
        win.clip_around_moment()
        assert [(p.start, p.end) for p in win.parts] == [(m[5], m[6])]
    finally:
        win.close()


def test_claude_builds_a_short_from_stills_at_the_moments(qapp, tmp_path, monkeypatch):
    ev = _busy(30, 38) + [(38.5, 0)]
    answer = {"summary": "Short aus der Verfolgung.",
              "ops": [{"op": "keep", "from": 26, "to": 44}, {"op": "mode", "value": "shorts"},
                      {"op": "short_title", "text": "Knapp entkommen"},
                      {"op": "subtitle", "from": 2, "to": 5, "text": "jetzt!"}]}
    fake = FakeOpener(answer)
    monkeypatch.setattr(askclaude, "OPENER", fake)
    win = _editor(tmp_path, ev)
    try:
        assert _pump(qapp, lambda: win.preview._img is not None and win._pstate != "loading")
        win.claude_key = lambda: KEY
        win._claude_refresh()
        assert not win.cl_short_btn.isVisible()                 # stills not allowed by the App
        win.claude_short()
        assert fake.bodies == []
        win.claude_frame = lambda: True
        win._claude_refresh()
        assert win.cl_short_btn.isVisible()
        win.claude_short()
        assert _pump(qapp, lambda: not win._claude_busy, 60)
        content = fake.bodies[0]["messages"][0]["content"]
        words = json.dumps([b for b in content if b["type"] == "text"])
        assert "Busy moments found locally" in words and "vertical short" in words
        assert "Coal" not in words and "Nurse" not in words and "mkv" not in words and "inputs" not in words
        pictures = [b for b in content if b["type"] == "image"]
        assert len(pictures) == len(highlights.still_times(sequence.duration(win.parts), [],
                                                           [(x + y) / 2 for x, y, *_r in win._moments][:8]))
        before = [(p.start, p.end) for p in win.parts]
        assert win.cl_take_btn.isVisible() and [(p.start, p.end) for p in win.parts] == before
        win.claude_take()
        assert win.mode_box.currentData() == "shorts" and win._short.title == "Knapp entkommen"
        assert round(sequence.duration(win.parts), 1) == 18.0
        win.undo()
        assert [(p.start, p.end) for p in win.parts] == before
    finally:
        win.close()
