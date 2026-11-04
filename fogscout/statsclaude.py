"""1.35 (user's release of 3.11.2026: "zusammengefasste Rundenwerte (keine Namen, keine Rohdaten) für
Statistik-Fragen"): what a statistics question sends to Claude and how the answer is read. Pure, no Qt, no network.

``summary`` folds the joined rounds (App._joined: own rounds + official matches) into counts and rates per group –
role, own killer, map, opposing killer, server region, time of day, weekday. Never a single round, never a time
stamp finer than the day of the first and last round, never a player name (the official file holds none; only the
character a player played is used, as a group), never a path, server address, file name or song title. Groups with
fewer than ``MIN_GROUP`` rounds are left out, at most ``MAX_GROUPS`` per kind (the most played).

Claude answers with one text (SCHEMA); the App shows it as plain text only (qt_common.PlainLabel), nothing runs."""
from __future__ import annotations

import json
import statistics
import time

from . import official

MAX_QUESTION = 300               # characters of the question sent at most
MAX_ANSWER = 1200                # characters of the answer shown at most
MAX_GROUPS = 25                  # groups per kind at most (the most played)
MIN_GROUP = 2                    # a group with fewer rounds is left out (one round would be raw data)
MAX_TOKENS = 2048
HOURS = (("night", 0, 6), ("morning", 6, 12), ("afternoon", 12, 18), ("evening", 18, 24))
WEEKDAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")

SYSTEM = ("You answer questions about a player's own Dead by Daylight statistics for Fog Scout, a desktop "
          "companion app. You get a JSON summary of the player's rounds: only counts, averages and rates per group "
          "(role, own killer, map, opposing killer, server region, time of day, weekday). 'kills' is the average "
          "number of survivors killed per killer match (0–4), 'escape' the share of survivor matches escaped, "
          "'n' the number of rounds, 'n_official' how many of them have official match data (kills, escapes and "
          "bloodpoints only exist for those). Answer in the language of the question in at most five short "
          "sentences, with the numbers that support the answer. Base everything on the summary; if it does not "
          "contain what the question needs, say so plainly. Do not invent rounds, players or numbers.")

SCHEMA = {"type": "object", "additionalProperties": False, "required": ["answer"],
          "properties": {"answer": {"type": "string"}}}


def _r(v, digits=2):
    return None if v is None else round(float(v), digits)


class _Group:
    __slots__ = ("n", "seconds", "kills", "escapes", "bp", "wait", "ping", "official")

    def __init__(self):
        self.n = 0
        self.seconds, self.kills, self.escapes, self.bp, self.wait, self.ping = [], [], [], [], [], []
        self.official = 0

    def add(self, r, m):
        self.n += 1
        if r.seconds:
            self.seconds.append(float(r.seconds))
        if r.wait is not None:
            self.wait.append(float(r.wait))
        if r.ping is not None:
            self.ping.append(float(r.ping))
        if m is None:
            return
        self.official += 1
        k = official.kills(m)
        if k is not None:
            self.kills.append(k)
        e = official.escaped(m)
        if e is not None:
            self.escapes.append(1.0 if e else 0.0)
        if m.bp:
            self.bp.append(float(m.bp))

    def out(self) -> dict:
        d = {"n": self.n}
        if self.official:
            d["n_official"] = self.official
        if self.seconds:
            d["minutes"] = _r(statistics.fmean(self.seconds) / 60, 1)
        if self.kills:
            d["kills"] = _r(statistics.fmean(self.kills))
            d["four_k"] = _r(sum(1 for k in self.kills if k >= 4) / len(self.kills))
        if self.escapes:
            d["escape"] = _r(statistics.fmean(self.escapes))
        if self.bp:
            d["bp"] = int(statistics.fmean(self.bp))
        if self.wait:
            d["queue_s"] = int(statistics.median(self.wait))
        if self.ping:
            d["ping_ms"] = int(statistics.median(self.ping))
        return d


def _table(groups: dict) -> dict:
    kept = [(k, g) for k, g in groups.items() if k and g.n >= MIN_GROUP]
    kept.sort(key=lambda kg: (-kg[1].n, kg[0]))
    return {str(k): g.out() for k, g in kept[:MAX_GROUPS]}


def _opposing_killer(m):
    """The killer a survivor match was against (the character only – never a name)."""
    if m is None or m.role != "survivor":
        return ""
    return next((p.character for p in m.opp if p.role == "killer" and p.character), "")


def summary(rounds, off: dict, include_farming: bool = True) -> dict:
    """The summary Claude sees. ``rounds``: history.Round (App._joined().rounds), ``off``: id(round) -> its
    official.Match. Custom games never count; farming rounds only with ``include_farming``."""
    used = [r for r in rounds if not r.custom and (include_farming or not r.farming)]
    out = {"rounds": len(used)}
    if not used:
        return out
    days = sorted(time.strftime("%Y-%m-%d", time.localtime(r.t)) for r in used)
    out["first_day"], out["last_day"] = days[0], days[-1]
    out["farming_rounds"] = sum(1 for r in used if r.farming)
    kinds = {"by_role": {}, "killer_by_own_killer": {}, "killer_by_map": {}, "survivor_by_map": {},
             "survivor_by_opposing_killer": {}, "by_region": {}, "by_time_of_day": {}, "by_weekday": {}}
    total = _Group()
    for r in used:
        m = off.get(id(r))
        role = r.role or (m.role if m is not None else "")
        lt = time.localtime(r.t)
        keys = {"by_role": role or "unknown",
                "by_region": r.region,
                "by_time_of_day": next(name for name, a, b in HOURS if a <= lt.tm_hour < b),
                "by_weekday": WEEKDAYS[lt.tm_wday]}
        if role == "killer":
            keys["killer_by_own_killer"] = r.killer or (m.character if m is not None else "")
            keys["killer_by_map"] = r.map
        elif role == "survivor":
            keys["survivor_by_map"] = r.map
            keys["survivor_by_opposing_killer"] = _opposing_killer(m)
        total.add(r, m)
        for kind, key in keys.items():
            if key:
                kinds[kind].setdefault(key, _Group()).add(r, m)
    out["all"] = total.out()
    for kind, groups in kinds.items():
        table = _table(groups)
        if table:
            out[kind] = table
    return out


def content(question: str, data: dict) -> str:
    return ("Statistics summary:\n" + json.dumps(data, ensure_ascii=False, sort_keys=True)
            + "\n\nQuestion: " + str(question or "").strip()[:MAX_QUESTION])


def answer(data: dict) -> str:
    """The answer's text, whitespace folded, at most MAX_ANSWER characters ("" = nothing usable)."""
    return " ".join(str(data.get("answer") or "").split())[:MAX_ANSWER]


def private_words(data: dict) -> set:
    """For the tests: every string value the summary holds (keys and values) – checked against names and paths."""
    found = set()

    def walk(v):
        if isinstance(v, dict):
            for k, x in v.items():
                found.add(str(k))
                walk(x)
        elif isinstance(v, (list, tuple)):
            for x in v:
                walk(x)
        elif isinstance(v, str):
            found.add(v)
    walk(data)
    return found

