"""1.8.80: daily copies of rounds.jsonl / official.jsonl in backup/ (backups.py)."""
import os
import time

from fogscout import backups

DAY = 86400


def _day(t):
    return time.strftime("%Y-%m-%d", time.localtime(t))


def test_a_changed_file_is_copied_once_a_day_and_unchanged_ones_are_not(tmp_path):
    root = str(tmp_path)
    (tmp_path / "rounds.jsonl").write_text("a\n")
    t0 = time.time()
    r = backups.snapshot(root, t0)
    assert r["copied"] == [f"rounds-{_day(t0)}.jsonl"] and r["pruned"] == []     # official.jsonl missing: skipped
    assert (tmp_path / "backup" / r["copied"][0]).read_text() == "a\n"
    assert backups.snapshot(root, t0)["copied"] == []                            # same day: once
    assert backups.snapshot(root, t0 + DAY)["copied"] == []                      # next day, same content: nothing
    (tmp_path / "rounds.jsonl").write_text("a\nb\n")
    (tmp_path / "official.jsonl").write_text("m\n")
    r = backups.snapshot(root, t0 + DAY)
    assert sorted(r["copied"]) == sorted([f"rounds-{_day(t0 + DAY)}.jsonl", f"official-{_day(t0 + DAY)}.jsonl"])
    assert backups.status(root) == (3, _day(t0 + DAY))
    assert backups.copies(str(tmp_path / "backup"), "rounds") == [f"rounds-{_day(t0)}.jsonl",
                                                                  f"rounds-{_day(t0 + DAY)}.jsonl"]


def test_only_the_newest_copies_stay(tmp_path):
    root = str(tmp_path)
    t0 = time.time() - 40 * DAY
    for i in range(backups.KEEP + 3):
        (tmp_path / "rounds.jsonl").write_text(f"{i}\n")
        backups.snapshot(root, t0 + i * DAY)
    kept = backups.copies(str(tmp_path / "backup"), "rounds")
    assert len(kept) == backups.KEEP and kept[0] == f"rounds-{_day(t0 + 3 * DAY)}.jsonl"
    assert (tmp_path / "backup" / kept[-1]).read_text() == f"{backups.KEEP + 2}\n"


def test_a_tagged_copy_is_taken_even_when_today_has_one(tmp_path):
    root = str(tmp_path)
    (tmp_path / "rounds.jsonl").write_text("a\n")
    t0 = time.time()
    backups.snapshot(root, t0)
    r = backups.snapshot(root, t0, tag="vorher")
    assert r["copied"] == [f"rounds-{_day(t0)}-vorher.jsonl"]
    assert backups.snapshot(root, t0, tag="vorher")["copied"] == []               # same content: no second copy
    assert backups.status(root)[0] == 2
    assert backups.saved(root, "rounds.jsonl")


def test_cleared_twice_a_day_the_rounds_since_the_first_copy_get_their_own(tmp_path):
    """1.46.4: "Alle Runden löschen" in the morning and again in the evening – the second copy was skipped (its
    name existed), the rounds played in between were gone."""
    root = str(tmp_path)
    t0 = time.time()
    for i in range(2, 12):
        (tmp_path / "rounds.jsonl").write_text(f"{i}\n")
        assert not backups.saved(root, "rounds.jsonl")
        backups.snapshot(root, t0, tag="vorher")
        assert backups.saved(root, "rounds.jsonl")
    names = backups.copies(str(tmp_path / backups.DIR), "rounds")
    day = _day(t0)
    assert names == [f"rounds-{day}-vorher.jsonl"] + [f"rounds-{day}-vorher{n}.jsonl" for n in range(2, 11)]
    assert (tmp_path / backups.DIR / names[-1]).read_text() == "11\n"           # numbers sort as numbers


def test_without_files_or_folder_nothing_happens(tmp_path):
    root = str(tmp_path)
    assert backups.snapshot(root) == {"copied": [], "pruned": [], "day": _day(time.time())}
    assert backups.status(root) == (0, "") and not (tmp_path / "backup").exists()
    (tmp_path / "backup").write_text("not a folder")                            # an unusable target: no crash
    (tmp_path / "rounds.jsonl").write_text("a\n")
    assert backups.snapshot(root)["copied"] == []


def test_everything_goes_into_one_zip_without_secrets_logs_or_links(tmp_path):
    """1.38.32 (project review F8): rounds, match data, the settings as exported (no secrets, no PC-specific
    values), own map pictures and the corpus; logs, caches and links stay out."""
    import json
    import zipfile
    from fogscout import backups
    d = tmp_path / "data"
    (d / "user_maps").mkdir(parents=True)
    (d / "corpus").mkdir()
    (d / "cache").mkdir()
    (d / "rounds.jsonl").write_text('{"t": 1}\n', encoding="utf-8")
    (d / "official.jsonl").write_text('{"t": 2}\n', encoding="utf-8")
    (d / "fogscout.log").write_text("log", encoding="utf-8")
    (d / "user_maps" / "a.webp").write_bytes(b"pic")
    (d / "corpus" / "20260101-000000-000.json").write_text("{}", encoding="utf-8")
    (d / "cache" / "x.bin").write_bytes(b"x")
    outside = tmp_path / "secret.txt"
    outside.write_text("nope", encoding="utf-8")
    try:
        os.symlink(str(outside), str(d / "user_maps" / "link.txt"))
    except (OSError, NotImplementedError):
        pass
    dest = tmp_path / "s.zip"
    n = backups.archive(str(d), str(dest), {"overlay": {"x": 1}, "claude_key": "dpapi:secret", "qt_geometry": "g"})
    with zipfile.ZipFile(dest) as z:
        names = sorted(z.namelist())
        cfg = json.loads(z.read("fogscout-einstellungen.json"))
    assert names == ["corpus/20260101-000000-000.json", "fogscout-einstellungen.json", "official.jsonl", "rounds.jsonl",
                     "user_maps/a.webp"] and n == 5
    assert cfg == {"overlay": {"x": 1}}


# ---------------------------------------------------------------- 1.38.42: back from the ZIP, merged
def _webp(colour=(10, 20, 30)) -> bytes:
    """A real little picture (1.38.57: map pictures from a ZIP are written only when PIL reads them)."""
    import io
    from PIL import Image
    buf = io.BytesIO()
    Image.new("RGB", (8, 8), colour).save(buf, "WEBP")
    return buf.getvalue()


def _data(folder, rounds=(), lost=(), matches=(), files=None):
    from fogscout import history, official
    os.makedirs(folder, exist_ok=True)
    for r in rounds:
        history.append(os.path.join(folder, history.FILE), r)
    for t, m in lost:
        history.append_lost(os.path.join(folder, history.FILE), t, m, "kein Ende")
    if matches:
        official.merge(os.path.join(folder, official.FILE), list(matches))
    for name, data in (files or {}).items():
        p = os.path.join(folder, *name.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(data)


def test_a_backup_is_merged_and_nothing_that_is_there_changes(tmp_path):
    """1.38.42 (user: "zusammenführen macht am meisten Sinn"): rounds, lost rounds and matches the backup has
    and the data folder not are added; a round in both stays as it is now (a later correction wins); files of
    user_maps/ and corpus/ are only added, never written over; the settings are handed back, not applied; a copy
    of the files goes to backup/ first."""
    import json
    import zipfile
    from fogscout import history, official
    R = history.Round
    old, now = str(tmp_path / "old"), str(tmp_path / "now")
    _data(old, rounds=[R(1000.0, 600, "coal", "Coal Tower", role="survivor"), R(2000.0, 600, "coal", "Coal Tower")],
          lost=[(3000.0, "Badham")], matches=[official.Match(t=962.0, map="Coal Tower"), official.Match(t=1962.0, map="X")],
          files={"user_maps/a.webp": _webp((1, 1, 1)), "user_maps/b.webp": _webp((2, 2, 2)), "corpus/c.json": b"{}"})
    _data(now, rounds=[R(2000.0, 600, "coal", "Coal Tower", role="killer"), R(5000.0, 300, "coal", "Coal Tower")],
          matches=[official.Match(t=1962.0, map="X")], files={"user_maps/a.webp": _webp((3, 3, 3))})
    zpath = str(tmp_path / "s.zip")
    backups.archive(old, zpath, {"overlay": {}, "hotkeys": {}})
    with zipfile.ZipFile(zpath, "a") as z:                       # what a crafted file could hold – never taken
        z.writestr("../evil.txt", b"x")
        z.writestr("user_maps/../../evil.txt", b"x")
        z.writestr("corpus/sub/deep.json", b"x")
        z.writestr("C:/evil.txt", b"x")
    assert backups.inspect(now, zpath) == {"rounds": 1, "lost": 1, "matches": 1, "files": 2, "known": 3,
                                          "settings": True}
    got = backups.restore(now, zpath, now=time.mktime((2026, 11, 6, 12, 0, 0, 0, 0, -1)))
    assert {k: v for k, v in got.items() if k != "settings"} == {"rounds": 1, "lost": 1, "matches": 1, "files": 2,
                                                                 "known": 3}
    assert json.loads(got["settings"]) == {"overlay": {}, "hotkeys": {}}
    rounds = history.load(os.path.join(now, history.FILE))
    assert [(r.t, r.role) for r in rounds] == [(1000.0, "survivor"), (2000.0, "killer"), (5000.0, "")]
    assert [t for t, _m, _r in history.load_lost(os.path.join(now, history.FILE))] == [3000.0]
    assert [m.t for m in official.load(os.path.join(now, official.FILE))] == [962.0, 1962.0]
    assert open(os.path.join(now, "user_maps", "a.webp"), "rb").read() == _webp((3, 3, 3))  # never written over
    assert open(os.path.join(now, "user_maps", "b.webp"), "rb").read() == _webp((2, 2, 2))
    assert os.path.isfile(os.path.join(now, "corpus", "c.json"))
    assert not (tmp_path / "evil.txt").exists() and not os.path.exists(os.path.join(now, "corpus", "sub"))
    assert backups.copies(os.path.join(now, backups.DIR), "rounds") == ["rounds-2026-11-06-restore.jsonl"]
    again = backups.restore(now, zpath)                          # a second time adds nothing
    assert (again["rounds"], again["lost"], again["matches"], again["files"]) == (0, 0, 0, 0)
    assert len(history.load(os.path.join(now, history.FILE))) == 3


def test_a_zip_that_is_no_backup_of_ours_is_refused(tmp_path):
    import zipfile
    import pytest
    for content in ({"readme.txt": b"hi"}, {"user_maps/a.webp": b"x"}):        # nothing of ours / pictures only
        p = str(tmp_path / "x.zip")
        with zipfile.ZipFile(p, "w") as z:
            for name, data in content.items():
                z.writestr(name, data)
        with pytest.raises(backups.NotOurs):
            backups.inspect(str(tmp_path), p)
    (tmp_path / "broken.zip").write_bytes(b"no zip")
    with pytest.raises(backups.NotOurs):
        backups.restore(str(tmp_path), str(tmp_path / "broken.zip"))


def test_device_names_odd_endings_and_foreign_kinds_are_never_taken():
    """1.38.57 (security review): Windows device names (any extension), names Windows cuts at the end, and kinds
    the program never stores there."""
    for name in ("user_maps/CON.webp", "user_maps/nul", "user_maps/Com1.png", "user_maps/LPT9 .jpg",
                 "corpus/aux.json", "user_maps/a.webp.", "user_maps/a.webp ", "user_maps/a.exe",
                 "user_maps/a.json", "corpus/a.png", "corpus/a.bat"):
        assert not backups._allowed(name), name
    for name in ("user_maps/coal-tower.webp", "user_maps/x.GIF", "corpus/20250101-000000-001.jpg",
                 "corpus/20250101-000000-001.json", "user_maps/console.png", "rounds.jsonl"):
        assert backups._allowed(name), name


def _zip(path, content, **kw):
    import zipfile
    with zipfile.ZipFile(path, "w", **kw) as z:
        for name, data in content.items():
            z.writestr(name, data)


def test_the_real_unpacked_bytes_count_and_unreadable_members_are_not_ours(tmp_path, monkeypatch):
    import zipfile
    import pytest
    p = str(tmp_path / "big.zip")
    _zip(p, {"rounds.jsonl": b"\n" * 1000, "official.jsonl": b"\n" * 1000, backups.SETTINGS_NAME: b"{}"},
         compression=zipfile.ZIP_DEFLATED)
    monkeypatch.setattr(backups, "MAX_TOTAL_BYTES", 1500)        # each member below the limit, together over it
    with pytest.raises(backups.NotOurs):
        backups.inspect(str(tmp_path / "data"), p)
    monkeypatch.undo()
    for err in (RuntimeError("encrypted"), NotImplementedError("compression"), zipfile.LargeZipFile("zip64")):
        def broken(self, *a, _e=err, **k):
            raise _e
        monkeypatch.setattr(zipfile.ZipFile, "open", broken)
        with pytest.raises(backups.NotOurs):
            backups.inspect(str(tmp_path / "data"), p)
        with pytest.raises(backups.NotOurs):
            backups.restore(str(tmp_path / "data"), p)
        monkeypatch.undo()


def test_a_map_picture_that_is_none_is_left_out(tmp_path):
    p = str(tmp_path / "s.zip")
    _zip(p, {backups.SETTINGS_NAME: b"{}", "user_maps/fake.webp": b"no picture", "user_maps/ok.webp": _webp()})
    data = str(tmp_path / "data")
    os.makedirs(data)
    got = backups.restore(data, p)
    assert got["files"] == 1 and os.listdir(os.path.join(data, "user_maps")) == ["ok.webp"]


def test_one_member_can_be_read_from_a_plain_zip(tmp_path):
    """1.38.57: the settings page reads the settings file from the archive on its own (a ZipFile, no counter)."""
    import zipfile
    path = tmp_path / "b.zip"
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(backups.SETTINGS_NAME, "{}")
    with zipfile.ZipFile(path) as z:
        assert backups._read(z, z.getinfo(backups.SETTINGS_NAME)) == b"{}"


def test_numbers_json_reads_as_nan_or_infinity_skip_the_line_instead_of_stopping_the_restore(tmp_path):
    """1.46.4: Python's json takes NaN/Infinity – round(nan) and int(inf) raised outside the skipped errors, the
    restore thread died without a word."""
    from fogscout import history, official
    good = '{"t": 1000.0, "seconds": 600, "map_id": "coal", "map": "Coal Tower"}'
    rounds = "\n".join([good, '{"t": NaN, "seconds": 600, "map_id": "coal"}',
                        '{"t": 1500.0, "seconds": Infinity, "map_id": "coal"}']) + "\n"
    matches = "\n".join(['{"t": NaN, "map": "x"}', '{"t": 1700000000, "bp": Infinity}',
                         '{"t": 962.0, "map": "Coal Tower"}']) + "\n"
    p = str(tmp_path / "s.zip")
    _zip(p, {"rounds.jsonl": rounds, "official.jsonl": matches})
    now = str(tmp_path / "now")
    os.makedirs(now)
    assert backups.inspect(now, p)["rounds"] == 1 and backups.inspect(now, p)["matches"] == 1
    got = backups.restore(now, p)
    assert (got["rounds"], got["matches"]) == (1, 1)
    assert [r.t for r in history.load(os.path.join(now, history.FILE))] == [1000.0]
    assert [m.t for m in official.load(os.path.join(now, official.FILE))] == [962.0]
