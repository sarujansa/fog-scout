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
    assert backups.snapshot(root, t0, tag="vorher")["copied"] == []               # the same tag once a day too
    assert backups.status(root)[0] == 2


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
          files={"user_maps/a.webp": b"OLD", "user_maps/b.webp": b"B", "corpus/c.json": b"{}"})
    _data(now, rounds=[R(2000.0, 600, "coal", "Coal Tower", role="killer"), R(5000.0, 300, "coal", "Coal Tower")],
          matches=[official.Match(t=1962.0, map="X")], files={"user_maps/a.webp": b"NEW"})
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
    assert open(os.path.join(now, "user_maps", "a.webp"), "rb").read() == b"NEW"         # never written over
    assert open(os.path.join(now, "user_maps", "b.webp"), "rb").read() == b"B"
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
