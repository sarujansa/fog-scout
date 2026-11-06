"""1.8.38 (QA audit): failures in one part must not leave the user with a dead detection, a map that stays up after
the round or OBS recording on after quitting – the detection loop, the round end in the app, quitting."""
import json
import os
import queue
import sys
import time

import cv2
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from fogscout import config, worker  # noqa: E402
from fogscout.catalog import Catalog  # noqa: E402


def _events(q, timeout, until):
    """Events of the worker until ``until(kinds)`` holds or the time is up."""
    seen, end = [], time.time() + timeout
    while time.time() < end and not until([e.kind for e in seen]):
        try:
            seen.append(q.get(timeout=0.1))
        except queue.Empty:
            pass
    return seen


def _worker(tmp_path, monkeypatch, fails):
    """A worker in simulation whose picture source raises for the first ``fails`` frames (None = always)."""
    frame = cv2.imread(os.path.join(ROOT, "tests", "data", "end", "spectate.jpg"))
    calls = {"n": 0}

    class Source:
        def __init__(self, *_a, **_k):
            pass

        def current(self):
            calls["n"] += 1
            if fails is None or calls["n"] <= fails:
                raise RuntimeError("bad frame")
            return frame

    monkeypatch.setattr(worker, "ImageSource", Source)
    monkeypatch.setattr(worker, "TICK_FAIL_WAIT_S", 0.01)
    events = queue.Queue()
    w = worker.DetectionWorker(ROOT, config.Settings(str(tmp_path / "settings.json")), Catalog(ROOT, ["en"]),
                               events, simulate=str(tmp_path), data_dir=str(tmp_path))
    return w, events, calls


def test_a_frame_that_raises_does_not_end_the_detection(tmp_path, monkeypatch):
    """Before, any exception in the loop (OCR, capture, a tracker) ended the thread for good: no end of the round,
    no next map until a restart – and only a bar in the hidden main window said so."""
    w, events, calls = _worker(tmp_path, monkeypatch, fails=3)
    w.start()
    try:
        seen = _events(events, 20, lambda kinds: "status" in kinds)
        kinds = [e.kind for e in seen]
        assert "status" in kinds and "error" not in kinds              # it went on with the next frame
        warns = [e.data["text"] for e in seen if e.kind == "warn"]
        assert len(warns) == 1 and warns[0].startswith("Erkennung:") and "bad frame" in warns[0]   # told once
        assert calls["n"] > 3 and w.is_alive()
    finally:
        w.stop()
        w.join(timeout=10)
    assert not w.is_alive()


def test_a_detection_that_fails_every_frame_is_reported_as_crashed(tmp_path, monkeypatch):
    """1.38.9: started again WORKER_RESTARTS times first (each run gives up after TICK_FAIL_LIMIT ticks) – only the
    last failure is a crash, reported once."""
    monkeypatch.setattr(worker, "TICK_FAIL_LIMIT", 4)
    monkeypatch.setattr(worker, "WORKER_RESTART_S", 0.01)
    w, events, calls = _worker(tmp_path, monkeypatch, fails=None)
    w.start()
    seen = _events(events, 20, lambda kinds: "error" in kinds)
    w.join(timeout=10)
    assert [e.kind for e in seen].count("error") == 1 and "bad frame" in seen[-1].data["text"]
    restarts = [e.data["text"] for e in seen if e.kind == "warn" and "neu gestartet" in e.data["text"]]
    assert restarts == ["Erkennung neu gestartet (1/2)", "Erkennung neu gestartet (2/2)"]
    assert calls["n"] == 4 * (worker.WORKER_RESTARTS + 1) and not w.is_alive()


def test_a_detection_that_broke_once_runs_on_after_its_restart(tmp_path, monkeypatch):
    """1.38.9: before, a passing cause (display change, lock screen) left the detection off until Fog Scout was
    restarted – now the run after the pause goes on, and nothing is reported as a crash."""
    monkeypatch.setattr(worker, "TICK_FAIL_LIMIT", 4)
    monkeypatch.setattr(worker, "WORKER_RESTART_S", 0.01)
    w, events, calls = _worker(tmp_path, monkeypatch, fails=4)
    w.start()
    try:
        seen = _events(events, 20, lambda kinds: "status" in kinds)
        kinds = [e.kind for e in seen]
        assert "status" in kinds and "error" not in kinds and calls["n"] > 4 and w.is_alive()
        assert "Erkennung neu gestartet (1/2)" in [e.data.get("text") for e in seen if e.kind == "warn"]
    finally:
        w.stop()
        w.join(timeout=10)
    assert not w.is_alive()


def test_stopping_during_the_restart_pause_ends_at_once_without_a_crash(tmp_path, monkeypatch):
    """The pause is 30 s here; the thread must be gone within the join's 10 s – stop() ends the pause (_nap)."""
    monkeypatch.setattr(worker, "TICK_FAIL_LIMIT", 2)
    monkeypatch.setattr(worker, "WORKER_RESTART_S", 30.0)
    w, events, calls = _worker(tmp_path, monkeypatch, fails=None)
    w.start()
    end, pausing = time.time() + 20, False
    while time.time() < end and not pausing:                       # until the first restart's pause begins
        try:
            e = events.get(timeout=0.1)
        except queue.Empty:
            continue
        pausing = e.kind == "warn" and "neu gestartet" in e.data["text"]
    assert pausing
    w.stop()
    w.join(timeout=10)
    rest = []
    while not events.empty():
        rest.append(events.get_nowait().kind)
    assert not w.is_alive() and "error" not in rest and calls["n"] == 2   # no second run started


# ------------------------------------------------------------------ the app
@pytest.fixture
def app(tmp_path):
    if sys.platform == "win32":
        pytest.skip("Linux: the Windows job tests the native parts; the app would touch the system there")
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    for name in ("maps", "models", "maps.json"):
        os.symlink(os.path.join(ROOT, name), tmp_path / name)
    (tmp_path / "sim").mkdir()
    (tmp_path / "settings.json").write_text(json.dumps({"welcome_seen": True}), encoding="utf-8")
    from fogscout.app import App
    a = App(str(tmp_path), simulate=str(tmp_path / "sim"))
    yield a
    a.quit()


def test_the_map_is_hidden_at_the_round_end_even_when_saving_the_round_fails(app):
    """The worker sends match_end once: when saving the round raised before, the map stayed up into the lobby."""
    app.show_map("shattered-square", 1, "auto")
    assert app.overlay.has_map() and not app.hidden_after_match

    def broken(*_a, **_k):
        raise OSError("rounds.jsonl locked")

    app._hist_close = broken
    app._dispatch(worker.Event("match_end", {"t": time.time(), "reason": "Ergebnisbildschirm"}))
    assert app.hidden_after_match and not app.menu_paused
    assert "Rundenverlauf" in app._errors_seen                         # and the user hears of it


def test_a_repeating_error_is_logged_once_a_minute_and_counted_in_the_window(app, caplog):
    """1.38.9: before, every call wrote the full traceback to the log (a tick step: up to 4×/s, into a log file
    without a size limit) and the window said it once, never that it kept coming."""
    import logging
    lines = []
    app._log = lambda text, kind="System": lines.append(text)
    text = "Traceback (most recent call last):\n  File x\nValueError: kaputt"
    with caplog.at_level(logging.ERROR, logger="fogscout"):
        for i in range(100):                                       # 25 s of a broken tick step
            app._report_once("Testschritt", text, now=1000.0 + i * 0.25)
        app._report_once("Testschritt", text, now=1000.0 + app.REPORT_LOG_S + 1)
    logged = [r.getMessage() for r in caplog.records if "ValueError: kaputt" in r.getMessage()]
    assert len(logged) == 2 and "(99× ohne Eintrag seit " in logged[1]
    assert lines == ["Testschritt: ValueError: kaputt – Details in fogscout.log"]      # the window: once so far
    app._report_once("Testschritt", text, now=1000.0 + app.REPORT_UI_S + 1)
    assert len(lines) == 2 and lines[1].startswith("Testschritt: ValueError: kaputt (101× seit ")
    assert app._error_counts["Testschritt"] == 102


def test_a_crashed_detection_shows_in_the_status_line(app):
    from fogscout import status
    app._dispatch(worker.Event("error", {"text": "Traceback …\nRuntimeError: boom"}))
    assert status.is_problem(app._worker_status) and "neu starten" in app._worker_status


def test_a_round_still_open_at_quit_is_kept_as_a_lost_round(app):
    """1.38.24 (review STAB-7): quit closed nothing – a round open at quit (or logoff) vanished without a trace."""
    from fogscout import history
    app._dispatch(_detected("coal-tower", 1))
    assert app._hist is not None
    app.recorder.quit = lambda: None
    app.recorder.join = lambda timeout=None: None
    app.quit()
    lost = history.load_lost(app._hist_path())
    assert len(lost) == 1 and lost[0][1].startswith("Coal Tower") and lost[0][2] == "quit"
    assert history.load_lost_rounds(app._hist_path())[0].map_id == "coal-tower" and app._hist is None


def test_quitting_runs_every_step_even_when_one_raises(app):
    calls = []

    def broken():
        raise RuntimeError("tray gone")

    app.tray.stop = broken
    save = app.settings.save
    app.settings.save = lambda: (calls.append("save"), save())
    app.recorder.quit = lambda: calls.append("recorder")
    app.recorder.join = lambda timeout=None: calls.append(("join", timeout))
    app.quit()
    assert calls == ["save", "recorder", ("join", 8)]
    assert not app.worker.is_alive()


def _detected(map_id, variant, p=0.9):
    return worker.Event("detected", {"map_id": map_id, "variant": variant, "probability": p,
                                     "variant_probability": p, "name_text": "COAL TOWER", "realm_text": "MACMILLAN"})


def test_the_round_follows_the_layout_read_later_in_the_same_banner(app):
    """1.8.39 (QA audit): later frames of one banner may decide another layout (Coal Tower I → II) – the overlay
    switched, but the round and its recording kept the first reading; a correction with the layout button too."""
    relabels = []
    app.recorder.relabel = lambda **meta: relabels.append(meta)
    starts = []
    app.recorder.start_round = lambda **meta: starts.append(meta)
    app._dispatch(_detected("coal-tower", 1))
    assert app._hist["map"] == "Coal Tower I" and len(starts) == 1
    t0 = app._hist["t"]
    app._dispatch(_detected("coal-tower", 2))                  # 3 frames later: the other layout
    assert app.current == ("coal-tower", 2)
    assert app._hist["map"] == "Coal Tower II" and app._hist["t"] == t0       # the same round, renamed
    assert relabels == [{"map_id": "coal-tower", "label": "Coal Tower II"}] and len(starts) == 1   # no new recording
    app.next_variant()                                         # the user: no, it was I
    assert app._hist["map"] == "Coal Tower I" and relabels[-1]["label"] == "Coal Tower I"
    app._dispatch(_detected("coal-tower", 1))                  # the same again: nothing to rename
    assert len(relabels) == 2


def test_a_map_shown_after_the_round_ended_does_not_rename_it(app):
    app.recorder.relabel = lambda **meta: pytest.fail("renamed a closed round")
    app.recorder.start_round = app.recorder.stop_round = lambda **meta: None
    app._dispatch(_detected("coal-tower", 1))
    app._dispatch(worker.Event("match_end", {"t": time.time() + 300, "reason": "Ergebnisbildschirm"}))
    assert app._hist is None
    app.next_variant()                                         # looking at the other layout in the lobby


def test_stopping_the_worker_does_not_wait_for_its_nap(tmp_path, monkeypatch):
    """1.8.84 (idea 8 of the UI review): without a picture the simulation slept half a second per loop and
    quitting waited for it – the nap now ends with the stop command."""
    w, events, calls = _worker(tmp_path, monkeypatch, fails=None)

    class Empty:
        def __init__(self, folder):
            pass

        def current(self):
            return None
    monkeypatch.setattr(worker, "ImageSource", Empty)
    w = worker.DetectionWorker(ROOT, config.Settings(str(tmp_path / "settings.json")), Catalog(ROOT, ["en"]),
                               events, simulate=str(tmp_path), data_dir=str(tmp_path))
    # 1.28 (audit F12): no time limit on a shared runner – every nap lasts ten minutes here; the worker ending at
    # all (join well before that) shows the stop command ended the nap
    import threading
    napping, real_nap = threading.Event(), w._nap

    def long_nap(seconds):
        napping.set()
        real_nap(600.0)
    w._nap = long_nap
    w.start()
    assert napping.wait(30)
    w.stop()
    w.join(timeout=60)
    assert not w.is_alive()


def _start(tmp_path, settings, rounds=None, matches=None):
    """A real App on a root with the given settings.json and history files (None = file missing)."""
    if sys.platform == "win32":
        pytest.skip("Linux: the Windows job tests the native parts; the app would touch the system there")
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    for name in ("maps", "models", "maps.json"):
        os.symlink(os.path.join(ROOT, name), tmp_path / name)
    (tmp_path / "sim").mkdir()
    (tmp_path / "settings.json").write_text(json.dumps(settings), encoding="utf-8")
    for name, data in (("rounds.jsonl", rounds), ("official.jsonl", matches)):
        if data is not None:
            (tmp_path / name).write_bytes(data)
    from fogscout.app import App
    return App(str(tmp_path), simulate=str(tmp_path / "sim"))


def _pump_app(a, seconds):
    from PySide6.QtWidgets import QApplication
    end = time.time() + seconds
    while time.time() < end:
        QApplication.processEvents()
        time.sleep(0.01)


def test_a_start_with_old_settings_and_broken_history_files_keeps_what_is_readable(tmp_path):
    """Post-review 1.16.2: settings of an old version with the OBS password in clear text, rounds.jsonl with broken,
    cut and binary lines, official.jsonl that is no JSON at all – the start works, the readable round counts, the
    password is taken over (protected on disk, clear in the field), and every page opens in quick succession."""
    good = json.dumps({"t": time.time() - 3600, "seconds": 600, "map_id": "coal-tower", "map": "Coal Tower",
                       "region": "", "source": "auto"})
    rounds = (good + "\n{broken\n" + '{"t": 1, "seconds": "x"}\n').encode() + b"\xff\xfe\x00junk\n" + b'{"t": 2, "map": "\xe2\x82'
    a = _start(tmp_path, {"settings_version": 5, "welcome_seen": True, "rec_password": "hunter2"},
               rounds=rounds, matches=b"\x00\x01 not json at all\n[1, 2]\n")
    try:
        from fogscout import app_settings
        assert a.rec_pw_var.get() == "hunter2"
        stored = a.settings.get("rec_password")
        assert app_settings.is_protected(stored) and "hunter2" not in stored
        _pump_app(a, 0.5)
        assert [r.map_id for r in a._joined().rounds] == ["coal-tower"] and a._joined().matches == []
        q = a.qt
        for _ in range(3):                                   # quick page changes while the warm-up runs
            for key in q.nav_keys():
                q.show_page(key)
                _pump_app(a, 0.02)
        _pump_app(a, 0.5)
        assert not a._errors_seen
        assert all(cat != "Fehler" for _t, cat, *_r in a._log_entries), [e for e in a._log_entries if e[1] == "Fehler"]
    finally:
        a.quit()


def test_a_start_without_any_history_file_is_quiet(tmp_path):
    a = _start(tmp_path, {"welcome_seen": True})
    try:
        _pump_app(a, 0.3)
        j = a._joined()
        assert j.rounds == [] and j.matches == [] and not a._errors_seen
        assert a.rec_pw_var.get() == "" and a.settings.get("rec_password") == ""
    finally:
        a.quit()


def test_an_unreadable_obs_password_stays_until_a_new_one_is_typed(tmp_path):
    """1.28 (audit F2b) – replaces the 1.16.2 test "is replaced on the next save": a value this PC cannot read is
    no longer overwritten by any save (a switch elsewhere on the OBS card wiped it); the error line says so, only a
    password the user types replaces it. Never the value in the log."""
    from fogscout import spotify
    a = _start(tmp_path, {"welcome_seen": True, "rec_password": "dpapi:AAAA"})
    try:
        assert a.rec_pw_var.get() == ""
        assert [t for _c, cat, t in a._log_entries if cat == "Fehler" and "OBS-Passwort" in t]
        assert "AAAA" not in " ".join(t for *_x, t in a._log_entries)
        a._rec_setting()
        a.rec_on_var.set(not a.rec_on_var.get())
        a._rec_setting()
        assert a.settings.get("rec_password") == "dpapi:AAAA"
        a.rec_pw_var.set("neu")
        stored = a.settings.get("rec_password")
        assert spotify.is_encrypted(stored) and spotify.unprotect(stored) == "neu"
    finally:
        a.quit()


def _secret_values():
    import base64
    return {k: "plain:" + base64.b64encode(("alt-" + k).encode()).decode()
            for k in ("rec_password", "spotify_token", "youtube_client_secret", "youtube_token", "claude_key")}


def test_old_plain_secrets_are_encrypted_on_the_start(tmp_path):
    """1.28 (audit F2): "plain:" (Base64, before 1.28) of every secret is encrypted on the start – read back the
    same, nothing in the file readable any more."""
    from fogscout import spotify
    old = _secret_values()
    a = _start(tmp_path, dict({"welcome_seen": True}, **old))
    try:
        for name in old:
            stored = a.settings.get(name)
            assert spotify.is_encrypted(stored) and spotify.unprotect(stored) == "alt-" + name, name
        a.settings.save()
        text = (tmp_path / "settings.json").read_text(encoding="utf-8")
        assert "plain:" not in text and not any(v[6:] in text for v in old.values())
        assert not [t for _c, cat, t in a._log_entries if "Unverschlüsselt" in t]
    finally:
        a.quit()


def test_without_the_windows_encryption_secrets_live_for_the_session_only(tmp_path, monkeypatch, caplog):
    """1.28 (audit F2/F2b): no DPAPI – old "plain:" values stay as they are (the log names the settings, never a
    value), a newly typed OBS password or YouTube secret works for this run but is not written; nothing new in
    clear text or Base64 lands in settings.json."""
    import base64
    import logging
    from fogscout import spotify
    caplog.set_level(logging.DEBUG)
    monkeypatch.setattr(spotify, "CIPHER", None)
    old = _secret_values()
    a = _start(tmp_path, dict({"welcome_seen": True}, **old))
    try:
        assert {k: a.settings.get(k) for k in old} == old
        line = [t for _c, cat, t in a._log_entries if cat == "Fehler" and "Unverschlüsselt" in t]
        assert line and "rec_password" in line[0] and "alt-" not in line[0]
        a.rec_pw_var.set("geheim-obs")
        a.yt_secret_var.set("geheim-yt")
        assert a._rec_cfg().password == "geheim-obs" and a.yt_secret_var.get() == "geheim-yt"
        assert a.settings.get("rec_password") == old["rec_password"]
        assert a.settings.get("youtube_client_secret") == old["youtube_client_secret"]
        assert [t for _c, _cat, t in a._log_entries if "OBS-Passwort gilt nur bis zum Beenden" in t]
        assert [t for _c, _cat, t in a._log_entries if "Client-Secret gilt nur bis zum Beenden" in t]
        a.settings.save()
        text = (tmp_path / "settings.json").read_text(encoding="utf-8")
        for secret in ("geheim-obs", "geheim-yt"):
            assert secret not in text and base64.b64encode(secret.encode()).decode() not in text
        logs = caplog.text + " ".join(t for *_x, t in a._log_entries)
        assert "geheim" not in logs and not any(v[6:] in logs for v in old.values())
    finally:
        a.quit()


def test_the_tray_opens_the_window_on_a_page(app):
    """1.17: the tray's Statistik / Aufnahmen open the window on that page; an unknown action does nothing."""
    app._dispatch(("tray", "page:stats"))
    assert app.qt.current_key() == "stats"
    app._dispatch(("tray", "page:recordings"))
    assert app.qt.current_key() == "recordings"
    app._dispatch(("tray", "nonsense"))
    assert app.qt.current_key() == "recordings"


def test_a_round_of_the_overview_opens_in_the_statistics_and_its_recording(tmp_path):
    """1.17.1: rows of the overview's "Letzte Runden" – a click opens Statistik › Letzte Runden with the round
    marked; ▶ shows only with a recording of it (same start time, file there) and opens it on Aufnahmen. A round
    without a recording, a recording whose file is gone and a broken index line raise nothing."""
    from fogscout import history, obsrec, overview
    now = time.time()
    t_rec, t_gone, t_none = now - 7200, now - 5400, now - 3600
    rounds = b"".join(json.dumps({"t": t, "seconds": 600, "map_id": "coal-tower", "map": "Coal Tower", "role": "killer",
                                  "source": "auto"}).encode() + b"\n" for t in (t_rec, t_gone, t_none))
    folder = tmp_path / "rec"
    folder.mkdir()
    (folder / "a.mkv").write_bytes(b"\0" * 100)
    a = _start(tmp_path, {"welcome_seen": True, "rec_folder": str(folder)}, rounds=rounds)
    try:
        a.recorder.folder = lambda: str(folder)
        obsrec.save_index(str(folder), [obsrec.Recording(t=t_rec, file="a.mkv", label="Coal Tower", end=t_rec + 600),
                                        obsrec.Recording(t=t_gone, file="gone.mkv", label="Coal Tower",
                                                         end=t_gone + 600)])
        with open(folder / obsrec.INDEX, "a", encoding="utf-8") as fh:
            fh.write("{broken\n")
        _pump_app(a, 0.3)
        rows = {r.t: r for r in overview.last_rounds(a)}
        assert rows[t_rec].recording == str(folder / "a.mkv")
        assert rows[t_gone].recording is None and rows[t_none].recording is None
        a._qt_event("ov_round", t_none)
        assert a.qt.current_key() == "stats" and a.stats_last.selection() == (repr(t_none),)
        assert a.stats_sel.winfo_manager() and not a.stats_sel_hint.winfo_manager()      # bar for the marked round
        a.stats_last.selection_set()
        a._stats_role_buttons()
        assert not a.stats_sel.winfo_manager() and a.stats_sel_hint.winfo_manager()      # nothing marked: the hint
        assert a._stats_last_menu_items() == []                                          # right click as before
        a._qt_event("ov_recording", t_rec)
        assert a.qt.current_key() == "recordings" and a.rec_table.selection() == (repr(t_rec),)
        assert a._show_round_recording(t_none) is False                                  # none: nothing marked
        assert history.load(a._hist_path())                                              # nothing written
    finally:
        a.quit()


def test_last_rounds_open_the_recording_of_a_round(tmp_path):
    """1.38.46 (user: "Aufnahme direkt aus „Letzte Runden“ öffnen"): Statistik › Letzte Runden – right click on one
    round offers „Aufnahme zeigen“ / „abspielen“ / „Clip bearbeiten …“, active only with a recording of it; several
    rounds marked: not offered. Double-click / Enter shows the recording on Aufnahmen; without one a log line and the
    page stays. „Abspielen“ opens only video files (the index is user-writable)."""
    from fogscout import obsrec
    now = time.time()
    t_rec, t_none, t_txt = now - 7200, now - 3600, now - 1800
    rounds = b"".join(json.dumps({"t": t, "seconds": 600, "map_id": "coal-tower", "map": "Coal Tower", "role": "killer",
                                  "source": "auto"}).encode() + b"\n" for t in (t_rec, t_none, t_txt))
    folder = tmp_path / "rec"
    folder.mkdir()
    (folder / "a.mkv").write_bytes(b"\0" * 100)
    (folder / "notes.txt").write_text("x")
    a = _start(tmp_path, {"welcome_seen": True, "rec_folder": str(folder)}, rounds=rounds)
    try:
        a.recorder.folder = lambda: str(folder)
        obsrec.save_index(str(folder), [obsrec.Recording(t=t_rec, file="a.mkv", label="Coal Tower", end=t_rec + 600),
                                        obsrec.Recording(t=t_txt, file="notes.txt", label="Coal Tower",
                                                         end=t_txt + 600)])
        _pump_app(a, 0.3)
        assert a._show_round(t_rec)

        def items():
            return {i[0]: i[2] for i in a._stats_last_menu_items() if i}
        got = items()
        assert got["rec_show"] and got["rec_play"] and got["rec_clip"]
        assert a._show_round(t_none)
        got = items()
        assert not got["rec_show"] and not got["rec_play"] and not got["rec_clip"]       # no recording: greyed out
        a.stats_last.selection_set(repr(t_rec), repr(t_none))
        assert "rec_show" not in items()                                                 # several rounds: none
        a.stats_last._dbdms_open(repr(t_none))                                           # double-click, none
        assert a.qt.current_key() == "stats"
        assert [t for _c, _cat, t in a._log_entries if "keine Aufnahme" in t]
        opened = []
        a._open = opened.append
        a._show_round(t_txt)
        a._stats_last_menu_act("rec_play")                                               # not a video: refused
        assert opened == [] and [t for _c, _cat, t in a._log_entries if "Keine Videodatei" in t]
        a._show_round(t_rec)
        a._stats_last_menu_act("rec_play")                                               # plays, page stays
        assert opened == [str(folder / "a.mkv")] and a.qt.current_key() == "stats"
        a.stats_last._dbdms_open(repr(t_rec))                                            # double-click: shown
        assert a.qt.current_key() == "recordings" and a.rec_table.selection() == (repr(t_rec),)
    finally:
        a.quit()


def test_a_session_opens_its_rounds_in_last_rounds(tmp_path):
    """1.38.47 (user's pick "Sitzungen als eigener Reiter", double-click marks): Statistik › Runden › Sitzungen
    lists the sessions newest first; a double-click opens Letzte Runden with exactly the session's rounds marked –
    also for an old session beyond the first 100 rows (more are loaded)."""
    now = time.time()
    old = [now - 400 * 3600, now - 400 * 3600 + 900]                    # one session, two rounds, long ago
    singles = [now - (i + 2) * 3600 for i in range(120)]                # 120 sessions of one round each, newer
    rounds = b"".join(json.dumps({"t": t, "seconds": 600, "map_id": "coal-tower", "map": "Coal Tower",
                                  "role": "killer", "source": "auto"}).encode() + b"\n" for t in old + singles)
    a = _start(tmp_path, {"welcome_seen": True}, rounds=rounds)
    try:
        _pump_app(a, 0.3)
        a.qt.show_page("stats")
        a._stats_select(_tab_title(a, "Sitzungen"))
        a._stats_render()
        a._stats_render_tab()
        rows = a.stats_sess.get_children()
        assert len(rows) == 121 and rows[-1] == repr(old[0])            # newest first, the old session last
        assert a.stats_sess_tiles.data and a.stats_sess_tiles.data[0].value == "121"
        assert a._stats_last_limit < 122
        a.stats_sess._dbdms_open(repr(old[0]))
        assert a._stats_current_title() == "Letzte Runden"
        assert sorted(a.stats_last.selection()) == sorted(repr(t) for t in old)
        a.stats_sess._dbdms_open("nonsense")                              # an unknown row does nothing
    finally:
        a.quit()


def _tab_title(a, title):
    assert title in [t for t, _p in a._stats_parts.values()]
    return title


def test_the_prestige_tab_lists_own_characters_and_draws_the_marked_one(tmp_path):
    """1.38.49 (user's pick "Prestige- und Level-Verlauf", table + line of the clicked character): Statistik ›
    Bloodpoints & Farming › Prestige (1.38.51; Gegner & Builds before) – one row per own character from the linked matches, the newest first and marked,
    its line drawn; marking the other row draws that one; without any grade a hint and an empty line."""
    from dataclasses import asdict
    from fogscout.official import Match
    now = time.time()
    plays = [(now - 7200, "The Nurse", "killer", 4, 10), (now - 5400, "Meg Thomas", "survivor", 10, 20),
             (now - 3600, "The Nurse", "killer", 4, 30)]
    rounds = b"".join(json.dumps({"t": t, "seconds": 600, "map_id": "coal-tower", "map": "Coal Tower", "role": role,
                                  "source": "auto"}).encode() + b"\n" for t, _c, role, _p, _l in plays)
    matches = b"".join(json.dumps(asdict(Match(t=t - 38, map="Coal Tower", role=role, character=c, seconds=600,
                                               prestige=p, level=lvl))).encode() + b"\n"
                       for t, c, role, p, lvl in plays)
    a = _start(tmp_path, {"welcome_seen": True}, rounds=rounds, matches=matches)
    try:
        _pump_app(a, 0.3)
        a.qt.show_page("stats")
        a._stats_select("Prestige")
        a._stats_render()
        a._stats_render_tab()
        t = a.stats_prestige
        names = [t.item(i, "values")[0] for i in t.get_children()]
        # 1.38.50: the main per role is marked; two matches an hour apart give no pace (span under three days)
        assert names == ["The Nurse · Main", "Meg Thomas · Main"] and t.selection() == ("0",)
        assert list(t.item("0", "values"))[2:5] == [4, 30, "+20 Level"]
        assert list(t.item("0", "values"))[7:9] == ["–", "–"]
        assert [x.title for x in a.stats_prestige_tiles.data][:2] == ["Charaktere", "Prestige gesamt"]
        assert a.stats_prestige._dbdms_hide == ("last",)
        panel = a.prestige_trend.data["prestige"]
        assert "The Nurse" in panel["title"] and panel["last"] == "P4 · 30"
        t.selection_set("1")
        t.event_generate("<<TreeviewSelect>>")
        assert "Meg Thomas" in a.prestige_trend.data["prestige"]["title"]
        assert not a.stats_prestige_var.get()
    finally:
        a.quit()


def test_reading_a_higher_prestige_grade_announces_it(tmp_path):
    """1.38.50 (user's pick "Meilenstein-Meldung"): the userscript's file brings a match with The Nurse at P10 while
    the stored matches knew P9 – the import's notification and the log say "Meilenstein: The Nurse ist jetzt
    Prestige 10"; a second file with the same grade says nothing more."""
    from dataclasses import asdict
    from fogscout.official import FORMAT, Match
    now = time.time()
    known = json.dumps(asdict(Match(t=now - 86400, map="Coal Tower", role="killer", character="The Nurse",
                                    seconds=600, prestige=9, level=50))).encode() + b"\n"
    dl = tmp_path / "downloads"
    dl.mkdir()
    a = _start(tmp_path, {"welcome_seen": True, "official_dir": str(dl)}, matches=known)
    try:
        shown = []
        a.toast.show = lambda title, text: shown.append(text)

        def drop(t, level):
            (dl / "fogscout-matches.json").write_text(json.dumps({
                "format": FORMAT, "version": 1, "script": 5, "exported": now, "matches": [
                    {"start": t, "map": "Coal Tower", "custom": False, "opponents": [],
                     "player": {"role": "VE_Slasher", "character": "The Nurse", "status": None, "seconds": 600,
                                "bp": 20000, "prestige": 10, "level": level}}]}), encoding="utf-8")
            a._official_take()
        drop(now - 3600, 2)
        assert shown and "Meilenstein: The Nurse ist jetzt Prestige 10" in shown[-1]
        assert [x for _c, _cat, x in a._log_entries if "ist jetzt Prestige 10" in x]
        drop(now - 1800, 5)                                                   # same grade: nothing new
        assert len(shown) == 2 and "ist jetzt Prestige" not in shown[-1]
    finally:
        a.quit()


def test_the_overview_tiles_open_their_rounds(tmp_path):
    """1.38.53 (user: "auf Rounds 8 heute klicken soll es mir diese zeigen – genau gleich bei den anderen Kacheln"):
    the tile "Runden" of "Heute" opens Statistik › Letzte Runden with the period "Heute", every other filter reset
    and farming shown (the count holds the farming rounds) – exactly its rounds; Farming, Bloodpoints of the week,
    a role and the recordings page open their part; "Farming ausblenden" is never switched on."""
    from fogscout import overview
    now = time.time()
    day = __import__("fogscout.history", fromlist=["x"]).period_start("day", now)
    rows = [("killer", False)] * 3 + [("survivor", False)] * 2 + [("killer", True)] * 2
    rounds = b"".join(json.dumps({"t": day + 60 + i * 700, "seconds": 600, "map_id": "coal-tower", "map": "Coal Tower",
                                  "role": role, "farming": farm, "source": "auto"}).encode() + b"\n"
                      for i, (role, farm) in enumerate(rows) if day + 60 + i * 700 < now)
    a = _start(tmp_path, {"welcome_seen": True, "hide_farming": True}, rounds=rounds)
    try:
        _pump_app(a, 0.3)
        n = len([1 for i in range(len(rows)) if day + 60 + i * 700 < now])
        facts, _note = overview.today(a, now)
        tile = next(f for f in facts if f.title == "Runden")
        assert tile.open == "day:last:all" and tile.value == str(n)
        a.stats_map_var.set("Coal Tower")                                          # a filter of the user: reset
        a._qt_event("tile_open", tile.open)
        assert a.qt.current_key() == "stats" and a._stats_current_title() == "Letzte Runden"
        assert a.stats_period_var.get() == "Heute" and a.stats_map_var.get() == "Alle Maps"
        assert not a._farming_hidden() and len(a.stats_last.get_children()) == n
        a._qt_event("tile_open", "day:last:survivor")
        assert a.stats_role_var.get() == "Survivor"
        assert all("Survivor" in a.stats_last.item(i, "values")[4] for i in a.stats_last.get_children())
        farm = next((f for f in facts if f.title == "Farming"), None)
        if farm is not None:
            a._qt_event("tile_open", farm.open)
            assert a._stats_current_title() == "Farming"
        a._farming_set(True)
        a._qt_event("tile_open", "week:bp:all")
        assert a._stats_current_title() == "Bloodpoints" and a.stats_period_var.get() == "Diese Woche"
        assert a._farming_hidden()                                                 # never switched on or off here
        a._qt_event("tile_open", "page:recordings")
        assert a.qt.current_key() == "recordings"
        a._qt_event("tile_open", "nonsense:x:y")                                   # unknown: nothing happens
        assert a.qt.current_key() == "recordings"
    finally:
        a.quit()


def test_record_and_dashboard_tiles_open_their_rounds_with_the_filters_kept(tmp_path):
    """1.38.54 (user: "mach das auch für die anderen Kacheln, wo es Sinn macht"): in the statistics a click on
    "Längste Runde" marks exactly that round under „Letzte Runden“, "Meiste Runden an einem Tag" all rounds of that
    day, and "Ø Wartezeit" of the overview opens the tab Wartezeit – the user's period filter stays as it was."""
    now = time.time()
    day = __import__("fogscout.history", fromlist=["x"]).period_start("day", now)
    start = day - 3 * 86400 + 20 * 3600                                   # three days ago, 20:00
    plan = [(start, 600), (start + 900, 1500), (start + 2700, 700), (start - 86400, 800)]
    rounds = b"".join(json.dumps({"t": t, "seconds": s, "map_id": "coal-tower", "map": "Coal Tower", "role": "killer",
                                  "wait": 60, "source": "auto"}).encode() + b"\n" for t, s in plan)
    a = _start(tmp_path, {"welcome_seen": True}, rounds=rounds)
    try:
        _pump_app(a, 0.3)
        a.qt.show_page("stats")
        a.stats_period_var.set(dict(a._stats_periods)["30d"])              # the user's own filter
        a._stats_select("Rekorde")
        a._stats_render()
        a._stats_render_tab()
        tiles = {t.title: t for t in a.stats_records.data}
        a._qt_event("tile_open", tiles["Längste Runde"].open)
        assert a._stats_current_title() == "Letzte Runden" and a.stats_last.selection() == (repr(float(start + 900)),)
        assert a.stats_period_var.get() == dict(a._stats_periods)["30d"]
        a._qt_event("tile_open", tiles["Meiste Runden an einem Tag"].open)
        assert sorted(a.stats_last.selection()) == sorted(repr(float(t)) for t, _s in plan[:3])
        a._stats_select("Übersicht")
        a._stats_render()
        a._stats_render_tab()
        wait = next(t for t in a.stats_dash.data.tiles if t.title == "Ø Wartezeit")
        a._qt_event("tile_open", wait.open)
        assert a._stats_current_title() == "Wartezeit" and a.stats_period_var.get() == dict(a._stats_periods)["30d"]
        a._qt_event("tile_open", "rounds:not-a-number")                      # broken target: nothing happens
        assert a._stats_current_title() == "Wartezeit"
    finally:
        a.quit()
