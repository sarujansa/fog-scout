"""1.18.1: fsops (the file primitives of project saving – nothing is ever replaced) and paths (the per-user data
folder). Linux runs the POSIX path, the Windows job the handle path; both check the same promises."""
import ast
import errno
import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import fsops, paths  # noqa: E402

WIN = sys.platform == "win32"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _write(path, data=b"x"):
    with open(path, "wb") as fh:
        fh.write(data)


def _read(path):
    with open(path, "rb") as fh:
        return fh.read()


def test_create_exclusive_refuses_an_existing_target(tmp_path):
    src, dst = str(tmp_path / "a.tmp"), str(tmp_path / "b.json")
    _write(src, b"ours")
    _write(dst, b"foreign")
    with pytest.raises(FileExistsError):
        fsops.create_exclusive(src, dst)
    assert _read(dst) == b"foreign" and _read(src) == b"ours"
    os.remove(dst)
    fsops.create_exclusive(src, dst)
    assert _read(dst) == b"ours" and not os.path.exists(src)


def test_write_new_is_complete_or_nothing_and_never_over_a_file(tmp_path):
    dst = str(tmp_path / "p.json")
    fsops.write_new(dst, b"first")
    with pytest.raises(FileExistsError):
        fsops.write_new(dst, b"second")
    assert _read(dst) == b"first"
    assert [n for n in os.listdir(tmp_path) if n.endswith(".tmp")] == []          # no temp file left behind


@pytest.mark.skipif(WIN, reason="the POSIX path")
def test_no_fallback_when_the_file_system_refuses(tmp_path, monkeypatch):
    """renameat2 missing or refused (EINVAL/ENOSYS) → UnsupportedFS, nothing renamed, and no other call (replace,
    rename, link, shutil) is tried."""
    import shutil
    calls = []
    for mod, name in ((os, "replace"), (os, "rename"), (os, "link"), (shutil, "move"), (shutil, "copyfile")):
        monkeypatch.setattr(mod, name, lambda *a, _n=name, **k: calls.append(_n))
    src, dst = str(tmp_path / "a.tmp"), str(tmp_path / "b.json")
    _write(src, b"ours")
    for code in (errno.EINVAL, errno.ENOSYS):
        def refuse(*a, _c=code):
            import ctypes
            ctypes.set_errno(_c)
            return -1
        monkeypatch.setattr(fsops, "_RENAMEAT2", [refuse])
        with pytest.raises(fsops.UnsupportedFS):
            fsops.create_exclusive(src, dst)
    monkeypatch.setattr(fsops, "_RENAMEAT2", [None])                               # glibc without renameat2
    with pytest.raises(fsops.UnsupportedFS):
        fsops.create_exclusive(src, dst)
    assert calls == [] and not os.path.exists(dst) and _read(src) == b"ours"


def test_an_unknown_platform_fails_safely(tmp_path, monkeypatch):
    monkeypatch.setattr(fsops, "WIN", False)
    monkeypatch.setattr(fsops, "LINUX", False)
    src = str(tmp_path / "a.tmp")
    _write(src)
    with pytest.raises(fsops.UnsupportedFS):
        fsops.create_exclusive(src, str(tmp_path / "b.json"))
    assert not os.path.exists(tmp_path / "b.json")


_RACE = r"""
import os, sys, time
sys.path.insert(0, sys.argv[1])
from fogscout import fsops
src, dst, go = sys.argv[2], sys.argv[3], sys.argv[4]
while not os.path.exists(go):
    time.sleep(0.001)
try:
    fsops.create_exclusive(src, dst)
    print("won")
except FileExistsError:
    print("lost")
"""


def test_two_processes_creating_the_same_file_exactly_one_wins(tmp_path):
    for round_ in range(20):
        d = tmp_path / str(round_)
        d.mkdir()
        dst, go = str(d / "p.json"), str(d / "go")
        procs = []
        for who in (b"one", b"two"):
            src = str(d / (who.decode() + ".tmp"))
            _write(src, who)
            procs.append(subprocess.Popen([sys.executable, "-c", _RACE, ROOT, src, dst, go], stdout=subprocess.PIPE,
                                          text=True))
        _write(go)
        outs = sorted(p.communicate(timeout=60)[0].strip() for p in procs)
        assert outs == ["lost", "won"], outs
        winner = b"one" if not os.path.exists(d / "one.tmp") else b"two"
        assert _read(dst) == winner                                               # the loser's file is untouched
        assert os.path.exists(d / ((b"two" if winner == b"one" else b"one").decode() + ".tmp"))


def test_the_exclusive_handle_reads_renames_and_never_replaces(tmp_path):
    a, b, c = str(tmp_path / "a.json"), str(tmp_path / "b.json"), tmp_path / "Sicherungen" / "c.json"
    _write(a, b"content")
    _write(b, b"foreign")
    c.parent.mkdir()
    with fsops.ExclusiveHandle(a) as h:
        assert h.read() == b"content"
        with pytest.raises(FileExistsError):
            h.rename_to(b)
        assert _read(b) == b"foreign"
        h.rename_to(str(c))                                                       # into a sub-folder (W23)
        assert h.read() == b"content"                                             # still the same file
    assert not os.path.exists(a) and _read(str(c)) == b"content"


def test_delete_verified_deletes_only_the_expected_content(tmp_path):
    a = str(tmp_path / "a.json")
    _write(a, b"kept")
    assert fsops.delete_verified(a, fsops.sha256_bytes(b"other"), 4) is False       # same size, other content
    assert fsops.delete_verified(a, fsops.sha256_bytes(b"kept"), 5) is False        # wrong size
    assert _read(a) == b"kept"
    assert fsops.delete_verified(a, fsops.sha256_bytes(b"kept"), 4) is True
    assert not os.path.exists(a)
    with pytest.raises(FileNotFoundError):
        fsops.delete_verified(a, fsops.sha256_bytes(b"kept"), 4)


_OPEN_TRY = r"""
import ctypes, sys
from ctypes import wintypes
k = ctypes.WinDLL("kernel32", use_last_error=True)
k.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD,
                          wintypes.DWORD, wintypes.HANDLE]
k.CreateFileW.restype = wintypes.HANDLE
h = k.CreateFileW(sys.argv[1], 0x40000000, 7, None, 3, 0x80, None)
print("blocked" if h is None or h in (-1, 2 ** 64 - 1, 2 ** 32 - 1) else "opened")
"""


@pytest.mark.skipif(not WIN, reason="Windows share modes")
def test_windows_nobody_can_open_the_file_between_the_check_and_the_rename(tmp_path):
    """While ExclusiveHandle holds the file – after reading it, before renaming – another process asking for write
    access with every share flag is refused; after the rename, too, until the handle closes."""
    a, b = str(tmp_path / "a.json"), str(tmp_path / "b.json")
    _write(a, b"content")
    with fsops.ExclusiveHandle(a) as h:
        assert h.read() == b"content"
        res = subprocess.run([sys.executable, "-c", _OPEN_TRY, a], capture_output=True, text=True, timeout=60)
        assert res.stdout.strip() == "blocked", res.stderr
        h.rename_to(b)
        res = subprocess.run([sys.executable, "-c", _OPEN_TRY, b], capture_output=True, text=True, timeout=60)
        assert res.stdout.strip() == "blocked", res.stderr
    res = subprocess.run([sys.executable, "-c", _OPEN_TRY, b], capture_output=True, text=True, timeout=60)
    assert res.stdout.strip() == "opened"


@pytest.mark.skipif(not WIN, reason="Windows share modes")
def test_windows_the_handle_cannot_be_had_while_another_program_has_the_file_open(tmp_path):
    a = str(tmp_path / "a.json")
    _write(a, b"content")
    with open(a, "rb"):
        with pytest.raises(PermissionError):
            fsops.ExclusiveHandle(a)
    fsops.ExclusiveHandle(a).close()


# ---- the guard: only these primitives touch names
ALLOWED = {                       # (module, function) → calls it may make
    ("fsops", "create_exclusive"): {"os.rename"},
    ("fsops", "rename_fallback"): {"os.rename"},
    ("fsops", "discard_tmp"): {"os.remove"},
    ("fsops", "delete_inside"): {"os.remove"},   # 1.33.5: POSIX, after every part below the folder was checked
    ("fsops", "delete"): {"os.unlink"},
    ("filehash", "_save_cache"): {"os.replace"},
    ("fsops", "write_atomic"): {"os.replace"},   # 1.34.2: the one replacing write (settings backup, format 1)
}
WATCHED = {"os.rename", "os.replace", "os.remove", "os.unlink", "os.link", "shutil.move", "shutil.copyfile",
           "shutil.copy", "shutil.copy2", "shutil.rmtree", "os.renames", "os.removedirs"}
MODULES = ("fsops", "paths", "project", "filehash", "projectsave")


def test_filesystem_calls_are_only_the_allowed_primitives():
    """1.18.1 (plan 3.7): in the modules of project saving, renaming/replacing/removing happens only in the reviewed
    primitives – os.replace only for the hash cache, no shutil anywhere."""
    found = []
    for mod in MODULES:
        path = os.path.join(ROOT, "fogscout", mod + ".py")
        if not os.path.exists(path):
            continue
        tree = ast.parse(open(path, encoding="utf-8").read())

        def visit(node, func):
            for child in ast.iter_child_nodes(node):
                f = child.name if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) else func
                if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute) \
                        and isinstance(child.func.value, ast.Name):
                    name = f"{child.func.value.id}.{child.func.attr}"
                    if name in WATCHED and name not in ALLOWED.get((mod, func), set()):
                        found.append((mod, func, name, child.lineno))
                visit(child, f)
        visit(tree, None)
    assert found == []


# ---- paths
def test_the_data_folder_is_the_test_folder_and_its_files_are_made_once(tmp_path, monkeypatch):
    monkeypatch.setenv(paths.ENV, str(tmp_path / "data"))
    assert paths.user_data_dir() == str(tmp_path / "data")
    wid = paths.writer_id()
    assert wid and len(wid) == 32 and paths.writer_id() == wid
    key = paths.backup_key()
    assert key and len(key) == 32 and paths.backup_key() == key


def test_a_broken_key_file_is_never_rewritten(tmp_path, monkeypatch):
    monkeypatch.setenv(paths.ENV, str(tmp_path))
    _write(str(tmp_path / paths.KEY_FILE), b"short")
    assert paths.backup_key() is None
    assert _read(str(tmp_path / paths.KEY_FILE)) == b"short"


def test_without_a_user_location_there_is_none_never_the_program_folder(monkeypatch):
    monkeypatch.delenv(paths.ENV, raising=False)
    monkeypatch.delenv("LOCALAPPDATA", raising=False)
    monkeypatch.setattr(paths, "_qt_location", lambda: "")
    assert paths.user_data_dir() is None and paths.ensure() is None
    monkeypatch.setenv("LOCALAPPDATA", os.path.join(os.sep, "users", "x", "AppData", "Local"))
    assert paths.user_data_dir() == os.path.join(os.sep, "users", "x", "AppData", "Local", "FogScout")


def test_an_unwritable_data_folder_reports_none(tmp_path, monkeypatch):
    blocker = tmp_path / "file"
    _write(str(blocker))
    monkeypatch.setenv(paths.ENV, str(blocker / "below-a-file"))
    assert paths.ensure() is None and paths.writer_id() is None


def test_the_one_replacing_write_is_whole_or_nothing(tmp_path, monkeypatch):
    """1.34.2 (review W8): the settings backup and a format-1 project were written to "<name>.tmp" without fsync, and
    a value json could not write left that .tmp behind – now one write_atomic: fsync'ed temp file, one replace."""
    from fogscout import config, project
    target = tmp_path / "f.json"
    fsops.write_atomic(str(target), b"one")
    fsops.write_atomic(str(target), b"two")
    assert target.read_bytes() == b"two" and os.listdir(tmp_path) == ["f.json"]

    def broken(src, dst):
        raise PermissionError(13, "locked")
    monkeypatch.setattr(fsops.os, "replace", broken)
    with pytest.raises(PermissionError):
        fsops.write_atomic(str(target), b"three")
    assert target.read_bytes() == b"two" and os.listdir(tmp_path) == ["f.json"]   # old file kept, no temp left
    monkeypatch.undo()
    proj = tmp_path / "Projekte" / "a.fogscout-project.json"
    assert project.save(str(proj), {"v": 1}) and json.loads(proj.read_text(encoding="utf-8")) == {"v": 1}
    assert not project.save(str(proj), {"v": object()})                  # not writable as json: nothing left over
    assert os.listdir(proj.parent) == [proj.name] and json.loads(proj.read_text(encoding="utf-8")) == {"v": 1}
    backup = tmp_path / "backup.json"
    config.export_settings({"ui_language": "de", "rec_password": "secret"}, str(backup))
    assert json.loads(backup.read_text(encoding="utf-8")) == {"ui_language": "de"}
    assert sorted(os.listdir(tmp_path)) == ["Projekte", "backup.json", "f.json"]
