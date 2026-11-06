"""Streaks and records (1.7, user's pick 6): longest and current 4K streak, longest and current escape streak,
best week as killer / survivor, most rounds in a day, longest session, longest round; 1.8.46 the fastest 4K.

Pure logic on the rounds the statistics selected and their official matches; the sub-tab "Rekorde" shows the
result as tiles (dashboard.Tile).
"""
from __future__ import annotations

import datetime
import time
from dataclasses import dataclass

from . import official
from .dashboard import Tile, play_time, rounds_target
from .i18n import _
from .textnorm import fmt_duration

WEEK_MIN = 5              # a week needs this many rounds with a result to be "the best week"
SESSION_GAP = 45 * 60     # rounds further apart than this (end -> next start) are two sessions


@dataclass
class Streak:
    best: int = 0
    best_end: float = 0.0     # start of the last round of the best streak
    current: int = 0          # the run the newest rounds are on
    rounds: int = 0           # rounds with a known result


def streak(items) -> Streak:
    """``items``: [(start, hit)] in any order; ``hit`` None = result unknown, neither extends nor breaks a run."""
    s = Streak()
    run = 0
    for t, hit in sorted((i for i in items if i[1] is not None), key=lambda i: i[0]):
        s.rounds += 1
        run = run + 1 if hit else 0
        if run > s.best:
            s.best, s.best_end = run, t
    s.current = run
    return s


def streak_rounds(items) -> list:
    """1.38.54: the start times of the best streak of ``items`` ([(start, hit)], as ``streak``: unknown results
    skipped) – the first of equally long ones, as ``streak`` counts it; [] without a hit."""
    best, run = [], []
    for t, hit in sorted((i for i in items if i[1] is not None), key=lambda i: i[0]):
        run = run + [t] if hit else []
        if len(run) > len(best):
            best = list(run)
    return best


def _day(t: float) -> float:
    return datetime.datetime.fromtimestamp(t).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()


def week_start(t: float) -> float:
    """Midnight of the Monday of the week ``t`` lies in (local time)."""
    d = datetime.datetime.fromtimestamp(t).replace(hour=0, minute=0, second=0, microsecond=0)
    return (d - datetime.timedelta(days=d.weekday())).timestamp()


def best_week(items, minimum=WEEK_MIN):
    """``items``: [(start, value)] -> (week start, mean, n) of the week with the highest mean among the weeks with
    at least ``minimum`` values; None without such a week. Ties go to the newer week."""
    weeks = {}
    for t, v in items:
        if v is not None:
            weeks.setdefault(week_start(t), []).append(float(v))
    best = None
    for start, vals in weeks.items():
        if len(vals) < minimum:
            continue
        mean = sum(vals) / len(vals)
        if best is None or mean > best[1] or (mean == best[1] and start > best[0]):
            best = (start, mean, len(vals))
    return best


def busiest_day(rounds):
    """(day start, rounds, play seconds) of the day with the most rounds; None without rounds."""
    days = {}
    for r in rounds:
        d = days.setdefault(_day(r.t), [0, 0.0])
        d[0] += 1
        d[1] += r.seconds
    if not days:
        return None
    start = max(days, key=lambda k: (days[k][0], k))
    return start, days[start][0], days[start][1]


def sessions(rounds, gap=SESSION_GAP) -> list:
    """[(first start, last end, rounds)]: rounds that follow each other within ``gap`` form a session."""
    out = []
    for r in sorted(rounds, key=lambda r: r.t):
        end = r.t + r.seconds
        if out and r.t - out[-1][1] <= gap:
            out[-1] = (out[-1][0], max(out[-1][1], end), out[-1][2] + 1)
        else:
            out.append((r.t, end, 1))
    return out


@dataclass
class Session:
    """1.38.47: one session of the sub-tab "Sitzungen" – its rounds and their sums (official numbers from the
    rounds tied to a match; None without any)."""
    start: float
    end: float
    rounds: list
    play_s: float = 0.0
    killer: int = 0
    survivor: int = 0
    farming: int = 0
    kills: float | None = None
    killer_matches: int = 0
    escaped: float | None = None
    survivor_matches: int = 0
    bp: int = 0
    bp_matches: int = 0
    wait: float | None = None


def session_rows(rounds, off: dict, gap=SESSION_GAP) -> list:
    """1.38.47 (user's pick from the feature report: "Sitzungen als eigener Reiter"): the sessions of ``rounds``,
    newest first – the same split as ``sessions`` (a gap of more than ``gap`` from one round's end to the next
    one's start), each with its rounds, play time, roles, farming rounds, Ø waiting time and, from the official
    matches (``off``: id(round) -> Match), Ø kills, share escaped and bloodpoints."""
    groups = []
    for r in sorted(rounds, key=lambda r: r.t):
        end = r.t + r.seconds
        if groups and r.t - groups[-1][1] <= gap:
            groups[-1][1] = max(groups[-1][1], end)
            groups[-1][2].append(r)
        else:
            groups.append([r.t, end, [r]])
    out = []
    for start, end, rs in groups:
        s = official.summary([off[id(r)] for r in rs if id(r) in off])
        waits = [r.wait for r in rs if r.wait is not None]
        out.append(Session(start=start, end=end, rounds=rs, play_s=sum(r.seconds for r in rs),
                           killer=sum(1 for r in rs if r.role == "killer" and not r.custom),
                           survivor=sum(1 for r in rs if r.role == "survivor" and not r.custom),
                           farming=sum(1 for r in rs if r.farming and not r.custom),
                           kills=s["kills"] if s["killer"] else None, killer_matches=s["killer"],
                           escaped=s["escaped"] if s["survivor"] else None, survivor_matches=s["survivor"],
                           bp=s["bp"], bp_matches=s["bp_matches"],
                           wait=sum(waits) / len(waits) if waits else None))
    out.reverse()
    return out


def session_tiles(rows) -> list:
    """1.38.47: the tiles above the sessions table – how many, Ø rounds and length per session, the longest."""
    if not rows:
        return []
    n = len(rows)
    longest = max(rows, key=lambda s: (s.end - s.start, s.start))
    return [Tile(_("Sitzungen"), str(n), _("{n} Runden", n=sum(len(s.rounds) for s in rows))),
            Tile(_("Ø Runden je Sitzung"), f"{sum(len(s.rounds) for s in rows) / n:.1f}"),
            Tile(_("Ø Dauer einer Sitzung"), play_time(sum(s.end - s.start for s in rows) / n)),
            Tile(_("Längste Sitzung"), play_time(longest.end - longest.start),
                 _date(longest.start) + " · " + _("{n} Runden", n=len(longest.rounds)),
                 open=rounds_target([r.t for r in longest.rounds]))]


def longest_session(rounds, gap=SESSION_GAP):
    """The session that lasted longest (first banner to last end): (start, end, rounds) or None."""
    ss = sessions(rounds, gap)
    return max(ss, key=lambda s: (s[1] - s[0], s[0])) if ss else None


def longest_round(rounds):
    return max(rounds, key=lambda r: (r.seconds, r.t)) if rounds else None


def fastest_four(pairs):
    """1.8.46: the 4K with the shortest match – (round, match, seconds) or None. The page's time in the match
    (exact) when it has one, else the detected length."""
    best = None
    for r, m in pairs:
        if official.kills(m) != 4:
            continue
        seconds = m.seconds or r.seconds
        if seconds > 0 and (best is None or seconds < best[2]):
            best = (r, m, seconds)
    return best


def _date(t: float) -> str:
    return time.strftime("%d.%m.%y", time.localtime(t))


def _streak_tile(title: str, s: Streak, empty: str, items=()) -> Tile:
    if not s.rounds:
        return Tile(title, sub=empty)
    sub = _("aktuell {n}", n=s.current)
    if s.best:
        sub += " · " + _("zuletzt {date}", date=_date(s.best_end))
    sub += " · " + _("{n} Runden", n=s.rounds)
    return Tile(title, str(s.best), sub, open=rounds_target(streak_rounds(items)))   # 1.38.54: its rounds


def tiles(rounds, pairs, killer_name=None) -> list:
    """The tiles of the sub-tab "Rekorde" for the selected ``rounds`` and their official ``pairs``;
    ``killer_name`` turns a killer id into its display name."""
    kills = [(r.t, official.kills(m)) for r, m in pairs]
    esc = [(r.t, official.escaped(m)) for r, m in pairs]
    # 1.38.54 (user: "mach das auch für die anderen Kacheln, wo es Sinn macht"): every record that comes from rounds
    # marks them under „Letzte Runden“ on a click (dashboard.rounds_target)
    four = [(t, None if k is None else k == 4) for t, k in kills]
    out = [_streak_tile(_("4K-Serie"), streak(four), _("keine Killer-Runden mit Stats-Daten"), four),
           _streak_tile(_("Entkommen-Serie"), streak(esc), _("keine Survivor-Runden mit Stats-Daten"), esc)]

    def week_rounds(items, start):
        return rounds_target([t for t, v in items if v is not None and week_start(t) == start])
    bw = best_week(kills)
    out.append(Tile(_("Beste Woche als Killer"), _("Ø {kills} Kills", kills=f"{bw[1]:.2f}"),
                    _("ab {date} · {n} Runden", date=_date(bw[0]), n=bw[2]), frac=bw[1] / 4,
                    open=week_rounds(kills, bw[0])) if bw
               else Tile(_("Beste Woche als Killer"), sub=_("ab {n} Killer-Runden in einer Woche", n=WEEK_MIN)))
    bw = best_week([(t, None if e is None else int(e)) for t, e in esc])
    out.append(Tile(_("Beste Woche als Survivor"), _("{share} entkommen", share=f"{bw[1]:.0%}"),
                    _("ab {date} · {n} Runden", date=_date(bw[0]), n=bw[2]), frac=bw[1],
                    open=week_rounds(esc, bw[0])) if bw
               else Tile(_("Beste Woche als Survivor"), sub=_("ab {n} Survivor-Runden in einer Woche", n=WEEK_MIN)))
    day = busiest_day(rounds)
    if day:
        out.append(Tile(_("Meiste Runden an einem Tag"), str(day[1]),
                        _date(day[0]) + " · " + _("{time} gespielt", time=play_time(day[2])),
                        open=rounds_target([r.t for r in rounds if _day(r.t) == day[0]])))
    ses = longest_session(rounds)
    if ses:
        out.append(Tile(_("Längste Sitzung"), play_time(ses[1] - ses[0]),
                        _date(ses[0]) + " · " + _("{n} Runden", n=ses[2]),
                        open=rounds_target([r.t for r in rounds if ses[0] <= r.t <= ses[1]])))
    r = longest_round(rounds)
    if r is not None:
        out.append(Tile(_("Längste Runde"), fmt_duration(r.seconds), f"{r.map} · {_date(r.t)}",
                        open=rounds_target([r.t])))
    fast = fastest_four(pairs)
    if fast is not None:
        r, _m, seconds = fast
        who = (killer_name or str)(r.killer) if r.killer else ""
        out.append(Tile(_("Schnellste 4K"), fmt_duration(seconds),
                        " · ".join(x for x in (who, r.map, _date(r.t)) if x), open=rounds_target([r.t])))
    return out


# ---------------------------------------------------------------- 1.38.28 (project review F2): the overlay's record line
def record_groups(pairs, key) -> dict:
    """{key(round): [(start, kills, escaped)]} of rounds tied to an official match (pairs: [(round, match)]) –
    the raw material of ``record_line``: averages and, in time order, streaks."""
    out = {}
    for r, m in pairs:
        out.setdefault(key(r), []).append((r.t, official.kills(m), official.escaped(m)))
    return out


def record_line(by_map: dict, by_pair: dict, map_id: str, role: str, killer: str, killer_name=None,
                min_rounds: int = 3) -> str:
    """The line under the timer for the map on display. With a killer known for this round (own as killer, the
    lobby's as survivor) and at least ``min_rounds`` results on this map with that killer: "Ø 3.2 Kills · 5 Runden
    als Nurse" / "40 % entkommen · 5 Runden gegen Nurse"; else the map alone as before (1.8.x). A current streak of
    two or more in the group shown is appended ("4K-Serie 3", "Entkommen-Serie 2"). "" below ``min_rounds``."""
    name = (killer_name or (lambda k: k))(killer) if killer else ""
    whole = by_map.get(map_id) or []
    pair = (by_pair.get((map_id, killer)) or []) if killer else []
    if role not in ("killer", "survivor"):
        ks = [k for _t, k, _e in whole if k is not None]
        es = [e for _t, _k, e in whole if e is not None]
        role = "killer" if len(ks) >= len(es) else "survivor"
    for group, with_killer in ((pair, True), (whole, False)):
        if role == "killer":
            ks = [(t, k) for t, k, _e in group if k is not None]
            if len(ks) >= min_rounds:
                avg = f"{sum(k for _t, k in ks) / len(ks):.1f}"
                text = (_("Ø {kills} Kills · {n} Runden als {killer}", kills=avg, n=len(ks), killer=name) if with_killer
                        else _("Ø {kills} Kills · {n} Runden", kills=avg, n=len(ks)))
                run = streak([(t, k == 4) for t, k in ks]).current
                return text + (" · " + _("4K-Serie {n}", n=run) if run >= 2 else "")
        else:
            es = [(t, e) for t, _k, e in group if e is not None]
            if len(es) >= min_rounds:
                share = f"{sum(1 for _t, e in es if e) / len(es):.0%}"
                text = (_("{share} entkommen · {n} Runden gegen {killer}", share=share, n=len(es), killer=name)
                        if with_killer else _("{share} entkommen · {n} Runden", share=share, n=len(es)))
                run = streak(es).current
                return text + (" · " + _("Entkommen-Serie {n}", n=run) if run >= 2 else "")
    return ""
