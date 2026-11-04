"""1.12.2 (user on the recordings page: "ich find das nicht schön"): the screenshots as a gallery, one status
column, the file column hidden until shown, the gallery taking the page's height."""
import os
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import thumbs  # noqa: E402
from fogscout.app_recordings import RecordingsTab  # noqa: E402


def test_the_status_column_shows_kept_marks_and_youtube_as_symbols():
    status = RecordingsTab._rec_status
    assert status(False, 0, "") == ""
    assert status(True, 2, "✓") == "★  ⚑2  ▶"
    assert status(False, 1, "…") == "⚑1  ▶…"                              # waiting in the upload queue
    assert status(True, 0, "") == "★"


def test_a_jpeg_thumbnail_is_decoded_at_a_reduced_scale_and_fits_its_box(tmp_path):
    src = tmp_path / "20261025194138_1.jpg"
    Image.new("RGB", (3440, 1440), (40, 60, 90)).save(src, quality=90)
    pic = thumbs.thumbnail(str(src), (322, 182), str(tmp_path / "cache"))
    assert pic.size == (322, 135) and pic.mode == "RGBA"
    assert thumbs.thumbnail(str(src), (322, 182), str(tmp_path / "cache")).size == (322, 135)   # from the cache
    assert thumbs.Loader((10, 10), name="shot-thumbs").name == "shot-thumbs"


def test_the_gallery_fills_its_rows_takes_the_pictures_shape_and_reports_clicks(tmp_path):
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_gallery, qt_window
    app = qt_window.application()
    paths = []
    for i in range(7):
        p = tmp_path / f"shot{i}.jpg"
        Image.new("RGB", (2100, 900), (30 * i, 40, 60)).save(p)                # 21:9 like an ultrawide screen
        paths.append(str(p))
    picked, opened = [], []
    g = qt_gallery.ShotGallery(str(tmp_path / "cache"), on_pick=picked.append, on_open=opened.append)
    try:
        g.resize(1200, 700)
        g.show()
        g.set_items([(p, f"25.10.26 · 19:4{i}", "47 KB", "Bearbeitet" if i == 0 else "") for i, p in enumerate(paths)])
        app.processEvents()
        assert g.paths() == paths and g.selected_path() is None
        tile = g.tile_size()
        n = (g.viewport().width() - 4) // tile.width()
        assert n >= 3 and n * tile.width() <= g.viewport().width()             # a row ends at the edge, no wrap gap
        assert (n + 1) * tile.width() > g.viewport().width() - 4
        g.load_all()
        assert g.aspect == pytest.approx(2100 / 900, rel=0.01)                 # tiles took the pictures' shape
        assert all(not g.pixmap(p).isNull() for p in paths)
        g.select_path(paths[2])
        assert g.selected_path() == paths[2] and picked == []                  # set from the App: no report back
        g.item(4).setSelected(True)
        assert picked[-1] == paths[4]
        g.itemActivated.emit(g.item(4))
        assert opened == [paths[4]]
        g.set_items([(p, "x", "y", "") for p in paths[3:]], selected=paths[4])  # another list keeps the pick
        assert g.paths() == paths[3:] and g.selected_path() == paths[4]
        assert set(g._pix) <= set(paths[3:])                                     # pixmaps of gone pictures dropped
        grab = g.grab()
        assert not grab.isNull()
    finally:
        g.close()


def test_the_file_column_is_hidden_until_the_user_shows_it():
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_views, qt_window
    qt_window.application()
    posted = []
    t = qt_views.Table("rec", lambda *a: posted.append(a))
    st = {"columns": [("when", "Wann", "w"), ("map", "Map", "w"), ("file", "Datei", "w")],
          "rows": [("a", 0, "", ["1", "Coal Tower", "x.mkv"], [], True)], "stretch": 1, "widths": [100, 130, 110],
          "hide": ["file"]}
    t.show_state(st)
    assert t.isColumnHidden(2) and not t.isColumnHidden(1)
    t._toggle_column("file", True)                                            # shown from the heading's menu
    assert not t.isColumnHidden(2) and posted[-1] == ("table_cols", ("when|map|file", []))
    t2 = qt_views.Table("rec", lambda *a: None)
    t2.set_hidden_map({"when|map|file": []})                                  # the remembered choice wins
    t2.show_state(st)
    assert not t2.isColumnHidden(2)


def test_a_host_packed_to_expand_takes_the_free_height_of_its_page():
    from fogscout import app_qt, qt_pages, uimodel as ui
    root = ui.Frame(None)
    h = ui.Host(root)
    h.pack(fill="both", expand=True)
    node = app_qt.ui_layout(root, {})
    assert node["children"][0]["grow"] is True and qt_pages._grows(node)
    other = ui.Frame(None)
    ui.Host(other).pack(side="left", fill="both")                             # the clip preview beside a table
    assert not app_qt.ui_layout(other, {})["children"][0]["grow"]


# ---- review fixes (1.12.2): screenshots tab, gallery thumbnails, table columns, clips menu
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def app_root(tmp_path, monkeypatch):
    if sys.platform == "win32":
        pytest.skip("Linux: the Windows job tests the native parts; the app would touch the system there")
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    for name in ("maps", "models", "maps.json"):
        os.symlink(os.path.join(ROOT, name), tmp_path / name)
    (tmp_path / "sim").mkdir()
    _own_home(tmp_path, monkeypatch)
    return tmp_path


def _own_home(tmp_path, monkeypatch):
    """A home of its own for "Bilder/Fog Scout" (steamshots.edit_folder(None)): HOME on Linux, USERPROFILE on
    Windows – expanduser ignores HOME there, and a test wrote into the user's real Pictures folder (and listed what
    was in it)."""
    import ntpath
    import posixpath
    home = str(tmp_path / "home")
    monkeypatch.setenv("HOME", home)
    monkeypatch.setenv("USERPROFILE", home)
    assert posixpath.expanduser("~") == home and ntpath.expanduser("~") == home    # both rules, on every system
    return home


def _settings(root, **values):
    import json
    (root / "settings.json").write_text(json.dumps({"welcome_seen": True, **values}), encoding="utf-8")


def _pictures(folder, n=1, size=(320, 135)):
    folder.mkdir(parents=True, exist_ok=True)
    out = []
    for i in range(n):
        p = folder / f"2026102519{i:04d}_1.jpg"
        Image.new("RGB", size, (20 + i % 200, 40, 60)).save(p)
        os.utime(p, (1_760_000_000 + i, 1_760_000_000 + i))
        out.append(str(p))
    return out


def _mkdir(path):
    os.makedirs(path, exist_ok=True)
    return path


def _open_shots(app):
    app.qt.resize(1400, 1100)
    app.qt.show()
    app.qt.show_page("recordings")
    app._rec_render(force=True)
    app.rec_nb.select(app.rec_nb.tabs()[2])
    app._qt_refresh(force=True)
    app.qapp.processEvents()
    gallery = app.qt.host(str(app.shot_host)).content
    gallery.doItemsLayout()
    return gallery


def test_a_right_click_on_a_screenshot_tile_opens_its_menu(app_root, tmp_path):
    """The gallery posted 2-tuples and a QPoint – popup_menu raised ValueError and no menu came."""
    from fogscout.app import App
    shots = _pictures(tmp_path / "shots")
    _settings(app_root, shots_folder=str(tmp_path / "shots"))
    app = App(str(app_root), simulate=str(app_root / "sim"))
    try:
        gallery = _open_shots(app)
        gallery._menu(gallery.visualItemRect(gallery.item(0)).center())         # the right click
        menu = app.qt._menu
        assert [(a.text(), a.isEnabled()) for a in menu.actions()] == [("Bild bearbeiten …", True),
                                                                       ("Bild im Explorer zeigen", True)]
        opened = []
        app._shot_edit = lambda path=None: opened.append(app._shot_sel)
        menu.actions()[0].trigger()
        app._poll()
        assert opened == shots
        menu.close()
    finally:
        app.quit()


def test_a_column_shown_again_stays_shown_after_a_restart(app_root, tmp_path):
    """Showing "Datei" posted [] and the App dropped the entry – the next start hid the column again."""
    from fogscout.app import App
    _pictures(tmp_path / "shots")                                               # something to show: the tabs
    _settings(app_root, shots_folder=str(tmp_path / "shots"))

    def rec_table(app):
        app.qt.show_page("recordings")
        app._rec_render(force=True)
        app._qt_refresh(force=True)
        return app.qt.forms["recordings"].controls[str(app.rec_table)][1]

    app = App(str(app_root), simulate=str(app_root / "sim"))
    try:
        t = rec_table(app)
        assert t.isColumnHidden(t._cols.index("file"))                         # hidden until shown
        t._toggle_column("file", True)                                          # ticked in the heading's menu
        app._poll()
        assert app.settings.get("hidden_columns") == {t.col_key(): []}
    finally:
        app.quit()
    app = App(str(app_root), simulate=str(app_root / "sim"))                    # the next start
    try:
        t = rec_table(app)
        assert not t.isColumnHidden(t._cols.index("file"))
    finally:
        app.quit()


class _StepLoader:
    """thumbs.Loader by hand: ``request`` replaces the list (the newest wins), ``pick`` = the thread takes the next
    path (no longer in the list), ``finish`` = it is made."""

    def __init__(self, make):
        self.make, self.todo, self.done, self.hand = make, [], [], None

    def request(self, paths):
        self.todo = list(paths)

    def pick(self):
        self.hand = self.todo.pop(0)

    def finish(self):
        self.done.append(self.make(self.hand))
        self.hand = None

    def run(self):
        while self.todo:
            self.pick()
            self.finish()

    def take(self, limit=8):
        out, self.done = self.done[:limit], self.done[limit:]
        return out

    @property
    def busy(self):
        return bool(self.todo) or bool(self.done)


def _gallery(tmp_path, n, size=(700, 420)):
    from fogscout import qt_gallery, qt_window
    app = qt_window.application()
    paths = _pictures(tmp_path / "pics", n, size=(210, 90))
    g = qt_gallery.ShotGallery(str(tmp_path / "cache"))
    g._loader = _StepLoader(g._loader.make)
    g.resize(*size)
    g.show()
    g.set_items([(p, "c", "s", "") for p in paths])
    app.processEvents()
    g.doItemsLayout()
    return g, paths


def _pump(g):
    """What the pump timer does while it runs (the loader's thread keeps up)."""
    while g._pump.isActive() and (g._loader.done or g._loader.todo):
        g._loader.run()
        g._take()


def _on_display(g):
    from fogscout import qt_gallery
    view = g.viewport().rect()
    return [g.item(i).data(qt_gallery.PATH_ROLE) for i in range(g.count())
            if g.visualItemRect(g.item(i)).intersects(view)]


def test_the_last_thumbnail_comes_although_the_loader_looked_idle_while_making_it(tmp_path):
    """Loader.busy is False while the thread makes the last picture – the pump stopped and that tile stayed black."""
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    g, paths = _gallery(tmp_path, 3)
    try:
        g._ask_visible()
        loader = g._loader
        assert loader.todo == paths
        for _i in range(2):
            loader.pick()
            loader.finish()
        loader.pick()                                     # the last one in the thread's hand
        g._take()
        assert not loader.busy
        loader.finish()
        if g._pump.isActive():                            # the timer's next tick
            g._take()
        assert all(p in g._pix and not g._pix[p].isNull() for p in paths)
        assert not g._pump.isActive()                     # then it rests
    finally:
        g.close()


def test_thumbnails_a_newer_request_dropped_are_asked_for_again(tmp_path):
    """The loader keeps only the newest request; a path asked once was never asked again – black after scrolling."""
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    g, _paths = _gallery(tmp_path, 60)
    try:
        g._ask_visible()
        top = _on_display(g)
        g._loader.pick()                                  # one is made, the rest still to do …
        g._loader.finish()
        g._take()
        sb = g.verticalScrollBar()
        assert sb.maximum() > 0
        sb.setValue(sb.maximum())                         # … when the user drags the bar down
        g._ask_visible()
        _pump(g)
        sb.setValue(0)
        g._ask_visible()
        _pump(g)
        assert top and all(p in g._pix for p in _on_display(g))
    finally:
        g.close()


def test_the_gallery_keeps_pixmaps_only_for_the_tiles_near_the_display(tmp_path, monkeypatch):
    """Every thumbnail scrolled past stayed a pixmap (~370 MB for 2000 screenshots); now the far ones go and come
    again from the disk cache when scrolled back."""
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_gallery
    monkeypatch.setattr(qt_gallery, "PIX_KEPT", 6, raising=False)
    g, paths = _gallery(tmp_path, 80, size=(700, 300))
    try:
        sb = g.verticalScrollBar()
        g._ask_visible()
        _pump(g)
        top = _on_display(g)
        most = 0
        for v in range(0, sb.maximum() + sb.pageStep(), sb.pageStep()):
            sb.setValue(min(v, sb.maximum()))
            g._ask_visible()
            _pump(g)
            most = max(most, len(g._pix))
        assert most < len(paths) // 2                                # not every picture scrolled past
        assert not any(p in g._pix for p in top)                     # far away now: let go
        sb.setValue(0)
        g._ask_visible()
        _pump(g)
        assert all(p in g._pix and not g._pix[p].isNull() for p in _on_display(g))    # back again
    finally:
        g.close()


def test_the_screenshot_folder_can_be_chosen_while_nothing_is_recorded(app_root, tmp_path):
    """No recording, no clip, no Steam folder: the tabs stay away – and with them "Anderen Ordner …", the only way to
    point the program at the pictures (Epic/Store, Steam saving elsewhere)."""
    from fogscout import uimodel as ui
    from fogscout.app import App

    def reachable(w):
        """Packed, and so is every frame up to the page (a notebook's pages are its tabs)."""
        while w is not None and w is not app.tab_recordings:
            if not isinstance(w.master, ui.Notebook) and not w.winfo_manager():
                return False
            w = w.master
        return True

    def buttons(w, text):
        return [c for c in w.winfo_children() if str(c.cget("text")) == text] + \
            [b for c in w.winfo_children() for b in buttons(c, text)]

    _settings(app_root)
    app = App(str(app_root), simulate=str(app_root / "sim"))
    try:
        app._rec_render(force=True)
        assert not app.rec_nb.winfo_manager() and app.rec_setup_btn.winfo_manager()
        btn = next((b for b in buttons(app.tab_recordings, "Anderen Ordner …") if reachable(b)), None)
        assert btn is not None and btn._dbdms_tip()
        label = next(w for w in app.rec_empty_shots.winfo_children() if isinstance(w, ui.Label))
        assert "Anderen Ordner" in str(label.cget("text"))           # the line says what the button is for
        chosen = []
        app._qt_file = lambda mode, title, initial, callback, *a: chosen.append(callback)
        btn.invoke()
        _pictures(tmp_path / "mine")
        chosen[0](str(tmp_path / "mine"))
        assert app.settings.get("shots_folder") == str(tmp_path / "mine")
        assert app.rec_nb.winfo_manager() and not reachable(btn)    # the tabs, on the screenshots
        assert app.rec_nb.select() == app.rec_nb.tabs()[2] and app._shot_count == 1
    finally:
        app.quit()


def test_the_empty_page_keeps_its_order_when_recording_is_switched(app_root, tmp_path):
    """The screenshot line was packed before the tabs, which an empty page does not show: switching recording on or
    off put "Aufnahmen einrichten …" / the note below it in the page's order."""
    from fogscout.app import App
    _settings(app_root, rec_folder=_mkdir(str(tmp_path / "rec")))
    app = App(str(app_root), simulate=str(app_root / "sim"))
    try:
        own = (app.rec_setup_btn, app.rec_empty_label, app.rec_empty_shots, app.rec_nb)

        def placed():
            return [w for w in app.rec_nb.master.placed_children() if w in own]

        for on in (False, True, False, True):
            app.settings.set("rec_on", on)
            app._rec_render(force=True)
            assert placed() == [app.rec_empty_label if on else app.rec_setup_btn, app.rec_empty_shots]
        _pictures(tmp_path / "mine")
        app._shot_folder_chosen(str(tmp_path / "mine"))
        assert placed() == [app.rec_nb]
    finally:
        app.quit()


def test_a_missing_own_folder_can_go_back_to_steam_from_the_empty_page(app_root, tmp_path, monkeypatch):
    """An own screenshot folder that is gone (drive unplugged) left the page empty with only "Anderen Ordner …" – the
    way back to Steam's folder was on the hidden tab."""
    from fogscout import steamshots
    from fogscout.app import App
    from fogscout.app_qt import ui_shown
    monkeypatch.setattr(steamshots, "steam_path", lambda: None)
    _settings(app_root, shots_folder=str(tmp_path / "gone"))
    app = App(str(app_root), simulate=str(app_root / "sim"))
    try:
        app.qt.show()
        app.qt.show_page("recordings")
        app._rec_render(force=True)
        app._qt_refresh(force=True)
        app.qapp.processEvents()
        btn = app.rec_empty_steam_btn
        assert not app.rec_nb.winfo_manager() and ui_shown(btn) and btn._dbdms_tip()
        assert "Eigener Ordner nicht gefunden" in app.shot_src_var.get()
        assert app.qt.forms["recordings"].controls[str(btn)][1].isVisible()          # in the window too
        btn.invoke()
        assert app.settings.get("shots_folder") == "" and not ui_shown(btn)
        assert not app.shot_steam_btn.winfo_manager()
    finally:
        app.quit()


def _clips_app(app_root, tmp_path, monkeypatch):
    """An App whose recordings folder holds a still, a GIF of the clip editor and a video clip."""
    import time
    from fogscout import obsrec
    from fogscout.app import App
    folder = str(tmp_path / "rec")
    cdir = os.path.join(folder, obsrec.CLIPS_DIR)
    os.makedirs(cdir)
    t = time.mktime((2026, 10, 17, 21, 40, 0, 0, 0, -1))
    Image.new("RGB", (64, 36)).save(os.path.join(cdir, "still.png"))
    for name in ("clip.gif", "clip.mp4"):
        with open(os.path.join(cdir, name), "wb") as fh:
            fh.write(b"\0" * 100)
    obsrec.save_clips(cdir, [obsrec.Clip(file="still.png", t=t, kind="still", label="Coal Tower", size=100),
                             obsrec.Clip(file="clip.gif", t=t + 1, kind="clip", label="Coal Tower", size=100),
                             obsrec.Clip(file="clip.mp4", t=t + 2, kind="clip", label="Coal Tower", size=100)])
    _settings(app_root, rec_on=True, rec_folder=folder)
    app = App(str(app_root), simulate=str(app_root / "sim"))
    monkeypatch.setattr(app.recorder, "folder", lambda: folder)
    return app


def test_a_still_opens_in_the_editor_from_the_row_menu_too(app_root, tmp_path, monkeypatch):
    """1.12 sent a still to the picture editor from the button, but the row menu kept "Im Editor öffnen …" grey."""
    app = _clips_app(app_root, tmp_path, monkeypatch)
    try:
        app._rec_render(force=True)
        app.clip_table.selection_set("still.png")
        app._clip_buttons()
        assert app.clip_edit_btn.cget("state") == "normal"
        assert ("edit", "Im Editor öffnen …", True) in app._clip_menu_items()
        opened = []
        app._shot_edit = opened.append
        app._clip_menu_act("edit")
        assert [os.path.basename(p) for p in opened] == ["still.png"]
    finally:
        app.quit()


def test_a_table_the_filters_empty_says_so(app_root, tmp_path, monkeypatch):
    """1.24.3 (phase 2 audit: a filter without a hit left an empty box): the clips table carries words for the
    empty state (Table draws them), only while there are clips and the filters hide all of them."""
    from fogscout.app_qt import ui_state
    app = _clips_app(app_root, tmp_path, monkeypatch)
    try:
        app._rec_render(force=True)
        assert app.clip_table.get_children() and app.clip_table._dbdms_empty == ""
        app.clip_role_var.set(dict(app._rec_roles)["killer"])           # no clip has a killer role
        app._clips_render()
        assert app.clip_table.get_children() == ()
        assert ui_state(app.clip_table)["empty"] == "Kein Clip passt zu den Filtern oben."
        app.clip_role_var.set(dict(app._rec_roles)["all"])
        app._clips_render()
        assert app.clip_table._dbdms_empty == ""
    finally:
        app.quit()


def test_obs_away_with_recordings_off_but_a_folder_keeps_the_next_step(app_root, tmp_path, monkeypatch):
    """1.24.6 (second review): with recording off but a folder set, F9 still records by hand – OBS away is amber
    (not red, not silent) and "Verbindung prüfen …" stays; the App hands the recorder's err on to the OBS line."""
    app = _clips_app(app_root, tmp_path, monkeypatch)
    try:
        app.settings.set("rec_on", False)
        app._rec_card_state({"connected": False, "error": "x"})
        assert app.rec_state_label._dbdms_level == "warn" and app.rec_obs_btn.winfo_manager()
        assert str(app.rec_f8_btn.cget("state")) == "disabled"                    # 1.24.7: a clip needs OBS too
        app._rec_card_state({"connected": True})
        assert str(app.rec_f8_btn.cget("state")) == "normal"
        app._rec_event("status", {"text": "OBS hat die Anmeldung abgelehnt – Passwort falsch?", "ok": False,
                                  "err": True})
        assert app.rec_status_label._dbdms_level == "err"
    finally:
        app.quit()


def test_a_gif_clip_is_not_offered_to_youtube(app_root, tmp_path, monkeypatch):
    """A GIF of the clip editor had an enabled YouTube button and menu entry that did nothing, without a word."""
    app = _clips_app(app_root, tmp_path, monkeypatch)
    added = []
    try:
        monkeypatch.setattr(app.youtube, "add", added.append)
        app.youtube._refresh = "ref"                                              # connected
        app._rec_render(force=True)
        app.clip_table.selection_set("clip.gif")
        app._clip_buttons()
        assert app.clip_yt_btn.cget("state") == "disabled"
        assert ("youtube", "Auf YouTube hochladen", False) in app._clip_menu_items()
        app._clip_youtube()
        assert added == []
        app.clip_table.selection_set("clip.mp4")                                  # a video still goes
        app._clip_buttons()
        assert app.clip_yt_btn.cget("state") == "normal"
        app._clip_youtube()
        assert [j.rel for j in added] == ["Clips/clip.mp4"]
    finally:
        app.quit()


class _ShotsOnly(RecordingsTab):
    """The screenshot list of the tab, without the App: settings and the recorder's folder."""

    def __init__(self, settings, folder):
        self.settings = settings
        self.recorder = type("Rec", (), {"folder": staticmethod(folder)})()


def test_an_own_folder_that_is_the_edit_folder_lists_each_picture_once(tmp_path, monkeypatch):
    """Own folder = the folder of the edited copies: every picture came twice (same path), a click on the second
    tile jumped back to the first."""
    from fogscout import steamshots
    monkeypatch.setattr(steamshots, "steam_path", lambda: None)
    _own_home(tmp_path, monkeypatch)
    rec = tmp_path / "rec"
    _pictures(rec / "Screenshots")
    tab = _ShotsOnly({"rec_on": True, "shots_folder": steamshots.edit_folder(str(rec))}, lambda: str(rec))
    assert [(os.path.basename(s.path), s.source) for s in tab._shots_list()] == [("20261025190000_1.jpg", "edited")]


def test_copies_edited_while_the_recordings_drive_was_away_stay_listed(tmp_path, monkeypatch):
    """A copy edited while the recordings drive was unplugged went to "Bilder/Fog Scout" and dropped out of the
    list once the drive was back."""
    from fogscout import steamshots
    monkeypatch.setattr(steamshots, "steam_path", lambda: None)
    _own_home(tmp_path, monkeypatch)
    rec = tmp_path / "rec"
    _pictures(rec / "Screenshots")
    present = {"on": False}
    tab = _ShotsOnly({"rec_on": True}, lambda: str(rec) if present["on"] else None)
    away = tab._shot_edit_dir()                                    # drive unplugged: copies go to "Bilder/Fog Scout"
    assert away == steamshots.edit_folder(None) and away.startswith(str(tmp_path))
    Image.new("RGB", (32, 18)).save(os.path.join(_mkdir(away), "away – bearbeitet.png"))
    present["on"] = True
    assert sorted(os.path.basename(s.path) for s in tab._shots_list() if s.source == "edited") == \
        ["20261025190000_1.jpg", "away – bearbeitet.png"]


def test_a_closed_editor_window_is_let_go(app_root, tmp_path):
    """The App kept the last closed editor in its list until the next one opened; a window whose Qt object is gone
    must not break the list."""
    import shiboken6
    from fogscout.app import App
    shots = _pictures(tmp_path / "shots")
    _settings(app_root, shots_folder=str(tmp_path / "shots"))
    app = App(str(app_root), simulate=str(app_root / "sim"))
    try:
        app._shot_edit(shots[0])
        win = app._clip_windows[-1]
        app._rec_tab_tick()
        assert app._clip_windows == [win]                          # open: kept
        win.close()
        app._rec_tab_tick()
        assert app._clip_windows == []                             # closed: let go at once
        app._shot_edit(shots[0])
        gone = app._clip_windows[-1]
        shiboken6.delete(gone)                                     # deleted on close (WA_DeleteOnClose)
        app._shot_edit(shots[0])
        assert len(app._clip_windows) == 1 and app._clip_windows[0] is not gone
        app._clip_windows[0].close()
    finally:
        app.quit()


def test_the_recording_card_text_follows_obs_state():
    """1.15 (audit of the video system): the card's three lines – state, values, warnings – from the poll."""
    from fogscout.app_recordings import rec_card_level, rec_card_text
    assert rec_card_text(None) == ("Warte auf OBS …", "", "")
    state, vals, warn = rec_card_text({"connected": False, "error": "Verbindung abgelehnt"})
    assert state == "OBS nicht erreichbar" and vals.endswith("Verbindung abgelehnt") and warn == ""
    base = {"connected": True, "recording": False, "paused": False, "seconds": 0.0, "bytes": 0, "ours": False,
            "buffer": True, "buffer_s": 20, "width": 2560, "height": 1440, "fps": 60.0, "encoder": "NVENC H.264",
            "disk_free": 500 * 1024 ** 3, "active_fps": 60.0}
    state, vals, warn = rec_card_text(base, clip_s=30)
    assert state == "Bereit · Wiederholungspuffer läuft (20 s)"
    assert vals == "2560×1440 · 60 fps · NVENC H.264 · 500 GB frei"
    assert "30 s eingestellt" in warn and "20 s" in warn                       # F8 longer than OBS's buffer
    assert rec_card_text(dict(base, buffer=None), clip_s=15)[0].endswith("nicht aktiviert")
    assert rec_card_text(dict(base, buffer=False), clip_s=15) [0].endswith("Wiederholungspuffer aus")
    rec = dict(base, recording=True, ours=True, label="Coal Tower", manual=True, seconds=61.0, bytes=3 * 1024 ** 2,
               marks=2, active_fps=58.0)
    state, vals, warn = rec_card_text(rec, extra_s=4.0, clip_s=15, now=1000.0, last_clip=("c.mp4", 940.0))
    assert state == "Nimmt auf · Coal Tower · von Hand gestartet · 01:05 · 3 MB · 2 Marken"   # 1.24.3: no ●/⚑
    assert vals == "2560×1440 · 60 fps (gerade 58) · NVENC H.264 · 500 GB frei · letzter Clip c.mp4 (vor 01:00)"
    assert warn == ""
    state = rec_card_text(dict(rec, paused=True), extra_s=4.0)[0]
    assert state.startswith("Pausiert") and "01:01" in state                   # the clock stands still
    assert "· 1 Marke" in rec_card_text(dict(rec, marks=1))[0]
    # 1.24.3 (phase 2): the line's colour (ui.level) – always with the words above
    assert rec_card_level(None, False) == "off" and rec_card_level(None, True) == ""
    assert rec_card_level({"connected": False}, True) == "err" and rec_card_level(rec, True) == "ok"
    assert rec_card_level(dict(rec, paused=True), True) == "warn"
    assert rec_card_level(dict(base, buffer=None), True) == "warn" and rec_card_level(base, True) == ""
    assert rec_card_level({"connected": False}, True, rec_on=False) == "warn"  # 1.24.6: off – F9 still needs OBS
    assert "von OBS selbst gestartet" in rec_card_text(dict(rec, ours=False))[0]
    warn = rec_card_text(dict(rec, output_skipped=20, output_total=1000, render_skipped=1, render_total=1000))[2]
    assert "lässt Bilder aus (20 von 1000" in warn and "Rendern" not in warn   # 0.1 % rendering: no warning
    assert "Rendern (50 von 1000" in rec_card_text(dict(rec, render_skipped=50, render_total=1000))[2]


def test_the_app_opens_the_new_editor_with_a_library_and_replaces_a_pristine_one(app_root, tmp_path, monkeypatch):
    """1.16: „Clip bearbeiten …“ opens qt_editor.EditorWindow; its library lists the folder's recordings and video
    clips (no stills, no GIFs) with marks, length and the round's name; a row opened from the library replaces the
    window while nothing was cut in it, else comes beside it; the compact editor's hand-over lands as one clip."""
    import subprocess
    import time
    from fogscout import obsrec
    from fogscout.qt_editor import EditorWindow
    FF = obsrec.ffmpeg_exe()
    if FF is None:
        pytest.skip("imageio-ffmpeg not installed")
    app = _clips_app(app_root, tmp_path, monkeypatch)
    folder = app.recorder.folder()
    t = time.mktime((2026, 10, 17, 21, 40, 0, 0, 0, -1))
    try:
        rec = os.path.join(folder, "2026-10-17 21-40 Coal Tower – Nurse.mkv")
        subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                        "testsrc=duration=4:size=320x180:rate=30", "-c:v", "libx264", "-preset", "veryfast",
                        "-pix_fmt", "yuv420p", rec], check=True, timeout=120)
        clip_mp4 = os.path.join(folder, obsrec.CLIPS_DIR, "clip.mp4")
        subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                        "testsrc=duration=2:size=320x180:rate=30", "-c:v", "libx264", "-preset", "veryfast",
                        "-pix_fmt", "yuv420p", clip_mp4], check=True, timeout=120)
        obsrec.save_index(folder, [obsrec.Recording(t=t, file=os.path.basename(rec), label="Coal Tower", role="killer",
                                                    killer="nurse", end=t + 4, size=1000, marks=[1.5])])
        items = app._media_items()
        kinds = sorted((it.kind, os.path.basename(it.path)) for it in items)
        assert kinds == [("clip", "clip.mp4"), ("round", os.path.basename(rec))]
        rnd = next(it for it in items if it.kind == "round")
        assert rnd.marks == [1.5] and rnd.seconds == pytest.approx(4.0) and rnd.round_t == t and "Coal Tower" in rnd.name
        app._rec_render(force=True)
        app.rec_table.selection_set(app.rec_table.get_children()[0])
        app._rec_clip(at=(1.0, 3.0, 2.0))
        win = app._clip_windows[-1]
        assert isinstance(win, EditorWindow) and win.path == rec
        from PySide6.QtWidgets import QApplication
        deadline = time.time() + 30                                     # 1.18.1: the hand-over waits for the lookup
        while time.time() < deadline and win._pstate == "loading":
            QApplication.instance().processEvents()
            time.sleep(0.01)
        assert [(p.start, p.end) for p in win.parts] == [(1.0, 3.0)] and win.pos == pytest.approx(1.0)
        assert win.library.model.rowCount() == 2 and win.library.model.current == os.path.normcase(os.path.abspath(rec))
        clip_item = next(it for it in items if it.kind == "clip")
        win._open_media(clip_item)                                      # cut here (the hand-over): a second window
        assert len(app._clip_windows) == 2 and app._clip_windows[-1].path == clip_item.path
        second = app._clip_windows[-1]
        second._open_media(rnd)                                         # pristine: replaced …
        app._rec_tab_tick()
        assert second not in app._clip_windows and app._clip_windows[-1].path == rec
        assert app._clip_windows == [win]                               # 1.18.1: … by the window open on it already
        app._rec_clip()                                                 # the same recording again: no second window
        assert app._clip_windows == [win]
        for w in list(app._clip_windows):
            w.close()
    finally:
        app.quit()


def test_marked_rounds_open_as_one_montage_listed_in_the_library(app_root, tmp_path, monkeypatch):
    """1.22 (user: „Mehrere Aufnahmen“ → Montage): two marked rounds → „Als Montage öffnen …“ makes one new montage,
    oldest first, one clip around each F8 mark; it is saved under Clips/Montagen, the library lists it and opening
    it there brings up the window open on it."""
    import subprocess
    import time
    from fogscout import obsrec, project
    from PySide6.QtWidgets import QApplication
    FF = obsrec.ffmpeg_exe()
    if FF is None:
        pytest.skip("imageio-ffmpeg not installed")
    app = _clips_app(app_root, tmp_path, monkeypatch)
    folder = app.recorder.folder()
    t = time.mktime((2026, 11, 2, 21, 0, 0, 0, 0, -1))
    try:
        recs = []
        for k, name in enumerate(("2026-11-02 21-00 Coal Tower – Nurse.mkv", "2026-11-02 21-30 Ormond – Wraith.mkv")):
            path = os.path.join(folder, name)
            subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                            "testsrc=duration=40:size=320x180:rate=30", "-c:v", "libx264", "-preset", "ultrafast",
                            "-pix_fmt", "yuv420p", path], check=True, timeout=120)
            recs.append(obsrec.Recording(t=t + 1800 * k, file=name, label=name[17:-4], role="killer", end=t + 1800 * k + 40,
                                         size=1000, marks=[25.0] if k == 0 else []))
        obsrec.save_index(folder, recs)
        app._rec_render(force=True)
        rows = app.rec_table.get_children()
        assert len(rows) == 2
        app.rec_table.selection_set(rows)
        items = app._rec_menu_items()
        assert [i[0] for i in items if i] == ["montage"]
        app._rec_menu_act("montage")
        win = app._clip_windows[-1]
        end = time.time() + 60
        while time.time() < end and len(getattr(win, "parts", [])) < 2:
            QApplication.instance().processEvents()
            time.sleep(0.01)
        assert win._montage and [os.path.basename(p) for p in win.sources] == [r.file for r in recs]
        assert [(p.src, p.start, p.end) for p in win.parts] == [(0, 5.0, 35.0), (1, 0.0, pytest.approx(40.0, abs=0.2))]
        mdir = os.path.join(folder, obsrec.CLIPS_DIR, project.MONTAGE_DIR)
        while time.time() < end and not (os.path.isdir(mdir) and os.listdir(mdir)):
            QApplication.instance().processEvents()
            time.sleep(0.01)
        lib = [it for it in app._media_items() if it.kind == "montage"]
        assert len(lib) == 1 and lib[0].recordings == 2 and lib[0].seconds == pytest.approx(70.0, abs=0.5)
        assert app._editor_for(win.path) is None                          # the round's own editor is another one
        app._editor_open(lib[0])
        assert app._clip_windows[-1] is win                               # open already: that window comes up
        for w in list(app._clip_windows):
            w._closing_asked = True
            w.close()
    finally:
        app.quit()


def test_the_recordings_page_reads_nothing_while_the_window_is_hidden(app_root, tmp_path):
    """1.22.4 (audit, prompt.md): the tab stays selected when the window goes to the tray – the index, the clips,
    the screenshots and OBS's state were read every few seconds for nobody. Shown again, it catches up at once."""
    from fogscout.app import App
    _settings(app_root, rec_on=True, rec_folder=_mkdir(str(tmp_path / "rec")))
    app = App(str(app_root), simulate=str(app_root / "sim"))
    try:
        renders, polls = [], []
        app._rec_render = lambda *a, **k: renders.append(1)
        app.recorder.poll = lambda: polls.append(1)
        app.nb.select(str(app.tab_recordings))
        app.qt.show()
        app.qt.hide()
        renders.clear()                                                   # the tab change renders once itself
        app._rec_dirty, app._rec_poll_t = True, 0.0
        app._rec_tab_tick()
        assert renders == [] and polls == []
        app.qt.show()
        app._rec_tab_tick()
        assert renders == [1] and polls == [1]
    finally:
        app.quit()


def test_a_click_is_handled_in_the_next_pass_of_the_event_loop(app_root):
    """1.22.4 (audit, prompt.md): a click waited for the next _poll (0–50 ms); now _qt_post asks for a pass at once
    – once, however many clicks come before it; posts from other threads keep the 50-ms beat."""
    import threading
    import time
    from fogscout.app import App
    _settings(app_root)
    app = App(str(app_root), simulate=str(app_root / "sim"))
    try:
        app._drain_events()
        timers, seen = [], []
        real_after, real_dispatch = app.root.after, app._dispatch
        app.root.after = lambda ms, fn: timers.append((ms, fn)) or real_after(ms, fn)
        app._dispatch = lambda ev: seen.append(ev) if ev[:2] == ("ui", "bench-click") else real_dispatch(ev)
        app._qt_post("bench-click", 1)
        app._qt_post("bench-click", 2)
        assert [ms for ms, _fn in timers] == [0]                         # one pass, at once
        timers[0][1]()                                                    # the pass the event loop runs
        assert [ev[2] for ev in seen] == [1, 2]                           # both, in order
        th = threading.Thread(target=app._qt_post, args=("bench-click", 3))
        th.start()
        th.join()
        assert [ms for ms, _fn in timers] == [0]                          # another thread: no timer from there
        app._drain_events()
        assert [ev[2] for ev in seen] == [1, 2, 3]
        # 1.23.1 (review): a slider or a drag posts on every mouse move – right after a refresh for a click, the
        # next post waits for the beat (no refresh per mouse move); after SOON_GAP_S a click comes at once again
        app._ui_refresh_t = time.monotonic()
        app._qt_post("bench-click", 4)
        assert [ms for ms, _fn in timers] == [0]
        app._drain_events()
        app._ui_refresh_t = time.monotonic() - 1.0
        app._qt_post("bench-click", 5)
        assert [ms for ms, _fn in timers] == [0, 0]
    finally:
        app.quit()


def test_a_double_click_plays_the_clip_and_two_marked_offer_a_montage(app_root, tmp_path, monkeypatch):
    """1.23 (audit, prompt.md): a row did nothing on double-click or Enter – it plays now (the Qt table posts
    ("open", row)); with two or more rows marked, „Als Montage öffnen …“ stands beside the buttons, not only in the
    right-click menu."""
    from fogscout.app_qt import ui_act, ui_state
    app = _clips_app(app_root, tmp_path, monkeypatch)
    try:
        app._rec_render(force=True)
        played = []
        app._open = played.append
        assert ui_state(app.clip_table)["open"] is True
        ui_act(app.clip_table, ("open", "clip.mp4"))
        assert app.clip_table.selection() == ("clip.mp4",) and [os.path.basename(p) for p in played] == ["clip.mp4"]
        assert not app.clip_montage_btn.winfo_manager()                 # one row: no montage button
        app.clip_table.selection_set(["clip.mp4", "clip.gif"])
        app._clip_buttons()
        assert app.clip_montage_btn.winfo_manager()
        app.clip_table.selection_set(["clip.mp4"])
        app._clip_buttons()
        assert not app.clip_montage_btn.winfo_manager()
        app.clip_table.selection_set(["clip.mp4", "clip.gif"])           # 1.23.1 (review): within a marking …
        ui_act(app.clip_table, ("open", "clip.gif"))
        assert app.clip_table.selection() == ("clip.gif",)                # … that row, not the first marked one
        assert [os.path.basename(p) for p in played] == ["clip.mp4", "clip.gif"]
    finally:
        app.quit()


def test_the_obs_card_does_not_repeat_its_title_in_the_reason():
    from fogscout.app_recordings import rec_card_text
    state, values, _warn = rec_card_text({"connected": False, "error": "OBS nicht erreichbar – läuft OBS, ist der "
                                          "WebSocket-Server an? (ConnectionRefusedError)"})
    assert state == "OBS nicht erreichbar" and values.endswith("Ursache: OBS läuft nicht, oder sein WebSocket-Server ist aus")   # 1.25: in words
    assert "läuft OBS" not in values
    _s, values, _w = rec_card_text({"connected": False, "error": "Passwort falsch"})
    assert values.endswith("Passwort falsch")                           # any other message stays as it is


def test_the_card_rates_the_recording_quality_and_a_click_sets_only_what_obs_takes(app_root, tmp_path, monkeypatch):
    """1.29 (user: "OBS-Aufnahmen mit guter Qualität"): 6 Mbit/s on 2560×1440@60 is mushy (red), the measurement
    stays after the recording; "Qualität verbessern …" asks before writing and hands only the plan to the recorder;
    the values before come back as "Zurücksetzen"."""
    app = _clips_app(app_root, tmp_path, monkeypatch)
    applied, restored = [], []
    monkeypatch.setattr(app.recorder, "apply_quality", applied.append)
    monkeypatch.setattr(app.recorder, "restore_quality", restored.append)
    base = {"connected": True, "mode": "Advanced", "encoder": "NVENC H.264", "encoder_raw": "jim_nvenc",
            "width": 2560, "height": 1440, "base_width": 2560, "base_height": 1440, "fps": 60.0, "rescale": "false"}
    try:
        app._rec_card_state(dict(base, recording=True, seconds=60.0, bytes=int(6e6 / 8 * 60)))
        assert "matschig" in app.rec_quality_var.get() and app.rec_quality_label._dbdms_level == "err"
        assert app.rec_quality_btn.winfo_manager() and not app.rec_quality_undo.winfo_manager()
        app._rec_card_state(dict(base, recording=False))
        assert "letzte Aufnahme" in app.rec_quality_var.get() and app.rec_quality_label._dbdms_level == "err"
        app.rec_quality_open()                                     # advanced, nothing a request can set: steps only
        title, text, retry = app._qt_question[:3]
        assert retry is None and "CQP" in text and not applied
        assert "Einschätzung aus Bitrate" in text                  # review F-07: an estimate, not a measurement
        app._rec_card_state(dict(base, recording=False, width=1920, height=1080))
        app.rec_quality_open()
        title, text, retry, ok_text = app._qt_question[:4]
        assert ok_text == "In OBS einstellen" and "2560×1440" in text and not applied
        app._confirmed = True
        retry()
        assert applied == [{"video": {"outputWidth": 2560, "outputHeight": 1440}}]
        before = {"video": {"outputWidth": 1920, "outputHeight": 1080}}
        app._rec_event("obs_quality", {"before": before})
        assert app.settings.get("rec_obs_before") == before and app.rec_quality_undo.winfo_manager()
        app._rec_event("obs_quality", {"before": {"video": {"outputWidth": 2560, "outputHeight": 1440},  # 2nd click
                                                  "profile": [("AdvOut", "RecRescale", "true")]}})
        assert app.settings.get("rec_obs_before") == {"video": {"outputWidth": 1920, "outputHeight": 1080},
                                                      "profile": [["AdvOut", "RecRescale", "true"]]}
        before = app.settings.get("rec_obs_before")
        app._confirmed = True
        app.rec_quality_restore()
        assert restored == [before]
        app._rec_event("obs_quality", {"done": True, "restore": True})
        assert app.settings.get("rec_obs_before") == {} and not app.rec_quality_undo.winfo_manager()
    finally:
        app.quit()


def test_an_option_that_needs_the_one_above_is_greyed_out_while_that_is_off(app_root, tmp_path, monkeypatch):
    """1.29.1 (user: "unübersichtlich, was gehört zu was"): the indented options of the OBS settings follow the one
    above them – greyed out while it is off, their value kept; a choice box comes back read-only, not editable."""
    app = _clips_app(app_root, tmp_path, monkeypatch)
    reg = app._qt_reg
    try:
        app.rec_window_var.set(False)
        app.rec_instant_var.set(False)
        app.rec_game_var.set(True)
        app._rec_setting()
        assert str(reg["st.more.rec_game"].cget("state")) == "disabled" and app.rec_game_var.get()
        assert str(reg["st.more.rec_clip"].cget("state")) == "disabled"
        app.rec_window_var.set(True)
        app.rec_instant_var.set(True)
        app._rec_setting()
        assert str(reg["st.more.rec_game"].cget("state")) == "normal"
        assert str(reg["st.more.rec_clip"].cget("state")) == "readonly"
    finally:
        app.quit()


def test_the_obs_snapshot_is_saved_when_taken_and_cleared_and_kept_when_the_restore_fails(app_root, tmp_path,
                                                                                         monkeypatch):
    """Review F-04: the values from before "In OBS einstellen" (rec_obs_before) are the only way back – setting and
    clearing them asks for a save at once (a crash before the next save lost them); the same values again write
    nothing; a restore that fails in OBS (no "done" event) keeps the snapshot, and so does the file."""
    import json
    from fogscout import obsrec
    app = _clips_app(app_root, tmp_path, monkeypatch)
    saves = []
    monkeypatch.setattr(app, "_save_soon", lambda: saves.append(1))
    try:
        before = {"video": {"outputWidth": 1920, "outputHeight": 1080}}
        app._rec_event("obs_quality", {"before": before})
        assert app.settings.get("rec_obs_before") == before and len(saves) == 1
        app._rec_event("obs_quality", {"before": before})               # nothing new: no second write
        assert len(saves) == 1
        app._rec_event("obs_quality", {"done": True, "restore": False})  # "In OBS einstellen" done: nothing to write
        assert len(saves) == 1 and app.settings.get("rec_obs_before") == before
        # a restore OBS refuses: the recorder posts no "done" – the snapshot stays, in memory and on disk
        posted = []
        rec = obsrec.Recorder(lambda kind, **d: posted.append((kind, d)))
        rec.cfg = obsrec.Config(on=True, port=1)                         # nothing listens there: OBS away
        with pytest.raises(obsrec.ObsError):
            rec._quality(dict(before, restore=True))
        assert not any(kind == "obs_quality" for kind, _d in posted)
        for kind, d in posted:                                            # whatever it said reaches the app
            app._rec_event(kind, d)
        assert app.settings.get("rec_obs_before") == before and len(saves) == 1
        app.settings.save()
        assert json.load(open(app.settings.path, encoding="utf-8"))["rec_obs_before"] == before
        app._rec_event("obs_quality", {"done": True, "restore": True})   # a restore that worked
        assert app.settings.get("rec_obs_before") == {} and len(saves) == 2
    finally:
        app.quit()
