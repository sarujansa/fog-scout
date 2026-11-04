"""1.33.5 (review S2/S4/S5/S6): Fog Scout runs elevated through its task, so a normal program of the same user must
not be able to steer what it deletes, writes, starts or loads – no links out of the recordings folder, no result
file that is really another file, no Windows folder or program taken from the environment or found through PATH."""
import ast
import os
import pathlib
import re
import sys

import pytest

from fogscout import fsops, hostsedit, netwatch, obsrec, paths

PKG = pathlib.Path(__file__).resolve().parent.parent / "fogscout"
posix_links = pytest.mark.skipif(sys.platform == "win32", reason="symlinks need a privilege on Windows; "
                                                                  "the Windows path is covered in test_windows.py")


# ---- S2: deleting only inside the folder
def test_a_plain_file_inside_is_deleted(tmp_path):
    (tmp_path / "Farming").mkdir()
    f = tmp_path / "Farming" / "a.mp4"
    f.write_bytes(b"x")
    fsops.delete_inside(str(tmp_path), str(f))
    assert not f.exists()
    with pytest.raises(FileNotFoundError):                      # like os.remove
        fsops.delete_inside(str(tmp_path), str(f))


def test_nothing_outside_the_folder_is_deleted(tmp_path):
    rec, other = tmp_path / "rec", tmp_path / "other"
    rec.mkdir()
    other.mkdir()
    victim = other / "important.dll"
    victim.write_bytes(b"x")
    for path in (str(victim), str(rec / ".." / "other" / "important.dll"), str(rec)):
        with pytest.raises(fsops.NotInside):
            fsops.delete_inside(str(rec), path)
    assert victim.exists()


@posix_links
def test_a_link_in_the_path_is_never_followed(tmp_path):
    """The attack: a junction "x" → C:\\Windows\\System32 inside the recordings folder and an index line "x/<file>"."""
    rec, system = tmp_path / "rec", tmp_path / "system32"
    rec.mkdir()
    system.mkdir()
    victim = system / "kernel.dll"
    victim.write_bytes(b"x")
    (rec / "x").symlink_to(system, target_is_directory=True)
    (rec / "link.mp4").symlink_to(victim)
    for path in (rec / "x" / "kernel.dll", rec / "link.mp4"):
        with pytest.raises(fsops.NotInside):
            fsops.delete_inside(str(rec), str(path))
    assert victim.exists() and (rec / "link.mp4").is_symlink()


@posix_links
def test_farming_cleanup_does_not_delete_through_a_linked_folder(tmp_path):
    rec, system = tmp_path / "rec", tmp_path / "system32"
    rec.mkdir()
    system.mkdir()
    victim = system / "kernel.dll"
    victim.write_bytes(b"x")
    (rec / "Farming").symlink_to(system, target_is_directory=True)
    entry = obsrec.Recording(file="Farming/kernel.dll", t=0.0, farming=True)
    left, deleted = obsrec.prune_farming(str(rec), [entry], days=1, now=10 * 86400)
    assert victim.exists() and deleted == []


# ---- S6: the helpers' result files
WRITERS = [fsops.open_plain_for_write, hostsedit._open_result, netwatch._open_result]


@pytest.mark.parametrize("opener", WRITERS)
def test_a_plain_result_file_is_written_in_place(opener, tmp_path):
    f = tmp_path / "result.json"
    f.write_text("old and longer", encoding="utf-8")
    with opener(str(f)) as fh:
        fh.write("{}")
    assert f.read_text(encoding="utf-8") == "{}"
    with pytest.raises(FileNotFoundError):                       # never created again
        opener(str(tmp_path / "gone.json"))


@posix_links
@pytest.mark.parametrize("opener", WRITERS)
def test_a_result_file_that_is_really_another_file_is_not_written(opener, tmp_path):
    victim = tmp_path / "hosts"
    victim.write_text("keep", encoding="utf-8")
    (tmp_path / "link.json").symlink_to(victim)
    os.link(victim, tmp_path / "hard.json")
    for name in ("link.json", "hard.json"):
        with pytest.raises(OSError):
            opener(str(tmp_path / name))
    assert victim.read_text(encoding="utf-8") == "keep"


def test_the_helpers_write_their_results_through_the_check(tmp_path):
    res = tmp_path / "res.json"
    res.write_text("", encoding="utf-8")
    netwatch.write(str(res), {"ok": True})
    assert res.read_text(encoding="utf-8") == '{"ok": true}'
    src = (PKG / "hostsedit.py").read_text(encoding="utf-8")
    assert "with _open_result(argv[2]) as fh:" in src


# ---- S4/S5: Windows' own folders and programs
def test_windows_folders_come_from_windows_not_the_environment(monkeypatch):
    monkeypatch.setenv("SystemRoot", "/tmp/evil")
    monkeypatch.setenv("ProgramFiles", "/tmp/evil")
    monkeypatch.setenv("COMSPEC", "/tmp/evil/cmd.exe")
    assert "evil" not in paths.system_dir() and "evil" not in paths.windows_dir()
    assert "evil" not in paths.system_exe("cmd.exe") and paths.system_exe("cmd.exe").endswith("cmd.exe")
    assert "evil" not in hostsedit.system_dir()
    if sys.platform != "win32":                              # on Windows the tests never touch the real hosts file
        monkeypatch.delenv("DBDMS_HOSTS_FILE", raising=False)
        assert "evil" not in hostsedit.hosts_path()
    from fogscout import autostart, restart
    assert "evil" not in restart.start_command() and "evil" not in autostart.relaunch_command()
    assert "evil" not in autostart.task_script(os.getcwd(), "Fog Scout", False)
    assert "evil" not in autostart.shortcut_script(os.getcwd(), "")
    if sys.platform != "win32":
        assert paths.known_folder("ProgramFiles") == "" and paths.known_folder("nope") == ""


ENV_NAMES = ("SystemRoot", "windir", "ProgramFiles", "ProgramW6432", "COMSPEC", "ProgramData")


def test_no_module_takes_a_windows_folder_from_the_environment():
    bad = []
    for f in sorted(PKG.glob("*.py")):
        text = f.read_text(encoding="utf-8")
        for name in ENV_NAMES:
            for m in re.finditer(r'environ(?:\.get)?[\[(]\s*"' + name + '"', text):
                bad.append(f"{f.name}:{text[:m.start()].count(chr(10)) + 1} {name}")
            if "$env:" + name in text:
                bad.append(f"{f.name} $env:{name}")
    assert bad == []


BARE_OK = {("update.py", "git")}          # start.bat mode only: git comes from the user's PATH on purpose


def test_programs_are_started_by_their_full_path():
    """subprocess with a bare program name searches the current folder and PATH – as administrator."""
    bad = []
    for f in sorted(PKG.glob("*.py")):
        tree = ast.parse(f.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess"
                    and node.args and isinstance(node.args[0], ast.List) and node.args[0].elts):
                continue
            first = node.args[0].elts[0]
            if isinstance(first, ast.Constant) and isinstance(first.value, str) \
                    and (f.name, first.value) not in BARE_OK:
                bad.append(f"{f.name}:{node.lineno} {first.value}")
    assert bad == []
