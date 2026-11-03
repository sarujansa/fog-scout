"""1.26: the command palette in the App – Ctrl+F darkens the window, the entries of every kind, what a pick does,
Claude only when switched on and only with names of the program's own entries; the key never leaves the PC."""
import json
import os
import sys
import time

import pytest

from fogscout import askclaude, config, history, spotify

KEY = "sk-ant-api03-" + "k" * 40


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def app_root(tmp_path):
    if sys.platform == "win32":
        pytest.skip("Linux: the Windows job tests the native parts; the app would touch the system there")
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    for name in ("maps", "models", "maps.json"):
        os.symlink(os.path.join(ROOT, name), tmp_path / name)
    (tmp_path / "sim").mkdir()
    return tmp_path


def _rows(p):
    from fogscout.qt_palette import ROLE
    return [p.rows.item(i).data(ROLE) for i in range(p.rows.count())]


def _app(root, **settings):
    from fogscout.app import App
    (root / "settings.json").write_text(json.dumps(dict({"welcome_seen": True}, **settings)), encoding="utf-8")
    return App(str(root), simulate=str(root / "sim"))


def _pump(app, n=5):
    for _i in range(n):
        app.qapp.processEvents()
        app._poll()


def _open(app):
    """Focus is checked in test_qt (the Linux overlay window takes the activation here, Windows' never does)."""
    app.qt.show()
    app.qt.resize(1100, 800)
    app.qt.focus_search()
    _pump(app)
    return app.qt.palette


def test_ctrl_f_darkens_the_window_and_offers_every_kind(app_root):
    history.append(str(app_root / "rounds.jsonl"), history.Round(time.time() - 900, 600, "coal", "Coal Tower",
                                                                role="killer", killer="The Nurse"))
    app = _app(app_root)
    try:
        p = _open(app)
        assert p.isVisible()
        kinds = {e.kind for e in p._entries}
        assert kinds == {"action", "page", "setting", "map", "round"}
        img = app.qt.grab().toImage()
        corner = img.pixelColor(img.width() - 4, img.height() - 4)       # outside the card: darkened
        assert corner.lightness() < 60
        p.field.setText("coal")
        rows = _rows(p)
        assert any(r and r[0] == "entry" and r[1].kind == "map" for r in rows)
        assert any(r and r[0] == "entry" and r[1].kind == "round" for r in rows)
        assert not any(r and r[0] == "ask" for r in rows)              # Claude off: no row to ask
        from PySide6.QtCore import Qt
        from PySide6.QtTest import QTest
        QTest.keyClick(p.field, Qt.Key_Escape)
        assert not p.isVisible()
    finally:
        app.quit()


def test_picks_run_what_the_buttons_do_and_are_remembered(app_root):
    history.append(str(app_root / "rounds.jsonl"), history.Round(time.time() - 900, 600, "coal", "Coal Tower"))
    app = _app(app_root)
    try:
        _open(app)
        mid = next(iter(app.catalog.maps))
        app._qt_event("palette_pick", ("m:" + mid, True))              # Ctrl+Enter: into the game
        assert app.current is not None and app.current[0] == mid
        app._qt_event("palette_pick", ("m:" + mid, False))             # Enter: big on the maps page
        assert app.qt.current_key() == "maps"
        app._qt_event("palette_pick", ("p:stats", False))
        assert app.qt.current_key() == "stats"
        t = app._joined().rounds[0].t
        app._qt_event("palette_pick", ("r:" + repr(t), False))
        assert app.qt.current_key() == "stats" and app.stats_last.selection() == (repr(t),)
        setting = next(e for e in app.qt.setting_entries() if e.title.startswith("Mit Windows starten"))
        app._qt_event("palette_pick", (setting.id, False))
        assert app.qt.current_key() == app.qt._found[setting.arg][0]
        called = []
        app.scan_now = lambda: called.append("scan")
        app._qt_event("palette_pick", ("a:scan", False))
        assert called == ["scan"]
        assert app.settings.get("palette_recent")[:2] == ["a:scan", setting.id]
        app._qt_event("palette_pick", ("nothing:there", False))         # an unknown id does nothing
    finally:
        app.quit()


def test_claude_is_asked_only_when_switched_on_and_gets_only_the_programs_names(app_root, monkeypatch):
    history.append(str(app_root / "rounds.jsonl"), history.Round(time.time() - 900, 600, "coal", "Coal Tower",
                                                                role="killer", killer="The Nurse"))
    asked = []

    class FakeAsker:
        def __init__(self, post):
            self.post = post

        def start(self):
            pass

        def ask(self, key, question, catalogue):
            asked.append((key, question, list(catalogue)))

        def stop(self):
            pass

        def diag_line(self):
            return "gefragt 1"

    monkeypatch.setattr(askclaude, "Asker", FakeAsker)
    app = _app(app_root)
    try:
        p = _open(app)
        app._qt_event("palette_ask", "wie mache ich die Karte grösser?")
        assert asked == []                                              # off: nothing sent
        app.cl_on_var.set(True)
        app._claude_setting()
        app.cl_key_var.set(KEY)
        assert app.settings.get("claude_key") != KEY and spotify.unprotect(app.settings.get("claude_key")) == KEY
        assert p._claude
        p.field.setText("karte grösser")
        last = _rows(p)[-1]
        assert last == ("ask", "karte grösser")
        app._qt_event("palette_ask", "karte grösser")
        (key, question, catalogue), = asked
        assert key == KEY and question == "karte grösser"
        ids = [i for i, _t in catalogue]
        assert all(i[:2] in ("s:", "p:", "a:") for i in ids)            # never maps or rounds
        text = json.dumps(catalogue)
        assert "Coal Tower" not in text and "Nurse" not in text and str(app_root) not in text
        sid = next(i for i in ids if i.startswith("s:"))
        app._claude_event("answer", {"answer": "Hier.", "ids": [sid, "p:overlay"], "question": "karte grösser"})
        assert p.answer.isVisible() and p.answer.text() == "Hier."
        shown = _rows(p)
        assert [v[1].id for v in shown if v[0] == "entry"] == [sid, "p:overlay"]
        app._claude_event("error", {"error": "auth", "question": "karte grösser"})
        assert "API-Key" in p.answer.text()
        app._claude_event("answer", {"answer": "alt", "ids": [], "question": "etwas anderes"})
        assert p.answer.text() != "alt"                                 # a stale answer is dropped
        diag = app._claude_diag()
        assert KEY not in diag and "grösser" not in diag
    finally:
        app.quit()


def test_the_key_is_never_in_the_backup(tmp_path):
    data = dict(config.DEFAULTS, claude_key=spotify.protect(KEY), claude_on=True, palette_recent=["a:scan"])
    path = str(tmp_path / "backup.json")
    config.export_settings(data, path)
    text = open(path, encoding="utf-8").read()
    assert "claude_key" not in text and "claude_on" in text
    assert "claude_key" in config.LOCAL_KEYS and "palette_recent" in config.LOCAL_KEYS


def test_the_card_opens_the_consoles_key_and_billing_pages(app_root, monkeypatch):
    """1.26.1 (user: "einen Button, dass man direkt auf die Seite kommt"): two buttons open the Anthropic Console's
    pages in the browser – only on a click, nothing is sent by the program."""
    import webbrowser
    opened = []
    monkeypatch.setattr(webbrowser, "open", lambda url, *a, **k: opened.append(url))
    app = _app(app_root)
    try:
        assert opened == []                                             # nothing opens by itself
        app._qt_reg["st.more.cl_keys"].invoke()
        app._qt_reg["st.more.cl_billing"].invoke()
        assert opened == [askclaude.CONSOLE_KEYS, askclaude.CONSOLE_BILLING]
        assert all(u.startswith("https://platform.claude.com/settings/") for u in opened)
    finally:
        app.quit()
