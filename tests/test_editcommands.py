"""1.27: Claude's edit operations in the clip editor (editcommands.py, pure)."""
import json

from fogscout import editcommands as ec, sequence, shorts
from fogscout.clipedit import Part


def _state(*parts, **kw):
    return sequence.EditState(list(parts), **kw)


def _ops(state, ops, mode="exact"):
    return ec.apply(state, ops, mode)


def _spans(parts):
    return [(round(p.start, 2), round(p.end, 2), p.speed) for p in parts]


def test_describe_shows_numbers_only_never_paths_or_names():
    st = _state(Part(10, 40), Part(100, 110, speed=2.0), Part(50, 50, hold=2.0),
                sources=["C:/Users/saru/Videos/2026-11-03 Coal Tower II - The Nurse.mkv"], fade_out=1.0)
    d = ec.describe(st, "exact", marks=[12.0, 3.5])
    assert d["length"] == 30 + 5 + 2 and [c["from"] for c in d["clips"]] == [0, 30, 35]
    assert d["clips"][1]["speed"] == 2.0 and d["clips"][2]["still"] is True and d["marks"] == [3.5, 12.0]
    text = ec.content("erste 10 s weg", st, "exact", [3.5])
    assert "Coal" not in text and "Nurse" not in text and "Videos" not in text and "saru" not in text
    assert "erste 10 s weg" in text and json.loads(text.split("\n")[1])["fade_out"] == 1.0


def test_cut_and_keep_take_ranges_of_the_finished_clip_across_clips():
    st = _state(Part(0, 20), Part(100, 120))                 # output 0–20, 20–40
    new, mode, done, skipped = _ops(st, [{"op": "cut", "from": 0, "to": 10}])
    assert _spans(new.parts) == [(10, 20, 1.0), (100, 120, 1.0)] and mode == "exact" and len(done) == 1
    new, *_ = _ops(st, [{"op": "cut", "from": 15, "to": 25}])        # over the seam
    assert _spans(new.parts) == [(0, 15, 1.0), (105, 120, 1.0)]
    new, *_ = _ops(st, [{"op": "keep", "from": 15, "to": 25}])
    assert _spans(new.parts) == [(15, 20, 1.0), (100, 105, 1.0)]
    assert _spans(st.parts) == [(0, 20, 1.0), (100, 120, 1.0)]     # the original untouched


def test_later_ops_see_the_clip_after_the_earlier_ones():
    st = _state(Part(0, 60))
    new, *_ = _ops(st, [{"op": "cut", "from": 0, "to": 10}, {"op": "cut", "from": 0, "to": 10}])
    assert _spans(new.parts) == [(20, 60, 1.0)]


def test_speed_only_with_an_offered_tempo_and_never_on_a_still():
    st = _state(Part(0, 30), Part(5, 5, hold=2.0))
    new, _m, done, skipped = _ops(st, [{"op": "speed", "from": 10, "to": 32, "factor": 2}])
    assert _spans(new.parts) == [(0, 10, 1.0), (10, 30, 2.0), (5, 5, 1.0)] and new.parts[2].hold == 2.0
    _n, _m, done, skipped = _ops(st, [{"op": "speed", "from": 0, "to": 10, "factor": 3}])
    assert not done and skipped[0][1][0] == "Tempo nicht erlaubt"


def test_split_hold_and_fades_snap_to_what_the_editor_offers():
    st = _state(Part(0, 30))
    new, _m, done, _s = _ops(st, [{"op": "split", "at": 12}, {"op": "hold", "at": 12, "seconds": 3},
                                   {"op": "fade", "in": 0.8, "out": 5}])
    assert [round(sequence.length(p), 2) for p in new.parts] == [12, 3, 18] and new.parts[1].hold == 3
    assert new.fade_in == 1.0 and new.fade_out == 2.0 and len(done) == 3


def test_short_texts_only_in_the_shorts_mode():
    st = _state(Part(0, 30))
    _n, mode, done, skipped = _ops(st, [{"op": "short_title", "text": "4K Nurse"}])
    assert mode == "exact" and not done and skipped[0][1][0] == "nur bei Export-Art Short"
    new, mode, done, _s = _ops(st, [{"op": "mode", "value": "shorts"}, {"op": "short_title", "text": "  4K   Nurse "},
                                    {"op": "subtitle", "from": 2, "to": 5, "text": "Hook!"}])
    assert mode == "shorts" and new.short.title == "4K Nurse"
    assert new.short.subs == [shorts.Sub(2, 5, "Hook!")] and st.short is None


def test_whatever_does_not_fit_is_skipped_never_guessed():
    st = _state(Part(0, 30))
    bad = [{"op": "explode"}, "nonsense", {"op": "cut", "from": 20, "to": 10}, {"op": "cut", "from": "a", "to": 3},
           {"op": "cut", "from": 50, "to": 60}, {"op": "split", "at": 0}, {"op": "mode", "value": "mp3"},
           {"op": "cut", "from": True, "to": 5}, {"op": "fade"}]
    new, mode, done, skipped = _ops(st, bad)
    assert not done and len(skipped) == len(bad) and new == st and mode == "exact"
    many = [{"op": "split", "at": 1 + i} for i in range(ec.MAX_OPS + 5)]
    _n, _m, done, _s = _ops(st, many)
    assert len(done) == ec.MAX_OPS


def test_an_answer_that_would_leave_nothing_changes_nothing():
    st = _state(Part(0, 30))
    new, mode, done, skipped = _ops(st, [{"op": "cut", "from": 0, "to": 30}])
    assert new == st and not done and skipped
    new, mode, done, skipped = _ops(st, [{"op": "cut", "from": 0, "to": 15}, {"op": "cut", "from": 0, "to": 15}])
    assert new.parts and len(done) == 1 and skipped                 # the second one would empty it: skipped


def test_the_schema_offers_exactly_the_kinds_apply_knows():
    assert ec.SCHEMA["properties"]["ops"]["items"]["properties"]["op"]["enum"] == list(ec.KINDS)
    for kind in ec.KINDS:
        assert kind in ec.SYSTEM
