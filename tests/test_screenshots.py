"""1.38.2: tools/screenshots.py draws every page offscreen – the pictures are how a GUI change is checked before and
after (not a timing, not a pixel comparison: only that each page, tab and setup step yields a file)."""
import importlib.util
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _tool():
    spec = importlib.util.spec_from_file_location("screenshots", os.path.join(ROOT, "tools", "screenshots.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def app_root(tmp_path):
    if sys.platform == "win32":
        pytest.skip("Linux: the Windows job tests the native parts; the app would touch the system there")
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    for name in ("maps", "models", "maps.json"):
        os.symlink(os.path.join(ROOT, name), tmp_path / name)
    (tmp_path / "sim").mkdir()
    (tmp_path / "settings.json").write_text('{"welcome_seen": true}', encoding="utf-8")
    return tmp_path


def test_every_page_tab_and_setup_step_gives_a_picture(app_root):
    from fogscout.app import App
    from fogscout import qt_window
    tool = _tool()
    app = App(str(app_root), simulate=str(app_root / "sim"))
    app.qt.resize(1100, 760)
    out = app_root / "shots"
    try:
        files = tool.shoot(app, str(out), pages=["settings", "overlay", "log", "setup"])
    finally:
        app.quit()
    names = sorted(os.path.basename(f) for f in files)
    assert all(os.path.getsize(f) > 1000 for f in files)
    tabs = qt_window.SPECS["settings"][0][1]                       # ("tabs", ((key, title, items), …))
    assert len(tabs) == 6
    for _key, title, _items in tabs:
        assert any(n.startswith("settings-" + tool._name(title)[:-4]) for n in names), (title, names)
    assert "log.png" in names and "overlay-Karte.png" in names
    assert [n for n in names if n.startswith("setup-")] == [f"setup-{i}.png" for i in range(1, 9)]
    assert all(not n.startswith(("overview", "stats", "maps")) for n in names)        # only the pages asked for
