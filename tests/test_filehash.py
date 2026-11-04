"""1.18.1: filehash – the identity of a recording (quick fingerprint for preselection, full SHA-256 as proof), its
cache by file id, the hasher thread (cancel, pause, a file that changes while read, cloud placeholders)."""
import hashlib
import os
import sys
import threading
import types

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import filehash  # noqa: E402


def _file(path, size=3 << 20):
    data = os.urandom(size)
    path.write_bytes(data)
    return data


def test_full_hash_is_the_sha256_of_the_whole_file_and_reports_progress(tmp_path, monkeypatch):
    monkeypatch.setattr(filehash, "PROGRESS_EVERY", 1 << 20)
    monkeypatch.setattr(filehash, "CHUNK", 256 << 10)
    data = _file(tmp_path / "r.mkv", (5 << 20) + 123)
    seen = []
    sha, st = filehash.full_sha256(str(tmp_path / "r.mkv"), progress=lambda d, t: seen.append((d, t)))
    assert sha == hashlib.sha256(data).hexdigest() and st.st_size == len(data)
    assert seen == sorted(seen) and seen[-1] == (len(data), len(data)) and len(seen) >= 5


def test_qfp_sees_only_the_ends_and_the_full_hash_sees_the_middle(tmp_path):
    data = bytearray(_file(tmp_path / "a.mkv", 6 << 20))
    data[3 << 20] ^= 1
    (tmp_path / "b.mkv").write_bytes(bytes(data))
    a, b = str(tmp_path / "a.mkv"), str(tmp_path / "b.mkv")
    assert filehash.qfp(a) == filehash.qfp(b)
    assert filehash.full_sha256(a)[0] != filehash.full_sha256(b)[0]


def test_a_file_that_changes_while_it_is_read_gives_no_hash(tmp_path, monkeypatch):
    path = tmp_path / "growing.mkv"
    _file(path)
    monkeypatch.setattr(filehash, "CHUNK", 1 << 20)
    real = filehash.full_sha256

    def grow(p, cancel=None, progress=None, paused=None):
        def prog(done, total):
            with open(p, "ab") as fh:
                fh.write(b"more")
        return real(p, cancel, prog, paused)
    monkeypatch.setattr(filehash, "PROGRESS_EVERY", 1 << 20)
    monkeypatch.setattr(filehash, "full_sha256", grow)
    h = filehash.Hasher(filehash.Cache(str(tmp_path / "c")), retry_s=0)
    assert h.hash_now(str(path))["kind"] == "changed"
    assert h.cache.get(os.stat(path)) is None                                  # nothing cached for it


def test_cancel_and_pause(tmp_path, monkeypatch):
    path = tmp_path / "r.mkv"
    _file(path)
    cancel = threading.Event()
    cancel.set()
    with pytest.raises(filehash.Cancelled):
        filehash.full_sha256(str(path), cancel)
    calls = []

    def paused():
        calls.append(1)
        return len(calls) < 3                                                  # paused for two looks, then free
    monkeypatch.setattr(filehash, "PAUSE_POLL_S", 0)
    sha, _st = filehash.full_sha256(str(path), threading.Event(), paused=paused)
    assert sha == hashlib.sha256(path.read_bytes()).hexdigest() and len(calls) >= 3


def test_the_cache_survives_a_rename_and_forgets_a_changed_file(tmp_path):
    path = tmp_path / "r.mkv"
    _file(path)
    cache = filehash.Cache(str(tmp_path / "c"))
    h = filehash.Hasher(cache, retry_s=0)
    first = h.hash_now(str(path))
    assert first["kind"] == "done" and not first["cached"]
    moved = tmp_path / "renamed.mkv"
    os.rename(path, moved)
    again = filehash.Hasher(filehash.Cache(str(tmp_path / "c")), retry_s=0).hash_now(str(moved))   # cache from disk
    assert again["kind"] == "done" and again["cached"] and again["sha256"] == first["sha256"]
    with open(moved, "ab") as fh:
        fh.write(b"x")
    third = h.hash_now(str(moved))
    assert not third["cached"] and third["sha256"] != first["sha256"]


def test_a_broken_cache_file_is_an_empty_cache(tmp_path):
    folder = tmp_path / "c"
    folder.mkdir()
    (folder / filehash.CACHE_FILE).write_text("{broken", encoding="utf-8")
    assert filehash.Cache(str(folder)).get(types.SimpleNamespace(st_dev=1, st_ino=2, st_size=3, st_mtime_ns=4)) is None


def test_cloud_placeholders_are_not_hashed_by_themselves(tmp_path, monkeypatch):
    path = tmp_path / "online-only.mkv"
    _file(path, 1000)
    real = os.stat

    def stat(p, *a, **k):
        st = real(p, *a, **k)
        if str(p) == str(path):
            return types.SimpleNamespace(**{n: getattr(st, n) for n in ("st_size", "st_mtime_ns", "st_dev", "st_ino")},
                                         st_file_attributes=0x400000)
        return st
    monkeypatch.setattr(filehash.os, "stat", stat)
    h = filehash.Hasher(filehash.Cache(str(tmp_path / "c")), retry_s=0)
    assert h.hash_now(str(path))["kind"] == "placeholder"
    monkeypatch.setattr(filehash.os, "stat", real)
    assert h.hash_now(str(path), allow_placeholder=True)["kind"] == "done"


def test_an_unreadable_file_is_an_error_not_a_hash(tmp_path):
    h = filehash.Hasher(filehash.Cache(str(tmp_path / "c")), retry_s=0)
    assert h.hash_now(str(tmp_path / "missing.mkv"))["kind"] == "error"


def test_the_thread_delivers_results_and_survives_a_bad_callback(tmp_path):
    path = tmp_path / "r.mkv"
    _file(path, 100_000)
    h = filehash.Hasher(filehash.Cache(str(tmp_path / "c")), retry_s=0)
    h.start()
    got = []
    done = threading.Event()
    try:
        h.request(str(path), lambda r: (_ for _ in ()).throw(RuntimeError("bad")))
        h.request(str(path), lambda r: (got.append(r), done.set()))
        assert done.wait(30) and got[0]["kind"] == "done"
    finally:
        h.stop()


def test_a_failing_answer_is_logged_and_the_next_waiter_still_gets_its_own(tmp_path, caplog):
    """1.34.2 (review W1): a window's callback that raises was swallowed without a trace – now it is in the log, and
    the other window waiting for the same file still gets the hash."""
    path = tmp_path / "r.mkv"
    _file(path, 4096)
    h = filehash.Hasher(filehash.Cache(str(tmp_path / "c")), retry_s=0)
    got = threading.Event()
    answers = []

    def broken(result):
        raise RuntimeError("window already closed")

    h.request(str(path), broken)
    h.request(str(path), lambda r: (answers.append(r), got.set()))
    with caplog.at_level("ERROR", logger="fogscout.filehash"):
        h.start()
        try:
            assert got.wait(30)
        finally:
            h.stop()
            h.join(10)
    assert answers[0]["kind"] == "ok" or answers[0].get("sha256")
    assert any("Hash fertig" in r.getMessage() and r.exc_info for r in caplog.records)
