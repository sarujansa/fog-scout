"""1.11.10: the line cache under rounds.jsonl / official.jsonl (fogscout/jsonlcache.py)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fogscout import history, jsonlcache  # noqa: E402


def _parse(line):
    d = json.loads(line)
    return d if isinstance(d, dict) and "n" in d else None


def test_a_grown_file_parses_only_its_new_lines_and_a_replaced_one_from_the_start(tmp_path):
    p = tmp_path / "f.jsonl"
    p.write_text("".join(json.dumps({"n": i}) + "\n" for i in range(3)), encoding="utf-8")
    c = jsonlcache.LineCache(_parse)
    assert [d["n"] for d in c.items(str(p))] == [0, 1, 2] and (c.full, c.tail) == (1, 0)
    with open(p, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"n": 3}) + "\n" + "not json\n" + json.dumps({"x": 1}) + "\n")
    assert [d["n"] for d in c.items(str(p))] == [0, 1, 2, 3] and (c.full, c.tail) == (1, 1)
    assert [d["n"] for d in c.items(str(p))] == [0, 1, 2, 3] and (c.full, c.tail) == (1, 2)     # unchanged
    # replaced (a correction rewrites the file): same length, other bytes early on → from the start
    text = p.read_text(encoding="utf-8").replace('{"n": 0}', '{"n": 9}')
    p.write_text(text, encoding="utf-8")
    assert [d["n"] for d in c.items(str(p))] == [9, 1, 2, 3] and c.full == 2
    p.write_text(json.dumps({"n": 5}) + "\n", encoding="utf-8")                    # shorter: from the start
    assert [d["n"] for d in c.items(str(p))] == [5] and c.full == 3


def test_a_line_without_its_break_is_read_but_not_kept(tmp_path):
    """A line still being written (or a file without a final break) counts, but is parsed again next time – once
    complete it is kept; a broken last line glued over by the next append (history._append_line) is skipped."""
    p = tmp_path / "f.jsonl"
    p.write_bytes(b'{"n": 1}\n{"n": 2}')
    c = jsonlcache.LineCache(_parse)
    assert [d["n"] for d in c.items(str(p))] == [1, 2]
    with open(p, "ab") as fh:
        fh.write(b"\n" + b'{"n": 3}\n')
    assert [d["n"] for d in c.items(str(p))] == [1, 2, 3] and c.tail == 1
    p.write_bytes(b'{"n": 1}\n{"n": 2')                                           # cut off mid-line
    assert [d["n"] for d in c.items(str(p))] == [1]
    assert c.items(str(tmp_path / "missing.jsonl")) == []


def test_history_hands_out_fresh_rounds_from_the_cache(tmp_path):
    """The statistics change the rounds they load (killer names, role from the stats page …) – the next load must
    not see that; a new round appended is read as the only new line."""
    path = str(tmp_path / "rounds.jsonl")
    history.append(path, history.Round(100, 600, "a", "A", role="killer"))
    first = history.load(path)
    first[0].role, first[0].killer = "survivor", "X"
    assert (history.load(path)[0].role, history.load(path)[0].killer) == ("killer", "")
    tail = history._LINES.tail
    history.append(path, history.Round(200, 600, "b", "B"))
    assert [r.map_id for r in history.load(path)] == ["a", "b"] and history._LINES.tail > tail
    assert history.set_role(path, 100, "custom").custom                            # rewritten: read anew
    assert [r.custom for r in history.load(path)] == [True, False]


def test_a_number_too_big_for_an_int_skips_only_its_line(tmp_path):
    """1.12.3 (audit): ``Infinity`` (json.dumps writes it for a float inf) made int() raise OverflowError, which the
    cache did not catch – one such line in official.jsonl and the whole file could not be read."""
    from fogscout import official
    path = str(tmp_path / "official.jsonl")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write('{"t": 1000.0, "map": "Coal Tower", "bp": 25000}\n')
        fh.write('{"t": 2000.0, "map": "Coal Tower", "bp": Infinity}\n')
        fh.write('{"t": 3000.0, "map": "Coal Tower", "bp": 12000}\n')
    assert [m.t for m in official.load(path)] == [1000.0, 3000.0]


def test_the_statistics_files_are_parsed_once_in_a_thread_at_start(tmp_path):
    """1.16.2 (A8): App._joined_preload parses rounds.jsonl / official.jsonl off the window's thread; the first
    join then reads only the cache (no second full parse), and missing or broken files never raise."""
    from types import SimpleNamespace
    from fogscout import official
    from fogscout.app_stats import StatsTab
    host = SimpleNamespace(root_dir=str(tmp_path))
    host._hist_path = lambda: StatsTab._hist_path(host)
    host._official_path = lambda: StatsTab._official_path(host)
    path = host._hist_path()
    history.append(path, history.Round(100, 600, "a", "A", role="killer"))
    with open(host._official_path(), "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"t": 62.0, "map": "A", "role": "killer"}) + "\n" + "{broken\n")
    rounds_full, matches_full = history._LINES.full, official._LINES.full
    StatsTab._joined_preload(host).join(10)
    assert (history._LINES.full, official._LINES.full) == (rounds_full + 1, matches_full + 1)
    assert [r.map_id for r in history.load(path)] == ["a"] and len(official.load(host._official_path())) == 1
    assert (history._LINES.full, official._LINES.full) == (rounds_full + 1, matches_full + 1)    # cache only
    empty = SimpleNamespace(_hist_path=lambda: str(tmp_path / "none" / "r.jsonl"),
                            _official_path=lambda: str(tmp_path / "none" / "o.jsonl"))
    t = StatsTab._joined_preload(empty)
    t.join(10)
    assert not t.is_alive()
