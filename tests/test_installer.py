"""1.32 (.exe, stage 4): the installer – tasks and shortcuts that start the .exe, --install-tasks/--remove-tasks, the
one-time takeover of a start.bat installation (copy only) and the Inno Setup script."""
import os
import re
import sys

import pytest

from fogscout import __main__ as entry
from fogscout import autostart, paths, takeover

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def installed_exe(tmp_path, monkeypatch):
    app = tmp_path / "Fog Scout & Co"
    app.mkdir()
    exe = app / "FogScout.exe"
    exe.write_bytes(b"MZ")
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(exe))
    return app, exe


def _checkout(folder, settings='{"ui_language": "en"}'):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "start.bat").write_text("@echo off\n", encoding="utf-8")
    (folder / "fogscout").mkdir(exist_ok=True)
    (folder / "settings.json").write_text(settings, encoding="utf-8")
    return folder


# ------------------------------------------------------------------ tasks and shortcuts start the .exe

def test_the_tasks_of_the_installed_program_start_the_exe_directly(installed_exe):
    app, exe = installed_exe
    assert autostart.frozen_exe() == str(exe) and autostart.app_root(ROOT) == str(app)
    on_demand = autostart.task_script(str(app), autostart.TASK, False, str(exe))
    logon = autostart.task_script(str(app), autostart.TASK_AUTO, True, str(exe))
    assert "-Execute " + autostart._q(str(exe)) in on_demand and "-Argument" not in on_demand
    assert "-Argument '--tray'" in logon and "-AtLogOn" in logon and "PT20S" in logon
    for script in (on_demand, logon):
        assert "cmd.exe" not in script and "start.bat" not in script and "-RunLevel Highest" in script
        assert "-WorkingDirectory " + autostart._q(str(app)) in script        # "&" in the folder: only a literal


def test_from_start_bat_the_tasks_stay_as_they_were():
    script = autostart.task_script(ROOT, autostart.TASK_AUTO, True)
    assert ".\\start.bat tray" in script and "cmd.exe" in script and autostart.app_root(ROOT) == ROOT


def test_install_points_tasks_and_shortcuts_at_the_exe(installed_exe, monkeypatch):
    app, exe = installed_exe
    scripts = []
    monkeypatch.setattr(autostart, "powershell", lambda s, timeout=60.0: scripts.append(s) or (True, "x.lnk"))
    monkeypatch.setattr(autostart, "set_link_app_id", lambda path: None)
    monkeypatch.setattr(autostart.icon_mod, "ensure_ico", lambda root: pytest.fail("no icon file in Program Files"))
    ok, _msg = autostart.install(os.path.join(str(app), "_internal"))
    assert ok
    task = next(s for s in scripts if "Register-ScheduledTask" in s)
    assert autostart._q(str(exe)) in task and autostart._q(str(app)) in task
    links = [s for s in scripts if "CreateShortcut" in s]
    assert len(links) == 2 and all(f"$s.IconLocation = {autostart._q(str(exe) + ',0')}" in s for s in links)
    assert all("schtasks.exe" in s for s in links)                 # the shortcut runs the task: no Windows prompt


def test_uninstall_removes_both_tasks_and_both_shortcuts():
    script = autostart.uninstall_script()
    assert script.count("Unregister-ScheduledTask") == 2
    assert autostart._q(autostart.TASK) in script and autostart._q(autostart.TASK_AUTO) in script
    assert "'Desktop'" in script and "'Programs'" in script and autostart._q(autostart.LINK_NAME) in script
    assert "Remove-Item" in script and "FogScout" not in script.replace("Fog Scout", "")    # no data folder


def test_installed_means_the_installer_left_its_uninstaller(installed_exe):
    app, _exe = installed_exe
    assert not paths.installed()
    (app / "unins000.exe").write_bytes(b"MZ")
    assert paths.installed()
    assert autostart.relaunch_command().endswith('schtasks.exe" /run /tn "Fog Scout"')


def test_install_tasks_notes_the_start_bat_folder_and_keeps_autostart_off(tmp_path, monkeypatch):
    old = _checkout(tmp_path / "old")
    data = tmp_path / "data"
    data.mkdir()
    (data / "settings.json").write_text('{"autostart": false}', encoding="utf-8")
    monkeypatch.setattr(entry, "_data", lambda: str(data))
    monkeypatch.setattr(takeover, "task_folder", lambda name: str(old) if name == autostart.TASK else None)
    calls = []
    monkeypatch.setattr(autostart, "install", lambda root: calls.append("install") or (True, ""))
    monkeypatch.setattr(autostart, "set_autostart", lambda root, on: calls.append(("auto", on)) or (True, ""))
    assert entry.install_tasks() == 0
    assert calls == ["install"]                                    # switched off before: stays off
    assert (data / takeover.SOURCE_FILE).read_text(encoding="utf-8") == str(old)
    (data / "settings.json").unlink()
    calls.clear()
    assert entry.install_tasks() == 0 and calls == ["install", ("auto", True)]     # a first install: on
    monkeypatch.setattr(autostart, "install", lambda root: (False, "no"))
    assert entry.install_tasks() == 1


def test_the_installer_entries_run_before_anything_else(monkeypatch):
    seen = []
    monkeypatch.setattr(entry, "install_tasks", lambda: seen.append("install") or 0)
    monkeypatch.setattr(entry, "remove_tasks", lambda: seen.append("remove") or 1)
    for arg, code in (("--install-tasks", 0), ("--remove-tasks", 1)):
        monkeypatch.setattr(sys, "argv", ["FogScout.exe", arg])
        with pytest.raises(SystemExit) as stop:
            entry.main()
        assert stop.value.code == code
    assert seen == ["install", "remove"]


# ------------------------------------------------------------------ takeover of a start.bat installation

def test_the_task_folder_survives_any_path():
    script = takeover.task_folder_script("Fog Scout")
    assert "Get-ScheduledTask -TaskName 'Fog Scout'" in script and "ToBase64String" in script
    import base64
    path = "C:\\Spiele & Tools\\O'Brien – Fog Scout"
    out = base64.b64encode(path.encode("utf-8")).decode()
    assert takeover.task_folder("Fog Scout", run=lambda s: (True, out + "\r\n")) == path
    assert takeover.task_folder("Fog Scout", run=lambda s: (True, "")) is None
    assert takeover.task_folder("Fog Scout", run=lambda s: (False, "boom")) is None
    assert takeover.task_folder("Fog Scout", run=lambda s: (True, "%%%")) is None


def test_only_a_real_start_bat_installation_is_offered_once(tmp_path):
    data = tmp_path / "data"
    assert not takeover.record(str(data), str(tmp_path / "nothing"))
    half = tmp_path / "half"
    half.mkdir()
    (half / "start.bat").write_text("", encoding="utf-8")
    assert not takeover.record(str(data), str(half))                     # no settings: nothing to take over
    old = _checkout(tmp_path / "old")
    assert takeover.record(str(data), str(old))
    assert takeover.pending(str(data)) == str(old)
    takeover.finish(str(data))
    assert takeover.pending(str(data)) is None and not (data / takeover.SOURCE_FILE).exists()
    assert not takeover.record(str(data), str(old))                       # asked once: never again


def test_no_offer_when_the_exe_already_has_settings(tmp_path):
    data = tmp_path / "data"
    old = _checkout(tmp_path / "old")
    takeover.record(str(data), str(old))
    (data / "settings.json").write_text("{}", encoding="utf-8")
    assert takeover.pending(str(data)) is None


def test_the_takeover_copies_and_never_changes_the_original(tmp_path):
    old = _checkout(tmp_path / "old")
    (old / "rounds.jsonl").write_text('{"map": "a"}\n', encoding="utf-8")
    (old / "official.jsonl").write_text("{}\n", encoding="utf-8")
    (old / "backup").mkdir()
    (old / "backup" / "rounds-2026-11-01.jsonl").write_text("x", encoding="utf-8")
    (old / "user_maps" / "Realm").mkdir(parents=True)
    (old / "user_maps" / "Realm" / "Own.webp").write_bytes(b"RIFF")
    for skip in ("fogscout.log", "diagnose.txt"):
        (old / skip).write_text("no", encoding="utf-8")
    (old / "cache").mkdir()
    (old / "cache" / "big.webp").write_bytes(b"x")
    before = {p: p.read_bytes() for p in old.rglob("*") if p.is_file()}
    data = tmp_path / "data"
    data.mkdir()
    (data / "rounds.jsonl").write_text("mine\n", encoding="utf-8")           # never overwritten
    done = takeover.copy(str(old), str(data))
    assert done == ["settings.json", "official.jsonl", "backup/", "user_maps/"]
    assert (data / "rounds.jsonl").read_text(encoding="utf-8") == "mine\n"
    assert (data / "user_maps" / "Realm" / "Own.webp").read_bytes() == b"RIFF"
    assert not (data / "cache").exists() and not (data / "fogscout.log").exists()
    assert {p: p.read_bytes() for p in old.rglob("*") if p.is_file()} == before


def test_the_first_start_asks_once_and_takes_over_on_yes(tmp_path):
    old = _checkout(tmp_path / "old")
    data = tmp_path / "data"
    takeover.record(str(data), str(old))
    questions = []
    assert entry.offer_takeover(str(data), ask=lambda text: questions.append(text) or True) == ["settings.json"]
    assert str(old) in questions[0] and "unverändert" in questions[0]
    assert (data / "settings.json").read_text(encoding="utf-8") == '{"ui_language": "en"}'
    assert entry.offer_takeover(str(data), ask=lambda text: pytest.fail("asked twice")) == []


def test_no_means_no_and_is_not_asked_again(tmp_path):
    old = _checkout(tmp_path / "old")
    data = tmp_path / "data"
    takeover.record(str(data), str(old))
    assert entry.offer_takeover(str(data), ask=lambda text: False) == []
    assert not (data / "settings.json").exists() and (data / takeover.MARKER).exists()
    assert entry.offer_takeover(str(data), ask=lambda text: pytest.fail("asked twice")) == []


# ------------------------------------------------------------------ the Inno Setup script and its CI check

def _iss():
    with open(os.path.join(ROOT, "installer", "fogscout.iss"), encoding="utf-8") as fh:
        return fh.read()


def test_the_installer_goes_to_program_files_for_everyone_and_keeps_the_data():
    iss = _iss()
    assert "DefaultDirName={autopf}\\Fog Scout" in iss and "PrivilegesRequired=admin" in iss
    assert re.search(r"^AppId=\{\{[0-9A-F-]{36}\}$", iss, re.M)              # never change: upgrades find it
    assert "AppMutex=Local\\FogScout.SingleInstance" in iss
    from fogscout import restart
    assert restart.MUTEX_NAME == "Local\\FogScout.SingleInstance"
    assert 'Parameters: "--install-tasks"' in iss and 'Parameters: "--remove-tasks"' in iss
    assert "skipifsilent" in iss and '/run /tn ""Fog Scout""' in iss          # first start through the task
    assert "{localappdata}" not in iss.lower() and "[UninstallDelete]" not in iss   # the data folder stays
    assert 'Name: "{app}\\_internal"' in iss and "Type: filesandordirs" in iss
    assert "..\\build\\fogscout\\fogscout.ico" in iss                          # written by the spec (workpath)


def test_ci_builds_installs_checks_and_uninstalls_the_setup():
    with open(os.path.join(ROOT, ".github", "workflows", "build.yml"), encoding="utf-8") as fh:
        wf = fh.read()
    assert re.search(r"INNO_SHA256: [0-9a-f]{64}", wf) and "Get-FileHash -Algorithm SHA256" in wf
    assert "github.com/jrsoftware/issrc/releases/download/" in wf
    assert "installer\\fogscout.iss" in wf and "/DAppVersion=" in wf
    for check in ('Get-ScheduledTask -TaskName "Fog Scout"', '"--tray"', '"Highest"', "Fog Scout.lnk",
                  "selftest-installed.json", "unins000.exe", "nach der Deinstallation"):
        assert check in wf, check
    assert "FogScout-Setup-${{ github.sha }}" in wf
