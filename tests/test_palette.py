"""1.26: the command palette's ranking (palette.py, pure)."""
import time

from fogscout import palette
from fogscout.palette import Entry


def _entries():
    return [Entry("action", "a:scan", "Scannen"),
            Entry("action", "a:toggle", "Karte ausblenden"),
            Entry("page", "p:overlay", "Overlay", "Was im Spiel erscheint, wo und wie gross"),
            Entry("page", "p:stats", "Statistik", "Deine Runden, Kills und Wartezeiten"),
            Entry("setting", "s:size", "Eigene Grösse zurücksetzen", "Overlay"),
            Entry("setting", "s:auto", "Mit Windows starten (im Infobereich)", "Einstellungen"),
            Entry("setting", "s:caption", "Map-Namen über der Karte anzeigen", "Overlay",
                  words="map-namen über der karte anzeigen | show the map name above the map"),
            Entry("map", "m:coal", "Coal Tower", "The MacMillan Estate", words="Kohleturm"),
            Entry("map", "m:gid", "Gideon Meat Plant", "The Game"),
            Entry("round", "r:1", "Coal Tower II", "03.11.2026 20:15 · The Nurse · 4 Kills")]


def _ids(query, **kw):
    return [e.id for e in palette.rank(query, _entries(), **kw)]


def test_a_word_start_comes_before_a_part_of_a_word_and_a_typo():
    assert _ids("scan")[0] == "a:scan"
    assert _ids("scanen") == ["a:scan"]                       # a typo is forgiven
    assert _ids("tower")[:2] == ["m:coal", "r:1"]
    assert "m:coal" in _ids("ower")                           # inside a word
    assert _ids("abc") == []                                  # too short for a typo, in nothing


def test_umlauts_ss_and_other_words_are_found():
    assert "s:size" in _ids("größe")
    assert "s:size" in _ids("grosse")
    assert "s:auto" in _ids("autostart")                      # SEARCH_ALSO
    assert "s:caption" in _ids("map name above")              # the English name in the words
    assert "m:coal" in _ids("kohleturm")                      # a map's other language


def test_every_typed_word_must_be_found_and_a_setting_is_not_found_by_its_page():
    assert _ids("coal kills") == ["r:1"]
    assert "s:size" not in _ids("overlay")                    # 1.8.38: "Overlay" matched every setting
    assert "p:overlay" in _ids("overlay")
    assert "r:1" in _ids("nurse")                             # a round by its killer


def test_a_question_finds_by_half_its_words_when_nothing_has_all():
    assert _ids("eigene grösse machen")[0] == "s:size"         # "machen" is in nothing
    assert _ids("coal kills") == ["r:1"]                      # every word found: only those
    assert _ids("xyz abc qqq") == []


def test_groups_follow_their_best_hit_and_the_limits_hold():
    got = palette.rank("coal", _entries())
    kinds = [e.kind for e in got]
    assert kinds == sorted(kinds, key=kinds.index)            # one block per kind
    many = [Entry("map", f"m:{i}", f"Map {i}") for i in range(20)] + [Entry("setting", "s:x", "Map-Grösse")]
    got = palette.rank("map", many)
    assert sum(e.kind == "map" for e in got) == palette.PER_KIND and any(e.id == "s:x" for e in got)
    assert len(palette.rank("map", many, limit=3)) == 3


def test_an_empty_query_shows_the_recent_picks_then_the_actions():
    recent = palette.remember(palette.remember([], "m:gid"), "s:size")
    assert recent == ["s:size", "m:gid"]
    assert _ids("", recent=recent) == ["s:size", "m:gid", "a:scan", "a:toggle"]
    assert _ids("  ") == ["a:scan", "a:toggle"]


def test_recent_picks_rank_a_little_higher_and_are_kept_short():
    entries = [Entry("setting", "s:a", "Position"), Entry("setting", "s:b", "Position")]
    assert [e.id for e in palette.rank("position", entries, recent=["s:b"])] == ["s:b", "s:a"]
    recent = []
    for i in range(20):
        recent = palette.remember(recent, f"x{i}")
    assert len(recent) == palette.RECENT_KEPT and recent[0] == "x19"
    assert palette.remember(recent, "x15")[:2] == ["x15", "x19"]


def test_ranking_a_large_index_per_key_press(capsys):
    """Measured, not limited (shared CI runners): ~1500 entries as a full catalogue has, prepared once."""
    entries = [Entry("setting", f"s:{i}", f"Einstellung Nummer {i} mit Text", "Seite") for i in range(1200)]
    entries += [Entry("map", f"m:{i}", f"Map {i}", "Realm", words="Karte map carte") for i in range(250)]
    entries += _entries()
    for e in entries:
        e.prepare()
    t0 = time.perf_counter()
    for q in ("e", "ei", "ein", "eins", "einst", "coal", "größe", "xyz"):
        palette.rank(q, entries)
    per = (time.perf_counter() - t0) / 8 * 1000
    with capsys.disabled():
        print(f"\npalette.rank: {len(entries)} Einträge, {per:.1f} ms je Tastendruck")
