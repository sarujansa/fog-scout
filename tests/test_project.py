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


# ---- 1.18.1: format 2 (Implementierungsplan Fassung 6, chapter 2 and 4.6)
def _state():
    return sequence.EditState([Part(2, 8, 0.5), Part(20, 30)], (0.1, 0.1, 0.5, 0.5), "free",
                              [annotate.Shape("text", [(0.2, 0.3)], text="Killer", t0=3.0, t1=6.0)], 0.5, 1.0,
                              [[0.0, 0.5, 0.26, 0.32]], True, "blur")


def _write2(folder, pid, source, content=None, name=None, rev=None):
    import json
    content = content or project.content_dict(_state(), {"name": "Clip"})
    data = project.to_dict2(content, pid, source, rev or {"seq": 1}, None)
    path = folder / (name or project.file_name2(source.get("file", "x.mkv"), pid))
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def _rec(sha="a" * 64, size=1000, qfp="q" * 64, file="rec.mkv", t=None, duration=60.0):
    return {"sha256": sha, "size": size, "qfp": qfp, "file": file, "t": t, "duration": duration}


def _src(rec, **kw):
    s = {"sha256": rec["sha256"], "size": rec["size"], "qfp": rec["qfp"], "file": rec["file"], "duration": rec["duration"]}
    s.update(kw)
    return s


def test_format2_file_names_never_collide_for_recordings_of_the_same_name():
    a = project.file_name2("A/2026-10-30 21-14 Coal Tower.mkv", project.new_id())
    b = project.file_name2("B/2026-10-30 21-14 Coal Tower.mkv", project.new_id())
    assert a != b and a.startswith("2026-10-30 21-14 Coal Tower--") and a.endswith(project.EXT)
    assert project.clean_stem('a<b>:c"d/e\\f|g?h*') == "a_b__c_d_e_f_g_h_"


def test_content_hash_ignores_rev_view_saved_and_source():
    c = project.content_dict(_state(), {"name": "Clip", "mode": "exact"})
    d1 = project.to_dict2(c, "id1", {"file": "a"}, {"seq": 1}, {"pos": 1, "span": 10, "offset": 0})
    d2 = project.to_dict2(c, "id1", {"file": "b"}, {"seq": 9}, None)
    strip = lambda d: {k: v for k, v in d.items() if k not in ("id", "rev", "view", "saved", "source", "format", "version")}   # noqa: E731
    assert project.content_hash(strip(d1)) == project.content_hash(strip(d2)) == project.content_hash(c)
    c2 = project.content_dict(_state(), {"name": "Anders"})
    assert project.content_hash(c2) != project.content_hash(c)


def test_view_differs_only_noticeably():
    b = {"pos": 10.0, "span": 30.0, "offset": 5.0}
    assert not project.view_differs(dict(b, pos=10.3), b)
    assert project.view_differs(dict(b, pos=10.6), b)
    assert project.view_differs(dict(b, span=31.0), b) and not project.view_differs(dict(b, span=30.2), b)
    assert project.view_differs(b, None) and not project.view_differs(None, b)


def test_validate_keeps_every_good_field_and_leaves_no_broken_reference():
    """Fassung 6, 4.6: NaN, negative, reversed, beyond the recording, unknown tempo, wrong types – only valid clips
    stay; none left → the default clip, drawings and censoring kept; drawing times clamped; fades and the view held
    inside the sequence."""
    data = project.to_dict2(project.content_dict(_state(), {"name": "Clip"}), "pid", {}, {}, None)
    data["parts"] = [["nan", 5, 1], [-3, 5, 0.3], [6, 4, 1], [55, 90, 1], [10, 10.05, 1], "junk", [1], [30, 40, "x"]]
    data["shapes"].append({"kind": "arrow", "pts": [[0.1, 0.1], [0.2, 0.2]], "t0": 50.0, "t1": 999.0})
    data["shapes"].append({"kind": "arrow", "pts": [[0.1, 0.1], [0.2, 0.2]], "t0": 9.0, "t1": 2.0})
    data["fade_in"] = 1e9
    data["view"] = {"pos": 1e6, "span": 20.0, "offset": -4}
    state, extra, view, notes = project.validate(data, 60.0, [Part(0, 60)])
    assert [(p.start, p.end, p.speed) for p in state.parts] == [(0.0, 5.0, 0.25), (55.0, 60.0, 1.0), (30.0, 40.0, 1.0)]
    assert notes == [] and extra["name"] == "Clip"
    assert (state.shapes[1].t0, state.shapes[1].t1) == (50.0, 60.0)
    assert (state.shapes[2].t0, state.shapes[2].t1) == (None, None)                 # reversed → always shown
    total = sum((p.end - p.start) / p.speed for p in state.parts)
    assert state.fade_in == pytest.approx(total / 2) and view == {"pos": pytest.approx(total), "span": 20.0, "offset": 0.0}
    data["parts"] = [["x", "y"]]
    state, _e, _v, notes = project.validate(data, 60.0, [Part(10, 40)])
    assert [(p.start, p.end) for p in state.parts] == [(10, 40)] and notes == ["parts"]
    assert len(state.shapes) == 3 and state.boxes and state.censor_on                 # the rest survived
    assert project.validate({"format": "other"}, 60, []) is None
    v1 = project.to_dict(_state(), "", "Alt")                                          # format 1 reads the same way
    st1, ex1, view1, _n = project.validate(v1, 40.0, [])
    assert st1 == _state() and ex1["name"] == "Alt" and view1 is None


def test_resolve_assigns_automatically_only_by_the_full_hash(tmp_path):
    rec = _rec()
    _write2(tmp_path, "a" * 32, _src(rec))
    r = project.resolve(rec, project.scan(str(tmp_path)))
    assert r.kind == "auto" and r.entries[0].id == "a" * 32
    moved = dict(rec, file="renamed elsewhere.mkv")                                  # moved/renamed: same content
    assert project.resolve(moved, project.scan(str(tmp_path))).kind == "auto"
    assert project.resolve(dict(rec, sha256=None), project.scan(str(tmp_path))).kind == "verify"
    assert project.resolve(dict(rec, duration=70.0), project.scan(str(tmp_path))).kind != "auto"


def test_a_change_only_in_the_middle_is_never_assigned(tmp_path):
    """Same size, same first and last MiB (qfp), one byte different in the middle → other full hash → mismatch."""
    import hashlib
    from fogscout import filehash
    a = tmp_path / "a.mkv"
    data = bytearray(os.urandom(8 << 20))
    a.write_bytes(bytes(data))
    data[4 << 20] ^= 0xFF
    b = tmp_path / "b.mkv"
    b.write_bytes(bytes(data))
    assert filehash.qfp(str(a)) == filehash.qfp(str(b))                               # the test hits the gap
    sha_a, sha_b = hashlib.sha256(a.read_bytes()).hexdigest(), hashlib.sha256(b.read_bytes()).hexdigest()
    assert sha_a != sha_b
    proj = tmp_path / "P"
    proj.mkdir()
    rec_a = _rec(sha=sha_a, size=8 << 20, qfp=filehash.qfp(str(a)), file="a.mkv")
    p = _write2(proj, "c" * 32, _src(rec_a))
    before = p.read_bytes()
    rec_b = dict(rec_a, sha256=sha_b, file="b.mkv")
    r = project.resolve(rec_b, project.scan(str(proj)))
    assert r.kind == "mismatch" and p.read_bytes() == before


def test_two_recordings_of_the_same_name_keep_their_own_projects(tmp_path):
    a, b = _rec(sha="1" * 64, qfp="x" * 64, size=10), _rec(sha="2" * 64, qfp="y" * 64, size=20)
    _write2(tmp_path, "1" * 32, _src(a))
    _write2(tmp_path, "2" * 32, _src(b))
    ra, rb = project.resolve(a, project.scan(str(tmp_path))), project.resolve(b, project.scan(str(tmp_path)))
    assert (ra.kind, rb.kind) == ("auto", "auto") and ra.entries[0].id == "1" * 32 and rb.entries[0].id == "2" * 32


def test_same_id_in_two_files_is_ambiguous_and_nothing_is_preferred(tmp_path):
    rec = _rec()
    _write2(tmp_path, "d" * 32, _src(rec))
    _write2(tmp_path, "d" * 32, _src(rec), name="copy-PCNAME" + project.EXT,
            content=project.content_dict(_state(), {"name": "anders"}))
    r = project.resolve(rec, project.scan(str(tmp_path)))
    assert r.kind == "ambiguous_id" and len(r.entries) == 2


def test_two_projects_for_one_recording_are_ambiguous(tmp_path):
    rec = _rec()
    _write2(tmp_path, "e" * 32, _src(rec))
    _write2(tmp_path, "f" * 32, _src(rec))
    assert project.resolve(rec, project.scan(str(tmp_path))).kind == "ambiguous_recording"


def test_unverified_and_user_verified_projects_are_never_automatic(tmp_path):
    rec = _rec()
    _write2(tmp_path, "g" * 32, _src(rec, sha256=None, verified="user"))
    assert project.resolve(rec, project.scan(str(tmp_path))).kind == "unverified"
    other = tmp_path / "o"
    other.mkdir()
    _write2(other, "h" * 32, _src(rec, sha256="9" * 64, verified="user"))           # "user" is no proof
    assert project.resolve(rec, project.scan(str(other))).kind == "mismatch"


def test_format1_is_offered_never_automatic_and_stays_byte_identical(tmp_path):
    src = tmp_path / "2026-10-30 21-14 Coal Tower.mkv"
    src.write_bytes(b"\0" * 100)
    clips = tmp_path / "Clips"
    path = project.project_path(str(clips), str(src))
    assert project.save(path, project.to_dict(_state(), str(src), "Alt"))
    before = open(path, "rb").read()
    rec = _rec(file=src.name, size=100)
    r = project.resolve(rec, project.scan(os.path.dirname(path)))
    assert r.kind == "legacy" and r.entries[0].path == path
    assert project.resolve(dict(rec, size=101), project.scan(os.path.dirname(path))).kind == "changed"
    _write2(clips / project.PROJECT_DIR, "i" * 32, _src(rec, migrated_from=os.path.basename(path), sha256="8" * 64,
                                                         qfp="z" * 64))
    assert project.resolve(rec, project.scan(os.path.dirname(path))).kind != "legacy"   # already carried on
    assert open(path, "rb").read() == before


def test_a_broken_file_does_not_break_the_catalog(tmp_path):
    rec = _rec()
    _write2(tmp_path, "j" * 32, _src(rec))
    (tmp_path / ("kaputt" + project.EXT)).write_text("{nope", encoding="utf-8")
    (tmp_path / (".tmp" + project.EXT)).write_text("{}", encoding="utf-8")            # hidden temp names are skipped
    entries = project.scan(str(tmp_path))
    assert sorted(e.ok for e in entries) == [False, True]
    assert project.resolve(rec, entries).kind == "auto"
