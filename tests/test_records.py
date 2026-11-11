"""Streaks and records (fogscout/records.py, 1.7) – pure logic."""
import datetime
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fogscout import records  # noqa: E402
from fogscout.history import Round  # noqa: E402
from fogscout.official import Match, Player  # noqa: E402


def _t(day, hour=20, minute=0):
    return datetime.datetime(2026, 3, day, hour, minute).timestamp()


def _killer_match(t, kills):
    stats = ["SACRIFICED"] * kills + ["ESCAPED"] * (4 - kills)
    return Match(t=t - 38, map="Coal Tower", role="killer", seconds=600,
                 opp=[Player(role="survivor", status=s) for s in stats])


def _survivor_match(t, escaped):
    return Match(t=t - 38, map="Coal Tower", role="survivor", seconds=600,
                 status="ESCAPED" if escaped else "SACRIFICED")


def test_streaks_run_in_time_order_and_unknown_results_are_skipped():
    s = records.streak([(3, True), (1, True), (2, True), (4, False), (5, True), (6, None), (7, True)])
    assert (s.best, s.best_end, s.current, s.rounds) == (3, 3, 2, 6)
    assert records.streak([]) == records.Streak()
    assert records.streak([(1, False)]).current == 0


def test_the_best_week_needs_enough_rounds_and_ties_go_to_the_newer_week():
    week1 = [(_t(2) + i, 4) for i in range(5)]                 # Mon 2.3.: five 4Ks
    week2 = [(_t(9) + i, 4) for i in range(5)]                 # Mon 9.3.: five 4Ks too -> newer wins
    week3 = [(_t(16) + i, 4) for i in range(3)]                # too few rounds, even if perfect
    week4 = [(_t(23) + i, 1) for i in range(6)]
    start, mean, n = records.best_week(week1 + week2 + week3 + week4)
    assert (start, mean, n) == (records.week_start(_t(9)), 4.0, 5)
    assert records.best_week(week3) is None and records.best_week([]) is None
    assert records.week_start(_t(4)) == _t(2, 0)               # Wednesday -> Monday midnight


def test_busiest_day_sessions_and_longest_round():
    rs = [Round(t=_t(1, 20), seconds=600, map_id="a", map="A"),
          Round(t=_t(1, 20, 15), seconds=900, map_id="a", map="A"),          # 5 min after the first ended
          Round(t=_t(1, 21, 30), seconds=300, map_id="b", map="B"),          # 60 min gap: a second session
          Round(t=_t(2, 20), seconds=1200, map_id="c", map="C II")]
    assert records.busiest_day(rs) == (_t(1, 0), 3, 1800)
    ses = records.sessions(rs)
    assert [(s[2], round((s[1] - s[0]) / 60)) for s in ses] == [(2, 30), (1, 5), (1, 20)]
    assert records.longest_session(rs) == ses[0]
    assert records.longest_round(rs).map == "C II"
    assert records.busiest_day([]) is None and records.longest_session([]) is None


def test_the_tiles_of_the_records_tab(monkeypatch):
    monkeypatch.setattr(time, "localtime", lambda t=None: time.gmtime(t))
    rs = [Round(t=_t(2, 10) + i * 1800, seconds=600, map_id="a", map="Coal Tower", role="killer") for i in range(6)]
    rs += [Round(t=_t(3, 10) + i * 3600, seconds=700, map_id="a", map="Coal Tower", role="survivor") for i in range(3)]
    ms = [_killer_match(r.t, k) for r, k in zip(rs[:6], (4, 4, 4, 2, 4, 4))]
    ms += [_survivor_match(r.t, e) for r, e in zip(rs[6:], (True, False, True))]
    tiles = {t.title: t for t in records.tiles(rs, list(zip(rs, ms)))}
    assert tiles["4K-Serie"].value == "3" and tiles["4K-Serie"].sub.startswith("aktuell 2 ·")
    assert tiles["Entkommen-Serie"].value == "1" and "3 Runden" in tiles["Entkommen-Serie"].sub
    assert tiles["Beste Woche als Killer"].value == "Ø 3.67 Kills" and "6 Runden" in tiles["Beste Woche als Killer"].sub
    assert tiles["Beste Woche als Survivor"].value == "–"           # three survivor rounds: fewer than WEEK_MIN
    assert tiles["Meiste Runden an einem Tag"].value == "6"
    assert tiles["Längste Sitzung"].sub.endswith("6 Runden")
    assert tiles["Längste Runde"].value == "11:40" and tiles["Längste Runde"].sub.startswith("Kohlelager")      # 1.50: in the UI language
    empty = {t.title: t for t in records.tiles([], [])}
    assert set(empty) == {"4K-Serie", "Entkommen-Serie", "Beste Woche als Killer", "Beste Woche als Survivor"}
    assert empty["4K-Serie"].value == "–"


def test_fastest_4k_takes_the_pages_time_and_names_the_killer(monkeypatch):
    """1.8.46: the record "Schnellste 4K" – the page's time in the match when it has one."""
    monkeypatch.setattr(time, "localtime", lambda t=None: time.gmtime(t))
    rs = [Round(t=_t(4, 20) + i * 1800, seconds=900, map_id="a", map=m, role="killer", killer=k)
          for i, (m, k) in enumerate((("Coal Tower", "nurse"), ("Badham", "huntress"), ("Ormond", "nurse")))]
    ms = [_killer_match(r.t, k) for r, k in zip(rs, (4, 4, 3))]
    ms[0].seconds, ms[1].seconds, ms[2].seconds = 0, 420, 300        # page time missing on the first: detected 15:00
    r, _m, seconds = records.fastest_four(list(zip(rs, ms)))
    assert (r.map, seconds) == ("Badham", 420)                      # the 3K is quicker but no 4K
    tiles = {t.title: t for t in records.tiles(rs, list(zip(rs, ms)), lambda k: k.title())}
    assert tiles["Schnellste 4K"].value == "07:00" and tiles["Schnellste 4K"].sub.startswith("Huntress · Badham ·")
    assert records.fastest_four([]) is None


def test_the_overlay_record_line_prefers_this_map_with_this_killer_and_names_a_streak():
    """1.38.28 (project review F2): the line under the timer counted the map over all killers; now map × killer
    first (own killer, or the lobby's as survivor) when it has enough results, the map alone otherwise; a current
    streak of two or more is named. Below the minimum: nothing."""
    t0 = _t(2, 10)
    rs = [Round(t=t0 + i * 1800, seconds=600, map_id="a", map="Coal Tower", role="killer",
                killer="nurse" if i % 2 == 0 else "wraith") for i in range(8)]
    ms = [_killer_match(r.t, k) for r, k in zip(rs, (4, 1, 4, 2, 4, 2, 4, 3))]       # nurse: 4,4,4,4 · wraith: 1,2,2,3
    pairs = list(zip(rs, ms))
    by_map = records.record_groups(pairs, lambda r: r.map_id)
    by_pair = records.record_groups(pairs, lambda r: (r.map_id, r.killer))
    name = lambda k: k.title()                                                   # noqa: E731
    assert records.record_line(by_map, by_pair, "a", "killer", "nurse", name) == "Ø 4.0 Kills · 4 Runden als Nurse · 4K-Serie 4"
    assert records.record_line(by_map, by_pair, "a", "killer", "wraith", name) == "Ø 2.0 Kills · 4 Runden als Wraith"
    assert records.record_line(by_map, by_pair, "a", "killer", "", name) == "Ø 3.0 Kills · 8 Runden"       # no killer known
    assert records.record_line(by_map, by_pair, "a", "killer", "hag", name) == "Ø 3.0 Kills · 8 Runden"    # none with her: the map
    assert records.record_line(by_map, by_pair, "a", "", "nurse", name).startswith("Ø 4.0 Kills")          # role from the map
    assert records.record_line(by_map, by_pair, "b", "killer", "nurse", name) == ""                        # never played there
    # survivor: escapes against this killer, the escape streak; fewer than min_rounds → the map
    sv = [Round(t=t0 + 90000 + i * 1800, seconds=600, map_id="a", map="Coal Tower", role="survivor", killer="nurse")
          for i in range(3)]
    sm = [_survivor_match(r.t, e) for r, e in zip(sv, (False, True, True))]
    by_map = records.record_groups(list(zip(sv, sm)), lambda r: r.map_id)
    by_pair = records.record_groups(list(zip(sv, sm)), lambda r: (r.map_id, r.killer))
    assert records.record_line(by_map, by_pair, "a", "survivor", "nurse", name) == "67% entkommen · 3 Runden gegen Nurse · Entkommen-Serie 2"
    assert records.record_line(by_map, by_pair, "a", "survivor", "nurse", name, min_rounds=4) == ""



def test_sessions_split_after_the_gap_and_sum_their_rounds():
    """1.38.47 (user's pick "Sitzungen als eigener Reiter"): records.session_rows – the same split as sessions()
    (more than SESSION_GAP from one round's end to the next start), newest first, with play time, roles, farming,
    Ø wait and – only from rounds tied to an official match – Ø kills, share escaped and bloodpoints."""
    h = 3600
    r1 = Round(_t(3), 600, "coal", "Coal Tower", role="killer", wait=60)
    r2 = Round(r1.t + 600 + records.SESSION_GAP, 600, "coal", "Coal Tower", role="survivor", wait=120)
    r3 = Round(r2.t + 3 * h, 900, "game", "The Game", role="killer", farming=True)
    r4 = Round(r3.t + 1200, 300, "game", "The Game", custom=True)
    m1, m2 = _killer_match(r1.t, 3), _survivor_match(r2.t, True)
    m1.bp, m2.bp = 20000, 15000
    rows = records.session_rows([r3, r1, r4, r2], {id(r1): m1, id(r2): m2})
    assert [len(s.rounds) for s in rows] == [2, 2]                        # newest first; the gap itself still joins
    new, old = rows
    assert new.start == r3.t and new.end == r4.t + 300 and new.play_s == 1200
    assert (new.killer, new.survivor, new.farming) == (1, 0, 1)           # the custom game counts no role
    assert new.kills is None and new.escaped is None and new.wait is None and new.bp_matches == 0
    assert old.start == r1.t and (old.killer, old.survivor) == (1, 1) and old.wait == 90
    assert old.kills == 3 and old.killer_matches == 1 and old.escaped == 1.0 and old.survivor_matches == 1
    assert old.bp == 35000 and old.bp_matches == 2
    split = records.session_rows([r1, Round(r1.t + 600 + records.SESSION_GAP + 1, 60, "coal", "Coal Tower")], {})
    assert len(split) == 2                                                # one second more: two sessions
    assert records.session_rows([], {}) == [] and records.session_tiles([]) == []
    tiles = records.session_tiles(rows)
    assert [t.title for t in tiles][:3] == ["Sitzungen", "Ø Runden je Sitzung", "Ø Dauer einer Sitzung"]
    assert tiles[0].value == "2" and tiles[1].value == "2.0"


def test_record_tiles_open_the_rounds_they_come_from():
    """1.38.54 (user: "mach das auch für die anderen Kacheln, wo es Sinn macht"): every record that comes from rounds
    carries their start times as its click target; streak_rounds = the first longest run, unknown results skipped."""
    assert records.streak_rounds([(5, True), (1, True), (2, None), (3, True), (4, False), (6, True)]) == [1, 3]
    assert records.streak_rounds([(1, False), (2, None)]) == []
    rs = [Round(_t(3, 20), 600, "coal", "Coal Tower", role="killer"),
          Round(_t(3, 20, 15), 900, "coal", "Coal Tower", role="killer"),
          Round(_t(4, 20), 1500, "game", "The Game", role="killer")]
    pairs = [(r, _killer_match(r.t, 4)) for r in rs]
    got = {t.title: t.open for t in records.tiles(rs, pairs)}
    ts = lambda *rounds: "rounds:" + ",".join(repr(float(r.t)) for r in rounds)   # noqa: E731
    assert got["4K-Serie"] == ts(*rs)
    assert got["Meiste Runden an einem Tag"] == ts(rs[0], rs[1])
    assert got["Längste Sitzung"] == ts(rs[0], rs[1])
    assert got["Längste Runde"] == ts(rs[2]) and got["Schnellste 4K"] == ts(rs[0])
    assert got["Entkommen-Serie"] == "" and got["Beste Woche als Survivor"] == ""   # no survivor rounds: no target
    from fogscout import dashboard
    dash = {t.title: t.open for t in dashboard.tiles(rs, pairs)}
    assert dash["Runden"] == "tab:last" and dash["Ø Kills"] == "tab:last:killer"
