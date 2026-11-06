"""1.28 (audit F13): what "Diagnose kopieren" and the visibility log line say about the PC – never another program's
window title, the home folder (with the account name) as "~"."""
import json
import os
import sys

import pytest

from fogscout import capture, diagnose

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_another_programs_window_is_named_by_its_kind_never_its_title(monkeypatch):
    monkeypatch.setattr(capture, "IS_WIN", True)
    monkeypatch.setattr(capture, "_window_text", lambda h: "Kontoauszug – Bank – Chrome")
    monkeypatch.setattr(capture, "_class_name", lambda h: "Chrome_WidgetWin_1")
    monkeypatch.setattr(capture, "is_game_window", lambda h: h == 7)
    assert capture.window_kind(5) == "anderes Programm [Chrome_WidgetWin_1]"
    assert capture.window_kind(7).startswith("DBD [")
    assert capture.window_kind(9, own={9}).startswith("Fog Scout [")
    assert capture.window_kind(0) == "(keins)"
    for h in (5, 7, 9):
        assert "Bank" not in capture.window_kind(h, own={9})


def test_the_home_folder_is_shortened_to_a_tilde(monkeypatch):
    home = os.path.join(os.sep, "home", "testuser")
    monkeypatch.setattr(os.path, "expanduser", lambda p: home if p == "~" else p)
    assert diagnose.home_short(os.path.join(home, "Downloads")) == "~" + os.sep + "Downloads"
    assert diagnose.home_short(home) == "~"
    assert diagnose.home_short(home + "x" + os.sep + "Downloads") == home + "x" + os.sep + "Downloads"   # not ours
    assert diagnose.home_short(os.path.join(os.sep, "data", "Downloads")) == os.path.join(os.sep, "data", "Downloads")
    assert diagnose.home_short(None) == ""


def test_the_match_data_line_of_the_diagnosis_shows_the_download_folder_with_a_tilde(tmp_path):
    if sys.platform == "win32":
        pytest.skip("Linux: the Windows job tests the native parts; the app would touch the system there")
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    for name in ("maps", "models", "maps.json"):
        os.symlink(os.path.join(ROOT, name), tmp_path / name)
    (tmp_path / "sim").mkdir()
    folder = os.path.join(os.path.expanduser("~"), "Downloads")
    (tmp_path / "settings.json").write_text(json.dumps({"welcome_seen": True, "official_dir": folder}),
                                            encoding="utf-8")
    from fogscout.app import App
    app = App(str(tmp_path), simulate=str(tmp_path / "sim"))
    try:
        line = app._official_diag()[0]
        assert "Ordner ~" + os.sep + "Downloads" in line and os.path.expanduser("~") + os.sep not in line
    finally:
        app.quit()


def test_the_log_shows_the_home_folder_as_tilde_in_message_and_traceback(monkeypatch, tmp_path):
    """1.38.57 (security review): log lines and exception text are pasted into issues – the home folder (account
    name) becomes "~", also inside a message and in the traceback; a longer folder name is not ours."""
    import logging
    from fogscout.__main__ import HomeFilter
    home = str(tmp_path / "Saru")
    monkeypatch.setattr(os.path, "expanduser", lambda p: home if p == "~" else p)
    target = os.path.join(home, "Videos", "clip.mp4")
    try:
        raise OSError(f"cannot open {target}")
    except OSError:
        import sys
        exc = sys.exc_info()
    rec = logging.LogRecord("fogscout", logging.ERROR, __file__, 1, "Datei %s fehlt (%s)", (target, home + "man"),
                            exc)
    assert HomeFilter().filter(rec)
    text = logging.Formatter("%(message)s").format(rec)
    assert home + os.sep not in text and home + "man" in text
    assert rec.getMessage() == f"Datei ~{os.sep}Videos{os.sep}clip.mp4 fehlt ({home}man)"
    assert f"cannot open ~{os.sep}Videos" in rec.exc_text


def test_crash_lines_show_the_home_folder_as_tilde(monkeypatch, tmp_path):
    home = str(tmp_path / "Saru")
    monkeypatch.setattr(os.path, "expanduser", lambda p: home if p == "~" else p)
    (tmp_path / diagnose.CRASH_LAST).write_text(f'  File "{home}{os.sep}app.py", line 3\n', encoding="utf-8")
    text = "\n".join(diagnose.crash_lines(str(tmp_path)))
    assert home not in text and f'"~{os.sep}app.py"' in text
