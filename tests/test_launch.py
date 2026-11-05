"""1.33.3: programs started from Fog Scout never get the packaged program's DLL search, PATH or Qt folders.

Saru's update to 1.33.2 stopped at ``_internal\\msvcp140.dll``: OBS, started by Fog Scout, had loaded it from there."""
import ast
import os
import pathlib
import sys

import pytest

from fogscout import launch

PKG = pathlib.Path(__file__).resolve().parent.parent / "fogscout"


def _bundle(tmp_path):
    b = tmp_path / "Fog Scout" / "_internal"
    b.mkdir(parents=True)
    return str(b)


def test_the_child_environment_drops_the_bundle(tmp_path):
    bundle = _bundle(tmp_path)
    plugins = os.path.join(bundle, "PySide6", "plugins")
    other = str(tmp_path / "Windows")
    env = {"PATH": os.pathsep.join([bundle, other, os.path.join(bundle, "sub")]),
           "QT_PLUGIN_PATH": plugins, "QML2_IMPORT_PATH": os.path.join(bundle, "PySide6", "qml"),
           "_PYI_APPLICATION_HOME_DIR": bundle, "_PYI_PARENT_PROCESS_LEVEL": "1", "_MEIPASS2": bundle,
           "HOME": "x"}
    out = launch.child_env(env, bundle)
    assert out["PATH"] == other
    assert "QT_PLUGIN_PATH" not in out and "QML2_IMPORT_PATH" not in out
    assert not any(k.startswith("_PYI_") or k == "_MEIPASS2" for k in out)
    assert out["HOME"] == "x" and env["PATH"].startswith(bundle)          # the given mapping is not changed


def test_the_users_own_qt_folder_and_a_similar_name_stay(tmp_path):
    bundle = _bundle(tmp_path)
    near = bundle + "2"                                                    # same prefix, other folder
    own = str(tmp_path / "MyQt" / "plugins")
    out = launch.child_env({"PATH": near, "QT_PLUGIN_PATH": own}, bundle)
    assert out == {"PATH": near, "QT_PLUGIN_PATH": own}


def test_from_source_nothing_changes(monkeypatch):
    monkeypatch.delattr(sys, "frozen", raising=False)
    assert launch.bundle_dir() == ""
    env = {"PATH": "a", "QT_PLUGIN_PATH": "b"}
    assert launch.child_env(env) == env
    before = dict(os.environ)
    with launch.clean_process():
        assert dict(os.environ) == before


def test_while_a_program_starts_the_process_environment_is_clean_and_comes_back(tmp_path, monkeypatch):
    bundle = _bundle(tmp_path)
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", bundle, raising=False)
    monkeypatch.setenv("PATH", os.pathsep.join([bundle, "keep"]))
    monkeypatch.setenv("QT_PLUGIN_PATH", os.path.join(bundle, "plugins"))
    monkeypatch.setenv("_PYI_PARENT_PROCESS_LEVEL", "1")
    before = dict(os.environ)
    seen = {}

    def fake_open(url, *a, **k):
        seen.update(os.environ)
        return True

    monkeypatch.setattr(launch.webbrowser, "open", fake_open)
    assert launch.open_url("https://example.org/")
    assert seen["PATH"] == "keep" and "QT_PLUGIN_PATH" not in seen and "_PYI_PARENT_PROCESS_LEVEL" not in seen
    assert dict(os.environ) == before


def test_obs_and_explorer_get_the_clean_environment(tmp_path, monkeypatch):
    bundle = _bundle(tmp_path)
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", bundle, raising=False)
    monkeypatch.setenv("PATH", os.pathsep.join([bundle, "keep"]))
    calls = []
    monkeypatch.setattr(launch.subprocess, "Popen", lambda args, **kw: calls.append((args, kw)))
    launch.start_program(["obs64.exe", "--minimize-to-tray"], cwd="C:/obs", creationflags=8)
    launch.show_in_folder("C:/Aufnahmen/a.mp4")
    (obs, kw1), (exp, kw2) = calls
    assert obs == ["obs64.exe", "--minimize-to-tray"] and kw1["cwd"] == "C:/obs" and kw1["creationflags"] == 8
    assert exp[0].lower().endswith("explorer.exe") and exp[0] != "explorer.exe" and exp[1] == "/select,"  # full path
    assert kw1["env"]["PATH"] == "keep" and kw2["env"]["PATH"] == "keep"


def test_obs_is_started_through_launch(monkeypatch):
    from fogscout import obsrec
    calls = []
    monkeypatch.setattr(launch, "start_program", lambda args, **kw: calls.append((args, kw)))
    obsrec.Recorder._start_obs_process(os.path.join("C:", "obs-studio", "bin", "64bit", "obs64.exe"))
    (args, kw), = calls
    assert args[0].endswith("obs64.exe") and kw["cwd"].endswith("64bit")


def test_the_elevated_program_opens_urls_and_files_through_the_users_shell(monkeypatch):
    """1.38.21 (audit SEC-1): Fog Scout runs as administrator. ``webbrowser.open``/``os.startfile`` would start the
    browser or the file's program elevated – and ShellExecute picks the handler from HKCU\\Software\\Classes first,
    which any program of the user can write (a known way to administrator rights without a prompt). Elevated, the
    target goes to explorer.exe, which hands it to the user's own shell; not elevated, nothing changes."""
    calls = []
    monkeypatch.setattr(launch.subprocess, "Popen", lambda args, **kw: calls.append(args))
    monkeypatch.setattr(launch.webbrowser, "open", lambda *a, **k: (_ for _ in ()).throw(AssertionError("browser")))
    monkeypatch.setattr(os, "startfile", lambda p: (_ for _ in ()).throw(AssertionError("startfile")), raising=False)
    monkeypatch.setattr(launch, "elevated", lambda: True)
    assert launch.open_url("https://stats.deadbydaylight.com/") is True
    launch.open_path("C:/Users/x/AppData/Local/FogScout/fogscout.log")
    launch.open_path("C:/Users/x/AppData/Local/FogScout")
    assert launch.open_url("file:///C:/Windows/System32/cmd.exe") is False      # only web addresses leave this way
    assert launch.open_url("javascript:alert(1)") is False
    assert len(calls) == 3 and all(a[0].lower().endswith("explorer.exe") and a[0] != "explorer.exe" for a in calls)
    assert calls[0][1] == "https://stats.deadbydaylight.com/" and calls[1][1].endswith("fogscout.log")
    # not elevated (a source checkout started by hand, Linux): the plain way as before
    monkeypatch.setattr(launch, "elevated", lambda: False)
    opened = []
    monkeypatch.setattr(launch.webbrowser, "open", lambda url, *a, **k: opened.append(url) or True)
    assert launch.open_url("https://example.org") is True and opened == ["https://example.org"] and len(calls) == 3


def test_the_elevated_start_drops_what_the_user_environment_could_steer(tmp_path, monkeypatch):
    """1.38.21 (audit SEC-2): the task starts Fog Scout as administrator with the user's environment, which any
    program of the user can extend in HKCU\\Environment – SSL_CERT_FILE (whom the update check trusts), PYTHON*
    (what the helpers import), GIT_* (hooks, sslCAInfo), Qt plugin folders. Those go at the start; proxies, the
    data folder and the bundle's own Qt variables stay."""
    bundle = _bundle(tmp_path)
    env = {"SSL_CERT_FILE": "C:/evil/ca.pem", "SSL_CERT_DIR": "C:/evil", "REQUESTS_CA_BUNDLE": "x", "CURL_CA_BUNDLE": "x",
           "PYTHONPATH": "C:/evil", "PYTHONHOME": "C:/evil", "pythonstartup": "C:/evil/s.py",
           "GIT_DIR": "C:/evil", "GIT_SSL_CAINFO": "x", "GIT_CONFIG_PARAMETERS": "'core.fsmonitor=evil'",
           "QT_PLUGIN_PATH": "C:/evil/plugins", "QML2_IMPORT_PATH": "C:/evil/qml", "QT_QPA_PLATFORM_PLUGIN_PATH": "C:/evil",
           "HTTPS_PROXY": "http://proxy:3128", "NO_PROXY": "localhost", "PATH": "C:/Windows", "DBDMS_DATA_DIR": "D:/data",
           "QT_QPA_PLATFORM": "offscreen", "LOCALAPPDATA": "C:/Users/x/AppData/Local"}
    out = launch.clean_elevated_environment(env, "")
    assert out == {"HTTPS_PROXY": "http://proxy:3128", "NO_PROXY": "localhost", "PATH": "C:/Windows",
                   "DBDMS_DATA_DIR": "D:/data", "QT_QPA_PLATFORM": "offscreen", "LOCALAPPDATA": "C:/Users/x/AppData/Local"}
    ours = {"QT_PLUGIN_PATH": os.path.join(bundle, "PySide6", "plugins"), "PATH": "x"}
    assert launch.clean_elevated_environment(ours, bundle) == ours               # the runtime hook's own values stay
    assert "QT_PLUGIN_PATH" not in launch.clean_elevated_environment({"QT_PLUGIN_PATH": "C:/evil"}, bundle)
    # the start applies it only when elevated
    monkeypatch.setenv("SSL_CERT_FILE", "C:/evil/ca.pem")
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy:3128")
    monkeypatch.setattr(launch, "elevated", lambda: False)
    assert launch.harden_start_environment() == [] and os.environ["SSL_CERT_FILE"] == "C:/evil/ca.pem"
    monkeypatch.setattr(launch, "elevated", lambda: True)
    gone = launch.harden_start_environment()
    assert "SSL_CERT_FILE" in gone and "SSL_CERT_FILE" not in os.environ and os.environ["HTTPS_PROXY"]
    assert not any(k.upper().startswith(("SSL_CERT_", "GIT_")) for k in os.environ)


def test_elevated_is_false_outside_windows():
    if sys.platform != "win32":
        assert launch.elevated() is False


# Calls that start another program; outside launch.py they must go through it.
FORBIDDEN = {("webbrowser", "open"), ("webbrowser", "open_new"), ("webbrowser", "open_new_tab"), ("os", "startfile"),
             ("QDesktopServices", "openUrl")}


def _offences(path: pathlib.Path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if (node.value.id, node.attr) in FORBIDDEN:
                yield f"{path.name}:{node.lineno} {node.value.id}.{node.attr}"
        if isinstance(node, ast.Call) and node.args and isinstance(node.args[0], (ast.List, ast.Tuple)):
            first = node.args[0].elts[:1]
            if first and isinstance(first[0], ast.Constant) and str(first[0].value).lower() in ("explorer",
                                                                                             "explorer.exe"):
                yield f"{path.name}:{node.lineno} explorer"
        if isinstance(node, ast.ImportFrom) and node.module == "webbrowser":
            yield f"{path.name}:{node.lineno} from webbrowser import"


def test_every_other_program_is_started_through_launch():
    """Nothing in the package opens a browser, a file or Explorer itself – a new place would hand the bundle on."""
    bad = [o for f in sorted(PKG.glob("*.py")) if f.name != "launch.py" for o in _offences(f)]
    assert bad == []


@pytest.mark.skipif(sys.platform != "win32", reason="SetDllDirectoryW gibt es nur unter Windows")
def test_the_dll_search_is_windows_own_while_a_program_starts(tmp_path, monkeypatch):
    bundle = _bundle(tmp_path)
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", bundle, raising=False)
    k32 = launch._kernel32()
    old = launch.dll_directory()
    k32.SetDllDirectoryW(bundle)
    try:
        with launch.clean_process():
            assert launch.dll_directory() == ""
        assert os.path.normcase(launch.dll_directory()) == os.path.normcase(bundle)
    finally:
        k32.SetDllDirectoryW(old or None)
