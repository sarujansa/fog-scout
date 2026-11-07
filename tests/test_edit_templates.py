"""1.44: „Schnitt-Vorlagen“ – an applied proposal kept as a recipe (moments from the start or before the end, no
censor boxes), stored in the settings, applied locally to another cut without a request, as one undo step."""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import askclaude, editcommands as ec, sequence  # noqa: E402
from fogscout.clipedit import Part  # noqa: E402

import test_editor_claude as tec  # noqa: E402
from test_editor_claude import FF, KEY, FakeOpener, _pump, _spans, _window  # noqa: E402

clip, qapp = tec.clip, tec.qapp                  # the same fixtures (an offscreen editor on a lavfi clip)


def _spans_of(state):
    return [(round(p.start, 2), round(p.end, 2), p.speed) for p in state.parts]


def test_a_template_keeps_moments_from_the_start_or_the_end_and_fits_another_length():
    st = sequence.EditState([Part(0, 10)])
    ops = [{"op": "cut", "from": 0, "to": 2, "why": "Anfang"}, {"op": "speed", "from": 5, "to": 8, "factor": 2},
           {"op": "censor", "x": 0, "y": 0, "w": 0.1, "h": 0.1}, {"op": "fade", "out": 1}]
    _new, _m, done, _s = ec.apply(st, ops, "copy", picture=True)
    tpl = ec.to_template(st, [op for op, _w in done], "copy", "  Mein​ Stil ")
    assert tpl["name"] == "Mein Stil" and [o["op"] for o in tpl["ops"]] == ["cut", "speed", "fade"]   # no box
    assert tpl["ops"][1]["from"] == ["e", 3.0] and "why" not in tpl["ops"][0]     # 8 s left: 5 s = 3 s before the end
    longer = sequence.EditState([Part(0, 20)])
    ops2 = ec.from_template(longer, tpl, "copy")
    assert ops2[1] == {"op": "speed", "factor": 2.0, "from": 15.0, "to": 18.0}
    new, _m, _d, skipped = ec.apply(longer, ops2, "copy")
    assert _spans_of(new) == [(2.0, 17.0, 1.0), (17.0, 20.0, 2.0)] and new.fade_out == 1.0 and not skipped
    assert ec.to_template(st, [ops[2]], "copy", "Nur Kasten") is None              # nothing but a box
    assert ec.to_template(st, ops[:1], "copy", "  ") is None                       # no name


def test_broken_or_too_many_templates_are_left_out():
    st = sequence.EditState([Part(0, 10)])
    bad = {"name": "x", "ops": [{"op": "cut", "from": ["s", "nan"], "to": ["s", 2]}, {"op": "explode"},
                                {"op": "censor", "x": 0, "y": 0, "w": 1, "h": 1}, {"op": "cut", "from": ["e", -1]},
                                {"op": "fade", "in": 1}]}
    assert ec.from_template(st, bad, "copy") == [{"op": "fade", "in": 1.0}]
    assert ec.from_template(st, None, "copy") == [] and ec.from_template(st, {"ops": "x"}, "copy") == []
    stored = [{"name": f"T{i}", "ops": [{"op": "fade", "in": 1}]} for i in range(30)] + ["x", {"name": "", "ops": [1]}]
    assert len(ec.templates(stored)) == ec.MAX_TEMPLATES and ec.templates("x") == []
    new = ec.with_template(stored, {"name": "T5", "ops": [{"op": "fade", "out": 1}]})
    assert new[0]["ops"] == [{"op": "fade", "out": 1}] and [t["name"] for t in new].count("T5") == 1
    assert len(new) == ec.MAX_TEMPLATES


@pytest.mark.skipif(FF is None, reason="imageio-ffmpeg not installed")
def test_the_editor_saves_a_taken_proposal_and_applies_it_without_a_request(qapp, clip, tmp_path, monkeypatch):
    fake = FakeOpener({"summary": "Anfang weg.", "ops": [{"op": "cut", "from": 0, "to": 2}, {"op": "fade", "out": 1}]})
    monkeypatch.setattr(askclaude, "OPENER", fake)
    store = {}
    win = _window(qapp, clip, tmp_path)
    try:
        win.on_setting = lambda k, v: store.__setitem__(k, json.loads(json.dumps(v)))
        win.templates_from = lambda: store.get("edit_templates") or []
        win._templates_refresh()
        assert not win.tpl_box.isVisible() and not win.tpl_save_btn.isVisible()     # nothing stored, nothing taken
        win.claude_key = lambda: KEY
        win._claude_refresh()
        before = _spans(win)
        win.cl_field.setText("erste 2 s weg, am Ende ausblenden")
        win.claude_ask()
        assert _pump(qapp, lambda: win.cl_take_btn.isVisible())
        win.claude_take()
        assert win.tpl_save_btn.isVisible()
        win.tpl_name.setText("Kurz")
        win.template_save()
        assert [t["name"] for t in store["edit_templates"]] == ["Kurz"] and not win.tpl_save_btn.isVisible()
        win.undo()
        assert _spans(win) == before
        win.claude_key = lambda: ""                                               # Claude off: still works
        win._claude_refresh()
        assert win.tpl_box.isVisible() and win.tpl_box.currentText() == "Kurz"
        win.template_apply()
        assert win.cl_take_btn.isVisible() and len(fake.bodies) == 1             # no request
        win.claude_take()
        assert _spans(win)[0][0] == 2.0 and win.fade_out_box.currentData() == 1.0
        win.undo()                                                                # one step
        assert _spans(win) == before
        win.template_delete()
        assert store["edit_templates"] == [] and not win.tpl_box.isVisible()
    finally:
        win.close()
