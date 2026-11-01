"""Editor projects (project.py) and the media library's list (medialib.py), both pure (1.16)."""
import os
import sys
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import annotate, medialib, project, sequence  # noqa: E402
from fogscout.clipedit import Part  # noqa: E402


def test_a_project_round_trips_and_garbage_is_refused(tmp_path):
    src = tmp_path / "2026-10-30 21-14 Coal Tower – Nurse.mkv"
    src.write_bytes(b"\0" * 10)
    state = sequence.EditState([Part(2, 8, 0.5), Part(20, 30)], (0.1, 0.1, 0.5, 0.5), "free",
                               [annotate.Shape("text", [(0.2, 0.3)], text="Killer", t0=3.0, t1=6.0)], 0.5, 1.0,
                               [[0.0, 0.5, 0.26, 0.32]], True, "blur")
    data = project.to_dict(state, str(src), "Mein Clip", {"mode": "exact", "mix_on": {"dbd": True}})
    path = project.project_path(str(tmp_path / "Clips"), str(src))
    assert path.endswith(os.path.join("Clips", project.PROJECT_DIR, "2026-10-30 21-14 Coal Tower – Nurse" + project.EXT))
    assert project.save(path, data) and project.exists(str(tmp_path / "Clips"), str(src))
    back = project.from_dict(project.load(path), duration=40.0)
    assert back is not None
    got, extra = back
    assert got == state and extra["name"] == "Mein Clip" and extra["mode"] == "exact"
    assert data["source"] == {"file": src.name, "size": 10}
    # held inside the recording, tempos inside SPEEDS, broken bits dropped
    weird = dict(data, parts=[[-3, 5, 99], [38, 60, 1], [1, 1.05, 1]], crop=[2, 0, 1, 1],
                 shapes=[{"kind": "nothing"}, data["shapes"][0]], censor={"on": "x", "style": "weird", "boxes": [[0, 0, 0, 0], [0.1, 0.1, 0.2, 0.2]]})
    got2, _extra = project.from_dict(weird, duration=40.0)
    assert [(p.start, p.end, p.speed) for p in got2.parts] == [(0.0, 5.0, 4.0), (38.0, 40.0, 1.0)]
    assert got2.crop is None and len(got2.shapes) == 1 and got2.boxes == [[0.1, 0.1, 0.2, 0.2]]
    assert got2.censor_on is True and got2.censor_style == "pixel"
    assert project.from_dict({"format": "other"}) is None and project.from_dict(dict(data, parts=[])) is None
    assert project.load(str(tmp_path / "missing.json")) is None
    (tmp_path / "bad.json").write_text("{not json", encoding="utf-8")
    assert project.load(str(tmp_path / "bad.json")) is None
    (tmp_path / "blocker").write_bytes(b"x")                                  # a file where a folder would have to be
    assert not project.save(str(tmp_path / "blocker" / "sub" / "p.json"), data)   # unwritable on every system


def test_the_library_filters_sorts_and_describes_items(tmp_path):
    now = time.time()
    a = medialib.MediaItem("/r/a.mkv", "Coal Tower · Nurse", "round", now - 100, 600.0, 900 * 1024 ** 2, [3.0], ["dbd"], "Coal Tower", "killer", "nurse", 1.0)
    b = medialib.MediaItem("/r/b.mkv", "Ormond · Wraith", "round", now - 200, 30.0, 40 * 1024 ** 2)
    c = medialib.MediaItem("/r/Clips/c.mp4", "Coal Tower – Clip", "clip", now - 50, 0.0, 0)
    items = [a, b, c]
    assert [it.name for it in medialib.sort_items(items, "new")] == [c.name, a.name, b.name]
    assert [it.name for it in medialib.sort_items(items, "old")] == [b.name, a.name, c.name]
    assert [it.name for it in medialib.sort_items(items, "name")][0] == "Coal Tower – Clip"
    assert [it.name for it in medialib.sort_items(items, "long")] == [a.name, b.name, c.name]
    assert [it.name for it in medialib.sort_items(items, "short")] == [b.name, a.name, c.name]   # unknown length last
    assert [it.name for it in medialib.filter_items(items, "coal")] == [a.name, c.name]
    assert [it.name for it in medialib.filter_items(items, "NURSE coal")] == [a.name]
    assert medialib.filter_items(items, "  ") == items and medialib.filter_items(items, "zzz") == []
    assert medialib.fmt_len(600.0) == "10:00" and medialib.fmt_len(3725) == "1:02:05" and medialib.fmt_len(0) == "–"
    assert medialib.fmt_len(65) == "1:05"
    assert medialib.fmt_size(900 * 1024 ** 2) == "900 MB" and medialib.fmt_size(3 * 1024 ** 3) == "3.0 GB"
    assert medialib.fmt_size(10) == "1 kB" and medialib.fmt_size(0) == ""
    assert medialib.facts(a).startswith("10:00 · ") and medialib.facts(a).endswith(" · 900 MB")
    assert medialib.facts(c) == medialib.fmt_when(c.when)
    assert medialib.fmt_when(0) == "" and medialib.fmt_when(now, now).count(":") == 1
    assert medialib.is_video("x.MKV") and not medialib.is_video("x.png")
    f = tmp_path / "import me.mp4"
    f.write_bytes(b"\0" * 5)
    it = medialib.from_file(str(f))
    assert (it.name, it.kind, it.size) == ("import me", "file", 5) and it.when > 0
    assert it.key == os.path.normcase(os.path.abspath(str(f)))
    with pytest.raises(TypeError):
        medialib.MediaItem()
