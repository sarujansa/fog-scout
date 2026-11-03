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
    assert _spans(new.parts) == [(10, 20, 1.0), (100, 120, 1.0)] and mode is None and len(done) == 1
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


def test_split_hold_and_fades_with_values_the_editor_offers():
    st = _state(Part(0, 30))
    new, _m, done, _s = _ops(st, [{"op": "split", "at": 12}, {"op": "hold", "at": 12, "seconds": 3},
                                   {"op": "fade", "in": 1, "out": 2}])
    assert [round(sequence.length(p), 2) for p in new.parts] == [12, 3, 18] and new.parts[1].hold == 3
    assert new.fade_in == 1.0 and new.fade_out == 2.0 and len(done) == 3


def test_short_texts_only_in_the_shorts_mode():
    st = _state(Part(0, 30))
    _n, mode, done, skipped = _ops(st, [{"op": "short_title", "text": "4K Nurse"}])
    assert mode is None and not done and skipped[0][1][0] == "nur bei Export-Art Short"
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
    assert not done and len(skipped) == len(bad) and new == st and mode is None
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


# ---- 1.28 (audit B1–B5): refuse instead of bend, no "done" without a change

def _words(items):
    return [w for _o, (w, _kw) in items]


def test_steps_too_close_to_a_clip_edge_are_skipped_not_reported_as_done():
    st = _state(Part(0, 10), Part(20, 30))
    for op in ({"op": "split", "at": 10.05}, {"op": "cut", "from": 9.95, "to": 10.05},
               {"op": "speed", "from": 9.95, "to": 10.05, "factor": 2}):
        new, _m, done, skipped = _ops(st, [op])
        assert not done and _words(skipped) == ["keine Änderung"] and new == st, op


def test_fade_values_outside_the_offered_ones_are_refused_not_moved():
    st = _state(Part(0, 30))
    for op in ({"op": "fade", "in": 0.7}, {"op": "fade", "out": 99}, {"op": "fade", "in": -5},
               {"op": "fade", "in": 1, "out": 3}, {"op": "fade", "in": "1"}):
        new, _m, done, skipped = _ops(st, [op])
        assert not done and _words(skipped) == ["Blende ungültig"] and (new.fade_in, new.fade_out) == (0.0, 0.0), op
    new, _m, done, _s = _ops(st, [{"op": "fade", "in": 0.5}])
    assert new.fade_in == 0.5 and len(done) == 1


def test_a_subtitle_is_measured_after_it_is_cut_to_the_clip():
    st = _state(Part(0, 30))
    new, _m, done, skipped = _ops(st, [{"op": "subtitle", "from": 29.95, "to": 40, "text": "x"}], mode="shorts")
    assert not done and _words(skipped) == ["Untertitel zu kurz"] and new.short is None
    new, _m, done, _s = _ops(st, [{"op": "subtitle", "from": 29, "to": 40, "text": "x"}], mode="shorts")
    assert new.short.subs == [shorts.Sub(29, 30, "x")]
    _n, _m, done, skipped = _ops(st, [{"op": "subtitle", "from": -1, "to": 3, "text": "x"}], mode="shorts")
    assert not done and _words(skipped) == ["Stelle ausserhalb"]


def test_a_freeze_frame_length_outside_the_limits_is_refused():
    st = _state(Part(0, 30))
    for sec in (1e9, 0.01, -3):
        new, _m, done, skipped = _ops(st, [{"op": "hold", "at": 5, "seconds": sec}])
        assert not done and _words(skipped) == ["Standbild: Dauer ungültig"] and new == st, sec


def test_ops_that_are_not_a_list_are_refused_loudly():
    import pytest
    st = _state(Part(0, 30))
    for bad in (5, "cut", {"op": "cut"}, None):
        with pytest.raises(ValueError):
            ec.apply(st, bad, "exact")


def test_the_export_type_changes_only_with_an_explicit_mode_step():
    st = _state(Part(0, 30))
    _n, mode, _d, _s = _ops(st, [{"op": "cut", "from": 0, "to": 5}], mode="exact")
    assert mode is None
    _n, mode, done, skipped = _ops(st, [{"op": "mode", "value": "exact"}], mode="exact")
    assert mode is None and not done and _words(skipped) == ["keine Änderung"]
    _n, mode, _d, _s = _ops(st, [{"op": "mode", "value": "gif"}], mode="exact")
    assert mode == "gif"


def test_steps_beyond_the_limit_are_reported_as_skipped():
    st = _state(Part(0, 60))
    many = [{"op": "split", "at": 1 + i} for i in range(ec.MAX_OPS + 3)]
    _n, _m, done, skipped = _ops(st, many)
    assert len(done) == ec.MAX_OPS and _words(skipped) == ["{n} weitere Schritte nicht ausgeführt (höchstens {max})"]
