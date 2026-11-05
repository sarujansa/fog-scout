"""1.8.31: the overlay tick's steps timed for the diagnosis (ticktime.TickTimes)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fogscout.ticktime import TickTimes  # noqa: E402


def test_steps_add_up_and_the_map_is_the_rest():
    tt = TickTimes(kept=3)
    for total, hud, music in ((20.0, 5.0, 8.0), (40.0, 6.0, 20.0), (10.0, 1.0, 2.0), (12.0, 2.0, 3.0)):
        tt.start()
        tt.add("hud", hud)
        tt.add("music", music / 2)
        tt.add("music", music / 2)                     # one step called twice in a tick: summed
        tt.end(total)
    assert len(tt.ticks) == 3                          # the oldest went
    assert tt.ticks[0] == {"hud": 6.0, "music": 20.0, "total": 40.0, "map": 14.0}
    line = tt.line()
    assert "gesamt 20.7/40" in line and "≥ 30 ms: 1×" in line and "Systemwerte 3.0/6" in line
    assert "Karte 9.3/14" in line and "Musik 8.3/20" in line and "Infos" not in line   # steps that never ran: left out
    tt.add("hud", 99)                                  # outside a tick: not counted
    assert len(tt.ticks) == 3 and TickTimes().line() == "Overlay-Takt: noch keine Messung"


def test_a_wrapped_step_counts_its_time_and_keeps_its_result():
    tt = TickTimes()
    tt.start()
    f = tt.timed("info", lambda x: x * 2)
    assert f(21) == 42 and f.__wrapped__(1) == 2
    tt.end(5.0)
    assert set(tt.ticks[0]) == {"info", "total", "map"} and tt.ticks[0]["info"] >= 0


def test_the_workers_looks_are_timed_per_step_with_counts_and_without_the_sleep():
    """1.38.22 (project review PERF-2): nothing measured what a look of the detection cost. LookTimes: a tick's
    total is the steps' sum (the sleep between looks says nothing), sparse steps (lobby once a second, banner strip
    five times) are averaged over the ticks they ran in, with their count."""
    from fogscout.ticktime import CpuShare, LookTimes
    lt = LookTimes(kept=10)
    for i in range(4):
        lt.start()
        lt.add("grab", 10.0)
        if i % 2 == 0:
            with lt.measure("lobby"):
                pass
            lt.add("lobby", 100.0)
        lt.end()                                           # no total: the steps' sum
    assert lt.ticks[-1]["total"] == 10.0 and lt.ticks[-2]["total"] >= 110.0 and lt.ticks[-1]["map"] == 0.0
    line = lt.line()
    assert line.startswith("Erkennungs-Takt (4 Takte") and "Aufnahme 10.0/10 (4×)" in line
    assert "Lobby-OCR 100.0/100 (2×)" in line and "Banner-OCR" not in line
    assert LookTimes().line() == "Erkennungs-Takt: noch keine Messung"
    cpu = CpuShare(kept=5)
    assert cpu.percent() is None and "noch keine" in cpu.line()
    for wall, used in ((0.0, 0.0), (1.0, 0.25), (2.0, 0.50), (3.0, 1.0)):
        cpu.note(wall, used)
    assert cpu.percent(60) == 100.0 * 1.0 / 3.0 and cpu.percent(1.5) == 50.0       # the last window only
    assert "letzte Minute 33.3 %" in cpu.line("Erkennung")
