"""1.39.1: a round's inputs next to its recording – the recorder turns wall times into seconds of its file (like the
F8 marks: pauses out, a joined pre-roll in front), writes "<file>.inputs.json" only with the box on, and the file is
moved and deleted with the recording; the editor only reads files of our own format."""
import json
import os
import time

import pytest

from fogscout import inputs, obsrec, recindex
from fogscout.inputs import InputState

from test_obsrec import FakeObs, _drain, _fake_ffmpeg, _recorder


@pytest.fixture
def obs(tmp_path):
    srv = FakeObs(record_dir=str(tmp_path))
    srv.start()
    yield srv
    srv.stop()


def test_a_wall_time_becomes_a_second_of_the_file():
    a = {"since": 100.0, "pauses": [(110.0, 115.0)], "paused_at": None}
    assert obsrec.rec_position(a, 99.0) is None                    # before the recording
    assert obsrec.rec_position(a, 105.0) == 5.0
    assert obsrec.rec_position(a, 112.0) is None                   # paused
    assert obsrec.rec_position(a, 120.0) == 15.0                   # 20 s on the clock, 5 of them paused
    assert obsrec.rec_position(dict(a, paused_at=130.0), 131.0) is None
    assert obsrec.rec_position(None, 1.0) is None and obsrec.rec_position({}, 1.0) is None


def test_the_reader_logs_only_changes_and_forgets_them_once_taken():
    states = iter([InputState(keys=frozenset({"w"})), InputState(keys=frozenset({"w"})),
                   InputState(keys=frozenset({"w", "shift"})), None])
    r = inputs.Reader(poll=lambda hwnd: next(states))
    r._hwnd = 1
    for _ in range(4):
        r.look()
    log = r.take_log()
    codes = [c for _t, c in log]
    assert codes == [inputs.encode(InputState(keys=frozenset({"w"}))),
                     inputs.encode(InputState(keys=frozenset({"w", "shift"}))), inputs.encode(inputs.EMPTY)]
    assert all(abs(t - time.time()) < 5 for t, _c in log)
    assert r.take_log() == []


def test_codes_keep_what_the_card_shows():
    st = InputState(keys=frozenset({"a", "lmb"}), pad=frozenset({"b", "up"}), lt=0.5, rt=1.0, lx=0.0, ly=1.0,
                    rx=-0.4, ry=-0.4)
    back = inputs.decode(inputs.encode(st))
    for lay in ("keyboard", "gamepad"):
        assert inputs.draw_key(back, lay) == inputs.draw_key(st, lay)
    assert inputs.decode(0) == InputState(pad_on=False)


def test_only_our_own_files_are_read(tmp_path):
    good = tmp_path / "a.mkv.inputs.json"
    good.write_bytes(inputs.dump([(2.0, 5), (1.0, 3)]))
    assert inputs.load(str(good)) == [(1.0, 3), (2.0, 5)]
    for bad in ({"events": [[1, 2]]}, {"format": "other", "events": [[1, 2]]}, [1, 2],
                {"format": inputs.FILE_FORMAT, "events": [[1, "x"], [float("nan"), 1], [-1, 1], [1, -1], [True, 1]]}):
        p = tmp_path / "bad.inputs.json"
        p.write_text(json.dumps(bad))
        assert inputs.load(str(p)) == []
    (tmp_path / "broken.inputs.json").write_text("{nope")
    assert inputs.load(str(tmp_path / "broken.inputs.json")) == []
    assert inputs.load(str(tmp_path / "missing.json")) == []


def _round(r, monkeypatch=None):
    r._begin({"t": 1.0, "label": "Coal Tower", "role": "killer", "killer": "Nurse"})
    r.active["since"] -= 50                                         # 50 s into the round …
    now = time.time()
    r._inputs([(now - 60, 1), (now - 40, 2), (now - 10, 3)])        # … one before the start, two in it


def test_the_round_inputs_are_written_next_to_its_file_with_the_pre_roll_in_front(tmp_path, monkeypatch):
    run, _calls = _fake_ffmpeg()
    monkeypatch.setattr(obsrec, "ffmpeg_exe", lambda: "ffmpeg")
    monkeypatch.setattr(obsrec, "_run", run)
    obs = FakeObs(record_dir=str(tmp_path), replay=True)
    obs.start()
    try:
        r, posted = _recorder(obs, str(tmp_path), pre=True, merge=True)
        _round(r)
        r._finish({})
        rec = obsrec.load_index(str(tmp_path))[0]
        assert rec.inputs == rec.file + inputs.INPUTS_SUFFIX
        events = inputs.load(obsrec.rel_path(str(tmp_path), rec.inputs))
        assert [c for _t, c in events] == [2, 3]                    # the one before the start is left out
        assert 9 <= events[0][0] - rec.pre_s <= 11 and 39 <= events[1][0] - rec.pre_s <= 41   # pre-roll in front
        assert rec.pre_s == 20.5
        _drain(posted)
    finally:
        obs.stop()


def test_no_file_without_inputs_and_the_old_index_still_reads(obs, tmp_path):
    r, _posted = _recorder(obs, str(tmp_path), pre=False)
    r._begin({"t": 1.0, "label": "A"})
    r._finish({})
    rec = obsrec.load_index(str(tmp_path))[0]
    assert rec.inputs == "" and not [n for n in os.listdir(str(tmp_path)) if n.endswith(inputs.INPUTS_SUFFIX)]
    line = json.dumps({"t": 2.0, "file": "x.mkv"})                  # an index line from 1.39
    (tmp_path / obsrec.INDEX).write_text(line + "\n", encoding="utf-8")
    assert obsrec.load_index(str(tmp_path))[0].inputs == ""


def test_the_input_file_moves_and_goes_with_its_recording(obs, tmp_path):
    r, _posted = _recorder(obs, str(tmp_path), pre=False, farming_sub=True)
    _round(r)
    r._finish({})
    rec = obsrec.load_index(str(tmp_path))[0]
    r._set_farming(rec.t, True)                                     # into Farming/ – both files
    rec = obsrec.load_index(str(tmp_path))[0]
    assert rec.file.startswith("Farming/") and rec.inputs.startswith("Farming/")
    assert os.path.exists(obsrec.rel_path(str(tmp_path), rec.inputs))
    stranger = tmp_path / "Farming" / "notes.json"                  # not ours: stays
    stranger.write_text("{}")
    r._delete_one(rec.t)
    assert sorted(os.listdir(str(tmp_path / "Farming"))) == ["notes.json"]


def test_pruning_deletes_the_input_file_but_never_a_stranger_named_as_one(tmp_path):
    for n in ("a.mkv", "a.mkv.inputs.json", "b.mkv", "secret.txt"):
        (tmp_path / n).write_bytes(b"x" * 10)
    recs = [recindex.Recording(t=1.0, file="a.mkv", inputs="a.mkv.inputs.json"),
            recindex.Recording(t=2.0, file="b.mkv", inputs="secret.txt")]       # a hand-made entry
    left, deleted = recindex.prune(str(tmp_path), recs, limit=1, free=10 ** 12)
    assert "a.mkv.inputs.json" in deleted and "secret.txt" not in deleted
    assert (tmp_path / "secret.txt").exists() and not (tmp_path / "a.mkv.inputs.json").exists()
    assert recindex.deletable("x.inputs.json", companion=True) and not recindex.deletable("x.inputs.json")
    assert not recindex.deletable("x.json", companion=True)


@pytest.mark.parametrize("record", [True, False])
def test_the_app_hands_the_round_inputs_over_only_with_the_box(record):
    from types import SimpleNamespace

    from fogscout.app_inputs import InputsCard
    sent = []
    app = InputsCard()
    app.settings = {"overlay": {"show_inputs": True}}
    app.settings = type("S", (dict,), {"get": dict.get})(app.settings, inputs_record=record)
    app.recorder = SimpleNamespace(inputs=sent.append)
    app.inputs = inputs.Reader(poll=lambda hwnd: InputState(keys=frozenset({"w"})))
    app.inputs._hwnd = 1
    app.inputs.look()
    app._inputs_round_end()
    assert (len(sent) == 1) is record and app.inputs.take_log() == []


def test_nothing_of_the_inputs_reaches_the_log(tmp_path, caplog):
    import logging
    caplog.set_level(logging.DEBUG)
    r = inputs.Reader(poll=lambda hwnd: InputState(keys=frozenset({"w", "a"})))
    r._hwnd = 1
    r.look()
    r.take_log()
    assert "w" not in " ".join(m.lower() for m in caplog.messages if "inputs" in m.lower() or "eingaben" in m.lower())
