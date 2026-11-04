"""1.31 (.exe, stage 3): the packaged program (PyInstaller, ``sys.frozen``) is its own elevated helper, restarts its
own .exe, sets up no start.bat tasks and runs a self-check; the build is pinned and checked in CI."""
import json
import os
import re
import sys

import pytest

from fogscout import __main__ as entry
from fogscout import autostart, regions, restart, selftest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = r"C:\Program Files\Fog Scout\FogScout.exe"


@pytest.fixture
def packaged(monkeypatch):
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", EXE)


def test_from_start_bat_the_helpers_stay_isolated_scripts():
    exe, params = regions.helper_command("hostsedit", [r"C:\T\job.json", r"C:\T\res.json"])
    assert exe == regions._python_exe()
    script = os.path.join(ROOT, "fogscout", "hostsedit.py")
    assert params == f'-I -S "{script}" "C:\\T\\job.json" "C:\\T\\res.json"'
    assert os.path.isfile(script) and os.path.isfile(os.path.join(ROOT, "fogscout", "netwatch.py"))


def test_the_packaged_program_is_its_own_helper(packaged):
    assert regions.helper_command("netwatch", ["a b.json", "c.json"]) == (EXE, '--helper netwatch "a b.json" "c.json"')
    assert regions.helper_command("hostsedit", ["j", "r"]) == (EXE, '--helper hostsedit "j" "r"')
    with pytest.raises(ValueError):
        regions.helper_command("cmd", ["x"])                 # only the two helpers, never anything else


def test_the_helper_entry_runs_only_the_two_helpers(monkeypatch):
    assert entry.HELPER_MODULES == regions.HELPERS
    assert entry.run_helper([]) == 2 and entry.run_helper(["update"]) == 2 and entry.run_helper(["../x"]) == 2
    assert entry.run_helper(["hostsedit"]) == 2                # wrong argument count: usage, nothing written
    assert entry.run_helper(["netwatch", "a"]) == 2
    monkeypatch.setattr(sys, "argv", ["FogScout.exe", "--helper", "hostsedit"])
    with pytest.raises(SystemExit) as stop:                    # before argparse, the mutex, the log and the window
        entry.main()
    assert stop.value.code == 2


def test_the_helper_entry_writes_the_hosts_file_like_the_script(tmp_path, monkeypatch):
    if sys.platform == "win32":
        pytest.skip("tests never touch the real hosts file (hosts_path ignores the test variable on Windows)")
    from fogscout import hostsedit
    hosts = tmp_path / "hosts"
    hosts.write_text("127.0.0.1 localhost\n", encoding="latin-1")
    monkeypatch.setenv("DBDMS_HOSTS_FILE", str(hosts))
    monkeypatch.setattr(hostsedit, "flush_dns", lambda: False)
    name = hostsedit.MANAGED[0]
    job, res = tmp_path / "job.json", tmp_path / "res.json"
    job.write_text(json.dumps({"block": [name]}), encoding="utf-8")
    res.write_text("", encoding="utf-8")       # made by the normal program first (regions.run_job); 1.33.5: the
    #                                            elevated helper only writes a plain file that is already there
    assert entry.run_helper(["hostsedit", str(job), str(res)]) == 0
    assert json.loads(res.read_text(encoding="utf-8"))["ok"]
    text = hosts.read_text(encoding="latin-1")
    assert hostsedit.BEGIN in text and name in text and "localhost" in text


def test_the_packaged_program_restarts_its_own_exe_without_an_update(packaged):
    assert restart.helper_args() == [EXE, "--restart", "--no-update"]
    assert restart.helper_args(update=True) == [EXE, "--restart", "--no-update"]   # no start.bat to install one
    started = []
    os.environ["DBDMS_FORCE_UPDATE"] = "1"
    try:
        assert restart.wait_and_start(r"C:\Program Files\Fog Scout", running=lambda: False,
                                      run=lambda cmd, env: started.append((cmd, env)))
    finally:
        os.environ.pop("DBDMS_FORCE_UPDATE", None)
    (cmd, env), = started
    assert cmd == [EXE] and "DBDMS_FORCE_UPDATE" not in env
    assert restart.process_name() == "FogScout.exe"


def test_from_start_bat_the_restart_is_unchanged():
    assert restart.helper_args("pythonw.exe", frozen=False) == ["pythonw.exe", "-m", "fogscout", "--restart"]
    started = []
    assert restart.wait_and_start(ROOT, running=lambda: False, run=lambda cmd, env: started.append(cmd), frozen=False)
    assert started == [restart.start_command()]
    assert restart.process_name() == "pythonw.exe"


def test_the_taskbar_button_of_the_packaged_program_starts_the_exe(packaged):
    assert autostart.relaunch_command() == f'"{EXE}"'      # not installed (the CI folder): no task to run


def test_the_packaged_program_renews_its_own_tasks_and_checks_releases_not_git(packaged, monkeypatch):
    """1.32: the installed .exe renews its tasks like start.bat did (they start the .exe – autostart.app_root); git
    fetch needs a checkout – updates come with stage 5."""
    from fogscout import app_settings
    calls, events = [], []
    monkeypatch.setattr(app_settings.autostart, "ensure", lambda root, *a: calls.append(("ensure", root)))
    monkeypatch.setattr(app_settings.autostart, "ensure_autostart", lambda *a, **k: calls.append("auto"))
    monkeypatch.setattr(app_settings.autostart, "task_exists", lambda name: True)
    monkeypatch.setattr(app_settings, "is_admin", lambda: True)
    monkeypatch.setattr(app_settings, "IS_WIN", True)

    class Var:
        v = ""

        def set(self, v):
            self.v = v

    class Fake(app_settings.SettingsTab):
        def __init__(self):
            self.settings = {"autostart": True}
            self.root_dir = ROOT
            self.events = type("Q", (), {"put": staticmethod(events.append)})()
            self.upd_status = Var()
            self.upd_btn = type("B", (), {"state": staticmethod(lambda s: calls.append(("btn", tuple(s))))})()
            self.upd_apply_btn = type("B", (), {"pack_forget": staticmethod(lambda: None)})()

    fake = Fake()
    fake._setup_then_read_autostart()
    assert ("ensure", ROOT) in calls and "auto" in calls
    (kind, exists, can_change, info), = events
    assert kind == "autostart" and exists is True and can_change is True
    calls.clear()                                                   # 1.33: the release check (no git) in a thread
    from fogscout import relupdate
    monkeypatch.setattr(relupdate, "check", lambda root: calls.append(("release", root)) or
                        ("current", "aktuell", False, None))
    monkeypatch.setattr(app_settings.threading, "Thread", lambda target, **k: type("T", (), {"start": staticmethod(target)})())
    fake.check_update()
    assert ("release", ROOT) in calls and events[-1] == ("upd_check", "current", "aktuell", False, None, False)


def test_the_self_check_passes_from_the_source_checkout(tmp_path):
    out = tmp_path / "selftest.json"
    assert selftest.main(ROOT, str(out)) == 0, out.read_text(encoding="utf-8")
    res = json.loads(out.read_text(encoding="utf-8"))
    assert res["ok"] and not res["failed"] and res["frozen"] is False
    assert any(p.startswith("Module: ") for p in res["passed"])


def test_the_self_check_names_what_is_missing(tmp_path):
    res = selftest.run(str(tmp_path))                          # an empty folder: no maps, models, fonts …
    assert not res["ok"]
    assert any(f.startswith("Dateien: ") and "maps.json" in f for f in res["failed"])
    assert any(f.startswith("OCR: ") for f in res["failed"])


def _spec():
    with open(os.path.join(ROOT, "installer", "fogscout.spec"), encoding="utf-8") as fh:
        return fh.read()


def test_the_build_carries_every_file_the_self_check_needs():
    spec = _spec()
    tops = {f.split("/")[0] for f in selftest.FILES}
    for top in tops - {"fogscout"}:
        assert f'"{top}"' in spec, top
    assert '"fonts"' in spec and '"matchexport.user.js"' in spec and '"maps"' in spec
    assert 'collect_data_files("imageio_ffmpeg", subdir="binaries")' in spec
    assert "console=False" in spec and "uac_admin=False" in spec and "upx=False" in spec
    assert re.search(r'name="FogScout"', spec)


def test_the_exe_is_built_and_checked_in_ci():
    with open(os.path.join(ROOT, ".github", "workflows", "build.yml"), encoding="utf-8") as fh:
        wf = fh.read()
    assert "runs-on: windows-latest" in wf and "permissions:\n  contents: read" in wf
    assert "-r requirements-build.txt" in wf and "--no-deps -r requirements-extra.txt" in wf
    assert "--only-binary=:all:" in wf
    assert "installer/fogscout.spec" in wf and "--selftest" in wf and '"--helper", "hostsedit"' in wf
    assert "retention-days: 14" in wf
    build_job = wf[wf.index("\n  exe:"):wf.index("\n  release:")]
    assert "contents: write" not in build_job and "gh release" not in build_job   # the build itself publishes nothing
