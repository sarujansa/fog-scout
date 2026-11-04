"""1.30.1 (.exe, stage 2 – user: "Exe gute Idee", installed to Program Files): the program's own files (maps,
models, HISTORY.md) and what it writes (settings, rounds, log, cache, backups, own pictures, debug) are two folders.
From start.bat they are the same folder, exactly as before; the installed program writes only into the per-user
data folder – Program Files is read-only and shared by every user."""
import json
import os
import sys

import pytest

from fogscout import paths

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_a_source_checkout_keeps_its_files_in_the_program_folder(monkeypatch, tmp_path):
    monkeypatch.delattr(sys, "frozen", raising=False)
    assert not paths.frozen()
    assert paths.data_root(str(tmp_path)) == str(tmp_path)


def test_the_installed_program_writes_into_the_per_user_folder(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    data = tmp_path / "LocalAppData" / "FogScout"
    monkeypatch.setenv(paths.ENV, str(data))
    assert paths.frozen()
    assert paths.data_root(str(tmp_path / "Program Files" / "Fog Scout")) == str(data)
    assert data.is_dir()                                                  # made on the first start
    monkeypatch.delenv(paths.ENV)
    monkeypatch.setattr(paths, "_qt_location", lambda: "")
    monkeypatch.delenv("LOCALAPPDATA", raising=False)
    with pytest.raises(OSError):                                          # never a silent fallback to Program Files
        paths.data_root(str(tmp_path / "Program Files" / "Fog Scout"))


def _snapshot(folder):
    out = set()
    for base, dirs, files in os.walk(folder, followlinks=False):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(base, d))]
        out.update(os.path.relpath(os.path.join(base, f), folder) for f in files)
    return out


def test_the_app_writes_nothing_into_the_program_folder_when_it_has_a_data_folder(tmp_path, monkeypatch):
    """Settings, rounds, the style cache, the OBS overlay picture, diagnosis and own map pictures go to data_dir;
    the program folder (maps, models, maps.json) is only read."""
    if sys.platform == "win32":
        pytest.skip("Linux: the Windows job tests the native parts; the app would touch the system there")
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import backups, catalog, history, mapimage, obsoverlay, official
    program = tmp_path / "program"
    program.mkdir()
    for name in ("maps", "models", "maps.json"):
        os.symlink(os.path.join(ROOT, name), program / name)
    (program / "sim").mkdir()
    data = tmp_path / "data"
    data.mkdir()
    (data / "settings.json").write_text(json.dumps({"welcome_seen": True}), encoding="utf-8")
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "home"))
    before = _snapshot(program)
    from fogscout.app import App
    app = App(str(program), simulate=str(program / "sim"), data_dir=str(data))
    try:
        assert app.data_dir == str(data) and app.worker.data_dir == str(data)
        assert app.settings.path == str(data / "settings.json")
        assert app._hist_path() == str(data / history.FILE) and app._official_path() == str(data / official.FILE)
        assert obsoverlay.path(app.data_dir).startswith(str(data))
        assert app.catalog.user_dir == str(data / mapimage.USER_DIR)
        assert catalog.Catalog(str(program)).user_dir == str(program / mapimage.USER_DIR)   # start.bat: as before
        app.settings.set("sysinfo", "left")
        app.settings.save()
        monkeypatch.setattr(app, "_open", lambda path: None)              # no viewer in the test
        app.show_diagnose()
        assert (data / "diagnose.txt").exists()
        app._backup_done(backups.snapshot(app.data_dir))
    finally:
        app.quit()
    assert _snapshot(program) == before                                    # nothing new in the program folder
    assert (data / "settings.json").exists()
