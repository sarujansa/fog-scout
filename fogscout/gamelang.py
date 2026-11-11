"""1.48 (user: "Dein Vorschlag gefällt mir" – the game language found by itself): a banner read cleanly that names a
map only in a game language not ticked (DBD in French, "TERRAIN DE LA CASSE" with only EN/DE on) is compared
with the names of every language in the catalogue; when it is one map in one other language, that language is
ticked for the user (worker → event "game_language" → App._game_language). Pure: text in, (code, map id) out.

Only at the start of a round (never mid-match, where signs in the game world are read too), only text that is
close to the name *and* the realm of that map in that language, never when the ticked languages read about as
well, and only after ``VOTES`` looks agree.
"""
from __future__ import annotations

import re

from .textnorm import fold_any as fold

# app.LANGS – first wins on a tie (es/es-MX, zh-Hans/zh-Hant)
ORDER = ("en", "de", "fr", "es", "es-MX", "it", "pl", "pt-BR", "tr", "ru", "zh-Hans", "zh-Hant", "ja", "ko")
LONG_NAME = 12       # 1.49: letters of another script from which a name needs no realm to count
PROBE_LOOKS = 3      # 1.49: looks of one banner the models of the scripts not in use are asked for (worker)
MIN_CHARS = 4        # a shorter read says too little ("GRA"); short names count only with their realm anyway
MAX_NAME = 0.15      # at most this share of the name's letters wrong (edit distance / length)
MAX_REALM = 0.25     # the realm line: compared over the realm name's length (the line often carries noise after it)
MARGIN = 0.15        # the ticked languages must read at least this much worse
VOTES = 2            # looks that must name the same map in the same language


def distance(a: str, b: str) -> float:
    """Edit distance of two folded texts as a share of the longer one (0 = equal, 1 = nothing alike)."""
    if not a or not b:
        return 1.0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1] / max(len(a), len(b))


def _realm_fits(realm_text: str, realm: str) -> bool:
    want = fold(realm)
    return bool(want) and distance(fold(realm_text)[:len(want)], want) <= MAX_REALM


def match(name_text: str, realm_text: str, maps, active) -> tuple | None:
    """(code, map id) of one look, or None. ``maps``: catalog entries (``id``, ``names``, ``realm_names``)."""
    name = fold(name_text)
    # a sign of Chinese, Japanese or Korean says as much as two letters ("血屋" is a whole name)
    if sum((2 if ord(c) >= 0x2E80 else 1) for c in name) < MIN_CHARS:
        return None
    bare = re.sub(r"[IVX]{1,4}$", "", name)          # the layout number at the end ("BADHAM ANAOKULU III")
    best_active, found = 1.0, []
    for m in maps:
        for code, text in (m.names or {}).items():
            other = fold(text)
            floor = min(abs(len(other) - len(n)) / max(len(other), len(n), 1) for n in (name, bare))   # d ≥ floor
            if floor >= (best_active if code in active else MAX_NAME + 1e-9):
                continue
            d = min(distance(name, other), distance(bare, other) if bare != name else 1.0)
            if code in active:
                best_active = min(best_active, d)
            elif d <= MAX_NAME:
                realm = (m.realm_names or {}).get(code) or (m.realm_names or {}).get("en") or ""
                # 1.49: a long name in another script speaks for itself – the realm below it may be read in Latin
                # look-alikes ("RAKKUN-SITI" for "РАККУН-СИТИ" under a name of 42 Cyrillic letters read right)
                if sum(ord(c) >= 0x250 for c in other) >= LONG_NAME or _realm_fits(realm_text, realm):
                    found.append((d, ORDER.index(code) if code in ORDER else len(ORDER), code, m.id))
    if not found:
        return None
    found.sort()
    d, _rank, code, map_id = found[0]
    if best_active - d < MARGIN:
        return None
    # the language is what counts: two maps of the same language (RPD east/west) or one name in two languages (es and
    # es-MX) are fine – only another map in another language that reads about as well leaves it open
    if any(f[2] != code and f[3] != map_id and f[0] - d < MARGIN for f in found[1:]):
        return None
    return code, map_id


def vote(votes: dict, name_text: str, realm_text: str, maps, active) -> tuple | None:
    """Count one look into ``votes`` (one dict per banner); (code, map id) once ``VOTES`` looks name the same map in
    the same unticked language, else None. One look at a time: the worker calls it for each new read."""
    hit = match(name_text, realm_text, maps, active)
    if hit is None:
        return None
    votes[hit] = votes.get(hit, 0) + 1
    if votes[hit] < VOTES:
        return None
    votes["text"] = name_text            # what was read, for the log line
    return hit
