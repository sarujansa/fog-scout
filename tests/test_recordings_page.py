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
    from fogscout.app_recordings import rec_card_text
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
    assert state == "● Nimmt auf · Coal Tower · von Hand gestartet · 01:05 · 3 MB · ⚑ 2 Marken"
    assert vals == "2560×1440 · 60 fps (gerade 58) · NVENC H.264 · 500 GB frei · letzter Clip c.mp4 (vor 01:00)"
    assert warn == ""
    state = rec_card_text(dict(rec, paused=True), extra_s=4.0)[0]
    assert state.startswith("⏸ Pausiert") and "01:01" in state                 # the clock stands still
    assert "von OBS selbst gestartet" in rec_card_text(dict(rec, ours=False))[0]
    warn = rec_card_text(dict(rec, output_skipped=20, output_total=1000, render_skipped=1, render_total=1000))[2]
    assert "lässt Bilder aus (20 von 1000" in warn and "Rendern" not in warn   # 0.1 % rendering: no warning
    assert "Rendern (50 von 1000" in rec_card_text(dict(rec, render_skipped=50, render_total=1000))[2]
