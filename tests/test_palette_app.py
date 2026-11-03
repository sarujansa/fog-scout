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
        assert all(i[:1] == "e" and i[1:].isdigit() for i in ids)       # 1.28: opaque ids, no entry text twice
        real = app._claude_ids                                          # … mapped back to settings/pages/actions
        assert all(real[i][:2] in ("s:", "p:", "a:") for i in ids)      # never maps or rounds
        text = json.dumps(catalogue)
        assert "Coal Tower" not in text and "Nurse" not in text and str(app_root) not in text
        cid = next(i for i in ids if real[i].startswith("s:"))
        pid = next(i for i in ids if real[i] == "p:overlay")
        app._claude_event("answer", {"answer": "Hier.", "ids": [cid, pid, "e9999"], "question": "karte grösser"})
        assert p.answer.isVisible() and p.answer.text() == "Hier."
        shown = _rows(p)
        assert [v[1].id for v in shown if v[0] == "entry"] == [real[cid], "p:overlay"]
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


class _BodyOpener:
    """Fake HTTP: records the request bodies the Claude search really sends (no network)."""

    def __init__(self):
        import threading
        self.bodies, self.sent = [], threading.Event()

    def open(self, req, timeout=None):
        import io
        self.bodies.append(req.data.decode("utf-8"))
        self.sent.set()
        reply = json.dumps({"stop_reason": "end_turn",
                            "content": [{"type": "text", "text": json.dumps({"answer": "ok", "ids": []})}]})

        class R(io.BytesIO):
            def __enter__(s):
                return s

            def __exit__(s, *a):
                return False
        return R(reply.encode("utf-8"))


def test_the_claude_search_sends_only_fixed_program_texts_never_status_paths_or_game_values(app_root, monkeypatch):
    """1.28 (audit F1, P1): the request body of the Claude search – read from the fake HTTP layer, not from a helper
    – holds no run-time text: a server status with a Windows path, statistics lines with a map, a time and a ping
    stay home; the fixed names of actions, pages and settings still go, so the search keeps working."""
    for i in range(6):
        history.append(str(app_root / "rounds.jsonl"), history.Round(time.time() - 9000 + i * 900, 600, "coal",
                                                                    "Coal Tower II", role="killer", killer="The Nurse"))
    opener = _BodyOpener()
    monkeypatch.setattr(askclaude, "OPENER", opener)
    app = _app(app_root, claude_on=True, claude_key=spotify.protect(KEY))
    try:
        secrets = ("C:\\Windows\\Testpfad", "Testpfad", "Coal Tower", "Nurse", "21:37", "47 ms", "eu-central-1")
        app.srv_status.set("hosts-Datei nicht lesbar: C:\\Windows\\Testpfad\\hosts – Frankfurt 47 ms")
        for var in ("stats_farm_var", "stats_rating_var", "stats_saved_var", "stats_wait_var"):
            getattr(app, var).set("Zuletzt: Coal Tower II, 21:37 – The Nurse, 47 ms, eu-central-1")
        p = _open(app)
        _pump(app)
        p.field.setText("wie mache ich die karte grösser")
        app._qt_event("palette_ask", "wie mache ich die karte grösser")
        assert opener.sent.wait(10), "no request was made"
        body = opener.bodies[0]
        sent = json.loads(body)["messages"][0]["content"]
        for s in secrets:
            assert s not in body, s
        for fixed in ("Overlay testen", "Statistik", "Mit Windows starten"):            # still usable
            assert fixed in sent, fixed
        assert "\\ts:" not in sent and "\\tp:" not in sent       # ids are opaque, entry texts not twice
    finally:
        app.quit()


def test_the_claude_key_is_stored_encrypted_or_lives_for_the_session_only(app_root, monkeypatch, caplog):
    """1.28 (audit F2/F2b): with the Windows encryption the card says „verschlüsselt gespeichert“; without it a new
    key works for this run only – settings.json keeps the old value, the card says so, never „verschlüsselt“; the
    key is never in a log."""
    import logging
    caplog.set_level(logging.DEBUG)
    app = _app(app_root)
    try:
        app.cl_on_var.set(True)
        app._claude_setting()
        app.cl_key_var.set(KEY)
        assert spotify.is_encrypted(app.settings.get("claude_key")) and app._claude_key() == KEY
        assert "(verschlüsselt gespeichert)" in app.cl_status_var.get()
        stored = app.settings.get("claude_key")
        monkeypatch.setattr(spotify, "CIPHER", None)
        other = "sk-ant-api03-" + "z" * 40
        app.cl_key_var.set(other)
        assert app.settings.get("claude_key") == stored and app._claude_key() == other
        status = app.cl_status_var.get()
        assert "nur für diese Sitzung" in status and "verschlüsselt gespeichert" not in status
        assert app._claude_ready()
        app.settings.save()
        text = (app_root / "settings.json").read_text(encoding="utf-8")
        assert other not in text and "plain:" not in text
        logs = caplog.text + " ".join(t for *_x, t in app._log_entries)
        assert KEY not in logs and other not in logs and "zzzzzzzz" not in logs
    finally:
        app.quit()


def test_an_unreadable_claude_key_survives_a_switch_and_goes_only_by_key_loeschen(app_root):
    """1.28 (audit F2b): a stored key this PC cannot read showed an empty field, and the next click on a switch
    wrote that empty field over it. Now switches leave it, the card says it is not readable, „Key löschen“ removes
    it on purpose."""
    app = _app(app_root, claude_key="dpapi:QUJD")
    try:
        assert app.cl_key_var.get() == "" and app._claude_key() == ""
        assert "nicht lesbar" in app.cl_status_var.get()
        app.cl_on_var.set(True)
        app._claude_setting()
        app.cl_editor_var.set(True)
        app._claude_setting()
        assert app.settings.get("claude_key") == "dpapi:QUJD"
        assert "verschlüsselt gespeichert" not in app.cl_status_var.get()
        app._qt_reg["st.more.cl_clear"].invoke()
        assert app.settings.get("claude_key") == "" and "nicht lesbar" not in app.cl_status_var.get()
    finally:
        app.quit()


def test_an_old_plain_claude_key_is_called_unencrypted_when_it_cannot_be_encrypted(app_root, monkeypatch):
    """1.28: a "plain:" key from before 1.28 that cannot be encrypted (no DPAPI) stays readable and the card says
    „unverschlüsselt gespeichert (alt)“ – never „verschlüsselt“."""
    import base64
    monkeypatch.setattr(spotify, "CIPHER", None)
    old = "plain:" + base64.b64encode(KEY.encode()).decode()
    app = _app(app_root, claude_key=old, claude_on=True)
    try:
        assert app.settings.get("claude_key") == old and app._claude_key() == KEY
        assert "unverschlüsselt gespeichert (alt)" in app.cl_status_var.get()
    finally:
        app.quit()
