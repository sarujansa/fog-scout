"""1.46 (user: "Overlay-Steuerung grundlegend modernisieren … das Overlay-Fenster ist sehr klein"): the overlay
editor's App side – the list of elements (pick, eye, lock), the quick places, the lock in the preview and in the
game, the focus view, old settings without a lock, the switches that were never shown."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import layout, layoutmem  # noqa: E402

import test_uimodel  # noqa: E402

app_root = test_uimodel.app_root                 # the same fixture (a program folder with maps for the App)
GAME = (0, 0, 3440, 1440)


def _app(app_root):
    from fogscout.app import App
    app = App(str(app_root), simulate=str(app_root / "sim"))
    app._game_rect = lambda: GAME
    return app


def _layer(app, name):
    return {n: (x, y, w, h) for n, x, y, w, h in app._preview_data()["layers"]}.get(name)


def test_the_game_snap_distance_grows_with_the_game_picture():
    assert [layoutmem.snap_game_tol(h) for h in (1440, 1080, 2160, 200)] == [10, 8, 15, 4]
    # snap_on_screen without a tolerance takes the game's own one: 14 px off the centre snaps at 4K, not at 1080p
    big = layoutmem.snap_on_screen((0, 0, 3840, 2160), 0, [], (1920 - 50 - 14, 500, 100, 50))
    small = layoutmem.snap_on_screen((0, 0, 1920, 1080), 0, [], (960 - 50 - 14, 500, 100, 50))
    assert big[2] == 1920 and small[2] is None


def test_old_settings_get_no_locks_and_keep_every_place(app_root):
    """No new settings version: the defaults fill "locked"; positions and per-size layouts stay as they were."""
    old = {"settings_version": 13, "sysinfo": "custom", "sysinfo_pos": [0.98, 0.38],
           "overlay": {"anchor": "custom", "pos_x": 0.01, "pos_y": 0.2, "media_pos": "custom", "media_xy": [0.9, 0.8]},
           "layouts": {"3440x1440": {"overlay": {"anchor": "custom", "pos_x": 0.01}}}, "layout_key": "3440x1440"}
    with open(app_root / "settings.json", "w", encoding="utf-8") as fh:
        json.dump(old, fh)
    app = _app(app_root)
    try:
        o = app.settings["overlay"]
        assert o["locked"] == [] and app._locked_names() == set()
        assert (o["anchor"], o["pos_x"], o["pos_y"], o["media_xy"]) == ("custom", 0.01, 0.2, [0.9, 0.8])
        assert app.settings["sysinfo_pos"] == [0.98, 0.38] and app.settings["layouts"]["3440x1440"]["overlay"]
        o["locked"] = "map"                                  # a hand-edited, broken value: nothing locked
        assert app._locked_names() == set()
        o["locked"] = ["map", "nonsense"]
        assert app._locked_names() == {"map"}
    finally:
        app.quit()


def test_the_list_picks_shows_hides_and_locks_through_the_known_switches(app_root):
    from fogscout.app_qt import ui_shown
    app = _app(app_root)
    try:
        for key in ("ov.master", "ov.small_off", "ov.per_size_hint"):       # were registered but never shown
            assert ui_shown(app._qt_reg[key]), key
        data = app._elements_data()
        assert data["order"] == ["map", "text", "hud", "today", "music", "inputs"]
        assert data["rows"]["map"]["shown"] and not data["rows"]["inputs"]["shown"]
        assert not data["rows"]["text"]["can_hide"] and data["rows"]["map"]["place"] == "automatisch"
        app._elements_act(("select", "music"))
        assert app._sel == "music" and app._elements_data()["selected"] == "music"
        app._elements_act(("show", "music", False))
        assert app.settings["overlay"]["show_media"] is False and not app.media_var.get()
        app._elements_act(("show", "music", True))
        assert app.settings["overlay"]["show_media"] is True
        side = app.settings["sysinfo"]
        app._elements_act(("show", "hud", False))
        assert app.settings["sysinfo"] == "off"
        app._elements_act(("show", "hud", True))
        assert app.settings["sysinfo"] == side                                 # back where it was
        app._elements_act(("show", "map", False))
        assert app.settings["overlay"]["show_map"] is False
        app._elements_act(("show", "map", True))
        app._elements_act(("lock", "today", True))
        assert app.settings["overlay"]["locked"] == ["today"] and app._elements_data()["rows"]["today"]["locked"]
        app._elements_act(("lock", "today", False))
        assert app.settings["overlay"]["locked"] == []
        app._elements_act(("lock", "nonsense", True))
        assert app.settings["overlay"]["locked"] == []
    finally:
        app.quit()


def test_a_locked_element_is_not_moved_in_the_preview_but_can_be_put_back(app_root):
    app = _app(app_root)
    try:
        o = app.settings["overlay"]
        app.toggle_edit()
        app._lock_toggle("music", True)
        before = (o["media_pos"], list(o["media_xy"]))
        app._preview_pick(("place", "music", 100, 100))
        app._select("music")
        app._preview_pick(("nudge", 10, 0))
        app._preview_pick(("resize", "music", 10 ** 6))
        app._anchor_cell(("cell", 0, 0))
        assert (o["media_pos"], list(o["media_xy"])) == before and o.get("media_scale", 1.0) == 1.0
        assert app._anchors_data()["enabled"] is False and app._preview_data()["locked"] == ["music"]
        app._lock_toggle("music", False)
        app._preview_pick(("place", "music", 100, 100))
        assert o["media_pos"] == "custom"
        app._lock_toggle("music", True)
        app._el_reset("music")                                 # the usual place: allowed while locked
        assert o["media_pos"] != "custom"
        app.toggle_edit()
    finally:
        app.quit()


def test_a_locked_window_stays_click_through_while_moving(app_root):
    """In the game: the windows of locked elements are not made grabbable (Qt overlay: transparent for input)."""
    from PySide6.QtCore import Qt
    app = _app(app_root)
    try:
        app.toggle_edit()
        assert app.overlay.editing and app.overlay.grabbable()
        app._lock_toggle("map", True)
        assert app.overlay.editing and not app.overlay.grabbable()          # the moving mode stays on
        if hasattr(app.overlay, "win"):                                    # QtOverlay (Linux)
            assert app.overlay.win.windowFlags() & Qt.WindowTransparentForInput
        app._lock_toggle("map", False)
        assert app.overlay.grabbable()
        app._lock_toggle("map", True)
        app.toggle_edit()
        app.toggle_edit()                                                  # on again: still locked
        assert not app.overlay.grabbable()
        assert app._el_editable("hud") and not app._el_editable("map")
        app.toggle_edit()
        assert not app._el_editable("hud")
    finally:
        app.quit()


def test_the_quick_places_put_every_kind_of_element_where_it_says(app_root):
    """Map corners = its preset anchors; map edges/centre, system values and cards = own places at the cell (with
    the margin) – each one undo step; the grid shows the cell the element is at."""
    app = _app(app_root)
    try:
        o = app.settings["overlay"]
        m = int(GAME[3] * o["margin"])
        app._select("map")
        assert app._anchors_data()["cell"] == "auto"
        app._anchor_cell(("cell", 2, 2))
        assert o["anchor"] == "bottom-right" and app._anchors_data()["cell"] == (2, 2)
        app._anchor_cell(("cell", 1, 0))
        assert o["anchor"] == "custom"
        x, y, w, h = _layer(app, "map")
        assert abs(x + w / 2 - GAME[2] / 2) <= 3 and abs(y - m) <= 10     # the map refits to its room there
        assert app._anchors_data()["cell"] == (1, 0)
        app._select("hud")
        app._anchor_cell(("cell", 0, 2))
        assert app.settings["sysinfo"] == "custom"
        x, y, w, h = _layer(app, "hud")
        assert abs(x - m) <= 3 and abs(y + h - (GAME[3] - m)) <= 3
        app._select("music")
        app._anchor_cell(("cell", 2, 1))
        assert o["media_pos"] == "custom"
        x, y, w, h = _layer(app, "music")
        assert abs(x + w - (GAME[2] - m)) <= 3 and abs(y + h / 2 - GAME[3] / 2) <= 3
        assert app._anchors_data()["cell"] == (2, 1)
        assert layout.own_places(o, app.settings["sysinfo"]) >= {"hud", "music"}
        app.undo_layout()                                      # one step each
        assert o["media_pos"] != "custom"
        app._anchor_cell(("auto",))                            # music is picked: back to its usual place
        app._select("hud")
        app._anchor_cell(("auto",))
        assert app.settings["sysinfo"] != "custom"
    finally:
        app.quit()


def test_focus_ends_when_the_overlay_page_is_left(app_root):
    app = _app(app_root)
    try:
        calls = []
        app.qt.set_focus_nav = lambda on: calls.append(on)
        app.qt.show_page("overlay")
        app._qt_post("act", ("ov.focus_mode", None))           # the button on the page
        app._drain_events()
        assert app._editor_focus and calls[-1] is True
        from fogscout.app_qt import ui_state
        assert ui_state(app._qt_reg["ov.focus_mode"])["pressed"] is True
        assert ui_state(app._qt_reg["ov.edit"])["pressed"] is False
        app._qt_post("page", "stats")
        app._drain_events()
        assert not app._editor_focus and calls[-1] is False
    finally:
        app.quit()
