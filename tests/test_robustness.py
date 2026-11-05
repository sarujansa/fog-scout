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
                               events, simulate=str(tmp_path))
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
                               events, simulate=str(tmp_path))
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
