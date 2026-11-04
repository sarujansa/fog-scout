"""1.35: the start's phases (starttime.py) – own process only, no behaviour depends on them."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import starttime  # noqa: E402


def test_phases_are_the_time_since_the_mark_before_and_the_total_counts_the_time_before_python():
    c = starttime.StartClock(before=0.9, now=100.0)
    c.mark("splash", 100.05)
    c.mark("loaded", 101.15)
    c.mark("built", 101.55)
    c.mark("ready", 101.6)
    c.mark("ready", 109.0)                          # a second mark of the same phase does not count
    ph = c.phases_ms()
    assert [round(ph[k]) for k in ("python", "splash", "loaded", "built", "ready")] == [900, 50, 1100, 400, 50]
    assert round(c.total_ms()) == 2500
    assert c.as_dict()["total"] == 2500
    assert c.diag() == ("Start: 2,50 s (bis Python 0,90 · Ladebildschirm 0,05 · Laden 1,10 · Aufbau 0,40 · "
                        "Fenster 0,05)")


def test_without_marks_or_without_the_process_age_it_says_so():
    c = starttime.StartClock(before=None, now=5.0)
    c.before = None
    assert c.total_ms() is None and c.diag() == "Start: nicht gemessen"
    c.mark("ready", 6.0)
    assert round(c.total_ms()) == 1000 and "bis Python" not in c.diag()


def test_the_process_age_is_this_process_only_and_plausible():
    age = starttime.process_age_s()
    if sys.platform.startswith("linux") or sys.platform == "win32":
        assert age is not None and 0.0 <= age < 24 * 3600
        time.sleep(0.05)
        assert starttime.process_age_s() >= age


def test_a_failing_reading_never_stops_the_start(monkeypatch):
    """1.35 (CI on Windows): GetProcessTimes without argtypes raised ctypes.ArgumentError in __main__ – any error
    of the reading gives None."""
    import builtins

    def broken(*a, **kw):
        raise RuntimeError("no reading")
    monkeypatch.setattr(builtins, "open", broken)
    monkeypatch.setattr(starttime.ctypes, "WinDLL", broken, raising=False)
    assert starttime.process_age_s() is None
    assert starttime.StartClock().before is None


def test_the_self_check_reports_the_start_times(tmp_path):
    from fogscout import selftest
    c = starttime.StartClock(before=0.4)
    res = selftest.run(str(tmp_path), c)
    assert res["start"]["python_ms"] == 400 and res["start"]["modules_ms"] >= 0
