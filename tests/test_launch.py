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
