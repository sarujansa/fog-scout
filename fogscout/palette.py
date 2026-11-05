"""1.26 (user: "wenn man was sucht soll sich das GUI verdunkeln und Vorschläge anhand der Suche geben"): the
command palette's model – pure, no Qt. Entries of five kinds (actions, pages, settings, maps, rounds) are ranked
against what was typed: word prefixes first, then parts of words, then a typo (difflib), with the words people
search with (SEARCH_ALSO) and the umlauts/ß folded away. The window draws them (qt_palette), the App fills and runs
them (app_palette)."""
from __future__ import annotations

import difflib
import unicodedata
from dataclasses import dataclass, field
from functools import lru_cache

KINDS = ("action", "page", "setting", "map", "round")      # the order of the groups in the list
LIMIT = 12                       # rows shown at most
PER_KIND = 6                     # … and at most this many of one kind (a map search does not hide the settings)
TYPO_MIN = 4                     # a typo is forgiven from words this long on
TYPO_RATIO = 0.8                 # difflib ratio of a typed word to a word of the entry
RECENT_BONUS = 0.5               # an entry chosen recently ranks a little higher
RECENT_KEPT = 8                  # how many chosen entries are remembered (setting palette_recent)

# 1.8.38 (QA audit: "autostart", "Tastenkürzel", "Backup" … found nothing): words people search with that the
# labels do not use – a label (either language, folded) containing the key is also found by the words.
# 1.26: here, so the palette and the window share them (qt_window re-exports it).
SEARCH_ALSO = {"tast": "hotkey shortcut tastenkürzel", "hotkey": "taste tastenkürzel shortcut",
               "mit windows starten": "autostart", "start with windows": "autostart",
               "farb": "color colour theme", "colour": "color farbe theme", "theme": "farbe color",
               "sicherung": "backup", "backup": "sicherung", "deckkraft": "opacity transparenz transparency",
               "opacity": "deckkraft transparenz transparency", "grösse": "size zoom grösser kleiner",
               "size": "grösse zoom bigger smaller", "cross-play": "crossplay", "crossplay": "cross-play",
               "aufnahme": "obs recording", "recording": "obs aufnahme", "einrichtung": "setup assistent wizard",
               "setup": "einrichtung assistent wizard", "aktualis": "update", "update": "aktualisieren",
               # 1.23: the folded part at the foot of the log page – found by what it holds (1.38.12: window
               # capture and scan rate are on Einstellungen → Erkennung → Technik now, found by their own labels)
               "erweitert (fehlersuche": "advanced debug-bilder rundenende diagnose",
               "advanced (troubleshooting": "erweitert debug pictures end of round"}


@dataclass
class Entry:
    """One row of the palette. ``id`` is stable across openings (recent picks, Claude's answer); ``action``/``arg``
    tell the App what to do (Enter), ``alt`` what Ctrl+Enter does ("" = the same)."""
    kind: str
    id: str
    title: str
    sub: str = ""
    action: str = ""
    arg: object = None
    alt: str = ""
    words: str = ""              # more to match against (other language, realm, killer …); not shown
    static: bool = False         # 1.28: a fixed program text (i18n.is_program_text) – only such go to Claude
    _words: tuple = field(default=(), repr=False, compare=False)

    def prepare(self) -> "Entry":
        # a setting's sub is its page: "Overlay" would find every setting of that page (1.8.38) – not matched
        sub = "" if self.kind == "setting" else self.sub
        self._words = tuple(_words(" ".join((self.title, sub, self.words, _also(self.title)))))
        return self


@lru_cache(maxsize=4096)
def norm(text: str) -> str:
    """Lower case, accents away, ß → ss, everything but letters and digits a space."""
    t = unicodedata.normalize("NFKD", str(text or "")).replace("ß", "ss").casefold()
    t = "".join(c for c in t if not unicodedata.combining(c))
    return "".join(c if c.isalnum() else " " for c in t)


def _words(text: str) -> list[str]:
    return [w for w in norm(text).split() if w]


def _also(title: str) -> str:
    low = str(title or "").casefold()
    return " ".join(v for k, v in SEARCH_ALSO.items() if k in low)


def _one(q: str, w: str) -> float:
    if w.startswith(q):
        return 3.0
    if q in w:
        return 2.0
    if len(q) >= TYPO_MIN and abs(len(w) - len(q)) <= 2:
        m = difflib.SequenceMatcher(None, q, w)
        if m.real_quick_ratio() >= TYPO_RATIO and m.quick_ratio() >= TYPO_RATIO and m.ratio() >= TYPO_RATIO:
            return 1.0
    return 0.0


def _word_score(q: str, words: tuple, memo: dict | None = None) -> float:
    """3 = a word starts with it, 2 = inside a word, 1 = a typo of a word, 0 = not there. ``memo``: (q, w) → score
    for one ranking – the entries share most of their words, so each pair is weighed once."""
    best = 0.0
    for w in words:
        if memo is None:
            s = _one(q, w)
        else:
            s = memo.get((q, w))
            if s is None:
                s = memo[(q, w)] = _one(q, w)
        if s > best:
            best = s
            if s == 3.0:
                break
    return best


def score(query: str, entry: Entry, memo: dict | None = None, need: int = 0) -> float:
    """0 = no match; else the mean of the typed words' scores, plus a little for a title that begins with the query.
    ``need``: how many typed words must be found (0 = every one)."""
    qs = _words(query)
    if not qs:
        return 0.0
    words = entry._words or entry.prepare()._words
    total, found = 0.0, 0
    for q in qs:
        s = _word_score(q, words, memo)
        if not s and not need:
            return 0.0
        total += s
        found += s > 0
    if found < (need or len(qs)):
        return 0.0
    s = total / len(qs)
    if norm(entry.title).strip().startswith(norm(query).strip()):
        s += 0.75
    return s


def rank(query: str, entries, recent=(), limit: int = LIMIT) -> list[Entry]:
    """The entries for ``query``, best first and grouped by kind (the kind of the best hit first, ties in KINDS
    order); at most ``limit`` rows and PER_KIND of one kind. An empty query: the recent picks, then the actions."""
    recent = list(recent or ())
    if not str(query or "").strip():
        by_id = {e.id: e for e in entries}
        out = [by_id[i] for i in recent if i in by_id]
        out += [e for e in entries if e.kind == "action" and e.id not in recent]
        return out[:limit]
    scored, memo = [], {}
    n = len(_words(query))
    for need in (0, (n + 1) // 2) if n > 1 else (0,):   # nothing has every word: half of them ("karte grösser machen")
        for i, e in enumerate(entries):
            s = score(query, e, memo, need)
            if s:
                if e.id in recent:
                    s += RECENT_BONUS
                scored.append((s, i, e))
        if scored:
            break
    scored.sort(key=lambda t: (-t[0], t[1]))
    picked, per = [], {}
    for _s, _i, e in scored:
        if per.get(e.kind, 0) >= PER_KIND:
            continue
        per[e.kind] = per.get(e.kind, 0) + 1
        picked.append(e)
        if len(picked) >= limit:
            break
    order = {k: n for n, k in enumerate(KINDS)}
    best = {}
    for n, e in enumerate(picked):                  # a kind's place follows its best hit, not the KINDS order
        best.setdefault(e.kind, n)
    return sorted(picked, key=lambda e: (best[e.kind], order.get(e.kind, 99)))


def remember(recent, entry_id: str) -> list[str]:
    """``recent`` with ``entry_id`` first, at most RECENT_KEPT."""
    out = [entry_id] + [i for i in (recent or ()) if i != entry_id]
    return out[:RECENT_KEPT]
